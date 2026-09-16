/**
 * WHAT A USER IS TOLD WHEN A RUN DOES NOT FINISH.
 *
 * THE OPERATOR, after watching a client stop a run: "when we stop the session, a message appear in conversation and say claude code
 * is stoped, we do not want to show claude code name to our users please correct it".
 *
 * WHAT THEY SAW, taken from the runs table rather than from memory:
 *
 *   "Claude Code process aborted by user"
 *   "Claude Code returned an error result: API Error: Sonnet 4.6 can't help with this. Start a new session to continue.
 *    Learn more: https://www.anthropic.com/legal/aup"
 *
 * The second is the worse of the two and nobody had reported it: it names the vendor, names the model, links the vendor's acceptable
 * use policy, and instructs a paying client to "start a new session" in a product they are not using.
 *
 * === WHY THIS IS A WHITELIST AND NOT A WORD FILTER ===
 *
 * The obvious fix is to strip "Claude Code" out of the string. That fix is wrong, and it is worth being precise about why, because it
 * looks like it works: it protects against exactly the two messages I happened to measure today. The SDK's text is not ours. It
 * changes when the SDK is upgraded, it varies by model, and it embeds provider names, model versions and URLs that we never chose to
 * publish. A filter defends against the phrasings someone thought of; the next release supplies a phrasing they did not.
 *
 * So NOTHING FROM THE UNDERLYING ERROR REACHES THE READER. This function classifies the failure and then returns the platform's OWN
 * sentence for that class. Unrecognised failures get the generic sentence. A vendor name cannot leak through a function that never
 * copies its input into its output -- which is a property, testable directly, rather than a list to keep up to date.
 *
 * THE RAW TEXT IS NOT DISCARDED. The caller logs it, so an operator reading the journal still has the real message. Only the
 * conversation is sanitised, and the diagnosis survives where diagnosis belongs.
 */

/**
 * The classes we can actually explain. Order matters only in that the first match wins, and the patterns are disjoint in practice.
 * `test` inspects the raw text; `text` is what a reader sees and shares nothing with it.
 */
const CLASSES = [
  {
    kind: 'stopped',
    /* A deliberate stop. The SDK reports the user's own abort as a process error, which is why a click on `stop` read as a
       failure -- it was reported through the same channel as a crash. */
    test: (s) => /abort|cancel|sigterm|sigint|interrupt/i.test(s),
    text: 'Stopped at your request. Everything produced up to this point is kept.',
  },
  {
    kind: 'declined',
    /* The reasoning model refused the request on its provider's usage policy. Worth saying plainly, because the reader can act on
       it, but said without naming the provider, the model or its policy page. */
    test: (s) => /can't help with this|cannot help with this|usage polic|\baup\b|refus/i.test(s),
    text:
      'The reasoning model declined to continue with this request. Rephrasing the objective, or starting a fresh conversation, ' +
      'usually clears it.',
  },
  {
    kind: 'budget',
    test: (s) => /budget|credit|quota|spend limit|max_budget/i.test(s),
    text: 'The run reached its spending limit and stopped. Raise the limit for this workspace to let it continue further.',
  },
  {
    kind: 'timeout',
    test: (s) => /timeout|timed out|etimedout|deadline/i.test(s),
    text: 'The run took longer than its time limit and stopped. Narrowing the objective into smaller steps usually helps.',
  },
  {
    kind: 'capacity',
    /* Upstream capacity and transport faults. A reader can only wait, so say that and nothing more. */
    test: (s) => /overloaded|rate limit|429|503|502|econnreset|socket hang up|fetch failed|enotfound/i.test(s),
    text: 'The run stopped because the reasoning service was briefly unavailable. Running it again is usually enough.',
  },
  {
    kind: 'unentitled',
    /* MEASURED on this deployment: three Bedrock models were not granted on the account, and the upstream words that as the model
       "not being available", which reads to a client as the platform being broken. */
    test: (s) => /not available for this account|not authorized|accessdenied|invalid api key|unauthorized|401|403/i.test(s),
    text:
      'The run stopped because the selected model is not enabled for this workspace. Choosing another model, or asking an ' +
      'administrator to enable it, will clear this.',
  },
];

const GENERIC = 'The run stopped on an internal error before it could finish. Everything produced up to this point is kept.';

/**
 * Classify a thrown failure and return the sentence a reader should see.
 *
 * @param {unknown} err anything a `catch` can receive
 * @returns {{ kind: string, text: string, stopped: boolean, raw: string }}
 *   `raw` is for logs only and MUST NOT be sent to a client. `stopped` marks a deliberate stop, which is not a fault.
 */
export function publicFailure(err) {
  const raw = String((err && (err.message ?? err.detail)) || err || '').slice(0, 2000);
  const hit = CLASSES.find((c) => c.test(raw));
  return {
    kind: hit ? hit.kind : 'internal',
    text: hit ? hit.text : GENERIC,
    stopped: hit ? hit.kind === 'stopped' : false,
    raw,
  };
}

/** Every sentence this module is capable of emitting, so a test can assert the output is always one of them. */
export const PUBLIC_TEXTS = Object.freeze([...CLASSES.map((c) => c.text), GENERIC]);

export default publicFailure;
