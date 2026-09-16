/**
 * The bridge to procedural memory, consulted BEFORE the model's first turn.
 *
 * SAME SHAPE AS governance.mjs AND runstore.mjs: a long-lived Python subprocess speaking JSON lines.
 * Separate process so a memory outage cannot take down governance or the run store.
 *
 * WHY THIS EXISTS AND NOT A PROMPT. memprefetch.py argues it precisely: telling the model to call
 * retrieve_procedures is advisory, and on the live run that produced this rebuild it did not comply.
 * Consulting memory HERE makes it a PROPERTY of the run -- it happens for every run, and the model's
 * compliance is not part of the question.
 *
 * FAILURE IS HONEST, NEVER SILENT. When memory is unreachable the returned message says so in its own
 * text, so the model knows the consultation failed and can say so in its report. A run that silently
 * proceeds as though memory were empty is indistinguishable from one that checked and found nothing.
 */

import { spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { resolveEnv } from './env.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ENV = resolveEnv();
const PY = ENV.py;
const BRIDGE = join(HERE, 'memory_bridge.py');
const SRC = ENV.src;

class MemoryBridge {
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
    this.proc.stderr.on('data', (d) => process.stderr.write('[memory] ' + d.toString()));
    this.proc.on('exit', (code) => {
      process.stderr.write(`[memory] bridge exited (${code}); will restart on next call\n`);
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

const bridge = new MemoryBridge();

/**
 * Consult memory before the first turn.
 *
 * Returns { message: {role, content}, meta: {procedures, episodes, lessons, errors} } on success,
 * or a degraded message when memory is unreachable. Returns null ONLY when the bridge itself is dead,
 * in which case the caller must fabricate a failure message -- a silent omission is never acceptable.
 */
export async function prefetch(task, k) {
  const params = { task };
  if (k != null) params.k = k;
  return bridge.ask('prefetch', params, 30000);
}

/**
 * Derive a readable name from code, reusing the platform's execisolate._script_slug.
 *
 * Used as the fallback title in consoleapi.mjs when captionFrom finds no leading comment.
 * Returns the slug string, or '' if derivation failed.
 */
export async function scriptSlug(code) {
  if (!code) return '';
  const r = await bridge.ask('script_slug', { code: String(code).slice(0, 8000) }, 5000);
  return (r && r.ok && r.slug) ? r.slug : '';
}
