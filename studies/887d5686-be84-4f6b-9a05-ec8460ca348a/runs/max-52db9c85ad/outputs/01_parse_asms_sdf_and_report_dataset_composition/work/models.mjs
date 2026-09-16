/**
 * WHICH MODELS A SELECTION MAY NAME, asked for rather than written down.
 *
 * A CLOSED SET IS STILL RIGHT. Accepting an arbitrary string turns a mistyped selection into a dead run several seconds
 * in, with the cost already incurred. What was wrong was writing the set by hand.
 *
 * MEASURED DEFECT THIS FIXES. `server.mjs` held a literal list of three Claude models, while
 * `/v1/operational/models`, which is what fills the console's selector, advertised TWELVE including both Qwen3 models
 * and named `qwen3-coder-480b` as its own default. A reader could select Qwen3, the literal would not recognise it, and
 * the run went to claude-sonnet-4-6 with the stored `model` column asserting sonnet. Across 365 max runs the only
 * models ever recorded are claude-sonnet-4-6 and claude-haiku-4-5. Not one Qwen3 run, despite Qwen3 being the
 * advertised default.
 *
 * THE ROUTER IS THE AUTHORITY, because it is the thing that either has a deployment for a name or does not. `serve.py`
 * already works this way for context limits: "THE LIMIT IS ASKED FOR, NOT WRITTEN DOWN."
 */

/**
 * The selectable set implied by a router listing, or null when the listing carries nothing usable.
 *
 * The configured model leads because it must always be selectable, whatever the router says, so that setting
 * RAYCA_MODEL to something new cannot lock the deployment out of its own default.
 */
export function modelsFromRouterPayload(body, configured) {
  const ids = Array.isArray(body?.data)
    ? body.data.map((m) => String(m?.id ?? '').trim()).filter(Boolean)
    : [];
  if (ids.length === 0) {
    return null;
  }
  return [configured, ...ids].filter((m, idx, all) => m && all.indexOf(m) === idx);
}

/** The set to use when the router cannot be reached, so an outage narrows selection instead of refusing every run. */
export function fallbackModels(configured) {
  return [configured, 'claude-sonnet-4-6', 'claude-haiku-4-5']
    .filter((m, idx, all) => m && all.indexOf(m) === idx);
}

/**
 * Ask the router what it serves. Returns null on any failure, so the caller keeps whatever it already had.
 *
 * `fetchImpl` is injectable ONLY so a test can drive the failure paths, which is the whole point: a router that answers
 * 500, or answers with an empty list, must not empty the selectable set.
 */
export async function fetchRouterModels({ baseUrl, key, configured, timeoutMs = 8000, fetchImpl = fetch }) {
  const base = String(baseUrl || '').replace(/\/+$/, '');
  if (!base) {
    return null;
  }
  const res = await fetchImpl(base + '/v1/models', {
    headers: key ? { Authorization: 'Bearer ' + key } : {},
    signal: AbortSignal.timeout(timeoutMs),
  });
  if (!res.ok) {
    throw new Error('HTTP ' + res.status);
  }
  return modelsFromRouterPayload(await res.json(), configured);
}
