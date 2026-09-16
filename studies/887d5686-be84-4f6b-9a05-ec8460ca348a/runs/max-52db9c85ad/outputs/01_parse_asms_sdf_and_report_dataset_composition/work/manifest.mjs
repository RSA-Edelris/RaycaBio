/**
 * manifest.mjs — a run's state of record, DERIVED and never maintained.
 *
 * WS-30 T4. Nothing on disk answers "what phase is this run in, what did it declare it would produce,
 * and what has it produced so far" in one place. The tape answers it only by replay, and the model's
 * own context does not survive compaction. The reference framework's first principle is a state of
 * record read at the start of every session, and its own words for why: "It survives compaction; your
 * conversation context does not." And: "If it is not on disk, it does not exist."
 *
 * DERIVED, WHICH IS THE WHOLE DESIGN. Every field here is computed from the tape and the artifact
 * index at the moment it is asked for. Nothing is accumulated, nothing is patched in place, and there
 * is no second copy of a fact that could disagree with the first.
 *
 * That choice is not stylistic. `LESSONS.md` in the reference framework opens with the failure mode of
 * the alternative: "Hooks rewrite the state file on every tool use, and parallel sessions may share
 * it. String-replacement edits silently no-op when the file's current shape differs from the assumed
 * one (this bit three times in one session)." A derived manifest cannot be edited into an inconsistent
 * state, because it is not edited at all.
 *
 * IT LIVES BESIDE THE RUN, NOT IN THE WORKSPACE. A file in the researcher's session directory would be
 * registered as one of the run's own artifacts and offered to them as a result, which is exactly the
 * confusion this layer exists to remove.
 *
 * WHERE THE TAPE ACTUALLY IS. Checked rather than assumed: `runstore.store().events_for_run()` on the
 * Python side returned 0 events for a run whose console tape holds 250, because the tape is written by
 * `Store` into MAX_DB and the Python store is a parallel record kept for the file manager. So this is
 * built here, where the tape is, and where the hooks that will read it in T6 already run.
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync, renameSync } from 'node:fs';
import { dirname, join } from 'node:path';

/** Schema version, so a reader can tell what it is looking at when this grows. */
export const MANIFEST_VERSION = 1;

/**
 * The directory manifests are written into, derived from the tape's own database path.
 *
 * Derived rather than configured separately so a test that redirects MAX_DB gets its manifests
 * redirected too. The `artifacts.ROOT` trap in the Python tree is the same shape and cost a suite that
 * silently wrote billing rows into the production database.
 */
export function manifestDir(dbPath) {
  return join(dirname(String(dbPath || '.')), 'manifests');
}

export function manifestPath(dbPath, runId) {
  /*
   * SANITISED, AND THE DOTS MATTER AS MUCH AS THE SLASHES.
   *
   * The first version replaced everything outside `[A-Za-z0-9._-]`, which left `..` intact because a
   * dot is in that set: `../../etc/passwd` became `......etc-passwd`. That could not actually escape,
   * since the slashes were gone, but a filename carrying `..` is one refactor away from being joined
   * differently, and a run id reaches this from a request body. Runs of dots are collapsed and leading
   * dots removed, which also keeps a manifest from becoming a hidden file.
   */
  const safe = String(runId || 'unknown')
    .replace(/[^A-Za-z0-9._-]/g, '-')
    .replace(/\.{2,}/g, '.')
    .replace(/^\.+/, '')
    // TRAILING DOTS TOO: a name ending in a dot meets the '.json' suffix and forms '..' again.
    .replace(/\.+$/, '') || 'unknown';
  return join(manifestDir(dbPath), `${safe}.json`);
}

/** The last event of a kind, or null. The tape is append-only, so the last one is the current truth. */
function lastOf(events, kind) {
  for (let i = events.length - 1; i >= 0; i -= 1) {
    if (events[i] && events[i].kind === kind) return events[i];
  }
  return null;
}

/**
 * The phases a run declared, from the newest plan snapshot.
 *
 * THE PLAN IS A SNAPSHOT, NOT A DIFF. `noteAndPublishTask` emits the WHOLE table whenever any task
 * changes, so the newest `plan` event is the complete current plan and earlier ones are superseded.
 * Reading all of them and merging would invent history the engine never claimed.
 *
 * `produces` is carried through even though the SDK's task signal has no such field and it is
 * therefore empty today: measured on run max-604740ffad, every phase reported `produces: []`. It is
 * here because it is the field a declaration would arrive in, and a manifest that dropped it would
 * hide the gap rather than showing it.
 */
export function phasesFrom(events) {
  const plan = lastOf(events, 'plan');
  const phases = (plan && Array.isArray(plan.phases) ? plan.phases : []).map((p, i) => ({
    id: String(p.id ?? i),
    index: Number.isFinite(Number(p.index)) ? Number(p.index) : i,
    name: String(p.goal || p.name || `phase ${i}`),
    state: String(p.state || 'unknown'),
    declared_produces: Array.isArray(p.produces) ? p.produces.map(String) : [],
    final: p.final === true,
  }));
  return phases;
}

/**
 * Which phase the run is in now.
 *
 * THE ENGINE'S OWN STATE IS BELIEVED. A phase carries `state` from the SDK's task list, which is the
 * only thing that actually knows. So the current phase is the first one not yet done, and when every
 * phase is done there is no current phase rather than a guess at the last one.
 */
export function currentPhase(phases) {
  const open = phases.find((p) => p.state !== 'done' && p.state !== 'completed');
  return open ? { phase_id: open.id, phase_name: open.name, phase_index: open.index } : null;
}

/**
 * What the run produced, from the artifact index rather than from the tape.
 *
 * THE INDEX IS THE AUTHORITY ON FILES and the tape is not, which was measured the hard way: on run
 * max-ff20d03e11 all eleven outputs were in the index under the correct run id and NOT ONE had been
 * announced on the tape, because announcement was wired to a filesystem diff that a second registrar
 * had already consumed. A manifest built from tape events would have reported zero files for a run
 * that produced eleven.
 *
 * `declared` says whether the producer or the plan named this file's role, which is what makes the
 * effect of WS-30 T1 visible in the manifest instead of only in a folder name.
 */
export function producedFrom(records) {
  return (records || []).map((r) => {
    const folder = String(r.folder || '');
    return {
      artifact_id: String(r.id || ''),
      name: String(r.name || ''),
      folder,
      role: folder ? folder.split('/').pop() : '',
      kind: String(r.kind || ''),
      phase: r.phase == null ? '' : String(r.phase),
      phase_index: r.phase_index == null ? null : Number(r.phase_index),
      step_seq: r.step_seq == null ? null : Number(r.step_seq),
      step_title: String(r.step_title || ''),
      bytes: Number.isFinite(Number(r.size)) ? Number(r.size) : null,
      sha256: String(r.sha256 || ''),
      /* WHERE THE FILE STILL IS ON DISK. `folder` is a LABEL, not a location -- `filing.py` says so in as
         many words, because artifacts are stored under an opaque hashed name. So a caller that wants to READ
         a document needs this, and T9's `verified` check does. */
      source_path: String(r.source_path || ''),
      declared: Boolean(r.role),
      version: r.version == null ? null : Number(r.version),
    };
  });
}

/**
 * The documents this run wrote, which are the produced files filed as reports.
 *
 * DERIVED FROM THE ROLE, not from a separate list. A report is a produced file like any other and
 * keeping a second register of them is how two records of one fact start to disagree. `verified` is
 * false for every entry until T7 gives a document a Verification section to check, and saying so is
 * better than omitting the field and leaving a reader to wonder.
 */
export function documentsFrom(produced, readDoc) {
  return produced
    .filter((f) => f.role === 'reports')
    .map((f) => {
      const path = f.folder ? `${f.folder}/${f.name}` : f.name;
      /*
       * `verified` IS READ, NOT ASSUMED. WS-30 T9.
       *
       * A document clears `verify_step` when its `## Verification` section has a non-empty body, which is
       * the reference framework's own rule: `state_guard.ts` does `body.split("## Verification")[1]` and
       * checks it is not blank. Until T9 no document had such a section, so this field was hard-coded false
       * and said so.
       *
       * `readDoc` is injected rather than imported, because reading an artifact means resolving its stored
       * name under a hashed path and that is the caller's business. A caller with no reader gets `false`,
       * which is honest: unread is not verified.
       */
      let text = '';
      if (typeof readDoc === 'function') {
        try {
          text = String(readDoc(f) || '');
        } catch {
          // A READER THAT THROWS MUST NOT TAKE DOWN THE MANIFEST. `readDoc` is injected, so it is not this
          // module's to trust, and a missing or unreadable document is exactly the case where the answer
          // matters: unread stays unverified, and the run keeps its state of record.
          text = '';
        }
      }
      const after = text.split('## Verification')[1] || '';
      const verificationBody = after.split(/\n## /)[0].trim();
      return {
        path,
        name: f.name,
        phase: f.phase,
        artifact_id: f.artifact_id,
        verified: verificationBody.length > 0,
        /* The exact label the reference matches on, so a container that ran is provably described. */
        names_container: /Container Image:/i.test(text),
      };
    });
}

/** Cluster and container work, from the job events the tape already carries. */
export function jobsFrom(events) {
  const byKey = new Map();
  for (const ev of events) {
    if (!ev || ev.kind !== 'job.submitted') continue;
    const key = String(ev.job_id || ev.tool || '');
    if (!key) continue;
    const prior = byKey.get(key) || {};
    byKey.set(key, {
      key,
      tool: String(ev.tool || prior.tool || ''),
      job_id: String(ev.job_id || prior.job_id || ''),
      host: String(ev.host || prior.host || ''),
      cluster: String(ev.cluster || prior.cluster || ''),
      // ABSENT UNTIL REPORTED. A job in flight has no exit code, and a zero would read as success.
      rc: ev.rc == null ? (prior.rc == null ? null : prior.rc) : Number(ev.rc),
      state: String(ev.state || prior.state || 'running'),
    });
  }
  return [...byKey.values()];
}

/** Obligations that gate a step's close. T8 turns these into a soft block at Stop; today they are advisory. */
export const PIPELINE_KINDS = Object.freeze(['document_step', 'verify_step', 'commit_step']);

/**
 * What this run still owes, DERIVED rather than accumulated.
 *
 * WS-30 T7. THIS IS THE ONE PLACE WHERE THIS DESIGN DEPARTS FROM THE REFERENCE FRAMEWORK, deliberately
 * and for the reason its own field notes give. There, `pending_obligations` is a mutable list in
 * `.project-state.yaml` that hooks add to and remove from on every tool call. `LESSONS.md` opens with
 * what that cost: "String-replacement edits silently no-op when the file's current shape differs from the
 * assumed one (pending_obligations: [] inline vs block-list forms flip constantly -- this bit three
 * times in one session)", followed by the discipline of grep-verifying after every write.
 *
 * A DERIVED OBLIGATION HAS NO CLEARING STEP, so none of that can happen. It stops being computed the
 * moment its condition is no longer true. It cannot be stale, cannot be double-added, cannot be lost by
 * a write that raced another session, and cannot disagree with the run it describes.
 *
 * WHAT IS NOT HERE YET, and why, because a list that quietly omits things is worse than a short one:
 *   verify_step   needs a document's `## Verification` section to read, and documents do not have one
 *                 until T9 writes them in that shape. Deriving it now would fire on every document in
 *                 every run and teach the reader to ignore the whole mechanism.
 *   container_doc the reference checks a document for `Container Image:`. Same dependency as above, and
 *                 MEASURED: the 50 `job.submitted` events on run max-604740ffad carry agent, at, gpu,
 *                 host, image, kind and tool, and no container name, so there is nothing to match yet.
 *   commit_step   belongs to T11, where the step push gets a call site and a step id to match on.
 */
export function obligationsFrom(manifest, events) {
  const out = [];
  const evs = Array.isArray(events) ? events : [];
  const at = (manifest && manifest.generated_at) || new Date().toISOString();
  const produced = (manifest && manifest.produced) || [];
  const documents = (manifest && manifest.documents) || [];
  const phases = (manifest && manifest.phases) || [];

  /* A file worth keeping was produced and nothing describes it.
     `work/` is excluded because working material is not a result: logs, intermediates and scratch are
     the majority of what a run writes and demanding a document for each would be the cage this
     workstream exists to avoid. Keyed on the PHASE, which is why the phase had to reach the record
     first: a run-wide obligation would clear as soon as any one phase was written up. */
  const documentedPhases = new Set(documents.map((d) => String(d.phase || '')));
  const owed = new Map();
  for (const f of produced) {
    if (!f.role || f.role === 'work' || f.role === 'reports') continue;
    const phase = String(f.phase || '');
    if (documentedPhases.has(phase)) continue;
    const seen = owed.get(phase) || [];
    if (seen.length < 4) seen.push(f.name);
    owed.set(phase, seen);
  }
  for (const [phase, names] of owed) {
    out.push({
      kind: 'document_step',
      created_at: at,
      phase,
      context: `${phase ? `phase ${phase}` : 'this run'} produced ${names.join(', ')} and has no document`,
    });
  }

  /* A phase finished and nobody looked at it independently.
     Recognised by an `audit` in the document's name, which is the reference framework's own rule
     (`rel.toLowerCase().includes("audit")` in state_guard.ts). Advisory: an audit that blocks a run is a
     cage, and the audit itself is T10. */
  const auditedPhases = new Set(
    documents.filter((d) => /audit/i.test(String(d.name || ''))).map((d) => String(d.phase || '')),
  );
  for (const p of phases) {
    if (p.state !== 'done' && p.state !== 'completed') continue;
    if (auditedPhases.has(String(p.name || '')) || auditedPhases.has(String(p.id || ''))) continue;
    out.push({
      kind: 'phase_audit',
      created_at: at,
      phase: String(p.name || p.id || ''),
      context: `phase ${p.name || p.id} finished and has no audit`,
    });
  }

  /* A document exists and says nothing checkable.
     WS-30 T9 made the section real, so this can be derived at last. The rule is the reference's own: a
     non-empty body under `## Verification`. A document that cannot be READ counts as unverified rather
     than as verified, because unread is not checked. */
  for (const d of documents) {
    if (d.verified) continue;
    out.push({
      kind: 'verify_step',
      created_at: at,
      phase: String(d.phase || ''),
      context: `${d.name} has no Verification section with anything in it`,
    });
  }

  /* A container ran and no document names its image.
     The reference clears this on a document containing `Container Image:`, and the renderer now writes
     exactly that label when a phase ran one. Advisory: an undescribed container is a gap in the record,
     not a reason to hold a turn open. */
  const containerJobs = (manifest && manifest.jobs) || [];
  if (containerJobs.length && documents.length && !documents.some((d) => d.names_container)) {
    out.push({
      kind: 'container_doc',
      created_at: at,
      phase: '',
      context: `${containerJobs.length} container job(s) ran and no document names the image that produced them`,
    });
  }

  /* A phase closed and its work was never pushed.
     WS-30 T11. THE ONLY OBLIGATION WHOSE EXISTENCE DEPENDS ON THE SESSION, and it is derived from evidence
     rather than from a lookup: `autoPushToGitHub` returns silently on `no_repo` and `no_credential`, so a
     session with nothing bound emits NO `publish` event, ever. The presence of at least one is therefore
     proof that a repository is bound, and its absence means this obligation is never created at all.

     That matters more than it looks. An obligation that can never be satisfied is precisely the cage the
     strictness split exists to prevent, and `commit_step` is a PIPELINE kind: it would hold turns open in
     every session that never connected a repository. */
  /*
   * A PUSH THAT SUCCEEDED. `ok === false` was not checked, and that turned a broken feature into a wrong instruction.
   *
   * WHAT HAPPENED ON RUN max-d6e2f8f2a9, and every link is mine. The phase-close push threw a ReferenceError, was caught,
   * and emitted `{ok: false, error: "hook_failed"}`. This filter counted it as evidence that a repository was bound. The
   * obligation then told the model that a phase "was not pushed to the bound repository" -- of a session that had none --
   * so the model went looking, picked `RaycaBio/binding-affinity-demo` as a "closest fit", and pushed fourteen files from
   * a throwaway test run into a real repository.
   *
   * A FAILED PUSH PROVES NOTHING ABOUT BINDING. It may have failed precisely because nothing was bound.
   */
  const pushes = evs.filter((ev) => ev && ev.kind === 'publish' && ev.ok !== false);
  if (pushes.length) {
    const pushedSteps = new Set(pushes.map((ev) => String(ev.step || '')).filter(Boolean));
    /* The repository the successful pushes actually went to, so the obligation can name it instead of implying one. */
    const repo = pushes.map((ev) => String(ev.repo || ev.repository || '')).find(Boolean) || '';
    for (const p of phases) {
      if (p.state !== 'done' && p.state !== 'completed') continue;
      if (pushedSteps.has(String(p.id))) continue;
      out.push({
        kind: 'commit_step',
        created_at: at,
        phase: String(p.name || p.id || ''),
        /*
         * NAMES THE REPOSITORY IT MEANS, and asks for nothing when it cannot.
         *
         * The old wording, "was not pushed to the bound repository", described a repository the session did not
         * necessarily have, and a model asked to satisfy that will find one. An instruction that cannot be followed
         * literally gets followed liberally, which is how fourteen files reached a repository nobody chose.
         */
        context: repo
          ? `phase ${p.name || p.id} closed and was not pushed to ${repo}`
          : `phase ${p.name || p.id} closed and its push did not complete`,
      });
    }
  }

  /* The context was compacted and nothing has been written since.
     Derived from the tape's own ordering rather than from a flag: the last `compact` event against the
     last file the run produced. If work has happened since the compaction, the run evidently found its
     feet again and there is nothing to ask for. */
  let lastCompact = -1;
  let lastFile = -1;
  evs.forEach((ev, i) => {
    if (!ev) return;
    if (ev.kind === 'compact') lastCompact = i;
    if (ev.kind === 'file.observed') lastFile = i;
  });
  if (lastCompact >= 0 && lastCompact > lastFile) {
    out.push({
      kind: 'recovery_audit',
      created_at: at,
      phase: '',
      context: 'the context was compacted and nothing has been produced since; re-read the manifest and the last documents',
    });
  }

  return out;
}

/**
 * The whole manifest for one run.
 *
 * `files` is passed in rather than fetched, because reading the artifact index means crossing the
 * Python bridge and this function must stay synchronous and testable without one. The caller that has
 * a bridge supplies the records; a caller that does not gets a manifest with an empty `produced` and a
 * `sources.index` of false, which says plainly that the file half is missing rather than implying the
 * run made nothing.
 */
export function buildManifest({ runId, run, events, files, at, readDoc }) {
  const evs = Array.isArray(events) ? events : [];
  const phases = phasesFrom(evs);
  const produced = producedFrom(files);
  const manifest = {
    version: MANIFEST_VERSION,
    run_id: String(runId || (run && run.id) || ''),
    session_key: String((run && (run.console_session || run.session_key)) || ''),
    task: String((run && run.task) || ''),
    state: String((run && run.state) || ''),
    started_at: (run && run.started_at) || null,
    ended_at: (run && run.ended_at) || null,
    generated_at: at || new Date().toISOString(),
    /* WHAT THIS MANIFEST WAS BUILT FROM, so a reader can tell a run that produced nothing from a
       manifest that could not see what it produced. The distinction was invisible for a whole day
       when announcement was broken, and it is the difference between a defect and a quiet run. */
    sources: { tape: evs.length, index: Array.isArray(files) },
    current: currentPhase(phases),
    phases,
    produced,
    documents: documentsFrom(produced, readDoc),
    jobs: jobsFrom(evs),
    obligations: [],
    /* STILL EMPTY, and T6 fills it: anything a run would hate to recompute belongs here. */
    critical_values: {},
  };
  /* DERIVED LAST, because an obligation is a statement ABOUT the manifest and needs the finished shape.
     Computing it inside the literal above would mean reading half-built fields. */
  manifest.obligations = obligationsFrom(manifest, evs);
  return manifest;
}

/**
 * Write a manifest, atomically.
 *
 * TEMP AND RENAME, because a reader can arrive at any moment: a hook fires while a turn is ending, and
 * a half-written state of record is worse than a stale one. The reference framework's cursor files use
 * the same shape for the same reason.
 */
export function writeManifest(dbPath, manifest) {
  const path = manifestPath(dbPath, manifest && manifest.run_id);
  mkdirSync(dirname(path), { recursive: true });
  const tmp = `${path}.tmp`;
  writeFileSync(tmp, `${JSON.stringify(manifest, null, 2)}\n`);
  renameSync(tmp, path);
  return path;
}

/** Read a manifest back, or null when there is none. Never throws: an absent manifest is not an error. */
export function readManifest(dbPath, runId) {
  const path = manifestPath(dbPath, runId);
  if (!existsSync(path)) return null;
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

/**
 * The manifest as the few lines a model should be handed after a compaction.
 *
 * SHORT ON PURPOSE. The reference framework's `snapshot()` is seven lines, and the reason is that this
 * text is injected into a context that has just been compacted to save room. A full manifest would
 * undo the compaction it is helping the run survive.
 */
export function snapshotOf(manifest) {
  if (!manifest) return '';
  const m = manifest;
  const cur = m.current;
  const roles = {};
  for (const f of m.produced || []) roles[f.role || 'unfiled'] = (roles[f.role || 'unfiled'] || 0) + 1;
  const byRole = Object.entries(roles).sort((a, b) => b[1] - a[1])
    .map(([r, n]) => `${r} ${n}`).join(', ');
  const lines = [
    `Run: ${m.run_id} (${m.state || 'state unknown'})`,
    `Task: ${String(m.task || '').slice(0, 160)}`,
    cur ? `Phase: ${cur.phase_name} (id ${cur.phase_id})` : `Phase: none open, ${m.phases.length} recorded`,
    `Files produced: ${(m.produced || []).length}${byRole ? ` (${byRole})` : ''}`,
  ];
  const declared = (m.produced || []).filter((f) => f.declared).length;
  if (declared) lines.push(`Of those, ${declared} filed by declaration rather than by guess.`);
  if ((m.documents || []).length) lines.push(`Documents: ${m.documents.map((d) => d.name).join(', ')}`);
  if ((m.jobs || []).length) {
    const open = m.jobs.filter((j) => j.rc == null).length;
    lines.push(`Jobs: ${m.jobs.length}${open ? `, ${open} with no result yet` : ''}`);
  }
  if ((m.obligations || []).length) {
    lines.push(`Open obligations: ${m.obligations.map((o) => o.kind).join(', ')}`);
  }
  const cv = Object.keys(m.critical_values || {});
  if (cv.length) lines.push(`Critical values: ${cv.join(', ')}`);
  return lines.join('\n');
}

/**
 * What a run should be told about itself when its own memory has just been taken away.
 *
 * WS-30 T6. THE OPERATOR asked for exactly this: "how to use the hook system to make sure after
 * compaction the agents read the docs for example is super importnat."
 *
 * PURE, AND EXPORTED FOR THAT REASON. Composed here rather than inside the hook so the cases can be
 * driven directly: a run with documents, one without, one with jobs still open. A hook body is only
 * reachable through a live SDK session, and text nobody can test is text nobody can trust.
 *
 * THE DOCUMENTS ARE NAMED, NOT SUMMARISED. The reference framework's recovery skill reads the last three
 * documents deliberately, because a compact summary "can't carry" the reasoning and the parameter values
 * and the documents can. Naming them with their paths makes re-reading one Read away. Three because that
 * is its number and for its reason: the recent ones are the ones that matter, and a longer list injected
 * into a just-compacted context defeats the compaction it is helping the run survive.
 */
export function rehydrationFrom(manifest, why) {
  if (!manifest) return '';
  const parts = [snapshotOf(manifest)];

  const docs = (manifest.documents || []).slice(-3);
  if (docs.length) {
    parts.push(`Read these before continuing, they carry the reasoning this summary cannot:\n${
      docs.map((d) => `  ${d.path}`).join('\n')}`);
  }

  /* A JOB WITH NO RESULT is the thing most likely to be forgotten and the most expensive to redo, so it
     is stated on its own rather than buried in a count. MEASURED on run max-604740ffad: five jobs on a
     COMPLETE run had no exit code, because `job.submitted` carries none. */
  const openJobs = (manifest.jobs || []).filter((j) => j.rc == null);
  if (openJobs.length) {
    parts.push(`Jobs with no result recorded: ${openJobs.map((j) => j.tool || j.job_id).filter(Boolean).join(', ')}. `
      + 'Check these before dispatching them again.');
  }

  parts.push("The manifest above is derived from this run's own tape and artifact index, so it is current. "
    + 'Your conversation context is not.');
  return `${String(why || '').trim()}\n\n${parts.join('\n\n')}`.trim();
}

/** How many times one run may be soft-blocked at Stop before the mechanism gets out of the way. */
export const MAX_STOP_BLOCKS = 2;

/**
 * How many times a run may be ADVISED at the end of a turn. One.
 *
 * THIS CAP WAS MISSING AND IT COST A REAL RUN ELEVEN MINUTES. On run max-70e85d02e6 the block cap worked exactly as
 * designed -- one block, then it stood aside -- and then the ADVISORY fired on every stop attempt that followed, 27 of
 * them. An advisory is delivered as `additionalContext`, and context on Stop re-prompts the model, so each advisory
 * produced another turn, another "Ready.", another stop attempt and another advisory. The run only ended when the model
 * gave up. It also sent the model hunting for what was holding it open, and it read an unrelated third-party plugin file
 * whose text named another product, which then surfaced in the operator's event stream.
 *
 * SO "ADVISORY" WAS NOT THE SAME AS "HARMLESS". Anything returned from this hook pushes the model, whether or not it
 * carries a block, and the only safe number of times to push without a cap is zero.
 *
 * ONE, NOT TWO, because unlike a block an advisory asks for nothing and repeating it adds nothing. The audit brief it
 * carries is just as complete the first time.
 */
export const MAX_STOP_ADVISORIES = 1;

/**
 * Whether a turn should be held open, and what to say.
 *
 * WS-30 T8. This is the "teeth" half of the reference framework's discipline, and the whole design of it
 * is about not becoming a cage.
 *
 * WHY A SOFT BLOCK AND NEVER A HARD ONE. `.claude/hooks/README.md` in the reference is explicit: exit 2
 * is a hard block and is "avoided here", while exit 0 with `{"decision":"block","reason":...}` "prevents
 * stop, continues working" and feeds the reason back so the model can close the step. We have our own
 * evidence for that choice. On 2026-08-29 a hard refusal was added to the dispatch path and removed the
 * same hour: it refused any dispatch longer than the enclosing cell could give, and three real gnina
 * dispatches in run max-802e89068c were refused with `requested=1800 available=872.8`. The operator:
 * "this was not happening yesterday! so this means you added a cage?"
 *
 * THREE INDEPENDENT ESCAPES, because one is not enough for something that can hold a turn open.
 *
 *   1. `stop_hook_active`, which the SDK sets when a Stop hook has already blocked and the model is
 *      continuing because of it (sdk.d.ts:7883). Blocking again on the same chain is how a loop starts,
 *      so this never does.
 *   2. A per-run cap. Even across separate chains, a run that has been asked twice is not asked again.
 *      A model that genuinely cannot write a document must be able to finish.
 *   3. Only PIPELINE obligations block at all. An audit or a recovery read is advisory for ever, because
 *      an audit that blocks a run is the cage in a different coat.
 *
 * AND BACKGROUND WORK IS NOT AN IDLE TURN. `background_tasks` distinguishes "the session is done" from
 * "the session is waiting", and holding a turn open while a container is still running would ask the
 * model to document work that has not finished.
 */
/**
 * WHY a turn should not end yet, before any budget is applied. Not exported: `stopDecision` is the answer.
 */
function stopReason({ manifest, stopHookActive, blocksSoFar, backgroundTasks }) {
  const obligations = (manifest && manifest.obligations) || [];
  if (!obligations.length) return { action: 'none' };

  const pipeline = obligations.filter((o) => PIPELINE_KINDS.includes(o.kind));
  const advisory = obligations.filter((o) => !PIPELINE_KINDS.includes(o.kind));

  const say = (list) => list.map((o) => o.context || o.kind).join('; ');

  /* Escape 3 first, because it is the cheapest and the most common: a run that owes only an audit is
     never held open. */
  if (!pipeline.length) {
    /* AND AN OPEN AUDIT ARRIVES WITH ITS BRIEF, WS-30 T10. An advisory that names a duty without saying
       how to discharge it is a nag. The engine cannot run the audit -- subagents are spawned by the model
       -- so the least it can do is hand over something precise enough to act on. */
    const audit = advisory.find((o) => o.kind === 'phase_audit');
    const brief = audit ? auditBrief(manifest, audit.phase) : '';
    return {
      action: 'advise',
      text: `Still open, not blocking: ${say(advisory)}.${brief ? `\n\n${brief}` : ''}`,
    };
  }

  if (Array.isArray(backgroundTasks) && backgroundTasks.length) {
    return {
      action: 'advise',
      text: `${backgroundTasks.length} background task(s) still running, so this turn is not held open. `
        + `Still owed once they finish: ${say(pipeline)}.`,
    };
  }

  if (stopHookActive) {
    /* Escape 1. Said once more as advice so the reason does not vanish, then out of the way. */
    return {
      action: 'advise',
      text: `Still owed: ${say(pipeline)}. Not blocking again this turn.`,
    };
  }

  if (Number(blocksSoFar || 0) >= MAX_STOP_BLOCKS) {
    /* Escape 2, and it says so plainly rather than going quiet, because a mechanism that stops mattering
       without explanation is worse than one that never existed. */
    return {
      action: 'advise',
      text: `Still owed: ${say(pipeline)}. This run has been asked ${MAX_STOP_BLOCKS} times, so it will `
        + 'not be held open again. Record what is missing or say why it cannot be recorded.',
    };
  }

  const parts = [
    `Before ending: ${say(pipeline)}.`,
    'Write the phase up before closing it. A result nobody described is a result nobody can check, cite '
      + 'or reuse.',
  ];
  if (advisory.length) parts.push(`Also open, but not blocking: ${say(advisory)}.`);
  return { action: 'block', text: parts.join(' ') };
}

/**
 * What the Stop hook should do, budget included.
 *
 * ONE CHOKE POINT, AND THE FIRST VERSION OF THIS CAP DID NOT HAVE ONE. I put the advisory budget inside a single branch
 * of `stopReason`, and there are FOUR other paths that return `advise`: background tasks outstanding, `stop_hook_active`
 * already set, the block budget spent, and no pipeline obligation left. Capping one of five is not capping.
 *
 * WORSE, the counter was not even reaching the function. The edit that passed `advisoriesSoFar` from the hook was lost
 * when a later assertion in the same script aborted the write, so the parameter kept its default of 0 and the cap could
 * never fire. MEASURED on run max-1614a1d494, after I had already reported the loop as fixed: 29 advisories on one run.
 * That is the second time this mechanism has looped, so the budget now sits where no branch can miss it.
 *
 * ASKED OF THE ANSWER, NOT OF THE REASON, which is what makes it hold for a branch added later: whatever `stopReason`
 * decides, an advisory past its budget becomes silence. Returning nothing is the only shape that cannot re-prompt.
 */
export function stopDecision(input) {
  const decision = stopReason(input || {});
  if (decision.action !== 'advise') {
    return decision;
  }
  if (Number((input && input.advisoriesSoFar) || 0) >= MAX_STOP_ADVISORIES) {
    return { action: 'none', text: '' };
  }
  return decision;
}

/**
 * The brief for a phase audit, handed to the model to run with an independent subagent.
 *
 * WS-30 T10. WHY A BRIEF AND NOT AN AUDIT. The engine cannot run this itself: subagents are spawned by the
 * MODEL through its Task tool, and `agentDefinitionsFor` only supplies the definitions it may use. The
 * reference framework has the same constraint and answers it the same way, and says so in
 * `.claude/hooks/README.md`: "hooks cannot run /branch themselves, so hand the user the exact command".
 * A hook that cannot act can still hand over something precise enough to act on.
 *
 * TOLD WHAT TO CHECK, NEVER WHAT TO EXPECT. This is the whole value of the reference's audit skill, whose
 * own brief ends "and tell it nothing about what answer to expect". Its reasoning is worth restating
 * because it is not obvious: per-step verification shares the author's assumptions, so it cannot catch a
 * self-consistent bug where the writer and the reader carry the same mistake and agree with each other.
 * `LESSONS.md` records the cost of learning that twice over: "Every CRITICAL across two audit rounds was
 * invisible to the per-step verification written alongside the code."
 *
 * THE FAILURE PATTERNS ARE NAMED because they are the ones this platform actually produces, and naming
 * them is not the same as naming an answer: index and numbering errors, similar identifiers, an API
 * signature from a different version than the one installed, a bare except that turns a failure into a
 * default, a rule derived from a single data point, and reversed positional arguments.
 */
export function auditBrief(manifest, phaseName) {
  if (!manifest) return '';
  const phase = String(phaseName || '');
  const files = (manifest.produced || []).filter(
    (f) => !phase || String(f.phase || '') === phase,
  );
  const docs = (manifest.documents || []).filter(
    (d) => !phase || String(d.phase || '') === phase,
  );
  const results = files.filter((f) => f.role && f.role !== 'work' && f.role !== 'source');
  const scripts = files.filter((f) => f.role === 'source');

  const lines = [
    `Audit the phase "${phase || manifest.run_id}" with a subagent, and give it this brief verbatim.`,
    '',
    'Use a SEPARATE subagent rather than checking it yourself. Per-step verification shares the '
      + 'assumptions of whoever wrote the step, so it cannot see a mistake that the writer and the reader '
      + 'both make and therefore agree about.',
    '',
    'Tell the subagent WHAT TO CHECK and nothing about what you expect it to find:',
  ];
  if (docs.length) {
    lines.push(`  - Read ${docs.map((d) => d.path).join(', ')}. For each claim in the Final working `
      + 'solution and Verification sections, open the file it refers to and confirm the claim against '
      + 'what is actually there.');
  } else {
    lines.push('  - No document exists for this phase, so there is nothing to check a claim against. '
      + 'Report that as the finding.');
  }
  if (results.length) {
    lines.push(`  - Re-open ${results.slice(0, 8).map((f) => f.name).join(', ')} and inspect two or three `
      + 'real values in each. Confirm they are consistent with what the report says about them.');
  }
  if (scripts.length) {
    lines.push(`  - Read ${scripts.slice(0, 6).map((f) => f.name).join(', ')} and ask what the riskiest `
      + 'assumption in it is. If exactly one thing in this phase were wrong, what would it be?');
  }
  lines.push('  - Check for: index and numbering errors including 0-based against 1-based; similar '
    + 'identifiers confused for one another; a function signature taken from a different version than the '
    + 'one installed, which you should confirm with the installed package rather than from memory; a bare '
    + 'except or a default value that turns a failure into a silent success; a rule derived from a single '
    + 'data point; and reversed positional arguments.');
  lines.push('');
  lines.push('Have it report findings as CRITICAL (invalidates results), MAJOR (may affect accuracy) or '
    + 'VERIFIED CORRECT with the evidence. The verified list is not optional: knowing what was checked and '
    + 'held up is worth as much as knowing what broke.');
  lines.push('');
  lines.push('Write the result to a file whose name contains "audit", which is what records that this '
    + 'phase was reviewed. This is advisory: it does not block the run.');
  return lines.join('\n');
}
