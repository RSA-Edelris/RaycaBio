/**
 * env.mjs: the ONE place that decides which environment this process is, and what that implies.
 *
 * WHY THIS EXISTS, and it is not a style preference. Nine files in this directory each resolved the engine's
 * source tree the same way:
 *
 *     const SRC = process.env.RAYCA_SRC || '/home/ubuntu/rayca-modulon-dev/src';   // five .mjs
 *     sys.path.insert(0, os.environ.get("RAYCA_SRC", "/home/ubuntu/rayca-modulon-dev/src"))  // four .py
 *
 * The default is the DEVELOPMENT tree. So a process started with RAYCA_SRC unset runs the code somebody is
 * editing, in production, against production's databases. MEASURED consequence (docs/design/
 * what-we-have-and-how-it-connects.md): the live rayca-modulon-max service runs out of the dev tree, so editing
 * a file changes in-flight researcher runs and there is no version boundary around a run. That is the defect
 * this module removes at its root: not by changing one caller, but by giving every caller a single resolver
 * whose default is SAFE.
 *
 * THE INVERSION THAT MATTERS. The default here is `production`, not `development`. A missing or mistyped
 * RAYCA_ENV can no longer silently run the dev tree in production. The only way to run development code is to
 * ASK for it, on a host configured to be development. A safe default fails towards "do not touch production's
 * source or data", which is the direction a mistake should fall.
 *
 * TWO LAYERS OF OVERRIDE, deliberately. RAYCA_ENV picks a whole profile from the table below. An individual
 * field (RAYCA_SRC, MAX_DB, ...) may still override a single value, because operations sometimes needs to point
 * one thing somewhere unusual without inventing a new environment. Precedence: explicit per-field env var >
 * RAYCA_ENV profile > safe production default.
 */

// The one table. Adding an environment is adding a row here, not editing nine files.
const PROFILES = {
  production: {
    src: '/home/ubuntu/rayca-modulon/src',                 // the PROMOTED tree that deploy-engine.py installs
    py: '/home/ubuntu/rayca-runtime/.venv/bin/python3',
    db: '/var/lib/rayca/modulon-max.sqlite',
    port: 8310,
    bind: '127.0.0.1',
    secretsFile: '/etc/rayca/modulon-max.env',
  },
  development: {
    src: '/home/ubuntu/rayca-modulon-dev/src',             // the tree under active edit
    py: '/home/ubuntu/rayca-runtime/.venv/bin/python3',
    db: '/var/lib/rayca/modulon-max-dev.sqlite',           // NEVER the production database
    port: 8310,
    bind: '127.0.0.1',
    secretsFile: '/etc/rayca/modulon-max-dev.env',
  },
};

/** Which profile is in force. Unknown or unset resolves to production, and says so. */
export function environment(env = process.env) {
  const raw = (env.RAYCA_ENV || '').trim().toLowerCase();
  if (raw && !PROFILES[raw]) {
    // A typo must be loud, not silently safe-defaulted into a surprise. But it still defaults to production,
    // because the alternative (defaulting to development on a typo) is the exact failure this module prevents.
    console.error(
      '[env] RAYCA_ENV=%s is not one of %s; treating as production',
      raw, Object.keys(PROFILES).join(', '),
    );
    return 'production';
  }
  return PROFILES[raw] ? raw : 'production';
}

/** Resolve the whole configuration for this process. Per-field env vars still win, for operational escape hatches. */
export function resolveEnv(env = process.env) {
  const name = environment(env);
  const p = PROFILES[name];
  return {
    name,
    src: env.RAYCA_SRC || p.src,
    py: env.RAYCA_PY || p.py,
    db: env.MAX_DB || p.db,
    port: Number(env.MAX_PORT || p.port),
    bind: env.MAX_BIND || p.bind,
    secretsFile: env.RAYCA_SECRETS_FILE || p.secretsFile,
  };
}

export const PROFILE_NAMES = Object.keys(PROFILES);
