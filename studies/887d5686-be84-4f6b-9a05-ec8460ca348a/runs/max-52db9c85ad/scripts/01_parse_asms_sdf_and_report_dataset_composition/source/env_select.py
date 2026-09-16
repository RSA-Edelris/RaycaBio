#!/usr/bin/env python3
"""env_select.py: the ONE place the Python bridges decide which environment they are.

This is the counterpart of env.mjs. Four Python files in this directory each did:

    sys.path.insert(0, os.environ.get("RAYCA_SRC", "/home/ubuntu/rayca-modulon-dev/src"))

defaulting to the DEVELOPMENT tree. A bridge spawned with RAYCA_SRC unset therefore imported the code
under active edit, in production. This module removes that: the default is PRODUCTION, and development
must be asked for. See env.mjs for the full reasoning; this mirrors its table exactly so the Node engine
and the Python it spawns can never disagree about which tree they are.

Usage at the top of a bridge, replacing the hardcoded insert:

    from env_select import resolve_src
    import sys
    sys.path.insert(0, resolve_src())
"""

from __future__ import annotations

import os
import sys
from typing import Dict, Mapping

# The one table. Kept byte-for-byte consistent with PROFILES in env.mjs.
PROFILES: Dict[str, Dict[str, str]] = {
    "production": {
        "src": "/home/ubuntu/rayca-modulon/src",
        "db": "/var/lib/rayca/modulon-max.sqlite",
        "secrets_file": "/etc/rayca/modulon-max.env",
    },
    "development": {
        "src": "/home/ubuntu/rayca-modulon-dev/src",
        "db": "/var/lib/rayca/modulon-max-dev.sqlite",
        "secrets_file": "/etc/rayca/modulon-max-dev.env",
    },
}


def environment(env: Mapping[str, str] = os.environ) -> str:
    """Which profile is in force. Unknown or unset resolves to production, loudly on a typo."""
    raw = (env.get("RAYCA_ENV", "") or "").strip().lower()
    if raw and raw not in PROFILES:
        sys.stderr.write(
            "[env] RAYCA_ENV=%s is not one of %s; treating as production\n"
            % (raw, ", ".join(PROFILES))
        )
        return "production"
    return raw if raw in PROFILES else "production"


def resolve_src(env: Mapping[str, str] = os.environ) -> str:
    """The source tree to import. Explicit RAYCA_SRC wins; else the profile; else production."""
    return env.get("RAYCA_SRC") or PROFILES[environment(env)]["src"]


def resolve_db(env: Mapping[str, str] = os.environ) -> str:
    return env.get("MAX_DB") or PROFILES[environment(env)]["db"]
