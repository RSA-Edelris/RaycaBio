/**
 * Runs and sessions that survive a restart.
 *
 * WHY DURABLE. The pilot kept runs in a `Map` in process memory, which is the same defect as the engine's in-memory
 * `_JOBS` dict: when the engine was OOM-killed this morning every cluster job it was tracking became unattributable,
 * and the researcher's study died at 1,344 events with no report. A run is the record of expensive, irreversible work
 * -- GPU hours, cluster submissions, real money -- so losing the record because a process restarted is not acceptable.
 *
 * AND ATTACHABLE, WHICH IS A SEPARATE PROBLEM. During the PD-L1 run the operator's browser could not see a run it had
 * not started, because the only handle was the id returned by the POST that created it. Runs are listed here so any
 * reader can attach to any run, which is also what made the console's rail panels blank on a run with 1,288 events.
 */

import { DatabaseSync } from 'node:sqlite';
import { mkdirSync } from 'node:fs';
import { dirname } from 'node:path';

export class Store {
  constructor(path) {
    mkdirSync(dirname(path), { recursive: true });
    this.db = new DatabaseSync(path);
    this.db.exec(`
      PRAGMA journal_mode = WAL;
      CREATE TABLE IF NOT EXISTS runs (
        id TEXT PRIMARY KEY,
        session_id TEXT,
        task TEXT NOT NULL,
        team INTEGER NOT NULL DEFAULT 0,
        model TEXT,
        state TEXT NOT NULL,
        started_ms INTEGER NOT NULL,
        -- Which process is driving this run, so orphan reconciliation can ask whether the owner is still
        -- alive rather than assuming any row marked running belongs to a process that died.
        owner_pid INTEGER,
        ended_ms INTEGER,
        turns INTEGER,
        cost REAL,
        answer TEXT
      );
      -- CLUSTER JOBS OUTLIVE THE RUN THAT SUBMITTED THEM, so they are recorded here rather than in memory.
      --
      -- MEASURED: the operator submitted a 12 hour MD job to Isambard, the run finished after submitting it, and asking
      -- a LATER run about job 6102452 answered "this run did not submit job 6102452, so there is nothing to report on".
      -- governance/cluster.py keeps its job table in a module-level dict inside the MCP server, which modulon-max
      -- spawns PER QUERY, so both the record and the watcher thread died with the process that made them.
      --
      -- A row here survives the run, the process and a restart, which is the least a 12 hour job deserves.
      CREATE TABLE IF NOT EXISTS cluster_jobs (
        job_id TEXT PRIMARY KEY,
        run_id TEXT,
        console_session TEXT,
        cluster TEXT,
        provider TEXT,
        host TEXT,
        state TEXT,
        scheduler_state TEXT,
        submitted_ms INTEGER,
        updated_ms INTEGER,
        ended_ms INTEGER,
        files TEXT,
        analysis_run TEXT,
        -- WHERE COLLECTED OUTPUTS GO, which the watcher cannot work out for itself.
        --
        -- MEASURED: job 6102566 completed and collected NOTHING. The watcher asked poll_remote to copy results into
        -- job.results_into, this table had no such column, so it passed an empty string and collection was skipped
        -- silently. The trajectory a 12 hour job exists to produce would have been left on the cluster.
        results_into TEXT
      );
      CREATE TABLE IF NOT EXISTS events (
        run_id TEXT NOT NULL,
        n INTEGER NOT NULL,
        at_ms INTEGER NOT NULL,
        kind TEXT NOT NULL,
        body TEXT NOT NULL,
        PRIMARY KEY (run_id, n)
      );
      CREATE INDEX IF NOT EXISTS events_run ON events(run_id, n);
    `);

    /*
     * TWO DIFFERENT THINGS ARE CALLED A SESSION, AND CONFLATING THEM MADE EVERY RUN INVISIBLE TO THE CONSOLE.
     *
     * `session_id` is the LOOP's session -- the transcript, what a resume or a fork reads. The console's session is the
     * CONVERSATION, and it is how the console asks "which runs belong to this chat" through
     * GET /v1/operational/runs?session_id=X. We recorded only the first, so that question passed through the front door
     * to the previous engine, which has never heard of a `max-` run, and answered `runs: []`.
     *
     * MEASURED CONSEQUENCES: reloading the page mid-run lost the run, and a forked run executed with nothing in the
     * browser showing it. The live stream was the ONLY way any run of this engine was ever visible.
     *
     * Added as a migration rather than a schema change because existing runs must keep working; a missing value simply
     * means "recorded before this column existed".
     */
    try {
      this.db.exec('ALTER TABLE runs ADD COLUMN console_session TEXT');
      } catch { /* already present */ }
      try {
        /* An empty value means "recorded before this column existed", and reconciliation then behaves as it always did
           rather than guessing at a liveness it cannot check. */
        this.db.exec('ALTER TABLE runs ADD COLUMN owner_pid INTEGER');
    } catch { /* already present */ }
    try {
      // The table shipped before this column existed, so an existing database needs it added.
      this.db.exec('ALTER TABLE cluster_jobs ADD COLUMN results_into TEXT');
    } catch { /* already present */ }
    try {
      // WHY A JOB FAILED. The table could say a job failed and never why, so all 33 failures on record carry a state and
      // nothing else, and every diagnosis needed a human to open a log. The engine reads the reason out of the job's own log
      // -- the ERR trap already prints the failing line and command -- and sends it here.
      this.db.exec('ALTER TABLE cluster_jobs ADD COLUMN reason TEXT');
    } catch { /* already present */ }
    try {
      // WHY A DIRECTORY WAS KEPT when a sibling still needed it. server.mjs has been sending this since last night and
      // updateClusterJob never destructured it, so it was dropped at the parameter boundary with no error anywhere. The
      // fourth instance of this exact shape in one week.
      this.db.exec('ALTER TABLE cluster_jobs ADD COLUMN workdir_kept TEXT');
    } catch {
      // already present
    }
  }

  /** Record a cluster job so it can be followed after the run that submitted it has ended. */
  rememberClusterJob({ jobId, runId, consoleSession, cluster, provider, host, state, schedulerState, resultsInto }) {
    const now = Date.now();
    this.db.prepare(
      `INSERT INTO cluster_jobs (job_id, run_id, console_session, cluster, provider, host, state,
                                 scheduler_state, submitted_ms, updated_ms, results_into)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
       ON CONFLICT(job_id) DO UPDATE SET state = excluded.state,
                                         scheduler_state = excluded.scheduler_state,
                                         updated_ms = excluded.updated_ms`,
    ).run(String(jobId), String(runId || ''), String(consoleSession || ''), String(cluster || ''),
      String(provider || ''), String(host || ''), String(state || 'submitted'),
      String(schedulerState || ''), now, now, String(resultsInto || ''));
  }

  /** Update a job's state, and close it when the scheduler says it is over. */
  updateClusterJob(jobId, { state, schedulerState, files, analysisRun, reason, workdirKept }) {
    const over = state === 'done' || state === 'failed';
    this.db.prepare(
      `UPDATE cluster_jobs SET state = COALESCE(?, state),
                               scheduler_state = COALESCE(?, scheduler_state),
                               files = COALESCE(?, files),
                               analysis_run = COALESCE(?, analysis_run),
                               reason = COALESCE(?, reason),
                               workdir_kept = COALESCE(?, workdir_kept),
                               updated_ms = ?,
                               ended_ms = CASE WHEN ? THEN ? ELSE ended_ms END
       WHERE job_id = ?`,
    ).run(state ?? null, schedulerState ?? null,
      files ? JSON.stringify(files) : null, analysisRun ?? null, reason ?? null, workdirKept ?? null,
      Date.now(), over ? 1 : 0, Date.now(), String(jobId));
  }

  /* Jobs that have not finished. What the watcher asks for on every tick, and after a restart. */
  openClusterJobs() {
    return this.db.prepare(
      `SELECT * FROM cluster_jobs WHERE ended_ms IS NULL ORDER BY submitted_ms`,
    ).all();
  }

  getClusterJob(jobId) {
    return this.db.prepare('SELECT * FROM cluster_jobs WHERE job_id = ?').get(String(jobId)) || null;
  }

  /*
   * A RUN WHOSE PROCESS IS GONE IS NOT RUNNING.
   *
   * MEASURED: an analysis run sat marked `running` with ZERO events for 62 minutes after the process that owned it had
   * exited. `/v1/operational/cancel` refused it as `run_not_active`, correctly -- it was not in the live map -- so there
   * was no way to close it and the restart guard treated it as work in progress and refused to restart. A stale row
   * blocked deployment of everything else.
   *
   * Runs live in this process's memory. When it starts, nothing is running by definition, so any row still marked
   * running belongs to a process that is gone. Closing them at startup is a statement of fact rather than a guess.
   *
   * `interrupted` rather than `error`, because they were not observed to fail: the process ended and took them with it,
   * which is a different thing and worth being able to tell apart afterwards.
   */
  reconcileOrphanedRuns() {
    /*
     * ONLY RUNS WHOSE OWNER IS GONE, PROVEN, not every run that happens to be marked running.
     *
     * MEASURED, and I caused it. This closed EVERY row marked running on the assumption that the only reason one could
     * exist at startup is a previous process having died. I then loaded this module in a throwaway process to check an
     * import, and it marked the operator's live run `max-beb6e19eee` as interrupted while the real engine carried on
     * writing its events. The run survived; its row did not, so the console would have shown a finished run, withdrawn
     * its stop control and stopped following it.
     *
     * A RUN THAT IS STILL WRITING IS NOT ORPHANED. `owner_pid` records which process is driving it, so liveness is a
     * question with an exact answer rather than an assumption about who else might be running. A row whose owner is
     * still alive is left entirely alone, whoever is asking.
     *
     * THE FALLBACK IS THE OLD BEHAVIOUR, deliberately, for rows written before this column existed: with no owner
     * recorded there is nothing to check and an interrupted row is still better than one that says running for ever.
     */
    const mine = process.pid;
    const candidates = this.db.prepare("SELECT id, owner_pid FROM runs WHERE state = 'running'").all();
    const rows = candidates.filter((r) => {
      const pid = Number(r.owner_pid || 0);
      /* No owner recorded: written before this column existed, so behave as this always did. */
      if (!pid) {
        return true;
      }
      /* MY OWN RUN IS NOT ORPHANED. I am the process driving it, and closing it would be this method ending the very
         work it exists to protect. */
      if (pid === mine) {
        return false;
      }
      try {
        /* Signal 0 asks whether the process exists without touching it. */
        process.kill(pid, 0);
        return false;
      } catch {
        return true;
      }
    });
    if (rows.length) {
      /* BY ID, because the filter above decided which rows are genuinely orphaned. A `WHERE state = 'running'` here
         would close every live run regardless of what was chosen, which is the defect this is fixing. */
      const close = this.db.prepare(
        "UPDATE runs SET state = 'interrupted', ended_ms = COALESCE(ended_ms, ?), answer = COALESCE(NULLIF(answer,''), ?) WHERE id = ?",
      );
      for (const r of rows) {
        close.run(Date.now(), 'the engine restarted while this run was in flight, so it did not finish', r.id);
      }
    }
    return rows.map((r) => r.id);
  }

  createRun({ id, task, team, model }) {
    /* WHICH PROCESS IS DRIVING THIS RUN, so orphan reconciliation can ask whether the owner is still alive instead of
       assuming that any row marked running must belong to a process that died. */
    this.db.prepare(
      'INSERT INTO runs (id, task, team, model, state, started_ms, owner_pid) VALUES (?, ?, ?, ?, ?, ?, ?)',
    ).run(id, task, team ? 1 : 0, model, 'running', Date.now(), process.pid);
  }

  /** The session id only becomes known once the loop reports it, so it is set rather than inserted. */
  noteSession(runId, sessionId) {
    this.db.prepare('UPDATE runs SET session_id = ? WHERE id = ?').run(sessionId, runId);
  }

  appendEvent(runId, n, ev) {
    this.db.prepare('INSERT OR REPLACE INTO events (run_id, n, at_ms, kind, body) VALUES (?, ?, ?, ?, ?)')
      .run(runId, n, ev.at ?? Date.now(), ev.kind, JSON.stringify(ev));
  }

  /**
   * Close a run, and record WHY it is closed.
   *
   * `complete` and `error` are not the only truthful states: a run whose process died is neither, and calling it
   * `error` would blame the science for an infrastructure failure. The engine's own runs table had exactly this
   * problem -- a test asserted it held only terminal states and broke the moment a real study was in flight.
   */
  finishRun(runId, { state, turns, cost, answer }) {
    this.db.prepare('UPDATE runs SET state = ?, ended_ms = ?, turns = ?, cost = ?, answer = ? WHERE id = ?')
      .run(state, Date.now(), turns ?? null, cost ?? null, answer ?? null, runId);
  }

  /** Any run left `running` by a process that is gone is orphaned, not live. Called once at startup. */
  reconcileOrphans() {
    const n = this.db.prepare("SELECT COUNT(*) AS c FROM runs WHERE state = 'running'").get().c;
    if (n > 0) {
      this.db.prepare("UPDATE runs SET state = 'interrupted', ended_ms = ? WHERE state = 'running'").run(Date.now());
    }
    return n;
  }

  /** The conversation a run belongs to, which is not the same as the transcript it reads. */
  noteConsoleSession(runId, consoleSession) {
    if (!consoleSession) return;
    this.db.prepare('UPDATE runs SET console_session = ? WHERE id = ?').run(String(consoleSession), runId);
  }

  /** Runs belonging to a conversation, newest last, in the shape the console's run list reads. */
  runsForConsoleSession(consoleSession, limit = 50) {
    return this.db.prepare(
      `SELECT r.id AS run_id, r.state, r.task, r.started_ms, r.ended_ms, r.model,
              (SELECT COUNT(*) FROM events e WHERE e.run_id = r.id) AS events_total
         FROM runs r WHERE r.console_session = ? ORDER BY r.started_ms ASC LIMIT ?`,
    ).all(String(consoleSession), limit);
  }

  getRun(id) {
    return this.db.prepare('SELECT * FROM runs WHERE id = ?').get(id) || null;
  }

  listRuns(limit = 50) {
    return this.db.prepare('SELECT * FROM runs ORDER BY started_ms DESC LIMIT ?').all(limit);
  }

  eventsFor(runId) {
    // `n` TRAVELS WITH THE BODY. It was selected for ordering and then thrown away, so every consumer that wanted to
    // know WHERE in the run an event sat saw `undefined`. That silently flattened the workflow graph: every method
    // recorded step 0, and the phase lookup, which walks forward to the event's position, stopped at the first event.
    return this.db.prepare('SELECT n, body FROM events WHERE run_id = ? ORDER BY n').all(runId)
      .map((r) => ({ ...JSON.parse(r.body), n: r.n }));
  }

  countEvents(runId) {
    return this.db.prepare('SELECT COUNT(*) AS c FROM events WHERE run_id = ?').get(runId).c;
  }
}
