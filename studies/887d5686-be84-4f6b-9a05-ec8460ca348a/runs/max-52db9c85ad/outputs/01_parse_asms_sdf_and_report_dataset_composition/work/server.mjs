#!/usr/bin/env node
/**
 * modulon-max: the Claude Agent SDK as a Rayca engine.
 *
 * WHAT THIS IS. Claude Code's loop does the reasoning. The Rayca platform provides the hands -- 799 containerised
 * tools, 92 Nextflow pipelines, the memory stack, 122 personas, both HPC clusters -- published over MCP by
 * `rayca_mcp_server.py`. Events are published in a shape native to how this loop actually behaves rather than
 * translated onto the flat tape the previous engine needed.
 *
 * WHAT IT REPLACES, MEASURED: executor.py (4,095 lines), dispatch.py (2,047), phases.py (989), contract.py (481),
 * toolcontract.py (438), contractadapt.py (419), recovery.py (450), fastpath.py (401), teamtool.py (392). About 9,700
 * lines, near 13% of the Python. Everything else -- governance, registries, memory, lineage, workspaces, credentials --
 * is kept and mounted, not ported.
 *
 * GOVERNANCE IS WIRED, in the `PreToolUse` hook rather than in `canUseTool`, because the SDK warns that
 * `bypassPermissions` auto-approves every tool call and never invokes that callback. A gate a permission mode can
 * switch off is not a gate. Gates, credit pricing, provenance and claim judging all run through
 * `governance_bridge.py`, which calls the platform's existing Python rather than reimplementing any of it.
 *
 * ISOLATION. Own port, own database, own process. Nothing here touches the engine on 8201 or the console.
 */

import { createServer } from 'node:http';
import { readFileSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { query, listSessions, forkSession, getSessionInfo, listSubagents, getSubagentMessages }
  from '@anthropic-ai/claude-agent-sdk';
import { KINDS, failedInside, producedNothing, nameAndOrigin } from './events.mjs';
import { newTaskTable, noteTask, taskPhases, taskCounts } from './tasks.mjs';
import { Store } from './store.mjs';
import { buildManifest, readManifest, rehydrationFrom, stopDecision, writeManifest } from './manifest.mjs';
import { rankPersonas, loadPersonas } from './personas.mjs';
import { governance } from './governance.mjs';
import { platformStore } from './runstore.mjs';
import { fallbackModels, fetchRouterModels } from './models.mjs';
import { fetchRouterPrices, costOf } from './pricing.mjs';
import { prefetch as memoryPrefetch, scriptSlug } from './memory.mjs';
import { Readable } from 'node:stream';
import { resolveAttachments, sessionWorkspace } from './attachments.mjs';
import { userPromptEvent, withPromptAttachments, toConsoleEvent, dispatchesIn, toJobEvent, toJobSubmittedEvent, clusterJobIn, toClusterJobEvent, OPS_SCHEMA_VERSION, workflowFrom, captionFrom } from './consoleapi.mjs';
import { publicFailure } from './publicfailure.mjs';
import { resolveEnv } from './env.mjs';

// The ONE place environment is decided. Default is production, so an unset RAYCA_ENV can never silently
// run the dev tree against the production database. See env.mjs for the reasoning and the profile table.
const ENV = resolveEnv();

const HERE = dirname(fileURLToPath(import.meta.url));
const PORT = ENV.port;
const SRC = ENV.src;
const PY = ENV.py;
const MCP = join(HERE, 'rayca_mcp_server.py');

/** The conversation a run belongs to, which is the key every file endpoint uses. */
function consoleSessionFor(runId) {
  try {
    return store.getRun(runId)?.console_session || '';
  } catch {
    return '';
  }
}
const MODEL = process.env.RAYCA_MODEL || 'claude-sonnet-4-6';

/*
 * WHICH MODELS A SELECTION MAY NAME. The reasoning, and the defect that forced it, are in models.mjs.
 */
let AVAILABLE_MODELS = fallbackModels(MODEL);

/*
 * WHAT A RUN IS ALLOWED TO SPEND, IN REAL DOLLARS.
 *
 * MEASURED: a Qwen3 run recorded $15.1690 against a $15 cap while the router's ledger for the same window shows $0.9437.
 * The SDK prices from a Claude-only table, so the cheapest model in the fleet exhausted the budget fastest. The full
 * measurement is in pricing.mjs.
 *
 * SO THE LIMIT IS ENFORCED HERE, on a figure computed from the router's prices, and the SDK's own budget is kept only as
 * a runaway backstop far above it. One enforcement path for every model: for Claude the two figures agree so nothing
 * changes, and for anything else this is the only one that is right.
 */
const BUDGET_USD = Number(process.env.MAX_BUDGET_USD || 30);
const SDK_BUDGET_BACKSTOP = 50;
let PRICES = {};

/** Ask the router for its per-token prices. Never throws: stale prices beat a broken start. */
async function refreshPrices() {
  try {
    const next = await fetchRouterPrices({
      baseUrl: process.env.ANTHROPIC_BASE_URL,
      key: process.env.ANTHROPIC_AUTH_TOKEN || process.env.ANTHROPIC_API_KEY || '',
    });
    if (next) {
      PRICES = next;
      console.error('[pricing] priced models=%d budget=$%s', Object.keys(next).length, BUDGET_USD);
    } else {
      console.error('[pricing] router published no prices, keeping %d', Object.keys(PRICES).length);
    }
  } catch (e) {
    console.error('[pricing] router prices failed, keeping %d: %s',
      Object.keys(PRICES).length, String((e && e.message) || e));
  }
  return PRICES;
}

/**
 * The real cost of a result message, and the figure the SDK claimed, so a divergence is visible rather than assumed.
 *
 * Falls back to the SDK's number only when nothing could be priced, because an unpriced model must not read as free.
 */
function realCostOf(msg) {
  const claimed = Number(msg?.total_cost_usd ?? 0) || 0;
  const out = costOf(msg?.modelUsage, PRICES);
  if (out.unpriced.length) {
    console.error('[pricing] no price for %s, falling back to the SDK figure',
      out.unpriced.map((u) => u.model).join(', '));
  }
  return { usd: out.complete ? out.usd : claimed, claimed, complete: out.complete };
}

/** Replace the selectable set from the router. Never throws: a stale set beats a broken start. */
async function refreshAvailableModels() {
  try {
    const next = await fetchRouterModels({
      baseUrl: process.env.ANTHROPIC_BASE_URL,
      key: process.env.ANTHROPIC_AUTH_TOKEN || process.env.ANTHROPIC_API_KEY || '',
      configured: MODEL,
    });
    if (!next) {
      console.error('[models] router listed nothing usable, keeping %d selectable', AVAILABLE_MODELS.length);
      return AVAILABLE_MODELS;
    }
    const added = next.filter((m) => !AVAILABLE_MODELS.includes(m));
    AVAILABLE_MODELS = next;
    console.error('[models] selectable=%d%s', next.length, added.length ? ' added ' + added.join(', ') : '');
  } catch (e) {
    console.error('[models] router listing failed, keeping %d selectable: %s',
      AVAILABLE_MODELS.length, String((e && e.message) || e));
  }
  return AVAILABLE_MODELS;
}

/**
 * The model a request asked for, or the configured one.
 *
 * MEASURED DEFECT THIS FIXES. `MODEL` was a module constant used everywhere, and NOTHING read a model from the request:
 * the console's settings control sent one and its own comment claimed "engine receives model/temperature in the request
 * body", while every route ignored it. Two consecutive sessions on different selections both ran claude-sonnet-4-6, and
 * the stored `model` column asserted sonnet either way, which is worse than having no control at all because the record
 * was confidently wrong about what ran.
 */
function modelFrom(body) {
  const asked = String(body?.model || '').trim();
  if (!asked) return MODEL;
  /* `auto` is offered by the catalogue and is not a deployment name. It means "let the platform choose", and the
     platform's choice is its configured model, so it resolves here instead of failing the includes test and arriving at
     the same place by accident. */
  if (asked.toLowerCase() === 'auto') return MODEL;
  return AVAILABLE_MODELS.includes(asked) ? asked : MODEL;
}

/**
 * The sampling temperature a request asked for, if it is one.
 *
 * Returns undefined rather than a default, so the SDK's own default stands when nothing was asked. Out of range values
 * are dropped rather than clamped: silently running at 1.0 because 2.5 was requested is a quiet lie about the run.
 */
function temperatureFrom(body) {
  const t = Number(body?.temperature);
  return Number.isFinite(t) && t >= 0 && t <= 1 ? t : undefined;
}
const DB = ENV.db;
const BIND = ENV.bind;
const SERVE_KEY = process.env.RAYCA_SERVE_KEY || '';
const UPSTREAM = (process.env.RAYCA_UPSTREAM_ENGINE || 'http://127.0.0.1:8201').replace(/\/+$/, '');

/**
 * AUTHENTICATION, BECAUSE THIS ENGINE RUNS ARBITRARY CODE AND SPENDS REAL MONEY.
 *
 * It executes Python, dispatches containers on a GPU host, submits jobs to two national supercomputers and bills a
 * Bedrock account. Until now it was only safe because it bound to 127.0.0.1, which is not a security control -- it is
 * an accident of configuration that the next person to widen the bind would silently remove. The console reaches its
 * engine at `host.docker.internal:8201` from inside a container, so a wider bind IS needed, and the operator engine
 * already answers 401 to an unauthenticated request. This matches it rather than inventing a second scheme.
 *
 * REFUSES TO SERVE WIDELY WITHOUT A KEY. If the bind is not loopback and no key is configured, the process exits
 * instead of starting: an engine like this being reachable unauthenticated is worse than an engine that is down.
 */
function authorised(req) {
  if (!SERVE_KEY) return true; // loopback-only, and the bind is refused below if that is not true
  const h = String(req.headers.authorization || '');
  const got = h.startsWith('Bearer ') ? h.slice(7).trim() : '';
  // Length-independent comparison is not warranted here: the key is not derived from user input and the endpoint is
  // not a timing oracle for anything. Naming that is better than implying a protection this does not have.
  return got !== '' && got === SERVE_KEY;
}

const store = new Store(DB);
const PERSONAS = loadPersonas();
const live = new Map(); // run_id -> { listeners, queue, n }

/* ------------------------------------------------------------------------------------------------------------------
 * An input channel that stays open, so a researcher can steer without killing the run
 * ---------------------------------------------------------------------------------------------------------------- */

/**
 * MEASURED NEED. During the PD-L1 run the operator asked to continue with 5 backbones instead of 40, and there was no
 * way to say so: the prompt had been passed as a fixed string, so the only options were to let it run or to kill it.
 * We killed it. The SDK accepts `AsyncIterable<SDKUserMessage>` for exactly this, and mid-run intervention was on the
 * operator's original list of things the platform must do.
 */
class InputChannel {
  constructor(first) {
    this.pending = [first];
    this.closing = false;
    this.wake = null;
  }

  push(text) {
    this.pending.push(text);
    if (this.wake) { this.wake(); this.wake = null; }
    return true;
  }

  /** Called when the loop reports a result. The channel drains anything queued before closing. */
  finish() {
    this.closing = true;
    if (this.wake) { this.wake(); this.wake = null; }
  }

  async *[Symbol.asyncIterator]() {
    for (;;) {
      while (this.pending.length) {
        const text = this.pending.shift();
        yield {
          type: 'user',
          message: { role: 'user', content: [{ type: 'text', text }] },
          parent_tool_use_id: null,
          session_id: '',
        };
      }
      if (this.closing) return;
      await new Promise((r) => { this.wake = r; });
    }
  }
}

/* ------------------------------------------------------------------------------------------------------------------
 * Running a task
 * ---------------------------------------------------------------------------------------------------------------- */

/*
 * ONE TASK TABLE PER RUN, and the snapshot that publishes it.
 *
 * KEYED BY RUN, not global, because two runs can be in flight and their plans are different studies. Dropped when the run ends,
 * for the same reason the workspace map is bounded: a server that remembers every table for ever is a leak with a plan in it.
 *
 * THE TAPE IS THE STATE. Nothing here is the source of truth after the fact: each snapshot is emitted as an ordinary event, so a
 * reloaded page reads the plan from the tape like everything else and the last snapshot wins. That is what makes the panel
 * correct after a refresh without this process having to be asked.
 */
const taskTables = new Map();
/* How many times each run has been soft-blocked at Stop. Bounded by the run's own lifetime, and the reason
   it exists is in `stopDecision`: a run that has been asked twice must be able to finish. */
const stopBlocks = new Map();
/* Advisories delivered per run, capped for the same reason blocks are: anything this hook returns re-prompts. */
const stopAdvisories = new Map();

/**
 * The phase a file produced right now belongs to, from the run's own task table.
 *
 * WS-30 T7, closing the half of T1 that was left open. `filing.folder_for` has taken a `phase` and a
 * `phase_index` all along, and `filereg.register_new` accepts them, and the live path passed NEITHER.
 * MEASURED on run max-604740ffad: all 43 produced records carried no phase, so every file landed in a
 * bare role folder and nothing in the run could be attributed to a phase. Obligations key on a phase, so
 * without this they could only ever be run-wide.
 *
 * THE FIRST PHASE NOT DONE, which is the same rule `manifest.currentPhase` uses and for the same reason:
 * the SDK's task list is the only thing that actually knows a phase's state, so it is believed rather
 * than inferred from event tags.
 *
 * Returns nulls rather than guesses when there is no plan. A file produced before any task exists has no
 * phase, and inventing `01_` for it would put unplanned work in a folder that claims otherwise.
 */
/**
 * Every container image this run has dispatched, from the tape.
 *
 * WS-30 T9. THE REPORT COULD NOT NAME AN IMAGE WITHOUT THIS, and an unnamed image makes the whole
 * `container_doc` obligation decorative: it is settled by a document containing `Container Image:`, and the
 * renderer can only write that line if something hands it a value.
 *
 * MEASURED: the workflow method records the report is built from carry no `image` field at all, while the
 * 50 `job.submitted` events on run max-604740ffad carry agent, at, gpu, host, image, kind and tool. The
 * fact exists; it was simply on the other side of the boundary. This is the side that has the tape.
 */
function containerImagesFor(runId) {
  try {
    const seen = [];
    for (const ev of store.eventsFor(runId) || []) {
      const image = String((ev && ev.image) || '');
      if (image && !seen.includes(image)) seen.push(image);
    }
    return seen;
  } catch {
    return [];
  }
}

function currentPhaseFor(runId) {
  try {
    const phases = taskPhases(taskTableFor(runId)) || [];
    const open = phases.find((p) => p.state !== 'done' && p.state !== 'completed');
    if (!open) return { phase: '', phaseIndex: null };
    return { phase: String(open.goal || ''), phaseIndex: Number(open.index) };
  } catch {
    return { phase: '', phaseIndex: null };
  }
}

function taskTableFor(runId) {
  let table = taskTables.get(runId);
  if (!table) {
    table = newTaskTable();
    taskTables.set(runId, table);
  }
  return table;
}

/** Record one task signal and, only if the table actually changed, put the whole plan on the tape. */
/* Released when the run is finalised. The tape keeps the plan; this process has no reason to. */
function releaseTaskTable(runId) {
  // RELEASED WITH THE TABLE. Without this the set of reported phases outlives every run on a long lived process.
  reportedPhases.delete(runId);
  taskTables.delete(runId);
  /* AND THE STOP COUNTER, or this map grows for the lifetime of a service that runs for days. Same reason
     the workspace map below is bounded: an unbounded map in a long-lived process is a slow leak. */
  stopBlocks.delete(runId);
  stopAdvisories.delete(runId);
}

/**
 * Read a task tool's own input as a status signal.
 *
 * NAMED BY SUFFIX rather than by an exact list, because these tools arrive with an MCP prefix on some paths and bare on others,
 * and a hand written list of the spellings would be a cage that breaks the first time one of them changes.
 */
/**
 * Remember a cluster job if this tool output announced one. Safe to call for every result: it does nothing when there is no job.
 *
 * ONE RECORDER, called from the run loop where the result actually arrives, and reused by the stream handler so the two cannot
 * record different things. A 12 hour job outlives the run that submitted it, and this record is what lets the watcher follow it
 * and what tells collection where the results belong.
 */
function rememberClusterJobFrom(runId, output) {
  const cj = clusterJobIn(output);
  if (!cj) {
    return null;
  }
  try {
    store.rememberClusterJob({
      jobId: cj.jobId, runId, consoleSession: consoleSessionFor(runId),
      cluster: cj.cluster, provider: cj.provider, host: cj.host,
      state: cj.state, schedulerState: cj.schedulerState,
      resultsInto: workspaceOf(runId),
    });
  } catch {
    /* Following a job is a bonus; failing to record one must not break the run that submitted it. */
  }
  return cj;
}

function noteTaskFromTool(runId, toolName, input) {
  const name = String(toolName || '');
  if (!/Task(Create|Update)$/.test(name) || !input || typeof input !== 'object') {
    return;
  }
  noteAndPublishTask(runId, {
    id: input.taskId ?? input.task_id ?? input.id,
    subject: input.subject ?? input.description ?? input.activeForm,
    status: input.status,
    needs: Array.isArray(input.addBlockedBy) ? input.addBlockedBy : undefined,
  });
}

/**
 * Phases already reported as done, per run, so one report is written per phase and not one per task signal.
 *
 * `noteAndPublishTask` fires on every task update, and a phase stays `done` for the rest of the study, so without this
 * the same report would be rewritten on each later signal. That is exactly the per step frequency the operator asked to
 * remove: "it should not be this frequent as now! maybe after each phase".
 */
const reportedPhases = new Map();

function noteAndPublishTask(runId, signal) {
  const table = taskTableFor(runId);
  if (!noteTask(table, signal)) {
    return;
  }
  const phases = taskPhases(table);
  emit(runId, KINDS.PLAN, { phases, counts: taskCounts(table) });
  /*
   * ONE MARKDOWN REPORT PER PHASE, WRITTEN WHEN THAT PHASE FINISHES.
   *
   * THE OPERATOR: "the files you generated and put into Report folder as .txt, they are useless to the user. very
   * fragmented and ugly ... make them beautiful MD files explaining each step methods and results section with beautiful
   * tables", and "maybe after each phase".
   *
   * HERE, because `taskPhases` is the only thing that knows a phase's state and this is the only place it changes. My
   * first attempt hooked the Python executor, which max REPLACES for every study it runs, so it fired for nothing:
   * measured on two real runs, no report and no log line either.
   *
   * FIRE AND FORGET. A report is documentation and must never delay or fail a study.
   */
  try {
    const sessionKey = consoleSessionFor(runId) || runId;
    if (!sessionKey) {
      return;
    }
    let done = reportedPhases.get(runId);
    if (!done) {
      done = new Set();
      reportedPhases.set(runId, done);
    }
    for (const phase of phases || []) {
      const id = String(phase?.id ?? phase?.goal ?? '');
      if (!id || phase?.state !== 'done' || done.has(id)) {
        continue;
      }
      done.add(id);
      platformStore
        // The report names the model that produced the phase, read back from the run rather than assumed.
        .phaseReport({ session: sessionKey, runId, phase, images: containerImagesFor(runId), model: store.getRun(runId)?.model || MODEL })
        .then((path) => {
          if (!path) {
            console.error('[report %s] phase "%s" produced no file', runId, id.slice(0, 40));
          }
        })
        .catch((e) => console.error('[report %s] phase "%s" failed: %s', runId, id.slice(0, 40),
          String(e && e.message || e)));

        /*
         * AND THE STEP IS PUSHED, IF A REPOSITORY IS BOUND. WS-30 T11.
         *
         * THE OPERATOR corrected me on this. I had it as a non-goal, reasoning that a researcher's workspace
         * is not a repository: "it is good to have when researcher connect the session to their github and
         * wamts to push after each step." They were right, and the mechanism already existed -- this same
         * function has run once per RUN from the finaliser since it was written.
         *
         * A SESSION WITH NOTHING BOUND COSTS ONE SUBPROCESS AND SAYS NOTHING. `autoPushToGitHub` returns
         * silently on `no_repo` and `no_credential`, deliberately, because "announcing it on every run would
         * train the reader to ignore this event". So there is no repository lookup to invent here: the
         * ABSENCE of a `publish` event is itself the evidence that nothing is bound, and that is what
         * `commit_step` keys on.
         *
         * FIRE AND FORGET, like the report above it. A push is a record of the work and not the work, and
         * `autoPushToGitHub` already never fails a run.
         */
        void autoPushToGitHub(runId, sessionKey, 'phase complete', {
          message: `Step ${id}: ${String(phase?.goal || 'phase complete').slice(0, 68)}`,
          step: id,
        });
    }
  } catch (e) {
    console.error('[report %s] could not schedule a phase report: %s', runId, String(e && e.message || e));
  }
}

function emit(runId, kind, data) {
  const rec = live.get(runId);
  // KIND LAST, DELIBERATELY. Spreading the payload first let a field called `kind` overwrite the event's own kind:
  // `emit(id, KINDS.GATE, { kind: 'governance' })` was stored as kind `governance`, so every reader filtering on
  // `gate` saw nothing and the governance events looked absent when they had been recorded all along. Measured on
  // run max-3100df7dcf.
  const ev = { at: Date.now(), ...data, kind };
  const n = rec ? rec.n++ : store.countEvents(runId);
  store.appendEvent(runId, n, ev);
  if (rec) {
    for (const send of rec.listeners) {
      try { send(ev); } catch { /* a dead reader must never stop a run */ }
    }
  }
  return ev;
}

function agentDefinitionsFor(task, runId, n = 4) {
  const chosen = rankPersonas(PERSONAS, task, n);
  const agents = {};
  for (const p of chosen) {
    agents[p.id] = {
      description: p.summary || p.name,
      // A MEMBER WITHOUT THE PLATFORM IS A SEARCH ENGINE. Measured: with only the parent's server named by string, a
      // member issued seventy WebFetch calls and touched no platform verb, at $3.51 for one run. The full record is
      // what actually reaches the 799 tools from inside a member.
      // EACH MEMBER'S SERVER IS LABELLED WITH THE PERSONA IT SERVES, and reports back to this engine. That label is
      // the only reliable way to attribute a tool call to a member: `SubagentStop` did not fire within four minutes on
      // a working member and `getSubagentMessages` returned nothing usable, so nothing the SDK exposes could tell us
      // who ran what. The server that served the call always knows.
      mcpServers: [{ rayca: { type: 'stdio', command: PY, args: [MCP],
        env: { RAYCA_SRC: SRC, PYTHONPATH: SRC, RAYCA_USER_ID: process.env.RAYCA_USER_ID || '',
          /*
           * A MEMBER WRITES INTO THE SAME CONVERSATION AS ITS LEAD, and leaving this out lost every specialist's files.
           *
           * `rayca_mcp_server.py` reads RAYCA_SESSION_ID and falls back to the literal string 'modulon-max' when it is
           * absent. The lead's environment sets it (see the lead's mcpServers block below); the member's did not. So a
           * specialist's files registered under a session no console has ever queried, in workspace_for('modulon-max'),
           * a directory nobody reads. The operator: "no files are generating on the file manager ... it is like some files
           * are not getting saves there." They were right, and it was not latency: the files were filed to a stranger.
           */
          RAYCA_SESSION_ID: consoleSessionFor(runId) || runId,
          RAYCA_MAX_CALLBACK: `http://127.0.0.1:${PORT}/max/tool`, RAYCA_RUN_ID: runId, RAYCA_AGENT: p.id,
          // WITHOUT THIS THE CALLBACK IS REJECTED. server.mjs opens only /healthz and /max/health; everything
          // else needs the bearer key, and this server posts its tool reports, progress beats and file
          // announcements back over HTTP. MEASURED: a POST to /max/file returned 401 "unauthorised" and the
          // Python side swallows failures by design, so the loss was silent.
          RAYCA_SERVE_KEY: SERVE_KEY || '' } } }],
      tools: ['mcp__rayca__run_python', 'mcp__rayca__inspect_environment', 'mcp__rayca__list_pipelines',
        'mcp__rayca__run_pipeline', 'mcp__rayca__list_compute', 'mcp__rayca__run_on_cluster', 'Read', 'Write'],
      prompt: [
        `You are the ${p.name}.`,
        p.summary ? `Your remit: ${p.summary}.` : '',
        'Use the rayca tools for anything you assert as a measurement. If you did not compute a number, say so',
        'rather than supplying one. Report disagreement with other members plainly; do not smooth it over.',
      ].filter(Boolean).join(' '),
    };
  }
  return { agents, chosen };
}

/**
 * @param resumeSession - a session id to continue from, for a resumed or forked run. Absent starts fresh.
 */
/** A step title for filing, from the tool that just ran. Spaced out of camel case so it reads as prose. */
function verbForFiling(toolName) {
  const { verb } = nameAndOrigin(toolName);
  return String(verb || '').replace(/([a-z0-9])([A-Z])/g, '$1 $2').replace(/_/g, ' ').toLowerCase();
}

/**
 * Register whatever a tool just wrote into the study, and announce each file on the run's stream.
 *
 * NEVER THROWS AND NEVER BLOCKS THE LOOP. A filing failure must degrade to the four second poll, which still runs; an
 * exception raised inside a hook would take out the tool call that produced the file.
 *
 * The snapshot is taken per run and advanced as files are found, so each call reports only what is new.
 */
const filingSnapshots = new Map(); // runId -> before
const announcedFiles = new Map(); // runId -> Set of name:size already announced
async function registerAndAnnounce(runId, sessionKey, stepTitle) {
  if (!sessionKey) { console.error('[filing %s] no sessionKey', runId); return; }
  try {
    /*
     * THE FLOOR IS SET AT RUN START, NOT ON THE FIRST TOOL CALL.
     *
     * MEASURED: with the snapshot taken here on first use, this returned early and the FIRST tool's files were never
     * announced. A run whose only write was `printf > bashmade.csv` produced the file correctly, in the right directory,
     * and announced nothing. Establishing the floor before the loop starts means the first write counts like every
     * other. A missing floor still degrades safely: with no snapshot recorded, nothing is claimed as new.
     */
    const before = filingSnapshots.get(runId);
    if (before === undefined) { console.error('[filing %s] NO FLOOR, nothing can be new', runId); return; }
    // THE PHASE TRAVELS WITH THE REGISTRATION, so a file lands in its phase's folder and can be attributed
    // to the work that produced it. Until now this call passed only the step title.
    const { phase, phaseIndex } = currentPhaseFor(runId);
    const registered = await platformStore.registerFiles({
      session: sessionKey, before, runId, stepTitle, phase, phaseIndex });
    if (Array.isArray(registered) && registered.length > 0) {
      const next = await platformStore.snapshot(sessionKey);
      if (next) filingSnapshots.set(runId, next);
    }
    /*
     * WHAT TO ANNOUNCE COMES FROM THE INDEX, NOT FROM THIS FUNCTION'S OWN DIFF.
     *
     * MEASURED, and it is the whole defect the operator reported four times. Two registrars share one artifact index: the
     * engine's code runner files what a script wrote, and this post-tool seam files anything else. Whichever arrives first
     * wins, and the loser diffs against a workspace that ALREADY contains the file, correctly concluding that nothing is
     * new. On run max-ff20d03e11 all eleven outputs, 6H0F.pdb and gnina_docked.sdf.gz among them, sat in the index under
     * the right run id with ZERO file events emitted. Nothing downstream could render a file it was never told about, and
     * no amount of console work could fix that.
     *
     * Asking the index makes announcement independent of who filed the file. The dedup below still decides what is new to
     * a READER, which is this side's actual job.
     */
    const indexed = await platformStore.filesForRun({ session: sessionKey, runId });
    const files = [];
    const seenPath = new Set();
    for (const f of [...(Array.isArray(registered) ? registered : []), ...(Array.isArray(indexed) ? indexed : [])]) {
      if (!f || !f.name) continue;
      const id = String(f.id || `${f.name}:${f.size ?? ''}`);
      if (seenPath.has(id)) continue;
      seenPath.add(id);
      files.push(f);
    }
    if (files.length === 0) return;
    /*
     * ANNOUNCED ONCE PER NAME PER RUN.
     *
     * MEASURED: a single `printf > routes.csv` was announced TWICE, because this hook fires per tool call and two calls
     * can be in flight while the snapshot between them has not yet advanced. The console's file list keys on the name
     * and collapses the repeat, but the timeline does not, so the reader would see the same file arrive twice.
     *
     * Keyed on name and size, so a genuine REWRITE is still announced: on a real tape the same comparison CSV grew
     * 465 -> 242 -> 140 -> 624 bytes across steps, and each of those is a real event in the study.
     */
    let announced = announcedFiles.get(runId);
    if (!announced) {
      announced = new Set();
      announcedFiles.set(runId, announced);
    }
    for (const f of files) {
      if (!f || !f.name) continue;
      const key = `${f.name}:${f.size ?? ''}`;
      if (announced.has(key)) continue;
      announced.add(key);
      emit(runId, KINDS.FILE, { agent: 'lead', file: f });
    }
  } catch {
    // Degraded record, not a lost step.
  }
}

/**
 * PUSH THIS RUN'S WORK TO GITHUB, IF A REPOSITORY IS BOUND TO IT.
 *
 * The operator's instruction was "yes push for everything", so this is called from the run's `finally` and not from the success
 * path: a run that failed still wrote code and still produced logs, and those are often the ones you most want versioned. The
 * outcome travels into the commit subject so a reader can tell them apart without opening a run.
 *
 * NOTHING IS PUSHED UNLESS A BINDING EXISTS. `repobind.resolve` answers for this session, then the group it belongs to, then
 * its project, and a session covered by none of them is left alone. Pushing a client's work into a repository nobody chose is
 * not undone by deleting a commit.
 *
 * THE RESULT IS ALWAYS REPORTED, success or failure. A push that fails silently would leave the operator believing work is in
 * a repository when it is not, which is the same class of defect as a cancel button that answered 409 into a void.
 *
 * A FAILURE HERE NEVER FAILS THE RUN. The science is already done and recorded; losing it because a remote was unreachable
 * would be a worse outcome than a run that completed with its push still to do.
 */
/**
 * Write this run's state of record, derived from the tape and the artifact index.
 *
 * WS-30 T4. NOTHING IS ACCUMULATED HERE. The manifest is computed from what already exists every time
 * it is written, so it cannot be edited into disagreeing with the tape. `LESSONS.md` in the reference
 * framework is the argument: a state file rewritten in place on every tool call, shared between
 * sessions, silently no-ops when its shape differs from the one assumed, and that bit them three times
 * in one session.
 *
 * NEVER FAILS A RUN. A manifest is a record ABOUT the work, not the work, so the reasoning is the same
 * as the push below: losing a finished run because a note about it could not be written would be
 * absurd. A failure is printed rather than swallowed in silence.
 */
/**
 * This run's manifest, then the text a just-compacted context should be handed.
 *
 * WS-30 T6. BUILT FRESH RATHER THAN READ BACK: the manifest is derived, so rebuilding costs one tape read
 * and one index read and cannot be stale. The file written at PreCompact is a fallback for when building
 * fails, and `rehydrationFrom` says the manifest is current, so handing over a stale one would make that
 * sentence a lie.
 *
 * The wording lives in `manifest.mjs` as a pure function, because a hook body is only reachable through a
 * live SDK session and text nobody can test is text nobody can trust.
 */
async function rehydrationText(runId, why) {
  let manifest = null;
  try {
    const run = store.getRun(runId);
    const events = store.eventsFor(runId);
    const session = (run && (run.console_session || run.session_key)) || '';
    let files = null;
    try { files = await platformStore.filesForRun({ session, runId }); } catch { files = null; }
    manifest = buildManifest({ runId, run, events, files, readDoc: readDocText });
  } catch {
    manifest = readManifest(DB, runId);
  }
  return rehydrationFrom(manifest, why);
}

/**
 * A produced document's text, or '' when it cannot be read.
 *
 * WS-30 T9. `folder` on an artifact record is a LABEL and not a location, because artifacts are stored under
 * an opaque hashed name; `filing.py` says so where it computes it. `source_path` is where the file still is,
 * so that is what is read.
 *
 * BOUNDED, because this is called for every document on every manifest build and a document is Markdown: a
 * megabyte is far more than any phase report and far less than a file that could stall a hook. Returning ''
 * on failure is deliberate: unread is treated as unverified, never as verified.
 */
function readDocText(record) {
  try {
    const path = String((record && record.source_path) || '');
    if (!path) return '';
    const bytes = readFileSync(path);
    return bytes.length > 1_000_000 ? bytes.subarray(0, 1_000_000).toString('utf8') : bytes.toString('utf8');
  } catch {
    return '';
  }
}

async function writeRunManifest(runId, why) {
  try {
    const run = store.getRun(runId);
    const events = store.eventsFor(runId);
    const session = (run && (run.console_session || run.session_key)) || '';
    // THE INDEX IS THE AUTHORITY ON FILES, not the tape: on run max-ff20d03e11 all eleven outputs were
    // filed under the right run id and not one had been announced, so a tape-only manifest would have
    // reported zero files for a run that produced eleven.
    let files = null;
    try {
      files = await platformStore.filesForRun({ session, runId });
    } catch {
      // `sources.index` then reads false, which is how a reader tells "produced nothing" apart from
      // "could not see what was produced".
      files = null;
    }
    return writeManifest(DB, buildManifest({ runId, run, events, files, readDoc: readDocText }));
  } catch (e) {
    console.error('[manifest %s] not written (%s): %s', runId, why || '', String((e && e.message) || e));
    return '';
  }
}

/*
 * `message` AND `step` ARE PARAMETERS, and their absence was a live ReferenceError.
 *
 * WS-30 T11 added two references to them in this function and the edit that DECLARED them was lost: the script that
 * changed this signature hit a failed assertion further down and never wrote the file, and I did not check that the
 * signature had actually changed. So every phase-close push threw `message is not defined`, was caught by the handler
 * below, and was recorded as `{ok: false, error: "hook_failed"}`. The feature never worked once.
 */
async function autoPushToGitHub(runId, sessionKey, outcome, { message = '', step = '' } = {}) {
  const userId = process.env.RAYCA_USER_ID || '';
  if (!userId) return;
  try {
    const args = ['-m', 'modulon.tools.github',
      '--session', sessionKey || '', '--run', runId || '',
      '--user', userId, '--outcome', outcome || ''];
    /* A STEP-SCOPED MESSAGE, WS-30 T11. THE OPERATOR: "it is good to have when researcher connect the
       session to their github and wamts to push after each step." The message carries the step id, because
       that is what makes `commit_step` satisfiable by OBSERVATION rather than assertion: the obligation
       looks for the id in what was actually pushed. Same shape as the reference's `Step <id>` convention. */
    if (message) args.push('--message', message);
    const out = await new Promise((resolve) => {
      const child = spawn(PY, args, {
        cwd: SRC.replace(/\/src$/, ''),
        env: { ...process.env, PYTHONPATH: SRC },
        stdio: ['ignore', 'pipe', 'pipe'],
      });
      let stdout = '';
      let stderr = '';
      child.stdout.on('data', (d) => { stdout += String(d); });
      child.stderr.on('data', (d) => { stderr += String(d); });
      // A PUSH IS BOUNDED. A hung remote must not hold a finished run open for ever; the run is already recorded either way.
      const timer = setTimeout(() => { try { child.kill('SIGKILL'); } catch { /* already gone */ } },
        Number(process.env.RAYCA_GITHUB_PUSH_TIMEOUT_MS || 240000));
      child.on('close', () => { clearTimeout(timer); resolve({ stdout, stderr }); });
      child.on('error', (e) => { clearTimeout(timer); resolve({ stdout: '', stderr: String(e?.message || e) }); });
    });
    let parsed = null;
    try { parsed = JSON.parse((out.stdout || '').trim().split('\n').filter(Boolean).pop() || 'null'); } catch { parsed = null; }
    if (!parsed) {
      // NO OUTPUT IS NOT NO EVENT. Something ran and said nothing parseable, and the reader needs to know the push did not
      // happen rather than being left to assume from silence that it did.
      emit(runId, KINDS.PUBLISH, { ok: false, error: 'no_result',
        detail: String(out.stderr || 'the push produced no readable result').slice(0, 300) });
      return;
    }
    if (parsed.error === 'no_repo' || parsed.error === 'no_credential') {
      // NOT AN ERROR WORTH SHOWING. No repository bound, or GitHub never connected, is the ordinary state of a session that
      // was never meant to be pushed. Announcing it on every run would train the reader to ignore this event.
      return;
    }
    /* THE STEP TRAVELS ON THE EVENT, so `commit_step` is derived from the tape rather than from a second
       record. Absent on a whole-run push, which is how the two are told apart. */
    emit(runId, KINDS.PUBLISH, step ? { ...parsed, step } : parsed);
  } catch (e) {
    emit(runId, KINDS.PUBLISH, { ok: false, error: 'hook_failed', detail: String(e?.message || e).slice(0, 300) });
  }
}

/*
 * ONE DESCRIPTION OF WHAT AN INTENT MEANS, USED BY EVERY START PATH.
 *
 * MEASURED: the console has always sent `intent` on a fork, under a comment promising a follow-up carries what a first
 * prompt carries. Only the fresh-start handler read it. So the second and every later click of Generate Dashboard ran
 * with the bare words "Generate Dashboard" and whatever the conversation still held. One run answered "Dashboard already
 * generated and ready" after two turns; another rebuilt the previous design from stale context. The operator: "last one
 * failed and the other one just used the previous template".
 *
 * This is the third field that was present on the fork request and ignored on this side, after the model and temperature
 * pair and the attachments. Hence one helper rather than a second copy of the logic.
 */
async function expandForIntent(body, task, sessionKey) {
  const intent = String(body.intent || '').toLowerCase();
  if (intent !== 'dashboard') return task;
  try {
    const brief = await platformStore.dashboardBrief({ session: sessionKey, title: body.title || '' });
    if (!brief) {
      console.error('[dashboard] no brief available for session %s', String(sessionKey).slice(0, 8));
      return task;
    }
    const extra = task && !/^generate dashboard$/i.test(task)
      ? `\n\nADDITIONAL REQUEST FROM THE USER, which does not relax anything above:\n${task}`
      : '';
    return `${brief}${extra}`;
  } catch (e) {
    console.error('[dashboard] brief failed: %s', String(e && e.message || e));
    return task;
  }
}

async function runTask(runId, task, teamMode, resumeSession = '', model = MODEL, temperature = undefined,
  attachments = []) {
  const { agents, chosen } = teamMode ? agentDefinitionsFor(task, runId) : { agents: undefined, chosen: [] };
  const rec = live.get(runId);
  /* HOW THIS RUN ENDED, for the commit subject. Set at the two places that actually decide it rather than read back from the
     store, which has no method for it: a reader invented here would have said "completed" for every failure. */
  let pushOutcome = 'completed';
  /*
   * BEFORE THE CHANNEL, WHICH IS THE WHOLE POINT.
   *
   * My first attempt folded the briefing in further down, once `platformStore.workspace()` had answered. It had no effect and the
   * measurement said so plainly: the model listed its own tools instead of the attached ones, and the run's task held no briefing.
   * `new InputChannel(task)` CAPTURES the string here, so a later reassignment of the parameter changes nothing that is ever read.
   * A variable that is read once, early, cannot be fixed up late.
   *
   * The workspace is therefore resolved from disk rather than waited for: a session's directory is its key plus a suffix, so it can
   * be found by prefix without a bridge round trip, and the bridge on this path has already been seen to time out and lose data.
   */
  const attachSession = consoleSessionFor(runId) || runId;
  const attachTask = withAttachments(
    runId, task, { attachments }, sessionWorkspace(attachSession), await artifactLookup(attachSession),
  );
  const channel = new InputChannel(attachTask);
  rec.queue = channel;

  /*
   * THE EVENT SHOWS WHAT THE READER ASKED, NOT WHAT THE MODEL WAS GIVEN.
   *
   * THE OPERATOR, twice: "i do not want the user to see this long prompt" and then "just for you to know the long prompt
   * still gets into the conversation and it is annoying for the user". The first fix corrected the run store and missed
   * this event, which is what the console actually renders as the prompt. MEASURED on a live run: the store held 18
   * characters while `session.start` carried 9601.
   *
   * READ BACK FROM THE STORE rather than passed in as another parameter. The store already holds the asked task, so the
   * event and every listing are the same string by construction and cannot drift apart the way these two just did.
   */
  const shownTask = (() => {
    try {
      return store.getRun(runId)?.task || task;
    } catch {
      return task;
    }
  })();
  emit(runId, KINDS.SESSION_START, {
    /*
     * THE MODEL THAT RAN, NOT THE ONE THIS DEPLOYMENT DEFAULTS TO.
     *
     * MEASURED: a run started with model=qwen3-coder-480b stored qwen3-coder-480b, the router really called
     * bedrock/qwen.qwen3-coder-480b-a35b-v1:0, and this event still announced claude-sonnet-4-6. `runTask` has taken a
     * `model` argument since the selector was fixed; this line kept reading the module constant, so the console showed
     * the wrong model for every run that was not on the default.
     */
    model, team: !!teamMode, task: shownTask,
    team_members: chosen.map((p) => ({ id: p.id, name: p.name, why: p.summary })),
  });

  const gov = await governance.begin(runId, process.env.RAYCA_GATE_MODE || '');
  emit(runId, KINDS.GATE, { gate: 'governance', state: gov.gates || 'unknown', advisory: true,
    detail: gov.gates === 'open' ? 'gates, credits and claim judging are active for this run'
      : 'governance is NOT active: figures in this run are unverified' });

  // MEMORY PREFETCH: consult procedural and episodic memory BEFORE the first model turn.
  // This is a MECHANISM, not an instruction. memprefetch.py argues why: on a real run the model
  // ignored the prompt to call retrieve_procedures. Querying here makes it a property of every run.
  let memoryContent = '';
  {
    const mem = await memoryPrefetch(task);
    if (mem && mem.ok && mem.message) {
      memoryContent = mem.message.content || '';
      const meta = mem.meta || {};
      const hasErrors = meta.errors && Object.keys(meta.errors).length > 0;
      emit(runId, KINDS.MEMORY, {
        procedures: meta.procedures || 0, episodes: meta.episodes || 0,
        lessons: meta.lessons || 0, failed: !!hasErrors, errors: meta.errors || {},
        /*
         * WHAT WAS CONSULTED, not only how much of it.
         *
         * THE OPERATOR: "i am wondering even the engrams being called? because the memory rail doesn't display
         * anything!" They were being called: 14 procedures and 24 episodes on a real run. This event carried only the
         * tallies, while the console's memory column renders `memory` as a list of calls each holding `records`, so the
         * retrieval was real and the rail had nothing to draw. `memprefetch.memory_calls` builds the identities; this
         * passes them on.
         */
        ...(Array.isArray(meta.memory) && meta.memory.length ? { memory: meta.memory } : {}),
        detail: hasErrors
          ? `consulted but degraded: ${Object.values(meta.errors).join('; ')}`
          : `${meta.procedures || 0} procedures, ${meta.episodes || 0} episodes, ${meta.lessons || 0} lessons`,
      });
    } else {
      // Bridge itself unreachable. Fabricate the honest failure message that memprefetch would have
      // returned, so the model knows and can say so. A silent omission is never acceptable.
      memoryContent = 'MEMORY WAS CONSULTED BEFORE THIS RUN.\n\n'
        + 'CONSULTATION FAILED - MemoryUnavailable: the memory bridge did not respond.\n'
        + 'This is an outage, NOT evidence that no relevant procedure exists.';
      emit(runId, KINDS.MEMORY, { procedures: 0, episodes: 0, lessons: 0, failed: true,
        errors: { bridge: 'memory bridge did not respond' },
        detail: 'memory bridge unreachable' });
    }
  }

  const verbOf = new Map();
  const inflight = new Map(); // tool_use id -> { verb, started }
  // OUTSTANDING MEMBERS. `Agent` is ASYNCHRONOUS: it returns a launch receipt, so the lead's loop can report a result
  // while its specialists are still working. Measured twice -- once at 22s and once at 19.5s -- a team run ended with
  // the members' findings absent from the answer. A team report containing no team is worse than a single-agent one,
  // because the reader has been told specialists were consulted.
  const members = new Map(); // child id -> { type, done }
  let sessionId = '';
  let turn = 0;
  let finalResult = null;
  let mergeRequested = false;
  // PLAN-BEFORE-DISPATCH GATE. In a team run the lead MUST create at least one task before delegating,
  // so the console's study plan and to-do list have content. MEASURED: a PROTAC team run dispatched 4
  // members immediately with ZERO task events, leaving the study plan empty. memprefetch.py argues
  // that a prompt is not a mechanism, and the same applies here: telling the model to plan first did
  // not hold on real runs. This counter is the mechanism -- the Agent tool is refused until it is > 0.
  let tasksCreated = 0;

  /** A long tool call must say it is still working. Silence looked like a freeze for fifteen minutes. */
  const ticker = setInterval(() => {
    for (const [id, f] of inflight) {
      const seconds = Math.round((Date.now() - f.started) / 1000);
      if (seconds >= 20) emit(runId, KINDS.PROGRESS, { agent: 'lead', id, verb: f.verb, seconds });
    }
  }, 20000);

  /*
   * THE STUDY'S DIRECTORY, RESOLVED ONCE.
   *
   * Asked of the platform rather than composed, because the path carries a hash. Failure is tolerated: with no path the
   * options omit `cwd` and behaviour is exactly what it was before, which is worse but not broken.
   */
  const sessionKey = consoleSessionFor(runId) || runId;
  let workspacePath = '';
  try {
    workspacePath = await platformStore.workspace(sessionKey);
  } catch {
    workspacePath = '';
  }
  /*
   * REMEMBERED FOR THIS RUN, because the cluster job watcher needs it and cannot resolve it synchronously.
   *
   * A cluster job's outputs are collected into the session workspace, which is also the directory the file manager
   * reads, so a collected trajectory lands beside the inputs that produced it. The watcher records the target when the
   * job is SUBMITTED, long before it finishes, and by then this is the only place that already knows the path.
   */
  if (workspacePath) {
    if (workspaces.size >= MAX_REMEMBERED_WORKSPACES) {
      workspaces.delete(workspaces.keys().next().value);
    }
    workspaces.set(runId, workspacePath);
  }

  // The filing floor, taken before any tool runs so that the first file written counts.
  try {
    const snap = await platformStore.snapshot(sessionKey);
    filingSnapshots.set(runId, snap || {});
  } catch (e) {
    console.error('[filing %s] floor FAILED: %s', runId, String(e && e.message || e));
    // No floor means nothing is claimed as new, which is the safe direction.
  }

  /*
   * The usable input budget for THIS run's model, from the router's published numbers. Null when the router has not
   * been reached yet or does not declare one, in which case the SDK keeps whatever default it would have used: a wrong
   * number here would be worse than no number, because it would compact a Claude run that had plenty of room left.
   */
  const compactWindow = (() => {
    const p = PRICES[model] || PRICES[String(model || '').toLowerCase()] || null;
    const n = Number(p && p.maxInput);
    return Number.isFinite(n) && n > 10000 ? Math.floor(n) : null;
  })();
  if (compactWindow) {
    console.error('[compact %s] model=%s window=%d tokens', runId, model, compactWindow);
  } else {
    console.error('[compact %s] model=%s no published window, leaving the SDK default', runId, model);
  }

  /*
   * THE PRE-TOOL GATE, LIFTED OUT SO A FAULT IN IT CANNOT LOOK LIKE A REFUSAL.
   * Its deny paths are unchanged and each still emits its own `refused` event first. See the wrapper at PreToolUse.
   */
  const preToolGate = async (i) => {
        const { verb, origin } = nameAndOrigin(i?.tool_name);
        /*
         * A SHELL COMMAND MAY NOT INSTALL INTO THE SHARED INTERPRETER.
         *
         * `install_package` now installs with `--target` into a directory belonging to this session, which is what makes
         * dependency isolation real. It is also trivially bypassed: `Bash` can run `pip install` and write straight into the
         * venv the engine, the platform and every other session share.
         *
         * MEASURED CONSEQUENCE OF THAT WRITE, from a real study: aizynthfinder arrived with eighty-nine other packages
         * including a replacement numpy, and `anndata` stopped importing everywhere. One study, permanent, every session.
         *
         * REFUSED WITH THE ALTERNATIVE NAMED, because the model wants a package and not a lecture: it is told to use the verb
         * that installs into this session. A bare refusal teaches it to try another shell spelling.
         *
         * DELIBERATELY NARROW. Only an install into the shared interpreter is refused; `pip download`, `pip show`, `pip list`
         * and an install that already carries `--target` all pass, since none of them mutate what is shared.
         */
        if (verb === 'Bash' || verb === 'Monitor') {
          const cmd = String(i?.tool_input?.command || '');
          const installs = /(^|[;&|]|\s)(pip[0-9.]*|uv|conda|mamba|poetry)\s+(install|add)\b/.test(cmd)
            || /-m\s+pip\s+install\b/.test(cmd);
          const alreadyIsolated = /--target\b|--prefix\b|--user\b/.test(cmd);
          if (installs && !alreadyIsolated) {
            emit(runId, KINDS.REFUSED, { agent: 'lead', verb, origin,
              reason: 'shared_environment_protected',
              detail: 'This would install into the interpreter every session shares, which is how one study broke '
                + 'numpy for all of them. Use the install_package verb: it installs into this session only.' });
            return {
              hookSpecificOutput: {
                hookEventName: 'PreToolUse',
                permissionDecision: 'deny',
                permissionDecisionReason: 'Installing into the shared interpreter is not permitted, because it changes '
                  + 'the environment of every other session. Call the install_package tool instead, which installs into '
                  + 'this session alone and is importable immediately.',
              },
            };
          }
        }

        // PLAN-BEFORE-DISPATCH GATE. The Agent tool is the delegation mechanism. In a team run, refusing
        // it until at least one task exists is what makes the study plan a PROPERTY of the run rather than
        // an instruction the model may ignore. MEASURED: a PROTAC team run dispatched 4 members with zero
        // task events, leaving the console's study plan and to-do list empty. A prompt asking "plan first"
        // did not hold; this gate does. Only checked for the lead (no agent_id), because a member calling
        // Agent is itself already delegated work that was planned.
        /*
         * A SOLO RUN NEEDS A PLAN TOO, and this gap was found by watching a real one.
         *
         * MEASURED on a CPTAC multi-omics run: 24 turns, 18 tool calls, and ZERO task events, because the plan requirement
         * only applied to team mode. So the study plan and the to-do list were EMPTY for the whole run -- the same complaint
         * the operator raised about a team run, reappearing on the other path because I fixed the path I was looking at.
         *
         * GATED ON SUBSTANTIVE WORK, NOT ON EVERY CALL. Looking at the environment or reading a file is how a run works out
         * what is possible; demanding a plan before that would force the model to plan in ignorance. `run_python` and the
         * platform verbs are where a study actually commits to doing something, so that is the line.
         */
        /*
         * THE GATE NOW MATCHES WHAT ITS OWN MESSAGE PROMISES.
         *
         * It told the model "Environment checks and file reads do not require this" and then implemented substantive as
         * `origin === 'platform'`, which is EVERY platform tool -- including the ones that only look. So `list_compute`
         * was denied by a gate that said it would not be.
         *
         * MEASURED, run max-f833f4a42a on 2026-09-03: a prompt asking only for `list_compute` output was denied, the
         * model reported the denial and stopped after two turns. Two earlier runs recovered by declaring a task and
         * retrying, so the usual cost is turns rather than failure -- but a run that only wanted to know what compute
         * exists was refused, which is exactly the "planning in ignorance" the comment above warns against.
         *
         * THE SET IS DECLARED ONCE, in `engine/fastpath.py` as `DISCOVERY_VERBS`, and mirrored here because this file
         * cannot import Python. A test asserts the two agree, so the copy cannot drift in silence.
         */
        const DISCOVERY_VERBS = new Set([
          'list_compute', 'query_cluster', 'check_cluster_job',
          'list_aidd_tools', 'find_tools', 'find_tool',
          'inspect_environment',
        ]);
        const substantive = (origin === 'platform' || verb === 'run_python') && !DISCOVERY_VERBS.has(verb);
        if (substantive && tasksCreated === 0 && !String(i?.agent_id || '')) {
          /*
           * `coaching`, AND IT IS WHAT KEEPS THIS OFF A CLIENT'S SCREEN.
           *
           * THE OPERATOR: "in the begining of the run, when planning wants to happend this flag appear in the conversation ... anyway
           * the planing happens so what is the point of showing this to user to make them uncomfortable??"
           *
           * They are right, and the flag says so HERE rather than the console keeping a list of reason codes to hide. THIS GATE IS A
           * HANDSHAKE WITH THE MODEL, NOT NEWS FOR A READER: it denies the first substantive call precisely so the model goes and
           * declares its plan, which is exactly what `permissionDecisionReason` below tells it to do. The denial succeeding looks
           * identical, from the outside, to the denial never having been needed -- the plan appears either way.
           *
           * MEASURED before deciding to hide it: the gate fired 117 times across 80 of 203 runs, and 78 of those 80 then declared
           * tasks. Of the two that did not, one was stopped by the user and one answered a property lookup in four turns. It has never
           * left a run stuck, so a reader loses nothing by not seeing it.
           *
           * The flag belongs with the code that knows WHY the gate exists, not as a list of strings in the UI that someone has to
           * remember to extend for the next gate.
           */
          emit(runId, KINDS.REFUSED, { agent: 'lead', verb, origin, reason: 'plan_required', coaching: true,
            detail: 'Declare your plan as tasks before running the study. A run without a task list leaves no record of '
              + 'what was intended, only of what happened.' });
          return {
            hookSpecificOutput: {
              hookEventName: 'PreToolUse',
              permissionDecision: 'deny',
              permissionDecisionReason: 'Create at least one task first, so the study plan is populated before work begins. '
                + 'Environment checks and file reads do not require this; running analysis does.',
            },
          };
        }

        if ((verb === 'Agent' || verb === 'Task') && teamMode && tasksCreated === 0 && !String(i?.agent_id || '')) {
          /* Coaching, for the same reason as the gate above: it exists to make the model plan, and the model then plans. */
          emit(runId, KINDS.REFUSED, { agent: 'lead', verb, origin, reason: 'plan_required', coaching: true,
            detail: 'You must create a task list BEFORE delegating. Use the task-creation mechanism to '
              + 'declare what each specialist will do, then delegate. A team run without a plan leaves the '
              + 'study with no record of what was intended.' });
          return {
            hookSpecificOutput: {
              hookEventName: 'PreToolUse',
              permissionDecision: 'deny',
              permissionDecisionReason: 'Create tasks first. The Agent tool is deferred until at least one '
                + 'task exists, so the study plan is populated before work begins.',
            },
          };
        }
        // `BaseHookInput` CARRIES `agent_id` AND `agent_type`, which is the authoritative answer to "who called this".
        // My first attempt labelled each member's own MCP server instead, and it could not work: members share the
        // parent's server because both register it under the name `rayca`, so every member call arrived labelled
        // `lead` and was skipped. The hook knows without anything having to be arranged.
        const who = String(i?.agent_id || '');
        if (who) {
          // A MEMBER'S CALL NEEDS A NAME AS MUCH AS THE LEAD'S. Fixing only the lead left 4 of 58 tool events on a team
          // run still reading `run_python`, and every one was a specialist's call: exactly the events a reader opens the
          // team view to understand.
          let mcap = captionFrom(i?.tool_input);
          if (!mcap) {
            const mcode = i?.tool_input && typeof i.tool_input === 'object'
              ? String(i.tool_input.code ?? i.tool_input.script ?? i.tool_input.source ?? '')
              : '';
            if (mcode) {
              const mslug = await scriptSlug(mcode);
              if (mslug) mcap = String(mslug).replace(/_/g, ' ');
            }
          }
          emit(runId, KINDS.MEMBER_CALL, { child: who, agent_type: i?.agent_type || '', verb, origin,
            input: i?.tool_input, ...(mcap ? { caption: mcap } : {}) });
        }
        const verdict = await governance.beforeTool({ runId, verb, origin, input: i?.tool_input });
        if (verdict.allow === false) {
          emit(runId, KINDS.REFUSED, { agent: 'lead', verb, origin, reason: verdict.reason, detail: verdict.detail });
          return {
            hookSpecificOutput: {
              hookEventName: 'PreToolUse',
              permissionDecision: 'deny',
              permissionDecisionReason: verdict.detail || verdict.reason || 'refused by governance',
            },
          };
        }
        if (verdict.gate) emit(runId, KINDS.GATE, { agent: 'lead', verb, origin, ...verdict.gate });
        return {};
  };

  const options = {
    model,
    // Omitted entirely when nothing was asked, so the SDK's own default stands.
    ...(temperature === undefined ? {} : { temperature }),
    // Claude Code's own judgement is opt-in in the SDK. Without this the loop has the tools and not the instincts,
    // which is the whole of the "the SDK is not as smart as the CLI" story; the first spike runs fell back to raw Bash.
    systemPrompt: {
      type: 'preset',
      preset: 'claude_code',
      ...(teamMode && chosen.length || memoryContent ? { append: [
        memoryContent || '',
        teamMode && chosen.length ? [
          'SPECIALISTS ARE AVAILABLE AND YOU ARE EXPECTED TO USE THEM. Agent team mode is on for this task. Delegate',
          'with the Agent tool to: ' + chosen.map((p) => p.id).join(', ') + '.',
          'Split the work by expertise, in parallel where the parts are independent. When members report, merge their',
          'findings and PRESERVE DISAGREEMENT rather than resolving it silently into one answer.',
        ].join(' ') : '',
      ].filter(Boolean).join('\n\n') } : {}),
    },
    /*
     * THE MODEL'S REAL CONTEXT WINDOW, TOLD TO THE SDK RATHER THAN GUESSED BY IT.
     *
     * THE OPERATOR, on being offered a fallback to a bigger model instead: "why should it hand over another model? can
     * it just compact the conversation?" They are right. Compaction is the correct answer for a conversation that
     * outgrows its window; handing over changes the model mid-study and costs about fourteen times as much per token.
     *
     * WHY COMPACTION WAS NOT FIRING. The SDK sizes auto-compaction from a context window it looks up by CANONICAL MODEL
     * ID, and the shipped bundle contains no non-Claude model names at all: its own type declaration puts `contextWindow`
     * next to `canonicalModel`, "the canonical model id used for the pricing lookup". So on Qwen it had no window to
     * measure against and never compacted, and the run died at Bedrock instead: "your prompt contains at least 99073
     * input tokens, for a total of at least 131073", one token over the limit, at turn one, having produced nothing.
     *
     * THE ROUTER KNOWS THE NUMBER, because it is the thing that talks to Bedrock, and it publishes it per model on
     * /model/info. MEASURED and corrected there: qwen3-coder-480b is 131072 TOTAL, not the 262000 input the config used
     * to claim, which left 99000 usable once the SDK's 32000-token output request is subtracted.
     *
     * PASSED PER RUN through `env`, which the SDK documents for exactly this, so two concurrent runs on different models
     * cannot race over one process-wide variable.
     */
    ...(compactWindow ? { env: { ...process.env, CLAUDE_CODE_AUTO_COMPACT_WINDOW: String(compactWindow) } } : {}),
    /*
     * THE ROOT CAUSE OF THE TOOL DENIALS, AND WHY THIS MODE IS NO LONGER THE ANSWER.
     *
     * THE OPERATOR: "it continuesly say File write blocked by permissions ... that was not happening yesterday!"
     *
     * MEASURED: 89 denied tool results across 34 runs since 21 August, 6.4% of all calls today against 0.21% yesterday.
     * Every one arrived at the model as the SDK's own sentence, "The user doesn't want to take this action right now",
     * so the model concluded the reader had refused and told a client to check their Claude Code permission settings and
     * paste shell output by hand. Nothing in this engine refused any of them: all four of our deny paths emit a `refused`
     * event first and those runs have none.
     *
     * WHAT ACTUALLY DENIES THEM is in the SDK's own type declarations: `SDKPermissionDeniedMessage`, documented as
     * "emitted when a tool call is auto-denied WITHOUT an interactive permission prompt (e.g. auto-mode classifier,
     * dontAsk mode, headless...)", carrying a `decision_reason_type` of 'classifier', 'asyncAgent', 'mode' or 'rule'.
     * So the SDK denies headlessly and says so on the message stream, and we were not reading that message.
     *
     * AND `bypassPermissions` IS WHY WE COULD NOT INTERVENE. It auto-approves the ordinary path, which is why most calls
     * work, but it also SHADOWS `canUseTool` -- the SDK warns about this explicitly -- so when the classifier decided to
     * deny there was no callback left that could say yes. The mode that was supposed to remove permission friction is the
     * mode that made the remaining friction unanswerable.
     *
     * SO: `default` plus a `canUseTool` that allows. Every call the SDK wants to ask about is now asked, and answered yes,
     * which is what a headless research engine needs. This is not a loosening. Governance is unchanged and still runs in
     * `PreToolUse`, which fires in EVERY mode, and its four denials still refuse with their own stated reasons. The
     * difference is that a refusal now only ever comes from us, with a reason a reader can act on, instead of from a
     * classifier speaking in the voice of the user.
     */
    /*
     * REVERTED TO `bypassPermissions`, AND THE MEASUREMENT IS WHY.
     *
     * I changed this to 'default' with a `canUseTool` that allows, reasoning that bypass shadows the callback so a classifier
     * denial could not be answered. The reasoning was sound and the result was WORSE, measured on the live platform:
     *
     *   before the change   172 tool results, 11 denied, 6.40%
     *   after the change     87 tool results, 14 denied, 16.09%
     *
     * Because `canUseTool` is never invoked at all -- instrumentation logged zero calls -- so under 'default' every call the
     * SDK wants to ask about has no approver and is auto-denied. `bypassPermissions` at least auto-approves the ordinary
     * path, which is why most work got done. Trading a mode that approves most calls for one that asks about many and can
     * answer none made the platform measurably worse for about half an hour.
     *
     * The `canUseTool` below stays because it costs nothing and is correct if the SDK ever routes to it. The real cause of
     * the residual denials is still open; what is now known is that it is NOT reachable through the permission mode, and the
     * `permission_denied` observer added alongside this is what will name it.
     */
    /*
     * THE ENGINE DOES NOT INHERIT THIS MACHINE'S PERSONAL CLAUDE CONFIGURATION.
     *
     * THE OPERATOR, repeatedly: "still tools are blocked!!" and "that was not happening yesterday."
     *
     * THE SDK LOADS THE HOST'S SETTINGS BY DEFAULT. Its own declaration says so: "When omitted, all sources are loaded
     * (matches CLI defaults). Pass `[]` to disable filesystem settings (SDK isolation mode)." We omitted it. So every client
     * run was loading `~/.claude/settings.json` off this box, which has EIGHTEEN plugins enabled, three of which register
     * hooks that can block work:
     *
     *   hookify            PreToolUse, PostToolUse, Stop, UserPromptSubmit
     *   security-guidance  PostToolUse, SessionStart, Stop, UserPromptSubmit  -- emits `decision: "block"`
     *   ralph-loop         Stop
     *
     * PROVEN INHERITED, not inferred: a probe script defining NO hooks at all still produced five `hook_started` events when
     * it ran a single Bash command through this SDK. Those hooks are not ours. And a real run recorded the model reasoning
     * about "a Stop hook feedback message", which is not language this platform ever emits.
     *
     * THAT IS ALSO THE ANSWER TO "WHY NOW". Nothing in our code changed: the SDK pin has been 0.3.238 since modulon-max's
     * first commit, and the denials start on the day it was installed. What varies is what a developer has enabled on this
     * host and what a given run happens to do, which is exactly why the rate wandered between 0% and 6% for ten days with no
     * release to blame. A client's run should never depend on that.
     *
     * `[]` IS SAFE HERE, CHECKED RATHER THAN ASSUMED. Isolation also stops `CLAUDE.md` and project settings being read, so:
     * no session workspace contains a `CLAUDE.md` (0 of them) and none contains `.claude/settings.json` (0). The engine
     * passes its own hooks, tools and system prompt programmatically, so nothing it relies on comes from the filesystem.
     *
     * This is not the same claim as "the denials are fixed". It removes an entire class of outside interference from client
     * runs, which is correct on its own terms; the `permission_denied` observer stays to name anything that remains.
     */
    settingSources: [],
    permissionMode: 'bypassPermissions',
    /*
     * ALWAYS YES, AND DELIBERATELY NOT A JUDGEMENT. This callback exists to answer the SDK's question, not to make policy:
     * what may run is decided in `PreToolUse` above, with the run's plan, credits and containment in hand. Two gates that
     * both decide would disagree, and the one without context would win by arriving first. `updatedInput` is passed
     * through untouched so approving a call cannot quietly alter it.
     */
    canUseTool: async (toolName, input) => {
      /* TEMPORARY INSTRUMENTATION while the residual denials are traced. Remove once the cause is named. */
      console.error(`[max ${runId}] canUseTool asked about ${toolName}`);
      return { behavior: 'allow', updatedInput: input };
    },
    // RESUME CARRIES THE TRANSCRIPT, so a forked or continued run knows what its parent did rather than being told
    // about it in a prompt. That distinction matters: a summary of prior work is the model's account of it, while a
    // resumed transcript is the record.
    ...(resumeSession ? { resume: resumeSession } : {}),
    // FOR THE MEMBER-PROVENANCE EXPERIMENT ONLY. Denying the lead a verb is the only way to prove that a figure
    // reported by the lead was computed by a MEMBER: left free, the lead ran the tool itself even when told not to,
    // so both transcripts contained the number and the test proved nothing.
    /*
     * WEB SEARCH IS NOT AVAILABLE ON BEDROCK, SO IT IS NOT OFFERED.
     *
     * MEASURED, and it killed a resumed session at turn 5. The SDK offers Anthropic's server-side web search tool, which
     * puts `web_search_options` in the request and a tool typed `web_search_20250305` in the tool list. The router
     * answered:
     *
     *   litellm.UnsupportedParamsError: bedrock does not support parameters: ['web_search_options'],
     *   for model=qwen.qwen3-coder-480b-a35b-v1:0
     *
     * and the fallback to Sonnet failed on the same request for a different reason, which is what proves this is about
     * Bedrock and not about Qwen:
     *
     *   Error doing the fallback: tools.0: Input tag 'web_search_20250305' found using 'type' does not match any of the
     *   expected tags: 'bash_20250124', 'custom', 'memory_20250818', 'text_editor_20250124', ...
     *
     * So the tool works on neither model here, because both are reached through Bedrock. What the reader saw was the
     * SDK's canned policy message, "qwen3-coder-480b can't help with this. Start a new session to continue", with a link
     * to an acceptable use policy. Nothing was refused on policy: a tool that cannot exist on this provider was offered,
     * the request was rejected for its shape, and the failure was reported as though the model had declined.
     *
     * THE SAME CLASS OF DEFECT AS run_aidd_tool, in the opposite direction: there the platform advertised a verb it did
     * not publish, here it publishes a verb the provider cannot accept. Both end with a capable model telling a
     * researcher it cannot work.
     *
     * MAX_LEAD_DENY still applies on top, so an operator can deny more without editing this.
     */
    disallowedTools: ['WebSearch', ...(process.env.MAX_LEAD_DENY ? process.env.MAX_LEAD_DENY.split(',') : [])]
      .map((t) => String(t).trim()).filter(Boolean),
    /*
     * A COST CEILING RATHER THAN A TURN COUNT.
     *
     * WHY THE TURN CAP WAS THE WRONG GUARD, MEASURED TWICE. Two EGFR/erlotinib MD runs reached 109 and 119 recorded turns
     * and both died on `maxTurns: 40` mid-preparation, one of them while debugging an acpype topology, having produced 87
     * files and never reaching the submission it was working towards. The operator: "why should we have max turns at
     * all?" Turns are a proxy for spend and a poor one: a study that needs 120 productive turns is punished exactly as
     * hard as one stuck in a loop.
     *
     * A LIMIT IS STILL NEEDED, and not hypothetically. On a real team run the lead spent turn after turn polling two
     * specialists that never reported -- "Both still running (47s and 37s in)", "Still waiting" -- which is the failure a
     * bound exists for: not slow work, but work that will never finish. `maxBudgetUsd` bounds exactly that, and lets a
     * long productive study run to completion.
     *
     * $15 IS THE OPERATOR'S FIGURE, chosen against measured costs: the PD-L1 binder design completed for $1.73, and the
     * MD preparation was heading past $4 when the turn cap stopped it.
     *
     * MAX_TURNS IS STILL HONOURED IF SET, so a hard turn cap remains available, but it is no longer imposed by default.
     * Omitting it entirely is safe: the SDK spreads the field conditionally, so an absent value sends no cap rather than
     * falling back to one of its own.
     */
    // A BACKSTOP, NOT THE LIMIT. The real limit is enforced on router-priced spend when each result arrives; this only
    // bounds a pathological loop in the case where our own accounting cannot price a model at all.
    maxBudgetUsd: BUDGET_USD * SDK_BUDGET_BACKSTOP,
    ...(process.env.MAX_TURNS ? { maxTurns: Number(process.env.MAX_TURNS) } : {}),
    ...(agents ? { agents } : {}),
    mcpServers: {
      rayca: {
        type: 'stdio', command: PY, args: [MCP],
        env: { RAYCA_SRC: SRC, PYTHONPATH: SRC, RAYCA_USER_ID: process.env.RAYCA_USER_ID || '',
          /*
           * THE CONVERSATION'S WORKSPACE, NOT A PRIVATE ONE PER RUN.
           *
           * `workspace_for(RAYCA_SESSION_ID)` is where the platform keeps a session's files, and it is exactly where the
           * console's file manager, artifacts, provenance and lineage all look -- keyed on the CONVERSATION the console
           * sends. Passing `runId` gave every run its own directory that nothing was looking at.
           *
           * MEASURED on the PROTAC run: it wrote 3MXF.pdb, 5T35.pdb, JQ1_ideal.sdf and VH032_ideal.sdf into
           * /home/ubuntu/rayca-sessions/max-651f2810c9-6df1bc034801 and the operator reported "no files are generating on
           * the file manager". The files were real the whole time and filed where no endpoint reads.
           *
           * Falls back to the run id, because a workspace nobody can find still beats no workspace.
           */
          RAYCA_SESSION_ID: consoleSessionFor(runId) || runId,
          RAYCA_MAX_CALLBACK: `http://127.0.0.1:${PORT}/max/tool`, RAYCA_RUN_ID: runId, RAYCA_AGENT: 'lead',
          RAYCA_SERVE_KEY: SERVE_KEY || '' },
      },
    },
    /*
     * THE STUDY'S OWN DIRECTORY IS THE WORKING DIRECTORY.
     *
     * WITHOUT THIS, THE SDK'S OWN TOOLS WRITE WHEREVER THE SERVICE STARTED. Governance was wired around the code-running
     * verb, which sets its own cwd; `Bash`, `Write`, `Read` and the rest never went near it. MEASURED on a real
     * retrosynthesis study: `Bash` downloaded 754 MB of AiZynthFinder models into /tmp/aizynth_data, the session workspace
     * held nothing but source files, and the operator asked whether files were 'generated but in another place and never
     * reached the file manager'. They were.
     *
     * A relative path now lands in the study by default, which is the behaviour a scientist expects and the only one the
     * file manager can see. An absolute path still escapes, and that is caught after the fact by registration below.
     */
    cwd: workspacePath || undefined,
    /*
     * GOVERNANCE STILL LIVES HERE, AND NOW FOR A BETTER REASON THAN BEFORE.
     *
     * This block used to explain that governance could not sit in `canUseTool` because `bypassPermissions` shadowed it.
     * That mode is gone -- it was the cause of the headless tool denials, see `permissionMode` above -- and there is now a
     * `canUseTool`, but it answers the SDK's permission question and nothing more.
     *
     * The gate stays in `PreToolUse` because a hook fires in EVERY permission mode, so what may run is not a property of
     * how permissions happen to be configured. That was the right instinct when it was written and it survives the change.
     */
    hooks: {
      // GOVERNANCE RUNS HERE, NOT IN `canUseTool`.
      //
      // MEASURED: with `permissionMode: 'bypassPermissions'` -- documented as "Bypass all permission checks" -- the
      // `canUseTool` callback is never invoked, so a script that declared itself a placeholder ran unchallenged. Hooks
      // fire regardless of permission mode, which is what a gate needs: something the mode cannot switch off.
      /*
       * A GATE THAT BREAKS MUST OPEN, NOT CLOSE, AND IT MUST SAY SO.
       *
       * THE OPERATOR: "the sdk must have permission to run tools and bash and everything freely without waiting for user's
       * permission!" They are right, and what they saw was worse than a permission prompt.
       *
       * MEASURED on run max-23eaa10f67, an Edelris client session. The model called Bash to read a job log and the result came
       * back in 0.121s:
       *
       *   "The user doesn't want to take this action right now. STOP what you are doing and wait for the user to tell you how
       *    to proceed."
       *
       * That is the SDK's own text for a refused tool, and NOTHING IN THIS ENGINE REFUSED IT. Every deny below emits a
       * `refused` event first; that run has none. `permissionMode` is `bypassPermissions`, there is one options object, no
       * deny list is configured and no settings file carries a permissions block -- all checked. What remains is that this
       * hook THREW: the SDK converts a hook that raises into a denial, and the message it substitutes describes a user who
       * declined. So an internal fault was presented to a client as their own permission settings.
       *
       * WHAT THE MODEL DID WITH THAT is the real damage. Told a tool was refused and given a reason about permissions, it
       * reasoned as instructed and told the client to "check what's happening in your Claude Code permission settings" and to
       * paste shell output by hand. Four runs did this. The platform's name for itself is not Claude Code, and a research
       * client should never be asked to run `cat` in a terminal.
       *
       * SO THE CHOICE HERE IS DELIBERATE: on an unexpected error this hook ALLOWS the call. A governance check exists to
       * catch a specific stated wrong -- installing into the shared interpreter, working without a plan, a refusal from
       * governance itself -- and each of those returns its own deny with its own reason. An exception is none of those. It is
       * this code failing, and failing closed means every fault in a check becomes an invisible refusal that the model then
       * explains to a client by inventing a cause.
       *
       * IT IS NOT SILENT. The failure is emitted on the tape as a refusal that did NOT happen, so a reader and I can both
       * see that a gate errored and what it was examining, and it is printed to the service log. A gate that opens quietly
       * is how the next fault stays hidden for a week.
       */
      PreToolUse: [{ hooks: [async (i) => {
        try {
          const decision = await preToolGate(i);
          /* TEMPORARY INSTRUMENTATION: what our own gate answered, for every call. */
          const d = decision?.hookSpecificOutput?.permissionDecision || 'allow';
          console.error(`[max ${runId}] gate ${i?.tool_name} -> ${d}`);
          return decision;
        } catch (err) {
          const { verb, origin } = nameAndOrigin(i?.tool_name);
          const detail = err && err.message ? String(err.message) : String(err);
          console.error(`[max] PreToolUse gate errored for ${runId} on ${verb}: ${detail}`);
          try {
            emit(runId, KINDS.GATE, { agent: 'lead', verb, origin, gate: 'gate_error', advisory: true,
              coaching: true, detail: `a governance check failed and the call was allowed: ${detail}` });
          } catch { /* the tape is not worth failing a tool call for; the console.error above still records it */ }
          return {};
        }
      }] }],
      // A MEMBER'S RESULT MUST REACH GOVERNANCE, or a figure it computed is indistinguishable from one it invented.
      // The lead's results come from its own message stream, so only member results are recorded here; recording both
      // would double every provenance entry and charge the same GPU second twice.
      PostToolUse: [{ hooks: [async (i) => {
        const who = String(i?.agent_id || '');
        /*
         * FILES ARE REGISTERED FOR EVERY TOOL, BEFORE ANYTHING ELSE IN THIS HOOK.
         *
         * This hook used to return immediately when there was no `agent_id`, which meant it only ever saw MEMBERS. The
         * lead's tool calls went entirely unaccounted for, and registration lived inside the code-running verb, so
         * anything written by `Bash`, `Write` or any other SDK tool was invisible to the file manager.
         *
         * MEASURED on a real retrosynthesis study: `Bash` downloaded 754 MB of models into /tmp, eleven scripts ran,
         * and the session workspace contained nothing but those scripts. The operator asked whether files were being
         * "generated but in another place and never reached the file manager". For the models, yes.
         *
         * This is the ONE seam that sees every tool, so it is where filing belongs. `run_python` still registers its
         * own files, and a second attempt finds nothing new because registration diffs against a snapshot.
         */
        /*
         * THE TASK TOOLS ARE ALSO A STATUS FEED, and a more dependable one than the message the loop was dropping.
         *
         * MEASURED on a real run: the `TaskCreated` and `TaskCompleted` hooks fired for all four tasks and NOTHING arrived
         * between them, so a task went straight from not started to done with no visible middle. `TaskUpdate`'s own input
         * carries `status` as pending, in_progress, completed or deleted, plus the ids that block it, and the model does call
         * it. Read here, 'ongoing' is the model's own declaration rather than a guess made from the order of events.
         *
         * AFTER THE TOOL, not before: this hook runs once the call has actually happened, so a status is not claimed for an
         * update that failed.
         */
        noteTaskFromTool(runId, i?.tool_name, i?.tool_input);
        await registerAndAnnounce(runId, sessionKey, verbForFiling(i?.tool_name));
        if (!who) return {};
        const { verb, origin } = nameAndOrigin(i?.tool_name);
        const out = typeof i?.tool_response === 'string' ? i.tool_response : JSON.stringify(i?.tool_response ?? '');
        const seconds = i?.duration_ms ? i.duration_ms / 1000 : 0;
        // Derive a caption for member BACK events the same way the lead's are derived.
        let caption = captionFrom(i?.tool_input);
        if (!caption && i?.tool_input && (verb === 'run_python' || verb === 'run_pipeline' || verb === 'run_on_cluster')) {
          const code = i.tool_input.code ?? i.tool_input.script ?? i.tool_input.source ?? '';
          if (code) {
            const slug = await scriptSlug(code);
            if (slug) caption = slug.replace(/_/g, ' ');
          }
        }
        emit(runId, KINDS.MEMBER_BACK, {
          child: who, agent_type: i?.agent_type || '', verb, origin,
          returned: true, failed_inside: failedInside(out), produced_nothing: producedNothing(out),
          caption: caption || undefined,
          seconds: Math.round(seconds * 1000) / 1000, output: out.slice(0, 12000),
        });
        await governance.afterTool({ runId, verb, origin, output: out, seconds,
          emit: (k, d) => emit(runId, k, { ...d, child: who }) });
        return {};
      }] }],
      SubagentStart: [{ hooks: [async (i) => {
        const cid = i?.agent_id || i?.agentId || '';
        if (cid) members.set(cid, { type: i?.agent_type || i?.subagent_type || 'general', done: false });
        emit(runId, KINDS.SPAWN, { agent: 'lead', child: cid,
          agent_type: i?.agent_type || i?.subagent_type || 'general',
          assignment: String(i?.prompt || i?.description || '').slice(0, 800) });
        return {};
      }] }],
      SubagentStop: [{ hooks: [async (i) => {
        const cid = i?.agent_id || i?.agentId || '';
        if (cid && members.has(cid)) members.get(cid).done = true;
        emit(runId, KINDS.MEMBER_DONE, { child: cid,
          ok: i?.error ? false : true, summary: String(i?.result || i?.summary || '').slice(0, 6000) });
        return {};
      }] }],
      PreCompact: [{ hooks: [async () => {
        // A run that quietly forgets its own history is worse than one that says so.
        emit(runId, KINDS.COMPACT, { phase: 'before', detail: 'the loop is compacting its context' });
        /*
         * AND THE RECORD IS FLUSHED BEFORE THE FORGETTING. This hook announced the compaction and then
         * returned an empty object, so the run said it was about to lose its history and did nothing to
         * preserve it. The manifest is written here, so whatever is on disk is current as of the moment
         * the context was dropped. Re-injecting it afterwards is WS-30 T6.
         */
        await writeRunManifest(runId, 'pre-compact');
        return {};
      }] }],
      /*
       * AFTER THE FORGETTING, THE RUN IS TOLD WHAT IT WAS DOING.
       *
       * `PostCompact` has NO `hookSpecificOutput` variant in this SDK. Checked against the union at
       * sdk.d.ts:7962, which lists SessionStart and Stop among nineteen others and not this event, so the
       * text goes in the top-level `systemMessage`. Getting that wrong would be schema-rejected and the
       * rehydration would silently never arrive, which is the failure mode this whole task exists to end.
       *
       * `compact_summary` is deliberately unused. That summary is the model's own account of the
       * conversation; the point of this hook is to hand back the facts an account cannot carry, namely
       * which phase, which files and which jobs are still open.
       */
      PostCompact: [{ hooks: [async (i) => {
        const text = await rehydrationText(runId,
          'Your context was compacted. This is what this run is, read from disk.');
        emit(runId, KINDS.COMPACT, {
          phase: 'after',
          trigger: String((i && i.trigger) || 'auto'),
          detail: text ? 'the run was re-grounded from its manifest' : 'no manifest to re-ground from',
        });
        return text ? { systemMessage: text } : {};
      }] }],
      /*
       * AND ON EVERY RESUME, for the same reason by a different route.
       *
       * `SessionStart` DOES have a hookSpecificOutput carrying `additionalContext`, so this one uses it.
       * A resumed session has the same problem as a compacted one: the run continues on disk and the
       * model's memory of it does not.
       */
      SessionStart: [{ hooks: [async (i) => {
        const source = String((i && i.source) || 'startup');
        // A FRESH START HAS NOTHING TO REHYDRATE, and injecting an empty manifest into the first turn of a
        // new run would spend context saying nothing.
        if (source === 'startup') return {};
        const text = await rehydrationText(runId,
          `This session ${source === 'resume' ? 'resumed' : `restarted (${source})`}. `
          + 'This is what the run is, read from disk.');
        if (!text) return {};
        return { hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: text } };
      }] }],
      /*
       * A TURN DOES NOT END QUIETLY ON AN UNDOCUMENTED RESULT.
       *
       * WS-30 T8. The decision is a pure function in manifest.mjs so its escapes can be driven directly;
       * this is only the wiring. `decision: 'block'` with a `reason` is a SOFT block: it prevents the stop
       * and feeds the reason back, and the model closes the step and continues. There is no hard refusal
       * anywhere in this workstream, for a measured reason recorded in `stopDecision`.
       *
       * NEVER FAILS A TURN. If the manifest cannot be built, the turn ends. A bookkeeping mechanism that
       * can strand a run is worse than no mechanism.
       */
      Stop: [{ hooks: [async (i) => {
        try {
          const run = store.getRun(runId);
          const events = store.eventsFor(runId);
          const session = (run && (run.console_session || run.session_key)) || '';
          let files = null;
          try { files = await platformStore.filesForRun({ session, runId }); } catch { files = null; }
          const manifest = buildManifest({ runId, run, events, files, readDoc: readDocText });

          const decision = stopDecision({
            manifest,
            stopHookActive: (i && i.stop_hook_active) === true,
            blocksSoFar: stopBlocks.get(runId) || 0,
            /* COUNTED AND ACTUALLY PASSED. The first attempt at this cap incremented the counter and never sent it, so
               the budget defaulted to 0 on every call and 29 advisories went out on one run. */
            advisoriesSoFar: stopAdvisories.get(runId) || 0,
            backgroundTasks: (i && i.background_tasks) || [],
          });
          if (decision.action === 'none') return {};

          /* VISIBLE TO THE OPERATOR EITHER WAY. A mechanism that holds a turn open without saying so on
             the tape is one the reader can only infer from odd behaviour. */
          emit(runId, KINDS.GATE, {
            agent: 'lead',
            kind: 'obligation',
            action: decision.action,
            detail: decision.text,
          });

          if (decision.action === 'block') {
            stopBlocks.set(runId, (stopBlocks.get(runId) || 0) + 1);
            return { decision: 'block', reason: decision.text };
          }
          stopAdvisories.set(runId, (stopAdvisories.get(runId) || 0) + 1);
          return { hookSpecificOutput: { hookEventName: 'Stop', additionalContext: decision.text } };
        } catch (e) {
          console.error('[obligations %s] Stop hook skipped: %s', runId, String((e && e.message) || e));
          return {};
        }
      }] }],
      /*
       * THE STUDY PLAN'S SNAPSHOT. Emitted whenever a task genuinely changes, and not otherwise.
       *
       * The SDK repeats itself: the same completion arrives once from the `TaskCompleted` hook and again in a `task_updated`
       * patch. `noteTask` answers whether the table actually changed, so a repeat writes nothing to the tape.
       */
      TaskCreated: [{ hooks: [async (i) => {
        // THE FIELDS ARE `task_subject` AND `task_description`, not `subject` and `description`. I guessed the shorter
        // names and every task arrived with an EMPTY body, so the run-details checklist rendered a row of blank lines --
        // a list that says a plan exists and cannot say what is in it. Read from the declared hook input instead.
        tasksCreated += 1;
        emit(runId, KINDS.TASK, {
          state: 'created',
          id: String(i?.task_id ?? ''),
          subject: String(i?.task_subject || i?.task_description || '').slice(0, 300),
          assignee: String(i?.teammate_name || '') || undefined,
        });
        noteAndPublishTask(runId, {
          id: i?.task_id,
          subject: i?.task_subject || i?.task_description,
          assignee: i?.teammate_name,
          /* A task the model has only just declared has not started. */
          status: 'pending',
        });
        return {};
      }] }],
      TaskCompleted: [{ hooks: [async (i) => {
        // A completion carries no subject, which is why the reader keeps the text from the creation event.
        emit(runId, KINDS.TASK, {
          state: 'completed',
          id: String(i?.task_id ?? ''),
          subject: String(i?.task_subject || '').slice(0, 300) || undefined,
        });
        noteAndPublishTask(runId, { id: i?.task_id, subject: i?.task_subject, status: 'completed' });
        return {};
      }] }],
    },
  };

  try {
    /*
     * AN ABORT CONTROLLER PER RUN, so cancel can actually stop the work rather than merely record that someone asked.
     *
     * The SDK propagates abort down the agent tree, which is what makes this correct for a team run: aborting the lead
     * stops its members too. Before this there was no controller at all, and the only thing that stopped a live PROTAC
     * team run was restarting the service.
     */
    const rec0 = live.get(runId);
    if (rec0 && !rec0.abort) rec0.abort = new AbortController();
    if (rec0?.abort) options.abortController = rec0.abort;
    for await (const msg of query({ prompt: channel, options })) {
      /*
       * A HEADLESS DENIAL IS NEVER SILENT AGAIN.
       *
       * This message was on the stream for the whole of the defect above and nothing read it, so a tool refused by the
       * SDK looked identical to a tool that simply failed, and the only account of it was the model's guess. Recording it
       * with the SDK's own `decision_reason_type` means the next one names its cause instead of being investigated.
       */
      if (msg.type === 'system' && msg.subtype === 'permission_denied') {
        const why = String(msg.decision_reason_type || 'unknown');
        console.error(`[max ${runId}] SDK denied ${msg.tool_name} headlessly, reason=${why}`);
        emit(runId, KINDS.REFUSED, {
          agent: msg.agent_id ? String(msg.agent_id) : 'lead',
          verb: String(msg.tool_name || ''),
          origin: 'sdk',
          reason: `sdk_${why}`,
          coaching: true,
          detail: `The model was not refused by this platform. The SDK declined ${msg.tool_name || 'a tool'} `
            + `without asking (${why}), which reaches the model as though the reader had refused.`,
        });
      }
      if (msg.type === 'system' && msg.subtype === 'task_updated') {
        /*
         * THE ONLY PLACE A TASK IS EVER REPORTED AS ONGOING, and the loop used to drop it.
         *
         * MEASURED in the SDK's own types: `SDKTaskUpdatedMessage` carries `task_id` and a `patch` whose `status` is one of
         * pending, running, completed, failed, killed or paused. This loop handled `init`, `assistant`, `user` and `result`
         * and ignored everything else, so the only task facts that survived were the two hook ends, created and completed.
         * Nothing could be shown as in progress because nothing ever said so.
         */
        noteAndPublishTask(runId, {
          id: msg.task_id,
          status: msg.patch?.status,
          subject: msg.patch?.description,
          error: msg.patch?.error,
        });
        continue;
      }
      if (msg.type === 'system' && msg.subtype === 'init') {
        // ONCE PER RUN. A spawned member starts its own session and emits its own init, which published a second
        // `ready` claiming the lead had restarted. The first one is the run's.
        if (sessionId) continue;
        sessionId = msg.session_id || '';
        if (sessionId) store.noteSession(runId, sessionId);
        const all = msg.tools || [];
        emit(runId, KINDS.READY, {
          session: sessionId,
          platform_verbs: all.filter((t) => String(t).startsWith('mcp__rayca__')).map((t) => nameAndOrigin(t).verb),
          own_tools: all.filter((t) => !String(t).startsWith('mcp__')),
          agents_available: Object.keys(agents || {}),
        });
      } else if (msg.type === 'assistant') {
        turn += 1;
        for (const blk of msg.message?.content || []) {
          if (blk.type === 'text' && blk.text.trim()) {
            emit(runId, KINDS.SAY, { agent: 'lead', turn, text: blk.text });
          } else if (blk.type === 'thinking' && blk.thinking?.trim()) {
            emit(runId, KINDS.THINK, { agent: 'lead', turn, text: blk.thinking });
          } else if (blk.type === 'tool_use') {
            const { verb, origin } = nameAndOrigin(blk.name);
            verbOf.set(blk.id, blk.name);
            inflight.set(blk.id, { verb, started: Date.now(), input: blk.input });
            // `Agent` is this SDK's delegation tool, not `Task`; the leaked source used the other name and every
            // delegation arrived as a flat tool call. `SubagentStart` publishes the spawn, so this only records.
            if (verb !== 'Agent' && verb !== 'Task') {
              /*
               * CAPTION THE CALL, NOT ONLY THE ANSWER.
               *
               * The slug fallback previously ran when the result came back, so a step whose code carried no comment
               * showed as bare `run_python` on the CALL card and only became readable once it finished. MEASURED on a
               * team run: 5 of 74 tool events still read `run_python`, all of them calls awaiting their result. A card
               * that is unreadable while the work is happening is unreadable exactly when the reader is watching.
               *
               * `captionFrom` is free (it reads the code's first comment). The slug costs one round trip on an already
               * warm bridge, and only when there is no comment to use.
               */
              let caption = captionFrom(blk.input);
              if (!caption) {
                const code = blk.input && typeof blk.input === 'object'
                  ? String(blk.input.code ?? blk.input.script ?? blk.input.source ?? '')
                  : '';
                // UNDERSCORES BECOME SPACES, matching what the result card does. Without this the call read
                // `chem_molfromsmiles` and its own result read `chem molfromsmiles`, which looks like two different
                // steps to anyone scanning the column.
                if (code) {
                  const slug = await scriptSlug(code);
                  if (slug) caption = String(slug).replace(/_/g, ' ');
                }
              }
              emit(runId, KINDS.CALL, {
                agent: 'lead', turn, id: blk.id, verb, origin, input: blk.input,
                ...(caption ? { caption } : {}),
              });
            }
          }
        }
      } else if (msg.type === 'user') {
        for (const blk of msg.message?.content || []) {
          if (blk.type !== 'tool_result') continue;
          const raw = verbOf.get(blk.tool_use_id) || '';
          const { verb, origin } = nameAndOrigin(raw);
          const f = inflight.get(blk.tool_use_id);
          inflight.delete(blk.tool_use_id);
          if (verb === 'Agent' || verb === 'Task') continue; // SubagentStop reports the member
          const body = typeof blk.content === 'string'
            ? blk.content
            : (blk.content || []).map((c) => c.text || '').join('\n');
          // THREE FACTS, KEPT APART. The call returned; the code inside it may still have failed; and it may have
          // succeeded while producing nothing at all, which is what cost a real study 507 events.
          // BETTER TITLE: when no leading comment exists, use the platform's step-name deriver
          // (execisolate._script_slug) via the memory bridge. Falls back to bare verb on bridge failure.
          let caption = captionFrom(f?.input);
          if (!caption && f?.input && (verb === 'run_python' || verb === 'run_pipeline' || verb === 'run_on_cluster')) {
            const code = f.input.code ?? f.input.script ?? f.input.source ?? '';
            if (code) {
              const slug = await scriptSlug(code);
              if (slug) caption = slug.replace(/_/g, ' ');
            }
          }
          emit(runId, KINDS.BACK, {
            agent: 'lead', id: blk.tool_use_id, verb, origin,
            returned: !blk.is_error,
            failed_inside: failedInside(body),
            produced_nothing: producedNothing(body),
            caption: caption || undefined,
            /* MILLISECOND PRECISION, NOT WHOLE SECONDS. `Math.round(ms / 1000)` reported every step faster than half
               a second as 0, and most steps in a study are file reads and small conversions. The operator: "the time it
               shows in the right side of them are all 0 and not real execution time." Measured on run max-c3eca0b57a:
               3 of its 8 completed steps reported 0.
               The console's formatter already renders anything under a second as milliseconds, so it was ready for this
               and had only ever been handed zeroes. Three decimals is exact to the millisecond and keeps float noise
               out of the tape. */
            seconds: f ? Math.round(Date.now() - f.started) / 1000 : null,
            output: body.slice(0, 12000),
          });
          /*
           * A SUBMITTED CLUSTER JOB IS REMEMBERED HERE, ON THE PATH THAT ACTUALLY RUNS.
           *
           * MEASURED, reported by the operator: three jobs submitted to Isambard, 6108784, 6108785 and 6108786, were
           * queued on the cluster and absent from `cluster_jobs` entirely. The only production call to
           * `rememberClusterJob` was inside the GET `/runs/:id/stream` handler, so a job was recorded only if somebody
           * happened to be following that particular run over that particular endpoint at that moment. A fresh run is
           * watched over the POST stream, so nothing recorded it.
           *
           * A WRITE BELONGS ON A WRITE PATH. Recording in a read handler means the record depends on who is looking,
           * which is how three real jobs came to exist on the cluster and nowhere in the engine: the watcher could not
           * follow them, their states were never updated, and `results_into` was never set so nothing could be
           * collected when they finished.
           */
          rememberClusterJobFrom(runId, body);
          await governance.afterTool({ runId, verb, origin, output: body,
            seconds: f ? (Date.now() - f.started) / 1000 : 0, emit: (k, d) => emit(runId, k, d) });
        }
      } else if (msg.type === 'result') {
        /*
         * PRICED FROM THE ROUTER, NOT FROM THE SDK. `modelUsage` carries accurate per-model token counts; the prices come
         * from the deployment's own router config. The SDK's `total_cost_usd` is kept beside it so a divergence is
         * logged rather than discovered by a stopped study.
         */
        const priced = realCostOf(msg);
        if (priced.complete && priced.claimed > 0) {
          const ratio = priced.claimed / Math.max(priced.usd, 1e-9);
          if (ratio > 1.5 || ratio < 0.67) {
            console.error('[pricing %s] the SDK claimed $%s, the router prices say $%s (%sx)',
              runId, priced.claimed.toFixed(4), priced.usd.toFixed(4), ratio.toFixed(1));
          }
        }
        finalResult = { turns: msg.num_turns, ms: msg.duration_ms, cost: priced.usd,
          answer: msg.result || '', error: !!msg.is_error };
        /*
         * THE REAL LIMIT. Checked here because the SDK emits one result per turn, so this is the earliest honest point at
         * which cumulative spend is known. Finishing the channel ends the run cleanly with everything it produced kept,
         * which is what the previous cap did, only at the right number.
         */
        if (priced.usd >= BUDGET_USD) {
          console.error('[pricing %s] real spend $%s reached the $%s limit, stopping',
            runId, priced.usd.toFixed(4), BUDGET_USD);
          emit(runId, KINDS.GATE, { gate: 'budget', state: 'reached', advisory: false,
            detail: 'this run has spent $' + priced.usd.toFixed(2) + ' of its $' + BUDGET_USD + ' limit and stopped' });
          channel.finish();
          continue;
        }
        // A LEAD THAT HAS DELEGATED IS NOT FINISHED.
        //
        // MEASURED: with members outstanding the lead's answer was the single sentence "Awaiting user input." Async
        // members report back INTO the session, so collecting them needs another turn -- which is precisely what the
        // intervention channel exists to provide. Closing here published a team report with no team in it, three runs
        // in a row. `SubagentStop` never fired within four minutes, so completion is detected by the transcripts
        // going quiet rather than by the hook alone.
        const outstanding = [...members.values()].filter((m) => !m.done).length;
        if (outstanding > 0 && !mergeRequested) {
          mergeRequested = true;
          await collectMembers(runId, sessionId, members);
          channel.push('Your specialists have now reported. Read their findings, merge them into one answer, and '
            + 'PRESERVE DISAGREEMENT: where two members reached different conclusions, say so and say why. Do not '
            + 'state any number that no tool produced.');
        } else {
          channel.finish();
        }
      }
    }
    clearInterval(ticker);
    await waitForMembers(runId, members);
    const fin = finalResult || { turns: turn, ms: 0, cost: 0, answer: '', error: true,
      detail: 'the loop ended without reporting a result' };

    // THE ANSWER IS JUDGED BEFORE IT IS PUBLISHED. A capable loop that states a figure nothing computed is more
    // dangerous than one that crashes, because the figure is readable and the crash is not. This is the check the
    // pilot did not have when it reported LigandMPNN sequences at 0.23 confidence with nothing flagging them.
    const verdict = await governance.judge({ runId, answer: fin.answer || '' });
    const spend = await governance.end(runId);
    emit(runId, KINDS.GATE, { gate: 'claim_judgement', advisory: verdict.ok !== false,
      verdict: verdict.verdict, sourced_ok: verdict.ok !== false,
      // `figures` is the three-state answer and `untraced` the raw fact behind it. Both travel, so a reader is never
      // shown "figures sourced" beside a gate listing a figure no tool produced.
      figures: verdict.figures || (verdict.ok === false ? 'unverified' : 'sourced'),
      untraced: verdict.untraced || [],
      // THE COUNTS LEAD, because they are facts. The auditor's verdict was measurably wrong about WHICH figures were
      // the problem on run max-f084f1c06b, so it travels as an opinion beside the arithmetic rather than as the headline.
      traced: verdict.traced ?? null, total_claims: verdict.total_claims ?? null,
      unsourced: verdict.unsourced || [], complaints: verdict.complaints || [],
      claims: verdict.claims ?? null, credits: spend.credits ?? null,
      gpu_seconds: spend.gpu_seconds ?? null,
      detail: verdict.figures === 'unverified'
        ? 'this report states figures that no tool produced'
        : verdict.figures === 'partly_untraced'
          ? 'the headline figures trace to a tool; some other numbers in the text do not, and are listed'
          : 'every figure in this report resolves to a tool that produced it' });
    emit(runId, KINDS.SESSION_END, { ...fin, judged: verdict.verdict,
      figures: verdict.figures || (verdict.ok === false ? 'unverified' : 'sourced'),
      untraced: verdict.untraced || [], figures_ok: verdict.ok !== false });
    store.finishRun(runId, { state: fin.error ? 'error' : 'complete', turns: fin.turns, cost: fin.cost,
      answer: fin.answer });
    pushOutcome = fin.error ? 'failed' : 'completed';
    // MIRROR TO PLATFORM RUNSTORE so the run's final state is visible to files/all and lineage.
    platformStore.lineageEvent({ runId, eventType: fin.error ? 'FAIL' : 'COMPLETE',
      jobName: 'modulon-max run' }).catch(() => {});
    platformStore.updateRun({ runId, state: fin.error ? 'error' : 'complete' }).catch(() => {});
  } catch (e) {
    clearInterval(ticker);
    /*
     * THE READER GETS OUR SENTENCE, NEVER THE SDK'S.
     *
     * This line used to be `String(e?.message || e)`, which put the underlying error straight into the conversation. MEASURED in the
     * runs table, that is how clients came to be shown "Claude Code process aborted by user" when they pressed stop, and "Claude Code
     * returned an error result: API Error: Sonnet 4.6 can't help with this ... anthropic.com/legal/aup" when the model refused --
     * vendor, model version and a link to someone else's usage policy, in a product they are not using.
     *
     * `publicFailure` classifies the fault and returns the platform's own wording for that class, so nothing from the original text
     * can reach a reader. The raw message is logged on the next line, which is where a diagnosis belongs and where it remains
     * available to us.
     */
    const failure = publicFailure(e);
    const detail = failure.text;
    console.error('[run %s] ended in failure (%s): %s', runId, failure.kind, failure.raw);
    // `turn`, NOT `turns`. This line read an identifier that does not exist, so the only path that reports a failure
    // threw its own ReferenceError and took the whole server process with it -- a crash handler that crashes.
    /*
     * THE COST IS KEPT, EVEN WHEN THE RUN THROWS.
     *
     * MEASURED: three of one afternoon's runs recorded $0.0000, and they were the three that ENDED IN ERROR and did the
     * most work -- two EGFR MD runs at 109 and 119 turns. The recorded six hour total of $11.45 understated the truth by
     * roughly $9, and the gap was concentrated in exactly the runs worth knowing the price of.
     *
     * WHY IT WAS LOST. The SDK yields a `result` message carrying `total_cost_usd` and THEN throws
     * "Claude Code returned an error result: ...". The result handler had already captured the figure into
     * `finalResult`; this catch ignored it and wrote a literal 0. The money was spent, measured, and then discarded one
     * line later.
     *
     * This matters more now that spend is bounded by `maxBudgetUsd` rather than a turn count: a run that stops BECAUSE it
     * exhausted its budget is precisely a run whose cost must not be recorded as zero.
     */
    const spent = finalResult && Number.isFinite(finalResult.cost) ? finalResult.cost : 0;
    const ranTurns = finalResult && finalResult.turns != null ? finalResult.turns : turn;
    emit(runId, KINDS.SESSION_END, { turns: ranTurns, ms: finalResult?.ms || 0, cost: spent,
      answer: '', error: true, detail });
    store.finishRun(runId, { state: 'error', turns: ranTurns, cost: spent, answer: detail });
    pushOutcome = 'failed';
    platformStore.updateRun({ runId, state: 'error', error: detail }).catch(() => {});
  } finally {
    const r = live.get(runId);
    if (r) r.finished = true;
    releaseTaskTable(runId);
    /* EVERY OUTCOME, which is why this is here and not on the success path. Awaited so the run is not reported finished before
       its work has been offered to the repository, and incapable of failing the run by construction. */
    try {
      /*
       * THE LIBRARIES GO IN AFTER THE MODEL HAS FINISHED WRITING.
       *
       * A model cannot type 1.3 MB of Plotly, and MEASURED on every dashboard this platform has produced, left to
       * itself it writes `https://cdn.plot.ly` instead. That file shows nothing when opened from disk and makes a
       * reader's browser call a third party while displaying proprietary results. The model writes a placeholder and
       * the vendored bytes are substituted here, once, when nothing is still being written.
       */
      try {
        const files = await platformStore.dashboardFinalise({ session: consoleSessionFor(runId) || runId });
        for (const f of files || []) {
          if ((f.missing || []).length > 0) {
            console.error('[dashboard %s] %s is missing %s, its charts will not render',
              runId, f.file, (f.missing || []).join(', '));
          }
          if ((f.network_refs || []).length > 0) {
            console.error('[dashboard %s] %s still loads %d external reference(s): %s',
              runId, f.file, (f.network_refs || []).length, (f.network_refs || []).slice(0, 3).join(' '));
          }
        }
      } catch (e) {
        console.error('[dashboard %s] finalise failed: %s', runId, String(e && e.message || e));
      }
      // THE RECORD BEFORE THE PUSH, so a run whose push fails still has its manifest on disk.
      await writeRunManifest(runId, 'run end');
      await autoPushToGitHub(runId, consoleSessionFor(runId) || runId, pushOutcome);
    } catch { /* reported inside; a push must never be the reason a finished run looks unfinished */ }
  }
}

/* ------------------------------------------------------------------------------------------------------------------
 * HTTP
 * ---------------------------------------------------------------------------------------------------------------- */

/**
 * Hold a finished lead open until its asynchronous members have reported.
 *
 * WHY THIS IS NEEDED AT ALL. `Agent` returns a launch receipt, not the member's work, so the lead's loop can report a
 * result while its specialists are still running. Measured three times: a team run ended at 22s, 19.5s and 22.1s with
 * the members' findings absent from the answer. A team report containing no team is worse than a single-agent one,
 * because the reader has been told specialists were consulted.
 *
 * BOUNDED, AND HONEST WHEN THE BOUND IS REACHED. A member still working when the budget expires is published as still
 * working: "produced no findings" and "was not waited for" are different facts and only one of them is a result.
 */
/**
 * Stream each member's real work into the tree.
 *
 * WHY POLLING AND NOT ONLY THE HOOK. `SubagentStart` fires immediately and is what makes a delegation visible at once,
 * but `SubagentStop` did not fire within four minutes on a member that was working, so it cannot be the only signal
 * that a member is finished. `getSubagentMessages` carries the turns themselves, which is also the only way to show
 * WHAT a member did rather than merely that it existed. Two quiet polls in a row is the completion signal available.
 */
async function collectMembers(runId, sessionId, members, budgetMs = Number(process.env.MAX_MEMBER_WAIT_MS || 300000)) {
  if (!sessionId) return;
  const deadline = Date.now() + budgetMs;
  const seen = new Map();
  let quiet = 0;
  while (Date.now() < deadline) {
    let ids = [];
    try { ids = await listSubagents(sessionId); } catch { /* not visible yet */ }
    let grew = false;
    for (const id of ids) {
      let msgs = [];
      try { msgs = await getSubagentMessages(sessionId, id); } catch { continue; }
      const already = seen.get(id) || 0;
      if (msgs.length <= already) continue;
      grew = true;
      // TOOL CALLS ARE NOT REPUBLISHED HERE. `PreToolUse` and `PostToolUse` carry `agent_id`, so a member's calls are
      // already attributed and already in governance's record. Emitting them again produced two cards for one call,
      // one labelled with the persona and one with the raw agent id. What this loop still contributes is the member's
      // PROSE, which no hook exposes, and the only available signal that a member has finished.
      for (const m of msgs.slice(already)) {
        for (const blk of m?.message?.content || []) {
          if (blk.type === 'text' && String(blk.text).trim()) {
            emit(runId, KINDS.MEMBER_SAY, { child: id, text: String(blk.text).slice(0, 6000) });
          }
        }
      }
      seen.set(id, msgs.length);
    }
    if (ids.length && !grew) {
      quiet += 1;
      if (quiet >= 2) {
        for (const id of ids) {
          if (members.has(id)) members.get(id).done = true;
          emit(runId, KINDS.MEMBER_DONE, { child: id, ok: true, turns: seen.get(id) || 0 });
        }
        return;
      }
    } else {
      quiet = 0;
    }
    await new Promise((r) => setTimeout(r, 2500));
  }
}

async function waitForMembers(runId, members, budgetMs = Number(process.env.MAX_MEMBER_WAIT_MS || 300000)) {
  if (!members || members.size === 0) return;
  const deadline = Date.now() + budgetMs;
  const outstanding = () => [...members.entries()].filter(([, m]) => !m.done).map(([id]) => id);
  while (Date.now() < deadline) {
    if (outstanding().length === 0) return;
    await new Promise((r) => setTimeout(r, 2000));
  }
  const left = outstanding();
  if (left.length) {
    emit(runId, KINDS.MEMBER_DONE, {
      child: left.join(','), ok: false, still_working: true,
      summary: 'This member was still working when the wait budget ran out. Its findings are NOT in the answer below, '
        + 'and their absence is a limit of how long we waited rather than a scientific result.',
    });
  }
}

function json(res, code, body) {
  const s = JSON.stringify(body);
  res.writeHead(code, { 'content-type': 'application/json', 'content-length': Buffer.byteLength(s) });
  res.end(s);
}

async function readJson(req) {
  let raw = '';
  for await (const c of req) raw += c;
  try { return JSON.parse(raw || '{}'); } catch { return {}; }
}

/*
 * THE CLUSTER JOB WATCHER.
 *
 * WHY IT LIVES HERE. `governance/cluster.py` already has a watcher with backoff polling, and it dies with the process
 * that starts it: the MCP server is spawned PER QUERY, so when a run ended its watcher went and the in-memory job table
 * went with it. MEASURED, on a 12 hour MD job: the submitting run finished, and a later run asking about job 6102452
 * answered "this run did not submit job 6102452, so there is nothing to report on". This process is the long-lived one,
 * and it survives restarts because the jobs are in sqlite rather than in memory.
 *
 * THE OPERATOR: "we should have a watcher to constantly check the hpc job and understand the pending and running
 * difference and when run finished fire the engine to get them analysed after trajectory is generated."
 *
 * ONE TIMER FOR ALL JOBS, not a thread each. A job is polled by asking the scheduler over ssh, which costs a round trip
 * on a login node shared with everyone on the machine, so the interval is deliberately slow and the same tick serves
 * every open job.
 */
/*
 * NOTHING IS RUNNING WHEN THIS PROCESS STARTS, so any row that says otherwise is from a process that is gone. Closed here
 * before anything else, because a stale `running` row makes the restart guard refuse to restart and blocks every later fix.
 */
try {
  const orphans = store.reconcileOrphanedRuns();
  if (orphans.length) {
    console.log('[max] closed ' + orphans.length + ' run(s) left marked running by a previous process: ' + orphans.join(', '));
  }
} catch (e) {
  console.log('[max] orphan reconciliation failed: ' + (e && e.message));
}

const WATCH_EVERY_MS = Number(process.env.MAX_JOB_WATCH_MS || 60_000);
const analysisStarted = new Set();

/*
 * A `KINDS.JOB` event in the shape `toClusterJobEvent` expects.
 *
 * The event is stored in the engine's own snake_case vocabulary; the projection speaks the console's. Converting in one
 * named place keeps the live stream and the replayed tape from drifting, which is how the two ends came to disagree about
 * operation classes earlier in this project.
 */
/*
 * ONE RUN'S EVENTS AS THE CONSOLE READS THEM, including the job rows.
 *
 * Shared by the per-run tape and the session tape so a refresh cannot show one thing and a reload of the same
 * conversation another. `seq` continues across runs, which is what lets a session tape carry several runs in order.
 */
/* One run described as the console's RunSummary, so both tape routes report it identically. */
function runSummary(run, retained, total) {
  return {
    run_id: run.id,
    session_id: run.console_session || '',
    task: run.task || '',
    mode: 'max',
    state: run.state || '',
    started_at: (run.started_ms || 0) / 1000,
    ended_at: run.ended_ms ? run.ended_ms / 1000 : null,
    duration_s: run.ended_ms && run.started_ms ? (run.ended_ms - run.started_ms) / 1000 : null,
    error: null,
    events_retained: retained,
    events_total: total,
    events_dropped: 0,
    truncated: false,
  };
}

function projectRun(runId, startSeq, after, out) {
  let seq = startSeq;
  /*
   * WHAT THE READER ATTACHED, HELD UNTIL THE PROMPT IT BELONGS TO.
   *
   * The engine records attachments as their own event, IMMEDIATELY BEFORE the prompt that carried them -- measured on
   * the tape: `attachments` at n=0, `session.start` at n=1, and the same order for a mid-run follow-up. So the items are
   * remembered when they pass and spent on the next event that is the reader's own words.
   *
   * SPENT, NOT KEPT, because a second prompt with no attachments must not inherit the first one's chips.
   */
  let pendingAttached = null;
  for (const ev of store.eventsFor(runId)) {
    if (ev.kind === KINDS.ATTACHED) {
      pendingAttached = ev.items || [];
    }
    /* The user's words come first, because they are what the run is an answer to. */
    if (ev.kind === KINDS.SESSION_START) {
      const asked = withPromptAttachments(userPromptEvent(ev, seq, runId), pendingAttached);
      if (asked) {
        pendingAttached = null;
        if (seq >= after) out.push(asked);
        seq += 1;
      }
    }
    let one = toConsoleEvent(ev, seq, runId);
    if (one && (one.meta || {}).role === 'user') {
      one = withPromptAttachments(one, pendingAttached);
      pendingAttached = null;
    }
    if (one) {
      if (seq >= after) out.push(one);
      seq += 1;
    }
    if (ev.kind === KINDS.JOB) {
      const je = ev.job_id
        ? toClusterJobEvent(jobFromEvent(ev), seq, runId, ev.at, ev.agent)
        : toJobSubmittedEvent(ev, seq, runId, ev.at, ev.agent);
      if (seq >= after) out.push(je);
      seq += 1;
    }
    if (ev.kind === KINDS.BACK || ev.kind === KINDS.MEMBER_BACK) {
      const cj = clusterJobIn(ev.output);
      if (cj) {
        if (seq >= after) out.push(toClusterJobEvent(cj, seq, runId, ev.at, ev.agent));
        seq += 1;
      }
      for (const d of dispatchesIn(ev.output)) {
        if (seq >= after) out.push(toJobEvent(d, seq, runId, ev.at, ev.agent));
        seq += 1;
      }
    }
  }
  return seq;
}

/*
 * A run's session workspace. Bounded because the process is long lived: the map is only read while a job is being
 * submitted, so old entries are of no use and an unbounded map in a service that runs for days is a slow leak.
 */
const workspaces = new Map();
const MAX_REMEMBERED_WORKSPACES = 500;

/* A run's session workspace, which is both where collected results belong and where the file manager looks. */
function workspaceOf(runId) {
  const known = workspaces.get(runId);
  return known || '';
}

function jobFromEvent(ev) {
  return {
    jobId: String(ev.job_id || ''),
    cluster: String(ev.cluster || ''),
    host: String(ev.host || ''),
    provider: String(ev.provider || ''),
    state: String(ev.state || 'submitted'),
    schedulerState: String(ev.scheduler_state || ''),
    queued: ev.queued === true,
    requested: null,
  };
}

/*
 * WHAT THE RESEARCHER ATTACHED, FOLDED INTO THE TASK AND RECORDED.
 *
 * The console has sent `attachments` on every run for months and `grep attachments server.mjs` found nothing: the field arrived and
 * was read by nobody, so a chip in the composer was a promise the engine never heard. The operator, twice: "non of the reach the
 * engine", and before that "I said read this file attached and the engine said I don't see any files."
 *
 * The briefing goes into the TASK rather than the system prompt, for two reasons that matter later in a long run: it is part of
 * what was asked, so it survives compaction the way the request does, and it appears in the recorded task, so what the model was
 * told is recoverable afterwards instead of being a property of a process that has exited.
 *
 * The event is emitted whether or not anything resolved, because "you attached four things and I found three" is the answer to the
 * question the operator was actually asking.
 */
/*
 * THE ARTIFACT REGISTRY, READ ONCE PER RUN START, so a file attachment resolves by the id the console sent rather than by hunting for
 * its name.
 *
 * MEASURED: a file uploaded from a computer never appears in the session workspace. It lands under `rayca-artifacts/<workspace id>/`,
 * keyed by an id that cannot be derived from the session key, so a directory search found produced files and missed uploaded ones.
 * The registry knows both, and it already carries the absolute path.
 *
 * SYNCHRONOUS BY DESIGN: the listing is fetched once, before the run starts, and turned into a lookup. Doing it per attachment would
 * put several HTTP calls on the path that must not stall, and this path has already cost us a lost registration by waiting.
 */
async function artifactLookup(sessionKey) {
  const key = String(sessionKey || '');
  if (!key || !UPSTREAM || !SERVE_KEY) {
    return null;
  }
  try {
    const res = await fetch(
      `${UPSTREAM}/v1/operational/artifacts?session_id=${encodeURIComponent(key)}`,
      { headers: { Authorization: `Bearer ${SERVE_KEY}`, 'X-Rayca-Session-Id': key } },
    );
    if (!res.ok) {
      return null;
    }
    const body = await res.json();
    const byId = new Map();
    const byName = new Map();
    for (const a of body?.artifacts || []) {
      const at = String(a?.path || '');
      if (!at) continue;
      if (a.id) byId.set(String(a.id), at);
      /* The newest wins for a repeated name, which is what someone attaching "the plot" means. */
      if (a.name) byName.set(String(a.name), at);
    }
    return (id, name) => byId.get(String(id || '')) || byName.get(String(name || '')) || '';
  } catch {
    return null;
  }
}

function withAttachments(runId, task, body, workspace, registry = null) {
  const items = Array.isArray(body?.attachments) ? body.attachments : [];
  if (!items.length) {
    return task;
  }
  let out;
  try {
    out = resolveAttachments(items, { workspace: workspace || '', registry });
  } catch (e) {
    process.stderr.write(`[attach] could not resolve for ${runId}: ${e?.message || e}\n`);
    return task;
  }
  try {
    emit(runId, KINDS.ATTACHED, { items: out.resolved, found: out.found });
  } catch { /* the briefing matters more than the record of it */ }
  return out.briefing ? task + out.briefing : task;
}

async function watchClusterJobs() {
  let open = [];
  try {
    open = store.openClusterJobs() || [];
  } catch {
    return;
  }
  for (const job of open) {
    let got;
    try {
      got = await platformStore.pollClusterJob({
        jobId: job.job_id, provider: job.provider, runId: job.run_id,
        resultsInto: job.results_into || '',
      });
    } catch {
      continue; // a transient ssh failure is not a finished job
    }
    if (!got || !got.ok) {
      continue;
    }
    const state = String(got.state || 'running');
    const sched = String(got.scheduler_state || '');
    // ANNOUNCED ONLY WHEN SOMETHING CHANGED, so a job queued for hours does not fill the tape with one repeated line.
    const changed = state !== job.state || (sched && sched !== job.scheduler_state);
    /* ONE OBJECT FOR BOTH THE ROW AND THE WIRE.
       This is the fourth time a field has been written to storage and dropped on the way to the console:
       `scope` was lost by the console proxy, `quick` was advertised in a schema its dispatch refused,
       `reason` was dropped by runstore_bridge, and `workdirKept` was dropped at updateClusterJob's own
       parameter list. Each was fixed by adding the field in a second place, which is why there was always
       a next one.
       The reason a researcher pays for this is concrete. Two LUMI jobs failed on 2026-09-10 with
       `line 86, exit 31: tee tleap.log` and `line 21, exit 1: return $__lmod_my_status` recorded in
       cluster_jobs, while the console showed only "failed". One run then spent 77 minutes and $7.17
       asking the agent what had gone wrong with a job whose cause was already in the database.
       So the payload is DERIVED rather than restated: whatever is recorded is what is announced. */
    const jobUpdate = {
      state, schedulerState: sched || null,
      files: got.files && got.files.length ? got.files : null,
      /* WHY IT FAILED, straight from the engine's reply. The engine reads it out of the job's own log, which it has just
         collected, so this is a pass-through rather than a second opinion. Null when the job succeeded or said nothing,
         which COALESCE leaves alone rather than blanking a reason recorded earlier. */
      reason: got.reason || null,
      /* WHY A DIRECTORY WAS KEPT, when a sibling job still needed it. Recorded beside the reason so a researcher wondering
         why scratch is filling up has the answer in the same place. */
      workdirKept: got.workdir_kept || null,
    };
    store.updateClusterJob(job.job_id, jobUpdate);
    if (changed) {
      emit(job.run_id, KINDS.JOB, {
        agent: 'lead', tool: job.cluster || 'cluster job', gpu: false,
        job_id: job.job_id, cluster: job.cluster, host: job.host,
        queued: !!got.queued,
        /* SPREAD, so a field added to the row above cannot be forgotten here. `scheduler_state` is kept
           in its snake form beside the spread because existing consumers read that name, and renaming a
           field the console already parses is a separate change from carrying a new one. */
        ...jobUpdate,
        scheduler_state: sched,
        files: got.files || [],
      });
    }
    if (state === 'done' && !analysisStarted.has(job.job_id)) {
      analysisStarted.add(job.job_id);
      await startAnalysisRun(job, got.files || []);
    }
  }
}

/*
 * A FINISHED JOB IS ANALYSED, NOT JUST COLLECTED.
 *
 * The operator: "when run finished fire the engine to get them analysed after trajectory is generated." A trajectory
 * sitting on disk is not a result; the question the job was submitted to answer is still unanswered.
 *
 * THE ANALYSIS RUN CONTINUES THE STUDY. It resumes the submitting run's SDK session, so the model already knows what was
 * simulated, what the system was and why -- rather than being handed a directory of files and asked to guess. It carries
 * the same console session, so the files, the jobs panel and the study plan stay one chain, for the same reason a
 * follow-up forks rather than starting cold.
 */
async function startAnalysisRun(job, files) {
  const parent = store.getRun(job.run_id);
  const names = (files || []).map((f) => String(f).split('/').pop()).filter(Boolean);
  const task = [
    `The cluster job ${job.job_id} you submitted to ${job.cluster || 'the cluster'} has finished`,
    names.length ? `and its outputs are collected: ${names.slice(0, 20).join(', ')}.` : 'but collected no output files.',
    'Analyse what came back and answer the question the job was submitted to answer.',
    'Report only numbers you compute from these files, and write a report of the findings.',
  ].join(' ');
  // Minted the same way every other run id in this file is, so nothing has to know where a run came from.
  const id = 'max-' + Math.random().toString(16).slice(2, 12);
  try {
    store.createRun({ id, task, team: false, model: parent?.model || MODEL });
    if (job.console_session) {
      store.noteConsoleSession(id, job.console_session);
    }
    store.updateClusterJob(job.job_id, { analysisRun: id });
    // Resumed rather than started: the transcript is what makes this an analysis and not a fresh guess.
    /*
     * A FAILED LAUNCH IS RECORDED, NOT SWALLOWED.
     *
     * MEASURED: this read `.catch(() => {})`. The analysis run for job 6102566 was created, never produced a single
     * event, and sat marked `running` for 62 minutes -- and because the rejection was discarded there was nothing
     * anywhere saying why. It then blocked the restart guard, which refused to restart while a run appeared to be in
     * flight. Swallowing the error cost more than the error.
     */
    /*
     * REGISTERED BEFORE IT IS RUN, WHICH THIS PATH ALONE FORGOT.
     *
     * MEASURED 2026-09-05: 14 of one researcher's 15 errored runs yesterday were this, every one reading "the follow-up
     * analysis could not start: Cannot set properties of undefined (setting 'queue')". `runTask` does `const rec =
     * live.get(runId)` and then `rec.queue = channel`, so a run id it has never seen throws immediately. The other three
     * callers all `live.set(...)` on the line before; this one did not, so the analysis after a cluster job could NEVER start
     * and has been failing on every completed job.
     *
     * The error was at least recorded rather than swallowed, which is why it was findable at all -- an earlier version of this
     * catch read `.catch(() => {})` and cost 62 minutes of a run sitting marked `running` with nothing saying why.
     */
    live.set(id, { listeners: new Set(), n: 0, queue: null, finished: false });
    runTask(id, task, false, parent?.session_id || '', parent?.model || MODEL).catch((e) => {
      const detail = 'the follow-up analysis could not start: ' + String(e?.message || e).slice(0, 400);
      try {
        store.finishRun(id, { state: 'error', turns: null, cost: 0, answer: detail });
        emit(id, KINDS.SESSION_END, { turns: 0, ms: 0, cost: 0, answer: '', error: true, detail });
      } catch { /* the record is best effort; the log below is the floor */ }
      console.log('[max] analysis run ' + id + ' for job ' + job.job_id + ' failed to start: ' + detail);
    });
  } catch {
    /* A failure to launch the analysis must not stop the watcher following other jobs. */
  }
}

setInterval(() => { watchClusterJobs().catch(() => {}); }, WATCH_EVERY_MS).unref();


const server = createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x');
  const path = url.pathname;

  // The liveness probes carry no run data and are what a supervisor uses to decide whether to restart, so they stay
  // open. Everything that can start work, read a transcript or steer a run requires the key.
  const OPEN = new Set(['/healthz', '/max/health']);
  if (!OPEN.has(path) && !authorised(req)) {
    return json(res, 401, { error: 'unauthorised',
      detail: 'this engine runs code and spends money; send Authorization: Bearer <RAYCA_SERVE_KEY>' });
  }

  if (req.method === 'GET' && (path === '/' || path === '/index.html')) {
    res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
    return res.end(readFileSync(join(HERE, 'ui.html')));
  }

  // ---------------------------------------------------------------------------------------------------------------
  // THE SURFACE THE CONSOLE ALREADY SPEAKS
  //
  // The console proxies /api/rayca/engine/operational/stream to ${RAYCA_ENGINE_URL}/v1/operational/stream, so serving
  // this endpoint makes the existing console able to drive this engine by changing one environment variable. No
  // console code is touched and the current engine stays the default.
  // ---------------------------------------------------------------------------------------------------------------

  if (req.method === 'GET' && path === '/v1/models') {
    return json(res, 200, { object: 'list', data: [{ id: 'modulon-max', object: 'model', owned_by: 'rayca' }] });
  }

  if (req.method === 'GET' && path === '/healthz') {
    // Named as the operator engine names it, so the same probes work against either.
    return json(res, 200, { status: 'ok', engine: 'modulon-max', personas: PERSONAS.length, model: MODEL,
      active_runs: [...live.keys()].filter((k) => !live.get(k).finished) });
  }

  if (req.method === 'POST' && path === '/v1/operational/stream') {
    const body = await readJson(req);
    let task = String(body.task || '').trim();
    if (!task) return json(res, 400, { error: 'no_task' });
    /*
     * WHAT THE MODEL READS IS NOT WHAT THE READER SEES.
     *
     * THE OPERATOR: "when i clicked on it it submited to prompts, one short and one long one. i do not want the user to
     * see this long prompt." They were right. A capability brief is 8566 characters, and storing it as the run's task put
     * the whole standard into the conversation as though the user had typed it. It also poisons everything else that
     * reads the task: the session title is generated from it, so a study would be named after a specification.
     *
     * The ASKED task is kept for everything a person or another feature reads. The expansion goes only to the model.
     */
    const askedTask = task;
    /*
     * "GENERATE DASHBOARD" IS ONE CLICK, NOT A PARAGRAPH THE USER HAS TO WRITE.
     *
     * THE OPERATOR: "it is hard for the user to set the bars high everytime, i can do it but not all people are able to
     * do it with prompting, so i need a systematic way of doing it and user just call this and engine will generate
     * this". So the standard lives in the engine. The console sends `intent: 'dashboard'` and the researched brief,
     * including this session's own artifact inventory, is prepended here.
     *
     * THE USER'S OWN WORDS SURVIVE. Anything they typed is appended under a heading, so a request like "focus on the
     * top twenty" still lands while the standard still applies.
     */
    task = await expandForIntent(body, task, body.session_id || req.headers['x-rayca-session-id'] || '');
    const id = 'max-' + Math.random().toString(16).slice(2, 12);
    // TEAM MODE ARRIVES AS A DECLARED FIELD. The console's composer sends it explicitly; it is never inferred from the
    // wording of a task, because a researcher who did not ask for a team should not be charged for one.
    const team = body.team === true || body.team_mode === true;
    // THE MODEL THAT WILL ACTUALLY RUN is recorded, not the configured constant. The column used to say sonnet
    // whatever was chosen, so the record was confidently wrong about what produced the results.
    const chosenModel = modelFrom(body);
    const chosenTemp = temperatureFrom(body);
    // STORED AS ASKED, so the conversation, the title and every listing show the request rather than the specification.
    store.createRun({ id, task: askedTask, team, model: chosenModel });
    /*
     * THE CONVERSATION THIS RUN BELONGS TO, which is a different thing from the transcript it will build.
     *
     * The console asks "which runs belong to this chat" through GET /v1/operational/runs?session_id=X, and X is the
     * CONVERSATION. Without recording it, that question fell through the front door to the previous engine, which has
     * never heard of a `max-` run, and answered `runs: []` -- so reloading the page mid-run lost the run and a forked run
     * executed with nothing in the browser showing it. The live stream was the only way any run here was ever visible.
     */
    store.noteConsoleSession(id, body.session_id || req.headers['x-rayca-session-id'] || '');
    // REGISTER IN THE PLATFORM RUN STORE so files/all, artifacts and lineage can see this run.
    // MEASURED: without this, runstore.store().sessions() returned no max-* runs and the file manager
    // was empty even though files were correctly written. The session_key is the CONVERSATION id,
    // which is what workspace_for() and every file endpoint uses to locate artifacts.
    const consoleSession = body.session_id || req.headers['x-rayca-session-id'] || '';
    // LINEAGE START. One identity per run, which is what WS-3 is for; the emitter promises never to raise and a
    // failure here must never touch the run, so it is fire and forget.
    platformStore.lineageEvent({ runId: id, eventType: 'START', jobName: 'modulon-max run' }).catch(() => {});
    platformStore.registerRun({ runId: id, sessionKey: consoleSession, task: askedTask, state: 'running',
      createdAt: Date.now() }).catch((e) => process.stderr.write(
      `[runstore] register failed for ${id}: ${e?.message || e}\n`));
    live.set(id, { listeners: new Set(), n: 0, queue: null, finished: false });

    res.writeHead(200, { 'content-type': 'text/event-stream', 'cache-control': 'no-cache', connection: 'keep-alive' });
    // The run id goes first so the console can steer or fork this run later; it is a status frame so a reader that
    // does not care simply shows it.
    let seq = 0;
    res.write('data: ' + JSON.stringify({ v: OPS_SCHEMA_VERSION, seq: seq++, ts: Date.now() / 1000, run_id: id,
      type: 'status', node: 'lead', title: 'run accepted', body: id, status: 'running',
      meta: { stage: 'accepted', run: id, engine: 'modulon-max', steerable: true } }) + '\n\n');

    const rec = live.get(id);
    /* Held until the prompt it belongs to, exactly as the replay does it. See `projectRun`: the two must agree, or a
       chip would appear on a reload and not while the run is going, or the other way round. */
    let pendingAttached = null;
    const send = (ev) => {
      if (ev.kind === KINDS.ATTACHED) {
        pendingAttached = ev.items || [];
      }
      /* Live and replayed tapes must agree, so the prompt is emitted here exactly as the replay emits it. */
      if (ev.kind === KINDS.SESSION_START) {
        const asked = withPromptAttachments(userPromptEvent(ev, seq, id), pendingAttached);
        if (asked) {
          pendingAttached = null;
          seq += 1;
          res.write('data: ' + JSON.stringify(asked) + '\n\n');
        }
      }
      let out = toConsoleEvent(ev, seq, id);
      if (out && (out.meta || {}).role === 'user') {
        out = withPromptAttachments(out, pendingAttached);
        pendingAttached = null;
      }
      if (out) { seq += 1; res.write('data: ' + JSON.stringify(out) + '\n\n'); }
      // A CONTAINER DISPATCH IS A JOB, AND THE JOBS PANEL CANNOT SEE IT OTHERWISE. This engine dispatches through
      // run_python calling the platform's toolkit, so the facts arrive as `[dispatch]` markers in the tool's output
      // rather than as the courier meta the previous engine emitted. Without this the Jobs section was empty on every
      // run, while the run had put a container on an A100.
      if (ev.kind === KINDS.BACK || ev.kind === KINDS.MEMBER_BACK) {
        /*
         * A SCHEDULER JOB IS A JOB TOO. `run_on_cluster` returns the scheduler's id as JSON rather than printing the
         * `[dispatch]` marker a container prints, so the loop below never saw one. MEASURED: the operator's
         * EGFR/erlotinib run queued job 6102452 on Isambard and the Jobs panel showed nothing, zero job events for
         * the whole run, while runStructure.ts had carried jobId, cluster and jobState fields for it all along.
         * Read from the same tool result at the same moment, so both kinds of job reach the panel symmetrically.
         */
        const cj = clusterJobIn(ev.output);
        if (cj) {
          /*
           * REMEMBERED THE MOMENT IT IS SEEN, so the watcher can follow it after this run ends.
           *
           * A 12 hour job outlives the run that submitted it by design. Recording it here rather than in the run's
           * memory is what turns "this run did not submit job 6102452" into an answer.
           */
          try {
            store.rememberClusterJob({
              jobId: cj.jobId, runId: id, consoleSession: consoleSessionFor(id),
              cluster: cj.cluster, provider: cj.provider, host: cj.host,
              state: cj.state, schedulerState: cj.schedulerState,
              /*
               * THE SESSION WORKSPACE IS WHERE RESULTS BELONG, and recording it now is what makes collection possible
               * later. MEASURED: without it the watcher asked for collection into an empty path and job 6102566
               * completed having collected nothing. It is also the directory the file manager reads, so a collected
               * trajectory appears beside the inputs that produced it rather than somewhere only the watcher knows.
               */
              resultsInto: workspaceOf(id),
            });
          } catch {
            /* Following a job is a bonus; failing to record one must not break the stream carrying it. */
          }
          res.write('data: ' + JSON.stringify(toClusterJobEvent(cj, seq, id, ev.at, ev.child ? (ev.agent_type || ev.child) : '')) + '\n\n');
          seq += 1;
        }
        for (const d of dispatchesIn(ev.output)) {
          res.write('data: ' + JSON.stringify(toJobEvent(d, seq, id, ev.at, ev.child ? (ev.agent_type || ev.child) : 'lead')) + '\n\n');
          seq += 1;
        }
      }
      // THE JOB'S BIRTH, so the panel has a row while the container still runs rather than only after it exits.
      if (ev.kind === KINDS.JOB) {
        // Same distinction as the replay: a scheduler job carries `job_id`, a container submission does not.
        res.write('data: ' + JSON.stringify(ev.job_id
          ? toClusterJobEvent(jobFromEvent(ev), seq, id, ev.at, ev.agent)
          : toJobSubmittedEvent(ev, seq, id, ev.at, ev.agent)) + '\n\n');
        seq += 1;
      }
      if (ev.kind === KINDS.SESSION_END) {
        res.write('data: [DONE]\n\n');
        res.end();
      }
    };
    rec.listeners.add(send);
    req.on('close', () => rec.listeners.delete(send));
    runTask(id, task, team, '', chosenModel, chosenTemp, body.attachments).catch((e) => {
      const detail = String(e?.message || e).slice(0, 600);
      try {
        emit(id, KINDS.SESSION_END, { turns: null, ms: 0, cost: 0, answer: '', error: true, detail });
        store.finishRun(id, { state: 'error', turns: null, cost: 0, answer: detail });
        platformStore.updateRun({ runId: id, state: 'error', error: detail }).catch(() => {});
      } catch { /* the run is unrecoverable; the server stays up */ }
      const r = live.get(id);
      if (r) r.finished = true;
      releaseTaskTable(id);
    });
    return undefined;
  }

  // REATTACH, WHICH IS WHAT A BROWSER REFRESH NEEDS. The console proxies
  // /v1/operational/runs/<id>/stream?after=<n>, and without it a reload shows an empty run that is still going. That
  // exact failure froze a healthy 222-event run in the previous console.
  /*
   * THE TAPE, REBUILT AFTER A REFRESH, SERVED FROM OUR OWN STORE.
   *
   * MEASURED, and it had been broken for every run since this loop replaced the old one. The operator reloaded the page
   * and "the submitted job was gone from the job section. also the recent cards including the asnwer to the run was
   * gone!!"
   *
   * WHY. This path is not one of the four loop endpoints, so it fell through to the passthrough and was answered by the
   * OLD engine on 8201. That engine holds the run's METADATA, because runs are mirrored to it for lineage, and none of
   * its events. Asking it directly returned the correct task and duration alongside `events_retained: 0,
   * events_total: 0` while this engine's store held 270 events for the same run. Nothing was lost; recovery looked in
   * the wrong place.
   *
   * Only visible on a reload: while the stream is open the console holds the events in memory and everything renders.
   *
   * THE JOB PROJECTIONS ARE REPLAYED TOO. The Jobs panel is built from the tape, so replaying only the conversation
   * would bring the cards back and leave the panel empty -- which is half the symptom the operator reported. Container
   * dispatches and scheduler jobs are re-derived here exactly as the live stream derives them.
   */
  if (req.method === 'GET' && /^\/v1\/operational\/runs\/[^/]+\/tape$/.test(path)) {
    const runId = path.split('/')[4];
    const after = Number(url.searchParams.get('after') || 0);
    const run = store.getRun(runId);
    if (!run) return json(res, 404, { error: 'no_such_run' });
    const events = [];
    const total = projectRun(runId, 0, after, events);
    return json(res, 200, { run: runSummary(run, events.length, total), events, after_index: total });
  }

  /*
   * THE WHOLE CONVERSATION, WHICH IS WHAT THE CONSOLE ASKS FOR FIRST.
   *
   * MEASURED, and my first attempt at this fixed the wrong route. The operator refreshed and the cards and the job row
   * did not come back. `useRunTape` tries the SESSION tape first and falls back to the per-run one only when the session
   * route fails -- and the passthrough answered it with HTTP 200 and an empty event list, which is a valid response, so
   * the fallback never ran. A route that fails cleanly would have degraded to something; one that succeeds emptily
   * cannot.
   *
   * The console's own comment says why it wants the session: "A conversation's events are spread across one run per
   * prompt, so restoring from a single run's tape dropped every earlier turn on refresh." Every run of the conversation
   * is replayed here in submission order, with `seq` continuing across them so the reducer sees one tape.
   */
  if (req.method === 'GET' && /^\/v1\/operational\/sessions\/[^/]+\/tape$/.test(path)) {
    const sess = decodeURIComponent(path.split('/')[4]);
    const after = Number(url.searchParams.get('after') || 0);
    const runs = store.runsForConsoleSession(sess) || [];
    if (!runs.length) return json(res, 200, { run: null, events: [], after_index: 0 });
    const events = [];
    let seq = 0;
    for (const r of runs) {
      /*
       * EVERY RUN NUMBERED FROM ZERO, exactly as that run's OWN stream numbers it.
       *
       * MEASURED, and this is why a refreshed page went dead. `seq` used to continue across the runs of a session, so the same
       * event carried one number here and a different one on `/runs/<id>/stream`: the second run's first event was seq 34 on
       * this route and seq 0 on its own. A console that identifies an event by (run, seq) therefore could not tell the replayed
       * copy from the live one, and could not use the number it held as a resume cursor either.
       *
       * NOTHING NEEDED THE RUNNING TOTAL. It was introduced so the console could order a multi-run tape by seq alone, and the
       * console stopped doing that when interleaving was fixed: it groups by run and places each run by the earliest timestamp
       * among its own events. `after_index` is read by no caller.
       */
      seq += projectRun(r.run_id, 0, after, events);
    }
    // The LATEST run, because the console's progress and stop controls act on it.
    const newest = store.getRun(runs[runs.length - 1].run_id);
    return json(res, 200, {
      run: newest ? runSummary(newest, events.length, seq) : null,
      events,
      after_index: seq,
    });
  }

  if (req.method === 'GET' && /^\/v1\/operational\/runs\/[^/]+\/stream$/.test(path)) {
    const runId = path.split('/')[4];
    const after = Number(url.searchParams.get('after') || 0);
    const run = store.getRun(runId);
    if (!run) return json(res, 404, { error: 'no_such_run' });
    res.writeHead(200, { 'content-type': 'text/event-stream', 'cache-control': 'no-cache', connection: 'keep-alive' });
    /*
     * THE SAME PROJECTION THE TAPE USES.
     *
     * This loop was a second copy of it, and copies drift: it had neither the job rows nor the user's prompt, so a run
     * recovered through this route showed a different conversation from the same run recovered through the tape. One
     * projection means one answer.
     */
    const replay = [];
    let seq = projectRun(runId, 0, after, replay);
    for (const out of replay) {
      res.write('data: ' + JSON.stringify(out) + '\n\n');
    }
    const rec = live.get(runId);
    if (!rec || rec.finished) {
      res.write('data: [DONE]\n\n');
      return res.end();
    }
    /* Same holding rule as the replay and the run stream. */
    let pendingAttached = null;
    const send = (ev) => {
      if (ev.kind === KINDS.ATTACHED) {
        pendingAttached = ev.items || [];
      }
      if (ev.kind === KINDS.SESSION_START) {
        const asked = withPromptAttachments(userPromptEvent(ev, seq, runId), pendingAttached);
        if (asked) { pendingAttached = null; seq += 1; res.write('data: ' + JSON.stringify(asked) + '\n\n'); }
      }
      let out = toConsoleEvent(ev, seq, runId);
      if (out && (out.meta || {}).role === 'user') {
        out = withPromptAttachments(out, pendingAttached);
        pendingAttached = null;
      }
      if (out) { seq += 1; res.write('data: ' + JSON.stringify(out) + '\n\n'); }
      if (ev.kind === KINDS.SESSION_END) { res.write('data: [DONE]\n\n'); res.end(); }
    };
    rec.listeners.add(send);
    req.on('close', () => rec.listeners.delete(send));
    return undefined;
  }

  if (req.method === 'GET' && path === '/max/health') {
    return json(res, 200, { ok: true, personas: PERSONAS.length, model: MODEL,
      live: [...live.keys()].filter((k) => !live.get(k).finished), db: DB });
  }

  if (req.method === 'GET' && path === '/max/runs') {
    return json(res, 200, { runs: store.listRuns(Number(url.searchParams.get('limit') || 50)) });
  }

  // ALIASED UNDER /v1/operational SO THE CONSOLE CAN REACH THEM. The console forwards a declared list of
  // `/v1/operational/*` paths; `/max/*` is this engine's own surface and the browser has no route to it. One handler,
  // two paths, rather than a second implementation that can drift from the first.
  if (req.method === 'GET' && (path === '/max/sessions' || path === '/v1/operational/sessions/list')) {
    /*
     * OUR RUNS, NOT EVERY SESSION ON THE HOST.
     *
     * MEASURED: `listSessions()` returns 5,859 entries here -- every Claude Code session this machine has ever held,
     * including the ones the operator's own coding agent created. Surfacing that as "your sessions" would bury a
     * researcher's dozen studies in thousands of unrelated transcripts.
     *
     * AND IT RETURNS OBJECTS, NOT STRINGS, despite being typed `Promise<string[]>`. My first version passed those
     * objects straight to `getSessionInfo`, which is why every entry came back null. The id is on `sessionId`.
     */
    const runs = store.listRuns(Number(url.searchParams.get('limit') || 40));
    const out = [];
    for (const r of runs) {
      const entry = {
        run: r.id, task: r.task, team: !!r.team, state: r.state, model: r.model,
        started_ms: r.started_ms, ended_ms: r.ended_ms, turns: r.turns, cost: r.cost,
        session: r.session_id || null,
        // A run with no session cannot be resumed or forked, and saying so is better than offering a button that fails.
        resumable: !!r.session_id, forkable: !!r.session_id,
      };
      if (r.session_id) {
        try {
          const info = await getSessionInfo(r.session_id);
          if (info) {
            entry.summary = info.summary ?? null;
            entry.last_modified_ms = info.lastModified ?? null;
          }
        } catch { /* a session file that has been rotated away is not an error, just not resumable detail */ }
      }
      out.push(entry);
    }
    return json(res, 200, { sessions: out });
  }

  // WHERE A MEMBER'S WORK BECOMES PART OF THE RECORD. Reported by the MCP server that served the call, so a member's
  // dispatches reach governance exactly as the lead's do. Without this, a figure a member computed was
  // indistinguishable from one it invented, because provenance had never seen the tool result.
  /*
   * A PROGRESS BEAT FROM A STEP THAT IS STILL RUNNING.
   *
   * The child process has always produced this -- `_run_cancellable` beats every fifteen seconds with the last 4000
   * characters of stdout -- and `run_isolated` had no parameter to forward it, so nothing could ask. What reached the
   * console instead was a twenty-second ticker carrying elapsed seconds and no content. On the operator's CPTAC run a
   * step took 141 seconds and the reader could learn only that it was still going.
   *
   * A BEAT IS NOT A RESULT. It carries a partial tail that the next beat supersedes, so it is recorded as progress and
   * never as what the step returned.
   */
  /*
   * ONE FILE, ANNOUNCED THE MOMENT IT IS REGISTERED.
   *
   * THE CONSOLE HAS ALWAYS KNOWN HOW TO READ THIS. `artifactTypes.ts` reads `meta.observed` and even explains why it
   * exists: "the engine now also announces each file the MOMENT it appears ... which is what makes the file show up
   * while the run is still working rather than when its step closes". That was built for the previous engine, and
   * modulon-max never emitted it, so the only path left was a four second poll that runs ONLY while streaming. Same
   * shape of defect as the missing step card: the console was ready and this side spoke a different dialect.
   *
   * ONE EVENT PER FILE, because that is the shape the reader's dedupe is written against: it keys on name so a
   * rewritten file collapses to its latest announcement in the file list while the timeline keeps every rewrite.
   */
  if (req.method === 'POST' && path === '/max/file') {
    const b = await readJson(req);
    const runId = String(b.run_id || '');
    if (!runId || !store.getRun(runId)) return json(res, 404, { error: 'no_such_run' });
    const f = b.file && typeof b.file === 'object' ? b.file : null;
    if (!f || !f.name) return json(res, 400, { error: 'no_file' });
    emit(runId, KINDS.FILE, { agent: String(b.agent || 'lead'), file: f });
    return json(res, 200, { ok: true });
  }

  /*
   * A CONTAINER JOB SAYS IT HAS STARTED, rather than being discovered once it has finished.
   *
   * THE OPERATOR, twice. First: "the jobs section only displays the job when it is finished, not when it is submitted,
   * and doesn't notify the user that the job is submitted and it's running -- this is a big problem." Then, after
   * watching RFdiffusion run on the A100 while the panel said the dispatch never reached a container: the panel should
   * "show the jobs once submitted and in real time show the resource usage on the vm and also say the name of the VM".
   *
   * WHY IT COULD NOT WORK BEFORE. The Jobs panel was built from `dispatchesIn()`, which parses the `[dispatch]` marker
   * out of a tool's OUTPUT TEXT, and output exists only once the container has exited. A row therefore could not exist
   * while the job ran, no matter what the panel did, and with no row there was nowhere to put the host, the elapsed
   * time or the files. This endpoint gives the row a birth, so the rest has somewhere to live.
   *
   * `dispatch.announce_dispatch` already existed and already wrote a `dispatch_submitted` row to the narration spool,
   * carrying a docstring quoting the operator's first complaint. `run_isolated` already had an `on_live` callback that
   * pumps that spool every 0.25 seconds. Neither end was connected to the other. This is the join.
   */
  /*
   * CANCEL A CONTAINER JOB. The operator: "a botton to cancell the run so user can control the remove jobs."
   *
   * WHY THIS IS SAFE TO EXPOSE. It stops one named container on the dispatch host and nothing else. The name arrives
   * from the console, which learned it from that job's own progress beat, so the researcher is stopping the job they
   * were looking at. The bridge validates the name's shape before it reaches a shell.
   *
   * THE RESULT IS PASSED THROUGH UNCHANGED, including a failure. "Cancelled" has to mean the container stopped, and a
   * researcher who is told it stopped when it did not will come back to a GPU that is still busy.
   */
  /*
   * TWO PATHS, ONE HANDLER. `/max/*` is this engine's own surface, reachable only from inside the host; the console
   * reaches the engine exclusively through a proxy that forwards named `/v1/operational/*` routes. A cancel button in
   * the browser therefore needs the operational path, and duplicating the handler to get it would be two places to
   * change when the semantics do.
   */
  /*
   * WHAT IS THAT JOB DOING, asked by anyone, at any time.
   *
   * MEASURED: a 12 hour MD job was queued on Isambard, the submitting run finished, and a LATER run asking about job
   * 6102452 was told "this run did not submit job 6102452, so there is nothing to report on". The job table lived in a
   * module-level dict inside the MCP server, which is spawned per query, so the record died with the run.
   *
   * Answered from the durable record, which the watcher keeps current, so the answer outlives the run, the process and a
   * restart.
   */
  if (req.method === 'GET' && (path === '/max/jobs' || path === '/v1/operational/jobs')) {
    let rows = [];
    try {
      rows = store.openClusterJobs() || [];
    } catch {
      rows = [];
    }
    return json(res, 200, { jobs: rows });
  }

  if (req.method === 'GET' && (path.startsWith('/max/job/') || path.startsWith('/v1/operational/job/'))) {
    const jobId = path.split('/').pop();
    const rec = store.getClusterJob(jobId);
    if (!rec) {
      return json(res, 404, { error: 'unknown_job', detail: `no record of cluster job ${jobId} on this engine` });
    }
    return json(res, 200, rec);
  }

  if (req.method === 'POST' && (path === '/max/job/cancel' || path === '/v1/operational/job/cancel')) {
    const b = await readJson(req);
    const container = String(b.container || '');
    if (!container) return json(res, 400, { error: 'no_container' });
    const out = await platformStore.cancelContainer(container);
    return json(res, out && out.ok ? 200 : 502, out);
  }

  if (req.method === 'POST' && path === '/max/job') {
    const b = await readJson(req);
    const runId = String(b.run_id || '');
    if (!runId || !store.getRun(runId)) return json(res, 404, { error: 'no_such_run' });
    const tool = String(b.tool || '');
    if (!tool) return json(res, 400, { error: 'no_tool' });
    emit(runId, KINDS.JOB, {
      agent: String(b.agent || 'lead'),
      tool,
      /*
       * ABSENT, NOT FALSE. `!!b.gpu` turned "this beat said nothing about GPU" into "this job is on CPU", and the console
       * composes the card's title from that flag. MEASURED on run max-604740ffad: the submission reported gpu=True and
       * all eleven progress beats reported gpu=False, so a GPU job was titled "deep-viscosity on CPU" for its whole life.
       * A beat reports PROGRESS. Where the job was sent was settled at submission and is not a beat's to restate.
       */
      gpu: b.gpu === undefined ? undefined : !!b.gpu,
      image: String(b.image || ''),
      // THE MACHINE IS NAMED, because "a job is queued" is not something a researcher can act on or verify without it.
      host: String(b.host || ''),
      /*
       * THE SAME ENDPOINT CARRIES THE BEATS, because a submission and its progress are two reports about ONE job and
       * the panel joins them on the tool. Absent on the first report and present thereafter, so a field that has not
       * been measured stays undefined rather than being sent as a zero that reads as a real measurement.
       */
      container: b.container ? String(b.container) : undefined,
      /*
       * THE OUTCOME, AND THE ONE FIELD THAT DECIDES WHETHER A JOB EVER FINISHES ON SCREEN.
       *
       * `rc` and `state` were not read here at all, so even once the sender forwarded them they had nowhere to land.
       * Both ends were shut: the sender hardcoded `state: running` and dropped rc, and this handler would have
       * ignored them regardless.
       *
       * ABSENT, NOT ZERO, for the same reason it is absent on a submission: a running job has no exit code, and 0
       * means success. `Number.isFinite` is the test rather than truthiness, because rc=0 is the commonest real value
       * and `b.rc || undefined` would have erased precisely the successes.
       */
      rc: Number.isFinite(Number(b.rc)) ? Number(b.rc) : undefined,
      state: b.state ? String(b.state) : undefined,
      detail: b.detail ? String(b.detail).slice(0, 300) : undefined,
      elapsed_s: Number.isFinite(Number(b.elapsed_s)) ? Number(b.elapsed_s) : undefined,
      tail: b.tail ? String(b.tail).slice(0, 4000) : undefined,
      gpu_util_pct: Number.isFinite(Number(b.gpu_util_pct)) ? Number(b.gpu_util_pct) : undefined,
      gpu_mem_used_mb: Number.isFinite(Number(b.gpu_mem_used_mb)) ? Number(b.gpu_mem_used_mb) : undefined,
      gpu_mem_total_mb: Number.isFinite(Number(b.gpu_mem_total_mb)) ? Number(b.gpu_mem_total_mb) : undefined,
    });
    return json(res, 200, { ok: true });
  }

  if (req.method === 'POST' && path === '/max/progress') {
    const b = await readJson(req);
    const runId = String(b.run_id || '');
    if (!runId || !store.getRun(runId)) return json(res, 404, { error: 'no_such_run' });
    emit(runId, KINDS.PROGRESS, {
      agent: String(b.agent || 'lead'),
      verb: String(b.verb || ''),
      seconds: Number(b.seconds || 0),
      tail: String(b.tail || '').slice(0, 4000),
    });
    return json(res, 200, { ok: true });
  }

  if (req.method === 'POST' && path === '/max/tool') {
    const b = await readJson(req);
    const runId = String(b.run_id || '');
    const agent = String(b.agent || 'lead');
    if (!runId || !store.getRun(runId)) return json(res, 404, { error: 'no_such_run' });
    // ATTRIBUTION COMES FROM THE HOOKS, NOT FROM HERE. Members share the parent's MCP server -- both register it as
    // `rayca` -- so this label is always `lead` and cannot identify a member. Kept as a record of what the platform
    // dispatched, which is useful when a member's own instance IS separate, and skipped otherwise.
    if (agent !== 'lead') {
      emit(runId, KINDS.MEMBER_CALL, { child: agent, verb: b.verb, origin: 'platform', input: b.input });
      emit(runId, KINDS.MEMBER_BACK, {
        child: agent, verb: b.verb, origin: 'platform',
        returned: !!b.ok,
        failed_inside: failedInside(b.output),
        produced_nothing: producedNothing(b.output),
        seconds: b.seconds ?? null,
        output: String(b.output || '').slice(0, 12000),
      });
    }
    // MEMBERS ONLY, OR EVERY LEAD CALL IS COUNTED TWICE. The lead's tool results already reach governance from its
    // own message stream, so recording them again here would duplicate every provenance entry and double the credit
    // charge for the same GPU second. The callback exists for the calls the message stream cannot see.
    if (agent !== 'lead') {
      await governance.afterTool({ runId, verb: String(b.verb || ''), origin: 'platform',
        output: String(b.output || ''), seconds: Number(b.seconds || 0),
        emit: (k, d) => emit(runId, k, { ...d, child: agent }) });
    }
    return json(res, 200, { ok: true });
  }

  if (req.method === 'POST' && path === '/max/run') {
    const body = await readJson(req);
    const task = String(body.task || '').trim();
    if (!task) return json(res, 400, { error: 'no_task' });
    const id = 'max-' + Math.random().toString(16).slice(2, 12);
    const startModel = modelFrom(body);
    const startTemp = temperatureFrom(body);
    store.createRun({ id, task, team: !!body.team, model: startModel });
    live.set(id, { listeners: new Set(), n: 0, queue: null, finished: false });
    // A RUN THAT FAILS MUST NOT TAKE THE ENGINE WITH IT. `runTask` is not awaited, so an unhandled rejection here
    // was an unhandled rejection in the process: one ReferenceError ended every other run on the server.
    // A RUN MAY CONTINUE ANOTHER. `resume` names a previous run of ours, and its session carries the transcript.
    const prior = body.resume ? store.getRun(String(body.resume)) : null;
    // REGISTER IN PLATFORM RUN STORE. The /max/run endpoint is the dev UI path; it also needs registration
    // for files/all to see its runs. session_id may arrive from the body or header.
    const maxConsoleSession = body.session_id || req.headers['x-rayca-session-id'] || '';
    if (maxConsoleSession) store.noteConsoleSession(id, maxConsoleSession);
    // LINEAGE START. One identity per run, which is what WS-3 is for; the emitter promises never to raise and a
    // failure here must never touch the run, so it is fire and forget.
    platformStore.lineageEvent({ runId: id, eventType: 'START', jobName: 'modulon-max run' }).catch(() => {});
    platformStore.registerRun({ runId: id, sessionKey: maxConsoleSession || id, task, state: 'running',
      createdAt: Date.now() }).catch(() => {});
    runTask(id, task, !!body.team, prior?.session_id || '', startModel, startTemp, body.attachments).catch((e) => {
      const detail = String(e?.message || e).slice(0, 600);
      try {
        emit(id, KINDS.SESSION_END, { turns: null, ms: 0, cost: 0, answer: '', error: true, detail });
        store.finishRun(id, { state: 'error', turns: null, cost: 0, answer: detail });
        platformStore.updateRun({ runId: id, state: 'error', error: detail }).catch(() => {});
      } catch { /* the run is already unrecoverable; the server stays up */ }
      const r = live.get(id);
      if (r) r.finished = true;
      releaseTaskTable(id);
    });
    return json(res, 200, { run: id, team: !!body.team });
  }

  // MID-RUN INTERVENTION. The thing whose absence forced us to kill a run to change its scope.
  if (req.method === 'POST' && path.startsWith('/max/say/')) {
    const id = path.split('/').pop();
    const rec = live.get(id);
    const body = await readJson(req);
    const text = String(body.text || '').trim();
    if (!rec || rec.finished || !rec.queue) return json(res, 409, { error: 'run_not_steerable' });
    if (!text) return json(res, 400, { error: 'no_text' });
    rec.queue.push(text);
    emit(id, KINDS.INTERVENTION, { text });
    return json(res, 200, { ok: true });
  }
  /*
   * WHICH RUNS BELONG TO THIS CONVERSATION, answered from our own store.
   *
   * MEASURED: this passed through to the previous engine, whose store has no `max-` runs, and it answered `runs: []` for
   * every conversation. So the console could never list a run of this engine -- a page reload mid-run lost it, run history
   * per conversation was empty, and a forked run would have executed invisibly. The live stream was the only window.
   *
   * WE ANSWER ONLY WHEN WE HAVE SOMETHING. A conversation whose runs live in the previous engine still passes through, so
   * older conversations keep their history. Answering with an empty list would erase it.
   */
  if (req.method === 'GET' && path === '/v1/operational/runs') {
    const want = url.searchParams.get('session_id') || '';
    if (want) {
      const rows = store.runsForConsoleSession(want, Number(url.searchParams.get('limit') || 50));
      if (rows.length) {
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end(JSON.stringify({
          session_id: want,
          runs: rows,
          active: rows.filter((r) => r.state === 'running'),
          engine: 'modulon-max',
        }));
        return;
      }
    }
  }
  /*
   * CANCEL, WHICH THIS ENGINE DID NOT HAVE AT ALL.
   *
   * MEASURED: asked to stop a live PROTAC team run, there was no way to do it. The console's cancel button posts to
   * /v1/operational/cancel, which fell through the front door to the previous engine, which has never heard of a `max-`
   * run. Mid-run intervention did not help either: the note was queued, but the lead was inside a turn with asynchronous
   * members outstanding, so it would not be read for minutes. The only thing that actually stopped the run was restarting
   * the service, which is indistinguishable from a crash and is not something a researcher should have to ask for.
   *
   * ABORTS THE LOOP ITSELF through the controller the run was started with, so members stop too -- the SDK propagates
   * abort down the agent tree. The run is recorded `cancelled`, which is not `error`: nothing failed, someone chose.
   */
  if (req.method === 'POST' && (path === '/v1/operational/cancel' || path.startsWith('/max/cancel/'))) {
    let id = path.startsWith('/max/cancel/') ? decodeURIComponent(path.split('/').pop()) : '';
    if (!id) {
      const body = await readJson(req);
      id = String(body.run_id || body.runId || '').trim();
    }
    const rec = id ? live.get(id) : null;
    if (id && (rec || store.getRun(id))) {
      if (!rec || rec.finished) return json(res, 409, { error: 'run_not_active', run_id: id });
      try {
        rec.cancelled = true;
        if (rec.abort) rec.abort.abort();
        if (rec.queue && typeof rec.queue.close === 'function') rec.queue.close();
      } catch {
        // an abort that throws still means the intent was recorded
      }
      emit(id, KINDS.CANCELLED, { by: 'researcher' });
      return json(res, 200, { ok: true, run_id: id, state: 'cancelling' });
    }
  }


  /*
   * MID-RUN INTERVENTION ON THE PATH THE CONSOLE ACTUALLY CALLS.
   *
   * THIS WAS A PATH MISMATCH HIDING A SHIPPED CAPABILITY. The loop supports steering a live run, and the console ALREADY
   * calls it: typing into the composer while a run is in flight posts `{run_id, note}` to /v1/operational/intervene. This
   * engine only answered /max/say/:runId, so that POST fell through the front door to the previous engine, which has never
   * heard of a `max-` run and answers 404 unknown_run. Both halves were built and the wire between them was the wrong
   * shape.
   *
   * IT MATTERS MORE THAN ITS SIZE. The absence of exactly this forced a 40-backbone PD-L1 study to be KILLED to change its
   * scope to 5, losing the work already on disk. A run that can be redirected does not have to be destroyed.
   *
   * A RUN WE DO NOT OWN STILL PASSES THROUGH, so the previous engine keeps answering for its own runs.
   */
  if (req.method === 'POST' && path === '/v1/operational/intervene') {
    const body = await readJson(req);
    const id = String(body.run_id || body.runId || '').trim();
    const text = String(body.note ?? body.text ?? '').trim();
    if (id && (live.has(id) || store.getRun(id))) {
      const rec = live.get(id);
      if (!text) return json(res, 400, { error: 'no_text' });
      if (!rec || rec.finished || !rec.queue) return json(res, 409, { error: 'run_not_steerable' });
      /*
       * AN ATTACHMENT ON A FOLLOW-UP IS PART OF THE INSTRUCTION.
       *
       * "read this file" is the commonest thing a researcher says mid-run, and the file named is usually one they have just attached.
       * The briefing is folded into the QUEUED TEXT rather than emitted beside it, because the model reads the queue and does not
       * read the tape. The reader's own words go first and the briefing after, so the instruction is not buried under a manifest.
       */
      rec.queue.push(withAttachments(id, text, body, workspaces.get(id) || ''));
      emit(id, KINDS.INTERVENTION, { text });
      return json(res, 200, { ok: true, run_id: id });
    }
  }


  // FORK: BRANCH A STUDY WITHOUT LOSING THE ONE IT CAME FROM.
  //
  // This is what a researcher actually wants from a finished run: "keep everything up to here, then ask something
  // different." The previous engine could only replay. `forkSession` copies the transcript, and the new run resumes
  // from the copy, so the original is untouched and both are independently readable.
  if (req.method === 'POST' && (path.startsWith('/max/fork/') || path.startsWith('/v1/operational/fork/'))) {
    const id = path.split('/').pop();
    const run = store.getRun(id);
    if (!run) return json(res, 404, { error: 'no_such_run' });
    if (!run.session_id) {
      return json(res, 409, { error: 'run_has_no_session',
        detail: 'this run never reported a session id, so there is no transcript to fork' });
    }
    const body = await readJson(req);
    const task = String(body.task || '').trim();
    if (!task) return json(res, 400, { error: 'no_task', detail: 'a fork needs a new question to ask' });
    /*
     * A FORK IS A FOLLOW-UP, AND A FOLLOW-UP CARRIES WHAT A FIRST PROMPT CARRIES.
     *
     * The operator: "the followup prompts cannot carry the attached files to the engine, the first prompt can". This handler
     * called runTask with four arguments while the two other start paths pass seven, so the model, the temperature and every
     * attachment defaulted away. The client has sent all three on a fork for some time under a comment promising the fork
     * carries what the fresh run carries; only this side never read them. Resolved through the same two helpers the fresh
     * path uses, so a field added to one start path cannot go missing from this one.
     */
    const forkModel = modelFrom(body);
    const forkTemp = temperatureFrom(body);
    // THE INTENT APPLIES HERE TOO. A follow-up asking for a dashboard is still asking for a dashboard.
    const askedTask = task;
    const forkTask = await expandForIntent(body, task, run.console_session || '');
    try {
      const forked = await forkSession(run.session_id);
      const child = typeof forked === 'string' ? forked : (forked?.sessionId || forked?.session_id || '');
      if (!child) return json(res, 500, { error: 'fork_returned_no_session' });
      const newId = 'max-' + Math.random().toString(16).slice(2, 12);
      store.createRun({ id: newId, task: askedTask, team: !!run.team, model: forkModel });
      store.noteSession(newId, child);
      /*
       * THE CHILD INHERITS THE PARENT'S CONVERSATION, and that single line is what makes forking visible with no new
       * console plumbing at all. The console picks the conversation's newest run by recency, so a fork registered under
       * the same conversation simply becomes the run the reader is already watching. Registering it elsewhere would start
       * real GPU work that nothing in the browser displays, which is worse than not offering the button.
       */
      store.noteConsoleSession(newId, run.console_session || '');
      // PLATFORM RUNSTORE: forked runs inherit the parent's conversation and must also be visible to files/all.
      platformStore.registerRun({ runId: newId, sessionKey: run.console_session || '', task: askedTask, state: 'running',
        createdAt: Date.now() }).catch(() => {});
      live.set(newId, { listeners: new Set(), n: 0, queue: null, finished: false });
      runTask(newId, forkTask, !!run.team, child, forkModel, forkTemp, body.attachments).catch(() => {
        const r = live.get(newId);
        if (r) r.finished = true;
        releaseTaskTable(newId);
      });
      return json(res, 200, { run: newId, forked_from_run: id, forked_from_session: run.session_id,
                              session: child });
    } catch (e) {
      return json(res, 500, { error: 'fork_failed', detail: String(e?.message || e) });
    }
  }

  if (req.method === 'GET' && path.startsWith('/max/stream/')) {
    const id = path.split('/').pop();
    const run = store.getRun(id);
    if (!run) return json(res, 404, { error: 'no_such_run' });
    res.writeHead(200, { 'content-type': 'text/event-stream', 'cache-control': 'no-cache', connection: 'keep-alive' });
    // REPLAY FROM THE DATABASE FIRST. A reader must see a whole run whether or not it started it, and whether or not
    // this process is the one that ran it. Both were missing during the PD-L1 run.
    for (const ev of store.eventsFor(id)) res.write('data: ' + JSON.stringify(ev) + '\n\n');
    const rec = live.get(id);
    if (!rec || rec.finished) return res.end();
    const send = (ev) => {
      res.write('data: ' + JSON.stringify(ev) + '\n\n');
      if (ev.kind === KINDS.SESSION_END) res.end();
    };
    rec.listeners.add(send);
    req.on('close', () => rec.listeners.delete(send));
    return undefined;
  }

  // -----------------------------------------------------------------------------------------------------------------
  // EVERYTHING THAT IS NOT THE LOOP GOES TO THE ENGINE THAT ALREADY SERVES IT
  //
  // MEASURED: the console calls 50 distinct engine endpoints and this engine implements four. The other forty-six are
  // not the agent loop at all -- credentials, files, artifacts, wallet, usage, rates, plans, autonomy profiles,
  // connectors, cancel, gate answers, sessions, titles. They are the platform's product surface, and reimplementing
  // them here would be forty-six chances to introduce a bug in code that already works.
  //
  // SO THIS IS A FRONT DOOR, NOT A COMPETITOR. modulon-max answers the run loop itself and passes the rest through, so
  // the console can point entirely at it: one engine from the console's view, the old LOOP retired, and its platform
  // services still serving. That is what makes retirement possible without losing forty-six endpoints.
  //
  // FAILS LOUDLY AND SAYS WHICH SIDE FAILED. A 502 that does not distinguish "modulon-max is broken" from "the
  // upstream engine is down" sends the next person to read the wrong log.
  /*
   * THE WORKFLOW GRAPH FOR OUR OWN RUNS, ANSWERED HERE RATHER THAN PASSED THROUGH.
   *
   * MEASURED: passing this through returned HTTP 200 with `0 nodes, 0 edges` for every run of this engine, because the
   * upstream builds the graph by reading ITS event store, and that store has no `max-*` runs. The panel the operator
   * asked for by name therefore rendered an EMPTY CANVAS on every run, while our tape held everything the graph needs.
   * A run we do not own still passes through, so the previous engine's runs are unaffected.
   */
  {
    const wf = /^\/v1\/operational\/runs\/([^/]+)\/workflow$/.exec(path);
    if (wf && req.method === 'GET') {
      const runId = decodeURIComponent(wf[1]);
      const run = store.getRun(runId);
      if (run) {
        const events = store.eventsFor(runId);
        // TRY THE SCIENTIFIC INTERPRETER FIRST, fall back to the structural deriver.
        // wfinterp.interpret uses a model to read the run as science: "receptor preparation",
        // "docking with gnina" rather than "run_python". The structural deriver reports
        // interpreted:false so the console knows the difference.
        // MEASURED: without interpretation, every method read "run_python" on the PROTAC run.
        let doc = null;
        let interpNote = '';
        try {
          const consoleEvents = events.map((ev, i) => toConsoleEvent(ev, i, runId)).filter(Boolean);
          const result = await platformStore.interpretWorkflow({
            runId, sessionKey: run.console_session || '', task: run.task || '', events: consoleEvents,
          });
          if (result && result.interpreted) {
            doc = result;
          } else if (result && result.note) {
            interpNote = String(result.note);
          }
        } catch (err) {
          // NEVER SWALLOW THIS SILENTLY. A bare catch here cost an hour: the endpoint quietly served the structural
          // reading while the interpreter was declining for a stated reason, and there was no way to see the reason from
          // outside. Falling back is correct; hiding WHY is not.
          console.error(`[max] workflow interpretation unavailable for ${runId}: ${err?.message || err}`);
        }
        if (!doc && interpNote) {
          console.error(`[max] workflow interpreter declined for ${runId}: ${interpNote}`);
        }

        if (!doc) {
          // STRUCTURAL FALLBACK: the deriver that reads tool names off the tape. It is honest
          // about what it is (interpreted:false) and the console shows the difference.
          doc = workflowFrom(run, events);
        }
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end(JSON.stringify(doc));
        return;
      }
    }
  }

  /*
   * THE MODEL CATALOGUE, CORRECTED BY THE PROCESS THAT ACTUALLY RUNS THE MODEL.
   *
   * MEASURED DEFECT, reported by the operator as "i think it still ran via sonnet, but i selected qwen3 coder".
   *
   * TWO ENGINES, TWO VARIABLES, ONE QUESTION. The catalogue is built upstream by serve.py, which answers
   * `"default": os.environ.get("RAYCA_LLM_MODEL")` and is set to qwen3-coder-480b. Runs execute HERE, on RAYCA_MODEL,
   * which is claude-sonnet-4-6. The console asked the engine that does not run the task.
   *
   * WHY THAT LOOKED LIKE A LOST SELECTION AND WAS WORSE THAN ONE. The selector displays the reported default when no
   * choice has been recorded, so it showed "Qwen3 Coder 480b" as the current model before anybody clicked anything. A
   * displayed value that was never recorded is never sent, so the run arrived with no model and this process used its
   * own default. The reader saw Qwen3 and got Sonnet, without touching the control.
   *
   * So the default is answered by the process that will honour it, and the offered list is narrowed to what this process
   * will accept, which it now learns from the router. Everything else upstream sends is passed through untouched.
   */
  if (req.method === 'GET' && path === '/v1/operational/models') {
    let upstreamBody = {};
    try {
      const r = await fetch(`${UPSTREAM}${path}${url.search}`, {
        headers: { authorization: `Bearer ${SERVE_KEY}` },
        signal: AbortSignal.timeout(15000),
      });
      if (r.ok) upstreamBody = await r.json();
      else console.error('[models] upstream catalogue HTTP %s', r.status);
    } catch (e) {
      console.error('[models] upstream catalogue failed: %s', String((e && e.message) || e));
    }
    const offered = Array.isArray(upstreamBody?.models) ? upstreamBody.models.map(String) : [];
    /* `auto` survives because this process resolves it; anything it would silently replace does not. */
    const honoured = offered.filter((m) => m.toLowerCase() === 'auto' || AVAILABLE_MODELS.includes(m));
    for (const m of AVAILABLE_MODELS) {
      if (!honoured.includes(m)) honoured.push(m);
    }
    return json(res, 200, { ...upstreamBody, models: honoured, default: MODEL, engine: 'modulon-max' });
  }

  if (path.startsWith('/v1/')) {
    try {
      const headers = { ...req.headers, host: undefined, authorization: `Bearer ${SERVE_KEY}` };
      delete headers.host;
      delete headers['content-length'];
      /* HOP BY HOP HEADERS MUST NOT BE RE-SENT. With the body now streamed, a forwarded transfer-encoding or connection
         header conflicts with what undici sets itself and the request is rejected before it leaves. MEASURED: the 500 MB
         upload failed in 0.04 s with the upstream unreachable while the upstream was answering 200 on the same path. */
      delete headers['transfer-encoding'];
      delete headers.connection;
      delete headers['accept-encoding'];
      /*
       * THE BODY IS FORWARDED AS BYTES, NOT COLLECTED INTO A STRING.
       *
       * This read the request with `raw += c`, which does two damaging things to anything that is not text. It decodes
       * the bytes as UTF-8, so a binary upload arrives corrupted, and it holds the entire body in memory, so a large one
       * cannot arrive at all. MEASURED: a 500 MB multipart upload through this path failed while the same request made
       * directly to the upstream succeeded in 10.6 s at 139 MB of RSS.
       *
       * Streaming also keeps the memory flat for every other forwarded call, and `duplex: 'half'` is what allows a
       * stream to be used as a request body at all.
       */
      const streamed = req.method !== 'GET' && req.method !== 'HEAD';
      const upstream = await fetch(`${UPSTREAM}${path}${url.search}`, {
        method: req.method,
        headers,
        ...(streamed ? { body: Readable.toWeb(req), duplex: 'half' } : {}),
      });
      res.writeHead(upstream.status, {
        'content-type': upstream.headers.get('content-type') || 'application/json',
      });
      // Streamed as it arrives, because some of these are SSE and buffering an SSE response defeats its purpose.
      if (upstream.body) {
        const reader = upstream.body.getReader();
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          res.write(Buffer.from(value));
        }
      }
      return res.end();
    } catch (e) {
      return json(res, 502, {
        error: 'upstream_engine_unreachable',
        upstream: UPSTREAM,
        path,
        detail: String(e?.message || e).slice(0, 300),
        note: 'modulon-max is running; the platform-services engine it passes non-loop endpoints to is not answering',
      });
    }
  }

  return json(res, 404, { error: 'not_found' });
});

const orphans = store.reconcileOrphans();
const loopback = BIND === '127.0.0.1' || BIND === 'localhost' || BIND === '::1';
if (!loopback && !SERVE_KEY) {
  console.error('[max] REFUSING TO START. Bind is ' + BIND + ' with no RAYCA_SERVE_KEY set. This engine executes '
    + 'Python, dispatches GPU containers and submits HPC jobs; reachable and unauthenticated is worse than down.');
  process.exit(2);
}
server.listen(PORT, BIND, () => {
  console.log(`[max] listening on http://${BIND}:${PORT}  auth=${SERVE_KEY ? 'bearer' : 'loopback-only'}`);
  console.log(`[max] personas ${PERSONAS.length}  model ${MODEL}  db ${DB}`);
  if (orphans) console.log(`[max] ${orphans} run(s) left by a previous process marked interrupted, not error`);
  console.log('[max] the engine on 8201 and the console are untouched by this process');
  /*
   * ASK THE ROUTER WHAT IT SERVES, once at boot and then periodically.
   *
   * Not awaited, because a slow or missing router must not delay accepting requests; the fallback set is already in
   * place and the first refresh only ever widens it. Refreshed on a timer so a model added to the router becomes
   * selectable without restarting a service that may have a run in flight.
   */
  refreshAvailableModels();
  refreshPrices();
  const modelTimer = setInterval(() => { refreshAvailableModels(); refreshPrices(); }, 10 * 60 * 1000);
  modelTimer.unref();
});
