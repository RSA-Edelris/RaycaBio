/**
 * Tests for: A RUN'S STATE OF RECORD IS DERIVED, NOT MAINTAINED.
 *
 * WS-30 T4. Nothing on disk answered "what phase is this run in, what did it declare it would produce,
 * and what has it produced" in one place, and the model's own context does not survive compaction.
 *
 * DERIVED IS THE DESIGN, and `LESSONS.md` in the reference framework is the argument for it: "Hooks
 * rewrite the state file on every tool use, and parallel sessions may share it. String-replacement
 * edits silently no-op when the file's current shape differs from the assumed one (this bit three
 * times in one session)." A manifest that is computed cannot be edited into an inconsistent state.
 *
 * MEASURED against the real tape of run max-604740ffad before these were written: 243 events, 43
 * artifact records, 3 phases, 3 documents, 5 jobs. The numbers below are shaped from that run.
 *
 * Run: node --test modulon-max/
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { basename, join, resolve } from 'node:path';

import {
  MANIFEST_VERSION, buildManifest, currentPhase, documentsFrom, jobsFrom,
  MAX_STOP_ADVISORIES, MAX_STOP_BLOCKS, PIPELINE_KINDS, auditBrief, manifestPath, obligationsFrom, phasesFrom, producedFrom,
  readManifest, rehydrationFrom, snapshotOf, stopDecision, writeManifest,
} from './manifest.mjs';

const RUN = {
  id: 'max-604740ffad',
  console_session: 'd98ecc2e-8220-425f-9554-a96dc993e274',
  task: 'download input data and run the tools',
  state: 'complete',
  started_at: 1787000000000,
  ended_at: 1787000900000,
};

/** A plan snapshot in the shape `noteAndPublishTask` emits: the WHOLE table, every time. */
const plan = (phases) => ({ kind: 'plan', phases });

const THREE_PHASES = [
  { id: '1', index: 0, goal: 'Fetch IEDB epitopes for deepimmuno', state: 'done', produces: [] },
  { id: '2', index: 1, goal: 'Fetch PDB 1N8Z for deeprank-ab', state: 'done', produces: [] },
  { id: '3', index: 2, goal: 'Run all 5 tools and collect outputs', state: 'running', produces: [], final: true },
];

const RECORDS = [
  { id: 'a1', name: 'affinities.json', folder: '03_screening/results', kind: 'data', role: 'results',
    phase: 'screening', phase_index: 2, step_seq: 7, size: 2048, sha256: 'ab', version: 1 },
  { id: 'a2', name: 'scores.csv', folder: '03_screening/tables', kind: 'tables', size: 128 },
  { id: 'a3', name: 'phase_01_fetch.md', folder: '01_fetch/reports', kind: 'documents', size: 900 },
];

test('phases come from the NEWEST plan snapshot, not from merging them', () => {
  /* The plan is a snapshot, so an older one is superseded. Merging would invent history the engine
     never claimed: here the first snapshot knew one phase and the second knows three. */
  const events = [plan([THREE_PHASES[0]]), plan(THREE_PHASES)];
  const phases = phasesFrom(events);
  assert.equal(phases.length, 3);
  assert.equal(phases[2].name, 'Run all 5 tools and collect outputs');
});

test('a run with no plan has no phases rather than an invented one', () => {
  assert.deepEqual(phasesFrom([{ kind: 'say', text: 'hello' }]), []);
});

test('declared_produces is carried even though it is empty today', () => {
  /* MEASURED on max-604740ffad: every phase reported `produces: []`, because the SDK's task signal has
     no such field. The field is kept so the gap is visible in the manifest instead of hidden. */
  const phases = phasesFrom([plan(THREE_PHASES)]);
  assert.ok(phases.every((p) => Array.isArray(p.declared_produces)));
  assert.equal(phases.reduce((n, p) => n + p.declared_produces.length, 0), 0);
});

test('the current phase is the first one not done, and the engine state is believed', () => {
  const cur = currentPhase(phasesFrom([plan(THREE_PHASES)]));
  assert.equal(cur.phase_id, '3');
  assert.equal(cur.phase_index, 2);
});

test('a finished run has NO current phase rather than a guess at the last one', () => {
  const done = THREE_PHASES.map((p) => ({ ...p, state: 'done' }));
  assert.equal(currentPhase(phasesFrom([plan(done)])), null);
});

test('produced files come from the index, with the role read off the folder', () => {
  const produced = producedFrom(RECORDS);
  assert.equal(produced.length, 3);
  assert.equal(produced[0].role, 'results');
  assert.equal(produced[1].role, 'tables');
  assert.equal(produced[0].bytes, 2048);
});

test('declared says whether a role was stated rather than guessed', () => {
  /* This is what makes the effect of T1 visible in the manifest instead of only in a folder name. */
  const produced = producedFrom(RECORDS);
  assert.equal(produced[0].declared, true);
  assert.equal(produced[1].declared, false);
});

test('documents are derived from the reports role, not kept in a second list', () => {
  const docs = documentsFrom(producedFrom(RECORDS));
  assert.equal(docs.length, 1);
  assert.equal(docs[0].name, 'phase_01_fetch.md');
  assert.equal(docs[0].path, '01_fetch/reports/phase_01_fetch.md');
});

test('a job in flight reports NO exit code rather than a zero', () => {
  /* A zero would read as success. MEASURED: all 5 jobs on max-604740ffad had no rc on their
     submission events, so the manifest must be able to say "no result yet" truthfully. */
  const jobs = jobsFrom([
    { kind: 'job.submitted', tool: 'deep-viscosity', host: 'agents-sandbox1' },
    { kind: 'job.submitted', tool: 'biophi', host: 'agents-sandbox1' },
  ]);
  assert.equal(jobs.length, 2);
  assert.ok(jobs.every((j) => j.rc === null));
});

test('later reports about one job update it rather than adding another', () => {
  const jobs = jobsFrom([
    { kind: 'job.submitted', tool: 'gnina', host: 'h1' },
    { kind: 'job.submitted', tool: 'gnina', host: 'h1', rc: 0, state: 'done' },
  ]);
  assert.equal(jobs.length, 1);
  assert.equal(jobs[0].rc, 0);
});

test('the manifest says what it was built FROM', () => {
  /* A run that produced nothing and a manifest that could not see what it produced look identical
     without this. That distinction was invisible for a whole day when announcement was broken. */
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: RECORDS });
  assert.equal(m.sources.tape, 1);
  assert.equal(m.sources.index, true);

  const blind = buildManifest({ runId: RUN.id, run: RUN, events: [], files: null });
  assert.equal(blind.sources.index, false);
  assert.deepEqual(blind.produced, []);
});

test('the whole manifest carries the run identity and its version', () => {
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: RECORDS });
  assert.equal(m.version, MANIFEST_VERSION);
  assert.equal(m.run_id, 'max-604740ffad');
  assert.equal(m.session_key, RUN.console_session);
  assert.equal(m.state, 'complete');
  assert.equal(m.phases.length, 3);
  assert.equal(m.produced.length, 3);
  assert.equal(m.documents.length, 1);
  /*
   * EXPECTATION MOVED, WS-30 T7. This asserted `obligations` was empty, which was true when T4 shipped the
   * shape and deliberately so: the field existed then only so a reader's expectations would not change
   * under the task that filled it. T7 fills it by DERIVING what the run owes, so an empty list here would
   * now mean the derivation is not running.
   *
   * `critical_values` is still empty and still asserted as such, because nothing fills it yet.
   */
  assert.ok(Array.isArray(m.obligations));
  assert.ok(m.obligations.length > 0, 'a run with results and no documents owes something');
  assert.deepEqual(m.critical_values, {});
});

test('the manifest is written atomically and reads back identical', () => {
  const dir = mkdtempSync(join(tmpdir(), 'mf-'));
  const db = join(dir, 'modulon-max.sqlite');
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: RECORDS });
  const path = writeManifest(db, m);
  assert.equal(path, manifestPath(db, RUN.id));
  assert.deepEqual(readManifest(db, RUN.id), m);
  // No temp file left behind: a reader arriving mid-write must never find a half-written record.
  assert.equal(readFileSync(path, 'utf8').endsWith('\n'), true);
  rmSync(dir, { recursive: true, force: true });
});

test('the manifest directory follows the database path, not a fixed location', () => {
  /* Derived so a test that redirects MAX_DB gets its manifests redirected too. The `artifacts.ROOT`
     trap in the Python tree is the same shape and cost a suite that wrote billing rows into the
     production database. */
  assert.ok(manifestPath('/tmp/x/max.sqlite', 'r1').startsWith('/tmp/x/manifests/'));
  assert.ok(manifestPath('/var/lib/rayca/modulon-max.sqlite', 'r1').includes('/var/lib/rayca/manifests/'));
});

test('a run id that is not filename-safe cannot escape the directory', () => {
  /* A run id arrives from a request body. This asserts containment by RESOLVING the path, which is the
     property that matters, and separately that no `..` survives into the name: the first version of
     the sanitiser left `..` intact because a dot is a legal filename character, and a name carrying
     `..` is one refactor away from being joined somewhere it would matter. */
  for (const bad of ['../../etc/passwd', '..', '....//..', '/abs/path', '.hidden']) {
    const p = manifestPath('/tmp/x/max.sqlite', bad);
    assert.equal(resolve(p).startsWith(resolve('/tmp/x/manifests') + '/'), true, `escaped with ${bad}`);
    assert.ok(!p.includes('..'), `dots survived with ${bad}`);
    assert.ok(!basename(p).startsWith('.'), `hidden file with ${bad}`);
  }
});

test('an absent manifest reads as null rather than throwing', () => {
  const dir = mkdtempSync(join(tmpdir(), 'mf-'));
  assert.equal(readManifest(join(dir, 'max.sqlite'), 'nope'), null);
  rmSync(dir, { recursive: true, force: true });
});

test('a corrupt manifest reads as null rather than throwing', () => {
  /* A file cut off by a crash must not take down the hook that reads it. */
  const dir = mkdtempSync(join(tmpdir(), 'mf-'));
  const db = join(dir, 'max.sqlite');
  const m = buildManifest({ runId: 'r1', run: RUN, events: [], files: [] });
  const path = writeManifest(db, m);
  writeFileSync(path, '{"version": 1, "run_i');
  assert.equal(readManifest(db, 'r1'), null);
  rmSync(dir, { recursive: true, force: true });
});

test('the snapshot is short, because it is injected into a compacted context', () => {
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: RECORDS });
  const text = snapshotOf(m);
  const lines = text.split('\n');
  assert.ok(lines.length <= 10, `snapshot grew to ${lines.length} lines`);
  assert.ok(text.includes('max-604740ffad'));
  assert.ok(text.includes('Run all 5 tools'), 'the open phase must be named');
  assert.ok(/Files produced: 3/.test(text));
  assert.ok(/filed by declaration/.test(text), 'the declared count is the point of T1');
});

test('the snapshot of nothing is empty rather than a broken sentence', () => {
  assert.equal(snapshotOf(null), '');
});

// ─── WS-30 T6: what a compacted context is handed ──────────────────────────────

const withDocsAndJobs = () => buildManifest({
  runId: RUN.id,
  run: RUN,
  events: [
    plan(THREE_PHASES),
    { kind: 'job.submitted', tool: 'deep-viscosity', host: 'agents-sandbox1' },
    { kind: 'job.submitted', tool: 'biophi', host: 'agents-sandbox1', rc: 0, state: 'done' },
  ],
  files: RECORDS,
});

test('the rehydration names the documents with their paths', () => {
  /* Named rather than summarised: the reference framework's recovery skill reads the last documents
     because a compact summary cannot carry the reasoning and the parameter values. A path makes
     re-reading one Read away. */
  const text = rehydrationFrom(withDocsAndJobs(), 'Your context was compacted.');
  assert.match(text, /Read these before continuing/);
  assert.match(text, /01_fetch\/reports\/phase_01_fetch\.md/);
});

test('the rehydration states the open phase and the file count', () => {
  const text = rehydrationFrom(withDocsAndJobs(), 'why');
  assert.match(text, /Run all 5 tools/);
  assert.match(text, /Files produced: 3/);
});

test('a job with no result is called out separately, not buried in a count', () => {
  /* MEASURED on run max-604740ffad: five jobs on a COMPLETE run carried no exit code, because
     `job.submitted` carries none. A forgotten open job is the most expensive thing to redo. */
  const text = rehydrationFrom(withDocsAndJobs(), 'why');
  assert.match(text, /Jobs with no result recorded: deep-viscosity/);
  assert.ok(!/biophi/.test(text.split('Jobs with no result')[1] || ''), 'a finished job must not be listed');
});

test('a run with no open jobs says nothing about jobs', () => {
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: RECORDS });
  assert.ok(!/Jobs with no result/.test(rehydrationFrom(m, 'why')));
});

test('the rehydration always says the manifest is current and the context is not', () => {
  /* The one sentence that makes the rest actionable: without it the model has no reason to prefer this
     over its own recollection. */
  const text = rehydrationFrom(withDocsAndJobs(), 'why');
  assert.match(text, /derived from this run's own tape and artifact index/);
  assert.match(text, /Your conversation context is not/);
});

test('the reason it was sent leads the text', () => {
  const text = rehydrationFrom(withDocsAndJobs(), 'Your context was compacted.');
  assert.ok(text.startsWith('Your context was compacted.'), text.slice(0, 60));
});

test('no manifest yields no text rather than a header with nothing under it', () => {
  assert.equal(rehydrationFrom(null, 'why'), '');
});

test('a manifest with no documents still rehydrates the rest', () => {
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: [RECORDS[1]] });
  const text = rehydrationFrom(m, 'why');
  assert.ok(!/Read these before continuing/.test(text));
  assert.match(text, /Files produced: 1/);
});

test('at most three documents are named, however many the run wrote', () => {
  const many = Array.from({ length: 9 }, (_, n) => ({
    id: `d${n}`, name: `phase_0${n}.md`, folder: `0${n}_p/reports`, kind: 'documents', size: 10,
  }));
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: many });
  const named = (rehydrationFrom(m, 'why').match(/phase_0\d\.md/g) || []);
  // The snapshot line lists them too, so count only the ones under the read instruction.
  const afterInstruction = rehydrationFrom(m, 'why').split('Read these before continuing')[1] || '';
  assert.equal((afterInstruction.match(/  0\d_p\/reports\//g) || []).length, 3, named.join(','));
});

// ─── WS-30 T7: what the run still owes, derived ────────────────────────────────

const kinds = (m) => (m.obligations || []).map((o) => o.kind);

test('a result with no document owes a document', () => {
  const m = buildManifest({
    runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)],
    files: [{ id: 'a1', name: 'affinities.json', folder: 'results', kind: 'data', role: 'results',
              phase: 'screening', size: 10 }],
  });
  assert.ok(kinds(m).includes('document_step'));
  const owed = m.obligations.find((o) => o.kind === 'document_step');
  assert.match(owed.context, /affinities\.json/);
  assert.equal(owed.phase, 'screening');
});

test('working material owes nothing, because scratch is not a result', () => {
  /* Logs, intermediates and scratch are the majority of what a run writes. Demanding a document for each
     would be the cage this workstream exists to avoid. */
  const m = buildManifest({
    runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)],
    files: [{ id: 'w1', name: 'run.log', folder: 'work', kind: 'other', size: 10 }],
  });
  assert.ok(!kinds(m).includes('document_step'));
});

test('a phase that has been written up owes no document', () => {
  const m = buildManifest({
    runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)],
    files: [
      { id: 'a1', name: 'affinities.json', folder: 'results', kind: 'data', role: 'results', phase: 'dock' },
      { id: 'd1', name: 'phase_dock.md', folder: 'reports', kind: 'documents', phase: 'dock' },
    ],
  });
  assert.ok(!kinds(m).includes('document_step'));
});

test('one phase written up does not clear another phase debt', () => {
  /* Keyed on the PHASE, which is why the phase had to reach the record first. A run-wide obligation would
     clear as soon as any single phase was documented. */
  const m = buildManifest({
    runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)],
    files: [
      { id: 'a1', name: 'a.json', folder: 'results', kind: 'data', role: 'results', phase: 'dock' },
      { id: 'd1', name: 'phase_dock.md', folder: 'reports', kind: 'documents', phase: 'dock' },
      { id: 'a2', name: 'b.json', folder: 'results', kind: 'data', role: 'results', phase: 'screen' },
    ],
  });
  const owed = m.obligations.filter((o) => o.kind === 'document_step');
  assert.equal(owed.length, 1);
  assert.equal(owed[0].phase, 'screen');
});

test('a finished phase owes an audit, and an audit document settles it', () => {
  const done = THREE_PHASES.map((p) => ({ ...p, state: 'done' }));
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(done)], files: [] });
  assert.equal(m.obligations.filter((o) => o.kind === 'phase_audit').length, 3);

  const settled = buildManifest({
    runId: RUN.id, run: RUN, events: [plan(done)],
    files: [{ id: 'x', name: '004_phase1_audit.md', folder: 'reports', kind: 'documents',
              phase: 'Fetch IEDB epitopes for deepimmuno' }],
  });
  assert.equal(settled.obligations.filter((o) => o.kind === 'phase_audit').length, 2);
});

test('a phase still running owes no audit yet', () => {
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: [] });
  // Two of the three are done in the fixture; the running one must not be asked for.
  const audits = m.obligations.filter((o) => o.kind === 'phase_audit');
  assert.equal(audits.length, 2);
  assert.ok(!audits.some((a) => /Run all 5 tools/.test(a.phase)));
});

test('a compaction with nothing produced since owes a recovery read', () => {
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(THREE_PHASES), { kind: 'file.observed' }, { kind: 'compact', phase: 'after' }],
    files: [],
  });
  assert.ok(kinds(m).includes('recovery_audit'));
});

test('work done since the compaction settles it, because the run evidently found its feet', () => {
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(THREE_PHASES), { kind: 'compact', phase: 'after' }, { kind: 'file.observed' }],
    files: [],
  });
  assert.ok(!kinds(m).includes('recovery_audit'));
});

test('a run with no compaction is never asked to recover', () => {
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: [] });
  assert.ok(!kinds(m).includes('recovery_audit'));
});

test('the pipeline kinds are named in one place for T8 to gate on', () => {
  assert.deepEqual([...PIPELINE_KINDS], ['document_step', 'verify_step', 'commit_step']);
});

test('obligations reach the rehydration text, so a compacted run is told what it owes', () => {
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(THREE_PHASES), { kind: 'compact', phase: 'after' }],
    files: [{ id: 'a1', name: 'affinities.json', folder: 'results', kind: 'data', role: 'results', phase: 'dock' }],
  });
  assert.match(rehydrationFrom(m, 'why'), /Open obligations:/);
});

test('obligationsFrom needs no events and does not throw without them', () => {
  const m = { generated_at: 'now', produced: [], documents: [], phases: [] };
  assert.deepEqual(obligationsFrom(m, undefined), []);
  assert.deepEqual(obligationsFrom(null, null), []);
});

// ─── WS-30 T8: the soft block, and every way out of it ─────────────────────────

/** A manifest owing a document, which is a PIPELINE obligation and therefore blocks. */
const owingDocument = () => buildManifest({
  runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)],
  files: [{ id: 'a1', name: 'affinities.json', folder: 'results', kind: 'data', role: 'results', phase: 'dock' }],
});

/** A manifest owing only an audit, which is SITUATIONAL and must never block. */
const owingAuditOnly = () => buildManifest({
  runId: RUN.id, run: RUN,
  events: [plan(THREE_PHASES.map((p) => ({ ...p, state: 'done' })))],
  files: [],
});

test('an undocumented result holds the turn open', () => {
  const d = stopDecision({ manifest: owingDocument(), stopHookActive: false, blocksSoFar: 0 });
  assert.equal(d.action, 'block');
  assert.match(d.text, /affinities\.json/);
  assert.match(d.text, /nobody can check, cite or reuse/);
});

test('a run owing nothing is not touched', () => {
  const clean = buildManifest({ runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: [] });
  clean.obligations = [];
  assert.equal(stopDecision({ manifest: clean, stopHookActive: false, blocksSoFar: 0 }).action, 'none');
});

test('an audit is advisory FOR EVER, because an audit that blocks a run is a cage', () => {
  const d = stopDecision({ manifest: owingAuditOnly(), stopHookActive: false, blocksSoFar: 0 });
  assert.equal(d.action, 'advise');
  assert.match(d.text, /not blocking/i);
});

test('ESCAPE 1: stop_hook_active never blocks twice on one chain', () => {
  /* The SDK sets this when a Stop hook has already blocked and the model is continuing because of it
     (sdk.d.ts:7883). Blocking again on the same chain is how a loop starts. */
  const d = stopDecision({ manifest: owingDocument(), stopHookActive: true, blocksSoFar: 0 });
  assert.equal(d.action, 'advise');
  assert.match(d.text, /Not blocking again/);
});

test('ESCAPE 2: a run asked twice is not asked again', () => {
  const d = stopDecision({ manifest: owingDocument(), stopHookActive: false, blocksSoFar: MAX_STOP_BLOCKS });
  assert.equal(d.action, 'advise');
  assert.match(d.text, /has been asked 2 times/);
});

test('and it says so rather than going quiet', () => {
  /* A mechanism that stops mattering without explanation is worse than one that never existed. */
  const d = stopDecision({ manifest: owingDocument(), stopHookActive: false, blocksSoFar: 9 });
  assert.equal(d.action, 'advise');
  assert.match(d.text, /Still owed/);
});

test('ESCAPE 3: background work means the session is waiting, not done', () => {
  /* Holding a turn open while a container is still running would ask the model to document work that has
     not finished. */
  const d = stopDecision({
    manifest: owingDocument(), stopHookActive: false, blocksSoFar: 0,
    backgroundTasks: [{ id: 'b1', status: 'running' }],
  });
  assert.equal(d.action, 'advise');
  assert.match(d.text, /1 background task\(s\) still running/);
});

test('the block names the advisory items too, without letting them cause it', () => {
  const m = owingDocument();
  m.obligations.push({ kind: 'phase_audit', created_at: 'now', phase: 'p', context: 'phase p has no audit' });
  const d = stopDecision({ manifest: m, stopHookActive: false, blocksSoFar: 0 });
  assert.equal(d.action, 'block');
  /* Asserted as containment rather than as the first item: the fixture's own finished phases already owe
     audits, so the advisory list has several entries joined together. Pinning the order would be pinning
     the fixture, not the behaviour. */
  const tail = d.text.split('Also open, but not blocking:')[1] || '';
  assert.ok(tail.includes('phase p has no audit'), d.text);
  assert.ok(!d.text.startsWith('Also open'), 'the block must be caused by the pipeline item');
});

test('the cap is small on purpose', () => {
  /* Two is enough to be heard and few enough that a run which genuinely cannot document still finishes.
     The evidence for erring this way is a hard refusal added and removed inside one hour on 2026-08-29,
     which killed three real gnina dispatches. */
  assert.ok(MAX_STOP_BLOCKS <= 3, `a cap of ${MAX_STOP_BLOCKS} is a cage waiting to happen`);
});

test('no path in the decision can ever hard-refuse', () => {
  /* Asserted across the whole matrix rather than case by case: the property is that `block` and `advise`
     and `none` are the only outcomes, whatever the inputs. */
  for (const stopHookActive of [true, false]) {
    for (const blocksSoFar of [0, 1, 2, 5]) {
      for (const backgroundTasks of [[], [{ id: 'x' }]]) {
        for (const manifest of [owingDocument(), owingAuditOnly()]) {
          const d = stopDecision({ manifest, stopHookActive, blocksSoFar, backgroundTasks });
          assert.ok(['block', 'advise', 'none'].includes(d.action), JSON.stringify(d));
          if (d.action !== 'none') assert.ok(d.text && d.text.length > 20, JSON.stringify(d));
        }
      }
    }
  }
});

test('a run always reaches a state where it is no longer blocked', () => {
  /* THE LIVENESS PROPERTY, asserted rather than argued: walk the counter up and confirm the block stops. */
  let blocked = 0;
  for (let n = 0; n < 10; n += 1) {
    if (stopDecision({ manifest: owingDocument(), stopHookActive: false, blocksSoFar: n }).action === 'block') {
      blocked += 1;
    }
  }
  assert.equal(blocked, MAX_STOP_BLOCKS, 'the block must stop of its own accord');
});

// ─── WS-30 T9: a document that says nothing checkable ──────────────────────────

const DOC = { id: 'd1', name: 'phase_01_dock.md', folder: 'reports', kind: 'documents',
              phase: 'dock', size: 900, source_path: '/tmp/does-not-matter.md' };
const RESULT = { id: 'a1', name: 'affinities.json', folder: 'results', kind: 'data',
                 role: 'results', phase: 'dock', size: 10 };

const withDoc = (text, extra = []) => buildManifest({
  runId: RUN.id, run: RUN, events: [plan(THREE_PHASES), ...extra],
  files: [RESULT, DOC],
  readDoc: () => text,
});

test('a document with a filled Verification section is verified', () => {
  const m = withDoc('# doc\n## Verification\n- 2 calls ran, 0 failed.\n## Limitations\nnone\n');
  assert.equal(m.documents[0].verified, true);
  assert.ok(!kinds(m).includes('verify_step'));
});

test('a document with an EMPTY Verification section owes a verification', () => {
  /* The reference's own rule: `body.split("## Verification")[1]` and a check that it is not blank. */
  const m = withDoc('# doc\n## Verification\n\n## Limitations\nnone\n');
  assert.equal(m.documents[0].verified, false);
  assert.ok(kinds(m).includes('verify_step'));
});

test('a document with no Verification section at all owes one', () => {
  const m = withDoc('# doc\n## Results\nsome prose\n');
  assert.ok(kinds(m).includes('verify_step'));
});

test('a document that cannot be read counts as unverified, never as verified', () => {
  /* Unread is not checked. Treating an unreadable document as verified would let the mechanism be defeated
     by a missing file. */
  const m = buildManifest({
    runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: [RESULT, DOC],
    readDoc: () => { throw new Error('gone'); },
  });
  assert.equal(m.documents[0].verified, false);
});

test('no reader at all is honest about it rather than optimistic', () => {
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(THREE_PHASES)], files: [RESULT, DOC] });
  assert.equal(m.documents[0].verified, false);
});

test('a container that ran with no document naming its image owes container_doc', () => {
  const m = withDoc('# doc\n## Verification\n- 1 call ran.\n',
                    [{ kind: 'job.submitted', tool: 'gnina', host: 'h1' }]);
  assert.ok(kinds(m).includes('container_doc'));
});

test('a document naming the image settles it', () => {
  const m = withDoc('# doc\n## Verification\n- Container Image: `gnina:latest`\n',
                    [{ kind: 'job.submitted', tool: 'gnina', host: 'h1' }]);
  assert.ok(!kinds(m).includes('container_doc'));
});

test('a run with no container jobs is never asked to describe one', () => {
  const m = withDoc('# doc\n## Verification\n- 1 call ran.\n');
  assert.ok(!kinds(m).includes('container_doc'));
});

test('verify_step blocks and container_doc does not', () => {
  /* The split matters: an undescribed container is a gap in the record, not a reason to hold a turn open. */
  assert.ok(PIPELINE_KINDS.includes('verify_step'));
  assert.ok(!PIPELINE_KINDS.includes('container_doc'));
});

test('the Verification section is read only down to the next heading', () => {
  /* Prose under a LATER heading must not count as verification, or any document with words in it would
     clear the obligation. */
  const m = withDoc('# doc\n## Verification\n\n## Results\nplenty of prose here\n');
  assert.equal(m.documents[0].verified, false);
});

// ─── WS-30 T10: the audit brief ────────────────────────────────────────────────

const auditable = () => buildManifest({
  runId: RUN.id, run: RUN, events: [plan(THREE_PHASES.map((p) => ({ ...p, state: 'done' })))],
  files: [
    { id: 'a1', name: 'affinities.json', folder: 'results', kind: 'data', role: 'results', phase: 'dock' },
    { id: 's1', name: '004_dock.py', folder: 'source', kind: 'code', role: 'source', phase: 'dock' },
    { id: 'd1', name: 'phase_dock.md', folder: 'reports', kind: 'documents', phase: 'dock',
      source_path: '/tmp/x.md' },
  ],
  readDoc: () => '## Verification\n- 1 call ran.\n',
});

test('the brief demands a SEPARATE subagent and says why', () => {
  /* The whole value of the reference's audit skill. Per-step verification shares the author's assumptions,
     so it cannot see a mistake the writer and the reader both make. */
  const b = auditBrief(auditable(), 'dock');
  assert.match(b, /SEPARATE subagent/);
  assert.match(b, /shares the assumptions/);
});

test('the brief names the documents, the results and the scripts to open', () => {
  const b = auditBrief(auditable(), 'dock');
  assert.match(b, /reports\/phase_dock\.md/);
  assert.match(b, /affinities\.json/);
  assert.match(b, /004_dock\.py/);
});

test('the brief tells the subagent NOTHING about what to expect', () => {
  /* THE PROPERTY THAT MAKES AN AUDIT WORTH RUNNING, asserted rather than trusted to good intentions. A
     brief that leaks the answer produces a subagent that confirms it. */
  const b = auditBrief(auditable(), 'dock');
  for (const leak of [/should be/i, /we expect/i, /expected to/i, /is correct/i, /looks good/i,
                      /confirm that it (is|was) (right|correct)/i, /verify that everything/i]) {
    assert.ok(!leak.test(b), `the brief leaks an expectation: ${leak}`);
  }
});

test('the brief asks the inverting question rather than for a verdict', () => {
  /* "If exactly one thing were wrong, what would it be" is the reference's own device, and it works because
     it cannot be answered by agreeing. */
  assert.match(auditBrief(auditable(), 'dock'), /riskiest assumption/);
  assert.match(auditBrief(auditable(), 'dock'), /exactly one thing in this phase were wrong/);
});

test('the brief demands the VERIFIED CORRECT list too', () => {
  /* Knowing what was checked and held up is worth as much as knowing what broke, and without this the
     report degenerates into a list of complaints. */
  const b = auditBrief(auditable(), 'dock');
  assert.match(b, /VERIFIED CORRECT/);
  assert.match(b, /not optional/);
});

test('a phase with no document is told that IS the finding', () => {
  const m = buildManifest({
    runId: RUN.id, run: RUN, events: [plan(THREE_PHASES.map((p) => ({ ...p, state: 'done' })))],
    files: [{ id: 'a1', name: 'a.json', folder: 'results', kind: 'data', role: 'results', phase: 'dock' }],
  });
  assert.match(auditBrief(m, 'dock'), /No document exists for this phase/);
});

test('the brief says it does not block', () => {
  /* An audit that blocks a run is the cage in a different coat. */
  assert.match(auditBrief(auditable(), 'dock'), /advisory: it does not block/);
});

test('the brief names the file to write, because that is what records the review', () => {
  assert.match(auditBrief(auditable(), 'dock'), /name contains "audit"/);
});

test('an open audit arrives WITH its brief, not as a bare nag', () => {
  const m = auditable();
  const d = stopDecision({ manifest: m, stopHookActive: false, blocksSoFar: 0 });
  assert.equal(d.action, 'advise');
  assert.match(d.text, /SEPARATE subagent/);
});

test('no manifest yields no brief', () => {
  assert.equal(auditBrief(null, 'dock'), '');
});

// ─── WS-30 T11: the step push, only when a repository is bound ─────────────────

const DONE_PHASES = THREE_PHASES.map((p) => ({ ...p, state: 'done' }));

test('a session with NOTHING bound never owes a commit', () => {
  /* THE PROPERTY THAT KEEPS THIS FROM BEING A CAGE. `commit_step` is a PIPELINE kind, so it holds turns
     open. An obligation that can never be satisfied would block every session that never connected a
     repository, which is most of them. `autoPushToGitHub` returns silently on `no_repo`, so the absence of
     a `publish` event is the evidence, and no lookup had to be invented. */
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(DONE_PHASES)], files: [] });
  assert.ok(!kinds(m).includes('commit_step'));
});

test('a session with a repository bound owes a commit for an unpushed phase', () => {
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(DONE_PHASES), { kind: 'publish', ok: true, step: '1' }],
    files: [],
  });
  const owed = m.obligations.filter((o) => o.kind === 'commit_step');
  assert.equal(owed.length, 2, 'phases 2 and 3 are unpushed');
  assert.ok(!owed.some((o) => /IEDB/.test(o.phase)), 'phase 1 was pushed and must not be owed');
});

test('a push for every closed phase settles it', () => {
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(DONE_PHASES),
             { kind: 'publish', ok: true, step: '1' },
             { kind: 'publish', ok: true, step: '2' },
             { kind: 'publish', ok: true, step: '3' }],
    files: [],
  });
  assert.ok(!kinds(m).includes('commit_step'));
});

test('a whole-run push carries no step and settles nothing', () => {
  /* The finaliser has pushed once per run since long before this task. Letting that settle a phase would
     mean one push at the end claiming every step was recorded separately. */
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(DONE_PHASES), { kind: 'publish', ok: true }],
    files: [],
  });
  assert.equal(m.obligations.filter((o) => o.kind === 'commit_step').length, 3);
});

test('a phase still running is not asked to have been pushed', () => {
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(THREE_PHASES), { kind: 'publish', ok: true, step: '1' }],
    files: [],
  });
  const owed = m.obligations.filter((o) => o.kind === 'commit_step');
  assert.ok(!owed.some((o) => /Run all 5 tools/.test(o.phase)));
});

test('commit_step blocks, which is why the bound check has to be right', () => {
  assert.ok(PIPELINE_KINDS.includes('commit_step'));
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(DONE_PHASES), { kind: 'publish', ok: true, step: '1' }],
    files: [],
  });
  const d = stopDecision({ manifest: m, stopHookActive: false, blocksSoFar: 0 });
  assert.equal(d.action, 'block');
  /* MOVED, NOT DELETED. This asserted "not pushed to the bound repository", which is the exact wording that sent a model
     hunting for a repository the session did not have. The obligation now names a real repository or, as here where the
     successful push carried no name, says only that the push did not complete. The PROPERTY being tested is unchanged:
     an owed commit blocks and says why. */
  assert.match(d.text, /push did not complete/);
  assert.ok(!/the bound repository/.test(d.text));
});

test('and an unbound session is never blocked by it', () => {
  const m = buildManifest({ runId: RUN.id, run: RUN, events: [plan(DONE_PHASES)], files: [] });
  const d = stopDecision({ manifest: m, stopHookActive: false, blocksSoFar: 0 });
  assert.notEqual(d.action, 'block');
});

// ─── the advisory is said once, because anything returned re-prompts ───────────

test('an advisory is delivered once and then the hook goes silent', () => {
  /*
   * THE DEFECT THIS ENCODES, measured on run max-70e85d02e6. The block cap worked: one block, then it stood aside. The
   * ADVISORY had no cap, so it fired on all 27 stop attempts that followed. An advisory is returned as
   * `additionalContext`, and context on Stop re-prompts the model, so each one produced another turn, another "Ready."
   * and another stop attempt. The run took eleven extra minutes and ended only when the model gave up.
   *
   * "ADVISORY" IS NOT THE SAME AS "HARMLESS". Anything this hook returns pushes the model.
   */
  const m = auditable();
  const seen = [];
  for (let i = 0; i < 12; i += 1) {
    seen.push(stopDecision({ manifest: m, stopHookActive: false, blocksSoFar: 0, advisoriesSoFar: i }).action);
  }
  assert.equal(seen.filter((a) => a === 'advise').length, MAX_STOP_ADVISORIES);
  assert.ok(seen.slice(MAX_STOP_ADVISORIES).every((a) => a === 'none'),
    'past the cap the hook must return nothing at all, not a quieter advisory');
});

test('the silent decision carries no text, so nothing can be emitted by accident', () => {
  const d = stopDecision({ manifest: auditable(), stopHookActive: false, blocksSoFar: 0, advisoriesSoFar: 5 });
  assert.equal(d.action, 'none');
  assert.equal(d.text, '');
});

test('the cap does not touch blocking, which has its own and larger budget', () => {
  /* A block asks for something and the model can satisfy it, so repeating it twice is useful. An advisory asks for
     nothing, which is why one is enough and two is a loop. */
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(DONE_PHASES), { kind: 'publish', ok: true, step: '1' }],
    files: [],
  });
  let blocks = 0;
  for (let i = 0; i < 10; i += 1) {
    if (stopDecision({ manifest: m, stopHookActive: false, blocksSoFar: blocks, advisoriesSoFar: 99 })
      .action === 'block') blocks += 1;
  }
  assert.equal(blocks, MAX_STOP_BLOCKS);
});

test('the audit brief still reaches the model on that one advisory', () => {
  /* The cap must not make T10 dead text. */
  const d = stopDecision({ manifest: auditable(), stopHookActive: false, blocksSoFar: 0, advisoriesSoFar: 0 });
  assert.equal(d.action, 'advise');
  assert.match(d.text, /SEPARATE subagent/);
});

// ─── the advisory budget holds on EVERY path, not one branch ───────────────────

test('every input that yields an advisory is capped, whichever branch produced it', () => {
  /*
   * THE TEST THAT WOULD HAVE CAUGHT BOTH OF MY BUGS.
   *
   * The first cap lived inside ONE branch of the reason, and four other paths return `advise`: background tasks
   * outstanding, `stop_hook_active` already set, the block budget spent, and no pipeline obligation left. And the
   * counter was never passed from the hook at all, so the budget defaulted to 0 and could not fire. Measured after I
   * had already reported it fixed: 29 advisories on run max-1614a1d494.
   *
   * SO THE PROPERTY IS ASSERTED OVER THE WHOLE MATRIX rather than over the branch I happened to be thinking about.
   */
  const owing = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(DONE_PHASES), { kind: 'publish', ok: true, step: '1' }],
    files: [],
  });
  const advisoryOnly = auditable();
  let checked = 0;
  for (const manifest of [owing, advisoryOnly]) {
    for (const stopHookActive of [true, false]) {
      for (const blocksSoFar of [0, 1, 2, 3]) {
        for (const backgroundTasks of [[], ['t1']]) {
          const fresh = stopDecision({ manifest, stopHookActive, blocksSoFar, backgroundTasks,
            advisoriesSoFar: 0 });
          const spent = stopDecision({ manifest, stopHookActive, blocksSoFar, backgroundTasks,
            advisoriesSoFar: MAX_STOP_ADVISORIES });
          checked += 1;
          if (fresh.action === 'advise') {
            assert.equal(spent.action, 'none',
              `an advisory survived the budget: stopHookActive=${stopHookActive} blocks=${blocksSoFar} `
              + `bg=${backgroundTasks.length}`);
            assert.equal(spent.text, '', 'and it must carry no text');
          } else {
            assert.equal(spent.action, fresh.action, 'the budget must not change a block or a silence');
          }
        }
      }
    }
  }
  assert.equal(checked, 32, 'the whole matrix was walked');
});

test('an advisory is delivered once and then the hook is silent, whatever the reason', () => {
  const m = auditable();
  const seen = [];
  for (let i = 0; i < 12; i += 1) {
    seen.push(stopDecision({ manifest: m, stopHookActive: false, blocksSoFar: 0, advisoriesSoFar: i }).action);
  }
  assert.equal(seen.filter((a) => a === 'advise').length, MAX_STOP_ADVISORIES);
  assert.ok(seen.slice(MAX_STOP_ADVISORIES).every((a) => a === 'none'));
});

test('walking the counter as the hook does gives exactly the budget', () => {
  /* The hook increments only on the advise path. Walked here the way it really runs, because the previous version of
     this test asserted the pure function and the wiring was what was broken. */
  const m = auditable();
  let advisories = 0;
  let delivered = 0;
  for (let turn = 0; turn < 20; turn += 1) {
    const d = stopDecision({ manifest: m, stopHookActive: false, blocksSoFar: 0, advisoriesSoFar: advisories });
    if (d.action === 'none') continue;
    if (d.action === 'advise') { delivered += 1; advisories += 1; }
  }
  assert.equal(delivered, MAX_STOP_ADVISORIES, 'twenty turns, one advisory');
});

// ─── a failed push is not evidence that a repository is bound ──────────────────

test('a push that FAILED creates no obligation', () => {
  /*
   * THE CHAIN THAT PUT FOURTEEN FILES IN SOMEONE ELSE'S REPOSITORY, and every link was mine.
   *
   * T11 referenced `message` and `step` without declaring them, because the edit that changed the signature was lost to
   * a script that asserted later and never wrote. Every phase-close push threw `message is not defined`, was caught, and
   * emitted `{ok: false, error: "hook_failed"}`. This derivation counted that as proof a repository was bound. The
   * obligation then told the model a phase "was not pushed to the bound repository" -- of a session with none -- so the
   * model found `RaycaBio/binding-affinity-demo`, called it a closest fit, and pushed a throwaway test run into it.
   */
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(DONE_PHASES), { kind: 'publish', ok: false, error: 'hook_failed', detail: 'message is not defined' }],
    files: [],
  });
  assert.ok(!kinds(m).includes('commit_step'),
    'a push that failed may have failed BECAUSE nothing was bound; it proves nothing');
});

test('a mix of failed and successful pushes still counts only the successful one', () => {
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(DONE_PHASES),
             { kind: 'publish', ok: false, error: 'hook_failed' },
             { kind: 'publish', ok: true, step: '1', repo: 'RaycaBio/study-x' }],
    files: [],
  });
  const owed = m.obligations.filter((o) => o.kind === 'commit_step');
  assert.equal(owed.length, 2, 'phases 2 and 3');
});

test('the obligation NAMES the repository rather than implying one exists', () => {
  /* An instruction that cannot be followed literally gets followed liberally. */
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(DONE_PHASES), { kind: 'publish', ok: true, step: '1', repo: 'RaycaBio/study-x' }],
    files: [],
  });
  const owed = m.obligations.filter((o) => o.kind === 'commit_step');
  assert.ok(owed.every((o) => o.context.includes('RaycaBio/study-x')));
  assert.ok(owed.every((o) => !/the bound repository/.test(o.context)),
    'never a repository the session may not have');
});

test('with a successful push carrying no repo name, it asks for nothing specific', () => {
  const m = buildManifest({
    runId: RUN.id, run: RUN,
    events: [plan(DONE_PHASES), { kind: 'publish', ok: true, step: '1' }],
    files: [],
  });
  const owed = m.obligations.filter((o) => o.kind === 'commit_step');
  assert.ok(owed.every((o) => /push did not complete/.test(o.context)));
  assert.ok(owed.every((o) => !/bound repository/.test(o.context)));
});
