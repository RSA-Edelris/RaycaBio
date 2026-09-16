/**
 * The engine's link to the governance layer.
 *
 * ONE PYTHON PROCESS, KEPT ALIVE. Governance is consulted before and after every tool call, so starting an interpreter
 * per call would add a second to every dispatch. The bridge speaks JSON lines and is restarted if it dies.
 *
 * FAILS OPEN FOR GATES AND CLOSED FOR JUDGEMENTS, deliberately. If the bridge is unreachable, a tool is still allowed
 * to run -- refusing all science because a sidecar died would be worse than the risk it manages. But a report whose
 * figures could not be checked is reported as UNVERIFIED rather than as clean, because silently approving an unchecked
 * number is the exact failure this layer exists to prevent.
 */

import { spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { resolveEnv } from './env.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ENV = resolveEnv();
const PY = ENV.py;
const BRIDGE = join(HERE, 'governance_bridge.py');
const SRC = ENV.src;

class Bridge {
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
        } catch { /* a partial or noisy line is not a protocol failure */ }
      }
    });
    this.proc.stderr.on('data', (d) => process.stderr.write('[gov] ' + d.toString()));
    this.proc.on('exit', (code) => {
      process.stderr.write(`[gov] bridge exited (${code}); governance is unavailable until it restarts\n`);
      this.available = false;
      this.proc = null;
      for (const [, w] of this.waiting) w(null);
      this.waiting.clear();
    });
  }

  async ask(op, params, timeoutMs = 20000) {
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

const bridge = new Bridge();

export const governance = {
  async begin(runId, mode = '') {
    return (await bridge.ask('begin', { run_id: runId, mode })) || { ok: false, gates: 'unavailable' };
  },

  /**
   * Consulted before every tool call.
   *
   * ALLOWS ON FAILURE. A silent sidecar must not stop a researcher's work; the alternative is an engine that refuses
   * everything the moment a subprocess dies.
   */
  async beforeTool({ runId, verb, origin, input }) {
    const r = await bridge.ask('before_tool', { run_id: runId, verb, origin, input });
    if (!r) return { allow: true };
    return r;
  },

  async afterTool({ runId, verb, origin, output, seconds = 0, emit }) {
    const r = await bridge.ask('after_tool', { run_id: runId, verb, origin, output: String(output || '').slice(0, 60000), seconds });
    if (r?.notes?.length && typeof emit === 'function') {
      for (const n of r.notes) emit('gate', { verb, kind: n.kind, detail: n.detail, advisory: true });
    }
    return r || { ok: false };
  },

  /**
   * Judge the final answer's figures.
   *
   * THE ONE PLACE THAT FAILS CLOSED. `verdict: 'unavailable'` is reported as unverified rather than clean, because a
   * report whose numbers were never checked is exactly what this layer exists to catch.
   */
  async judge({ runId, answer }) {
    const r = await bridge.ask('judge', { run_id: runId, answer }, 60000);
    if (!r) {
      return { ok: false, verdict: 'unavailable', complaints: ['governance was unreachable; figures are UNVERIFIED'] };
    }
    return r;
  },

  async end(runId) {
    return (await bridge.ask('end', { run_id: runId })) || { ok: false };
  },
};
