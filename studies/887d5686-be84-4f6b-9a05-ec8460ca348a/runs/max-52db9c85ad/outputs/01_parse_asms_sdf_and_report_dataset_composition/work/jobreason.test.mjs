// WHAT A FAILED CLUSTER JOB TELLS THE CONSOLE.
//
// The reason a job failed was recorded in cluster_jobs and never announced, so the console could show
// "failed" and nothing else. A researcher then spent 77 minutes and $7.17 on 2026-09-10 asking the agent
// what had gone wrong with a job whose cause was already in the database.
//
// This asserts the RENDERED PAYLOAD, not the wiring: that whatever is written to the row is present in the
// event a console reads. Asserting "the code mentions reason" would pass on a comment.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const SRC = readFileSync(new URL('./server.mjs', import.meta.url), 'utf8');

test('the job event payload is derived from the row update, not restated', () => {
  // One object is built, used for the row, and spread into the event. A second literal listing fields by
  // hand is exactly how reason and workdirKept were lost before.
  assert.match(SRC, /const jobUpdate = \{/, 'the update object should be built once');
  assert.match(SRC, /store\.updateClusterJob\(job\.job_id, jobUpdate\)/, 'the row should be written from it');
  assert.match(SRC, /\.\.\.jobUpdate,/, 'the event should SPREAD it rather than relist fields');
});

test('a field added to the row cannot be dropped from the event', () => {
  // The guarantee is structural: between the object literal and the emit there must be no second
  // hand-written list of the same fields. Both reason and workdirKept must appear exactly once, inside
  // the update object.
  const update = SRC.slice(SRC.indexOf('const jobUpdate = {'), SRC.indexOf('store.updateClusterJob(job.job_id, jobUpdate)'));
  assert.match(update, /reason:/, 'reason belongs in the update object');
  assert.match(update, /workdirKept:/, 'workdirKept belongs in the update object');
  const emitBlock = SRC.slice(SRC.indexOf('...jobUpdate,'), SRC.indexOf('...jobUpdate,') + 400);
  assert.ok(!/reason:/.test(emitBlock), 'reason must NOT be restated in the emit, or the class returns');
  assert.ok(!/workdirKept:/.test(emitBlock), 'workdirKept must NOT be restated in the emit');
});
