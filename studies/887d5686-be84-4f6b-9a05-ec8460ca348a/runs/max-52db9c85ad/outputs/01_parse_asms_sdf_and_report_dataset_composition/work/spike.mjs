#!/usr/bin/env node
/**
 * modulon-max spike: drive the Rayca platform with Claude Code's own agent loop.
 *
 * WHAT THIS IS TESTING, and nothing more. Can a loop we did not write pick the right verb from the platform, call it
 * with a valid argument shape, and report a number it actually computed? That is the whole question. It is not a
 * console, not a replacement engine, and it deliberately touches neither.
 *
 * THE ANSWER IS KNOWN IN ADVANCE, which is the only reason the result means anything. Imatinib's exact molecular
 * weight is 493.2590086120001 -- measured today by the current engine in run-6d9b10e91772, matching local RDKit to
 * the last floating-point digit including the trailing noise. A loop that reports 493.6 has recalled it from
 * training. A loop that reports 493.2590086120001 has run RDKit through our platform.
 *
 * ISOLATION. The verbs arrive over MCP from a separate Python process. The live engine on port 8201 is untouched and
 * still serving. Nothing here writes to the console.
 */

import { query } from '@anthropic-ai/claude-agent-sdk';
import { resolveEnv } from './env.mjs';

// A spike is a development test harness by definition, but it still resolves through the one seam so it
// exercises the same resolution the service uses. Run it with RAYCA_ENV=development.
const ENV = resolveEnv();
const SRC = ENV.src;
const PY = ENV.py;
const SERVER = process.env.RAYCA_MCP || '/home/ubuntu/rayca-modulon-dev/modulon-max/rayca_mcp_server.py';

const TASK = process.argv.slice(2).join(' ') || [
  'Using the tools available to you, compute the exact molecular weight and the number of rotatable bonds',
  'for imatinib. Do not answer from memory: run the calculation and report what it returns.',
  'Imatinib SMILES: CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5',
].join(' ');

/** Every tool the platform publishes is allowed; the point is to see which one it reaches for. */
const options = {
  model: process.env.RAYCA_MODEL || 'claude-sonnet-4-6',
  // CLAUDE CODE'S OWN SYSTEM PROMPT IS OPT-IN, and this is the whole of the "the SDK is not as smart" story.
  // Omit it and you get a bare model with tools attached. The docs name this preset as "Claude Code's default system
  // prompt", so without it you are not running Claude Code's judgement, only its plumbing.
  systemPrompt: process.env.RAYCA_NO_PRESET ? undefined : { type: 'preset', preset: 'claude_code' },
  permissionMode: 'bypassPermissions',
  maxTurns: 12,
  mcpServers: {
    rayca: {
      type: 'stdio',
      command: PY,
      args: [SERVER],
      env: {
        RAYCA_SRC: SRC,
        PYTHONPATH: SRC,
        RAYCA_USER_ID: process.env.RAYCA_USER_ID || '',
      },
    },
  },
};

const seen = { tools: [], text: [], errors: [] };

console.log('  task: ' + TASK.slice(0, 110) + '...');
console.log('  model: ' + options.model + '   verbs: over MCP from ' + SERVER.split('/').pop());
console.log('  ---');

try {
  for await (const msg of query({ prompt: TASK, options })) {
    if (msg.type === 'system' && msg.subtype === 'init') {
      const t = (msg.tools || []).filter((x) => String(x).startsWith('mcp__rayca__'));
      console.log('  loop initialised. rayca verbs visible to it: ' + t.length);
      if (t.length) console.log('    ' + t.slice(0, 8).map((x) => x.replace('mcp__rayca__', '')).join(', '));
      const srv = (msg.mcp_servers || []).map((s) => s.name + '=' + s.status).join(', ');
      if (srv) console.log('    mcp servers: ' + srv);
    }
    if (msg.type === 'assistant') {
      for (const blk of msg.message?.content || []) {
        if (blk.type === 'tool_use') {
          const nm = String(blk.name).replace('mcp__rayca__', '');
          seen.tools.push(nm);
          console.log('  -> CALLS ' + nm + ' ' + JSON.stringify(blk.input).slice(0, 150));
        }
        if (blk.type === 'text' && blk.text.trim()) seen.text.push(blk.text.trim());
      }
    }
    if (msg.type === 'user') {
      for (const blk of msg.message?.content || []) {
        if (blk.type === 'tool_result') {
          const body = typeof blk.content === 'string'
            ? blk.content
            : (blk.content || []).map((c) => c.text || '').join(' ');
          const flag = blk.is_error ? 'ERROR' : 'ok';
          if (blk.is_error) seen.errors.push(body.slice(0, 200));
          console.log('  <- ' + flag + ' ' + body.replace(/\s+/g, ' ').slice(0, 220));
        }
      }
    }
    if (msg.type === 'result') {
      console.log('  ---');
      console.log('  turns: ' + msg.num_turns + '   ms: ' + msg.duration_ms + '   cost: $' + (msg.total_cost_usd ?? 0));
      console.log('  verbs called: ' + (seen.tools.join(', ') || 'NONE'));
      const final = (msg.result || seen.text.join('\n')).slice(0, 900);
      console.log('  --- final answer ---');
      console.log('  ' + final.replace(/\n/g, '\n  '));
      // The check that matters. Recall gives 493.5 or 493.6; the platform gives the exact float.
      const exact = /493\.2590/.test(final) || /493\.2590/.test(seen.text.join(' '));
      console.log('  ---');
      console.log('  EXACT VALUE FROM THE PLATFORM (493.2590086120001): ' + (exact ? 'YES' : 'NOT FOUND'));
      if (seen.errors.length) console.log('  tool errors: ' + seen.errors.length);
    }
  }
} catch (e) {
  console.log('  FAILED: ' + (e?.message || String(e)).slice(0, 500));
  process.exitCode = 1;
}
