#!/usr/bin/env python3
"""Consult procedural memory before the model's first turn.

SAME BRIDGE PATTERN AS governance_bridge.py AND runstore_bridge.py: a long-lived Python subprocess
speaking JSON lines. One process, kept alive, because starting an interpreter per call would add a
second to every dispatch.

SEPARATE FROM THE OTHER TWO for the same reason runstore is separate from governance: memory's failure
posture is DEGRADE HONESTLY (say that consultation failed), while governance ALLOWS on failure and
runstore REQUIRES success. Mixing them means a memory outage takes down the runstore or the governance
layer crashes the memory path.

CALLS memprefetch.prefetch_message, which ALREADY handles all failure paths honestly: when memory is
unreachable the returned message says so in its own text. This bridge adds nothing clever; it is a
thin JSON-lines wrapper around the existing mechanism.
"""

from __future__ import annotations

import json
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from env_select import resolve_src  # noqa: E402  the one place environment is decided
sys.path.insert(0, resolve_src())


def log(msg: str) -> None:
    sys.stderr.write("[memory] %s\n" % msg)
    sys.stderr.flush()


def _prefetch(p: dict) -> dict:
    """Call memprefetch.prefetch_message and return the result."""
    from modulon.engine import memprefetch

    task = str(p.get("task") or "")
    k = int(p.get("k") or memprefetch.DEFAULT_K)
    if not task:
        return {"ok": False, "error": "no task text"}
    result = memprefetch.prefetch_message(task, k=k)
    return {"ok": True, **result}


def _script_slug(p: dict) -> dict:
    """Derive a readable name from code using the platform's own step-name deriver.

    REUSED FROM execisolate._script_slug, not reimplemented. The function extracts a human-readable
    slug from a Python script's opening comment or first call. Used as the fallback title when the
    model writes no leading comment.
    """
    from modulon.engine.execisolate import _script_slug as slug_fn

    code = str(p.get("code") or "")
    if not code:
        return {"ok": True, "slug": ""}
    return {"ok": True, "slug": slug_fn(code)}


def main() -> int:
    ops = {
        "prefetch": _prefetch,
        "script_slug": _script_slug,
    }
    log("ready")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:  # noqa: BLE001
            continue
        rid = req.get("id")
        op_name = str(req.get("op") or "")
        fn = ops.get(op_name)
        if fn is None:
            out = {"error": "no_such_op", "op": op_name}
        else:
            try:
                out = fn(req)
            except Exception:  # noqa: BLE001
                out = {"error": "bridge_failed", "detail": traceback.format_exc(limit=2)[:600]}
        sys.stdout.write(json.dumps({"id": rid, "result": out}, default=str) + "\n")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
