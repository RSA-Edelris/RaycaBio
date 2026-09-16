/**
 * WHAT A RUN ACTUALLY COST, priced from the router's own numbers.
 *
 * MEASURED DEFECT THIS FIXES, reported by the operator as "the session stops and said you reached spending limit".
 *
 * The run stopped at a recorded $15.1690 against a $15 cap after 52 turns and 5.4 minutes. The router's ledger for the
 * same window shows the truth: 72 calls to bedrock/qwen.qwen3-coder-480b-a35b-v1:0, 4,135,528 input tokens, 18,828
 * output tokens, $0.9437. The platform charged SIXTEEN TIMES what the work cost and stopped the study for it.
 *
 * WHY. The recorded figure was `total_cost_usd` from the SDK's result message. The SDK prices a run from its own table,
 * which it looks up by canonical model id, and the shipped bundle contains no non-Claude model names at all. So Qwen3
 * tokens were priced at Claude rates. The arithmetic confirms it: 4.13M input at $3/M plus 18.8k output at $15/M is
 * about $12.7 before cache-creation pricing, against $0.94 at Qwen's real $0.22/M and $1.80/M.
 *
 * The cheapest model in the fleet exhausted the budget fastest, which is the opposite of what a cost control is for.
 *
 * SO THE PRICES COME FROM THE ROUTER, which is the thing that actually pays. It publishes per-token costs per model on
 * /model/info, declared in the deployment's own config, and the SDK publishes accurate TOKEN COUNTS per model on every
 * result message. Counts from the SDK, prices from the router, arithmetic here. Nothing is assumed about either.
 */

/** Per-token prices for one model. Missing cache prices fall back to the input rate, which is what a model without
 *  prompt caching charges for those tokens anyway. */
function pricesFor(modelInfo) {
  const num = (v) => (Number.isFinite(Number(v)) ? Number(v) : null);
  const input = num(modelInfo?.input_cost_per_token);
  const output = num(modelInfo?.output_cost_per_token);
  if (input === null && output === null) {
    return null;
  }
  return {
    input: input ?? 0,
    output: output ?? 0,
    cacheRead: num(modelInfo?.cache_read_input_token_cost) ?? input ?? 0,
    cacheWrite: num(modelInfo?.cache_creation_input_token_cost) ?? input ?? 0,
    maxInput: num(modelInfo?.max_input_tokens),
  };
}

/** The price table implied by a router /model/info listing, or null when it carries nothing usable. */
export function pricesFromRouterPayload(body) {
  const rows = Array.isArray(body?.data) ? body.data : [];
  const out = {};
  for (const row of rows) {
    const name = String(row?.model_name ?? '').trim();
    const p = pricesFor(row?.model_info);
    if (name && p) {
      out[name] = p;
    }
  }
  return Object.keys(out).length ? out : null;
}

/** Ask the router for its prices. Throws on a bad response so the caller can keep what it had. */
export async function fetchRouterPrices({ baseUrl, key, timeoutMs = 8000, fetchImpl = fetch }) {
  const base = String(baseUrl || '').replace(/\/+$/, '');
  if (!base) {
    return null;
  }
  const res = await fetchImpl(base + '/model/info', {
    headers: key ? { Authorization: 'Bearer ' + key } : {},
    signal: AbortSignal.timeout(timeoutMs),
  });
  if (!res.ok) {
    throw new Error('HTTP ' + res.status);
  }
  return pricesFromRouterPayload(await res.json());
}

/**
 * Match a usage key to a price table entry.
 *
 * The SDK reports usage under whatever model string went out, which may carry a provider prefix or a Bedrock inference
 * profile id. An exact name wins; otherwise the longest table name contained in the key wins, so `qwen3-coder-480b`
 * matches `bedrock/qwen.qwen3-coder-480b-a35b-v1:0` and the shorter `qwen3-235b` cannot steal it.
 */
export function priceKeyFor(usageKey, prices) {
  const key = String(usageKey || '');
  if (!key) {
    return null;
  }
  if (prices[key]) {
    return key;
  }
  const lower = key.toLowerCase();
  let best = null;
  for (const name of Object.keys(prices)) {
    if (lower.includes(name.toLowerCase()) && (!best || name.length > best.length)) {
      best = name;
    }
  }
  return best;
}

/**
 * What a run cost, from the SDK's per-model token counts and the router's prices.
 *
 * REPORTS WHAT IT COULD NOT PRICE rather than quietly returning a smaller number. A model missing from the table is a
 * condition somebody has to fix, and an under-report is the same class of error as the over-report this replaces.
 */
export function costOf(modelUsage, prices) {
  const usage = modelUsage && typeof modelUsage === 'object' ? modelUsage : {};
  const table = prices && typeof prices === 'object' ? prices : {};
  let usd = 0;
  const priced = [];
  const unpriced = [];
  for (const [key, u] of Object.entries(usage)) {
    const n = (v) => (Number.isFinite(Number(v)) ? Number(v) : 0);
    const inTok = n(u?.inputTokens);
    const outTok = n(u?.outputTokens);
    const cacheRead = n(u?.cacheReadInputTokens);
    const cacheWrite = n(u?.cacheCreationInputTokens);
    const name = priceKeyFor(key, table);
    if (!name) {
      unpriced.push({ model: key, inputTokens: inTok, outputTokens: outTok });
      continue;
    }
    const p = table[name];
    const cost = inTok * p.input + outTok * p.output + cacheRead * p.cacheRead + cacheWrite * p.cacheWrite;
    usd += cost;
    priced.push({ model: key, pricedAs: name, usd: cost, inputTokens: inTok, outputTokens: outTok });
  }
  return { usd, priced, unpriced, complete: unpriced.length === 0 && priced.length > 0 };
}
