/**
 * The native event tree for modulon-max.
 *
 * WHY THIS IS NOT A TRANSLATION OF THE EXISTING TAPE. The operational tape is FLAT and ordered by a `seq` integer,
 * which is right for an engine that runs one tool at a time in one thread. This loop does not work that way: it spawns
 * sub-agents that run their own turns and call their own tools, it keeps its own task list, and it compacts its own
 * context when a run gets long. The truthful shape is a TREE with an agent on every node, so ordering is arrival order
 * WITHIN an agent and there is no global sequence number to get wrong. A `seq` used as a sort key is what put a mid-run
 * prompt above the first turn in the console this morning.
 *
 * EVERY KIND HERE EXISTS BECAUSE A REAL RUN NEEDED IT. The PD-L1 run on 2026-08-21 exposed three holes, all of them
 * cases where the reader was told less than the truth:
 *
 *   - `member.*` arrived only after the lead had finished, because members were polled at the end. Two specialists had
 *     already reported and none of it was visible. Now driven by the `SubagentStart` / `SubagentStop` hooks.
 *   - a 15-minute rfdiffusion call emitted NOTHING, so the screen looked frozen. That is the operator's HPC complaint
 *     in mirror image: not a card per second, but silence. Hence `tool.progress`.
 *   - a Python traceback was reported as `ok: true`, because the event carried only the MCP-level result. `meta.ok` is
 *     True on failing steps in this codebase, so success has to be judged on the payload. Hence `failed_inside`.
 */

/** Every event kind this engine can publish. Named so a reader can switch on them exhaustively. */
export const KINDS = Object.freeze({
  SESSION_START: 'session.start',
  READY: 'ready',
  SAY: 'say',
  THINK: 'think',
  CALL: 'call',
  PROGRESS: 'tool.progress',
  FILE: 'file.observed',
  JOB: 'job.submitted',
  BACK: 'back',
  GATE: 'gate',
  REFUSED: 'refused',
  SPAWN: 'spawn',
  MEMBER_SAY: 'member.say',
  MEMBER_CALL: 'member.call',
  MEMBER_BACK: 'member.back',
  MEMBER_DONE: 'member.done',
  TASK: 'task',
  /* The whole task table, emitted as one snapshot whenever any task changes, which is what the study plan draws. */
  PLAN: 'plan',
  /* A PUSH TO GITHUB, reported like any other step so a reload shows it.
   *
   * The operator asked for every run to be pushed, including failures, which means the push itself is a thing that can fail
   * while the run succeeded. A silent failure here would be the same defect as the cancel button that answered 409 into a
   * void: the work would not be in the repository and nobody would be told. */
  PUBLISH: 'publish',
  COMPACT: 'compact',
  INTERVENTION: 'intervention',
  MEMORY: 'memory',
  /*
   * WHAT THE RESEARCHER ATTACHED, AND WHETHER IT WAS FOUND.
   *
   * Recorded as an event rather than only folded into the prompt, because the operator's complaint was that attachments
   * "do not reach the engine" and the only way to answer that is to be able to point at the moment they arrived. It also
   * makes an unresolved attachment visible in the conversation instead of only in the model's reply.
   */
  ATTACHED: 'attachments',
  CANCELLED: 'cancelled',
  SESSION_END: 'session.end',
});

/**
 * Did the code inside the tool actually work?
 *
 * THE TRAP THIS EXISTS FOR. A tool can return successfully while the thing it ran failed: `run_python` hands back a
 * traceback as its output with a perfectly good exit status, and `meta.ok` is True on failing steps throughout this
 * codebase. Reporting that as success is how a reader ends up trusting a number that was never computed. So the
 * payload is inspected, and the two facts are kept separate: the call returned, and the work inside it did not.
 */
export function failedInside(output) {
  const s = typeof output === 'string' ? output : JSON.stringify(output ?? '');
  if (!s) return false;
  return /Traceback \(most recent call last\)/.test(s)
    || /^\s*"?rc"?\s*[:=]\s*[1-9]/m.test(s)
    || /\berror\b"?\s*:\s*"(?!none")/i.test(s)
    || /\btool_failed\b/.test(s);
}

/**
 * Does this payload claim to have produced something while producing nothing?
 *
 * MEASURED, on run-f2e7c8c64b6b: `binderflow` returned rc=0 four times with `n_backbones: 0, n_filtered: 0,
 * n_scored: 0, n_hits: 0`, and the model responded by loosening scoring thresholds three more times -- which cannot
 * help when nothing was generated. Derived from the shape of the payload rather than from a list of tool names,
 * because a list would miss the next tool to do this.
 */
export function producedNothing(output) {
  let o = output;
  if (typeof o === 'string') {
    try { o = JSON.parse(o); } catch { return false; }
  }
  if (!o || typeof o !== 'object') return false;
  const counts = Object.entries(o).filter(([k]) => /^n_|_count$|^num_/.test(k));
  const lists = Object.entries(o).filter(([, v]) => Array.isArray(v));
  const allCountsZero = counts.length > 0 && counts.every(([, v]) => v === 0);
  const allListsEmpty = lists.length > 0 && lists.every(([, v]) => v.length === 0);
  if (counts.length === 0 && lists.length === 0) return false;
  return (counts.length ? allCountsZero : true) && (lists.length ? allListsEmpty : true);
}

/** Strip the `mcp__rayca__` prefix so a reader sees the verb, and say where it came from. */
export function nameAndOrigin(toolName) {
  const n = String(toolName || '');
  return n.startsWith('mcp__rayca__')
    ? { verb: n.slice('mcp__rayca__'.length), origin: 'platform' }
    : { verb: n, origin: 'own' };
}
