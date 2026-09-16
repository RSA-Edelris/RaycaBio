/**
 * The bridge to the platform run store and the scientific workflow interpreter.
 *
 * SAME SHAPE AS governance.mjs: a long-lived Python subprocess speaking JSON lines. One process, kept alive,
 * restarted if it dies. This is NOT a second mechanism: it is the same pattern the operator already trusts,
 * with a different Python file behind it.
 *
 * WHY A SIBLING AND NOT AN EXTENSION OF governance_bridge.py. The governance bridge's failure posture is
 * ALLOW ON FAILURE (a dead sidecar must not stop science). The runstore bridge's failure posture is the
 * opposite: a run not registered is invisible to files/all, artifacts and lineage. Mixing them means a
 * governance restart (which happens when the claim judge OOMs on a long answer) would also blank the file
 * manager until the bridge recovers. Separate processes, separate failure domains.
 *
 * MEASURED NEED: a PROTAC team run wrote 3MXF.pdb, 5T35.pdb, JQ1_ideal.sdf, VH032_ideal.sdf and the file
 * manager stayed empty because runstore.store().sessions() had no max-* runs.
 */

import { spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { resolveEnv } from './env.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ENV = resolveEnv();
const PY = ENV.py;
const BRIDGE = join(HERE, 'runstore_bridge.py');
const SRC = ENV.src;

class RunstoreBridge {
  constructor() {
    this.proc = null;
    this.waiting = new Map();
    this.seq = 0;
    this.buf = '';
    this.available = false;
  }

  start() {
    if (this.proc) return;
    this.proc = spawn(PY, [BRIDGE], {
      env: { ...process.env, RAYCA_SRC: SRC, PYTHONPATH: SRC },
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    this.available = true;
    this.proc.stdout.on('data', (d) => {
      this.buf += d.toString();
      let i;
      while ((i = this.buf.indexOf('\n')) >= 0) {
        const line = this.buf.slice(0, i).trim();
        this.buf = this.buf.slice(i + 1);
        if (!line) continue;
        try {
          const msg = JSON.parse(line);
          const w = this.waiting.get(msg.id);
          if (w) { this.waiting.delete(msg.id); w(msg.result); }
        } catch { /* partial or noisy line is not a protocol failure */ }
      }
    });
    this.proc.stderr.on('data', (d) => process.stderr.write('[runstore] ' + d.toString()));
    this.proc.on('exit', (code) => {
      process.stderr.write(`[runstore] bridge exited (${code}); will restart on next call\n`);
      this.available = false;
      this.proc = null;
      for (const [, w] of this.waiting) w(null);
      this.waiting.clear();
    });
  }

  async ask(op, params, timeoutMs = 30000) {
    this.start();
    if (!this.available) return null;
    const id = ++this.seq;
    const p = new Promise((resolve) => {
      this.waiting.set(id, resolve);
      setTimeout(() => {
        if (this.waiting.has(id)) { this.waiting.delete(id); resolve(null); }
      }, timeoutMs);
    });
    try {
      this.proc.stdin.write(JSON.stringify({ id, op, ...params }) + '\n');
    } catch {
      this.waiting.delete(id);
      return null;
    }
    return p;
  }
}

const bridge = new RunstoreBridge();

export const platformStore = {
  /**
   * Register a new run so files/all, artifacts and lineage can see it.
   *
   * Called when a run starts. The session_key is the CONVERSATION id (console_session), not the
   * transcript session, because that is what workspace_for() and the file endpoints use.
   */
  async registerRun({ runId, sessionKey, task, state, createdAt }) {
    /*
     * REGISTRATION IS RETRIED, BECAUSE LOSING IT LOSES THE SESSION'S FOLDER.
     *
     * MEASURED, and the operator found it before I did: "no files for this sssion is appearing oon the file manger, even th
     * session folder is not crated." The files were all present -- 61 on disk, 50 registered, 28 MB -- and the session had no
     * folder, because the file manager builds its list of sessions from RUNS. A session whose run is missing has nowhere to
     * show its files.
     *
     * WHY IT WAS MISSING. `bridge.ask` resolves NULL after 30 seconds rather than rejecting, and the log records the failure
     * exactly 30 seconds after the run began: `[runstore] register failed for max-6a8ebf8fc0: null`. The bridge is one process
     * handling one op at a time, and a run start fires several at once -- workspace, snapshot, files, workflow, lineage -- so
     * registration queues behind them and one slow start is enough to drop it. Fire and forget was right for lineage, which is
     * a nice-to-have, and wrong here, because a run's existence is what makes its files reachable.
     *
     * THREE ATTEMPTS, SPACED, because the cause is contention rather than a bad request: the same call that timed out at run
     * start succeeds seconds later, which I confirmed by making it by hand for the run that had been lost. Beyond three
     * attempts the problem is not contention and a fourth will not find that out.
     */
    let last = null;
    for (let attempt = 1; attempt <= 3; attempt += 1) {
      last = await bridge.ask('register_run', {
        run_id: runId,
        session_key: sessionKey,
        task: task || '',
        state: state || 'running',
        created_at: createdAt ? createdAt / 1000 : Date.now() / 1000,
        started_at: Date.now() / 1000,
      });
      if (last && last.ok) {
        if (attempt > 1) {
          process.stderr.write(`[runstore] registered ${runId} on attempt ${attempt}\n`);
        }
        return last;
      }
      /* Spaced so the queue this is stuck behind has time to drain, and not so long that a finished run reports before it. */
      if (attempt < 3) {
        await new Promise((done) => setTimeout(done, attempt * 4000));
      }
    }
    process.stderr.write(
      `[runstore] register failed for ${runId} after 3 attempts: ${JSON.stringify(last)}. ` +
        'Its files will not be listed under a session folder until it is registered.\n',
    );
    return last;
  },

  /**
   * Update a run's state (complete, error, cancelled).
   *
   * Called when a run finishes so the run store's state matches reality.
   */
  async updateRun({ runId, state, error }) {
    return bridge.ask('update_run', {
      run_id: runId,
      state: state || 'complete',
      error: error || '',
      ended_at: Date.now() / 1000,
    });
  },

  /**
   * Interpret a run's events scientifically using wfdistil + wfinterp.
   *
   * Returns the workflow document with interpreted:true when a model actually ran, or
   * interpreted:false with a note explaining why not. The caller keeps the structural
   * deriver as the fallback.
   *
   * Timeout is generous (90s) because interpretation involves an LLM call.
   */
  /*
   * ONE OPENLINEAGE RUN EVENT, and never fatal.
   *
   * WHY THIS IS SO SMALL. `rayca_lineage` is 2,843 lines across eleven modules: an OpenLineage emitter, LangFuse and
   * MLflow bridges, idempotent Marquez sync, and an identity module that mints ONE value and re-encodes it so a run
   * carries the same identity in every system. `governance/lineage.py` already exposes it, already redacts
   * caller-supplied facets, and already promises never to raise. The only thing missing was a caller on this side.
   *
   * MEASURED: identity_for('max-x') returns available=true with an ol_run_id, so runs of this engine were always
   * eligible and nothing ever emitted for them. That is why WS-3 T-3.10 stayed open.
   */
  async lineageEvent({ runId, eventType, jobName = '', facets = {} }) {
    try {
      return await bridge.ask('lineage_event', {
        run_id: runId, event_type: eventType, job_name: jobName, facets,
      });
    } catch {
      // Lineage that can break a run is worse than no lineage. That is the module's own rule and it holds here too.
      return { ok: false, emitted: false, reason: 'bridge_unavailable' };
    }
  },

  /**
   * Where a session's files live.
   *
   * ASKED FOR RATHER THAN COMPOSED, because the path carries a hash that this side cannot derive. It becomes the agent
   * session's working directory, so a tool writing a relative path writes into the study instead of into whatever
   * directory the service happens to have started in.
   */
  async workspace(session) {
    const r = await bridge.ask('workspace', { session });
    return r && r.ok ? String(r.path || '') : '';
  },

  /** The filesystem state to diff a later registration against. */
  /*
   * STOP A CONTAINER JOB, at the researcher's request.
   *
   * The whole result is returned rather than a boolean, because a cancel that did not stop anything must be
   * distinguishable from one that did. A researcher told "cancelled" who comes back to a busy GPU has been misled by
   * their own tool, which is worse than no button at all.
   */
  /* Ask the scheduler what a job is doing. Used by the watcher in server.mjs, which outlives the run. */
  async pollClusterJob({ jobId, provider, runId, resultsInto }) {
    const r = await bridge.ask('poll_cluster_job', {
      job_id: jobId, provider, run_id: runId, results_into: resultsInto || '',
    });
    return r || { ok: false, error: 'bridge_unreachable' };
  },

  async cancelContainer(container) {
    const r = await bridge.ask('cancel_container', { container });
    return r || { ok: false, error: 'bridge_unreachable' };
  },

  async snapshot(session) {
    const r = await bridge.ask('snapshot', { session });
    return r && r.ok ? (r.before || {}) : null;
  },

  /**
   * Register everything that has appeared in the workspace since `before`.
   *
   * THE UNIVERSAL SEAM, and the reason it exists is measured: registration used to happen inside the code-running verb
   * only, so files written by the SDK's own tools were never filed. On a real study `Bash` put 754 MB of retrosynthesis
   * models outside the session and the workspace held nothing but source. This is called from the one hook that sees
   * every tool.
   */
  async registerFiles({ session, before, runId, stepTitle, phase, phaseIndex }) {
    const r = await bridge.ask('register_files', {
      session, before, run_id: runId || '', step_title: stepTitle || '',
      // THE PHASE, so `filing.folder_for` can put the file in its phase's folder. It has accepted these
      // two arguments all along and the live path passed neither: measured on run max-604740ffad, all 43
      // produced records carried no phase.
      phase: phase || '', phase_index: Number.isFinite(Number(phaseIndex)) ? Number(phaseIndex) : null,
    });
    return r && r.ok ? (r.files || []) : [];
  },

  /**
   * Every artifact the index holds for one run, whoever filed it.
   *
   * The diff-based registration above only reports what IT discovered. A file already filed by the code runner is invisible
   * to it, and was therefore never announced to a reader. This asks the index instead, so announcement no longer depends on
   * which registrar happened to see the file first.
   */
  /**
   * Render and file one phase's Markdown report, returning its path.
   *
   * The renderer lives in Python beside the records it reads. This is the seam that already carries the run store
   * across the boundary, so the report is written by the side that holds the workflow and the artifact index.
   */
  /**
   * The dashboard standard for a session, with that session's own artifact inventory folded in.
   *
   * The standard lives in the engine rather than in whatever the user managed to type, which is the whole point: every
   * user gets the researched version, not the one they could describe.
   */
  async dashboardBrief({ session, title }) {
    const r = await bridge.ask('dashboard_brief', { session, title: title || '' }, 30000);
    return r && r.ok ? (r.brief || '') : '';
  },

  /**
   * Substitute the vendored libraries into any dashboard the run wrote, and report what external references remain.
   *
   * A model cannot type 1.3 MB of Plotly, and left to itself it reaches for a CDN, which is what every earlier
   * dashboard on this platform did. Sixty seconds because the file can be several megabytes.
   */
  async dashboardFinalise({ session }) {
    const r = await bridge.ask('dashboard_finalise', { session }, 120000);
    return r && r.ok ? (r.files || []) : [];
  },

  async phaseReport({ session, runId, phase, images, model }) {
    /* `images` comes from the TAPE, which is the only place a container image is recorded: the workflow
       method records the report is built from carry no such field. Without it the report cannot write the
       `Container Image:` line, and the `container_doc` obligation would be decorative. */
    const r = await bridge.ask('phase_report', {
      session, run_id: runId || '', phase, images: images || [], model: model || '' }, 60000);
    return r && r.ok ? (r.path || '') : '';
  },

  async filesForRun({ session, runId }) {
    const r = await bridge.ask('files_for_run', { session, run_id: runId || '' });
    return r && r.ok ? (r.files || []) : [];
  },

  async interpretWorkflow({ runId, sessionKey, task, events }) {
    return bridge.ask('interpret_workflow', {
      run_id: runId,
      session_key: sessionKey || '',
      task: task || '',
      events,
    }, 90000);
  },
};
