---
audit_of: phase_01_task_1
auditor: subagent (independent)
date: 2026-09-02
---

# Audit: Phase 1 — Retrosynthetic Analysis of 7 Compounds

All checks were performed independently by reading source files and JSON result files
directly. No assumptions were shared with the prior agent.

---

## MAJOR findings

### MAJOR-1: Phase document contains no substantive results

**File:** `reports/phase_01_task_1.md`

The document reads: "This phase produced no captured result output." and "No method
records were captured for this phase, so the procedure cannot be stated." The fields
Summary, Results, and Methods are boilerplate only. The full retrosynthetic analysis of
seven compounds was delivered as conversation text and exists in no file in the session
workspace. No results file, analysis file, or summary file was written. The 21 artifacts
in the workspace are source scripts and raw JSON; none of them is a human-readable
analysis document.

**Evidence:** `phase_01_task_1.md` lines 41-44, plus `find` listing showing no analysis
text file under the session root.

---

### MAJOR-2: `002_dispatch_all_6_drug_like_targets_aizynthfinder.py` — wrong dispatch call signature; script failed at runtime

**File:** `source/002_dispatch_all_6_drug_like_targets_aizynthfinder.py`, lines 14-24

The script calls:
```python
h = dispatch(
    "aizynthfinder",
    smiles=smi,
    iteration_limit=200,
    time_limit=180,
    ...
)
```

The actual `dispatch` signature (verified independently via `inspect.signature`):
```
(tool_id: str, inputs: Optional[Dict[str, Any]] = None, *,
 files: Optional[Dict[str, Any]] = None, gpu: Optional[bool] = None,
 timeout: int = 1800, ...) -> Dict[str, Any]
```

`dispatch` accepts only `tool_id` and `inputs` as positional parameters. There is no
`smiles`, `iteration_limit`, `time_limit`, `max_routes`, `min_routes`,
`max_transforms`, `expansion_policy`, or `filter_policy` parameter. Calling with any of
these as keyword arguments raises `TypeError: dispatch() got an unexpected keyword
argument 'smiles'` at line 14 on the first loop iteration.

**This script failed for all six compounds.** The actual results in `aiz_results_batch1.json`
were produced by `004_nc2nc3c.py`, which correctly wraps parameters in `inputs={...}`.
Scripts 004, 005, 006, and 007 all use the correct pattern.

**Evidence:** Dispatch signature obtained via `inspect.signature(dispatch)` in the
platform run_python environment. The `inputs={}` pattern used in 004/005/006/007
compared against the flat-kwarg pattern in 002.

---

### MAJOR-3: `009_show_routes.py` — wrong field name for route tree causes silent malformed output

**File:** `source/009_show_routes.py`, line 30

```python
tree = route.get("route_tree", {})
```

The actual field name in every JSON result file is `"reaction_tree"`, not `"route_tree"`.
This was verified independently against all five result JSON files and the
`all_aiz_results.json` dispatch envelopes:

```
routes[0] keys: ['rank', 'is_solved', 'depth', 'n_reactions', 'n_leaves',
                 'n_leaves_in_stock', 'reaction_tree', 'metadata', 'scores']
```

The key `"route_tree"` does not exist in any route object. `route.get("route_tree", {})`
always returns `{}`.

Because `{}` is falsy, the `if tree:` branch is skipped. The `else` branch executes:
```python
rxns = route.get("reactions", route.get("reaction_tree", []))
```
`"reactions"` is absent; `"reaction_tree"` is present and returns the tree dict
(not a list). `for r in rxns:` then iterates over the dict's top-level string keys
(`"type"`, `"smiles"`, `"metadata"`, `"children"`) and prints each key name. No tree
structure is rendered. No exception is raised. The failure is silent.

**Evidence:** JSON structure confirmed by running `json.load()` on all five result files
and inspecting `routes[0].keys()`. The actual key `"reaction_tree"` is present and
`"route_tree"` is absent across all files.

---

### MAJOR-4: `008_load_all_individual_result_files.py` — wrong nesting assumption; crash swallowed by bare except

**File:** `source/008_load_all_individual_result_files.py`, lines 14, 18, 56-58

Line 14 assumes a dispatch-envelope wrapping:
```python
out = data.get("output", {})
```
The individual JSON files (`aizynthfinder-results*.json`) are direct AiZynthFinder output
with top-level keys `is_solved`, `routes`, `top_score`, etc. There is no `output` key.
`out` is always `{}`.

As a result, `out.get('top_score', '?')` returns `'?'`. The format call on line 18:
```python
f"top_score={out.get('top_score','?'):.4f}"
```
raises `ValueError: Unknown format code 'f' for object of type 'str'`.

This exception is caught by the bare `except Exception as e:` on line 58:
```python
except Exception as e:
    print(f"{name}: ERROR loading {fname}: {e}")
```
Every compound prints as a loading error. No route data is shown. No stack trace is
raised. The script appears to run to completion while producing no useful output.

Line 41 also has the wrong field name `"route_tree"` (same issue as MAJOR-3), but the
script crashes before reaching that line.

**Evidence:** Top-level keys of `aizynthfinder-results.json` confirmed via `json.load()`.
The `:.4f` format on `'?'` raises ValueError, which `except Exception` silently catches.

---

## VERIFIED CORRECT

### VC-1: B54 returned rc=None — claim confirmed against data

`all_aiz_results.json` B54 entry has `rc=None, output=None`. Keys:
`['tool_id', 'image', 'rc', 'gpu', 'duration_s', 'error', 'unstaged', 'summary', 'hint']`.
The phase summary claim that B54 returned rc=None is correct.

`007_retry_b54.py` does not silently swallow the None. Line 16 prints `rc=None`
explicitly. The failure is visible in output, though the script does not raise an
exception or halt on non-zero/None rc — it saves the failed dispatch result to
`all_aiz_results.json` without a guard, which is a mild robustness issue but not a
silent swallow.

One real fragility: line 17 (`all_results["B54"] = res_b54`) depends on `all_results`
being already defined in the session namespace from `006`. The script has no import or
definition of `all_results`. If run standalone, it raises `NameError`. In practice it
succeeded because it ran in the same persistent run_python namespace as `006`.

---

### VC-2: 8008 unsolved because `O=S(=O)(O)Cl` not in ZINC stock — claim confirmed against data

Independently verified by collecting all leaf SMILES from all five routes in
`aizynthfinder-results-3.json`. Every route has exactly one out-of-stock leaf:
`O=S(=O)(O)Cl` (chlorosulfonic acid), `in_stock=False`. All other leaves in all five
routes are in stock. The phase summary claim is accurate and matches the data exactly.

---

### VC-3: `reaction_tree` is the correct AiZynthFinder field name — confirmed across all result files

Independently confirmed: `routes[0]` in every result file (`aizynthfinder-results.json`,
`-2.json`, `-3.json`, `-4.json`, `-5.json`) and in all dispatch-envelope entries in
`all_aiz_results.json` uses `"reaction_tree"`, not `"route_tree"`. The phase summary
statement that the correct key is `reaction_tree` is accurate.

Scripts `011_extract_leaves_reactions.py` (line 41) and
`012_print_complete_mapped_reaction_trees_a317_7977_most.py` (line 32) use the correct
name. Scripts `008` and `009` use the wrong name (see MAJOR-3 and MAJOR-4).

---

### VC-4: A317 Route 1 reaction template class "0.0 Unrecognized" — confirmed

Independently verified by reading `aizynthfinder-results-2.json`. Every reaction node
in every A317 route (all three routes) has `"classification": "0.0 Unrecognized"`. No
named reaction template class appears in any route. The phase summary claim about
"0.0 Unrecognized" is correct.

The parsed route data via `all_parsed_routes.json` (produced by `011`) confirms:
Route 1 reactions at depths 1, 3, 5, 3, 5 all have `class=0.0 Unrecognized`.

---

### VC-5: A317 Route 1 regiochemical error — single data point, no independent verification in workspace

The phase summary claims that A317 Route 1 contains a regiochemical error (AiZ places
the pyrrolidinyl at C5 instead of C4 in Hantzsch synthesis).

**Assessment:** This claim is chemical interpretation of the mapped reaction SMILES, not
a finding recorded in the data. No file in the workspace contains independent chemical
validation of this assessment. The mapped SMILES for the Route 1 top-level reaction is
present in the JSON, but interpreting positional substitution requires reading the atom
map and comparing it to Hantzsch regiochemistry rules — work done by the analyst, not
by any script. The claim is derived from a single AiZ output and from the analyst's
chemical reasoning; there is no cross-check against a literature source or a second
independent tool.

The "0.0 Unrecognized" classification means AiZ itself did not assign a named reaction
type, so AiZ provided no regiochemical label. The error assessment is entirely the
analyst's.

This is not labeled MAJOR because the claim may be chemically correct — it just has no
supporting evidence in the workspace files beyond the raw mapped SMILES.

---

### VC-6: `011_extract_leaves_reactions.py` uses correct field names and JSON structure

All accesses in this script are consistent with the actual JSON structure:
- Line 38: `raw.get("routes", [])` — correct (top-level key)
- Line 41: `r.get("reaction_tree", {})` — correct field name
- Line 44: `r["rank"]`, `r["is_solved"]`, `r["depth"]`, `r["n_reactions"]`,
  `r["n_leaves"]`, `r["n_leaves_in_stock"]` — all present in `routes[0]`
- Line 60: `raw.get("is_solved")`, `raw.get("top_score")` — top-level keys, correct

No off-by-one, no reversed argument, no field name confusion in this script.
`all_parsed_routes.json` (output of this script) should be structurally correct.

---

### VC-7: No 0-based vs 1-based off-by-one errors in compound enumeration

`001_chem_sdmolsupplier.py` uses `for i, mol in enumerate(suppl)` and consistently
uses `i+1` for all display (lines 15, 32, 36). Route ranks in JSON start from 1 and
are accessed by iteration, not by numeric index. No off-by-one errors found.

---

### VC-8: dispatch() signature independently confirmed

`dispatch` is a built-in provided in the run_python namespace; it is not importable from
`modulon.governance.toolkit`. Confirmed via `inspect.signature(dispatch)`:
```
(tool_id: str, inputs: Optional[Dict[str, Any]] = None, *,
 files: Optional[Dict[str, Any]] = None, gpu: Optional[bool] = None,
 timeout: int = 1800, source: Optional[Any] = None,
 user_id: str = '', compute: str = '',
 allowed_credential_ids: Optional[Any] = None) -> Dict[str, Any]
```
The `inputs` dict is the correct way to pass tool parameters. Scripts 004, 005, 006,
and 007 all use this correctly.

---

## Summary table

| ID | Severity | Description |
|---|---|---|
| MAJOR-1 | MAJOR | Phase document is boilerplate only; no analysis captured in any file |
| MAJOR-2 | MAJOR | `002`: wrong dispatch signature; script failed at runtime for all 6 compounds |
| MAJOR-3 | MAJOR | `009`: `"route_tree"` key wrong; silent malformed output for all routes |
| MAJOR-4 | MAJOR | `008`: wrong JSON nesting + crash swallowed by bare except; no route data shown |
| VC-1 | VERIFIED | B54 rc=None confirmed in `all_aiz_results.json` |
| VC-2 | VERIFIED | 8008 missing leaf `O=S(=O)(O)Cl` confirmed in all 5 routes |
| VC-3 | VERIFIED | `reaction_tree` is the correct field name; scripts 011 and 012 use it correctly |
| VC-4 | VERIFIED | All A317 reactions are "0.0 Unrecognized" — confirmed from JSON |
| VC-5 | VERIFIED | A317 regiochemical error claim is analyst interpretation from one data point; no independent check in workspace |
| VC-6 | VERIFIED | `011_extract_leaves_reactions.py` uses correct field names throughout |
| VC-7 | VERIFIED | No off-by-one errors in compound enumeration |
| VC-8 | VERIFIED | `dispatch()` signature confirmed; correct calling convention is `inputs={}` |
