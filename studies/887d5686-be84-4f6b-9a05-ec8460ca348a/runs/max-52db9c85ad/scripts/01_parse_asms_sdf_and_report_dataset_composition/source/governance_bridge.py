#!/usr/bin/env python3
"""The governance layer, in front of a loop that does not have one.

WHY THIS FILE EXISTS. Claude Code's loop is better at running scientific work than the engine we wrote. It has no
opinion whatever about whether the work is honest. The Rayca platform's value is the opposite: gates before expensive
or irreversible actions, a credit ledger, provenance for every figure, and a judge that refuses a report stating a
number nothing computed. None of that is in the SDK, and adopting the loop without it would trade a truthful engine
for a capable one.

MEASURED NEED, from the pilot's own runs on 2026-08-21:

  - LigandMPNN returned sequences at confidence 0.23 that were almost entirely charged residues, and nothing in the
    path said so. A researcher reading that report would have taken them as candidates.
  - A job was submitted to a national supercomputer whose script fabricated its RMSD and energy values from a loop
    counter. Every provenance check would have passed it: real job, real cluster, exit code 0, real output file.
  - `binderflow` returned rc=0 four times having generated nothing, and the model responded by loosening scoring
    thresholds -- which cannot help when there is nothing to score.

SPEAKS JSON LINES ON STDIN AND STDOUT so the Node engine can consult it per tool call without embedding Python. One
process, kept alive for the life of the engine, because starting an interpreter per tool call would add a second to
every dispatch.

REPORTS RATHER THAN REFUSES, EXCEPT WHERE REFUSING IS THE ONLY HONEST ANSWER. A judgement about scientific quality
belongs to the researcher. A script that declares itself a placeholder before burning cluster time does not.
"""

from __future__ import annotations

import json
import os
import sys
import traceback
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from env_select import resolve_src  # noqa: E402  the one place environment is decided
sys.path.insert(0, resolve_src())


def log(msg: str) -> None:
    sys.stderr.write("[governance] %s\n" % msg)
    sys.stderr.flush()



class Auditor:
    """A model for the claim judge, which is the part I disabled and then compensated for badly.

    `judge_claims` is BUILT to reason about a borderline figure with a model: its `llm` parameter is documented as any
    object with `.invoke(str) -> reply`. I passed None, which takes the documented no-auditor path -- "not a refusal" --
    and then downgraded the verdict myself to stop unsourced figures passing silently. That downgrade was right given no
    auditor, and wrong as a permanent arrangement, because it cannot tell the two cases apart:

      FABRICATED, and must fail: a member with no tool access computed caffeine's mass by hand and reported 194.19.
      EXPLANATORY, and must not: an answer computed 194.08150 through run_python and then showed its working by quoting
      standard atomic weights -- 12.0, 1.00794, 14.00307, 15.99491. All four were flagged and the whole report was
      marked unverified, even though the figure a researcher would act on was properly computed.

    A crude filter cannot separate those without semantics, and every attempt I have made at prose rules in this codebase
    has been wrong. So the judge gets what it was designed to have.

    SAME PROXY THE ENGINE USES, so there is one place model access is configured. A CHEAP model on purpose: this is an
    audit of a short text, not the science, and paying the run's own rate to check it would double the cost of honesty.
    """

    def __init__(self) -> None:
        self.base = os.environ.get("RAYCA_LLM_BASE_URL", "http://127.0.0.1:4000").rstrip("/")
        self.key = os.environ.get("RAYCA_LLM_API_KEY", "") or os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = os.environ.get("RAYCA_JUDGE_MODEL", "claude-haiku-4-5")

    def invoke(self, prompt: str) -> str:
        """Never raises. A judge that throws would take a run's report down with it; one that returns nothing is
        handled by the caller as "the auditor could not run", which is a fact rather than a verdict."""
        import json as _json
        import urllib.request

        body = _json.dumps({
            "model": self.model,
            "max_tokens": 900,
            "messages": [{"role": "user", "content": prompt}],
        }).encode()
        req = urllib.request.Request(
            self.base + "/v1/messages",
            data=body,
            headers={"content-type": "application/json", "anthropic-version": "2023-06-01",
                     "authorization": "Bearer " + self.key},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                out = _json.loads(r.read().decode())
            blocks = out.get("content") or []
            return "".join(b.get("text", "") for b in blocks if isinstance(b, dict))
        except Exception as ex:  # noqa: BLE001
            log("auditor unavailable: %s" % str(ex)[:160])
            return ""


class Governor:
    """Holds one run's governance state: what ran, what it cost, and what was claimed."""

    def __init__(self) -> None:
        self.runs: Dict[str, Dict[str, Any]] = {}

    # -- lifecycle ---------------------------------------------------------------------------------------------------

    def begin(self, run_id: str, mode: str = "") -> Dict[str, Any]:
        self.runs[run_id] = {"tool_results": [], "credits": 0.0, "gpu_seconds": 0.0, "notes": []}
        try:
            from modulon.governance import gates

            gates.begin_run(run_id, mode or None)
            return {"ok": True, "gates": "open", "mode": gates.normalize_mode(mode or None)}
        except Exception as ex:  # noqa: BLE001
            return {"ok": True, "gates": "unavailable", "detail": str(ex)[:200]}

    def end(self, run_id: str) -> Dict[str, Any]:
        try:
            from modulon.governance import gates

            gates.end_run(run_id)
        except Exception:  # noqa: BLE001
            pass
        st = self.runs.get(run_id) or {}
        return {"ok": True, "credits": round(float(st.get("credits") or 0.0), 4),
                "gpu_seconds": round(float(st.get("gpu_seconds") or 0.0), 1),
                "tool_calls": len(st.get("tool_results") or [])}

    # -- before a tool runs ------------------------------------------------------------------------------------------

    def before_tool(self, run_id: str, verb: str, origin: str, payload: Any) -> Dict[str, Any]:
        """The only place a tool can be stopped before it spends anything.

        REFUSES EXACTLY ONE CLASS, and it is the one measured this morning: a cluster script that declares in its own
        text that it is a placeholder. Job 6081554 asked Isambard AI for a GH200 for two hours to write files whose
        contents were the sentence "Dummy trajectory file", and an analysis CSV whose RMSD column was `5.0 + i * 0.5`.
        The markers are the author's own admissions, so refusing on them is taking the author at their word rather
        than inferring intent.
        """
        st = self.runs.setdefault(run_id, {"tool_results": [], "credits": 0.0, "gpu_seconds": 0.0, "notes": []})
        body = json.dumps(payload, default=str).lower() if not isinstance(payload, str) else payload.lower()

        admissions = [m for m in (
            "placeholder", "dummy trajectory", "dummy data", "in a real implementation",
            "actual implementation would", "would contain actual", "fake data", "stub implementation",
            "for demonstration purposes only",
        ) if m in body]
        if admissions and verb in ("run_on_cluster", "run_python", "run_pipeline"):
            return {
                "allow": False,
                "reason": "declares_itself_a_placeholder",
                "detail": ("This code says in its own text that it does not do the work: %s. It was NOT run. "
                           "Compute time produces numbers a researcher will read as measurements, so code that "
                           "generates values it did not compute is worse than no code at all. Write the real "
                           "calculation, or say plainly that you cannot do this step and why."
                           % ", ".join(repr(a) for a in admissions[:5])),
            }

        # A CEILING IS A GATE, NOT A REFUSAL. Crossing it asks the researcher; it does not decide for them.
        ceiling = float(os.environ.get("RAYCA_CREDIT_CEILING", "0") or 0)
        if ceiling and float(st.get("credits") or 0.0) >= ceiling:
            return {"allow": True, "gate": {"kind": "credit_ceiling", "spent": round(st["credits"], 2),
                                            "ceiling": ceiling,
                                            "detail": "this run has passed its credit ceiling and is continuing"}}
        return {"allow": True}

    # -- after a tool returns ----------------------------------------------------------------------------------------

    def after_tool(self, run_id: str, verb: str, origin: str, output: str, seconds: float = 0.0) -> Dict[str, Any]:
        """Record what ran, price it, and say when a success produced nothing.

        THE TOOL RESULT SHAPE IS THE ENGINE'S. `provenance_of` and `judge_claims` both read tool-role messages with
        `tool_call_id`, `name` and `content`, so the same shape is kept here rather than invented, which is what lets
        the existing judge work unchanged against a loop it was never written for.
        """
        st = self.runs.setdefault(run_id, {"tool_results": [], "credits": 0.0, "gpu_seconds": 0.0, "notes": []})
        st["tool_results"].append({
            "tool_call_id": "%s-%d" % (verb, len(st["tool_results"])),
            "name": verb,
            "content": output if isinstance(output, str) else json.dumps(output, default=str),
        })

        notes: List[Dict[str, Any]] = []
        if seconds and origin == "platform":
            try:
                from modulon.governance import credits as _c

                gpu = float(seconds)
                st["gpu_seconds"] = float(st.get("gpu_seconds") or 0.0) + gpu
                st["credits"] = float(st.get("credits") or 0.0) + _c.credits_for_gpu_seconds(gpu)
            except Exception:  # noqa: BLE001
                pass

        low = (output or "")[:20000]
        if "rc=1" in low or "tool_failed" in low:
            notes.append({"kind": "tool_failed", "verb": verb,
                          "detail": "the tool ran and failed; read its error before changing anything else"})
        return {"ok": True, "notes": notes,
                "credits": round(float(st.get("credits") or 0.0), 4)}

    # -- the answer --------------------------------------------------------------------------------------------------

    def judge(self, run_id: str, answer: str) -> Dict[str, Any]:
        """Does the report state a number that nothing computed?

        THIS IS THE WHOLE POINT OF THE PLATFORM. A capable loop that fabricates a figure is more dangerous than one
        that crashes, because the figure is readable and the crash is not. `provenance_of` resolves every numeric claim
        in the report to the tool call that produced it; `judge_claims` is only consulted when some claim resolves to
        nothing, which is the contract those two functions already have with each other.
        """
        st = self.runs.get(run_id) or {"tool_results": []}
        results = st.get("tool_results") or []
        if not answer.strip():
            return {"ok": True, "verdict": "empty_answer", "complaints": []}
        try:
            from modulon.engine import provenance as _p

            rep = _p.provenance_of(answer, results)
            claims = list(getattr(rep, "claims", []) or [])
            unsourced = [str(getattr(c, "text", getattr(c, "value", ""))) for c in claims
                         if not bool(getattr(c, "sourced", True))]
            self_computed = [str(getattr(c, "text", getattr(c, "value", ""))) for c in claims
                            if bool(getattr(c, "self_computed", False))]
        except Exception as ex:  # noqa: BLE001
            return {"ok": True, "verdict": "provenance_unavailable", "detail": str(ex)[:250], "complaints": []}

        if not unsourced:
            return {"ok": True, "verdict": "all_figures_sourced", "figures": "sourced", "untraced": [],
                    "traced": len(claims), "total_claims": len(claims),
                    "claims": len(claims),
                    "self_computed": len(self_computed), "complaints": []}
        try:
            from modulon.engine import claimjudge as _j

            auditor = Auditor()
            status: Dict[str, Any] = {}
            ok, complaints = _j.judge_claims(answer, results, llm=auditor,
                                             unsourced=unsourced, self_computed=self_computed,
                                             status=status)
            complaints = [str(c)[:400] for c in (complaints or [])]
            audited = bool(status.get("ran"))

            # AN UNADJUDICATED FIGURE IS NOT AN APPROVED ONE.
            #
            # MEASURED: a report claiming "binding affinity is 12.7 nM" with no tool having produced 12.7 came back
            # ok=True. `judge_claims` is built to reason about a borderline figure WITH a model; called with llm=None
            # it cannot, and its permissive default is right for a judge and wrong for a gate. So the verdict is
            # downgraded here rather than in the judge, whose own contract is unchanged.
            #
            # `self_computed` is excluded deliberately. A figure printed by the model's own run_python IS evidence,
            # just not independent evidence -- collapsing the two caused a measured false refusal when a phase computed
            # a pocket centroid from a PDB file the engine had itself downloaded and tracked.
            unadjudicated = [u for u in unsourced if u not in set(self_computed)]
            # ONLY WHEN THE AUDITOR DID NOT RUN. With a model, `judge_claims` has already weighed these figures and its
            # answer stands: overriding a judgement that was actually made is how a governance layer starts crying wolf,
            # and a layer that cries wolf gets ignored precisely when it is right.
            if ok and unadjudicated and not audited:
                ok = False
                complaints.append(
                    "These figures appear in no tool output and could not be adjudicated because no model was "
                    "available to the judge: %s. Treat them as unverified rather than as measurements."
                    % ", ".join(unadjudicated[:8]))
            # THREE STATES, BECAUSE THERE ARE THREE SITUATIONS AND COLLAPSING THEM MISLEADS EITHER WAY.
            #
            # MEASURED, with a real auditor: an answer that computed caffeine's mass through run_python and then quoted
            # standard atomic weights to show its working was passed (correctly -- the figure a researcher acts on was
            # computed). An answer claiming a docking affinity with no docking tool run was refused, with a precise
            # complaint. And an answer stating a molecular weight with NO tool run at all was ALSO passed, because the
            # auditor treats a textbook property as knowledge rather than as a measurement.
            #
            # That last one is a real limit. So the raw fact travels regardless of the verdict: `untraced` is what
            # appears in no tool output, and a reader sees it even when the judge excused it. Reporting "figures
            # sourced" while the gate lists an untraced figure is a contradiction a console should never show, and
            # pretending to a semantic judgement I cannot make reliably is worse than naming the limit.
            # COUNTS ARE FACTS; THE VERDICT IS AN OPINION, AND THEY MUST NOT BE PRESENTED AS THE SAME THING.
            #
            # MEASURED on run max-f084f1c06b: the report computed aspirin's logP (1.310) and TPSA (63.6) through
            # run_python, and provenance traced BOTH. The only untraced figures were 5.0 and 140.0 -- the Lipinski
            # thresholds quoted as reference bounds. The auditor refused anyway, and its complaint blamed logP and TPSA,
            # which were sourced. So its verdict alone cannot drive a red light: it was wrong about which figures were
            # the problem, and it refuses cited cutoffs while passing a bare unsourced molecular weight.
            #
            # What is TRUE and cheap: how many numeric claims resolved to a tool and which did not. A reader given
            # "12 of 14 figures trace to a tool; these two do not: 5.0, 140.0" can judge for themselves, and the
            # auditor's note travels beside it as an opinion rather than as a verdict.
            traced = max(0, len(claims) - len(unsourced))
            # THE COLOUR FOLLOWS THE ARITHMETIC; THE AUDITOR'S WORDS TRAVEL BESIDE IT.
            #
            # MEASURED on a CPTAC multi-omics run: 74 of 80 figures traced to tool output, and the six that did not were
            # a CITATION YEAR (2020, from the Gillette 2020 Cell paper), a sample count and two thresholds. The auditor
            # refused anyway and its complaint named gene counts that the run had demonstrably computed and saved. Showing
            # that report in the same accusing red as a fabricated binding affinity is not a judgement, it is noise, and
            # noise in this signal is what teaches a reader to ignore it.
            #
            # SO `unverified` NOW MEANS THE REPORT DOES NOT REST ON TRACED WORK: nothing traced, or the untraced figures
            # outnumber the traced ones. Anything else with untraced figures is `partly_untraced`, which still names every
            # one of them in amber. The auditor's prose is preserved either way, so a real fabrication it has identified
            # is still readable; what changes is that its boolean can no longer paint a 92% traced report red on its own.
            if not unadjudicated:
                state = "sourced"
            elif traced == 0 or len(unadjudicated) > traced:
                state = "unverified"
            elif not ok:
                state = "partly_untraced"
            else:
                state = "partly_untraced"
            return {"ok": bool(ok), "verdict": "judged" if audited else "judged_without_auditor",
                    "figures": state, "untraced": unadjudicated[:12],
                    "traced": traced, "total_claims": len(claims),
                    "audited": audited, "claims": len(claims),
                    "unsourced": unsourced[:12], "unadjudicated": unadjudicated[:12],
                    "self_computed": len(self_computed), "complaints": complaints}
        except Exception as ex:  # noqa: BLE001
            # A judge that cannot run must not silently approve. The unsourced figures are reported as they stand.
            return {"ok": False, "verdict": "judge_unavailable", "detail": str(ex)[:250],
                    "unsourced": unsourced[:12], "complaints": ["the claim judge could not run; figures unverified"]}


def main() -> int:
    g = Governor()
    ops = {
        "begin": lambda p: g.begin(p.get("run_id", ""), p.get("mode", "")),
        "end": lambda p: g.end(p.get("run_id", "")),
        "before_tool": lambda p: g.before_tool(p.get("run_id", ""), p.get("verb", ""), p.get("origin", ""),
                                               p.get("input")),
        "after_tool": lambda p: g.after_tool(p.get("run_id", ""), p.get("verb", ""), p.get("origin", ""),
                                            p.get("output", "") or "", float(p.get("seconds") or 0)),
        "judge": lambda p: g.judge(p.get("run_id", ""), p.get("answer", "") or ""),
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
        fn = ops.get(str(req.get("op") or ""))
        if fn is None:
            out = {"error": "no_such_op", "op": req.get("op")}
        else:
            try:
                out = fn(req)
            except Exception:  # noqa: BLE001
                out = {"error": "governance_failed", "detail": traceback.format_exc(limit=2)[:600]}
        sys.stdout.write(json.dumps({"id": rid, "result": out}, default=str) + "\n")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
