#!/usr/bin/env python3
"""Expose the Rayca Modulon platform to any MCP client, over stdio.

WHY THIS EXISTS. The platform's assets -- 799 containerised tools, 92 Nextflow pipelines, 142 skills, 122 personas,
62 databases, the memory stack, the lineage emitter, both HPC clusters -- are all reachable from Python, through a set
of verbs the engine registers as `ToolSpec`s. This server republishes those same verbs over the Model Context Protocol
so that an agent loop written by someone else can drive the platform without any of it being ported.

THE VERBS ARE THE DOORWAY, NOT THE INVENTORY. There are roughly sixty verbs and 2,318 registry records. The records
are NOT published individually and must not be: sixty schemas fit in a prompt and 2,318 do not. `find_capability`
searches the registry and the dispatch verbs run what it finds, which is the same search-then-run path the engine's
own model takes. This is the one piece of architecture Modulon already had in common with Claude Code, whose
`ToolSearchTool` exists for exactly this reason.

DERIVED, NOT LISTED. The verb set is discovered by walking `modulon.engine` and `modulon.governance` for callables
named `*_tool_spec` / `*_tool_specs`, then calling the ones whose arguments can be satisfied. A hand-written list
would go stale the first time a verb was added -- which is exactly how `pipelines.py` stayed unreachable from
anywhere for the life of the project despite being catalogued.

ISOLATION. This process does NOT touch the running engine. It imports the same library, opens its own run context and
writes to the same registry and databases the engine reads. It is a second reader of the platform, not a second
engine, and the service on port 8201 is unaffected by anything here.
"""

from __future__ import annotations

import ast
import csv
import inspect
import json
import os
import shutil
import pkgutil
import re
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable, Dict, List, Optional, Tuple

# The engine's own source tree. Resolved by env_select from RAYCA_ENV (default: production), so an
# unset environment can never silently import the dev tree in production. See env_select.py / env.mjs.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from env_select import resolve_src  # noqa: E402  the one place environment is decided
sys.path.insert(0, resolve_src())

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "rayca-modulon"
SERVER_VERSION = "0.1.0"


def _log(msg: str) -> None:
    """Diagnostics go to stderr. stdout is the protocol channel and must carry nothing else."""
    sys.stderr.write("[rayca-mcp] %s\n" % msg)
    sys.stderr.flush()



# --------------------------------------------------------------------------------------------------------------------
# Reporting every dispatch back to the engine
# --------------------------------------------------------------------------------------------------------------------

CALLBACK = os.environ.get("RAYCA_MAX_CALLBACK", "").strip()
# The bearer the engine requires on every path but its two health probes. Without it each callback returns 401 and,
# because these functions swallow failures so a reporting problem can never fail a tool call, the loss is silent.
_KEY = os.environ.get("RAYCA_SERVE_KEY", "").strip()


def _headers() -> Dict[str, str]:
    h = {"content-type": "application/json"}
    if _KEY:
        h["authorization"] = "Bearer " + _KEY
    return h
RUN_ID = os.environ.get("RAYCA_RUN_ID", "").strip()
AGENT = os.environ.get("RAYCA_AGENT", "lead").strip() or "lead"


def _durable_job_fallback(name: str, args: Any, out: Any) -> Any:
    """Answer a cluster job question from the engine's durable record when this process has no memory of it.

    MEASURED, twice, and the second time on my own half-finished fix. `governance/cluster.py` keeps its job table in a
    module-level dict, and this server is spawned PER QUERY, so a job submitted by an earlier run is unknown to a later
    one: `check_cluster_job 6102566` answered "this run did not submit job 6102566, so there is nothing to report on"
    about a job that was queued, real, and being watched.

    The engine now records every cluster job in sqlite and serves it at /max/job/:id, which is what makes the answer
    outlive the run. This is the piece that was missing: the VERB the model calls still read the dict. Making the record
    durable and leaving the verb reading memory fixed the storage and not the question.

    ONLY ON A MISS, and only for that one error. A job this process did submit is answered by the live poll above, which
    is fresher; this fills in the gap rather than replacing anything. Any other failure is returned untouched.
    """
    try:
        if str(name or "") not in ("check_cluster_job", "cancel_cluster_job"):
            return out
        if not isinstance(out, dict) or out.get("error") != "unknown_job":
            return out
        jid = ""
        if isinstance(args, dict):
            jid = str(args.get("job_id") or "").strip()
        if not jid or not CALLBACK:
            return out
        base = CALLBACK.rsplit("/", 1)[0]
        req = urllib.request.Request(base + "/job/" + urllib.parse.quote(jid),
                                     headers=_headers(), method="GET")
        with urllib.request.urlopen(req, timeout=8) as fh:
            rec = json.loads(fh.read().decode() or "{}")
        if not isinstance(rec, dict) or not rec.get("job_id"):
            return out
        files = []
        try:
            files = json.loads(rec.get("files") or "[]") or []
        except Exception:  # noqa: BLE001
            files = []
        return {
            "ok": True,
            "job_id": rec.get("job_id"),
            "cluster": rec.get("cluster") or "",
            "host": rec.get("host") or "",
            "state": rec.get("state") or "unknown",
            # The scheduler's own word, so "pending" is not read as "running".
            "scheduler_state": rec.get("scheduler_state") or "",
            "queued": (rec.get("scheduler_state") or "") in ("pending", "configuring", "requeued"),
            "files": files,
            "analysis_run": rec.get("analysis_run") or "",
            "detail": ("this job was submitted by an earlier run and is being followed by the engine's watcher, "
                       "so its state is reported from the engine's own record"),
        }
    except Exception:  # noqa: BLE001 - a fallback that fails leaves the original answer, which is honest
        return out


def job_submitted(tool: str, gpu: bool, image: str) -> None:
    """Tell the engine a container job has STARTED, while it is still running.

    THE OPERATOR, having watched RFdiffusion run on the A100 while the panel said the dispatch never reached a
    container: the jobs section should "show the jobs once submitted and in real time show the resource usage on the vm
    and also say the name of the VM it is running on".

    WHY NOTHING ARRIVED BEFORE. The Jobs panel was built from the `[dispatch]` marker, which a tool prints when it
    EXITS, so a row could not exist while the job ran and there was nowhere to hang the host or the elapsed time.
    Two halves of the answer were already written and never joined: `dispatch.announce_dispatch` spools a
    `dispatch_submitted` row at submission, and `run_isolated` has an `on_live` callback that pumps that spool every
    0.25 seconds. This function is what the callback calls.

    THE HOST IS NAMED HERE, not at the source, because `announce_dispatch` reports what the tool is and this end knows
    where it goes: the same `RAYCA_GPU_HOST` the dispatcher resolves, read from the platform rather than repeated.
    """
    if not CALLBACK or not RUN_ID or not tool:
        return
    host = ""
    if gpu:
        try:
            from modulon.engine.dispatch import GPU_HOST
            host = str(GPU_HOST or "")
        except Exception:  # noqa: BLE001
            host = ""
    try:
        body = json.dumps({
            "run_id": RUN_ID, "agent": AGENT, "tool": str(tool),
            "gpu": bool(gpu), "image": str(image or ""), "host": host,
        }).encode()
        req = urllib.request.Request(
            CALLBACK.rsplit("/", 1)[0] + "/job", data=body,
            headers=_headers(), method="POST")
        urllib.request.urlopen(req, timeout=5).read()
    except Exception:  # noqa: BLE001
        # A job must not fail because its announcement did not land.
        pass


class _LiveDispatchSpool:
    """Report a container dispatch WHILE IT RUNS, from a process that is running it itself.

    THE OPERATOR: "when the job get dispatched the job section doesn't show it as runnnign job, after it is done, then it
    appears there as completed job ... i want the job section to be synced with all the running job in real time."

    WHY IT WAS INVISIBLE, and it is not the reason the old comment here gave. `announce_dispatch` writes to the narration
    SPOOL, and the spool path comes from the `RAYCA_NARRATION_SPOOL` environment variable, which narrate.py documents as
    "set by the parent before dispatch; absent in the parent itself". In this process it is unset, so `_spool` returns
    False and the submission is not merely undrained, it is never WRITTEN. Nothing was lost in transit because nothing was
    ever recorded.

    MEASURED: across fourteen days, 10 of 88 completed container jobs had no live submission on the tape at all, and every
    one of them went through this route. Since 08-28 this route is how the model reaches containers, so the share is
    growing, not shrinking.

    SO THE PROCESS BECOMES ITS OWN PARENT for the length of the call: point the variable at a real file, poll that file
    while the work happens, and forward what appears. This is exactly what `run_isolated` does for a child through
    `on_live`, and reusing the mechanism means the submission, the beats, the GPU sample and the container name all arrive
    by the route that already works, with no second channel to keep in step.

    NOT A TICKET. The previous note said making this live "means making the dispatch hand back a ticket instead of
    blocking, which is a larger change to the tool's contract". That was true of the approach it had in mind and is not
    needed: the verb stays synchronous and its contract is untouched. Only the reporting becomes live.

    NEVER FAILS THE WORK. Every step is best effort, in the same spirit as the spool it borrows: if the file cannot be
    made or the thread cannot start, the dispatch runs exactly as it does today and the panel is merely late again.
    """

    #: How often to look. The container watcher beats every 15 s, so this only has to be small next to that; 0.5 s is
    #: what `run_isolated` uses for the same job and there is no reason for a second number.
    POLL_S = 0.5

    def __init__(self) -> None:
        self._path = ""
        self._prev = None
        self._stop = None
        self._thread = None
        self._seen = 0

    def __enter__(self) -> "_LiveDispatchSpool":
        try:
            import tempfile
            import threading

            fd, self._path = tempfile.mkstemp(prefix="rayca-live-", suffix=".jsonl")
            os.close(fd)
            # REMEMBERED, so a nested call restores rather than clears. `None` and "" are different states here.
            self._prev = os.environ.get("RAYCA_NARRATION_SPOOL")
            os.environ["RAYCA_NARRATION_SPOOL"] = self._path
            self._stop = threading.Event()
            self._thread = threading.Thread(target=self._poll, daemon=True)
            self._thread.start()
        except Exception:  # noqa: BLE001 - reporting must never be more dangerous than silence
            self._teardown()
        return self

    def _forward(self) -> None:
        """Send the rows that appeared since the last look. Reads without consuming."""
        try:
            from modulon.engine import narrate

            rows = narrate.drain_spool(self._path, consume=False)
        except Exception:  # noqa: BLE001
            return
        # COUNTED RATHER THAN CLEARED, because the file must survive for the authoritative post-exit drain and because
        # re-sending a beat would put a second row in the panel for one container.
        fresh, self._seen = rows[self._seen:], len(rows)
        for row in fresh:
            if not isinstance(row, dict):
                continue
            try:
                kind = row.get("kind")
                if kind == "dispatch_submitted":
                    job_submitted(str(row.get("tool") or ""), bool(row.get("gpu")), str(row.get("image") or ""))
                elif kind == "dispatch_progress":
                    job_progress(row)
            except Exception:  # noqa: BLE001
                continue

    def _poll(self) -> None:
        while self._stop is not None and not self._stop.is_set():
            self._forward()
            self._stop.wait(self.POLL_S)

    def _teardown(self) -> None:
        try:
            if self._stop is not None:
                self._stop.set()
            if self._thread is not None:
                self._thread.join(timeout=2.0)
        except Exception:  # noqa: BLE001
            pass
        try:
            if self._prev is None:
                os.environ.pop("RAYCA_NARRATION_SPOOL", None)
            else:
                os.environ["RAYCA_NARRATION_SPOOL"] = self._prev
        except Exception:  # noqa: BLE001
            pass
        try:
            if self._path:
                os.unlink(self._path)
        except Exception:  # noqa: BLE001
            pass
        self._stop = None
        self._thread = None
        self._path = ""

    def __exit__(self, *exc: Any) -> bool:
        # ONE LAST LOOK before going, so a submission written microseconds before the verb returned is not dropped on
        # the floor by a poll that had already happened.
        try:
            if self._path:
                self._forward()
        except Exception:  # noqa: BLE001
            pass
        self._teardown()
        return False


def _announce_container_job(out: Any) -> None:
    """Put a DIRECTLY dispatched container job in the Jobs panel.

    THE OPERATOR, on a boltzgen run that really did execute on the A100: "even the failed botzgen run did not appear in
    the job section!" They were right, and it was a consequence of publishing `run_aidd_tool` as a verb.

    HOW THE PANEL USED TO BE FED, and why the new route missed it. A container dispatch spools a `dispatch_submitted`
    row, and `run_isolated` drains that spool every 0.25 s through `on_live`, which calls `job_submitted`. That drain
    belongs to the `run_python` CHILD process. Until 08-28 the model reached containers by writing python, so every
    dispatch went through that child and every job appeared. `run_aidd_tool` runs the dispatch in THIS process instead,
    where nothing drains the spool, so a real job on a real GPU left no row at all. MEASURED on run max-e38c2c37ca:
    `boltzgen rc=1 (GPU) in 27.6s`, and `job.submitted` events in that run: zero.

    DERIVED FROM THE RESULT, NOT FROM A LIST OF VERB NAMES. Any verb whose result carries a container's identity and a
    return code is a container dispatch, so a tool added later is covered without touching this function.

    ONE HONEST LIMITATION, stated because the panel is about live work: this reports the job when the call RETURNS, not
    while it runs, because the verb is synchronous and there is nothing to report until it finishes. The row is
    therefore complete rather than live. Making it live means making the dispatch hand back a ticket instead of
    blocking, which is a larger change to the tool's contract and is not this fix.
    """
    if not isinstance(out, dict):
        return
    tool = str(out.get("tool_id") or "")
    if not tool or "rc" not in out:
        return
    try:
        job_submitted(tool, bool(out.get("gpu")), str(out.get("image") or ""))
        row = {
            "kind": "dispatch_progress",
            "tool": tool,
            "image": str(out.get("image") or ""),
            "gpu": bool(out.get("gpu")),
            "elapsed_s": out.get("duration_s"),
            "rc": out.get("rc"),
            "state": "failed" if out.get("rc") not in (0, None) else "done",
        }
        detail = out.get("summary") or out.get("detail") or out.get("error")
        if detail:
            row["detail"] = " ".join(str(detail).split())[:300]
        job_progress(row)
    except Exception:  # noqa: BLE001 - a missing panel row must never fail the tool that ran
        pass


def job_progress(row: Dict[str, Any]) -> None:
    """Update a running container job: how long it has been going, and what the machine is doing.

    The operator asked the jobs panel to "in real time show the resource usage on the vm and also say the name of the VM
    it is running on". `_watch_container` in the platform's dispatcher already beats with the log tail and elapsed time,
    and now samples the host's GPU on the same beat. This forwards that beat to the engine.

    SENT TO THE SAME ENDPOINT as the submission, keyed by tool, because these are two reports about ONE job and the
    panel has to be able to join them. A second endpoint would invite two rows for one container.
    """
    if not CALLBACK or not RUN_ID:
        return
    tool = str(row.get("tool") or "")
    if not tool:
        return
    try:
        body = json.dumps({
            "run_id": RUN_ID, "agent": AGENT, "tool": tool,
            # THE OUTCOME, WHEN THERE IS ONE.
            #
            # THIS USED TO HARDCODE `state: "running"` AND DROP `rc` ENTIRELY, and that is why a finished job never
            # finished in the panel. `_announce_container_job` builds a completion row carrying rc and state=done,
            # hands it to this function, and every bit of the outcome was discarded on the way out. MEASURED across
            # the whole tape: 0 of 10,773 job events carry an rc, going back to 25 July.
            #
            # ASKED OF THE ROW rather than assumed, so a beat with nothing to report still says running while a row
            # that knows the outcome can say so. `rc` travels only when the row HAS one: absent means still going,
            # and sending a zero would read as success.
            "state": str(row.get("state") or "") or "running",
            **({"rc": int(row["rc"])}
               if isinstance(row.get("rc"), (int, float)) else {}),
            **({"detail": " ".join(str(row.get("detail")).split())[:300]}
               if row.get("detail") else {}),
            "elapsed_s": row.get("elapsed_s"),
            "container": str(row.get("container") or ""),
            "tail": str(row.get("output_tail") or "")[:4000],
            "host": str(row.get("host") or ""),
            "gpu_util_pct": row.get("gpu_util_pct"),
            "gpu_mem_used_mb": row.get("gpu_mem_used_mb"),
            "gpu_mem_total_mb": row.get("gpu_mem_total_mb"),
        }).encode()
        req = urllib.request.Request(
            CALLBACK.rsplit("/", 1)[0] + "/job", data=body,
            headers=_headers(), method="POST")
        urllib.request.urlopen(req, timeout=5).read()
    except Exception:  # noqa: BLE001
        pass


def progress(verb: str, seconds: float, tail: str) -> None:
    """One progress beat for a step that is still running.

    SEPARATE FROM `report` because a beat is not a result: it carries a partial tail that a later beat supersedes, and
    the engine must not record it as what the step returned.
    """
    if not CALLBACK or not RUN_ID:
        return
    try:
        body = json.dumps({
            "run_id": RUN_ID,
            "agent": AGENT,
            "verb": verb,
            "seconds": round(float(seconds), 1),
            # Bounded here as well as at the source, because this crosses a wire.
            "tail": str(tail or "")[:4000],
        }, default=str).encode()
        req = urllib.request.Request(CALLBACK.replace("/max/tool", "/max/progress"), data=body,
                                     headers=_headers(), method="POST")
        urllib.request.urlopen(req, timeout=3).read()
    except Exception:  # noqa: BLE001 - a lost beat is not a lost step
        pass


# The platform category of a written file -> the kind of science the step was doing.
#
# NOT A KEYWORD LIST, and the distinction matters. There is no table here from library or tool NAME to discipline:
# a list reading rdkit, alphafold, gnina is wrong the first time a study uses the fourth thing, and
# governance/toolkit.py:188 records that this platform deliberately built its matching "generic across the whole
# registry, with no per-domain keyword list to maintain". What this maps instead is the OUTPUT of
# governance/artifacts.classify, whose category vocabulary is finite, owned by the platform and already maintained
# there for the file manager. Adding a file type therefore teaches this at the same time.
#
# The evidence is what the step PRODUCED, which cannot be faked by how the code was written.
_CLASS_BY_CATEGORY = {
    "molecules": "structure",
    "images": "visualisation",
    "tables": "measurement",
    "documents": "composition",
}


def _written_row(path: Any) -> Dict[str, Any]:
    """One entry in `files_written`, built from a path.

    `appeared_since` reports WHAT APPEARED, by path, registering nothing. The name is the basename and the kind is what
    the platform's own classifier makes of it, so this stays in the vocabulary the file manager already uses rather than
    a second one invented here.
    """
    name = os.path.basename(str(path or ""))
    try:
        from modulon.governance import artifacts as _artifacts

        return {"name": name, "kind": _artifacts.classify(name) or ""}
    except Exception as err:  # noqa: BLE001
        # PRINTED, not swallowed: a missing classifier must not cost the model its list of files, but it must be seen.
        print("[files_written] could not classify %s: %s" % (name, err), file=sys.stderr)
        return {"name": name, "kind": ""}


def _operation_class(meta: Any, produced: Any) -> str:
    """What kind of science a step was, derived from observable effects only.

    Returns "" when the evidence does not say. AN ABSENT CLASS IS HONEST and the console falls back to its existing
    appearance; a guessed one would colour a card with a claim nothing supports.
    """
    m = meta if isinstance(meta, dict) else {}
    # Dispatch wins over everything written, because a step that sent work to a container or a GPU is an experiment
    # being run whatever it happened to bring back.
    if m.get("dispatch_submitted") or m.get("gpu") or m.get("job_id"):
        return "simulation"
    cats = []
    try:
        # Imported here rather than at module scope to match how `filereg` is taken in this file: this server starts
        # before the platform is guaranteed importable, and a top-level import would make that a startup failure.
        from modulon.governance import artifacts as _artifacts
    except Exception:  # noqa: BLE001
        return ""
    for r in (produced or []):
        try:
            # A PATH, as `appeared_since` returns. This read `r.get("name")` inside a SWALLOWING handler, so after
            # WS-30 T5 it did not crash here: it classified nothing, and every step that wrote files quietly became
            # "inspection". A silent wrong answer, beside the loud one that crashed.
            cats.append(_artifacts.classify(os.path.basename(str(r))))
        except Exception:  # noqa: BLE001
            pass
    # Most specific evidence first, in the order of the map, so a step that wrote both a structure and a log reads as
    # structural work rather than as whichever file the filesystem happened to list first.
    for cat, cls in _CLASS_BY_CATEGORY.items():
        if cat in cats:
            return cls
    # Ran and wrote nothing classifiable: it looked at something.
    return "inspection" if cats or produced is not None else ""


# `_push_file` WAS REMOVED, not left unused.
#
# It announced one registered file on the run's stream, and it was the right mechanism when only this verb registered
# anything. `PostToolUse` in server.mjs now registers and announces after EVERY tool, which is the seam that also catches
# Bash and Write, so keeping this made every file arrive twice: MEASURED
# ["aspirin_logp.csv", "001_aspirin_smiles.py", "aspirin_logp.csv", "001_aspirin_smiles.py"], and report.md twice again
# through the generic verb path. Two announcers for one fact is a bug waiting for the next reader.
def _with_explanation(out: Any, spec: Any) -> Any:
    """Attach the verb's published description to its result, when the result can carry one.

    Returns `out` untouched for anything that is not a dict, because wrapping a string result would change the shape
    the model reads and a cosmetic field is not worth that.
    """
    if not isinstance(out, dict):
        return out
    # THE CODE EXECUTION SUBSTRATE GETS NO EXPLANATION.
    #
    # Its published description is "Execute Python in the persistent session namespace and return its output", which is
    # mechanism rather than science and carries exactly the vocabulary the operator asked to be rid of: "all the
    # elements should be in the scientific wording not like Run_Python and Tool calling ... these are very bad for the
    # scientist user." MEASURED by a test that renders the card and scans its text: the word "Execute" reached the
    # screen through this field.
    #
    # The card loses nothing. Its title is the engine's own interpretation of what the step DID, which for these steps
    # is the informative part; the description would only restate that Python ran.
    #
    # IDENTIFIED BY IDENTITY, NOT BY NAME, so a rename cannot quietly reintroduce it: the substrate is whichever spec
    # dispatches into this module's own code runner.
    try:
        _fn = getattr(spec, "dispatch", None)
        # Unwrapped because a function reached through a class becomes a bound method and would fail an identity test
        # against the plain function. MEASURED: the first version of this check passed the substrate straight through.
        if getattr(_fn, "__func__", _fn) is _run_code:
            return out
    except Exception:  # noqa: BLE001
        pass
    try:
        desc = str(getattr(spec, "description", "") or "").strip()
    except Exception:  # noqa: BLE001
        return out
    if not desc:
        return out
    # First sentence or so. The full description can run to 4000 characters, which is documentation rather than a card
    # subtitle, and the reader wants to know what this step IS in one line.
    head = desc.split("\n\n")[0].strip()
    out.setdefault("explanation", head[:400])
    return out


def _recover_strays(src: str, cwd: str, since: float) -> list:
    """Bring files the step wrote OUTSIDE the session workspace into it.

    MEASURED, NOT HYPOTHETICAL. Asked to save a CSV and a chart, the model wrote
    `fig.savefig("/tmp/logp_chart.png")`. The chart was real and correct and the file manager stayed empty, because
    registration diffs the session workspace and /tmp is not it. That is the operator's complaint in full: "i feel the
    files are not appearing fast in the file manager ... it is like some files are not getting saves there".

    A PROMPT WOULD NOT FIX IT. Telling the model to use relative paths makes correct filing depend on the model
    remembering, and src/modulon/engine/memprefetch.py argues at length why an instruction is not a mechanism. This
    copies instead, so a study's outputs are filed whatever path the author chose.

    BOUNDED THREE WAYS, because copying arbitrary paths named in code would be a way to pull the filesystem into a
    session:
      - the path must appear as a literal in THIS step's own source, so nothing is discovered by scanning directories
      - it must have been created or modified DURING this step, which excludes every pre-existing system file
      - it must be a regular file under a size cap, so a device node or a huge dump is left alone
    """
    out = []
    try:
        tree = ast.parse(src)
    except Exception:  # noqa: BLE001 - the step ran, so this is only about reading it back
        return out
    seen = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        cand = node.value
        if not cand.startswith("/") or len(cand) > 400 or cand in seen:
            continue
        seen.add(cand)
        try:
            real = os.path.realpath(cand)
            # Already inside the workspace: registration will find it without help.
            if real.startswith(os.path.realpath(cwd) + os.sep):
                continue
            # A DIRECTORY LITERAL COUNTS TOO, because the path that gets written is often composed.
            #
            # MEASURED: `out = pathlib.Path("/home/ubuntu/rayca-modulon-dev/modulon-max")` then
            # `fig.savefig(out / "logp_barchart.png")`. The only literal in the source is the DIRECTORY, so a scan for
            # file paths finds nothing and the figure is lost. This is also how run output kept appearing inside the
            # repository itself and having to be gitignored after the fact.
            #
            # Only files whose mtime falls inside this step's window are taken, so pointing at a populated directory
            # recovers what this step wrote there and nothing else.
            targets = []
            if os.path.isdir(real):
                try:
                    for entry in sorted(os.listdir(real))[:200]:
                        targets.append(os.path.join(real, entry))
                except Exception:  # noqa: BLE001
                    continue
            else:
                targets.append(real)
            for t in targets:
                try:
                    if not os.path.isfile(t):
                        continue
                    st = os.stat(t)
                    if st.st_mtime < since - 1.0:
                        continue
                    if st.st_size > 64 * 1024 * 1024:
                        continue
                    dest = os.path.join(cwd, os.path.basename(t))
                    if os.path.exists(dest):
                        continue
                    shutil.move(t, dest)
                    out.append(os.path.basename(t))
                except Exception:  # noqa: BLE001
                    continue
        except Exception:  # noqa: BLE001 - a file that cannot be recovered is left where the author put it
            continue
    return out


def _looks_like_unsaved_results(text: str) -> bool:
    """Whether output reads like results that should have been written down.

    THREE SIGNALS, ALL FROM THE OUTPUT ITSELF, because the alternative is a list of verbs that ought to save and that
    list would be wrong for the first study nobody anticipated:
      - it is substantial, so a one line status is not scolded
      - it contains numbers, since a measurement is what there is to lose
      - it has several lines, which is what a table or a ranking looks like when printed
    """
    t = str(text or "")
    if len(t) < 200:
        return False
    if not any(ch.isdigit() for ch in t):
        return False
    lines = [ln for ln in t.splitlines() if ln.strip()]
    if len(lines) < 4:
        return False
    # At least a few lines must carry numbers, or this is prose that merely mentions a version.
    numeric_lines = sum(1 for ln in lines if any(ch.isdigit() for ch in ln))
    return numeric_lines >= 3


def _result_body(text: str) -> str:
    """The step's own output, with the engine's instrumentation removed.

    MEASURED ON THE FIRST REAL RUN OF THIS LAYER. The saved result held the study's table and then three paragraphs of
    `[note]` lines the harness appends to every call, explaining which names carry over and that files persist. That is
    the engine talking to the model. It is not a result, it does not belong in a file a scientist opens, and it broke
    table detection on an output that was otherwise a clean four column table.

    Nothing the model itself printed is removed here, so the fallback that writes output verbatim stays faithful.
    """
    lines = str(text or "").splitlines()
    return "\n".join(ln for ln in lines if not ln.lstrip().startswith("[note]"))


def _is_decoration(line: str) -> bool:
    """Whether a line is a rule under a header rather than data.

    `print` of a hand made table puts `-----` between the header and the rows, and markdown puts `|---|---|`. Those
    lines carry no values, and counting them as rows is what made a genuinely rectangular table look ragged.
    """
    stripped = str(line or "").strip()
    if not stripped:
        return False
    return all(ch in "-=+|_ \t" for ch in stripped)


def _table_rows(text: str) -> Optional[list]:
    """The output's own rows and columns, if it printed a table, else None.

    DERIVED FROM THE TEXT'S SHAPE, not from the verb that produced it or from a list of tools that print tables.
    A delimiter qualifies when it splits SEVERAL lines into the SAME number of at least two fields, which is what a
    table is and what prose is not. Candidates are tried widest-evidence first.

    POSITION ALIGNED OUTPUT IS DELIBERATELY NOT PARSED, and this is a decision rather than an omission.
    `print(df)` on a pandas frame aligns columns by character position with no delimiter, and its header names contain
    spaces of their own. Two attempts at reading it by column position both MANGLED the data on the real observed
    output: deriving boundaries from all lines merged four values into one field, and deriving them from the data rows
    alone sliced the header mid-word into `g/mol) cLogP` and `A (A2`. A results file whose column reads `180.16  1.31`
    is worse than the text it came from, so that shape now falls through to being written verbatim, which loses
    nothing. Anyone tempted to try again should know it has been tried twice.

    THE TWO-OR-MORE-SPACES CANDIDATE IS THE IMPORTANT ONE. `print(df)` on a pandas frame aligns columns with runs of
    spaces and carries no delimiter at all, and that is the single most common way a study prints its results here.
    Recognising it is what turns a printed frame into a file the reader can open as a table.
    """
    t = str(text or "")
    lines = [ln.rstrip() for ln in t.splitlines() if ln.strip() and not _is_decoration(ln)]
    if len(lines) < 2:
        return None
    best = None
    for split in (lambda ln: ln.split("\t"),
                  lambda ln: ln.split(","),
                  lambda ln: [c.strip() for c in ln.strip().strip("|").split("|")],
                  lambda ln: re.split(r"\s{2,}", ln.strip())):
        rows = [split(ln) for ln in lines]
        widths = {len(r) for r in rows}
        # EVERY LINE MUST AGREE, and this strictness is a correctness requirement rather than fastidiousness.
        #
        # MEASURED, and it is why the first version of this was dangerous. A printed pandas frame whose index and first
        # column are separated by a single space splits raggedly: on a six line frame the field counts were {5:4, 6:1,
        # 4:1}, and a majority rule accepted the modal width and returned FOUR of the six rows. That silently drops
        # compounds from a results table, which is worse than saving no table at all, because the file looks complete.
        #
        # So a table is only a table when the delimiter explains the whole output. Anything less is written verbatim as
        # text by the caller, which loses nothing. The bonus case is not worth a single lost row.
        if len(widths) == 1 and rows and len(rows[0]) >= 2:
            if best is None or len(rows) > len(best):
                best = rows
    return best


def step_title_for_results(src: str) -> str:
    """A name for this step, from the same slug that names the archived source script beside it.

    Deliberately the SAME source as the `source/NNN_*.py` filename, so a result and the code that produced it read as a
    pair in the file manager instead of as two unrelated files.
    """
    try:
        from modulon.engine.execisolate import _script_slug
        return _script_slug(str(src or "")).replace("_", " ")
    except Exception:  # noqa: BLE001
        return ""


def step_index_for_results(cwd: str) -> Optional[int]:
    """This step's position in the session, counted from the source scripts already archived.

    Counted rather than tracked, because the archive is the record every other reader uses and a counter held in this
    process would disagree with it the moment a member ran in a second process.
    """
    try:
        srcdir = os.path.join(cwd, "source")
        if os.path.isdir(srcdir):
            return len([f for f in os.listdir(srcdir) if f[:3].isdigit()]) + 1
    except Exception:  # noqa: BLE001
        return None
    return None


def _persist_results(text: str, cwd: str, step_title: str, step_seq: Optional[int]) -> Optional[str]:
    """Write this step's output into the workspace so a result is never lost to the transcript.

    THE PROBLEM THIS SOLVES, MEASURED TWICE. On the operator's imatinib run all eleven registered files were
    `kind=code` and the eleven scripts contained 71 `print` calls and zero writes. On the TKI run the file manager
    held six files, every one of them a `.py` source script, while the descriptors and ADMET predictions the study
    existed to produce were printed to a transcript and then gone. The filing layer was working perfectly and filing
    everything that existed; nothing existed. The operator: "every step of the work every results need to be saved".

    WHY THE ENGINE DOES THIS AND NOT THE MODEL. Asking the model to save its results is a request it can forget, and
    it did forget on every study we have measured. Persisting the output is a property of the step instead, so it
    holds whether the model cooperates, whether it is the lead or a member, and whether anyone remembered to ask.

    WRITTEN BEFORE THE REGISTRATION DIFF, so this file is discovered by the ordinary path and is filed, folder-placed,
    classified and announced by exactly the same code as a file the model wrote itself. No second mechanism, and
    therefore nothing that can disagree with the first one.

    A TABLE IS SAVED AS A TABLE. When the output's own shape is tabular it is written as `.csv`, which `artifacts.py`
    classifies previewable, so it renders inline in the conversation as a grid rather than as a wall of text. That is
    the same requirement from the other side: the reader sees the result, not a filename.

    Returns the path written, or None when there was nothing worth keeping.
    """
    t = _result_body(text)
    if not t.strip():
        return None
    # BOUNDED. A runaway loop can print megabytes and that is not a result, it is a log.
    if len(t) > 2 * 1024 * 1024:
        t = t[: 2 * 1024 * 1024]
    rows = _table_rows(t)
    # A TABLE IS A RESULT AT ANY SIZE, and the length threshold below must not be allowed to discard one.
    #
    # MEASURED: a clean six line comma separated table of five compounds and three descriptors is about 180 characters,
    # so a flat 200 character rule silently dropped a complete result set. Tabular shape is itself the evidence that
    # something was computed, which is a stronger signal than length, so it decides on its own.
    if rows is None:
        # PROSE MUST EARN IT: an import, a version string or a one line status has no result to lose, and a file for
        # every such step would bury the real ones. Same threshold `_looks_like_unsaved_results` uses.
        if len(t.strip()) < 200:
            return None
        # NO LINE COUNT RULE. A one line status is what this guards against and a status is SHORT, which the length
        # threshold above already rejects. A LONG single line is the opposite case: a fetched JSON payload arrives as
        # one line and is exactly the kind of result the operator asked to stop losing, so length decides alone.
    # THE STEP'S OWN TITLE NAMES THE FILE, so a reader scanning the file manager sees what each result is without
    # opening it. Non-word characters collapse to single underscores and the stem is bounded, matching how the source
    # scripts beside them are named.
    stem = re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", str(step_title or "").lower())).strip("_")[:48]
    stem = stem or "step_output"
    prefix = ("%03d_" % step_seq) if isinstance(step_seq, int) else ""
    results_dir = os.path.join(cwd, "results")
    try:
        os.makedirs(results_dir, exist_ok=True)
        if rows:
            path = os.path.join(results_dir, "%s%s.csv" % (prefix, stem))
            with open(path, "w", newline="", encoding="utf-8") as fh:
                csv.writer(fh).writerows(rows)
        else:
            # A STEP'S STDOUT IS A TRANSCRIPT, NOT A RESULT, AND IS NO LONGER FILED AS ONE.
            #
            # THE OPERATOR: "the files you generated and put into Report folder as .txt, they are useless to the user.
            # very fragmented and ugly, we do not want them." MEASURED on a live KRAS G12C session: 31 of the 50
            # artifacts a scientist could see were these numbered pairs, so the noise outnumbered the science.
            #
            # A TABLE IS STILL SAVED, above, because tabular output is data a person opens and reuses. Prose output now
            # reaches the reader through the per phase Markdown report, which has a methods section, a results section
            # and the same content in context rather than one file per step with no explanation.
            return None
        return path
    except Exception:  # noqa: BLE001
        # A step must not fail because its transcript could not be saved.
        return None


def report(verb: str, payload: Any, output: Any, seconds: float, ok: bool) -> None:
    """Tell the engine what this server just ran, and for whom.

    WHY AT THE SOURCE. A team member's tool calls were invisible to the engine: `SubagentStop` did not fire within four
    minutes on a working member and `getSubagentMessages` returned nothing usable, so `member.call` was zero on every
    team run. The consequence was precise and dangerous -- if a member computed a figure and the lead reported it,
    governance never saw the tool result, so provenance could not source it and a real number was indistinguishable
    from an invented one.

    THIS SERVER ALREADY KNOWS. Every platform verb, for the lead and for every member, passes through here. Recording
    it at the point of dispatch does not depend on the SDK exposing anything, and each member runs its own instance of
    this server labelled with the persona it serves, which is where `RAYCA_AGENT` comes from.

    NEVER RAISES, AND NEVER DELAYS THE SCIENCE. A reporting failure must not fail a tool call: the engine losing an
    event is a degraded record, while a raised exception here would be a lost dispatch.
    """
    if not CALLBACK or not RUN_ID:
        return
    try:
        body = json.dumps({
            "run_id": RUN_ID,
            "agent": AGENT,
            "verb": verb,
            "input": payload if isinstance(payload, (dict, list)) else str(payload)[:4000],
            "output": (output if isinstance(output, str) else json.dumps(output, default=str))[:40000],
            "seconds": round(float(seconds), 2),
            "ok": bool(ok),
        }, default=str).encode()
        req = urllib.request.Request(CALLBACK, data=body,
                                     headers=_headers(), method="POST")
        urllib.request.urlopen(req, timeout=5).read()
    except Exception:  # noqa: BLE001 - a lost event is not a lost dispatch
        pass


# --------------------------------------------------------------------------------------------------------------------
# Verb discovery
# --------------------------------------------------------------------------------------------------------------------

_NS_STATE: Dict[str, Any] = {}


def _run_code(*args: Any, **kwargs: Any) -> Any:
    """Execute Python the way the engine does, not a shortcut around it.

    ACCEPTS THE ARGUMENT UNDER WHATEVER NAME THE SCHEMA PUBLISHES IT. The first spike failed here: this took
    `source`, while `python_tool_spec`'s schema calls the field `code`, so a correct call from a correct client got
    `unexpected keyword argument 'code'`. The schema is the contract the caller can see, so the callable bends to it.

    AND IT GOES THROUGH `run_isolated`, WHICH THE SECOND SPIKE GOT WRONG. I looked for a module-level `run_python` in
    `dispatch` and there is none: the engine builds this per agent as a closure in `governance/serve.py:386` over
    `execisolate.run_isolated` and `workspace.workspace_for`. Reusing those two primitives means the crash boundary,
    the session workspace and the persistent namespace all behave here exactly as they do in a real run. Reaching for
    `exec` instead would have produced a working spike that proved nothing about the platform.
    """
    src = ""
    if args:
        src = str(args[0] or "")
    else:
        for key in ("code", "source", "python", "script"):
            if key in kwargs:
                src = str(kwargs[key] or "")
                break

    from modulon.engine.execisolate import run_isolated
    from modulon.engine.workspace import workspace_for

    session = os.environ.get("RAYCA_SESSION_ID", "modulon-max")
    cwd = workspace_for(session)
    # REGISTER FILES THE MOMENT THEY APPEAR, using the platform's own mechanism rather than a new one.
    #
    # THE GAP THIS CLOSES. `files/all` reads the platform's file REGISTRY, not the directory, so a file written straight
    # to disk is invisible to the file manager however correct its path is. MEASURED on the PROTAC run: it wrote
    # 3MXF.pdb, 5T35.pdb, JQ1_ideal.sdf and VH032_ideal.sdf, and the operator reported "no files are generating on the
    # file manager". The files were real and simply never announced.
    #
    # `filereg` is the wiring module built for exactly this, and `governance/artifacts.py` underneath it already
    # classifies a file by extension, decides honestly whether the browser can preview it, and keeps a per-session
    # index. Organisation is therefore the platform's existing answer rather than a scheme invented here.
    before = None
    try:
        from modulon.engine import filereg as _filereg
        before = _filereg.snapshot_before(session)
    except Exception:  # noqa: BLE001
        before = None

    # LIVE OUTPUT WHILE THE STEP RUNS, not only when it ends.
    #
    # `_run_cancellable` beats every fifteen seconds with the last 4000 characters of the child's stdout and nothing
    # was asking for it. On the operator's CPTAC run one step took 141 seconds and the console could show only six
    # heartbeats reading "still running", because elapsed time was all that reached it.
    #
    # NEVER DELAYS THE SCIENCE. The post has a short timeout and swallows everything: a lost beat is a degraded
    # record, while an exception here would be a lost step.
    def _beat(elapsed, tail):
        progress(name, float(elapsed or 0), str(tail or ""))

    # Recorded so stray recovery can tell a file this step wrote from one that was already on the host.
    _started_at = time.time()
    def _live(row: Any) -> None:
        """Forward a narration row the child spooled, while the step is still running.

        Only `dispatch_submitted` is forwarded. The other narration kinds already reach the console by their own routes,
        and echoing them here would double them.
        """
        try:
            if not isinstance(row, dict):
                return
            kind = row.get("kind")
            if kind == "dispatch_submitted":
                job_submitted(str(row.get("tool") or ""), bool(row.get("gpu")), str(row.get("image") or ""))
            elif kind == "dispatch_progress":
                # THE SAME ROW, UPDATED. `_watch_container` beats every 15 seconds with the container's log tail, the
                # elapsed time and a sample of the host's GPU, so the row the submission created stops being a
                # bare name and starts reporting.
                job_progress(row)
        except Exception:  # noqa: BLE001
            pass

    text, ns, meta = run_isolated(src, _NS_STATE, on_live=_live, cwd=cwd, on_progress=_beat)
    _NS_STATE.update(ns or {})

    # THIS STEP'S RESULTS BECOME A FILE, UNCONDITIONALLY.
    #
    # MEASURED, and this placement is the fix rather than a preference. The first version sat inside the
    # `if before is not None:` block that guards the registration diff. On a real run the snapshot was unavailable, so
    # a step that printed a clean four column table of four compounds wrote no result file at all, while the source
    # script beside it was still registered by the `PostToolUse` hook. Saving a result cannot depend on whether a
    # snapshot happened to be taken: those are two different jobs and only one of them loses data when it is skipped.
    #
    # Written before any registration path runs, so whichever one runs discovers it as an ordinary file and files,
    # classifies and announces it with no second mechanism.
    _persist_results(text, cwd, step_title_for_results(src), step_index_for_results(cwd))

    produced = []
    if before is not None:
        try:
            from modulon.engine import filereg as _filereg
            # FEED THE FILING LAYER, WHICH ALREADY DECIDES WHERE A FILE BELONGS.
            #
            # `governance/filing.py` decides the folder from step_seq, step_title, phase, phase_index and produces, and
            # `artifacts.py:410` records why it is a layer rather than a console convention, quoting the operator from an
            # earlier round: "we should have a governing layer on top of the engine which the engine should obey in how to
            # actually create folders ... so the engine doesn't behave randomly."
            #
            # We passed run_id ALONE, so every record arrived with an empty step_title and no declared role and filing had
            # almost nothing to work with. MEASURED: records came back with step_title="" while turn folders were already
            # correct, which is what pointed at this rather than at filing.
            #
            # THE ENGINE OBEYS FILING AND DOES NOT DECIDE. If a file lands somewhere unhelpful the fix belongs in filing.py,
            # where every reader sees the same answer, and never here.
            step_title = ""
            try:
                from modulon.engine.execisolate import _script_slug
                step_title = _script_slug(src).replace("_", " ")
            except Exception:  # noqa: BLE001
                step_title = ""
            step_seq = None
            try:
                _srcdir = os.path.join(cwd, "source")
                if os.path.isdir(_srcdir):
                    step_seq = len([f for f in os.listdir(_srcdir) if f[:3].isdigit()])
            except Exception:  # noqa: BLE001
                step_seq = None

            # Recovered BEFORE the diff runs, so a stray file is registered by the ordinary path rather than by a
            # second mechanism that could disagree with it.
            _strays = _recover_strays(src, cwd, _started_at)
            # THE STEP'S RESULTS BECOME A FILE, and this is deliberately the line before the diff so that file is
            # discovered, filed, folder-placed, classified and announced by the ordinary path with no second mechanism.
            # ASKED, NOT REGISTERED. WS-30 T5.
            #
            # This called `register_new`, which WRITES the artifact index, for an answer it needed: did
            # this step write anything, or did it print its results and lose them? The write came along
            # whether it was wanted or not, and `PostToolUse` in server.mjs already registers after EVERY
            # tool, the seam that also catches Bash and Write. So there were two registrars for one index
            # and which of them filed a given file was a race.
            #
            # MEASURED consequence, across 1332 records filed in three days: `step_title` reads
            # `os path join`, `open` and `time time` when this path won, because `_script_slug` takes a
            # slug off the code, and `run aidd tool` or `task create` when the seam won, because it uses
            # the verb. One field carrying two vocabularies, decided by whoever arrived first.
            #
            # The question is now answered without the side effect. Registration, filing, folder
            # placement, classification and announcement all happen once, in the seam. `step_seq` is
            # derived there from the workspace exactly as it was here.
            produced = _filereg.appeared_since(session, before) or []
            # PUSHED, NOT POLLED.
            #
            # The console asks GET /operational/artifacts every four seconds AND ONLY WHILE STREAMING, with one
            # settle fetch afterwards, so a file registered between polls was invisible until the reader did
            # something. The operator: "i feel the files are not appearing fast in the file manager ... it is like
            # some files are not getting saves there". This end already knows the instant a file appears, so it says
            # so rather than leaving the console to discover it.
            #
            # HONEST LIMIT: registration diffs the directory after the step returns, so this is prompt rather than
            # mid-step. A file written at second 2 of a 140 second step still waits for the step to end. Making that
            # live would mean watching the directory during execution, which is not what this changes.
            # NOT ANNOUNCED FROM HERE ANY MORE. `PostToolUse` in server.mjs registers and announces after EVERY tool,
            # which is the seam that also catches Bash and Write. Announcing here as well produced each file TWICE:
            # MEASURED ["aspirin_logp.csv", "001_aspirin_smiles.py", "aspirin_logp.csv", "001_aspirin_smiles.py"].
            # Registration still happens here, because the diff around this step is what gives a file its step title.
        except Exception:  # noqa: BLE001
            produced = []
    # `meta.ok` is True even on failing steps, so the caller is given the output and the metadata rather than a
    # verdict this layer is not entitled to reach.
    out = {"output": text, "meta": meta, "workspace": cwd}
    # A STEP THAT COMPUTED RESULTS AND SAVED NOTHING IS TOLD SO.
    #
    # MEASURED, and it cost a real study. Asked for ranked synthetic routes to imatinib, a run produced eleven scripts
    # named "retrosynthetic analysis identify key bond", "score three routes using step ideality feasibility" and
    # "risk assessment per step across routes gram scale". Every one of them printed. NOT ONE WROTE A FILE: 71 print
    # calls, zero writes, and a workspace containing only source. The science happened and evaporated into stdout, and
    # the reader was left with prose in a chat window and nothing to open, cite or check.
    #
    # THIS IS NOT THE SAME PROBLEM AS A MISPLACED FILE, and the stray recovery above cannot help: there was nothing on
    # disk to move. It is the absence of a write.
    #
    # STATED, NEVER ENFORCED. Plenty of steps legitimately write nothing -- checking a version, listing a directory,
    # reshaping a variable -- so a rule that demanded a file would be wrong more often than right. The condition is
    # deliberately narrow: substantial output, containing numbers, and no file registered. The model is told and decides,
    # which is the same posture as the harness telling it about files it named but never wrote.
    if not produced and _looks_like_unsaved_results(text):
        out["note"] = (
            "This step printed results and saved nothing, so they exist only in this transcript and will not appear in "
            "the file manager, the report, or anything the reader can open. Write the values you computed to a file in "
            "the working directory (a CSV for a table, a PNG for a figure) and they will be filed automatically."
        )
    # WHAT KIND OF SCIENCE THIS WAS, derived from what the step actually did.
    _cls = _operation_class(meta, produced)
    if _cls:
        out["operation_class"] = _cls
    if produced:
        # NAMES AND IDS ONLY. The full records reach the console through the file registry; repeating them in the tool
        # result would spend the model's context on data it cannot act on.
        #
        # PATHS, NOT RECORDS, AND THIS WAS A REAL BREAK. WS-30 T5 replaced `register_new` here with `appeared_since`,
        # to stop asking a question by way of a side effect. The two return different things: `register_new` gave
        # artifact RECORDS, `appeared_since` gives PATHS, and this line went on calling `r.get("name")` on each. Every
        # cell that wrote a file raised AttributeError AFTER doing its work, so the science ran and the result was
        # discarded. Measured on three runs today before it was caught.
        #
        # NO `id`, because nothing is registered here any more and there is none to give. The registry assigns ids at
        # the PostToolUse seam; inventing one to keep the old shape would be a fabrication the console would look up.
        out["files_written"] = [_written_row(r) for r in produced][:40]
    return out


class _LazyExecutor:
    """The engine's own executor, built on first use rather than on import.

    WHY THIS EXISTS AT ALL. `capability_tool_spec(executor)` builds `find_capability`, the verb that searches the whole
    registry -- the 800 container tools, the data and literature connectors, and installable packages. `_satisfy` could
    fill a `Callable` argument and nothing else, so this one factory was skipped and the verb reached no model. MEASURED:
    17 verbs published, `find_capability` absent, and every study fell back to hand written Python because from inside
    the loop the 800 tools did not exist. The verb's own description tells the model to call it "INSTEAD of assuming it
    does not exist", which it could not do.

    WHY THE REAL EXECUTOR AND NOT A STUB. `find_capability` does two things: it searches, and it BINDS the connector
    group of whatever matched so the tool is callable on the next step. Binding needs the object that owns the tool
    table -- `wire()`, `tools`, `tool_group()`, `active_tool_groups`, `scope_tools()`. A stub would make the search work
    and leave the binding silently inert, which is the worse failure: the model would be told a tool is now available
    and find it missing. `Executor()` takes all-default arguments, so the real one is available for the asking.

    WHY LAZY. Constructing it MEASURED 6.63 seconds, and this server is spawned per query, so paying that on every run
    to support a verb many runs never call is a cost with no return. The first attribute access builds it once.
    """

    def __init__(self) -> None:
        self._real = None

    def _load(self):
        if self._real is None:
            from modulon.engine.executor import Executor
            self._real = Executor()
        return self._real

    def __getattr__(self, name: str) -> Any:
        # `__getattr__` runs only for names not found normally, so `_real` and `_load` never reach here.
        return getattr(self._load(), name)


_EXECUTOR = _LazyExecutor()


def _satisfy(fn: Callable[..., Any]) -> Optional[Dict[str, Any]]:
    """Work out whether a spec builder can be called, and with what.

    Returns the kwargs to call it with, or None if it needs something we cannot supply. Builders in this codebase
    take either nothing or a callable that runs code, so anything else is left alone rather than guessed at.
    """
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return None
    kwargs: Dict[str, Any] = {}
    for name, p in sig.parameters.items():
        if p.default is not inspect.Parameter.empty:
            continue
        if p.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        ann = str(p.annotation)
        if "Callable" in ann or name in ("dispatch", "run_code", "run_python"):
            kwargs[name] = _run_code
        elif name == "executor":
            # THE ENGINE'S TOOL TABLE, which `find_capability` needs both to search and to bind what it finds.
            # Supplied lazily; see `_LazyExecutor` for why this is the real executor rather than a stub.
            kwargs[name] = _EXECUTOR
        else:
            return None  # a required argument we have no honest value for
    return kwargs


def discover_verbs() -> List[Any]:
    """Every ToolSpec the platform can build, found by walking the packages rather than by being told."""
    specs: List[Any] = []
    seen: set = set()
    import modulon  # noqa: F401

    # `modulon.tools` IS SCANNED TOO, being the package literally named for tools. It was omitted, so a verb defined
    # there was published nowhere: MEASURED 16 verbs discovered with write_report absent while its builder was correct.
    for pkg_name in ("modulon.engine", "modulon.governance", "modulon.tools"):
        try:
            pkg = __import__(pkg_name, fromlist=["*"])
        except Exception as ex:  # noqa: BLE001
            _log("skipped package %s: %s" % (pkg_name, ex))
            continue
        for mod_info in pkgutil.iter_modules(pkg.__path__):
            mod_full = "%s.%s" % (pkg_name, mod_info.name)
            try:
                mod = __import__(mod_full, fromlist=["*"])
            except Exception:
                continue  # a module that will not import cannot contribute verbs; not fatal
            for attr in dir(mod):
                if not (attr.endswith("_tool_spec") or attr.endswith("_tool_specs")):
                    continue
                fn = getattr(mod, attr, None)
                if not callable(fn):
                    continue
                kwargs = _satisfy(fn)
                if kwargs is None:
                    continue
                try:
                    got = fn(**kwargs)
                except Exception:
                    continue  # a builder that raises is reported by /healthz already; not this server's job
                for s in (got if isinstance(got, (list, tuple)) else [got]):
                    nm = getattr(s, "name", None)
                    if nm and nm not in seen:
                        seen.add(nm)
                        specs.append(s)
    return specs


def _schema_of(spec: Any) -> Dict[str, Any]:
    """The verb's argument schema, in MCP's shape.

    `ToolSpec.parameters` is already JSON Schema, so this is a pass-through with a floor. The floor matters: MCP
    clients reject a tool whose inputSchema is absent, and a verb with no arguments still needs an object schema.
    """
    params = getattr(spec, "parameters", None)
    if isinstance(params, dict) and params:
        out = dict(params)
        out.setdefault("type", "object")
        out.setdefault("properties", {})
        return out
    return {"type": "object", "properties": {}}


def to_mcp_tool(spec: Any) -> Dict[str, Any]:
    return {
        "name": str(getattr(spec, "name", "") or ""),
        "description": str(getattr(spec, "description", "") or "")[:4000],
        "inputSchema": _schema_of(spec),
    }


# --------------------------------------------------------------------------------------------------------------------
# Server
# --------------------------------------------------------------------------------------------------------------------

class Server:
    def __init__(self) -> None:
        self.specs: List[Any] = []
        self.by_name: Dict[str, Any] = {}
        self.ready = False

    def load(self) -> None:
        self.specs = discover_verbs()
        self.by_name = {getattr(s, "name"): s for s in self.specs if getattr(s, "name", None)}
        self.ready = True
        _log("published %d verbs: %s" % (len(self.specs), ", ".join(sorted(self.by_name)[:12])))

    def open_run_context(self) -> None:
        """Give the verbs a run to belong to.

        Without this, anything touching credentials, clusters or the ledger returns `no_user_context` -- which is not
        a failure of the verb but the absence of a session. The engine does the same thing per request.
        """
        try:
            from modulon.engine.dispatch import set_run_context

            uid = os.environ.get("RAYCA_USER_ID", "").strip()
            set_run_context(user_id=uid, compute=os.environ.get("RAYCA_COMPUTE", "") or "")
            _log("run context open for user %s" % (uid[:12] + "..." if uid else "<none>"))
        except Exception as ex:  # noqa: BLE001
            _log("could not open a run context: %s" % ex)

    # -- JSON-RPC ----------------------------------------------------------------------------------------------------

    def handle(self, req: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        method = req.get("method") or ""
        rid = req.get("id")
        if method == "initialize":
            return self._ok(rid, {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            })
        if method in ("notifications/initialized", "initialized"):
            return None  # a notification has no id and takes no reply
        if method == "tools/list":
            return self._ok(rid, {"tools": [to_mcp_tool(s) for s in self.specs]})
        if method == "tools/call":
            return self._call(rid, req.get("params") or {})
        if method == "ping":
            return self._ok(rid, {})
        return self._err(rid, -32601, "method not found: %s" % method)

    def _call(self, rid: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        name = str(params.get("name") or "")
        args = params.get("arguments") or {}
        spec = self.by_name.get(name)
        if spec is None:
            return self._ok(rid, {
                "content": [{"type": "text", "text": json.dumps({
                    "error": "no_such_verb", "name": name,
                    "detail": "This platform publishes %d verbs. Call tools/list to see them, or use "
                              "find_capability to search the 2,318 registry records behind them."
                              % len(self.specs),
                })}],
                "isError": True,
            })
        fn = getattr(spec, "dispatch", None)
        if not callable(fn):
            return self._ok(rid, {"content": [{"type": "text", "text": json.dumps(
                {"error": "verb_not_dispatchable", "name": name})}], "isError": True})
        started = time.time()
        try:
            # REPORTED WHILE IT RUNS, not only when it returns. See `_LiveDispatchSpool`: this process had no
            # spool path set, so a dispatch's own submission was never written anywhere and the panel could not
            # learn a container existed until the call came back. The verb stays synchronous; only the
            # reporting changes.
            with _LiveDispatchSpool():
                out = fn(**args) if isinstance(args, dict) else fn(args)
            out = _durable_job_fallback(name, args, out)
            # STILL CALLED, and now it is the row that CLOSES the job rather than the only row there is. It
            # carries rc and the final duration, which no beat can know.
            _announce_container_job(out)
            # THE VERB'S OWN DESCRIPTION IS THE SCIENTIFIC EXPLANATION, attached where the spec is in hand.
            #
            # AUTHORED, NOT INFERRED. Every card today says what was invoked and whether it returned, never what the
            # operation IS. The operator asked for "scientific explainnigns and titles for operation cards", and the
            # honest source is the prose the platform already wrote for this verb and publishes over MCP as its tool
            # description. Nothing is generated: a verb with no description gets no explanation, and a card with only
            # a title is honest where a guessed sentence would not be.
            #
            # NOT the AIDD registry, which was the obvious guess and is wrong: list_aidd_tools() indexes external
            # tool packages (a3-net-master, ablang, abdev) and contains no entry for run_python or any platform verb.
            # MEASURED: five verbs looked up, zero hits.
            out = _with_explanation(out, spec)
            # FILES FROM ANY VERB, not only from run_python.
            #
            # MEASURED: a run called write_report, the document was written and registered correctly, and it never
            # appeared on the stream, because only the code runner announced what it produced. A verb that reports
            # files it registered has them announced the same way, so the reader sees a report arrive rather than
            # discovering it on a later poll.
            if isinstance(out, dict):
                _reg = out.get("registered") or []
                # ANNOUNCED BY `PostToolUse` ALONE. Pushing here too gave report.md twice on a real run. One seam.
                
                # THE CLASS FOR EVERY VERB, not only for the code runner.
                #
                # MEASURED on a team run: 58 events, 13 paired steps, 7 files, and `operation_class` EMPTY on all of
                # them. The specialists' work arrives through `run_as_member`, which is an ordinary verb, and only
                # `run_python` was deriving a class. So every card on a team run lost its scientific identity while
                # every solo card had one.
                if _reg and not out.get("operation_class"):
                    _cls = _operation_class(out.get("meta"), _reg)
                    if _cls:
                        out["operation_class"] = _cls
            report(name, args, out, time.time() - started, True)
        except TypeError as ex:
            # A WRONG ARGUMENT SHAPE IS REPORTED, NOT RAISED. This is the failure class that cost a real study
            # 507 events: a verb accepted a malformed field, returned success and generated nothing. Saying exactly
            # what was wrong lets the caller fix it in one step instead of guessing at thresholds.
            report(name, args, {"error": "bad_arguments", "detail": str(ex)}, time.time() - started, False)
            return self._ok(rid, {"content": [{"type": "text", "text": json.dumps({
                "error": "bad_arguments", "verb": name, "detail": str(ex),
                "expected": _schema_of(spec),
            })}], "isError": True})
        except Exception as ex:  # noqa: BLE001
            report(name, args, {"error": type(ex).__name__, "detail": str(ex)[:400]}, time.time() - started, False)
            return self._ok(rid, {"content": [{"type": "text", "text": json.dumps({
                "error": type(ex).__name__, "verb": name, "detail": str(ex)[:1200],
            })}], "isError": True})
        return self._ok(rid, {"content": [{"type": "text", "text": _render(out)}]})

    @staticmethod
    def _ok(rid: Any, result: Dict[str, Any]) -> Dict[str, Any]:
        return {"jsonrpc": "2.0", "id": rid, "result": result}

    @staticmethod
    def _err(rid: Any, code: int, msg: str) -> Dict[str, Any]:
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": msg}}


def _render(out: Any) -> str:
    if isinstance(out, str):
        return out
    try:
        return json.dumps(out, default=str)[:200000]
    except Exception:  # noqa: BLE001
        return str(out)[:200000]


def main() -> int:
    srv = Server()
    try:
        srv.load()
        srv.open_run_context()
    except Exception:
        _log("failed to load the platform:\n%s" % traceback.format_exc())
        return 1

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue
        try:
            resp = srv.handle(req)
        except Exception:  # noqa: BLE001
            resp = srv._err(req.get("id"), -32603, "internal error: %s" % traceback.format_exc(limit=2))
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
