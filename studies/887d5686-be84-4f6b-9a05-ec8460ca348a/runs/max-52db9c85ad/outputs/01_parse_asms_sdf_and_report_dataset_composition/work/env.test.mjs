/**
 * Tests for: DEVELOPMENT CODE MUST NOT RUN IN PRODUCTION BY DEFAULT.
 *
 * WHY THIS EXISTS, and it is not hypothetical. Nine files in this directory each resolved the engine's
 * source tree as `process.env.RAYCA_SRC || '/home/ubuntu/rayca-modulon-dev/src'` (five .mjs) or the
 * Python equivalent (four .py). The default was the DEVELOPMENT tree, so the live rayca-modulon-max
 * service ran out of the tree under active edit: editing a file changed in-flight researcher runs, and
 * there was no version boundary around a run (docs/design/what-we-have-and-how-it-connects.md, three
 * documented code-vs-reality mismatches trace to this).
 *
 * env.mjs replaced those nine defaults with one resolver whose default is PRODUCTION. These tests pin
 * the properties that make the defect impossible to reintroduce silently:
 *
 *   1. An unset environment resolves to production, NOT development.
 *   2. Production resolves to the promoted tree, never the dev tree under edit.
 *   3. Development resolves to the dev tree AND a separate database, so a dev run cannot write the
 *      production tape.
 *   4. A typo does not silently become development.
 *   5. An explicit per-field override still works, because operations needs an escape hatch.
 *
 * Run: node --test modulon-max/
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';

import { resolveEnv, environment, PROFILE_NAMES } from './env.mjs';

const DEV_TREE = '/home/ubuntu/rayca-modulon-dev/src';
const LIVE_TREE = '/home/ubuntu/rayca-modulon/src';
const PROD_DB = '/var/lib/rayca/modulon-max.sqlite';
const DEV_DB = '/var/lib/rayca/modulon-max-dev.sqlite';

test('an unset environment resolves to production, not the dev tree', () => {
  assert.equal(environment({}), 'production');
  const e = resolveEnv({});
  assert.equal(e.src, LIVE_TREE, 'unset RAYCA_ENV must NOT resolve to the dev tree');
  assert.equal(e.db, PROD_DB);
  assert.notEqual(e.src, DEV_TREE);
});

test('production resolves to the promoted tree that deploy-engine.py installs', () => {
  const e = resolveEnv({ RAYCA_ENV: 'production' });
  assert.equal(e.src, LIVE_TREE);
  assert.equal(e.db, PROD_DB);
});

test('development resolves to the dev tree AND a separate database', () => {
  const e = resolveEnv({ RAYCA_ENV: 'development' });
  assert.equal(e.src, DEV_TREE);
  assert.equal(e.db, DEV_DB, 'a dev run must never write the production tape');
  assert.notEqual(e.db, PROD_DB);
});

test('a typo does not silently become development', () => {
  // The whole point of the safe default: a mistake falls towards production-safe, not dev-in-prod.
  assert.equal(environment({ RAYCA_ENV: 'developmnt' }), 'production');
  assert.equal(environment({ RAYCA_ENV: 'staging' }), 'production');
  assert.equal(environment({ RAYCA_ENV: 'PROD' }), 'production');
});

test('RAYCA_ENV is case-insensitive for the known names', () => {
  assert.equal(environment({ RAYCA_ENV: 'Development' }), 'development');
  assert.equal(environment({ RAYCA_ENV: 'PRODUCTION' }), 'production');
});

test('an explicit per-field override still wins, for operational escape hatches', () => {
  const e = resolveEnv({ RAYCA_ENV: 'production', RAYCA_SRC: '/tmp/pin/src', MAX_DB: '/tmp/pin/db.sqlite' });
  assert.equal(e.src, '/tmp/pin/src');
  assert.equal(e.db, '/tmp/pin/db.sqlite');
});

test('the two environments never share a source tree or a database', () => {
  const prod = resolveEnv({ RAYCA_ENV: 'production' });
  const dev = resolveEnv({ RAYCA_ENV: 'development' });
  assert.notEqual(prod.src, dev.src);
  assert.notEqual(prod.db, dev.db);
  assert.notEqual(prod.secretsFile, dev.secretsFile);
});

test('only the two intended profiles exist', () => {
  assert.deepEqual(PROFILE_NAMES.sort(), ['development', 'production']);
});
