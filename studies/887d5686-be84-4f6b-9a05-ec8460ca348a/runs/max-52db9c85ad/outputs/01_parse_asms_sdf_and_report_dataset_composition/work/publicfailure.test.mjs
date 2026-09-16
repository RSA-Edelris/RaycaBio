/**
 * WHAT A READER IS TOLD WHEN A RUN DOES NOT FINISH, AND WHAT THEY ARE NEVER TOLD.
 *
 * THE OPERATOR: "when we stop the session, a message appear in conversation and say claude code is stoped, we do not want to show
 * claude code name to our users please correct it".
 *
 * === THE ASSERTION THAT ACTUALLY PROTECTS THIS ===
 *
 * The tempting test is a list: "the output must not contain Claude". That passes for the two strings measured today and gives no
 * protection against the next SDK release, which will phrase things differently and may name a different provider, model or policy
 * page. A list of forbidden words is a cage, and it is a cage around the wrong thing.
 *
 * So the load-bearing test here is a PROPERTY: feed the function a random token nobody could have anticipated and assert the token does
 * not appear in the output. That holds for every possible input rather than the handful I thought of, and it is only satisfiable by an
 * implementation that never copies its input into its output, which is the real requirement.
 *
 * The measured strings are still tested, but for CLASSIFICATION, which is the other half: a deliberate stop must not read as a crash.
 *
 * Run: node --test modulon-max/
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';

import { publicFailure, PUBLIC_TEXTS } from './publicfailure.mjs';

/** The exact strings clients were shown, read out of the `runs` table of the live deployment rather than recalled. */
const OBSERVED = {
  stop: 'Claude Code process aborted by user',
  refusal:
    "Claude Code returned an error result: API Error: Sonnet 4.6 can't help with this. " +
    'Start a new session to continue.  Learn more: https://www.anthropic.com/legal/aup',
};

test('a public failure never echoes its input, for any input', () => {
  // The property. A token no classifier can match, so the generic path is exercised too.
  for (let i = 0; i < 200; i++) {
    const token = `zq${Math.random().toString(36).slice(2)}${i}`;
    assert.ok(!publicFailure(new Error(`something failed: ${token}`)).text.includes(token));
  }
});

test('a public failure answers only with sentences the platform owns', () => {
  // Stronger than "does not contain the input": the output is always from a known, reviewable set, so a new leak cannot appear without
  // someone adding a sentence to that set, where a reader will see it.
  const inputs = [
    OBSERVED.stop,
    OBSERVED.refusal,
    'Anthropic API overloaded_error 529',
    'The model claude-sonnet-5 is not available for this account',
    'socket hang up',
    'run exceeded maxBudgetUsd of 5',
    'ETIMEDOUT',
    '',
    'total gibberish',
  ];
  for (const i of inputs) {
    assert.ok(PUBLIC_TEXTS.includes(publicFailure(new Error(i)).text), i);
  }
  // A catch receives non-Errors too.
  for (const i of ['a bare string', undefined, null, 42, {}]) {
    assert.ok(PUBLIC_TEXTS.includes(publicFailure(i).text));
  }
});

test('no vendor, model or policy link survives, for the strings clients were actually shown', () => {
  const forbidden = ['claude', 'anthropic', 'sonnet', 'opus', 'haiku', 'bedrock', 'openai',
    'api error', 'legal/aup', 'start a new session to continue'];
  for (const raw of Object.values(OBSERVED)) {
    const out = publicFailure(new Error(raw)).text.toLowerCase();
    for (const word of forbidden) {
      assert.ok(!out.includes(word), `${word} leaked`);
    }
  }
});

test('the raw text survives for the journal, separately from what a reader sees', () => {
  // Sanitising the conversation must not cost us the diagnosis. The caller logs `raw`; only `text` is published.
  const f = publicFailure(new Error(OBSERVED.refusal));
  assert.ok(f.raw.includes('Claude Code'));
  assert.ok(!f.text.includes('Claude Code'));
});

test('a deliberate stop is not reported as a crash', () => {
  const f = publicFailure(new Error(OBSERVED.stop));
  assert.equal(f.kind, 'stopped');
  assert.equal(f.stopped, true);
  assert.match(f.text, /stopped at your request/i);
  // Beyond wording: a reader who stops a run needs to know their work survived.
  assert.match(f.text, /kept/i);
});

test('a real failure is not dressed up as a stop', () => {
  for (const raw of ['socket hang up', 'ETIMEDOUT', 'undefined is not a function']) {
    assert.equal(publicFailure(new Error(raw)).stopped, false, raw);
  }
});

test('a model refusal is explained without naming the model', () => {
  const f = publicFailure(new Error(OBSERVED.refusal));
  assert.equal(f.kind, 'declined');
  assert.match(f.text, /declined/i);
  // Actionable, which the original was too. It just named someone else's product while saying so.
  assert.match(f.text, /rephras|fresh conversation/i);
});
