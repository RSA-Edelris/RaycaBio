/**
 * The surface the Rayca console already speaks.
 *
 * WHY A PROJECTION AND NOT A REWRITE. The operator asked for an event stream native to how this loop behaves, and that
 * is what `/max/stream` serves: a tree with an agent on every node and no global sequence number. But the console
 * reaches its engine through one env var, `RAYCA_ENGINE_URL`, and proxies `/api/rayca/engine/operational/stream` to
 * `${RAYCA_ENGINE_URL}/v1/operational/stream`. Presenting that endpoint means the existing console can drive this
 * engine by changing a single variable, with no console code touched and the current engine still the default.
 *
 * THE TREE IS CARRIED, NOT FLATTENED AWAY. The console schema has a `node` field, so the agent that produced an event
 * travels with it: `lead` for the top-level loop and the persona id for a member. A reader that only understands the
 * flat schema still shows every event in order; a reader that understands agents can rebuild the tree from the same
 * frames. Nothing is discarded to fit.
 *
 * `seq` IS MONOTONIC AND NOTHING ELSE. The console sorts by it, and the engine it was written for once set
 * `seq: -turn.index` on a user turn, which sorted a mid-run prompt above the first event of the run. Here `seq` is the
 * event's index in the run and is never derived from anything a caller controls.
 */

import { KINDS } from './events.mjs';

export const OPS_SCHEMA_VERSION = 1;

/**
 * The container dispatches inside a tool's output, as JOB records the console's Jobs panel can read.
 *
 * THE GAP THIS CLOSES. `readJobs` in the console requires `meta.dispatch_submitted === true`, a field the previous
 * engine emitted from its dispatch courier. This engine dispatches containers through `run_python` calling the
 * platform's toolkit, so the same facts arrive as MARKERS in the tool's stdout:
 *
 *   [dispatch] tool=ligandmpnn rc=0 gpu=True duration_s=17.7
 *   [dispatch] tool=ligandmpnn rc=1 gpu=True duration_s=18.2 error=tool_failed cause=...
 *
 * Without this the Jobs section was simply EMPTY on every run of this engine, while the run had in fact put a container
 * on an A100 -- the most consequential and most expensive thing a study does, invisible.
 *
 * PARSED, NOT GUESSED. Only the marker's own fields are reported: a job with no duration in the marker has no duration
 * here rather than an estimated one.
 */
const DISPATCH_MARK = /\[dispatch\]\s+([^\n]+)/g;

export function dispatchesIn(text) {
  const out = [];
  if (!text) {
    return out;
  }
  /*
   * ESCAPED NEWLINES FIRST, and this was the bug that made the parser find a tool but lose its duration.
   *
   * A tool result reaches here as the JSON text the MCP server produced, so a newline inside it is the TWO characters
   * backslash-n, not a line break. `[^\n]+` then ran past the end of the marker and swallowed the next line, so
   * `duration_s=17.7` became `duration_s=17.7\nb` and parsed as NaN. Normalising once is simpler and less fragile than
   * teaching every field pattern about both forms.
   */
  const raw = typeof text === 'string' ? text : JSON.stringify(text);
  const body = raw.replace(/\\r\\n|\\n|\\r/g, '\n');
  for (const m of body.matchAll(DISPATCH_MARK)) {
    const fields = {};
    for (const pair of m[1].split(/\s+/)) {
      const eq = pair.indexOf('=');
      if (eq > 0) {
        fields[pair.slice(0, eq)] = pair.slice(eq + 1);
      }
    }
    if (!fields.tool) {
      continue;
    }
    const rc = fields.rc === undefined ? null : Number(fields.rc);
    out.push({
      tool: fields.tool,
      rc: Number.isFinite(rc) ? rc : null,
      gpu: String(fields.gpu || '').toLowerCase() === 'true',
      seconds: fields.duration_s === undefined ? null : Number(fields.duration_s),
      error: fields.error || '',
    });
  }
  return out;
}

/**
 * A dispatch as the Jobs panel expects it: `dispatch_submitted` with `job_state` done or running.
 *
 * A CONTAINER THAT FAILED IS STILL A JOB THAT RAN. `ok` is derived from `job_state`, and rc carries the truth about
 * whether the work succeeded, so a failed dispatch appears as a row rather than vanishing.
 */
/**
 * A container job the moment it is SUBMITTED, before it has an exit code or a duration.
 *
 * WHY A SECOND PROJECTION RATHER THAN A FLAG ON THE FIRST. `toJobEvent` is built from the `[dispatch]` marker, which
 * carries rc and duration -- neither of which exists yet at submission. Reusing it would mean inventing values for both
 * and the panel derives its outcome from them, so a job that had merely started would render as a job that finished.
 *
 * `job_state: 'running'` is what the Jobs panel reads to set its `running` flag, which is the field that distinguishes
 * a job in flight from one that failed to start. MEASURED: with no submitted event at all, RFdiffusion ran for minutes
 * on the A100 while the panel reported the dispatch never reached a container, because a null exit code was the only
 * thing it had to go on.
 */
/**
 * A SCHEDULER JOB, read out of a `run_on_cluster` or `check_cluster_job` result.
 *
 * MEASURED, on the operator's EGFR/erlotinib run. `run_on_cluster` returned
 *   {"ok": true, "cluster": "Isambard-AI_HPC", "job_id": "6102452", "state": "submitted",
 *    "host": "ai-p2.access.isambard.ac.uk"}
 * and the job ran on Isambard, yet the Jobs panel stayed empty: zero job events for the whole run. The operator: "the
 * jobs is not listed under job section".
 *
 * WHY NOTHING ARRIVED. The panel was fed only by `dispatchesIn()`, which parses the `[dispatch]` marker a CONTAINER
 * prints, and by the container submission spool. A cluster job prints no marker and spools nothing: it is an ordinary
 * platform verb returning JSON. So an HPC job has never appeared in that panel under this loop, while
 * `runStructure.ts` has carried `jobId`, `cluster` and `jobState` fields for it the whole time, waiting for an event
 * that was never sent.
 *
 * Returns null when the result is not a cluster submission, so the caller can ask about every tool result cheaply.
 */
export function clusterJobIn(output) {
  if (!output) {
    return null;
  }
  let parsed = output;
  if (typeof parsed === 'string') {
    try {
      parsed = JSON.parse(parsed);
    } catch {
      return null;
    }
  }
  if (!parsed || typeof parsed !== 'object') {
    return null;
  }
  const jobId = parsed.job_id === undefined || parsed.job_id === null ? '' : String(parsed.job_id);
  if (!jobId) {
    return null;
  }
  return {
    jobId,
    cluster: String(parsed.cluster || ''),
    host: String(parsed.host || ''),
    provider: String(parsed.provider || ''),
    /*
     * THE SCHEDULER'S OWN WORD, not our inference. MEASURED: `run_on_cluster` answers `state: "submitted"` and
     * `check_cluster_job` answered `state: "running"` for a job that `squeue` reported as PENDING. Passing the value
     * through unchanged keeps that disagreement visible to be fixed at its source rather than laundering it here.
     */
    state: String(parsed.state || 'submitted'),
    /*
     * THE SCHEDULER'S OWN WORD, when the engine reported it.
     *
     * MEASURED: job 6102452 sat PENDING behind higher-priority work and the panel said "running". A researcher waiting
     * for their job to start was told it already had, which for a 12 hour job decides whether they wait or resubmit
     * smaller. `state` is the engine's coarse answer and stays as it is; this is what the cluster actually said.
     */
    schedulerState: String(parsed.scheduler_state || ''),
    queued: parsed.queued === true,
    requested: parsed.requested && typeof parsed.requested === 'object' ? parsed.requested : null,
  };
}


/**
 * A scheduler job as the Jobs panel expects it.
 *
 * SEPARATE FROM THE CONTAINER PROJECTIONS because the two are not the same object. A container is identified by its
 * tool and lives inside our own sandbox; a cluster job has an id issued by a scheduler on a machine shared with other
 * people, and without that id and the cluster's name "a job is queued" is not something a researcher can verify or act
 * on. `runStructure.ts` says exactly this where `jobId` is declared.
 */
export function toClusterJobEvent(j, seq, runId, at, agent) {
  const done = j.state === 'completed' || j.state === 'done';
  const failed = j.state === 'failed' || j.state === 'cancelled' || j.state === 'timeout';
  // QUEUED IS NOT RUNNING. Shown as its own word so the reader knows the job is waiting, not executing.
  const queued = j.queued || j.schedulerState === 'pending';
  return {
    v: OPS_SCHEMA_VERSION,
    seq,
    ts: (at || Date.now()) / 1000,
    run_id: runId,
    type: 'status',
    node: agent || 'lead',
    title: `job ${j.jobId} on ${j.cluster || 'the cluster'}`,
    body: `${j.cluster || 'cluster'} job ${j.jobId} ${j.schedulerState || j.state}`,
    status: done ? 'ok' : failed ? 'error' : 'running',
    meta: {
      stage: 'dispatch',
      dispatch_submitted: true,
      // The panel reads this to decide whether the row is finished, and a scheduler job is the case it was written for.
      job_state: done ? 'done' : failed ? 'failed' : queued ? 'queued' : 'running',
      // Passed through so the panel can say "pending (Priority)" rather than inventing a word for it.
      scheduler_state: j.schedulerState || null,
      job_id: j.jobId,
      cluster: j.cluster || null,
      host: j.host || null,
      tool: j.cluster || 'cluster job',
      // A SCHEDULER JOB IS NOT OUR GPU. `gpu` describes the sandbox card, and claiming it here would put a cluster
      // job's hardware in a field that means something else.
      gpu: false,
      rc: null,
      duration_s: null,
      elapsed_s: null,
      error: null,
    },
  };
}


/**
 * Has this report settled the job, and how did it end?
 *
 * ASKED AS A QUESTION rather than compared against a string, the same way `stopDecision` asks about terminality. The
 * state vocabulary on this channel is the CONTAINER's -- `done`, `failed`, `cancelled`, `running` -- and it is not the
 * console's `OperationalEventStatus`, so mapping one to the other in one named place keeps the two from being confused
 * at each site that cares.
 *
 * AN EXIT CODE SETTLES IT EVEN WITHOUT A STATE. `_announce_container_job` sends both, but a report carrying only rc is
 * still a finished job and must not be shown as running.
 */
export function jobOutcome(d) {
  const rc = Number.isFinite(Number(d && d.rc)) ? Number(d.rc) : null;
  const state = String((d && d.state) || '');
  const failedState = state === 'failed' || state === 'error' || state === 'cancelled';
  const doneState = state === 'done' || state === 'ok' || state === 'complete';
  if (rc === null && !failedState && !doneState) {
    return { settled: false, ok: false, rc: null, state: state || 'running' };
  }
  /* rc IS THE AUTHORITY WHEN IT IS PRESENT, because it comes from the container itself while the state is a label put
     on top of it. A non-zero code with state=done is a failure, and saying otherwise would hide it. */
  const ok = rc === null ? doneState : rc === 0;
  return { settled: true, ok, rc, state: state || (ok ? 'done' : 'failed') };
}

export function toJobSubmittedEvent(d, seq, runId, at, agent) {
  const where = d.host ? ` on ${d.host}` : '';
  const outcome = jobOutcome(d);
  return {
    v: OPS_SCHEMA_VERSION,
    seq,
    ts: (at || Date.now()) / 1000,
    run_id: runId,
    type: 'status',
    node: agent || 'lead',
    title: `${d.tool} on ${d.gpu ? 'GPU' : 'CPU'}`,
    /* SAYS WHAT HAPPENED, not always "submitted". A finished job reading "submitted" is the same defect as a finished
       job showing as running, just in prose. */
    body: outcome.settled
      ? `${d.tool} ${outcome.ok ? 'finished' : 'failed'}${where}${
        Number.isFinite(Number(d.elapsed_s)) ? ` after ${Number(d.elapsed_s)}s` : ''}`
      : `${d.tool} submitted${where}`,
    /* NOT 'ok' WHILE IT RUNS: nothing has succeeded yet, and not 'error' either, because a job in flight has no
       outcome. Once the container reports one, this carries it, which is what lets a card stop spinning. */
    status: outcome.settled ? (outcome.ok ? 'ok' : 'error') : 'running',
    meta: {
      stage: 'dispatch',
      dispatch_submitted: true,
      job_state: outcome.state,
      tool: d.tool,
      gpu: !!d.gpu,
      // ABSENT, NOT ZERO, until the container reports. A zero exit code means success and a zero duration means it took
      // no time; either invented would be a lie. `rc` arriving is the whole difference between a job that finishes on
      // screen and one that spins forever.
      rc: outcome.rc,
      duration_s: outcome.settled && Number.isFinite(Number(d.elapsed_s)) ? Number(d.elapsed_s) : null,
      // ELAPSED IS THE ONE THING A RUNNING JOB HONESTLY HAS, once a beat has reported it.
      elapsed_s: Number.isFinite(Number(d.elapsed_s)) ? Number(d.elapsed_s) : null,
      error: outcome.settled && !outcome.ok ? (d.detail ? String(d.detail) : `the container exited ${outcome.rc}`) : null,
      image: d.image || null,
      // THE MACHINE, so "a job is running" is something the researcher can go and verify.
      host: d.host || null,
      /*
       * WHAT THE MACHINE IS DOING, when a beat has measured it. Undefined until then rather than zero: a GPU reading of
       * zero means the card is idle, which is a real and different statement from not having looked yet.
       */
      container: d.container || null,
      gpu_util_pct: d.gpu_util_pct === undefined ? null : d.gpu_util_pct,
      gpu_mem_used_mb: d.gpu_mem_used_mb === undefined ? null : d.gpu_mem_used_mb,
      gpu_mem_total_mb: d.gpu_mem_total_mb === undefined ? null : d.gpu_mem_total_mb,
      output_tail: d.tail || null,
    },
  };
}


export function toJobEvent(d, seq, runId, at, agent) {
  return {
    v: OPS_SCHEMA_VERSION,
    seq,
    ts: (at || Date.now()) / 1000,
    run_id: runId,
    type: 'status',
    node: agent || 'lead',
    title: `${d.tool} on ${d.gpu ? 'GPU' : 'CPU'}`,
    body: d.error
      ? `${d.tool} did not complete: ${d.error}`
      : `${d.tool} finished`,
    status: d.rc === 0 ? 'ok' : 'error',
    meta: {
      stage: 'dispatch',
      dispatch_submitted: true,
      /*
       * `done` ONLY WHEN THE CONTAINER ACTUALLY RETURNED A CODE.
       *
       * MEASURED: the real marker for an unreachable GPU host reads `rc=None gpu=False duration_s=0.0
       * error=host_unreachable`. Reporting that as `done` would make the Jobs panel show it as OK, because the panel
       * derives `ok` from `job_state === 'done'` -- so a dispatch that never left the building would have been presented
       * as a completed job. A run whose GPU host was down must not look like a run whose GPU work succeeded.
       */
      job_state: typeof d.rc === 'number' ? 'done' : 'unreachable',
      tool: d.tool,
      gpu: d.gpu,
      rc: d.rc,
      duration_s: d.seconds,
      elapsed_s: d.seconds,
      error: d.error || null,
    },
  };
}

/**
 * Map one native event onto the console's schema.
 *
 * Returns null for events the console has no place for, rather than forcing them into a type that means something
 * else: a frame the console cannot interpret is worse than a frame it never receives.
 */
/**
 * The operation class a tool put in its own result.
 *
 * READ FROM THE OUTPUT RATHER THAN FROM THE CALLBACK, because the two paths differ and only one of them has it.
 * `/max/tool` fires for MEMBERS only -- server.mjs:998 skips the lead, since members share the parent's MCP server
 * and the label is always `lead` there -- while the lead's results arrive through the SDK message stream instead.
 * Reading the result covers both, and the result is where the class was computed.
 *
 * Returns null on anything unparseable, which is the common case: most tool output is plain text.
 */
function fieldOf(output, key) {
  if (typeof output !== 'string' || output.length === 0 || output[0] !== '{') return null;
  try {
    const parsed = JSON.parse(output);
    const v = parsed && parsed[key];
    return typeof v === 'string' && v ? v : null;
  } catch {
    return null;
  }
}

function classOf(output) {
  return fieldOf(output, 'operation_class');
}

/*
 * THE USER'S OWN WORDS, AS AN EVENT ON THE TAPE.
 *
 * THIS IS THE DEFECT UNDERNEATH A WEEK OF SYMPTOMS, and the operator named it exactly: "we have a session, then when user
 * go into it, it will see what is generated in that session!! and it will maintain its state, the use prompts and all
 * event stream in that session!! why such a thing should be this mess!!"
 *
 * MEASURED. The opening prompt of a run was on the tape only inside `session.start`, and `session.start` projects as a
 * STATUS line titled "run started" attributed to the lead agent. So the transcript the server serves contained no user
 * message for the prompt that began the run. An INTERVENTION, a follow-up sent mid-run, does project as a user message --
 * which is why follow-ups survived a reload and opening prompts did not.
 *
 * WHAT THAT ABSENCE COST, all of it downstream of this one omission. The console had to MINT the user's card itself at
 * send time, in the browser, with no sequence number because sequence belongs to the service and no identity because the
 * service had not issued one. From there: the card vanished whenever the tape was rebuilt from the server, because it had
 * never been in the server's copy; identity fell back to run and sequence, which for such a card was the empty string, so
 * the first prompt matched every later prompt and they were discarded as duplicates; and ordering had to be inherited
 * from whatever event preceded the card, which is why a per-run counter ended up sorting a whole conversation and runs
 * interleaved.
 *
 * The prompt is now an event like any other, with the run and the sequence the service assigns. Nothing needs to be
 * minted, inherited, or reconciled, because the transcript the client renders is the transcript the server holds.
 */
/**
 * The attachment chips a prompt card shows, in the shape the console reads.
 *
 * THE DEFECT THIS CLOSES, reported by the operator: "my attachemnts arre not visible in the followup prompt. the engine
 * can get them but they are not appearing on top of the prompts."
 *
 * They were right about both halves. The engine RESOLVES attachments and folds a briefing into the task, so the model
 * genuinely receives them, and it records them as their own `attachments` tape event. But the prompt event -- the card
 * the reader sees their own words on -- carried `meta: { role: "user" }` and nothing else.
 *
 * WHY THAT SHOWED UP AS A DISAPPEARING CHIP RATHER THAN A MISSING ONE. The browser mints the prompt card optimistically
 * WITH its chips, from the composer's own store. Then the console asks the engine for the whole conversation and
 * REPLACES what it holds, deliberately: "the server's transcript is the transcript". A locally minted card survives only
 * until the server has the same text. So the chips appeared, then vanished the moment the authoritative tape arrived
 * carrying a prompt event that had never heard of them.
 *
 * `rayca_attachments` IS THE FIELD THE CONSOLE ALREADY READS, in `console/conversation.ts`. Nothing new is invented
 * here; the engine simply starts filling in a channel the reader was already looking at.
 */
export function promptAttachmentsFrom(items) {
  return (Array.isArray(items) ? items : [])
    .map((i) => ({
      kind: String((i && i.kind) || ''),
      id: String((i && i.id) || ''),
      name: String((i && i.name) || ''),
      ...(i && i.category_label ? { category_label: String(i.category_label) } : {}),
      /*
       * WHERE THE FILE LIVES, and dropping it is why a file chip could not be opened.
       *
       * An artifact id is only meaningful inside its own session, so the console needs the origin to read the bytes
       * back. The chip carried kind, id and name and this projection quietly discarded the one field that says WHICH
       * session to ask. MEASURED on the real tape: every chip the browser received had no session, so the viewer asked
       * the run being viewed and got a truthful "artifact not found in this session".
       */
      ...(i && i.session ? { session: String(i.session) } : {}),
    }))
    /* A chip with neither a name nor an id would render as an empty pill, which is worse than one fewer chip. */
    .filter((a) => a.name || a.id);
}

/**
 * Put the chips on a prompt card, if this event is one and there are any.
 *
 * ASKED OF THE EVENT rather than decided by the caller, so the two projection sites cannot disagree about which events
 * are a reader's own words. Both the run's opening prompt and a mid-run follow-up are `role: 'user'`, and both should
 * carry what was attached to them.
 */
export function withPromptAttachments(consoleEvent, items) {
  const chips = promptAttachmentsFrom(items);
  if (!consoleEvent || !chips.length) {
    return consoleEvent;
  }
  const meta = consoleEvent.meta || {};
  if (meta.role !== 'user') {
    return consoleEvent;
  }
  return { ...consoleEvent, meta: { ...meta, rayca_attachments: chips } };
}

export function userPromptEvent(ev, seq, runId) {
  const task = String(ev.task || '').trim();
  if (!task) {
    return null;
  }
  return {
    v: OPS_SCHEMA_VERSION,
    seq,
    ts: (ev.at || Date.now()) / 1000,
    run_id: runId,
    type: 'message',
    node: 'researcher',
    title: 'Your request',
    body: task,
    status: 'ok',
    meta: { role: 'user' },
  };
}

export function toConsoleEvent(ev, seq, runId) {
  const base = { v: OPS_SCHEMA_VERSION, seq, ts: (ev.at || Date.now()) / 1000, run_id: runId };
  const agent = ev.child ? String(ev.agent_type || ev.child) : 'lead';

  switch (ev.kind) {
    case KINDS.SESSION_START:
      return { ...base, type: 'status', node: 'lead', title: ev.team ? 'agent team' : 'run started',
        body: ev.task || '', status: 'running',
        meta: { stage: 'start', team: !!ev.team, team_members: ev.team_members || [] } };

    case KINDS.READY:
      return { ...base, type: 'status', node: 'lead', title: 'tools ready',
        body: `${(ev.platform_verbs || []).length} platform verbs, ${(ev.own_tools || []).length} own tools`,
        status: 'running',
        meta: { stage: 'ready', platform_verbs: ev.platform_verbs || [], agents: ev.agents_available || [] } };

    case KINDS.SAY:
      return { ...base, type: 'message', node: 'lead', title: '', body: ev.text || '',
        meta: { role: 'assistant', turn: ev.turn } };

    case KINDS.THINK:
      // Marked ephemeral so a console that hides reasoning can, without the engine deciding for it.
      return { ...base, type: 'message', node: 'lead', title: 'thinking', body: ev.text || '',
        meta: { role: 'thinking', ephemeral: true, turn: ev.turn } };

    case KINDS.CANCELLED:
      // NOT AN ERROR. Nothing failed; a researcher chose to stop. Reporting a choice as a failure would teach the reader
      // to distrust the error state, which has to stay meaningful.
      return { ...base, type: 'status', node: 'lead', title: 'stopped by you',
        body: 'The run was stopped. Everything it had already written is kept.',
        status: 'ok', meta: { stage: 'cancelled', by: ev.by || 'researcher' } };

    case KINDS.INTERVENTION:
      return { ...base, type: 'message', node: 'researcher', title: 'intervention', body: ev.text || '',
        meta: { role: 'user' } };

    /*
     * THE TOOL USE ID TRAVELS, because without it a card cannot be paired with its own result.
     *
     * The engine has always known the id: it is on both the call and the result event, and the projection dropped it.
     * So the console could not have shown a step in progress even if it had tried, because it had no way to say "this
     * result belongs to that card". Pairing by adjacency is not an alternative -- the moment two members work at once,
     * which is the normal case in a team run, adjacency is wrong.
     */
    case KINDS.CALL:
      return { ...base, type: 'execute', node: 'lead', title: ev.caption || titleFor(ev.verb, ev.input),
        body: readableBody(ev.input), status: 'running',
        meta: { tool: ev.verb, input: ev.input, origin: ev.origin, call_id: ev.id || null,
          ...(codeOf(ev.input) ? { language: 'python' } : {}) } };

    case KINDS.MEMBER_CALL:
      return { ...base, type: 'execute', node: agent, title: ev.caption || titleFor(ev.verb, ev.input),
        body: readableBody(ev.input), status: 'running',
        meta: { tool: ev.verb, input: ev.input, origin: ev.origin, call_id: ev.id || null, agent, member: true,
          ...(codeOf(ev.input) ? { language: 'python' } : {}) } };

    case KINDS.FILE: {
      /*
       * `meta.observed` IS THE SHAPE THE CONSOLE ALREADY READS, so this projects into it rather than defining a
       * second announcement format. artifactTypes.ts keys its dedupe on the file NAME because a real tape showed
       * the same comparison CSV rewritten at almost every step, growing 465 -> 242 -> 140 -> 624 bytes: keying on
       * name plus size is right for announcing a genuine rewrite and wrong for a file list, which would then show
       * thirteen rows of one file and leave the reader to guess which is current.
       */
      const f = ev.file || {};
      return { ...base, type: 'artifact', node: ev.agent || 'lead',
        title: String(f.name || 'file'),
        body: '',
        status: 'ok',
        meta: { observed: f, agent: ev.agent || 'lead' } };
    }
    case KINDS.PROGRESS:
      // THE ANSWER TO A FIFTEEN-MINUTE SILENCE. A long tool call emitted nothing at all and the screen looked frozen.
      /*
       * THE TAIL TRAVELS WITH THE BEAT, so an open card can show what the step is printing.
       *
       * `call_id` is included because that is how the console finds the card this belongs to: `conversation.ts` keys its
       * open acts on it. Without the id a beat is a status line floating beside the work rather than part of it.
       */
      return { ...base, type: 'status', node: 'lead', title: `${ev.caption || ev.verb} still running`,
        body: ev.tail ? String(ev.tail) : `${Math.round(Number(ev.seconds) || 0)}s elapsed`, status: 'running',
        meta: { stage: 'tool_progress', tool: ev.verb, elapsed_s: ev.seconds, ephemeral: true,
          call_id: ev.id || null, tail: ev.tail || '' } };

    case KINDS.BACK:
    case KINDS.MEMBER_BACK: {
      const member = ev.kind === KINDS.MEMBER_BACK;
      // THREE FACTS, KEPT APART, because a call that returned is not a call that worked and a call that worked is not
      // a call that produced anything. Collapsing them is how a traceback got reported as success.
      const bad = ev.returned === false || ev.failed_inside;
      return { ...base, type: 'observe', node: member ? agent : 'lead',
        /*
         * TITLED THE SAME WAY AS THE CALL, which this line was not doing.
         *
         * MEASURED on a live run: `TaskCreate`, `TaskUpdate` and `write_report` reached the screen as titles from HERE,
         * even after the call side had been fixed. A `back` event carries no `input` -- the arguments were on the call --
         * so `captionFrom` yields nothing and this fell through to `ev.verb`, printing the raw identifier.
         *
         * `titleFor` is used instead so the fallback is at least ordinary English, and so this path cannot drift from
         * the call's naming again. With no input it produces "task create" rather than "TaskCreate".
         */
        title: bad ? `${ev.caption || titleFor(ev.verb, ev.input)} failed`
          : (ev.caption || titleFor(ev.verb, ev.input)),
        body: readableBody(ev.output),
        status: bad ? 'error' : 'ok',
        meta: { tool: ev.verb, origin: ev.origin, call_id: ev.id || null, elapsed_s: ev.seconds ?? null,
          returned: ev.returned !== false, failed_inside: !!ev.failed_inside,
          produced_nothing: !!ev.produced_nothing, agent: member ? agent : 'lead', member,
          // WHAT KIND OF SCIENCE THIS WAS, derived at the source from what the step produced, so the console can
          // give a structure prediction and a correlation different identities. Absent when the evidence does not
          // say, and the console then keeps its existing appearance rather than colouring on a guess.
          operation_class: ev.operation_class || classOf(ev.output),
          // The verb's own published description, so a card can say what the operation IS and not only
          // what it was called. Absent when the platform never wrote one.
          explanation: ev.explanation || fieldOf(ev.output, 'explanation') } };
    }

    case KINDS.SPAWN:
      return { ...base, type: 'plan', node: 'lead', title: `delegates to ${ev.agent_type || 'specialist'}`,
        body: ev.assignment || '',
        meta: { stage: 'delegate', agent: ev.agent_type || '', child: ev.child || '' } };

    case KINDS.MEMBER_SAY:
      return { ...base, type: 'message', node: agent, title: '', body: ev.text || '',
        meta: { role: 'assistant', agent, member: true } };

    case KINDS.MEMBER_DONE:
      return { ...base, type: 'status', node: agent,
        title: ev.still_working ? 'member still working when the wait ended' : 'member finished',
        body: ev.summary || '', status: ev.still_working ? 'error' : 'ok',
        meta: { stage: 'member_done', agent, still_working: !!ev.still_working } };

    case KINDS.PLAN:
      /*
       * THE STUDY PLAN. `meta.phases` is the field the console's `readPlan` looks for, and the reason that panel was empty is
       * that nothing here had ever produced it.
       *
       * The title counts rather than describing, because the plan itself is the description and a heading that repeated it
       * would be noise above a list that already says the same thing.
       */
      return { ...base, type: 'plan', node: 'lead',
        title: `plan: ${ev.counts?.done || 0} of ${ev.counts?.total || 0} done`,
        body: '',
        meta: { stage: 'plan', phases: ev.phases || [], counts: ev.counts || {} } };

    case KINDS.TASK:
      return { ...base, type: 'plan', node: 'lead', title: `task ${ev.state}`, body: ev.subject || '',
        meta: { stage: 'task', task_id: ev.id, task_state: ev.state } };

    case KINDS.COMPACT:
      // A run that quietly forgets its own history is worse than one that says so.
      return { ...base, type: 'status', node: 'lead', title: 'compacting context',
        body: ev.detail || '', status: 'running', meta: { stage: 'compact' } };

    case KINDS.ATTACHED: {
      /* Named plainly, and it says how many were NOT found, because that is the number a reader needs. */
      const missing = (ev.items || []).filter((i) => !i.found);
      return { ...base, type: 'status', node: 'lead', title: 'attachments received',
        body: `${ev.found || 0} of ${(ev.items || []).length} attachments resolved`
          + (missing.length ? `. Not found: ${missing.map((i) => i.name).join(', ')}` : ''),
        status: missing.length ? 'warn' : 'ok',
        meta: { stage: 'attachments', items: ev.items || [], found: ev.found || 0 } };
    }

    case KINDS.MEMORY:
      // WHAT WAS CONSULTED, so the console can show whether memory contributed to this run.
      return { ...base, type: 'status', node: 'lead',
        title: ev.failed ? 'memory consultation failed' : 'memory consulted',
        body: ev.detail || '',
        status: ev.failed ? 'error' : 'ok',
        meta: { stage: 'memory', procedures: ev.procedures ?? 0, episodes: ev.episodes ?? 0,
          lessons: ev.lessons ?? 0, failed: !!ev.failed, errors: ev.errors || {} } };

    case KINDS.GATE:
      /*
       * A NOTICE IS NOT A QUESTION, and conflating them put an empty card in front of the operator saying an answer was
       * needed when nothing had been asked.
       *
       * MEASURED on the PROTAC run: the tape held exactly ONE gate event, the governance notice "gates, credits and claim
       * judging are active for this run". The console's `readGate` looks for `question`, `prompt`, `options` or `decided`;
       * a notice has none of them, so it became an undecided question with nothing in it. The operator reported it as
       * "it is saying a question is waiting and answer needed but the card for questions are empty".
       *
       * `type: 'gate'` MEANS THE RUN IS WAITING FOR THIS READER. Only a real decision request may claim it. Everything
       * else -- governance coming up, credits priced, a claim judged -- is a status line, which is what it always was.
       */
      if (!ev.question && !ev.questions && !ev.options) {
        return { ...base, type: 'status', node: ev.child ? agent : 'lead',
          // Gate names are identifiers in the code and prose on the screen: `claim_judgement` was reaching a reader
          // as written. Spaced by the same rule used for verbs, so a new gate needs no entry anywhere.
          title: String(ev.gate || 'governance').replace(/_/g, ' '), body: ev.detail || '',
          status: ev.sourced_ok === false ? 'error' : 'ok',
          meta: { stage: 'notice', gate: ev.gate, advisory: true, ephemeral: false,
            figures: ev.figures, untraced: ev.untraced || [],
            traced: ev.traced ?? null, total_claims: ev.total_claims ?? null,
            unsourced: ev.unsourced || [], complaints: ev.complaints || [],
            credits: ev.credits ?? null } };
      }
      return { ...base, type: 'gate', node: ev.child ? agent : 'lead',
        title: String(ev.gate || ev.kind_detail || 'gate').replace(/_/g, ' '), body: ev.detail || '',
        status: ev.sourced_ok === false ? 'error' : 'ok',
        meta: { stage: 'gate', gate: ev.gate, advisory: ev.advisory !== false,
          // THREE STATES, and the raw fact alongside. `figures` is the judge's answer; `untraced` is what appears in
          // no tool output and travels regardless, so a reader is never shown "figures sourced" beside a gate that
          // lists an untraced figure.
          figures: ev.figures, untraced: ev.untraced || [],
          traced: ev.traced ?? null, total_claims: ev.total_claims ?? null,
          unsourced: ev.unsourced || [], complaints: ev.complaints || [],
          credits: ev.credits ?? null, gpu_seconds: ev.gpu_seconds ?? null, verdict: ev.verdict } };

    case KINDS.REFUSED:
      /*
       * A REFUSAL NAMES WHAT WAS ASKED FOR, NOT THE VERB THAT WOULD HAVE DONE IT.
       *
       * MEASURED on a team run: the only remaining vocabulary leak in any rendered title was `refused: run_python`.
       * Every other surface had been cleaned and this one put the substrate's name in front of the reader at the one
       * moment they most need to understand what happened, which is when something did not happen.
       *
       * The REASON is what matters and is what is shown: governance refused because no plan existed, not because of
       * which tool was about to run. `plan_required` becomes "plan required" by replacing its underscores, which is a
       * derivation rather than a table of reason codes to sentences that would need extending for every new gate.
       */
      return { ...base, type: 'error', node: 'lead',
        title: ev.reason ? `not permitted yet: ${String(ev.reason).replace(/_/g, ' ')}` : 'not permitted yet',
        body: ev.detail || ev.reason || '', status: 'error',
        /* `coaching` TRAVELS, because the console cannot tell a gate that steers the model from one that stops the reader, and
           should not have to guess from the reason string. Set by the gate that raised it; see the note at the plan gate in
           server.mjs for the measurement behind hiding those from a conversation. */
        meta: { stage: 'refused', tool: ev.verb, reason: ev.reason, coaching: ev.coaching === true } };

    case KINDS.SESSION_END:
      return { ...base, type: 'result', node: 'lead',
        title: ev.error ? 'ended with an error' : 'result',
        body: ev.answer || ev.detail || '', status: ev.error ? 'error' : 'ok',
        meta: { final: true, turns: ev.turns ?? null, elapsed_s: ev.ms ? Math.round(ev.ms / 1000) : null,
          cost: ev.cost ?? null, figures_ok: ev.figures_ok, figures: ev.figures,
          untraced: ev.untraced || [], judged: ev.judged } };

    default:
      return null;
  }
}

/* ====================================================================================================================
 * THE ADAPTIVE WORKFLOW, derived from this engine's own tape
 *
 * THE GAP. The console's workflow panel fetches `/v1/operational/runs/:runId/workflow`. The front door passed that
 * through to the previous engine, which builds the graph by reading ITS event store -- and that store has no `max-*`
 * runs at all. MEASURED: HTTP 200 with `0 nodes, 0 edges` for every run of this engine. So the panel the operator asked
 * for by name rendered an empty canvas on every run, while the tape held everything the graph needs.
 *
 * WHAT A METHOD IS HERE. One scientific step, not one tool call. The same verb called four times to design four
 * backbones is ONE method with four attempts, because a reader asking "what did this study do" wants the step, and a
 * reader auditing it wants to know it ran four times. Both facts survive.
 *
 * THE DISPATCHED TOOL IS THE METHOD, NOT `run_python`. The model reaches containers through run_python, so the wire
 * name is always run_python and the container that did the science is invisible. A graph of a PD-L1 campaign that reads
 * "run_python, run_python, run_python" says nothing; one that reads "rfdiffusion, ligandmpnn, boltzdesign" is the study.
 * ================================================================================================================== */

/** The task that was open at a given point, which is the closest thing the tape has to a phase. */
function phaseAt(events, seq) {
  let open = null;
  for (const e of events) {
    if ((e.n ?? 0) > seq) break;
    if (e.kind !== KINDS.TASK) continue;
    if (e.state === 'created') open = e.subject || open;
    else if (e.state === 'completed' && e.subject && e.subject === open) open = null;
  }
  return open || undefined;
}

/** Numeric literals in a finding, so a conclusion can say which figures it rests on. */
function figuresIn(text) {
  return [...new Set(String(text || '').match(/-?\d+\.\d+|-?\b\d{2,}\b/g) || [])].slice(0, 12);
}

export function workflowFrom(run, events) {
  const calls = new Map();
  for (const e of events) {
    if (e.kind === KINDS.CALL) calls.set(e.id, e);
  }
  const byMethod = new Map();
  const order = [];

  const record = (name, e, call, done, failed) => {
    let m = byMethod.get(name);
    if (!m) {
      m = {
        id: `m-${byMethod.size + 1}`,
        method: name,
        // ORIGIN IS THE HONEST CATEGORY. The tape records whether a verb is the platform's or the loop's own, and that
        // is a fact; inventing scientific categories from tool names would be a guess dressed as structure.
        category: e.origin || 'tool',
        categoryLabel: e.origin === 'platform' ? 'Platform capability' : 'Agent tool',
        tools: [], steps: [], attempts: 0, status: 'running',
        phase: phaseAt(events, e.n ?? 0),
      };
      byMethod.set(name, m);
      order.push(m);
    }
    m.attempts += 1;
    m.steps.push(e.n ?? 0);
    if (!m.tools.includes(e.verb) && e.verb) m.tools.push(e.verb);
    if (done) m.status = 'done';
    else if (failed && m.status !== 'done') m.status = 'failed';
    if (!m.summary) {
      const first = String(e.output || '').split(/\\n|\n/).map((x) => x.trim()).filter(Boolean)[0];
      if (first) m.summary = first.slice(0, 220);
    }
    if (call && !m.inputs?.length) {
      const inp = call.input && typeof call.input === 'object' ? Object.keys(call.input) : [];
      if (inp.length) m.inputs = inp.slice(0, 8);
    }
    return m;
  };

  /*
   * TASK BOOKKEEPING IS NOT A SCIENTIFIC METHOD, and this is derived rather than listed.
   *
   * The loop keeps its task list through its own tools, so a graph built from raw calls opened with `TaskCreate` and
   * `TaskUpdate` as though they were steps of the study -- next to the previous engine's graph, which reads "Target
   * structure acquisition" and "Denovo mini-binder generation with BinderFlow". The structural test: a call whose window
   * contains a task event is a call that was MAINTAINING the task list, and that fact is already shown as the to-do
   * list. Representing it again as a method double-counts one fact and buries the science.
   */
  const taskSeqs = events.filter((e) => e.kind === KINDS.TASK).map((e) => e.n ?? -1);
  /*
   * THE TEST IS ON THE VERB, NOT ON THE SINGLE CALL, and that correction came from watching it half-work. Checking each
   * call's own window caught `TaskCreate`, whose window did contain a task event, and MISSED `TaskUpdate`, whose two
   * calls happened not to straddle one -- so the graph still opened with a bookkeeping step. A verb that maintained the
   * task list ONCE is a bookkeeping verb for the whole run, so one observation is generalised to every call of it. The
   * set is still computed from this run's own tape; nothing is hand-listed.
   */
  const bookkeepingVerbs = new Set();
  for (const e of events) {
    if (e.kind !== KINDS.BACK) continue;
    const call = calls.get(e.id);
    if (!call) continue;
    const lo = call.n ?? 0;
    const hi = e.n ?? lo;
    if (taskSeqs.some((t) => t >= lo && t <= hi) && call.verb) bookkeepingVerbs.add(call.verb);
  }
  const isBookkeeping = (call, back) => {
    const verb = call?.verb || back?.verb;
    return Boolean(verb && bookkeepingVerbs.has(verb));
  };

  for (const e of events) {
    if (e.kind !== KINDS.BACK) continue;
    const call = calls.get(e.id) || null;
    if (isBookkeeping(call, e)) continue;
    const failed = e.failed_inside === true || e.returned === false;
    const ds = dispatchesIn(e.output);
    if (ds.length) {
      // A run_python that dispatched containers is one method PER CONTAINER, because that is where the science happened.
      for (const d of ds) {
        const m = record(d.tool, e, call, d.rc === 0, d.rc !== 0);
        if (!m.frameworks) m.frameworks = ['container'];
        if (typeof d.seconds === 'number' && d.seconds > 0) {
          m.parameters = { ...(m.parameters || {}), seconds: d.seconds, gpu: d.gpu };
        }
      }
    } else {
      record(e.verb || 'step', e, call, !failed, failed);
    }
  }

  // A call with no answer yet is a method that is RUNNING, which is the whole point of a live canvas.
  for (const [, c] of calls) {
    if (events.some((e) => e.kind === KINDS.BACK && e.id === c.id)) continue;
    record(c.verb || 'step', c, c, false, false);
  }

  const ended = events.find((e) => e.kind === 'session.end') || {};
  const answer = run?.answer || ended.answer || '';
  const conclusions = answer
    ? [{ id: 'c-1', finding: String(answer).slice(0, 1200), figures: figuresIn(answer),
        methods: order.map((m) => m.id) }]
    : [];

  return {
    ok: true,
    runId: run?.id,
    schemaVersion: 1,
    // NOT INTERPRETED, and saying so matters: this graph is read straight off the tape with no model in the loop, so
    // nothing in it is a paraphrase. The console shows the difference.
    interpreted: false,
    methods: order,
    conclusions,
    runState: run?.state,
    runActive: run?.state === 'running',
    stepsRead: events.length,
    model: run?.model,
    revision: events.length,
    updatedAt: Date.now(),
    canRebuild: false,
  };
}
/* ====================================================================================================================
 * WHAT A STEP WAS FOR, said in the words the run itself used
 *
 * THE OPERATOR, watching a PROTAC ternary-complex study: "they are all titled run python instead of human readable
 * texts for scientist users". Sixty events in a row reading `run_python` is a log, not a record of a study.
 *
 * THE CAPTION IS ALREADY IN THE INPUT AND I WAS THROWING IT AWAY. Nearly every call the loop writes opens with a comment
 * saying what it is about to do, because that is how people write analysis code. From the operator's own run:
 *     # CRITICAL FINDING: 5T35 has 4 molecules including BRD4!
 *     # Get JQ1 atom coordinates and identify the exit vector
 *     # The PROTAC 759 has 69 atoms spanning both VHL and BRD4 pockets
 * Those are better titles than anything a rule could compose, and they are the author's own words rather than a guess.
 *
 * NEVER INVENTED. No comment means the verb, which is honest and no worse than today.
 * ================================================================================================================== */

/*
 * THE CODE A STEP IS ABOUT TO RUN, so the card can show the work while it is happening.
 *
 * `call_id` AND `execute` ARE THE CONSOLE'S EXISTING VOCABULARY, not a new one invented here. `console/conversation.ts`
 * already opens an `act` unit on `execute`, keyed on `meta.call_id`, marks it running, and closes it when the matching
 * `observe` arrives -- the whole mechanism the operator asked for was already built and tested for the previous engine.
 * This engine was emitting `tool_call` with its own id field, which that code has no branch for, so `observe` fell into
 * its "no open act" path and MANUFACTURED A FRESH UNIT AT RESULT TIME. That is the entire "cards load after the pythin
 * is ran": a step ran for 141 seconds on the operator's CPTAC run and the reader saw nothing until it finished.
 *
 * Speaking the vocabulary that already works is better than teaching the console a second one. Two mechanisms for the
 * same fact is how a producer and a browser drift apart.
 */
/* ==================================================================================================================
 * AN EVENT BODY AS SOMETHING A PERSON CAN READ
 * ==================================================================================================================
 *
 * THE OPERATOR: "for the event stream cards, the ones that have python code, the codes view is not considering the next
 * line slashes and all the codes are packed together instead of being shown in proper lines." Then, after a first fix
 * that changed the wrong layer: "it is still not solved. make sure you do a fundamental fix."
 *
 * WHAT IS ACTUALLY HAPPENING, measured against the stored tape of run max-c3eca0b57a through the real /tape endpoint.
 * Five of its 86 event bodies carry LITERAL backslash-n and zero real newlines. They are the results of the python
 * steps, and they look like this:
 *
 *     {"output": "Downloaded 6LU7: 239112 chars, 2952 lines\nNon-solvent HETATM residues: {...}\n\n[note] ..."}
 *
 * An MCP tool returns its result as TEXT, and that text is itself a JSON document. So the newlines in it are JSON
 * ESCAPES, two characters each, and nothing on the way to the screen ever parsed them back. `typeof ev.output ===
 * 'string'` was true, so the string was forwarded verbatim and the reader got a one-line blob.
 *
 * WHY MY FIRST ATTEMPT MISSED, recorded because the shape of the mistake matters more than the fix. I changed `asText`
 * in the console's own conversation builder, which handles bodies that arrive as OBJECTS. These arrive as STRINGS that
 * merely contain JSON, so the string branch returned early and the new code never ran. I verified the wrong layer: the
 * synthetic event I built to reproduce had an object body, which the real engine never sends. Driving the real
 * PRODUCER, or reading one real stored event, would have shown that immediately.
 *
 * THIS IS THE ONE PLACE TO FIX IT. `toConsoleEvent` is the only translator from engine events to console events, and it
 * runs on read: the live stream and the history endpoint both go through it. So this repairs every run already on disk
 * as well as every future one, without a migration.
 *
 * NO LIST OF FIELD NAMES. `codeOf` below reads `code`, `script`, `source`, which is a list that goes stale the first
 * time a tool names its argument something else, and the fallback then packed the whole payload onto one line. What
 * identifies the readable part of a payload is its SHAPE: it is the longest string in there. Nothing else about the
 * field matters, so nothing needs to be enumerated.
 * ================================================================================================================== */

/** How much of a payload a SINGLE-LINE string must account for before it is shown alone. */
const DOMINATES = 0.6;

/**
 * Every multi-line string inside a payload, with the key it was found under.
 *
 * WHY MULTI-LINE SPECIFICALLY, and why this is the whole mechanism rather than a detail. `JSON.stringify` ESCAPES
 * NEWLINES INSIDE STRING VALUES. Indenting the document does not change that: pretty-printing puts the keys on separate
 * lines and leaves every newline inside a value as a two-character escape. So a payload holding printed output can
 * never be shown by serialising it, at any indent. The multi-line strings have to be lifted OUT and printed as
 * themselves.
 *
 * Depth-capped, because bodies come off the wire and may be cyclic.
 */
function multilineStrings(value, depth = 0, key = '') {
  if (depth > 6) return [];
  if (typeof value === 'string') return value.includes('\n') ? [{ key, text: value }] : [];
  if (Array.isArray(value)) {
    return value.flatMap((item, n) => multilineStrings(item, depth + 1, key ? `${key}[${n}]` : `[${n}]`));
  }
  if (value !== null && typeof value === 'object') {
    return Object.entries(value).flatMap(([k, item]) =>
      multilineStrings(item, depth + 1, key ? `${key}.${k}` : k),
    );
  }
  return [];
}

/** The longest string anywhere inside a payload, used only when no multi-line string exists. */
function longestString(value, depth = 0) {
  if (depth > 6) return null;
  if (typeof value === 'string') return value;
  const items = Array.isArray(value)
    ? value
    : value !== null && typeof value === 'object'
      ? Object.values(value)
      : null;
  if (!items) return null;
  let best = null;
  for (const item of items) {
    const found = longestString(item, depth + 1);
    if (found !== null && (best === null || found.length > best.length)) best = found;
  }
  return best;
}

/**
 * A payload rendered for a human, whatever shape it arrived in.
 *
 * A STRING CARRYING JSON IS PARSED FIRST. That is what turns a two-character escape back into a newline. Only a
 * document is unwrapped, never a bare scalar: `42` and `null` parse, and a tool that printed either meant the text.
 *
 * THEN THE MULTI-LINE STRINGS ARE LIFTED OUT AND PRINTED AS THEMSELVES.
 *
 * WHAT THE OPERATOR PASTED, which is why this is not the ratio I tried first. A run_python result is
 * `{ output, meta, workspace, operation_class, files_written }`. The printed output is well under 60% of that document,
 * so it failed a dominance test and fell through to pretty-printing -- and pretty-printing re-escaped every newline it
 * contained. The card showed indented JSON with `\n` running through the middle of it. The ratio was the wrong
 * instrument: what matters is not how BIG the readable part is, it is that a multi-line string cannot survive being
 * serialised at all.
 *
 * One multi-line string is returned alone. Several are printed as labelled blocks, so a result carrying both stdout and
 * a traceback shows both rather than whichever happened to be longer. The single-line ratio survives for payloads with
 * no multi-line content, where serialising is harmless because there are no newlines to escape.
 *
 * WHAT IS DELIBERATELY LEFT OUT. Returning the output alone hides the bookkeeping beside it: `meta.returncode`,
 * `workspace`, `files_written`. None of it is lost to the reader, because the console already carries each one
 * elsewhere -- the outcome tick comes from `status` on this same event, files are announced as artifacts and appear in
 * the previews, and the workspace is on the run. Printing them again under every step is the log the operator asked us
 * to stop being: "sixty events in a row reading run_python is a log, not a record of a study."
 *
 * KNOWN LIMIT, stated rather than hidden: the engine slices a tool result to 12000 characters before emitting, so a
 * longer document arrives cut mid-string and cannot parse. Those degrade to the raw text and stay escaped. The fix is
 * to slice the readable text rather than the document, which is a change on the emit path and not here.
 */
export function readableBody(value) {
  if (value === null || value === undefined) return '';

  let subject = value;
  if (typeof value === 'string') {
    const trimmed = value.trim();
    if (!trimmed.startsWith('{') && !trimmed.startsWith('[')) return value;
    try {
      const parsed = JSON.parse(trimmed);
      if (parsed === null || typeof parsed !== 'object') return value;
      subject = parsed;
    } catch {
      // Not JSON after all, or truncated mid-document. The text is the best we have.
      return value;
    }
  }

  const multi = multilineStrings(subject);
  if (multi.length === 1) return multi[0].text;
  if (multi.length > 1) {
    return multi.map(({ key, text }) => (key ? `${key}:\n${text}` : text)).join('\n\n');
  }

  let pretty;
  try {
    pretty = JSON.stringify(subject, null, 2);
  } catch {
    return typeof value === 'string' ? value : '';
  }
  if (typeof pretty !== 'string') return typeof value === 'string' ? value : '';

  const longest = longestString(subject);
  if (longest !== null && longest.length >= pretty.length * DOMINATES) return longest;
  return pretty;
}

function codeOf(input) {
  if (!input || typeof input !== 'object') return '';
  return String(input.code ?? input.script ?? input.source ?? '');
}

/** The first comment line of a snippet, which is what the author wrote to explain the step. */
export function captionFrom(input) {
  const code = input && typeof input === 'object'
    ? String(input.code ?? input.script ?? input.source ?? '')
    : '';
  if (!code) return '';
  for (const raw of code.split(/\r?\n/).slice(0, 12)) {
    const line = raw.trim();
    if (!line) continue;
    if (!line.startsWith('#')) {
      // Code before any comment means the author did not caption this step. Reading further would pick up a comment
      // about a detail halfway down and present it as the purpose of the whole step.
      break;
    }
    const text = line.replace(/^#+\s*/, '').trim();
    // A ruler or a shebang is punctuation, not a caption.
    if (!text || /^[-=*_#\s]+$/.test(text) || text.startsWith('!')) continue;
    if (text.length < 3) continue;
    return text.slice(0, 120);
  }
  return '';
}

/**
 * WHAT AN OPERATION WAS ABOUT, taken from the call's own arguments.
 *
 * MEASURED PROBLEM. `captionFrom` reads only code fields, so every verb that is not a code runner fell through to its
 * own name, and the names the SDK uses are not science: a live run put "Skill", "Read", "TaskCreate" and "TaskUpdate"
 * on the wire as step titles. The operator was explicit that this is the thing to remove -- "we want the scientist user
 * to feel like home and not a strage place with unknown vocabulary" -- and my earlier vocabulary ban list did not catch
 * these, because I wrote it before I had seen them.
 *
 * DERIVED, NOT TABULATED. There is no map here from a tool name to a phrase. Such a map would need a new entry for
 * every built-in the SDK adds and would say nothing about what THIS call did. What a reader wants is the SUBJECT: which
 * file was read, which task was created. That is in the arguments, and reading them works for a tool nobody has seen
 * yet.
 *
 * Preference order is about how much a value tells a reader:
 *   1. prose, meaning a value with spaces in it, which is how a task subject or a description arrives
 *   2. a path, reduced to its basename, since the directory is noise and the filename is the subject
 *   3. any other short string
 * Long values are skipped rather than truncated: a wall of text is not a title.
 */
/**
 * Whether a value is a handle rather than something to read.
 *
 * Three shapes, all of them things this system actually passes around: a short prefix followed by digits (`t1`, `run7`),
 * a long unbroken hexadecimal or base32 token (`toolu_bdrk_01CBCgvbUjx`, a sha), and a uuid.
 */
/** Extensions this platform produces. One definition, because two would drift. */
const FILE_EXT = /\.(png|svg|jpe?g|csv|tsv|md|markdown|pdb|cif|sdf|mol2|json|parquet|html|txt|py|tex|gz)$/i;

function isOpaqueId(v) {
  /*
   * A FILENAME IS NEVER A HANDLE, and this has to be decided FIRST.
   *
   * MEASURED: with this check placed last, `/s1/logp_chart_2.png` was rejected by the "mostly not letters" rule below,
   * which counts the slashes, the underscores, the digit and the dot and finds seven non-letters in twenty characters.
   * The path never reached the exemption written for it, and a card that should have read "logp_chart_2.png" read
   * "read". Checked against a closed set of extensions this platform produces, so a version string is not mistaken for
   * a file.
   */
  if (FILE_EXT.test(v)) {
    return false;
  }
  if (/^[A-Za-z]{0,6}[-_]?\d{1,6}$/.test(v)) return true;
  if (/^[0-9a-f]{12,}$/i.test(v)) return true;
  if (/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(v)) return true;
  // A token with no spaces that is mostly not letters reads as machine output, not as a subject.
  if (!v.includes(' ') && v.length >= 16 && (v.match(/[^A-Za-z]/g) || []).length > v.length / 3) return true;
  /*
   * A HANDLE: no spaces, long, and joining words to digits with separators. `toolu_bdrk_01CBCgvbUjx` is the shape, and
   * it survived every rule above because it is not hex and not mostly punctuation.
   *
   * Filenames were exempted at the top of this function, so they never reach here.
   */
  if (!v.includes(' ') && v.length >= 12 && /\d/.test(v) && /[_-]/.test(v)) return true;
  return false;
}

export function subjectFrom(input) {
  if (!input || typeof input !== 'object') return '';
  const strings = [];
  for (const [key, value] of Object.entries(input)) {
    if (typeof value !== 'string') continue;
    const v = value.trim();
    // Code is captionFrom's business, and a whole script is never a title.
    if (!v || v.length > 200 || /\r?\n/.test(v)) continue;
    if (key === 'code' || key === 'script' || key === 'source') continue;
    // AN OPAQUE IDENTIFIER IS NOT A SUBJECT. MEASURED: a TaskUpdate carrying {task_id: 't1', task_state: 'completed'}
    // was titled "t1", which tells a reader strictly less than the verb name it replaced. Rejected by SHAPE rather than
    // by field name, so a run id, a call id or a handle nobody has named yet is caught the same way.
    if (isOpaqueId(v)) continue;
    strings.push(v);
  }
  if (strings.length === 0) return '';
  const prose = strings.filter((v) => v.includes(' ') && v.length <= 120);
  if (prose.length > 0) {
    // The longest reads as the most complete description of the two, a subject beating a one word status.
    prose.sort((a, b) => b.length - a.length);
    return prose[0];
  }
  const paths = strings.filter((v) => v.includes('/'));
  if (paths.length > 0) {
    const base = paths[0].split('/').filter(Boolean).pop();
    if (base) return base;
  }
  const short = strings.filter((v) => v.length <= 60);
  if (short.length === 0) return '';
  /*
   * UNDERSCORES BECOME SPACES, but only where the value is not a filename.
   *
   * MEASURED: a TaskUpdate's status arrived as the title "in_progress", which is a machine token in a place a person
   * reads. A filename must be left exactly as it is, because `logp_chart.png` is the name of a real object and
   * "logp chart.png" is not, so the same extension test that exempts filenames from being treated as handles exempts
   * them from being reworded.
   */
  return FILE_EXT.test(short[0]) ? short[0] : short[0].replace(/_/g, ' ');
}

/**
 * A title a scientist can read.
 *
 * The author's own caption first, then what the call was about, and the verb only when the arguments say nothing at all.
 * That last case is spaced out of its camel case rather than left as an identifier: `TaskCreate` becomes "Task create".
 * It is still not scientific vocabulary, and it is what honesty leaves: with no evidence of a subject, inventing a
 * scientific phrase would be a fabrication, and this platform's whole auditing posture is against that.
 */
export function titleFor(verb, input) {
  const caption = captionFrom(input);
  if (caption) return caption;
  const subject = subjectFrom(input);
  if (subject) return subject;
  const name = String(verb || '');
  return name.replace(/([a-z0-9])([A-Z])/g, '$1 $2').replace(/_/g, ' ').toLowerCase();
}

