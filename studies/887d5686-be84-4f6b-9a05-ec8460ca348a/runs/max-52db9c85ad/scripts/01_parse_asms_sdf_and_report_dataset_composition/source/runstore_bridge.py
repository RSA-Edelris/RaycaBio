#!/usr/bin/env python3
"""Register modulon-max runs in the platform run store and interpret their workflows.

WHY THIS EXISTS. The platform's file manager iterates runstore.store().sessions(), and that store has no
modulon-max runs -- so files/all, artifacts, provenance and lineage all return empty even though the files
are correctly written and registered. MEASURED on a real PROTAC team run: 3MXF.pdb, 5T35.pdb, JQ1_ideal.sdf
and VH032_ideal.sdf were all present in the workspace and the file manager stayed empty.

The fix: register each run in the SAME sqlite database the platform already reads. A run that exists in
modulon-max's own store.mjs but not in runstore.py is invisible to every file, artifact and lineage endpoint.

SPEAKS JSON LINES ON STDIN AND STDOUT, the same pattern as governance_bridge.py. One process, kept alive,
because starting an interpreter per call would add a second to each run start.

ALSO HOUSES THE SCIENTIFIC WORKFLOW INTERPRETER, because it needs the same Python environment and the same
long-lived model access. wfinterp.interpret requires an llm object, and the Auditor class here provides one
through the same proxy the governance bridge uses.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import traceback
from typing import Any, Dict, List, Optional, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from env_select import resolve_src  # noqa: E402  the one place environment is decided
sys.path.insert(0, resolve_src())


def log(msg: str) -> None:
    sys.stderr.write("[runstore] %s\n" % msg)
    sys.stderr.flush()


class _RunObj:
    """A duck-typed run object for runstore.upsert_run, which reads attributes."""

    def __init__(self, **kw: Any) -> None:
        for k, v in kw.items():
            setattr(self, k, v)


def _register_run(p: Dict[str, Any]) -> Dict[str, Any]:
    """Register or update a modulon-max run in the platform run store."""
    from modulon.governance import runstore

    store = runstore.store()
    if not store.ok:
        return {"ok": False, "error": "runstore not available"}

    run_id = str(p.get("run_id") or "")
    session_key = str(p.get("session_key") or "")
    if not run_id:
        return {"ok": False, "error": "no run_id"}

    run = _RunObj(
        run_id=run_id,
        session_key=session_key,
        task=str(p.get("task") or ""),
        mode=str(p.get("mode") or "max"),
        state=str(p.get("state") or "running"),
        error=str(p.get("error") or "") or None,
        created_at=float(p.get("created_at") or time.time()),
        started_at=float(p.get("started_at") or time.time()),
        ended_at=float(p.get("ended_at") or 0) or None,
        user_id=str(p.get("user_id") or ""),
        org_id=str(p.get("org_id") or ""),
    )
    store.upsert_run(run)
    return {"ok": True, "run_id": run_id, "session_key": session_key}


def _update_run(p: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing run's state in the platform run store."""
    from modulon.governance import runstore

    store = runstore.store()
    if not store.ok:
        return {"ok": False, "error": "runstore not available"}

    run_id = str(p.get("run_id") or "")
    if not run_id:
        return {"ok": False, "error": "no run_id"}

    # Read existing, update fields that changed
    existing = store.get_run(run_id)
    if not existing:
        # Not yet registered; treat as a full register
        return _register_run(p)

    run = _RunObj(
        run_id=run_id,
        session_key=existing.get("session_key") or str(p.get("session_key") or ""),
        task=existing.get("task") or str(p.get("task") or ""),
        mode=existing.get("mode") or "max",
        state=str(p.get("state") or existing.get("state") or "running"),
        error=str(p.get("error") or "") or existing.get("error") or None,
        created_at=existing.get("created_at") or time.time(),
        started_at=existing.get("started_at") or time.time(),
        ended_at=float(p.get("ended_at") or 0) or existing.get("ended_at") or None,
        user_id=str(p.get("user_id") or existing.get("user_id") or ""),
        org_id=str(p.get("org_id") or existing.get("org_id") or ""),
    )
    store.upsert_run(run)
    return {"ok": True, "run_id": run_id, "state": run.state}


# ---------------------------------------------------------------------------
# Scientific workflow interpretation
# ---------------------------------------------------------------------------

class _Auditor:
    """LLM proxy for wfinterp, same shape as governance_bridge.Auditor.

    wfinterp.interpret requires an object with .invoke(str) -> reply text. This uses the same LiteLLM
    proxy the rest of the platform uses, and the same cheap model the governance judge uses.
    """

    def __init__(self) -> None:
        self.base = os.environ.get("RAYCA_LLM_BASE_URL", "http://127.0.0.1:4000").rstrip("/")
        self.key = os.environ.get("RAYCA_LLM_API_KEY", "") or os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = os.environ.get("RAYCA_INTERP_MODEL", "claude-haiku-4-5")

    def invoke(self, prompt: str) -> str:
        """Never raises. A failed interpretation is reported honestly, not as a crash."""
        import urllib.request

        body = json.dumps({
            "model": self.model,
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
        }).encode()
        req = urllib.request.Request(
            self.base + "/v1/messages",
            data=body,
            headers={
                "content-type": "application/json",
                "anthropic-version": "2023-06-01",
                "authorization": "Bearer " + self.key,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                out = json.loads(r.read().decode())
            blocks = out.get("content") or []
            return "".join(b.get("text", "") for b in blocks if isinstance(b, dict))
        except Exception as ex:  # noqa: BLE001
            log("interpreter llm unavailable: %s" % str(ex)[:200])
            return ""


def _translate_events_for_distil(console_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert modulon-max console wire events into the shape wfdistil.distil() expects.

    wfdistil reads:
      - type="execute" events with body=code, meta.call_id for pairing, meta.tool for the tool name
      - type="observe" events with body=output, meta.call_id for pairing, status=ok|error

    modulon-max's toConsoleEvent produces:
      - type="tool_call" with body={tool, input}, meta={tool, input, origin}
      - type="observe" with body=output_text, meta={tool, elapsed_s, ...}

    The pairing must be reconstructed: tool_call and observe arrive in sequence (call then result),
    so we assign synthetic call_ids by matching each observe to its preceding tool_call.
    """
    translated: List[Dict[str, Any]] = []
    pending_call_id = 0
    last_tool_call_id: Optional[str] = None

    for ev in console_events:
        etype = str(ev.get("type") or "")

        if etype == "tool_call":
            pending_call_id += 1
            cid = "mc-%d" % pending_call_id
            last_tool_call_id = cid

            # Extract code from the input. run_python carries code in input.code; other tools
            # carry their input as a dict that we serialize as the "code" for distil to read.
            body_raw = ev.get("body")
            meta_raw = ev.get("meta") if isinstance(ev.get("meta"), dict) else {}
            tool = str(meta_raw.get("tool") or "")
            inp = meta_raw.get("input") or (body_raw if isinstance(body_raw, dict) else {})
            if isinstance(inp, dict):
                code = str(inp.get("code") or inp.get("script") or inp.get("source") or "")
                if not code:
                    # For non-code tools, serialize the input as a pseudo-code comment so distil
                    # can still read what the tool was asked to do.
                    code = "# %s\n%s" % (tool, json.dumps(inp, default=str)[:4000])
            else:
                code = str(inp)[:4000]

            translated.append({
                "v": ev.get("v"),
                "seq": ev.get("seq"),
                "ts": ev.get("ts"),
                "run_id": ev.get("run_id"),
                "type": "execute",
                "node": ev.get("node", "execute"),
                "title": ev.get("title", "Execute python"),
                "body": code,
                "status": "started",
                "meta": {"tool": tool, "call_id": cid},
            })

        elif etype == "observe":
            cid = last_tool_call_id or ("mc-%d" % pending_call_id)
            last_tool_call_id = None  # consumed

            meta_raw = ev.get("meta") if isinstance(ev.get("meta"), dict) else {}
            translated.append({
                "v": ev.get("v"),
                "seq": ev.get("seq"),
                "ts": ev.get("ts"),
                "run_id": ev.get("run_id"),
                "type": "observe",
                "node": ev.get("node", "execute"),
                "title": ev.get("title", "Observation"),
                "body": ev.get("body", ""),
                "status": ev.get("status", "ok"),
                "meta": {
                    "call_id": cid,
                    "tool": str(meta_raw.get("tool") or ""),
                    "ok": meta_raw.get("failed_inside") is not True and ev.get("status") != "error",
                    "elapsed_s": meta_raw.get("elapsed_s"),
                },
            })

        else:
            # Pass through other event types unchanged (status, plan, message, etc.)
            # wfdistil ignores them but they provide context for distil_run.
            translated.append(ev)

    return translated


def _lineage_event(req):
    """One OpenLineage run event for a run of this engine.

    WHY THIS IS HERE AND WHY IT IS SMALL. `rayca_lineage` is 2,843 lines across eleven modules -- an OpenLineage
    emitter, LangFuse and MLflow bridges, idempotent Marquez sync, and an identity module that mints ONE value and
    re-encodes it so a run has the same identity in every system. `governance/lineage.py` already exposes it, already
    redacts caller-supplied facets, and already promises never to raise. So the only thing missing was a caller.

    MEASURED: `identity_for('max-x')` returns available=True with an ol_run_id, so runs of this engine were always
    eligible; nothing emitted for them. WS-3 T-3.10 asks for a run visible in lineage end to end, and the reason it
    stayed open is that the emitter had no caller on this side.

    NEVER FATAL. Lineage that can break a run is worse than no lineage, which is the module's own stated rule.
    """
    try:
        from modulon.governance import lineage as _lin
        res = _lin.emit_run_event(
            str(req.get("run_id") or ""),
            str(req.get("event_type") or "START"),
            job_name=str(req.get("job_name") or ""),
            facets=req.get("facets") or {},
        )
        return {"ok": True, **(res if isinstance(res, dict) else {})}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "emitted": False, "reason": f"{type(exc).__name__}: {exc}"}


def _interpret_workflow(p: Dict[str, Any]) -> Dict[str, Any]:
    """Run the scientific workflow interpretation on modulon-max console events.

    Returns the interpreted workflow document or a structural fallback indicator.
    The caller (consoleapi.mjs) decides whether to use this or fall back to workflowFrom.
    """
    from modulon.engine import wfdistil as _distil
    from modulon.engine import wfinterp as _interp

    events_raw = p.get("events") or []
    task = str(p.get("task") or "")[:2000]
    run_id = str(p.get("run_id") or "")

    if not events_raw:
        return {"ok": False, "interpreted": False, "note": "no events"}

    # Translate from console wire shape to wfdistil's expected shape
    events = _translate_events_for_distil(events_raw)

    candidates = _distil.mark(_distil.distil(events))
    if not candidates:
        return {"ok": True, "interpreted": False, "note": "no executable steps found in this run"}

    evidence = _distil.distil_run(events)

    # The LLM is required for interpretation. Without it, we report honestly.
    llm = _Auditor()
    # Test the auditor is reachable before committing to interpretation
    if not llm.key:
        return {
            "ok": True,
            "interpreted": False,
            "note": "no LLM credentials available for scientific interpretation",
            "candidates": len(candidates),
        }

    res = _interp.interpret(candidates, llm=llm, task=task, evidence=evidence)
    doc = res.as_dict()
    doc["runId"] = run_id
    high = max((c.index for c in candidates), default=0)
    doc["stepsRead"] = high
    doc["rebuilt"] = True

    # Persist if interpreted, so subsequent reads do not need the model again
    if res.interpreted:
        try:
            from modulon.engine.wfstore import WorkflowStore
            WorkflowStore().put(run_id, doc, session_key=str(p.get("session_key") or ""), step_high=high)
        except Exception as ex:  # noqa: BLE001
            log("workflow store write failed: %s" % str(ex)[:160])

    return {"ok": True, **doc}


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def _workspace(p: Dict[str, Any]) -> Dict[str, Any]:
    """Where a session's files live, resolved by the platform rather than guessed.

    The path carries a hash, so it cannot be composed from the session id on the Node side. It is asked for here for
    ONE reason: to become the working directory of the agent session, so a tool that writes a relative path writes into
    the study.
    """
    from modulon.engine.workspace import workspace_for

    session = str(p.get("session") or "")
    if not session:
        return {"ok": False, "error": "no_session"}
    try:
        return {"ok": True, "path": workspace_for(session)}
    except Exception as ex:  # noqa: BLE001
        return {"ok": False, "error": type(ex).__name__, "detail": str(ex)[:200]}


def _dashboard_brief(p: Dict[str, Any]) -> Dict[str, Any]:
    """The full dashboard standard for one session, with that session's real artifact inventory.

    THE POINT OF THIS OP. The operator: "it is hard for the user to set the bars high everytime, i can do it but not all
    people are able to do it with prompting, so i need a systematic way of doing it". The standard lives in code, so
    every user gets the version that was researched rather than the one they managed to describe.
    """
    from modulon.engine import dashboard as _dash
    from modulon.governance import artifacts as _art

    session = str(p.get("session") or "")
    if not session:
        return {"ok": False, "error": "no_session"}
    try:
        index = _art._read_index(session) or []
    except Exception as exc:  # noqa: BLE001
        log("dashboard_brief: no artifact index for %s: %s" % (session[:8], exc))
        index = []
    # THE PREVIOUS DASHBOARD IS TAKEN OUT OF THE WAY, AS A MECHANISM RATHER THAN AN INSTRUCTION.
    #
    # MEASURED: asked to regenerate, the model found the existing file, answered "Platform already processed it.
    # Dashboard is ready", and finished in three turns having built nothing. Telling it not to do that is a rule it can
    # reason around. Removing the file is not.
    #
    # SAFE TO REMOVE because the previous dashboard was filed as an artifact when it was finished, so it stays
    # downloadable from the console. Only the working copy goes.
    import glob

    from modulon.engine.workspace import workspace_for as _wsf

    workspace = _wsf(session, create=False)
    cleared = []
    if workspace:
        stale = glob.glob(os.path.join(workspace, "*_dashboard.html"))
        stale += glob.glob(os.path.join(workspace, _dash.SCRATCH_NAME))
        stale += glob.glob(os.path.join(workspace, _dash.PART_GLOB))
        for path in stale:
            try:
                os.remove(path)
                cleared.append(os.path.basename(path))
            except OSError as exc:
                log("dashboard_brief: could not clear %s: %s" % (path, exc))
        if cleared:
            log("dashboard_brief cleared previous output: %s" % ", ".join(cleared))

    text = _dash.brief(session_id=session, title=str(p.get("title") or ""), artifacts=index)
    return {"ok": True, "brief": text, "artifacts": len(index), "assets": _dash.available(),
            "cleared": cleared}



_NODE_CANDIDATES = ("/usr/local/bin/node", "/usr/bin/node", "node")


def _check_js(body: str) -> Optional[Dict[str, Any]]:
    """Parse JavaScript with the real engine. None means it parses.

    A regex cannot do this job: my first attempt tracked quotes by hand, mistook a regex literal containing a quote for a
    string, and turned one failing block into three. So the parser decides, and every repair below is verified by it.
    """
    import subprocess
    import tempfile

    fd, path = tempfile.mkstemp(suffix=".js")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(body)
        for exe in _NODE_CANDIDATES:
            try:
                r = subprocess.run([exe, "--check", path], capture_output=True, text=True, timeout=60)
            except (OSError, subprocess.SubprocessError):
                continue
            if r.returncode == 0:
                return None
            import re as _re
            m = _re.search(_re.escape(path) + r":(\d+)", r.stderr or "")
            msg = [ln.strip() for ln in (r.stderr or "").splitlines() if "Error" in ln]
            return {"line": int(m.group(1)) if m else 0, "message": (msg[0] if msg else "parse failed")}
        log("_check_js: no usable node binary, skipping validation")
        return None
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def _repair_and_validate_js(html: str) -> Dict[str, Any]:
    """Fix string literals broken across lines, then report whatever still cannot parse.

    MEASURED, and it cost the operator half an hour: a run wrote .join with an escaped newline from Python, Python
    consumed the escape, and a real newline landed inside the JavaScript string. One character, a SyntaxError, and the
    entire page rendered blank with no explanation. Rendered proof of the repair: 46 visible elements and 2 page errors
    before, 931 elements and 0 errors after.
    """
    from modulon.engine import dashboard as _dash

    fixed = 0
    failures: List[str] = []
    for block in _dash.iter_inline_scripts(html):
        err = _check_js(block["body"])
        if not err:
            continue
        candidate = _dash.escape_line_break(block["body"], err["line"])
        if candidate is not None and _check_js(candidate) is None:
            html = _dash.replace_block_body(html, block, candidate)
            fixed += 1
        else:
            failures.append("script at byte %d, line %d: %s" % (block["start"], err["line"], err["message"]))
    return {"html": html, "fixed": fixed, "failures": failures}


def _dashboard_finalise(p: Dict[str, Any]) -> Dict[str, Any]:
    """Substitute the vendored libraries, publish the finished file under its real name, and file it once.

    THREE MEASURED DEFECTS THIS CLOSES.

    1. A model cannot type 1.3 MB of Plotly, and left to itself it writes `https://cdn.plot.ly`, which is what every
       dashboard this platform had produced did. Such a file shows nothing when opened from disk and makes a reader's
       browser call a third party while displaying proprietary results.
    2. Building straight into the final name filed TEN versions of one dashboard as it grew, at 9837 through 92308
       bytes, so the file panel showed ten copies and nine were half written.
    3. The copy the console served was registered mid write, BEFORE substitution, so downloading it gave 92308 bytes
       with three unsubstituted placeholders and no working charts while the file on disk was 1957758 bytes and fine.

    So the model builds into a dotted scratch name the scanner ignores, and this publishes and files the finished bytes
    exactly once.
    """
    import glob

    from modulon.engine import dashboard as _dash
    from modulon.engine import filereg as _filereg
    from modulon.engine.workspace import workspace_for as _wsf
    from modulon.governance import artifacts as _art

    session = str(p.get("session") or "")
    if not session:
        return {"ok": False, "error": "no_session"}
    workspace = _wsf(session, create=False)
    if not workspace:
        return {"ok": False, "error": "no_workspace"}

    scratch = os.path.join(workspace, _dash.SCRATCH_NAME)

    # NUMBERED PARTS ARE ASSEMBLED HERE, so no single model reply ever has to carry the document.
    #
    # MEASURED: a run computed its data over nine turns and then died with "API Error: The response stalled before a
    # response was produced" while writing the whole page in one go. Assembling on this side makes the small step the
    # natural one and keeps partial work: a stall at part six still leaves parts one to five on disk.
    parts = sorted(
        (q for q in glob.glob(os.path.join(workspace, _dash.PART_GLOB)) if _dash.part_index(q) >= 0),
        key=_dash.part_index,
    )
    if parts and not os.path.isfile(scratch):
        joined = _dash.assemble_parts(parts)
        with open(scratch, "w", encoding="utf-8") as fh:
            fh.write(joined)
        log("dashboard_finalise assembled %d parts into %s (%d bytes)"
            % (len(parts), _dash.SCRATCH_NAME, len(joined)))

    sources = [scratch] if os.path.isfile(scratch) else []
    # A dashboard written before this change, or by a run that ignored the scratch rule, is still worth completing.
    for other in sorted(glob.glob(os.path.join(workspace, "*.html"))):
        try:
            with open(other, "r", encoding="utf-8", errors="replace") as fh:
                head = fh.read(200000)
            if "rayca-asset:" in head:
                sources.append(other)
        except OSError:
            continue

    done = []
    for source in sources:
        try:
            with open(source, "r", encoding="utf-8", errors="replace") as fh:
                html = fh.read()
            # PUNCTUATION IS NORMALISED BEFORE THE LIBRARIES GO IN, so the substitution only ever touches the model's own
            # text. MEASURED: a run that was told "No em dashes" emitted four and reported zero.
            cleaned = _dash.normalise_text(html)
            if cleaned["total"]:
                log("dashboard_finalise normalised %d forbidden characters: %s"
                    % (cleaned["total"], cleaned["replaced"]))
            # THE JAVASCRIPT IS PARSED BEFORE PUBLISHING. A page whose script cannot run is blank, and a blank page
            # with no message is the worst outcome this feature can produce.
            checked = _repair_and_validate_js(cleaned["html"])
            if checked["fixed"]:
                log("dashboard_finalise repaired %d broken string literal(s)" % checked["fixed"])
            body_html = checked["html"]
            if checked["failures"]:
                log("dashboard_finalise UNPARSEABLE JAVASCRIPT: %s" % "; ".join(checked["failures"][:3]))
                banner = _dash.error_banner(checked["failures"])
                m = re.search(r"<body[^>]*>", body_html, re.I)
                if m:
                    body_html = body_html[:m.end()] + banner + body_html[m.end():]
            result = _dash.inline_assets(body_html)
            target = os.path.join(workspace, _dash.final_name(session))

            # THE FLOOR IS TAKEN BEFORE THE FILE EXISTS, so the diff below registers this dashboard and nothing else.
            before = _art.snapshot(_filereg._session_roots(session))
            with open(target, "w", encoding="utf-8") as fh:
                fh.write(result["html"])
            if os.path.abspath(source) != os.path.abspath(target):
                try:
                    os.remove(source)
                except OSError as exc:
                    log("dashboard_finalise: could not remove scratch %s: %s" % (source, exc))
            # The parts have been published, so they go. Leaving them would let a later finalise assemble stale sections.
            for q in parts:
                try:
                    os.remove(q)
                except OSError as exc:
                    log("dashboard_finalise: could not remove part %s: %s" % (q, exc))

            filed = 0
            try:
                produced = _art.collect(session, before, run_id=str(p.get("run_id") or ""),
                                        step_title="dashboard",
                                        roots=_filereg._session_roots(session)) or []
                filed = len(produced)
            except Exception as exc:  # noqa: BLE001 - an unfiled dashboard still exists on disk
                log("dashboard_finalise: could not file %s: %s" % (target, exc))

            left = _dash.remaining_network_refs(result["html"])
            done.append({"file": os.path.basename(target), "inlined": result["inlined"],
                         "missing": result["missing"], "network_refs": left,
                         "bytes": len(result["html"]), "filed": filed})
            log("dashboard_finalise %s bytes=%d inlined=%s missing=%s network=%d filed=%d"
                % (os.path.basename(target), len(result["html"]), result["inlined"],
                   result["missing"], len(left), filed))
        except Exception as exc:  # noqa: BLE001
            log("dashboard_finalise FAILED on %s: %s" % (source, exc))
    return {"ok": True, "files": done}


def _phase_report(p: Dict[str, Any]) -> Dict[str, Any]:
    """Render and file one phase's Markdown report.

    HERE RATHER THAN IN THE EXECUTOR. The report generator is Python and modulon-max is Node, and max REPLACES the
    Python executor for every study it runs, so a hook added there fired for nothing. Measured: two real runs produced
    no report and no log line. This is the seam that already carries the run store across the boundary.

    The renderer is pure and separately tested. This function only gathers what it needs from the records that exist.
    """
    import platform as _platform
    import sys as _sys

    from modulon.engine import phasereport as _pr
    from modulon.engine.workspace import workspace_for as _wsf
    from modulon.governance import artifacts as _art

    session = str(p.get("session") or "")
    phase = p.get("phase") or {}
    run_id = str(p.get("run_id") or "")
    if not session or not isinstance(phase, dict):
        return {"ok": False, "error": "no_session_or_phase"}
    workspace = _wsf(session, create=False)
    if not workspace:
        return {"ok": False, "error": "no_workspace"}

    try:
        from modulon.engine.wfstore import WorkflowStore as _WFS

        doc = (_WFS().get(run_id) if run_id else None) or _WFS().latest_for_session(session)
    except Exception as exc:  # noqa: BLE001
        log("phase_report: no workflow for %s: %s" % (run_id[:14], exc))
        doc = None
    all_methods = list((doc or {}).get("methods") or [])

    # ATTRIBUTED BY THE PHASE THE RECORD CARRIES, and the whole set when it carries none.
    #
    # MEASURED on a real retrosynthesis run: every method entry had `phase` set to the empty string, so filtering
    # strictly would have produced an empty methods section for a phase that plainly did work.
    pid = str(phase.get("id") or "")
    tagged = [m for m in all_methods if str(m.get("phase") or "") == pid] if pid else []
    methods = tagged or all_methods

    try:
        index = _art._read_index(session) or []
        artifacts = [r for r in index if str(r.get("run_id") or "") == run_id] or index
    except Exception as exc:  # noqa: BLE001
        log("phase_report: no artifact index for %s: %s" % (session[:8], exc))
        artifacts = []

    versions = {}
    for _name in ("rdkit", "pandas", "scikit-learn", "openmm", "numpy"):
        try:
            import importlib.metadata as _md

            versions[_name] = _md.version(_name)
        except Exception:  # noqa: BLE001 - a package that is not installed has no version to report
            pass

    try:
        markdown = _pr.render(
            phase=phase,
            methods=methods,
            # THE IMAGES THAT RAN, from the tape by way of the caller. The workflow method records this
            # report is built from carry no image field, so without this the report cannot name one and
            # the `container_doc` obligation would be settled by nothing.
            images=[str(x) for x in (p.get("images") or []) if str(x or "").strip()],
            artifacts=artifacts,
            environment={"host": _platform.node(), "platform": _platform.platform(),
                         "python": _sys.version.split()[0]},
            versions=versions,
            meta={"run_id": run_id, "study_id": session,
                  "status": "complete" if phase.get("final") else "phase complete",
                  "model": str(p.get("model") or "")},
        )
        path = _pr.write(workspace, phase, markdown)
    except Exception as exc:  # noqa: BLE001
        log("phase_report FAILED for %s phase %s: %s" % (session[:8], pid or "?", exc))
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)[:200]}
    if not path:
        return {"ok": False, "error": "not_written"}
    log("phase_report wrote %s" % path)
    return {"ok": True, "path": path, "bytes": len(markdown)}


def _files_for_run(p: Dict[str, Any]) -> Dict[str, Any]:
    """Every artifact the index already holds for one run.

    WHY THE DIFF IS NOT ENOUGH, MEASURED. Two registrars share one index: the code runner files what a script wrote, and the
    universal post-tool seam files anything else. Whichever gets there first wins, and the loser diffs against a workspace that
    already contains the file and correctly reports nothing new. On the CRBN run `max-ff20d03e11` all eleven outputs, including
    6H0F.pdb and gnina_docked.sdf.gz, were filed under the right run id and NOT ONE was announced, because the announcing side
    only ever learned about files from its own diff. The operator saw an empty conversation four times over.

    Reading the index instead makes announcement independent of who filed the file. The caller still decides what is new to a
    READER, which it already tracks per run.
    """
    from modulon.governance import artifacts

    session = str(p.get("session") or "")
    run_id = str(p.get("run_id") or "")
    if not session or not run_id:
        return {"ok": False, "error": "no_session_or_run"}
    try:
        records = [r for r in artifacts._read_index(session) if str(r.get("run_id") or "") == run_id]
        return {"ok": True, "files": records}
    except Exception as ex:  # noqa: BLE001
        return {"ok": False, "error": type(ex).__name__, "detail": str(ex)[:200]}


def _step_seq_for(session: str) -> Optional[int]:
    """How many numbered scripts this session has written, which is the step this file belongs to.

    WS-30 T5. Derived from the workspace because that is where the evidence is. The code runner computed
    the same number from the same directory and registered with it, and that second registration is what
    made attribution a race: 1332 records filed in three days carried `step_title` in two different
    vocabularies depending on which registrar arrived first.

    Returns None rather than 0 when there is no `source/` directory yet. A zero would claim this is the
    first step, and "not known" is a different statement from "step zero".
    """
    try:
        from modulon.engine.workspace import workspace_for

        ws = workspace_for(session, create=False) or ""
        src = os.path.join(ws, "source")
        if not ws or not os.path.isdir(src):
            return None
        return len([f for f in os.listdir(src) if f[:3].isdigit()])
    except Exception:  # noqa: BLE001 - an unknown step number must not stop a file being filed
        return None


def _register_files(p: Dict[str, Any]) -> Dict[str, Any]:
    """Register whatever has appeared in a session's workspace since a snapshot.

    THE UNIVERSAL SEAM. Registration used to live inside the code-runner verb alone, so anything written by the SDK's own
    tools was invisible: MEASURED on a real study, `Bash` downloaded 754 MB of retrosynthesis models into /tmp and the
    session's workspace held nothing but source files. This is callable after ANY tool, from the one hook that sees them
    all.
    """
    from modulon.engine import filereg

    session = str(p.get("session") or "")
    if not session:
        return {"ok": False, "error": "no_session"}
    before = p.get("before") or {}
    try:
        produced = filereg.register_new(
                session, before,
                run_id=str(p.get("run_id") or ""),
                step_title=str(p.get("step_title") or ""),
                # THE PHASE THIS FILE BELONGS TO. `register_new` and `filing.folder_for` have accepted
                # these since they were written; the live caller passed neither, so every file landed in
                # a bare role folder. Measured on run max-604740ffad: 43 of 43 records had no phase.
                phase=str(p.get("phase") or ""),
                phase_index=(int(p["phase_index"])
                             if isinstance(p.get("phase_index"), (int, float)) else None),
                # THE STEP NUMBER, derived here now that this is the ONLY registrar. WS-30 T5.
                #
                # The code runner used to compute this and register with it, which is the reason two
                # registrars existed at all. It counted the numbered scripts in `source/`, and so does
                # this: the count is a property of the workspace, not of whoever happens to be asking.
                step_seq=_step_seq_for(session),
            ) or []
        return {"ok": True, "files": produced}
    except Exception as ex:  # noqa: BLE001
        return {"ok": False, "error": type(ex).__name__, "detail": str(ex)[:200]}


def _snapshot(p: Dict[str, Any]) -> Dict[str, Any]:
    """The filesystem state to diff a later registration against."""
    from modulon.engine import filereg

    session = str(p.get("session") or "")
    if not session:
        return {"ok": False, "error": "no_session"}
    try:
        return {"ok": True, "before": filereg.snapshot_before(session)}
    except Exception as ex:  # noqa: BLE001
        return {"ok": False, "error": type(ex).__name__, "detail": str(ex)[:200]}


def _cancel_container(req):
    """Stop a running container job on the dispatch host, at the researcher's request.

    THE OPERATOR asked for "a botton to cancell the run so user can control the remove jobs". A long GPU job the
    researcher can see and cannot stop is worse than one they cannot see: the A100 is shared, so a wrong job left
    running blocks the next one.

    BY NAME AND NOTHING ELSE. The name is supplied by the caller, having reached the console on that job's own progress
    beat, so this stops the container the researcher was actually looking at rather than resolving a name here and
    possibly choosing a different one.

    A MISS IS REPORTED AS A MISS. A name matching no running container returns ok false, because "cancelled" has to mean
    it stopped. Treating that as success is how a researcher comes back to find the GPU still busy.

    NARROW BY CONSTRUCTION: the name is validated against the shape docker accepts before it is used, and quoted, so
    nothing from the wire reaches the shell as anything other than a container name.
    """
    import re as _re
    import shlex as _shlex
    name = str(req.get("container") or "").strip()
    if not name or not _re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.\-]{0,127}", name):
        return {"ok": False, "error": "bad_container_name"}
    try:
        from modulon.engine.dispatch import _ssh, GPU_HOST
        rc, out, err = _ssh("docker rm -f %s" % _shlex.quote(name), timeout=30)
        # THE EXIT CODE IS NOT THE ANSWER, MEASURED. `docker rm -f` on a container that does not exist returned rc 0
        # while printing "Error response from daemon: No such container", so trusting rc alone reported a cancel that
        # stopped nothing as a success. A researcher told the job was cancelled who returns to a busy GPU has been
        # misled by their own tool.
        #
        # DOCKER'S OWN ANSWER DECIDES. On success it echoes the name it removed; on failure it says so. Both are read.
        _blob = (str(out or "") + " " + str(err or "")).strip()
        stopped = rc == 0 and "error response from daemon" not in _blob.lower()
        return {
            "ok": stopped,
            "container": name,
            "host": str(GPU_HOST or ""),
            "detail": (str(out or "").strip() or str(err or "").strip())[:300],
        }
    except Exception as ex:  # noqa: BLE001
        return {"ok": False, "error": type(ex).__name__, "detail": str(ex)[:200]}


def _poll_cluster_job(req):
    """Ask the scheduler what a job is doing, and collect its outputs when it is over.

    THE WATCHER LIVES IN THE LONG-LIVED PROCESS AND ASKS THROUGH HERE. `governance/cluster.py` already has a watcher
    thread with backoff polling, and it dies with the process that started it: the MCP server is spawned PER QUERY, so
    the moment the run ended the thread went and the in-memory job table with it. MEASURED as "this run did not submit
    job 6102452" when a later run asked about a job that was queued and real.

    Returns the coarse state the poll needs AND the scheduler's own word, because "pending" and "running" are different
    facts to a researcher and only the first tells them to wait.
    """
    job_id = str(req.get("job_id") or "").strip()
    provider = str(req.get("provider") or "").strip()
    run_id = str(req.get("run_id") or "").strip()
    user_id = str(req.get("user_id") or os.environ.get("RAYCA_USER_ID", "")).strip()
    into = str(req.get("results_into") or "").strip()
    if not job_id or not provider:
        return {"ok": False, "error": "job_id and provider are required"}
    try:
        from modulon.governance import remote as _remote
        # THE SIBLING GUARD HAS TO BE PASSED HERE, AND IT WAS NOT.
        #
        # FOUND BY AN INDEPENDENT AUDIT 2026-09-05. F1 stopped a finished job deleting the working directory a still-running
        # sibling was using, and it was wired into cluster.py's own watcher. But THAT watcher dies with the MCP process, which
        # is the entire reason this bridge exists: the long-lived Node service polls through here. So the protection was absent
        # from the only path that cleans up in production, and the fault that cost a researcher 80 minutes of GH200 time and an
        # almost complete trajectory was still live after being declared fixed.
        #
        # cluster.siblings_of is the same predicate cluster.py passes, imported lazily like every other governance import here.
        def _siblings():
            from modulon.governance import cluster as _cl

            return _cl.siblings_of(run_id, job_id)

        got = _remote.poll_remote(user_id, provider, run_id, job_id, results_into=into,
                                  siblings_busy=_siblings)
        # EVERY FIELD `poll_remote` PRODUCES MUST BE LISTED HERE, AND ONE WAS NOT.
        #
        # MEASURED 2026-09-05. `reason` shipped on 09-04: the engine produced it, server.mjs forwarded it, store.mjs had a
        # column, and a seam test proved the value round-tripped through the store. Then 21 overnight jobs recorded no reason,
        # because THIS dict rebuilds the reply by hand and the new key was not in its list. Every end was correct and the field
        # died in the middle -- the same shape as the `scope` field a console proxy dropped on 09-03, which destroyed a 7,253
        # character note, and the third time this shape has cost something in one week.
        #
        # STILL AN EXPLICIT LIST rather than a blind pass-through, because this reply becomes one JSON line between processes
        # and a file list can be long. `tests/test_bridge_forwards_poll_fields.py` compares this list against what poll_remote
        # can actually return, so a new field now fails a test instead of vanishing.
        return {"ok": True, "job_id": job_id,
                "state": str(got.get("state") or "running"),
                "scheduler_state": str(got.get("scheduler_state") or ""),
                "queued": bool(got.get("queued")),
                "files": list(got.get("files") or []),
                "reason": str(got.get("reason") or "")[:400],
                "workdir_kept": str(got.get("workdir_kept") or "")[:300],
                "detail": str(got.get("detail") or "")[:300]}
    except Exception as ex:  # noqa: BLE001 - a transient ssh failure is not a finished job
        return {"ok": False, "error": type(ex).__name__, "detail": str(ex)[:240]}


def main() -> int:
    ops = {
        "poll_cluster_job": _poll_cluster_job,
        "cancel_container": _cancel_container,
        "register_run": _register_run,
        "workspace": _workspace,
        "snapshot": _snapshot,
        "register_files": _register_files,
        "files_for_run": _files_for_run,
        "phase_report": _phase_report,
        "dashboard_brief": _dashboard_brief,
        "dashboard_finalise": _dashboard_finalise,
        "update_run": _update_run,
        "interpret_workflow": _interpret_workflow,
        "lineage_event": _lineage_event,
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
