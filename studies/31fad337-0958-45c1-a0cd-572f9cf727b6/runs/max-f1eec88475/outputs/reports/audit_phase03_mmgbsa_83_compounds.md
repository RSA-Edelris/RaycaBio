---
title: "Audit: Phase 3 MM-GBSA — 83 CDK2-CyclinE1 Compounds"
audit_target: "phase_03_mmgbsa_83_cdk2_cycline1_compounds.md"
auditor: "claude-sonnet-4-6 (independent)"
source_files_checked:
  - cdk2_campaign/mmgbsa_results.json
  - cdk2_campaign/gbsa_batch_results_00.json
  - cdk2_campaign/poses_all_H/CTX-1020732_best_pose_H.sdf
  - cdk2_campaign/receptor_gromacs_ready.pdb
  - cdk2_campaign/run_mmgbsa_threaded.py
date: "2026-09-06"
---

# Audit: Phase 3 MM-GBSA — 83 CDK2-CyclinE1 Compounds

## Scope

This audit checks the phase document and execution script against source data for:
1. Index / numbering errors (0-based vs 1-based)
2. Similar identifier confusion
3. Function signatures vs the installed package schema
4. Bare-except and silent-default patterns
5. Rules derived from a single data point
6. Reversed positional arguments

Numerical claims are verified directly from `mmgbsa_results.json` and `gbsa_batch_results_00.json`.

---

## MAJOR Findings

### MAJOR-1 — VdW mean in report text is wrong

**Location:** Phase document, "Docking vs MM-GBSA concordance" section.

**Claim:** "The dominant energy term is van der Waals burial (mean −57.6 kcal/mol across the series)"

**Actual value computed from mmgbsa_results.json:**

| Subset | VdW mean (kcal/mol) |
|:---|---:|
| All 83 compounds | **−54.671** |
| Top 20 compounds only | −73.309 |

Neither subset produces −57.6 kcal/mol. The all-series mean of −54.671 is consistent with the total ΔG mean of −55.199 (the polar and non-polar solvation terms partially cancel VdW and electrostatic, leaving a small residual). The stated value of −57.6 kcal/mol does not correspond to any computable subset or energy term in the source data.

The qualitative claim (VdW is the dominant term) is correct; only the stated magnitude is wrong.

**Impact:** Incorrect number in the descriptive analysis. Does not affect rankings or compound ΔG values.

---

### MAJOR-2 — Sort key uses `or 9999`, silently misclassifies dG = 0.0

**Location:** `run_mmgbsa_threaded.py`, line 100.

```python
all_results.sort(key=lambda x: x.get("dG_kcal_mol") or 9999)
```

**Problem:** Python's `or` operator tests truthiness. The value `0.0` is falsy, so a compound with exactly 0.0 kcal/mol binding free energy would evaluate as `0.0 or 9999 = 9999` and be sorted to the end of the list alongside failed calculations — silently mislabelled as a failure.

**Impact on current data:** All 83 computed dG values are negative (range −83.19 to −24.69); none equals 0.0. The sort order in `mmgbsa_results.json` is correct for this dataset (verified: strictly ascending). The bug is latent but will produce a silent wrong ranking if this script is reused on a compound set that includes a ligand with near-zero or exactly-zero binding affinity.

**Fix:** `key=lambda x: x.get("dG_kcal_mol") if x.get("dG_kcal_mol") is not None else 9999`

---

### MAJOR-3 — Thread timeout is silent; timed-out ligands leave no trace in merged JSON

**Location:** `run_mmgbsa_threaded.py`, lines 93–97.

```python
for t in threads:
    t.join(timeout=870)

elapsed = time.time() - t_start
print(f"\nAll threads joined in {elapsed:.0f}s")
```

**Problem:** `t.join(timeout=870)` returns when the timeout expires regardless of whether the thread has finished. The code never calls `t.is_alive()` after the join, so a thread that timed out is indistinguishable from one that completed. The daemon thread continues running after the main thread proceeds to sort and save `mmgbsa_results.json`; any ligands that thread was still processing are simply absent from the saved JSON, with no error entry and no warning.

The phase document reports "1 timeout" among the ligands, but detection and remediation depended entirely on the operator noticing a missing ligand in the final count — the code itself provides no signal. Had the operator not checked, a ligand would be missing from the final results with no record of failure.

**Impact on current data:** The four "cleanup" ligands (1 timeout + 3 transient failures) were re-run sequentially and their results are confirmed present in `mmgbsa_results.json`. Final data is complete.

---

### MAJOR-4 — Default 0.0 for missing energy components silently corrupts partial tool failures

**Location:** `run_mmgbsa_threaded.py`, lines 64–70.

```python
"TOTAL":              float(res.get("TOTAL", 0))             if res else None,
"Van_der_Waals":      float(res.get("Van der Waals", 0))     if res else None,
"Electrostatic":      float(res.get("Electrostatic", 0))     if res else None,
...
```

**Problem:** The guard `if res else None` returns `None` only when `res` is an empty dict `{}` (falsy). If the tool returns a non-empty result dict that is missing some energy keys — for example `{"status": "S"}` with no numeric fields — each `.get("KEY", 0)` silently substitutes 0.0. The row would then appear to have status "S" but all-zero energy decomposition terms, with no flag in the data to indicate the partial failure.

**Impact on current data:** All 83 rows in `mmgbsa_results.json` have non-zero, non-null energy components. The four-component sum (VdW + Elec + Polar + NonPolar) matches TOTAL to within floating-point rounding for a sample of four widely-spaced entries (ranks 1, 21, 41, 83), confirming the energy decomposition is internally consistent throughout.

---

## Verified Correct

| Claim | Source | Computed/observed value | Result |
|:---|:---|:---|:---:|
| 83 entries in mmgbsa_results.json | mmgbsa_results.json | 83 | CONFIRMED |
| All 83 status = "S" | mmgbsa_results.json | 83 × "S" | CONFIRMED |
| All 83 dG values non-null | mmgbsa_results.json | 0 nulls | CONFIRMED |
| No duplicate ligand names | mmgbsa_results.json | 83 unique | CONFIRMED |
| Sorted ascending by dG | mmgbsa_results.json | strictly ascending | CONFIRMED |
| Rank 1 = CTX-1020732, ΔG = −83.188 | mmgbsa_results.json row 0 | −83.187723 | CONFIRMED |
| Rank 83 = CTX-1020739, ΔG = −24.691 | mmgbsa_results.json row 82 | −24.691461 | CONFIRMED |
| CTX-1017233 rank 51, ΔG = −49.925 | mmgbsa_results.json index 50 | rank 51, −49.925490 | CONFIRMED |
| Mean ΔG = −55.199 / −55.20 | mmgbsa_results.json | −55.199281 | CONFIRMED |
| Median ΔG = −54.234 | mmgbsa_results.json rank 42 | −54.233920 | CONFIRMED |
| SD = 15.769 | mmgbsa_results.json | 15.768582 | CONFIRMED |
| CTX-1020732: 66 total atoms, 28 explicit H | CTX-1020732_best_pose_H.sdf molblock header | 66 atoms; H count = 28 | CONFIRMED |
| Batch_00 has 10 ligands | gbsa_batch_results_00.json | 10 entries | CONFIRMED |
| Batch_00 dG values match mmgbsa_results.json | cross-file comparison | 0 mismatches | CONFIRMED |
| Top-20 table: all ΔG values (rounded to 3 dp) | mmgbsa_results.json rows 0–19 | All match (see detail below) | CONFIRMED |
| Top-20 VdW, Elec, Polar, NonPolar values | mmgbsa_results.json rows 0–19 | All match to 3 dp | CONFIRMED |
| Energy components sum to TOTAL | sample: ranks 1, 21, 41, 83 | matches to <0.01 kcal/mol | CONFIRMED |
| gbsa tool input fields match declared schema | aidd_tool_schema("gbsa") | task, proteinFile, ligandFile, mode, method, proteinForceField, ligandForceField, ligandCharge, threads all declared | CONFIRMED |
| Output field `best_dG_kcal_per_mol` exists | aidd_tool_schema output_fields | listed | CONFIRMED |
| Receptor PDB chain A starts at residue 1 | receptor_gromacs_ready.pdb line 10 | ATOM 1, SER A 1 | CONFIRMED |
| No 0-based/1-based confusion in rank claims | mmgbsa_results.json | Rank 1 = index 0, Rank 51 = index 50, Rank 83 = index 82 — all consistent | CONFIRMED |
| No similar-identifier confusion in top-20 | mmgbsa_results.json | CTX-1019757/1019758, CTX-1020440/1020441, CTX-1020748/1020749 all in correct rank positions | CONFIRMED |

### Top-20 ΔG detail (rounded to 3 decimal places)

| Rank | Compound | Report ΔG | JSON raw | Match |
|:---:|:---|---:|---:|:---:|
| 1 | CTX-1020732 | −83.188 | −83.187723 | ✓ |
| 2 | CTX-1020811 | −80.272 | −80.271521 | ✓ |
| 3 | CTX-1020521 | −80.075 | −80.074737 | ✓ |
| 4 | CTX-1020903 | −79.956 | −79.955915 | ✓ |
| 5 | CTX-1020743 | −78.495 | −78.494879 | ✓ |
| 6 | CTX-1020748 | −77.689 | −77.689135 | ✓ |
| 7 | CTX-1020555 | −76.526 | −76.526050 | ✓ |
| 8 | CTX-1019757 | −75.475 | −75.475022 | ✓ |
| 9 | CTX-1020759 | −75.200 | −75.200469 | ✓ |
| 10 | CTX-1020800 | −74.601 | −74.600795 | ✓ |
| 11 | CTX-1020749 | −74.571 | −74.571207 | ✓ |
| 12 | CTX-1019758 | −74.240 | −74.240258 | ✓ |
| 13 | CTX-1020441 | −73.814 | −73.813836 | ✓ |
| 14 | CTX-1019613 | −73.477 | −73.476993 | ✓ |
| 15 | CTX-1019813 | −73.154 | −73.154069 | ✓ |
| 16 | CTX-1020842 | −72.509 | −72.508630 | ✓ |
| 17 | CTX-1020685 | −71.348 | −71.348456 | ✓ |
| 18 | CTX-1020440 | −70.464 | −70.463967 | ✓ |
| 19 | CTX-1020697 | −69.611 | −69.610576 | ✓ |
| 20 | CTX-1020562 | −68.508 | −68.507732 | ✓ |

---

## Items Checked and Not Found

| Check | Finding |
|:---|:---|
| 0-based vs 1-based rank confusion | None. Report uses 1-based ranks throughout; row 0 = rank 1 etc., all consistent. |
| Similar identifiers confused (e.g. CTX-1019757 vs CTX-1019758, CTX-1020440 vs CTX-1020441) | Not confused. Both pairs appear at correct rank positions with correct dG values. |
| `run_aidd_tool` positional argument order reversed | Not reversed. The installed schema declares `tool_id` first and `params` second, matching usage `run_aidd_tool("gbsa", {...})`. Results are non-null and internally consistent, confirming correct dispatch. |
| Bare `except:` clause | Not present. The script uses `except Exception as e:` (explicit type). |
| Rules derived from single data point | None identified. The re-ranking narrative references multiple compounds and the pharmacophore claim references the top-20 docked pose set (from prior phase). |
| `proteinFile` / `ligandFile` argument reversal | Not present. `proteinFile=REC` (a .pdb path) and `ligandFile=lig_path` (a .sdf path) match the schema's type annotations (`file_format: pdb` and `file_format: sdf` respectively). |

---

## Summary

No finding invalidates the 83 computed ΔG values or the compound rankings. All individual ΔG, VdW, electrostatic, polar-solvation, and non-polar solvation values in the top-20 table are confirmed correct to three decimal places. The four key statistics (mean, median, SD, n) are confirmed.

One numerical claim in the descriptive text is wrong (VdW mean stated as −57.6 kcal/mol; actual value from source data is −54.671 kcal/mol). Three code-quality issues in the execution script pose reproducibility or silent-failure risks for future reuse but did not affect the current dataset.

| Severity | Count | Items |
|:---|:---:|:---|
| CRITICAL | 0 | — |
| MAJOR | 4 | VdW mean in text; `or 9999` sort key; silent thread-timeout; 0.0 default for missing components |
| VERIFIED CORRECT | 20+ | All summary statistics, all top-20 values, schema conformance, identifier assignments |
