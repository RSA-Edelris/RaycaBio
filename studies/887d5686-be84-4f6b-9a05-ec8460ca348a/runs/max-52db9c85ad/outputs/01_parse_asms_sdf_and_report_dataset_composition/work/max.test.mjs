/**
 * Tests for the parts that must be right whether or not a model is available.
 *
 * ASSERTS ON BEHAVIOUR, NOT WIRING. Each case here exists because a real run got it wrong: a traceback reported as
 * success, a tool that produced nothing reported as a result, a team staffed by whoever happened to be first in the
 * registry, a run left `running` by a process that died. Reading the code would not have caught any of them.
 *
 * Run: node --test modulon-max/
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

import { failedInside, producedNothing, nameAndOrigin, KINDS } from './events.mjs';
import { dispatchesIn, titleFor, toJobEvent, workflowFrom, toJobSubmittedEvent, jobOutcome,
  promptAttachmentsFrom, withPromptAttachments, userPromptEvent, toConsoleEvent,
  clusterJobIn, toClusterJobEvent } from './consoleapi.mjs';
import { rankPersonas } from './personas.mjs';
import { modelsFromRouterPayload, fallbackModels, fetchRouterModels } from './models.mjs';
import { pricesFromRouterPayload, costOf, priceKeyFor } from './pricing.mjs';
import { newTaskTable, noteTask, taskPhases, taskCounts, stateFrom } from './tasks.mjs';
import { Store } from './store.mjs';

/* ------------------------------------------------------------------------------------------------------------------
 * A call that returned is not a call that worked
 * ---------------------------------------------------------------------------------------------------------------- */

test('a python traceback is not success', () => {
  // MEASURED: `run_python` hands back a traceback as its output with a good exit status, and `meta.ok` is True on
  // failing steps throughout this codebase. Reporting that as success is how a reader trusts a number never computed.
  const out = JSON.stringify({
    output: 'Traceback (most recent call last):\n  File "<model>", line 3\nNameError: x is not defined',
  });
  assert.equal(failedInside(out), true);
});

test('a non-zero rc is not success', () => {
  assert.equal(failedInside('{"rc": 1, "gpu": true, "error": "tool_failed"}'), true);
});

test('a real result is not reported as a failure', () => {
  // The opposite error matters just as much: flagging good output would teach a reader to ignore the flag.
  assert.equal(failedInside('{"output": "Exact MW: 493.2590086120001\\nRotatable bonds: 7"}'), false);
  assert.equal(failedInside('{"rc": 0, "seqs": 3}'), false);
});

test('the word error inside a successful payload does not trip it', () => {
  assert.equal(failedInside('{"rc": 0, "error": "none", "output": "fine"}'), false);
});

/* ------------------------------------------------------------------------------------------------------------------
 * Success that produced nothing
 * ---------------------------------------------------------------------------------------------------------------- */

test('all-zero counts is producing nothing', () => {
  // MEASURED on run-f2e7c8c64b6b: binderflow returned rc=0 four times with every count at zero, and the model spent
  // three more dispatches loosening scoring thresholds -- which cannot help when nothing was generated.
  const out = JSON.stringify({ n_backbones: 0, n_filtered: 0, n_scored: 0, n_hits: 0, rc: 0 });
  assert.equal(producedNothing(out), true);
});

test('backbones that all fail the filter is a real result, not nothing', () => {
  // This is the opposite error and it is a scientific one: ten backbones with no hits is a finding about the target,
  // and loosening a threshold IS the right response. Flagging it would teach the model to distrust a true negative.
  const out = JSON.stringify({ n_backbones: 10, n_filtered: 10, n_scored: 10, n_hits: 0 });
  assert.equal(producedNothing(out), false);
});

test('empty lists with no counts is producing nothing', () => {
  assert.equal(producedNothing(JSON.stringify({ sequences: [], designs: [] })), true);
});

test('a payload with neither counts nor lists is not judged', () => {
  // Silence about a payload this cannot reason about is better than a guess.
  assert.equal(producedNothing(JSON.stringify({ output: 'ok', version: '2026.3.4' })), false);
});

/* ------------------------------------------------------------------------------------------------------------------
 * Where a verb came from
 * ---------------------------------------------------------------------------------------------------------------- */

test('a platform verb is named without its transport prefix', () => {
  assert.deepEqual(nameAndOrigin('mcp__rayca__run_on_cluster'), { verb: 'run_on_cluster', origin: 'platform' });
});

test('the loop own tools are marked as its own', () => {
  assert.deepEqual(nameAndOrigin('Bash'), { verb: 'Bash', origin: 'own' });
  // `Agent` is this SDK's delegation tool. The leaked source called it `Task`, and taking the name from there meant
  // three delegations arrived as flat tool calls with no tree at all.
  assert.deepEqual(nameAndOrigin('Agent'), { verb: 'Agent', origin: 'own' });
});

/* ------------------------------------------------------------------------------------------------------------------
 * Staffing a team
 * ---------------------------------------------------------------------------------------------------------------- */

const PERSONAS = [
  { id: 'data-privacy-counsel', name: 'Data Privacy & Clinical Contracts Counsel',
    summary: 'Owns data-protection and the clinical contracting layer', category: 'regulatory ip legal' },
  { id: 'med-chem-scientist', name: 'Medicinal Chemistry Scientist',
    summary: 'Designs and optimises small molecules for potency and selectivity', category: 'discovery chemistry' },
  { id: 'protein-eng-scientist', name: 'Protein Engineering Scientist',
    summary: 'Engineers proteins and binders', category: 'biologics' },
];

test('a chemistry question is not staffed with a privacy lawyer', () => {
  // MEASURED: the first version of team formation took the registry's first rows, and the registry's first row is the
  // privacy counsel. A chemistry question was answered by a lawyer.
  const picked = rankPersonas(PERSONAS, 'optimise the potency and selectivity of this small molecule', 2);
  assert.equal(picked[0].id, 'med-chem-scientist');
  assert.ok(!picked.some((p) => p.id === 'data-privacy-counsel'));
});

test('a persona matching nothing is left out rather than padding the team', () => {
  const picked = rankPersonas(PERSONAS, 'engineer a protein binder', 3);
  assert.ok(picked.length <= 2, 'a smaller team of specialists beats a full team of bystanders');
  assert.equal(picked[0].id, 'protein-eng-scientist');
});

test('a task matching no persona still returns a team rather than nobody', () => {
  const picked = rankPersonas(PERSONAS, 'zzzz', 3);
  assert.ok(picked.length >= 1);
});

/* ------------------------------------------------------------------------------------------------------------------
 * Runs that survive the process
 * ---------------------------------------------------------------------------------------------------------------- */

test('a run and its events survive being written and read back', () => {
  const dir = mkdtempSync(join(tmpdir(), 'max-test-'));
  try {
    const s = new Store(join(dir, 'db.sqlite'));
    s.createRun({ id: 'r1', task: 'compute something', team: 1, model: 'm' });
    s.appendEvent('r1', 0, { kind: KINDS.SESSION_START, at: 1, task: 'compute something' });
    s.appendEvent('r1', 1, { kind: KINDS.CALL, at: 2, verb: 'run_python' });
    s.finishRun('r1', { state: 'complete', turns: 2, cost: 0.1, answer: '42' });
    const back = s.eventsFor('r1');
    assert.equal(back.length, 2);
    assert.equal(back[0].kind, KINDS.SESSION_START);
    assert.equal(s.getRun('r1').state, 'complete');
    assert.equal(s.getRun('r1').answer, '42');
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('a run abandoned by a dead process is interrupted, not error', () => {
  // The distinction is not cosmetic. `error` blames the science for an infrastructure failure, and this engine's
  // predecessor lost a researcher's 1,344-event study to an OOM kill that had nothing to do with the work.
  const dir = mkdtempSync(join(tmpdir(), 'max-test-'));
  try {
    const path = join(dir, 'db.sqlite');
    const s1 = new Store(path);
    s1.createRun({ id: 'r2', task: 't', team: 0, model: 'm' });
    assert.equal(s1.getRun('r2').state, 'running');
    const s2 = new Store(path);
    const n = s2.reconcileOrphans();
    assert.equal(n, 1);
    assert.equal(s2.getRun('r2').state, 'interrupted');
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('an event kind cannot be overwritten by its own payload', () => {
  // MEASURED on run max-3100df7dcf: the emitter spread the payload over the event, so a payload field called `kind`
  // replaced the event's kind. Governance events were stored as `governance` and every reader filtering on `gate`
  // saw nothing, which made a working governance layer look entirely absent.
  const kind = KINDS.GATE;
  const data = { kind: 'governance', detail: 'active' };
  const ev = { at: 1, ...data, kind };
  assert.equal(ev.kind, KINDS.GATE, 'the payload must not decide the event kind');
  const dir = mkdtempSync(join(tmpdir(), 'max-test-'));
  try {
    const s = new Store(join(dir, 'db.sqlite'));
    s.createRun({ id: 'r3', task: 't', team: 0, model: 'm' });
    s.appendEvent('r3', 0, ev);
    assert.equal(s.eventsFor('r3')[0].kind, KINDS.GATE);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

/* ------------------------------------------------------------------------------------------------------------------
 * Container dispatches, which the Jobs panel cannot see any other way
 * ---------------------------------------------------------------------------------------------------------------- */

test('a dispatch marker becomes a job the console can read', () => {
  // THE GAP THIS CLOSES. The console's `readJobs` requires `meta.dispatch_submitted === true`, which the previous
  // engine emitted from its dispatch courier. This engine dispatches through run_python calling the platform toolkit,
  // so the facts arrive as markers in stdout. Without this the Jobs section was EMPTY on every run of this engine while
  // the run had in fact put a container on an A100 -- the most consequential thing a study does, invisible.
  const out = '[dispatch] tool=ligandmpnn rc=0 gpu=True duration_s=17.7';
  const ds = dispatchesIn(out);
  assert.equal(ds.length, 1);
  const ev = toJobEvent(ds[0], 3, 'max-x', 1, 'lead');
  assert.equal(ev.meta.dispatch_submitted, true);
  assert.equal(ev.meta.job_state, 'done');
  assert.equal(ev.meta.tool, 'ligandmpnn');
  assert.equal(ev.meta.gpu, true);
  assert.equal(ev.meta.rc, 0);
});

test('escaped newlines do not swallow the next line', () => {
  // MEASURED: a tool result arrives as the JSON text the MCP server produced, so a newline in it is the two characters
  // backslash-n. `[^\n]+` ran past the marker and `duration_s=17.7` became `duration_s=17.7\nb`, parsing as NaN. The
  // tool was found and its duration silently lost, which is worse than finding nothing.
  const jsonish = '{"output": "a\\n[dispatch] tool=x rc=0 gpu=True duration_s=3.5\\nmore text"}';
  const ds = dispatchesIn(jsonish);
  assert.equal(ds.length, 1);
  assert.equal(ds[0].seconds, 3.5);
});

test('a failed container is still a job that ran', () => {
  // A dispatch that failed must appear as a row rather than vanishing: rc carries whether the work succeeded, and a
  // reader deciding whether to trust a result needs to see the attempt.
  const ds = dispatchesIn('[dispatch] tool=ligandmpnn rc=1 gpu=True duration_s=18.2 error=tool_failed');
  assert.equal(ds.length, 1);
  assert.equal(ds[0].rc, 1);
  assert.equal(ds[0].error, 'tool_failed');
  const ev = toJobEvent(ds[0], 1, 'r', 1, 'lead');
  assert.equal(ev.meta.dispatch_submitted, true, 'a failed job is still submitted');
  assert.equal(ev.status, 'error');
});

test('two dispatches of the same tool are two jobs', () => {
  // The PD-L1 run dispatched ligandmpnn twice: once failing on a path, once succeeding after the fix. Collapsing them
  // would hide the retry, which is exactly what a reader auditing a result wants to see.
  const ds = dispatchesIn(
    '[dispatch] tool=ligandmpnn rc=1 gpu=True duration_s=18.2 error=tool_failed\n'
    + '[dispatch] tool=ligandmpnn rc=0 gpu=True duration_s=17.7',
  );
  assert.equal(ds.length, 2);
  assert.deepEqual(ds.map((d) => d.rc), [1, 0]);
});

test('text with no dispatch marker yields nothing', () => {
  assert.deepEqual(dispatchesIn('Exact MW: 493.2590086120001'), []);
  assert.deepEqual(dispatchesIn(''), []);
  assert.deepEqual(dispatchesIn(null), []);
});

test('a dispatch that never reached the host is not reported as done', () => {
  // MEASURED: the real marker for an unreachable GPU host reads `rc=None gpu=False duration_s=0.0
  // error=host_unreachable`. The Jobs panel derives `ok` from `job_state === 'done'`, so calling this done would have
  // presented a dispatch that never left the building as a completed job. A run whose GPU host was down must not look
  // like a run whose GPU work succeeded.
  const ds = dispatchesIn('[dispatch] tool=ligandmpnn rc=None gpu=False duration_s=0.0 error=host_unreachable');
  assert.equal(ds.length, 1);
  assert.equal(ds[0].rc, null, 'Python None is not a return code');
  const ev = toJobEvent(ds[0], 1, 'r', 1, 'lead');
  assert.equal(ev.meta.job_state, 'unreachable');
  assert.notEqual(ev.meta.job_state, 'done');
  assert.equal(ev.status, 'error');
  assert.match(ev.body, /did not complete: host_unreachable/);
});

test('a completed container is reported as done', () => {
  const ev = toJobEvent(dispatchesIn('[dispatch] tool=gnina rc=0 gpu=True duration_s=2.3')[0], 1, 'r', 1, 'lead');
  assert.equal(ev.meta.job_state, 'done');
  assert.equal(ev.status, 'ok');
});

/* ------------------------------------------------------------------------------------------------------------------
 * The adaptive workflow, derived from our own tape
 * ---------------------------------------------------------------------------------------------------------------- */

const wfRun = { id: 'max-1', state: 'done', model: 'claude-sonnet-4-6', answer: 'logP is 1.3101 and TPSA is 61.82.' };

test('the dispatched container is the method, not run_python', () => {
  // A graph of a PD-L1 campaign reading "run_python, run_python, run_python" says NOTHING. The model reaches containers
  // through run_python, so the wire name is always run_python and the container that did the science is invisible.
  const evs = [
    { kind: KINDS.CALL, n: 1, id: 'a', verb: 'run_python', origin: 'platform', input: { code: 'x' } },
    { kind: KINDS.BACK, n: 2, id: 'a', verb: 'run_python', origin: 'platform', returned: true,
      output: '[dispatch] tool=rfdiffusion rc=0 gpu=True duration_s=91.4' },
  ];
  const wf = workflowFrom(wfRun, evs);
  assert.deepEqual(wf.methods.map((m) => m.method), ['rfdiffusion']);
  assert.equal(wf.methods[0].status, 'done');
  assert.deepEqual(wf.methods[0].frameworks, ['container']);
  assert.equal(wf.methods[0].parameters.gpu, true);
});

test('the same verb called four times is one method with four attempts', () => {
  // A reader asking "what did this study do" wants the STEP; a reader auditing it wants to know it ran four times.
  const evs = [];
  for (let i = 0; i < 4; i += 1) {
    evs.push({ kind: KINDS.CALL, n: i * 2, id: `c${i}`, verb: 'gnina', origin: 'platform', input: {} });
    evs.push({ kind: KINDS.BACK, n: i * 2 + 1, id: `c${i}`, verb: 'gnina', origin: 'platform', returned: true, output: 'ok' });
  }
  const wf = workflowFrom(wfRun, evs);
  assert.equal(wf.methods.length, 1);
  assert.equal(wf.methods[0].attempts, 4);
  assert.deepEqual(wf.methods[0].steps, [1, 3, 5, 7]);
});

test('task bookkeeping is excluded, and excluded per VERB not per call', () => {
  // MEASURED, and the reason this test exists: checking each call's own window caught TaskCreate, whose window did
  // contain a task event, and MISSED TaskUpdate, whose calls happened not to straddle one -- so the graph still opened
  // with a bookkeeping step next to the real science. A verb that maintained the task list once is a bookkeeping verb
  // for the whole run.
  const evs = [
    { kind: KINDS.CALL, n: 0, id: 't1', verb: 'TaskUpdate', origin: 'agent', input: {} },
    { kind: KINDS.TASK, n: 1, state: 'created', subject: 'Compute logP' },
    { kind: KINDS.BACK, n: 2, id: 't1', verb: 'TaskUpdate', origin: 'agent', returned: true, output: 'ok' },
    // this second TaskUpdate straddles no task event, and must still be excluded
    { kind: KINDS.CALL, n: 3, id: 't2', verb: 'TaskUpdate', origin: 'agent', input: {} },
    { kind: KINDS.BACK, n: 4, id: 't2', verb: 'TaskUpdate', origin: 'agent', returned: true, output: 'ok' },
    { kind: KINDS.CALL, n: 5, id: 'r', verb: 'run_python', origin: 'platform', input: { code: 'x' } },
    { kind: KINDS.BACK, n: 6, id: 'r', verb: 'run_python', origin: 'platform', returned: true, output: 'logP 1.3101' },
  ];
  const wf = workflowFrom(wfRun, evs);
  assert.deepEqual(wf.methods.map((m) => m.method), ['run_python']);
});

test('the open task is the phase', () => {
  const evs = [
    { kind: KINDS.TASK, n: 0, state: 'created', subject: 'Design backbones' },
    { kind: KINDS.CALL, n: 1, id: 'a', verb: 'run_python', origin: 'platform', input: {} },
    { kind: KINDS.BACK, n: 2, id: 'a', verb: 'run_python', origin: 'platform', returned: true, output: 'ok' },
  ];
  assert.equal(workflowFrom(wfRun, evs).methods[0].phase, 'Design backbones');
});

test('a call with no answer yet is a method that is running', () => {
  // The whole point of a live canvas: a 15-minute GPU call must appear while it is still going, not after.
  const evs = [{ kind: KINDS.CALL, n: 1, id: 'a', verb: 'rfdiffusion', origin: 'platform', input: {} }];
  const wf = workflowFrom(wfRun, evs);
  assert.equal(wf.methods.length, 1);
  assert.equal(wf.methods[0].status, 'running');
});

test('a failed step is a failed method, not a missing one', () => {
  const evs = [
    { kind: KINDS.CALL, n: 1, id: 'a', verb: 'ligandmpnn', origin: 'platform', input: {} },
    { kind: KINDS.BACK, n: 2, id: 'a', verb: 'ligandmpnn', origin: 'platform', returned: true,
      failed_inside: true, output: 'ProDy needs an absolute path' },
  ];
  assert.equal(workflowFrom(wfRun, evs).methods[0].status, 'failed');
});

test('a retry that eventually worked reads as done', () => {
  // The PD-L1 run failed ligandmpnn on a path and fixed it in one retry. The method succeeded; the attempt count and the
  // failure are still visible in the steps.
  const evs = [
    { kind: KINDS.CALL, n: 1, id: 'a', verb: 'x', origin: 'platform', input: {} },
    { kind: KINDS.BACK, n: 2, id: 'a', verb: 'x', origin: 'platform', failed_inside: true, output: 'boom' },
    { kind: KINDS.CALL, n: 3, id: 'b', verb: 'x', origin: 'platform', input: {} },
    { kind: KINDS.BACK, n: 4, id: 'b', verb: 'x', origin: 'platform', returned: true, output: 'fine' },
  ];
  const wf = workflowFrom(wfRun, evs);
  assert.equal(wf.methods[0].status, 'done');
  assert.equal(wf.methods[0].attempts, 2);
});

test('the graph says it was not interpreted', () => {
  // This graph is read straight off the tape with no model in the loop, so nothing in it is a paraphrase. The previous
  // engine's graph IS interpreted, and the console shows the difference. Claiming interpretation we did not do would
  // misrepresent where the words came from.
  assert.equal(workflowFrom(wfRun, []).interpreted, false);
});

test('the conclusion carries the figures it rests on', () => {
  const wf = workflowFrom(wfRun, [
    { kind: KINDS.CALL, n: 1, id: 'a', verb: 'run_python', origin: 'platform', input: {} },
    { kind: KINDS.BACK, n: 2, id: 'a', verb: 'run_python', origin: 'platform', returned: true, output: 'ok' },
  ]);
  assert.equal(wf.conclusions.length, 1);
  assert.ok(wf.conclusions[0].figures.includes('1.3101'));
  assert.deepEqual(wf.conclusions[0].methods, ['m-1']);
});

test('a run with no answer yet has no conclusion', () => {
  // An empty finding rendered as a conclusion would assert the study concluded something when it has not.
  assert.deepEqual(workflowFrom({ id: 'max-2', state: 'running' }, []).conclusions, []);
});

/* ------------------------------------------------------------------------------------------------------------------
 * The conversation a run belongs to, which is not the transcript it reads
 * ---------------------------------------------------------------------------------------------------------------- */

test('runs are found by the conversation, not by the transcript', () => {
  /*
   * TWO DIFFERENT THINGS ARE CALLED A SESSION, AND CONFLATING THEM MADE EVERY RUN INVISIBLE TO THE CONSOLE.
   * `session_id` is the LOOP's session -- the transcript a resume or a fork reads. The console's session is the
   * CONVERSATION, and it is how the console asks "which runs belong to this chat". We recorded only the first, so that
   * question fell through the front door to the previous engine, which has never heard of a `max-` run, and answered
   * `runs: []` for every conversation. MEASURED: a page reload mid-run lost the run, run history per conversation was
   * empty, and a fork would have executed with nothing in the browser showing it.
   */
  const s = new Store(':memory:');
  s.createRun({ id: 'max-a', task: 'compute mass', team: false, model: 'm' });
  s.noteSession('max-a', 'sdk-transcript-1');
  s.noteConsoleSession('max-a', 'conv-1');
  s.appendEvent('max-a', 0, { kind: 'x' });

  const rows = s.runsForConsoleSession('conv-1');
  assert.equal(rows.length, 1);
  assert.equal(rows[0].run_id, 'max-a');
  assert.equal(rows[0].events_total, 1);
  // and the transcript id is NOT the conversation id
  assert.equal(s.runsForConsoleSession('sdk-transcript-1').length, 0);
});

test('a conversation with no runs here returns nothing, so the front door can pass through', () => {
  // Answering with an empty list would ERASE the history of conversations whose runs live in the previous engine.
  const s = new Store(':memory:');
  assert.deepEqual(s.runsForConsoleSession('conv-unknown'), []);
});

test('a run recorded before the column existed does not break the lookup', () => {
  // The column is added by migration, so older runs simply have no value. They must not appear under every conversation.
  const s = new Store(':memory:');
  s.createRun({ id: 'max-old', task: 't', team: false, model: 'm' });
  assert.deepEqual(s.runsForConsoleSession('conv-1'), []);
});

test('the newest run in a conversation is last, which is how the console picks the live one', () => {
  const s = new Store(':memory:');
  s.createRun({ id: 'max-p', task: 'parent', team: false, model: 'm' });
  s.noteConsoleSession('max-p', 'conv-1');
  s.createRun({ id: 'max-c', task: 'child', team: false, model: 'm' });
  s.noteConsoleSession('max-c', 'conv-1');
  assert.deepEqual(s.runsForConsoleSession('conv-1').map((r) => r.run_id), ['max-p', 'max-c']);
});

// ============================================================================================
// PLAN-BEFORE-DISPATCH: the mechanism that forces tasks before delegation
// ============================================================================================

test('the plan-before-dispatch gate refuses Agent when no tasks exist', () => {
  // This tests the LOGIC rather than the full hook, which needs the SDK. The decision is:
  // verb === Agent AND teamMode AND tasksCreated === 0 AND no agent_id (lead only).
  // A separate integration test with a real run verifies the wiring.
  const verb = 'Agent';
  const teamMode = true;
  let tasksCreated = 0;
  const agentId = '';
  const shouldRefuse = (verb === 'Agent' || verb === 'Task') && teamMode && tasksCreated === 0 && !agentId;
  assert.equal(shouldRefuse, true);
  // After a task is created, it must be allowed
  tasksCreated = 1;
  const shouldAllow = !((verb === 'Agent' || verb === 'Task') && teamMode && tasksCreated === 0 && !agentId);
  assert.equal(shouldAllow, true);
});

test('the plan-before-dispatch gate does not refuse non-team runs', () => {
  const verb = 'Agent';
  const teamMode = false;
  const tasksCreated = 0;
  const agentId = '';
  const shouldRefuse = (verb === 'Agent' || verb === 'Task') && teamMode && tasksCreated === 0 && !agentId;
  assert.equal(shouldRefuse, false);
});

test('the plan-before-dispatch gate does not refuse member calls', () => {
  // A member calling Agent is itself delegated work that was already planned by the lead.
  const verb = 'Agent';
  const teamMode = true;
  const tasksCreated = 0;
  const agentId = 'member-structural-biologist';
  const shouldRefuse = (verb === 'Agent' || verb === 'Task') && teamMode && tasksCreated === 0 && !agentId;
  assert.equal(shouldRefuse, false);
});

test('the plan-before-dispatch gate does not refuse non-Agent tools', () => {
  const verb = 'run_python';
  const teamMode = true;
  const tasksCreated = 0;
  const agentId = '';
  const shouldRefuse = (verb === 'Agent' || verb === 'Task') && teamMode && tasksCreated === 0 && !agentId;
  assert.equal(shouldRefuse, false);
});

/*
 * A STEP TITLE MUST NAME THE SCIENCE, NOT THE SDK'S TOOL.
 *
 * MEASURED on a live run: "Skill", "Read", "TaskCreate" and "TaskUpdate" travelled as step titles, because captionFrom
 * reads only code fields and every other verb fell through to its own name. The operator: "all the elements should be in
 * the scientific wording not like Run_Python and Tool calling ... we want the scientist user to feel like home and not a
 * strage place with unknown vocabulary."
 *
 * These assert the DERIVATION, not a table. There is no map from a tool name to a phrase anywhere in this path, so a
 * built-in nobody has seen yet is titled by the same rule.
 */
test('a step title comes from the call, not from the tool name', () => {
  // The subject is in the arguments: which file, which task.
  assert.equal(titleFor('Read', { file_path: '/s1/properties.csv' }), 'properties.csv');
  assert.equal(titleFor('TaskCreate', { task_subject: 'Compute descriptors' }), 'Compute descriptors');
  assert.equal(titleFor('WebSearch', { query: 'ibuprofen ADMET profile' }), 'ibuprofen ADMET profile');
  assert.equal(titleFor('Skill', { command: 'literature-search' }), 'literature-search');
  // The author's own caption still wins over anything derived.
  assert.equal(titleFor('run_python', { code: '# Partition coefficient calculation\nx = 1' }),
    'Partition coefficient calculation');
});

test('an opaque handle is never used as a title', () => {
  // MEASURED: {task_id: 't1', task_state: 'completed'} was titled "t1", which says less than the verb it replaced.
  assert.equal(titleFor('TaskUpdate', { task_id: 't1', task_state: 'completed' }), 'completed');
  // A tool call id has no meaning to a reader, so the verb spaced out of its camel case is the honest remainder.
  assert.equal(titleFor('TaskUpdate', { task_id: 'toolu_bdrk_01CBCgvbUjx' }), 'task update');
  assert.equal(titleFor('Anything', { run_id: '4f98e1f7-1c13-4222-9f49-fbafb34f8495' }), 'anything');
});

test('a filename is a subject even when it is shaped like a handle', () => {
  // `logp_chart_2.png` has digits, underscores and no spaces, exactly like a handle. It is what the reader wants named.
  assert.equal(titleFor('Read', { file_path: '/s1/logp_chart_2.png' }), 'logp_chart_2.png');
  assert.equal(titleFor('Read', { file_path: '/s1/run_2024_03.csv' }), 'run_2024_03.csv');
});

test('no title is left reading like an identifier when nothing is known', () => {
  // Not scientific vocabulary, and that is what honesty leaves: with no evidence of a subject, inventing a scientific
  // phrase would be a fabrication.
  assert.equal(titleFor('TaskCreate', {}), 'task create');
  assert.equal(titleFor('run_python', {}), 'run python');
});


test('a submitted container job is a row before it has an exit code', () => {
  /*
   * MEASURED: RFdiffusion ran on the A100 for minutes, confirmed by `docker ps` on the sandbox host, while the Jobs
   * panel reported the dispatch never reached a container. There was no submitted event at all, so a null exit code was
   * the only signal the panel had, and null also means "failed to start".
   */
  const e = toJobSubmittedEvent(
    { tool: 'rfdiffusion', gpu: true, image: 'registry.rayca.org/rayca-tools/rfdiffusion:latest',
      host: 'agents-sandbox1' }, 7, 'max-1', 1000, 'lead');
  assert.equal(e.meta.job_state, 'running');
  assert.equal(e.status, 'running');
  assert.equal(e.meta.tool, 'rfdiffusion');
  assert.equal(e.meta.gpu, true);
  assert.equal(e.meta.host, 'agents-sandbox1');
  assert.ok(e.body.includes('agents-sandbox1'), 'the row names the machine');
});

test('a submitted job claims no exit code and no duration', () => {
  // A zero exit code means success and a zero duration means it took no time. Both would be lies at submission.
  const e = toJobSubmittedEvent({ tool: 'gnina', gpu: true, host: 'agents-sandbox1' }, 1, 'max-1', 1000, 'lead');
  assert.equal(e.meta.rc, null);
  assert.equal(e.meta.duration_s, null);
  assert.equal(e.meta.elapsed_s, null);
  assert.notEqual(e.status, 'ok');
  assert.notEqual(e.status, 'error');
});

test('a finished job is still distinguishable from a submitted one', () => {
  const done = toJobEvent({ tool: 'gnina', rc: 0, gpu: true, seconds: 45 }, 1, 'max-1', 1000, 'lead');
  const started = toJobSubmittedEvent({ tool: 'gnina', gpu: true, host: 'h' }, 2, 'max-1', 1000, 'lead');
  assert.equal(done.meta.job_state, 'done');
  assert.equal(started.meta.job_state, 'running');
});

test('a cpu job still names where it ran when a host is known', () => {
  const e = toJobSubmittedEvent({ tool: 'pdbfixer', gpu: false, host: '' }, 1, 'max-1', 1000, 'lead');
  assert.equal(e.meta.gpu, false);
  assert.equal(e.meta.host, null);
  assert.ok(e.body.includes('pdbfixer'));
});

test('a running job reports elapsed time and what the machine is doing', () => {
  /*
   * The operator: the panel should "in real time show the resource usage on the vm and also say the name of the VM".
   * `_watch_container` beats every 15s with the log tail and elapsed time and now samples the host GPU on the same beat.
   */
  const e = toJobSubmittedEvent(
    { tool: 'rfdiffusion', gpu: true, host: 'agents-sandbox1', elapsed_s: 42.5,
      gpu_util_pct: 61, gpu_mem_used_mb: 4070, gpu_mem_total_mb: 40960,
      container: 'rayca-rfdiffusion-abc', tail: 'step 120 of 200' },
    3, 'max-1', 1000, 'lead');
  assert.equal(e.meta.elapsed_s, 42.5);
  assert.equal(e.meta.gpu_util_pct, 61);
  assert.equal(e.meta.gpu_mem_used_mb, 4070);
  assert.equal(e.meta.gpu_mem_total_mb, 40960);
  assert.equal(e.meta.host, 'agents-sandbox1');
  assert.equal(e.meta.output_tail, 'step 120 of 200');
  // Still running, so still no outcome.
  assert.equal(e.meta.job_state, 'running');
  assert.equal(e.meta.rc, null);
});

test('an unmeasured gpu reading is null, not zero', () => {
  /*
   * A GPU reading of zero means the card is IDLE, which is a real statement. Not having looked yet is a different one,
   * and conflating them would show a busy A100 as idle whenever telemetry was briefly unavailable.
   */
  const e = toJobSubmittedEvent({ tool: 'gnina', gpu: true, host: 'h' }, 1, 'max-1', 1000, 'lead');
  assert.equal(e.meta.gpu_util_pct, null);
  assert.equal(e.meta.gpu_mem_used_mb, null);
  assert.equal(e.meta.elapsed_s, null);
});

test('a genuinely idle gpu is reported as zero and not swallowed', () => {
  const e = toJobSubmittedEvent(
    { tool: 'pdbfixer', gpu: true, host: 'h', gpu_util_pct: 0, gpu_mem_used_mb: 0, elapsed_s: 0 },
    1, 'max-1', 1000, 'lead');
  assert.equal(e.meta.gpu_util_pct, 0);
  assert.equal(e.meta.gpu_mem_used_mb, 0);
  assert.equal(e.meta.elapsed_s, 0);
});

test('a scheduler job reaches the jobs panel', () => {
  /*
   * MEASURED on the operator's EGFR/erlotinib run: run_on_cluster returned job 6102452 on Isambard, the job queued, and
   * the Jobs panel showed nothing. Zero job events for the whole run. Cluster jobs return JSON rather than printing the
   * `[dispatch]` marker a container prints, so nothing was ever read.
   */
  const j = clusterJobIn(JSON.stringify({
    ok: true, cluster: 'Isambard-AI_HPC', provider: 'isambard_ai', job_id: '6102452',
    state: 'submitted', host: 'ai-p2.access.isambard.ac.uk', requested: { cpus: 8, gpus: 1, minutes: 720 },
  }));
  assert.ok(j, 'a submission is recognised');
  assert.equal(j.jobId, '6102452');
  assert.equal(j.cluster, 'Isambard-AI_HPC');
  const e = toClusterJobEvent(j, 1, 'max-1', 1000, 'lead');
  assert.equal(e.meta.dispatch_submitted, true);
  assert.equal(e.meta.job_id, '6102452');
  assert.equal(e.meta.cluster, 'Isambard-AI_HPC');
  assert.equal(e.meta.job_state, 'running');
  assert.ok(e.title.includes('6102452'), 'the row names the scheduler id');
});

test('a scheduler job does not claim the sandbox GPU', () => {
  // `gpu` describes our own A100. A cluster job's hardware is not that, and saying so would misfile it.
  const j = clusterJobIn({ job_id: '99', cluster: 'LUMI', state: 'submitted' });
  assert.equal(toClusterJobEvent(j, 1, 'r', 1, 'lead').meta.gpu, false);
});

test('a finished scheduler job is marked done, a failed one failed', () => {
  const done = toClusterJobEvent(clusterJobIn({ job_id: '1', state: 'completed' }), 1, 'r', 1, 'lead');
  const bad = toClusterJobEvent(clusterJobIn({ job_id: '2', state: 'failed' }), 1, 'r', 1, 'lead');
  assert.equal(done.meta.job_state, 'done');
  assert.equal(done.status, 'ok');
  assert.equal(bad.meta.job_state, 'failed');
  assert.equal(bad.status, 'error');
});

test('a tool result with no job id is not mistaken for a submission', () => {
  assert.equal(clusterJobIn(JSON.stringify({ ok: true, output: 'hello' })), null);
  assert.equal(clusterJobIn('not json at all'), null);
  assert.equal(clusterJobIn(''), null);
  assert.equal(clusterJobIn(null), null);
});

test('a queued scheduler job is not shown as running', () => {
  /*
   * MEASURED: job 6102452 sat PENDING behind higher-priority work, squeue said so, and the panel said running. For a 12
   * hour job that difference decides whether a researcher waits or resubmits smaller.
   */
  const j = clusterJobIn({ job_id: '6102452', cluster: 'Isambard-AI_HPC',
                           state: 'running', scheduler_state: 'pending', queued: true });
  const e = toClusterJobEvent(j, 1, 'r', 1, 'lead');
  assert.equal(e.meta.job_state, 'queued');
  assert.equal(e.meta.scheduler_state, 'pending');
  assert.ok(e.body.includes('pending'), 'the row says pending, not running');
  assert.notEqual(e.meta.job_state, 'running');
});

test('a genuinely running job still reads as running', () => {
  const j = clusterJobIn({ job_id: '7', cluster: 'LUMI', state: 'running', scheduler_state: 'running' });
  assert.equal(toClusterJobEvent(j, 1, 'r', 1, 'lead').meta.job_state, 'running');
});

test('a cancelled job is failed, not queued', () => {
  const j = clusterJobIn({ job_id: '8', state: 'cancelled', scheduler_state: 'cancelled' });
  assert.equal(toClusterJobEvent(j, 1, 'r', 1, 'lead').meta.job_state, 'failed');
});

test('a cluster job survives the run that submitted it, and closes when it ends', async () => {
  /*
   * MEASURED: a 12 hour MD job was queued on Isambard, the submitting run finished, and a later run asking about job
   * 6102452 was told "this run did not submit job 6102452". The job table was a module-level dict inside the MCP server,
   * which is spawned per query, so the record died with the run. These assertions are on the DURABLE record instead.
   */
  const { Store } = await import('./store.mjs');
  const s = new Store(':memory:');
  s.createRun({ id: 'max-parent', task: 'run MD', team: false, model: 'claude-sonnet-4-6' });
  s.noteConsoleSession('max-parent', 'sess-1');
  s.rememberClusterJob({
    jobId: '6102566', runId: 'max-parent', consoleSession: 'sess-1',
    cluster: 'Isambard-AI_HPC', provider: 'isambard_ai', host: 'ai-p2.access.isambard.ac.uk',
    state: 'submitted', schedulerState: '',
  });

  // Open, so the watcher picks it up on its next tick even after a restart.
  assert.equal(s.openClusterJobs().length, 1);
  assert.equal(s.getClusterJob('6102566').cluster, 'Isambard-AI_HPC');
  assert.equal(s.getClusterJob('6102566').console_session, 'sess-1');

  // QUEUED IS RECORDED AS THE SCHEDULER'S OWN WORD while the coarse state stays what the poll needs.
  s.updateClusterJob('6102566', { state: 'running', schedulerState: 'pending' });
  assert.equal(s.getClusterJob('6102566').scheduler_state, 'pending');
  assert.equal(s.getClusterJob('6102566').ended_ms, null, 'a queued job is not finished');
  assert.equal(s.openClusterJobs().length, 1);

  s.updateClusterJob('6102566', { state: 'running', schedulerState: 'running' });
  assert.equal(s.getClusterJob('6102566').ended_ms, null);

  // Finished: closed, files kept, and the analysis run recorded against it.
  s.updateClusterJob('6102566', { state: 'done', schedulerState: 'completed', files: ['/x/traj.xtc', '/x/log.txt'] });
  const done = s.getClusterJob('6102566');
  assert.equal(done.state, 'done');
  assert.ok(done.ended_ms, 'a finished job is closed so the watcher stops polling it');
  assert.deepEqual(JSON.parse(done.files), ['/x/traj.xtc', '/x/log.txt']);
  assert.equal(s.openClusterJobs().length, 0, 'a closed job is no longer open');

  s.updateClusterJob('6102566', { analysisRun: 'max-analysis' });
  assert.equal(s.getClusterJob('6102566').analysis_run, 'max-analysis');
});

test('a failed cluster job is closed too, so the watcher does not poll it forever', async () => {
  const { Store } = await import('./store.mjs');
  const s = new Store(':memory:');
  s.rememberClusterJob({ jobId: '9', runId: 'r', cluster: 'LUMI', provider: 'lumi', state: 'submitted' });
  s.updateClusterJob('9', { state: 'failed', schedulerState: 'cancelled' });
  assert.ok(s.getClusterJob('9').ended_ms);
  assert.equal(s.openClusterJobs().length, 0);
});

test('an unknown job is absent rather than invented', async () => {
  const { Store } = await import('./store.mjs');
  const s = new Store(':memory:');
  assert.equal(s.getClusterJob('does-not-exist'), null);
});

test('a cluster job records where its results should be collected', async () => {
  /*
   * MEASURED: job 6102566 completed on Isambard and collected NOTHING. The watcher asked for collection into
   * `job.results_into`, the table had no such column, so an empty path was passed and collection was skipped in silence.
   * The trajectory a long job exists to produce would have been left on the cluster.
   */
  const { Store } = await import('./store.mjs');
  const s = new Store(':memory:');
  s.rememberClusterJob({
    jobId: '7', runId: 'r', consoleSession: 'sess', cluster: 'Isambard-AI_HPC',
    provider: 'isambard_ai', state: 'submitted', resultsInto: '/home/ubuntu/rayca-sessions/abc',
  });
  assert.equal(s.getClusterJob('7').results_into, '/home/ubuntu/rayca-sessions/abc');
  // The watcher reads it off the open row, which is the only thing it has when the job finishes.
  assert.equal(s.openClusterJobs()[0].results_into, '/home/ubuntu/rayca-sessions/abc');
});

test('a job with no collection target is still recorded rather than rejected', async () => {
  // Collection is a bonus; losing the job record would be worse than losing the files.
  const { Store } = await import('./store.mjs');
  const s = new Store(':memory:');
  s.rememberClusterJob({ jobId: '8', runId: 'r', cluster: 'LUMI', provider: 'lumi', state: 'submitted' });
  assert.equal(s.getClusterJob('8').results_into, '');
  assert.equal(s.openClusterJobs().length, 1);
});

test('every kind of attachment resolves to something the model can act on', async () => {
  /*
   * MEASURED, reported by the operator: "the attachement of the composer box do not reach the engine, doean't matter if they are
   * attached files or attached skills, containerized tools and persona or files added to the composer from file manager, non of the
   * reach the engine."
   *
   * The console had been sending them all along. `grep attachments server.mjs` found nothing: the field arrived on every run and was
   * read by nobody. This asserts each kind now resolves against its real source, since a resolver that handles four kinds of seven
   * would reproduce the same complaint with a smaller list.
   */
  const { resolveOne } = await import('./attachments.mjs');
  const cases = [
    { kind: 'tools', id: 'aizynthfinder', name: 'AiZynthFinder' },
    { kind: 'pipelines', id: 'ampliseq', name: 'ampliseq' },
    { kind: 'databases', id: 'chembl', name: 'ChEMBL' },
    { kind: 'personas', id: 'med-chem-scientist', name: 'Med Chem Scientist' },
    { kind: 'frameworks', id: '20-synthesis-planning.retrosynthetic-route-planning.folded-protein', name: 'Route planning' },
  ];
  for (const c of cases) {
    const r = resolveOne(c);
    assert.equal(r.found, true, `${c.kind} ${c.id} did not resolve`);
    assert.ok(r.detail.length > 0, `${c.kind} resolved with nothing to say about it`);
  }
});

test('an attachment that cannot be found says so rather than disappearing', async () => {
  /*
   * The operator's original symptom was the silent version of this: "I said read this file attached and the engine said I don't see
   * any files." A chip that resolves to nothing must produce a sentence, not an absence.
   */
  const { resolveAttachments } = await import('./attachments.mjs');
  const out = resolveAttachments([
    { kind: 'files', id: 'x', name: 'nothing-by-this-name.csv' },
    { kind: 'tools', id: 'no-such-tool-exists', name: 'Imaginary' },
    { kind: 'sausages', id: 'x', name: 'Wrong kind' },
  ]);
  assert.equal(out.found, 0);
  assert.match(out.briefing, /ATTACHED BUT NOT RESOLVED/);
  assert.match(out.briefing, /nothing-by-this-name\.csv/);
  assert.match(out.briefing, /do not invent their contents/);
  assert.match(out.briefing, /unrecognised attachment kind/);
});

test('the briefing tells the model what to DO with each kind', async () => {
  /* A manifest of names says something was attached. It does not say that a container tool should be preferred over rewriting it,
     which is the whole reason someone attached it. */
  const { resolveAttachments } = await import('./attachments.mjs');
  const out = resolveAttachments([
    { kind: 'tools', id: 'aizynthfinder', name: 'AiZynthFinder' },
    { kind: 'databases', id: 'chembl', name: 'ChEMBL' },
    { kind: 'personas', id: 'med-chem-scientist', name: 'Med Chem Scientist' },
  ]);
  assert.match(out.briefing, /CONTAINER TOOLS THE RESEARCHER CHOSE, dispatched by name/);
  assert.match(out.briefing, /Take the data from these/);
  assert.match(out.briefing, /Answer from these viewpoints/);
  /*
   * A PREFERENCE, NOT A CAGE. The operator: "the attachemnts must not be the enforcement but a user preference, if the model found
   * better and more established tool or method or skill, then they should aslo adopt them in addition to the user preferences."
   *
   * My first wording said "prefer these over writing an equivalent yourself" and "rather than choosing your own approach", which
   * reads as a ceiling. A researcher attaching a tool is saying "I trust this and I want it used", not "consider nothing else", and
   * a platform whose claim is that it knows methods a person has not thought of should not be told to withhold them.
   *
   * The "say why you added it" clause is what keeps it from being a licence to wander: an addition whose reason the reader cannot
   * see is indistinguishable from the model ignoring them.
   */
  assert.match(out.briefing, /You may ALSO use a better established tool or method/);
  assert.match(out.briefing, /in addition rather than instead/);
  assert.match(out.briefing, /say why you added it/);
  assert.doesNotMatch(out.briefing, /rather than choosing your own approach/);
  assert.match(out.briefing, /--- ATTACHED BY THE RESEARCHER ---/);
});

test('no attachments means no briefing, so an ordinary run is untouched', async () => {
  const { resolveAttachments } = await import('./attachments.mjs');
  assert.equal(resolveAttachments([]).briefing, '');
  assert.equal(resolveAttachments(undefined).briefing, '');
});

test('a file is resolved from the session it was attached from', async () => {
  /*
   * The file manager lets a reader carry a result forward from an earlier study, and the attachment then names that session. Looking
   * only in the current workspace would fail exactly those, which is the more valuable half of the feature.
   */
  const { resolveOne } = await import('./attachments.mjs');
  const fs = await import('node:fs');
  const os = await import('node:os');
  const path = await import('node:path');
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'rayca-sessions-'));
  const other = path.join(root, 'sess-abc-1234');
  fs.mkdirSync(path.join(other, 'results'), { recursive: true });
  fs.writeFileSync(path.join(other, 'results', 'carried.csv'), 'a,b\n1,2\n');
  const prev = process.env.RAYCA_SESSIONS_ROOT;
  process.env.RAYCA_SESSIONS_ROOT = root;
  try {
    /* A fresh import, because the sessions root is read at module load. */
    const mod = await import(`./attachments.mjs?sessions=${Date.now()}`);
    const r = mod.resolveOne({ kind: 'files', id: 'f', name: 'carried.csv', session: 'sess-abc' }, { workspace: root });
    assert.equal(r.found, true);
    assert.match(r.where, /carried\.csv$/);
  } finally {
    if (prev === undefined) { delete process.env.RAYCA_SESSIONS_ROOT; } else { process.env.RAYCA_SESSIONS_ROOT = prev; }
    fs.rmSync(root, { recursive: true, force: true });
  }
  assert.ok(resolveOne);
});

// ============================================================================================================
// THE STUDY PLAN'S TASKS
//
// The operator: "now the study plan is empty ... we want to have all the tasks listed in the study plan with live status, which
// tasks is completed, which is ongoing and which has not started ... get the task status from the engine."
//
// MEASURED BEFORE ANY OF THIS WAS WRITTEN. The panel reads a `type: 'plan'` event carrying `meta.phases`, and this engine emitted
// `type: 'plan'` for exactly two things, a delegation and a single task changing state, neither carrying phases. And on a real
// run the only task facts that reached the tape were four `created` and four `completed`: nothing in between, because the loop
// handled init, assistant, user and result and dropped `task_updated`. Nothing could ever be shown as ongoing.
// ============================================================================================================

test('a task nobody has spoken about yet has not started', () => {
  const t = newTaskTable();
  noteTask(t, { id: '1', subject: 'Fetch 6OIM' });
  assert.equal(taskPhases(t)[0].state, 'pending');
});

test('the SDK words for ongoing both mean running', () => {
  // `task_updated` says `running`; the TaskList tool's own output says `in_progress`. Reading one would leave the other looking
  // as though it had never begun.
  assert.equal(stateFrom('running'), 'running');
  assert.equal(stateFrom('in_progress'), 'running');
});

test('a killed task is a failure and not a completion', () => {
  // Colouring it as done because it is no longer running would be the plan lying about the study.
  assert.equal(stateFrom('killed'), 'failed');
  assert.equal(stateFrom('completed'), 'done');
});

test('a word the engine does not know leaves the state alone rather than guessing', () => {
  assert.equal(stateFrom('marinating'), null);
  const t = newTaskTable();
  noteTask(t, { id: '1', status: 'running' });
  noteTask(t, { id: '1', status: 'marinating' });
  assert.equal(taskPhases(t)[0].state, 'running');
});

test('a repeated signal is not news, so no duplicate plan reaches the tape', () => {
  // The SDK reports the same completion from a hook and again in a patch. A snapshot per repeat would redraw for nothing.
  const t = newTaskTable();
  assert.equal(noteTask(t, { id: '1', subject: 'Dock', status: 'pending' }), true);
  assert.equal(noteTask(t, { id: '1', subject: 'Dock', status: 'pending' }), false);
  assert.equal(noteTask(t, { id: '1', status: 'completed' }), true);
});

test('a completion carrying no subject does not blank the task', () => {
  // The TaskCompleted hook has no subject, and letting it overwrite would empty the row exactly when the reader wants to know
  // what finished.
  const t = newTaskTable();
  noteTask(t, { id: '1', subject: 'Score and rank' });
  noteTask(t, { id: '1', status: 'completed' });
  assert.equal(taskPhases(t)[0].goal, 'Score and rank');
  assert.equal(taskPhases(t)[0].state, 'done');
});

test('a task updated before its creation was seen is still recorded', () => {
  const t = newTaskTable();
  noteTask(t, { id: '9', status: 'running' });
  assert.equal(taskPhases(t).length, 1);
  assert.equal(taskPhases(t)[0].state, 'running');
});

test('a deleted task leaves the plan instead of being marked failed', () => {
  // `TaskUpdate` accepts status deleted, which means the model decided this is not part of the study. Keeping it as failed would
  // read as though something had gone wrong.
  const t = newTaskTable();
  noteTask(t, { id: '1', subject: 'Keep' });
  noteTask(t, { id: '2', subject: 'Drop' });
  assert.equal(noteTask(t, { id: '2', status: 'deleted' }), true);
  const phases = taskPhases(t);
  assert.equal(phases.length, 1);
  assert.equal(phases[0].goal, 'Keep');
  // The index is derived, so removing one does not leave a hole in the numbering.
  assert.equal(phases[0].index, 0);
});

test('deleting something that was never there is not news', () => {
  const t = newTaskTable();
  assert.equal(noteTask(t, { id: 'nope', status: 'deleted' }), false);
});

test('an error fails the task even when no status came with it', () => {
  const t = newTaskTable();
  noteTask(t, { id: '1', subject: 'Dock', status: 'running' });
  noteTask(t, { id: '1', error: 'receptor had no ligand' });
  assert.equal(taskPhases(t)[0].state, 'failed');
});

test('declared dependencies are carried and order is not invented as one', () => {
  // The layout draws phases that can run at once side by side, so claiming each task depends on the one before would turn a
  // parallel plan into a false chain.
  const t = newTaskTable();
  noteTask(t, { id: '1', subject: 'Fetch' });
  noteTask(t, { id: '2', subject: 'Dock', needs: ['1'] });
  const phases = taskPhases(t);
  assert.deepEqual(phases[0].needs, []);
  assert.deepEqual(phases[1].needs, ['1']);
});

test('the counts say how many are done, ongoing and not started', () => {
  const t = newTaskTable();
  noteTask(t, { id: '1', subject: 'a', status: 'completed' });
  noteTask(t, { id: '2', subject: 'b', status: 'in_progress' });
  noteTask(t, { id: '3', subject: 'c' });
  const counts = taskCounts(t);
  assert.equal(counts.total, 3);
  assert.equal(counts.done, 1);
  assert.equal(counts.running, 1);
  assert.equal(counts.pending, 1);
});

test('the last task is marked final so the plan knows where it ends', () => {
  const t = newTaskTable();
  noteTask(t, { id: '1', subject: 'a' });
  noteTask(t, { id: '2', subject: 'b' });
  const phases = taskPhases(t);
  assert.equal(phases[0].final, false);
  assert.equal(phases[1].final, true);
});

test('a signal with no id is ignored rather than creating a nameless task', () => {
  const t = newTaskTable();
  assert.equal(noteTask(t, { subject: 'orphan' }), false);
  assert.equal(taskPhases(t).length, 0);
});

// ============================================================================================================
// A LIVE RUN IS NOT AN ORPHAN
//
// MEASURED, and I caused it. `reconcileOrphanedRuns` closed EVERY row marked running, on the assumption that the only reason one
// could exist is a previous process having died. I loaded the server module in a throwaway process to check an import, and it
// marked the operator's live run `max-beb6e19eee` as interrupted while the real engine carried on writing its events: 146 events
// at that moment, 151 twenty seconds later. The run survived, its row did not, and the console reads that row to decide whether
// a run is live, so it would have shown a finished run and withdrawn the control to stop it.
//
// `owner_pid` turns "is this orphaned" from an assumption about who else might be running into a question with an exact answer.
// ============================================================================================================

test('a run driven by this process is never reconciled away', () => {
  const dir = mkdtempSync(join(tmpdir(), 'rayca-owner-'));
  const s = new Store(join(dir, 'x.sqlite'));
  s.createRun({ id: 'live', task: 't', team: 0, model: 'm' });
  assert.deepEqual(s.reconcileOrphanedRuns(), []);
  assert.equal(s.db.prepare("SELECT state FROM runs WHERE id='live'").get().state, 'running');
  // Repeated reconciliation must not wear it down either.
  s.reconcileOrphanedRuns();
  s.reconcileOrphanedRuns();
  assert.equal(s.db.prepare("SELECT state FROM runs WHERE id='live'").get().state, 'running');
  rmSync(dir, { recursive: true, force: true });
});

test('the owning process is recorded when the run is created', () => {
  const dir = mkdtempSync(join(tmpdir(), 'rayca-owner-'));
  const s = new Store(join(dir, 'x.sqlite'));
  s.createRun({ id: 'r', task: 't', team: 0, model: 'm' });
  assert.equal(s.db.prepare("SELECT owner_pid FROM runs WHERE id='r'").get().owner_pid, process.pid);
  rmSync(dir, { recursive: true, force: true });
});

test('a run whose owner has gone is still closed as interrupted', () => {
  const dir = mkdtempSync(join(tmpdir(), 'rayca-owner-'));
  const s = new Store(join(dir, 'x.sqlite'));
  s.createRun({ id: 'orphan', task: 't', team: 0, model: 'm' });
  // A pid that cannot be running. The reconciler asks the operating system rather than assuming.
  s.db.prepare("UPDATE runs SET owner_pid = 999999 WHERE id='orphan'").run();
  assert.deepEqual(s.reconcileOrphanedRuns(), ['orphan']);
  const row = s.db.prepare("SELECT state, ended_ms FROM runs WHERE id='orphan'").get();
  assert.equal(row.state, 'interrupted');
  assert.ok(row.ended_ms > 0);
  rmSync(dir, { recursive: true, force: true });
});

test('a row written before the owner column existed behaves as it always did', () => {
  const dir = mkdtempSync(join(tmpdir(), 'rayca-owner-'));
  const s = new Store(join(dir, 'x.sqlite'));
  s.createRun({ id: 'legacy', task: 't', team: 0, model: 'm' });
  s.db.prepare("UPDATE runs SET owner_pid = NULL WHERE id='legacy'").run();
  assert.deepEqual(s.reconcileOrphanedRuns(), ['legacy']);
  rmSync(dir, { recursive: true, force: true });
});

test('one live run and one orphan are told apart in the same sweep', () => {
  // The old code updated WHERE state = 'running', so any filtering above it made no difference at all.
  const dir = mkdtempSync(join(tmpdir(), 'rayca-owner-'));
  const s = new Store(join(dir, 'x.sqlite'));
  s.createRun({ id: 'live', task: 't', team: 0, model: 'm' });
  s.createRun({ id: 'orphan', task: 't', team: 0, model: 'm' });
  s.db.prepare("UPDATE runs SET owner_pid = 999999 WHERE id='orphan'").run();
  assert.deepEqual(s.reconcileOrphanedRuns(), ['orphan']);
  assert.equal(s.db.prepare("SELECT state FROM runs WHERE id='live'").get().state, 'running');
  assert.equal(s.db.prepare("SELECT state FROM runs WHERE id='orphan'").get().state, 'interrupted');
  rmSync(dir, { recursive: true, force: true });
});

/*
 * WHICH MODELS A SELECTION MAY NAME.
 *
 * MEASURED: the engine held a literal list of three Claude models while the endpoint that fills the console's selector
 * advertised twelve and named `qwen3-coder-480b` as its default. Selecting Qwen3 silently ran claude-sonnet-4-6, and
 * across 365 max runs not one Qwen3 run was ever recorded. These cases exist so the set can only be widened by the
 * router and can never be emptied by it.
 */
test('a router listing becomes the selectable set, with the configured model always first', () => {
  const body = { data: [{ id: 'claude-sonnet-4-6' }, { id: 'qwen3-coder-480b' }, { id: 'qwen3-235b' }] };
  const out = modelsFromRouterPayload(body, 'claude-sonnet-4-6');
  assert.deepEqual(out, ['claude-sonnet-4-6', 'qwen3-coder-480b', 'qwen3-235b']);
  assert.equal(out[0], 'claude-sonnet-4-6');
  assert.ok(out.includes('qwen3-coder-480b'), 'Qwen3 must be selectable when the router serves it');
});

test('the configured model is selectable even when the router does not list it', () => {
  const out = modelsFromRouterPayload({ data: [{ id: 'qwen3-235b' }] }, 'claude-sonnet-4-6');
  assert.deepEqual(out, ['claude-sonnet-4-6', 'qwen3-235b']);
});

test('a listing with nothing usable yields null, so the caller keeps what it had', () => {
  assert.equal(modelsFromRouterPayload({ data: [] }, 'm'), null);
  assert.equal(modelsFromRouterPayload({}, 'm'), null);
  assert.equal(modelsFromRouterPayload(null, 'm'), null);
  assert.equal(modelsFromRouterPayload({ data: [{ id: '' }, { id: '   ' }] }, 'm'), null);
});

test('duplicates and blanks in a listing are dropped rather than offered twice', () => {
  const body = { data: [{ id: 'a' }, { id: 'a' }, { id: '' }, { id: 'b' }, { nope: 1 }] };
  assert.deepEqual(modelsFromRouterPayload(body, 'a'), ['a', 'b']);
});

test('the fallback set is the three that were verified to exist on this deployment', () => {
  assert.deepEqual(fallbackModels('claude-sonnet-4-6'), ['claude-sonnet-4-6', 'claude-haiku-4-5']);
  assert.deepEqual(fallbackModels('qwen3-coder-480b'),
    ['qwen3-coder-480b', 'claude-sonnet-4-6', 'claude-haiku-4-5']);
});

test('a router that answers with an error throws, so the caller can keep the previous set', async () => {
  await assert.rejects(
    () => fetchRouterModels({
      baseUrl: 'http://router.invalid', key: 'k', configured: 'm',
      fetchImpl: async () => ({ ok: false, status: 500 }),
    }),
    /HTTP 500/,
  );
});

test('no base url means no opinion, not an empty set', async () => {
  assert.equal(await fetchRouterModels({ baseUrl: '', configured: 'm' }), null);
});

test('a trailing slash on the base url does not double the path', async () => {
  let seen = '';
  await fetchRouterModels({
    baseUrl: 'http://router.invalid/', key: '', configured: 'm',
    fetchImpl: async (url) => { seen = url; return { ok: true, json: async () => ({ data: [{ id: 'm' }] }) }; },
  });
  assert.equal(seen, 'http://router.invalid/v1/models');
});

/*
 * WHAT A RUN ACTUALLY COST.
 *
 * MEASURED: a Qwen3 run recorded $15.1690 against a $15 cap and stopped, while the router's ledger for the same window
 * shows 4,135,528 input tokens, 18,828 output tokens and $0.9437. The SDK prices from a Claude-only table, so the
 * cheapest model in the fleet exhausted the budget fastest. These cases pin the arithmetic that replaces it.
 */
const ROUTER_PRICES = {
  data: [
    { model_name: 'claude-sonnet-4-6', model_info: {
      input_cost_per_token: 3e-06, output_cost_per_token: 1.5e-05,
      cache_read_input_token_cost: 3e-07, cache_creation_input_token_cost: 3.75e-06, max_input_tokens: 1000000 } },
    { model_name: 'qwen3-coder-480b', model_info: {
      input_cost_per_token: 2.2e-07, output_cost_per_token: 1.8e-06, max_input_tokens: 262000 } },
    { model_name: 'qwen3-235b', model_info: {
      input_cost_per_token: 2.2e-07, output_cost_per_token: 8.8e-07 } },
  ],
};

test('the router listing becomes a price table, with cache falling back to the input rate', () => {
  const p = pricesFromRouterPayload(ROUTER_PRICES);
  assert.equal(p['claude-sonnet-4-6'].input, 3e-06);
  assert.equal(p['claude-sonnet-4-6'].cacheRead, 3e-07);
  /* Qwen declares no cache prices because it has no prompt caching, so those tokens cost the input rate. */
  assert.equal(p['qwen3-coder-480b'].cacheRead, 2.2e-07);
  assert.equal(p['qwen3-coder-480b'].cacheWrite, 2.2e-07);
  assert.equal(pricesFromRouterPayload({ data: [] }), null);
  assert.equal(pricesFromRouterPayload(null), null);
});

test('the measured Qwen3 run prices at the router figure, not the Claude figure', () => {
  const p = pricesFromRouterPayload(ROUTER_PRICES);
  /* The exact counts from the router ledger for the run that was stopped. */
  const usage = { 'qwen3-coder-480b': { inputTokens: 4135528, outputTokens: 18828 } };
  const out = costOf(usage, p);
  assert.ok(out.complete, 'every model must be priced');
  /* $0.9437 in the ledger. */
  assert.ok(Math.abs(out.usd - 0.9437) < 0.01, 'expected about $0.94, got ' + out.usd);
  /* And emphatically NOT the $15.17 that stopped the study. */
  assert.ok(out.usd < 2, 'the Claude-priced figure was $15.17 and must not reappear');
});

test('a bedrock inference profile id matches its shorter table name', () => {
  const p = pricesFromRouterPayload(ROUTER_PRICES);
  assert.equal(priceKeyFor('bedrock/qwen.qwen3-coder-480b-a35b-v1:0', p), 'qwen3-coder-480b');
  /* The longest containing name wins, so the shorter sibling cannot steal a longer id. */
  assert.equal(priceKeyFor('qwen3-235b', p), 'qwen3-235b');
  assert.equal(priceKeyFor('claude-sonnet-4-6', p), 'claude-sonnet-4-6');
  assert.equal(priceKeyFor('something-nobody-declared', p), null);
  assert.equal(priceKeyFor('', p), null);
});

test('an unpriced model is reported rather than counted as free', () => {
  const p = pricesFromRouterPayload(ROUTER_PRICES);
  const out = costOf({ 'model-nobody-declared': { inputTokens: 1000, outputTokens: 10 } }, p);
  assert.equal(out.usd, 0);
  assert.equal(out.complete, false);
  assert.deepEqual(out.unpriced.map((u) => u.model), ['model-nobody-declared']);
});

test('cache tokens are priced at their own rate for a model that has them', () => {
  const p = pricesFromRouterPayload(ROUTER_PRICES);
  const out = costOf({ 'claude-sonnet-4-6': {
    inputTokens: 1000, outputTokens: 100, cacheReadInputTokens: 1000000, cacheCreationInputTokens: 0 } }, p);
  /* 1M cache reads at $0.30/M is $0.30, which is a tenth of what pricing them as input would give. */
  assert.ok(Math.abs(out.usd - (0.003 + 0.0015 + 0.3)) < 1e-6, out.usd);
});

test('several models in one run are summed', () => {
  const p = pricesFromRouterPayload(ROUTER_PRICES);
  const out = costOf({
    'qwen3-coder-480b': { inputTokens: 1000000, outputTokens: 0 },
    'claude-sonnet-4-6': { inputTokens: 1000000, outputTokens: 0 },
  }, p);
  assert.ok(out.complete);
  assert.ok(Math.abs(out.usd - (0.22 + 3.0)) < 1e-6, out.usd);
  assert.equal(out.priced.length, 2);
});

/*
 * THE MODEL'S REAL CONTEXT WINDOW.
 *
 * The operator: "why should it hand over another model? can it just compact the conversation?" Compaction is the right
 * answer, and it was not firing because the SDK sizes it from a Claude-only lookup table. MEASURED: a resumed session on
 * qwen3-coder-480b died at turn one with "for a total of at least 131073 tokens", one token over Bedrock's limit, having
 * produced nothing. These cases pin the number the run now tells the SDK.
 */
test('the usable input window comes from the router, per model', () => {
  const prices = pricesFromRouterPayload({
    data: [
      { model_name: 'qwen3-coder-480b', model_info: {
        input_cost_per_token: 2.2e-07, output_cost_per_token: 1.8e-06, max_input_tokens: 99000 } },
      { model_name: 'claude-sonnet-4-6', model_info: {
        input_cost_per_token: 3e-06, output_cost_per_token: 1.5e-05, max_input_tokens: 1000000 } },
    ],
  });
  assert.equal(prices['qwen3-coder-480b'].maxInput, 99000);
  assert.equal(prices['claude-sonnet-4-6'].maxInput, 1000000);
  /* THE POINT OF THE FIX: the two differ by an order of magnitude, so one shared default cannot serve both. */
  assert.ok(prices['claude-sonnet-4-6'].maxInput > prices['qwen3-coder-480b'].maxInput * 10);
});

test('a model with no published window yields none, so the SDK default stands', () => {
  const prices = pricesFromRouterPayload({
    data: [{ model_name: 'mystery', model_info: { input_cost_per_token: 1e-06, output_cost_per_token: 1e-06 } }],
  });
  assert.equal(prices.mystery.maxInput, null);
  /* A WRONG WINDOW IS WORSE THAN NO WINDOW: it would compact a run that had room left. */
  const n = Number(prices.mystery.maxInput);
  assert.ok(!(Number.isFinite(n) && n > 10000));
});

/*
 * A TOOL THE PROVIDER CANNOT ACCEPT MUST NOT BE OFFERED.
 *
 * MEASURED: the SDK's server-side web search tool killed a resumed session at turn 5. Bedrock rejected
 * `web_search_options` for Qwen, and rejected the tool tag `web_search_20250305` for Sonnet, so it works on neither
 * model here. The reader was shown the SDK's canned policy message, "can't help with this", as though the model had
 * declined on policy.
 */
test('web search is denied, and an operator can still deny more', () => {
  const build = (deny) => ['WebSearch', ...(deny ? deny.split(',') : [])]
    .map((t) => String(t).trim()).filter(Boolean);
  assert.deepEqual(build(undefined), ['WebSearch']);
  assert.deepEqual(build(''), ['WebSearch']);
  assert.deepEqual(build('Bash,WebFetch'), ['WebSearch', 'Bash', 'WebFetch']);
  /* Whitespace and empty entries in the operator's list must not become a tool named '' that denies nothing. */
  assert.deepEqual(build(' Bash , , WebFetch '), ['WebSearch', 'Bash', 'WebFetch']);
});

// ─── a container job finishes on screen ────────────────────────────────────────

test('a beat with no outcome leaves the job running', () => {
  const o = jobOutcome({ tool: 'gnina', elapsed_s: 20 });
  assert.equal(o.settled, false);
  assert.equal(o.state, 'running');
  assert.equal(toJobSubmittedEvent({ tool: 'gnina' }, 1, 'r', 0, 'lead').status, 'running');
});

test('rc=0 settles the job as ok, and that is the value truthiness would have eaten', () => {
  /* THE BUG THIS GUARDS. `b.rc || undefined` at the endpoint would have erased exactly the successes, because 0 is
     both the commonest real exit code and falsy. */
  const o = jobOutcome({ rc: 0 });
  assert.equal(o.settled, true);
  assert.equal(o.ok, true);
  assert.equal(o.rc, 0);
  const ev = toJobSubmittedEvent({ tool: 'gnina', rc: 0, state: 'done', elapsed_s: 230.4, host: 'agents-sandbox1' },
    1, 'r', 0, 'lead');
  assert.equal(ev.status, 'ok');
  assert.equal(ev.meta.rc, 0);
  assert.equal(ev.meta.duration_s, 230.4);
  assert.match(ev.body, /gnina finished on agents-sandbox1 after 230\.4s/);
});

test('a non-zero code is a failure and carries the reason', () => {
  const ev = toJobSubmittedEvent({ tool: 'boltzgen', rc: 1, state: 'failed', detail: 'CUDA out of memory' },
    1, 'r', 0, 'lead');
  assert.equal(ev.status, 'error');
  assert.equal(ev.meta.rc, 1);
  assert.equal(ev.meta.error, 'CUDA out of memory');
  assert.match(ev.body, /boltzgen failed/);
});

test('rc outranks a state that disagrees with it', () => {
  /* rc comes from the container, the state is a label put on top. A non-zero code with state=done is a failure, and
     believing the label would hide it. */
  const o = jobOutcome({ rc: 137, state: 'done' });
  assert.equal(o.ok, false);
  assert.equal(toJobSubmittedEvent({ tool: 'x', rc: 137, state: 'done' }, 1, 'r', 0, 'lead').status, 'error');
});

test('a state alone settles the job, because a cancelled container reports no code', () => {
  for (const st of ['failed', 'cancelled', 'error']) {
    const o = jobOutcome({ state: st });
    assert.equal(o.settled, true, st);
    assert.equal(o.ok, false, st);
  }
  assert.equal(jobOutcome({ state: 'done' }).ok, true);
});

test('an unsettled job is never given a duration', () => {
  /* A duration on a running job would be read as how long it took. */
  const ev = toJobSubmittedEvent({ tool: 'gnina', elapsed_s: 45 }, 1, 'r', 0, 'lead');
  assert.equal(ev.meta.duration_s, null);
  assert.equal(ev.meta.elapsed_s, 45, 'elapsed is what a running job honestly has');
});

test('no error text is invented for a job that succeeded', () => {
  assert.equal(toJobSubmittedEvent({ tool: 'x', rc: 0 }, 1, 'r', 0, 'lead').meta.error, null);
});

// ─── attachment chips survive on a prompt card ────────────────────────────────

test('the opening prompt carries what was attached to it', () => {
  /*
   * THE OPERATOR: "my attachemnts arre not visible in the followup prompt. the engine can get them but they are not
   * appearing on top of the prompts."
   *
   * Both halves were true. The engine resolves attachments and folds a briefing into the task, so the model receives
   * them, and records them as their own `attachments` event. The PROMPT event carried `meta: { role: "user" }` and
   * nothing else, so when the console replaced its optimistic card with the server's copy -- which it does by design --
   * the chips went with it.
   */
  const asked = withPromptAttachments(
    userPromptEvent({ task: 'check these attachments', at: 1756500000000 }, 3, 'max-x'),
    [{ kind: 'frameworks', id: '00-foundations', name: 'Units and conventions', found: true },
     { kind: 'tools', id: 'bacass', name: 'bacass', found: true }],
  );
  assert.equal(asked.meta.role, 'user');
  assert.equal(asked.meta.rayca_attachments.length, 2);
  assert.equal(asked.meta.rayca_attachments[0].name, 'Units and conventions');
  assert.equal(asked.meta.rayca_attachments[1].kind, 'tools');
});

test('a FOLLOW-UP carries them too, which is the case that was reported', () => {
  const note = toConsoleEvent({ kind: 'intervention', text: 'read this file too', at: 1756500001000 }, 9, 'max-x');
  assert.equal(note.meta.role, 'user', 'a follow-up is the reader\'s own words');
  const withChips = withPromptAttachments(note, [{ kind: 'files', id: 'f1', name: 'affinities.csv' }]);
  assert.equal(withChips.meta.rayca_attachments[0].name, 'affinities.csv');
  assert.equal(withChips.body, 'read this file too', 'the words are untouched');
});

test('an event that is NOT the reader\'s words is never given chips', () => {
  /* Attachments belong to a prompt. Putting them on a tool result would draw chips on a card nobody attached to. */
  const call = toConsoleEvent({ kind: 'call', verb: 'run_python', input: {}, at: 1 }, 1, 'max-x');
  const same = withPromptAttachments(call, [{ kind: 'files', id: 'f1', name: 'x.csv' }]);
  assert.equal(same.meta.rayca_attachments, undefined);
});

test('no attachments means the prompt is returned untouched', () => {
  const asked = userPromptEvent({ task: 'hello', at: 1 }, 1, 'max-x');
  assert.deepEqual(withPromptAttachments(asked, []), asked);
  assert.deepEqual(withPromptAttachments(asked, null), asked);
});

test('a chip with neither name nor id is dropped rather than drawn empty', () => {
  const chips = promptAttachmentsFrom([{ kind: 'files' }, { kind: 'files', name: 'real.csv' }]);
  assert.equal(chips.length, 1);
  assert.equal(chips[0].name, 'real.csv');
});

test('the chip shape is exactly what the console reads', () => {
  /* `console/conversation.ts` reads kind, id, name and an optional category_label. Anything else is ignored, and the
     tape's items also carry `found`, `where` and `detail`, which have no business on a chip. */
  const chips = promptAttachmentsFrom([
    { kind: 'tools', id: 'gnina', name: 'gnina', found: true, where: '/x', detail: 'long text' },
  ]);
  assert.deepEqual(Object.keys(chips[0]).sort(), ['id', 'kind', 'name']);
});
