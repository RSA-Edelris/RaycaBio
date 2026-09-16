/**
 * Tests for: A TOOL RESULT REACHES THE CONSOLE AS LINES, NOT AS AN ESCAPED JSON STRING.
 *
 * THE OPERATOR: "for the event stream cards, the ones that have python code, the codes view is not considering the next
 * line slashes and all the codes are packed together instead of being shown in proper lines." Then, after a first fix
 * on the wrong layer: "it is still not solved. make sure you do a fundamental fix."
 *
 * MEASURED against the stored tape of run max-c3eca0b57a: 4 of its 86 event bodies were a single line carrying literal
 * backslash-n, all of them results of python steps. An MCP tool returns its result as TEXT which is itself a JSON
 * document, so the newlines in it are two-character JSON escapes, and nothing on the path to the screen parsed them.
 *
 * THESE DRIVE `toConsoleEvent` WITH RAW EVENTS in the exact shape `emit` records, taken from server.mjs. The first
 * attempt at this defect was verified against a synthetic event with an OBJECT body, a shape the engine never sends, so
 * it passed while the console was still broken. That is the mistake these are built to avoid: the payloads below are
 * strings containing JSON, because that is what really arrives.
 *
 * Run: node --test modulon-max/
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';

import { readableBody, toConsoleEvent } from './consoleapi.mjs';

const SCRIPT = [
  'import numpy as np',
  '',
  'def score(x):',
  '    total = 0.0',
  '    for v in x:',
  '        total += v ** 2',
  '    return total',
].join('\n');

/** A tool result exactly as an MCP server returns it: text that happens to be a JSON document. */
const toolResultText = (output) => JSON.stringify({ output });

test('a tool result that is a JSON document arrives with real newlines', () => {
  const raw = toolResultText('Downloaded 6LU7: 239112 chars\nNon-solvent HETATM: 3\n\n[note] gone: r');
  // The payload really is one line before translation. If this ever stops being true the test below proves nothing.
  assert.equal(raw.includes('\n'), false);
  assert.ok(raw.includes('\\n'));

  const out = readableBody(raw);
  assert.equal(out.split('\n').length, 4);
  assert.equal(out.includes('\\n'), false);
  assert.match(out, /^Downloaded 6LU7/);
});

test('the result of a python step is not one packed line in the console event', () => {
  const ev = {
    kind: 'back',
    agent: 'lead',
    id: 'call-1',
    verb: 'run_python',
    origin: 'platform',
    returned: true,
    seconds: 12,
    output: toolResultText('Protein lines: 2232\nLigand HETATM lines: 37\nMol atoms: 37'),
  };
  const out = toConsoleEvent(ev, 3, 'max-test');
  assert.equal(out.type, 'observe');
  assert.equal(out.body.split('\n').length, 3);
  assert.equal(out.body.includes('\\n'), false);
  assert.equal(out.body.includes('{"output"'), false);
});

test('the code a step is about to run keeps its indentation', () => {
  const ev = {
    kind: 'call', agent: 'lead', turn: 1, id: 'call-2', verb: 'run_python', origin: 'platform',
    input: { code: SCRIPT },
  };
  const out = toConsoleEvent(ev, 1, 'max-test');
  assert.equal(out.type, 'execute');
  assert.equal(out.body, SCRIPT);
  assert.ok(out.body.includes('        total += v ** 2'));
});

test('code under a field name nobody listed still arrives as code', () => {
  /*
   * THE CAGE THIS REMOVES. `codeOf` reads `code`, `script`, `source`. A tool naming its argument anything else fell
   * through to a whole-payload stringify, which is how a script became one line. Derivation by SHAPE has no list to go
   * stale: the longest string in the payload is the readable part, whatever it is called.
   */
  const ev = {
    kind: 'call', agent: 'lead', turn: 1, id: 'call-3', verb: 'run_cell', origin: 'platform',
    input: { cell_contents: SCRIPT },
  };
  const out = toConsoleEvent(ev, 1, 'max-test');
  assert.equal(out.body, SCRIPT);
});

test('a small argument object reads as a block, not one dense line', () => {
  const ev = {
    kind: 'call', agent: 'lead', turn: 1, id: 'call-4', verb: 'query_geo', origin: 'platform',
    input: { accession: 'GSE123456', include_metadata: true },
  };
  const out = toConsoleEvent(ev, 1, 'max-test');
  assert.ok(out.body.split('\n').length > 3);
  assert.ok(out.body.includes('GSE123456'));
});

/*
 * EXPECTATION MOVED, and this one was wrong in a way worth recording. It used to also assert that a payload was not
 * reduced to its longest field when that field was MULTI-LINE, on the reasoning that siblings should not vanish. The
 * operator's next paste disproved it: a real run_python result is
 * `{ output, meta, workspace, operation_class, files_written }`, its printed output is well under 60% of the document,
 * so the ratio sent it to pretty-printing -- which re-escaped every newline in it. The card showed indented JSON with
 * backslash-n running through the middle.
 *
 * A multi-line string cannot survive being serialised AT ALL, at any indent. So the ratio now governs only single-line
 * payloads, where serialising is harmless because there are no newlines to escape, and that is what this pins.
 */
test('a payload of short fields keeps all of them rather than showing the longest', () => {
  const value = {
    receptor: '9C56.pdb', ligand: 'EDS00760714.sdf', centre: [12.5, 4.25, -8.0],
    exhaustiveness: 32, seed: 42, scoring: 'vina',
    note: 'a slightly longer note that is still not the substance of this call',
  };
  const out = readableBody(value);
  assert.ok(out.includes('9C56.pdb'));
  assert.ok(out.includes('exhaustiveness'));
});

test("the operator's own run_python result reads as lines, not as indented JSON", () => {
  /*
   * COPIED FROM WHAT THEY PASTED, field for field, because the payload's SHAPE is the defect: the printed output is a
   * small part of a document carrying meta, workspace, operation_class and files_written. Any rule that weighs the
   * readable part against the whole document gets this case wrong.
   */
  const payload = JSON.stringify({
    output: 'Protein lines: 2232, Ligand HETATM lines: 37\nMol atoms: 37\nFiles written: True True\n\n'
      + '[note] these names could not be carried to the next call and are gone: f, writer',
    meta: { crashed: false, returncode: 0, dropped: ['f', 'writer'], narrations: [], finished: false,
      finish_answer: null },
    workspace: '/home/ubuntu/rayca-sessions/d98ecc2e-8220-425f-9554-a96dc993e274-3f11403ae973',
    operation_class: 'structure',
    files_written: [
      { name: 'receptor_1IEP_A.pdb', id: '618eaf686bac4edea1773a77f9acca7e', kind: 'molecules' },
      { name: 'ref_ligand_STI.sdf', id: 'b9e2e163587348e3bef3d5dadd8a8031', kind: 'molecules' },
    ],
  });

  const out = readableBody(payload);
  assert.equal(out.includes('\\n'), false, 'no escape may survive into what the reader sees');
  assert.equal(out.trimStart().startsWith('{'), false, 'the reader must not be shown a JSON document');
  assert.equal(out.split('\n')[0], 'Protein lines: 2232, Ligand HETATM lines: 37');
  assert.equal(out.split('\n')[1], 'Mol atoms: 37');
});

test('a result carrying both stdout and a traceback shows both, each labelled', () => {
  /*
   * THE COST OF RETURNING ONE STRING ALONE, paid for rather than ignored. With a single multi-line field there is
   * nothing to label and a bare string is right. With two, silently keeping the longer one would hide a traceback
   * behind ordinary output, which is the worst possible thing to hide.
   */
  const payload = JSON.stringify({
    stdout: 'step 1 ok\nstep 2 ok',
    stderr: 'Traceback (most recent call last):\n  File "<cell>", line 3\nValueError: bad input',
  });
  const out = readableBody(payload);
  assert.ok(out.includes('stdout:'));
  assert.ok(out.includes('stderr:'));
  assert.ok(out.includes('ValueError: bad input'));
  assert.equal(out.includes('\\n'), false);
});

test('plain text output is left exactly as it is', () => {
  assert.equal(readableBody('rc=0 in 27.6s'), 'rc=0 in 27.6s');
  assert.equal(readableBody('gnina --receptor r.pdb\n--ligand l.sdf'), 'gnina --receptor r.pdb\n--ligand l.sdf');
});

test('a bare scalar that happens to be valid JSON is treated as the text it is', () => {
  // `42` and `null` parse, and a tool that printed either meant the characters. Only documents are unwrapped.
  assert.equal(readableBody('42'), '42');
  assert.equal(readableBody('null'), 'null');
  assert.equal(readableBody('true'), 'true');
});

test('a truncated JSON result degrades to the raw text instead of throwing', () => {
  /*
   * A REAL CASE, not a hypothetical: the engine slices a tool result to 12000 characters before emitting, so a longer
   * document arrives cut mid-string and cannot parse. It must still render, and it must not take the run's card down.
   */
  const cut = toolResultText('x'.repeat(200)).slice(0, 120);
  const out = readableBody(cut);
  assert.equal(typeof out, 'string');
  assert.ok(out.length > 0);
});

test('a cyclic payload does not hang the translator', () => {
  const a = { name: 'a' };
  a.self = a;
  const out = readableBody(a);
  assert.equal(typeof out, 'string');
});
