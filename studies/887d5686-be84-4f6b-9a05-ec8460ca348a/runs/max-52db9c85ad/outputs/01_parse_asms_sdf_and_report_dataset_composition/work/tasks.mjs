/**
 * THE STUDY PLAN'S TASKS, AND WHAT STATE EACH ONE IS IN.
 *
 * The operator: "now the study plan is empty. When the planning happens we want to have all the tasks listed in the study plan
 * with live status, which tasks is completed, which is ongoing and which has not started ... make sure it maintains state and it
 * is always live and get the task status from the engine."
 *
 * WHY THE PANEL WAS EMPTY, measured before any of this was written. The console reads its plan from an event of `type: 'plan'`
 * carrying `meta.phases`, and modulon-max emitted `type: 'plan'` for exactly two things: a delegation, and a single task changing
 * state. Neither carried `phases`, so `readPlan` found nothing and the surface had nothing to draw. The panel, its layout and its
 * five states were all already built and tested; the engine had simply never spoken the sentence they were waiting for.
 *
 * WHERE THE STATUS COMES FROM, and this is the part that did not exist at all. The SDK publishes
 * `{ type: 'system', subtype: 'task_updated', task_id, patch: { status, description, error, ... } }`, where status is one of
 * pending, running, completed, failed, killed or paused. The loop handled `init`, `assistant`, `user` and `result` and dropped
 * everything else, so every transition between created and completed was thrown away. The two hooks that WERE wired,
 * `TaskCreated` and `TaskCompleted`, can only report the two ends: nothing could ever be reported as ongoing.
 *
 * A SNAPSHOT, NOT A DELTA. Each change emits the WHOLE table, because the tape is what a reloaded page reads: a client that had
 * to fold deltas would need every one of them, in order, and would show a wrong plan for any it missed. With snapshots the last
 * one wins and a reload is correct by construction, which is the whole of "maintains state" on this side.
 */

/** The console's five states. Everything the SDK can say has to land on one of these, and nothing else may be invented. */
const PENDING = 'pending';
const RUNNING = 'running';
const DONE = 'done';
const FAILED = 'failed';
const WAITING = 'waiting';

/**
 * SDK STATUS TO THE STATE THE PANEL DRAWS.
 *
 * `in_progress` is here beside `running` because the two live in different parts of the same SDK: the task_updated patch says
 * `running` and the TaskList tool's own output says `in_progress`. Reading only one of them would leave whichever arrived from
 * the other side looking like it had never begun.
 *
 * `killed` is a failure rather than a completion. A task that was stopped did not do what it said it would, and colouring it
 * green because it is no longer running would be the plan lying about the study.
 *
 * `paused` maps to waiting, which is the state the panel already uses for work held up rather than finished or failed.
 */
const STATE_OF = {
  pending: PENDING,
  queued: PENDING,
  running: RUNNING,
  in_progress: RUNNING,
  active: RUNNING,
  completed: DONE,
  done: DONE,
  failed: FAILED,
  error: FAILED,
  killed: FAILED,
  paused: WAITING,
  blocked: WAITING,
};

/** A task nobody has said anything about yet has not started. Stated once, rather than defaulted differently in three places. */
export const DEFAULT_STATE = PENDING;

/** Keeps a plan readable when a model writes an essay into a subject line. */
export const MAX_SUBJECT = 300;

/**
 * Read a status the SDK reported, or null when it said nothing recognisable.
 *
 * NULL RATHER THAN A GUESS. An unknown status must leave the state it found alone: inventing `pending` for a word we do not know
 * would march a running task backwards, and inventing `running` would claim work that may not have begun.
 */
export function stateFrom(status) {
  const key = String(status || '').trim().toLowerCase();
  if (!key) {
    return null;
  }
  return STATE_OF[key] || null;
}

/** A fresh, empty table. A plain object so a run record can hold it and `store` can serialise it without ceremony. */
export function newTaskTable() {
  return { order: [], byId: new Map() };
}

/**
 * RECORD WHAT WAS JUST SAID ABOUT ONE TASK, and answer whether the table actually changed.
 *
 * THE ANSWER IS THE POINT. A snapshot is emitted on every change, and the SDK repeats itself: the same status arrives from a
 * hook and again in a patch. Emitting for a repeat would put duplicate plans on the tape and make the panel redraw for nothing,
 * so the caller is told when there is genuinely news and stays quiet otherwise.
 *
 * FIRST SIGHT CREATES THE ROW, whichever signal arrives first. A task can be updated before its creation hook has been seen,
 * and refusing to record it then would lose it for the rest of the run.
 */
/**
 * A TASK THE MODEL DELETED IS NOT A FAILED TASK, so it leaves the plan rather than being coloured red.
 *
 * `TaskUpdate` accepts `status: 'deleted'`, which means the model decided this work is not part of the study after all. Keeping
 * it as failed would make a plan that reads as if something went wrong when nothing did.
 */
export function dropTask(table, id) {
  const key = String(id || '').trim();
  if (!key || !table.byId.has(key)) {
    return false;
  }
  table.byId.delete(key);
  table.order = table.order.filter((x) => x !== key);
  return true;
}

export function noteTask(table, signal) {
  const id = String(signal?.id || '').trim();
  if (!id) {
    return false;
  }
  if (String(signal.status || '').trim().toLowerCase() === 'deleted') {
    return dropTask(table, id);
  }
  const known = table.byId.get(id);
  const row = known || { id, subject: '', assignee: '', state: DEFAULT_STATE, needs: [], error: '' };
  let changed = !known;
  if (!known) {
    table.order.push(id);
    table.byId.set(id, row);
  }

  const subject = String(signal.subject || '').slice(0, MAX_SUBJECT).trim();
  /* A LATER EMPTY SUBJECT IS IGNORED: a completion carries no text, and letting it overwrite the creation's would blank the
     row at the exact moment the reader wants to know what finished. */
  if (subject && subject !== row.subject) {
    row.subject = subject;
    changed = true;
  }

  const assignee = String(signal.assignee || '').trim();
  if (assignee && assignee !== row.assignee) {
    row.assignee = assignee;
    changed = true;
  }

  const state = stateFrom(signal.status);
  if (state && state !== row.state) {
    row.state = state;
    changed = true;
  }

  const error = String(signal.error || '').slice(0, MAX_SUBJECT).trim();
  if (error && error !== row.error) {
    row.error = error;
    /* An error that arrives without a status still means this task failed. */
    row.state = FAILED;
    changed = true;
  }

  if (Array.isArray(signal.needs)) {
    const needs = signal.needs.map((x) => String(x || '').trim()).filter(Boolean);
    if (needs.join('\u0000') !== row.needs.join('\u0000')) {
      row.needs = needs;
      changed = true;
    }
  }

  return changed;
}

/**
 * THE TABLE AS THE CONSOLE'S PLAN, in the shape `readPlan` already parses.
 *
 * `goal` CARRIES THE SUBJECT, because that is the sentence the planner wrote about this task and `goal` is the field the panel
 * shows as the stage's heading. `rationale` is left empty rather than filled with a restatement: the panel shows less when there
 * is no reasoning to show, and inventing one would put words in the planner's mouth.
 *
 * `needs` IS DECLARED DEPENDENCY, NOT ORDER. The layout draws phases that can run at the same time side by side, so claiming
 * every task depends on the one before it would turn a genuinely parallel plan into a false chain. Where the SDK reports
 * `blockedBy` it is carried through; where it reports nothing, nothing is asserted.
 */
export function taskPhases(table) {
  return table.order.map((id, index) => {
    const row = table.byId.get(id);
    return {
      id,
      index,
      goal: row.subject || 'task ' + id,
      rationale: '',
      steps: [],
      produces: [],
      needs: row.needs.slice(),
      decides: [],
      /* THE STATE THE ENGINE DECLARES. The console infers phase state from event tags when a plan does not say; a plan that
         does say must be believed, because the SDK's task list is the only thing that actually knows. */
      state: row.state,
      assignee: row.assignee || undefined,
      error: row.error || undefined,
      final: index === table.order.length - 1,
    };
  });
}

/** How many tasks are in each state, for a one-line summary beside the plan. */
export function taskCounts(table) {
  const out = { total: table.order.length, pending: 0, running: 0, done: 0, failed: 0, waiting: 0 };
  for (const id of table.order) {
    const state = table.byId.get(id)?.state || DEFAULT_STATE;
    out[state] = (out[state] || 0) + 1;
  }
  return out;
}

export default { newTaskTable, noteTask, dropTask, taskPhases, taskCounts, stateFrom, DEFAULT_STATE, MAX_SUBJECT };
