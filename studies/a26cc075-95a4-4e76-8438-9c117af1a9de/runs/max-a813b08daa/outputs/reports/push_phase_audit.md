# Audit: Push session artifacts to RSA-Edelris/RaycaBio

**Session:** a26cc075-95a4-4e76-8438-9c117af1a9de  
**Commit:** 92a3f4492b48884f26de47bdda274510db1fea1e  
**Repo:** RSA-Edelris/RaycaBio, branch main  
**Files committed:** 71  
**Tool:** mcp__rayca__push_to_github  
**Audited source:** /home/ubuntu/rayca-modulon-dev/src/modulon/tools/github.py  
**Audit date:** 2026-09-18  

---

## PRIMARY FINDING

**No phase document exists for this phase.**

All seven phase reports in the session's `reports/` directory cover earlier analytical phases
(HTE analysis, plate design, viridis redraw, plate labelling, etc.). None records the push. The
filenames are:

- phase_01_analyse_hte_hplc_data_and_generate_96_well_plate.md
- phase_01_design_next_96_well_hte_plate_dmcyda_optimizatio.md
- phase_01_hte_analysis_v2_viridis_plate_heatmap_condition_.md
- phase_01_redraw_96_well_plate_well_ids_plate_max_normalis.md
- phase_01_redraw_hte_viridis_heatmap_figure_with_white_bac.md
- phase_01_redraw_screen_2_plate_design_with_white_backgrou.md
- phase_01_regenerate_plate_heatmap_transposed_12_8_black_t.md

No push phase report was generated. There is no document to check any claim against, and the
checks below are therefore performed against the tool implementation that executed the push.

---

## FINDINGS

### MAJOR — Bare except swallows `refresh_repo_docs` failure; `ok: True` is returned regardless

**Location:** github.py lines 484–500

```python
docs = {}
try:
    docs = refresh_repo_docs(user_id, target, target_branch, ...)
except Exception as err:  # noqa: BLE001
    docs = {"ok": False, "error": "docs_failed", "detail": str(err)[:200]}

return {
    "ok": True,          # ← returned unconditionally
    ...
    "docs": docs.get("written") if isinstance(docs, dict) else None,
}
```

If `refresh_repo_docs` raises (network failure, permissions issue, tree unreadable), the bare
`except Exception` catches it, assigns a failure dict, and the function returns `"ok": True`
anyway. A consumer that checks only the top-level `ok` field concludes the push succeeded in
full when STUDIES.md and the session README may not have been written. The `docs: None` in the
return value is the only signal, and it is indistinguishable from "docs key not present" at a
glance.

The in-code comment (lines 480–482) acknowledges the intent: "a failure to refresh leaves the
study committed and only the index stale, which is the right way round." That design choice is
reasonable, but the consequence is that the push summary returned to the operator contains no
explicit flag distinguishing partial success (data committed, index stale) from full success
(both committed). A reader of the push result who sees `ok: True, docs: null` cannot tell
whether the null reflects no-docs-attempted or a silently swallowed exception.

**Impact on this run:** Cannot be confirmed from session records because no push phase report
exists. If `refresh_repo_docs` succeeded, STUDIES.md and the session README were written in a
second commit (as designed). If it failed, neither exists in the repository and the push result
would still have read `ok: True`.

---

## VERIFIED CORRECT

The following items were checked and held up:

### 1. `publish_study` call signature matches the installed function

**Checked:** github.py lines 452–463 against publish.py lines 714–727.

Installed signature (publish.py:714):
```
publish_study(contract, code_files, input_files, output_files,
              tool_versions, provenance_records,
              review_state=None, run_metadata=None, *,
              remote_url=None, threshold=..., path_prefix="")
```

Call site (github.py:452):
```
publish.publish_study(
    contract,
    parts["code_files"],      # positional 2: code_files
    parts["input_files"],     # positional 3: input_files
    parts["output_files"],    # positional 4: output_files
    tool_versions=[],
    provenance_records=parts["manifest"],
    run_metadata={...},
    remote_url=_plain_remote(target),
    path_prefix=repobind.study_path(session_id, run_id),
)
```

No positional reversal. `review_state` is intentionally omitted (defaults to None). The
installed version was read directly; this was not taken from memory.

### 2. No reversed positional arguments: `input_files` vs `output_files`

`parts["input_files"]` is always an empty dict `{}` in this path (set but never populated in
`bundle_inputs_for_session`). `parts["output_files"]` holds the artifact bytes. Even if their
positions were swapped, the call would behave identically at runtime. Confirmed they are in the
correct order regardless.

### 3. Path-segment indexing in `_studies_in` is correct (0-based, matches structure)

`study_path(session, run_id)` returns `"studies/<session>/runs/<run_id>"`.
After `path.split("/")`:  
- parts[0] = "studies" — checked against `STUDY_ROOT` ✓  
- parts[1] = session_id ✓  
- parts[2] = "runs" — gating check ✓  
- parts[3] = run_id ✓  

`len(parts) < 4` guard prevents out-of-bounds. No off-by-one error.

### 4. `STUDY_ROOT = "studies"` is used consistently; no identifier drift

`STUDY_ROOT` is defined once in repobind.py (line 41) and imported at each use site in
github.py. Both `_studies_in` (which parses paths) and `study_path` (which builds them) resolve
the same constant. No independent re-declaration or differing string literal.

### 5. `artifacts._read_index` and `artifacts.session_dir` names match installed module

github.py calls `artifacts._read_index(session_id)` (line 278) and
`_artifacts.session_dir(session_id)` (line 310). The installed artifacts.py defines
`def _read_index(session_key: str)` at line 198 and `def session_dir(session_key: str)` at
line 183. Both names resolve. The parameter is named `session_key` in the definition and
`session_id` at the call site — same value, different local names, no functional difference.

### 6. No 0-based vs 1-based numbering confusion found

No numeric indices, page numbers, or list offsets that mix 0-based and 1-based access. The
GitHub pagination uses 1-based page numbers (`page = 1`, then `page += 1`) which is correct for
the GitHub API. List indexing (`runs[-1]` for latest run, `findings[:8]` for truncation) is
standard Python 0-based indexing applied correctly.

### 7. `RSA-Edelris` (owner) vs `RaycaBio` (repo name) are not confused

`DEFAULT_OWNER = "RaycaBio"` in github.py is the default organisation name, not the repository
name. The push target `RSA-Edelris/RaycaBio` was passed as the explicit `repo` parameter, so
`DEFAULT_OWNER` was not consulted. No identifier substitution.

---

## SCOPE NOTE

Because no phase document exists, the audit cannot verify: what arguments were passed to
`push_to_github`, what the tool returned, whether `docs` was null or populated, or whether the
71-file count came from `files_committed` or some other count. All findings above are against
the tool implementation, not against a recorded trace of this specific invocation.
