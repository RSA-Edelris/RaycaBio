# Audit: Phase 1 — task bymr9kz1y

**Document audited:** `reports/phase_01_task_bymr9kz1y.md`  
**Script audited:** `analyze_protac_series.py`  
**SLURM log:** `slurm-6534300.log`  
**Audited by:** Claude Sonnet 4.6 (automated audit, Rayca session)  
**Date:** 2026-09-14  

---

## Scope

The phase document describes running `python3 analyze_protac_series.py boltz_series` on 10 Boltz-2
ternary complex predictions and producing a cooperativity ranking table. The document itself exists
and contains specific claims. Each claim was checked against its primary source: the confidence
JSON files, the PDB files, the SLURM log, and the script source.

Checks performed:
- Chain index mapping and key types in confidence JSONs
- Whether `pair_chains_iptm["2"]["0"]` equals `ligand_iptm`
- Cα counts from actual PDB file
- Compound count (subdirectory count)
- HA values claimed vs. formula vs. actual SMILES-derived counts
- Ranking sort direction
- ETKDGv3 warning line number
- ARV-471 reference value (existence and content of JSON)
- Bare `except` clauses and default-zero returns that mask failures
- Positional argument reversal in distance functions
- Unsorted `os.listdir()` used for path selection

---

## Findings

---

### MAJOR — HA column formula is wrong for all 10 compounds

**Location:** `analyze_protac_series.py`, line 173  
**Claim:** The HA column in the printed table is computed as `LINKER_INFO[r['name']][2] + 35`.  
**Evidence:** rdkit was used to count actual heavy atoms from the SMILES in each YAML input file.
The formula underestimates by 9–12 atoms for every compound:

| Compound | Formula HA | Actual HA (rdkit) | Error |
| :---     | ---:       | ---:              | ---:  |
| ARV_001  | 44         | 53                | −9    |
| ARV_002  | 42         | 51                | −9    |
| ARV_003  | 45         | 55                | −10   |
| ARV_004  | 39         | 45                | −6    |
| ARV_005  | 42         | 48                | −6    |
| ARV_006  | 45         | 51                | −6    |
| ARV_007  | 48         | 54                | −6    |
| ARV_008  | 51         | 57                | −6    |
| ARV_009  | 54         | 60                | −6    |
| ARV_010  | 75         | 87                | −12   |

The constant `+35` is not the correct atom count for the shared scaffold (ERα warhead + CRBN binder).
The actual scaffold contribution ranges from ~41–47 atoms depending on compound.

**Impact:** The HA column in every printed table row is wrong. This does not affect iptm values or
the cooperativity ranking, but any downstream interpretation of molecular size from this table is
incorrect for all 10 compounds.

---

### MAJOR — Internal inconsistency in script: two different HA values for ARV-010

**Location:** `analyze_protac_series.py`, line 173 (table) vs. line 203 (limitation text)  
**Claim:** Line 203 prints `"4. Predictions for ARV-010 (87 HA, PEG-13 linker) ..."` (hardcoded).
Line 173 computes HA for the table as `LINKER_INFO['ARV_010'][2] + 35 = 40 + 35 = 75`.  
**Evidence:** rdkit from the SMILES in `ARV_010_ERalpha_CRBN_boltz_input.yaml` gives 87 heavy atoms.
The hardcoded "87 HA" on line 203 is correct. The table column formula gives 75, which is wrong.
The same script produces both values; they differ by 12 for the same compound.

**Impact:** Any reader comparing the ARV-010 HA value in the table (75) with the limitation note (87)
will find a contradiction. The table value is wrong; the limitation note is right.

---

### MAJOR — Broken cross-reference: referenced results document does not exist

**Location:** `reports/phase_01_task_bymr9kz1y.md`, Results section  
**Claim:** "Full results are documented in `phase_09_protac_series_predictions.md`."  
**Evidence:** `ls reports/ | grep protac_series_pred` returns nothing. No file matching that name
exists in the `reports/` directory. The closest file is `phase_09_task_aa17c52d2d059e38f.md`,
which describes a single-compound ARV-471 prediction, not the 10-compound series analysis.

**Impact:** The phase document's primary results pointer is a dead link. The numerical results
summarised in the phase document cannot be traced to a retrievable output document.

---

### MAJOR — Default-zero fallbacks make missing-data compounds indistinguishable from score-zero

**Location:** `analyze_protac_series.py`, lines 124–132 and 129–131  
**Detail:**
```python
"lig_crbn_iptm": float(pci.get("2", {}).get("1", 0)),
```
If `pair_chains_iptm` is absent from a confidence JSON, or if chain "2" or key "1" is absent,
the compound receives `lig_crbn_iptm = 0.0` and is silently ranked last. No warning is raised.
Similarly `conf.get("confidence_score", 0)` etc. return 0 for any absent top-level key.

**Evidence:** All 10 JSONs in this run contain the expected keys, so no silent failure occurred
here. This is a structural defect in the script that would be invisible in any run that completed
without broken JSON.

---

### MAJOR — `os.listdir()` without ordering picks the prediction subdirectory

**Location:** `analyze_protac_series.py`, lines 99–101  
```python
for d in os.listdir(inner):
    pred_dir = os.path.join(inner, d)
    break
```
`os.listdir()` returns entries in arbitrary filesystem order. If `inner` contained more than one
subdirectory (e.g., multiple input names from a re-run), the script would silently process
whichever directory the OS returned first.

**Evidence:** In all 10 actual prediction directories, `inner` (`predictions/`) contains exactly
one subdirectory each (confirmed: `ls boltz_series/ARV_001/.../predictions/ | wc -l` = 1).
No incorrect selection occurred in this run, but the code has no guard against it.

---

## Verified Correct

Each item below was checked against a primary source file. None were taken on faith from the
phase document alone.

**1. JSON chain keys are strings, not integers.**
Evidence: `confidence_ARV_001_ERalpha_CRBN_boltz_input_model_0.json` has
`"pair_chains_iptm": {"0": {...}, "1": {...}, "2": {...}}`. Keys are quoted strings.
The script uses `pci.get("2", {}).get("1", 0)` — correct string lookups throughout.

**2. Chain "0" = ERα, "1" = CRBN, "2" = ligand.**
Evidence: `ARV_001_ERalpha_CRBN_boltz_input.yaml` declares sequences in order:
protein id A (ERα, 258 aa), protein id B (CRBN, 469 aa), ligand id C (SMILES).
Boltz-2 assigns chain indices 0-based in YAML sequence order, so index 0 = A = ERα,
index 1 = B = CRBN, index 2 = C = ligand. Confirmed consistent with PDB chain labels.

**3. `pair_chains_iptm["2"]["0"]` equals `ligand_iptm` exactly.**
Evidence: ARV_001 JSON: `pair_chains_iptm["2"]["0"]` = 0.9195163249969482;
`ligand_iptm` = 0.9195163249969482. Bit-for-bit identical (Python `==` True).
Same check for ARV-471 JSON: both = 0.9064819812774658. Claim holds.

**4. ERα Cα count = 258.**
Evidence: `grep "^ATOM" ARV_001..._model_0.pdb | awk '$3=="CA"{print $5}' | sort | uniq -c`
returns `258 A`. Matches the 258-residue ERα sequence in the YAML.

**5. CRBN Cα count = 469.**
Evidence: Same PDB grep returns `469 B`. Matches the 469-residue CRBN sequence in the YAML.

**6. 10 of 10 compounds present.**
Evidence: `ls boltz_series/` lists exactly 10 subdirectories: ARV_001 through ARV_010.

**7. Ranking sort direction is descending (higher = better).**
Evidence: `analyze_protac_series.py` line 163:
`ranked = sorted(results, key=lambda x: x["lig_crbn_iptm"], reverse=True)`
`reverse=True` means descending. Claim correct.

**8. ETKDGv3 warning is on line 244 of slurm-6534300.log.**
Evidence: `grep -n "ETKDGv3" slurm-6534300.log` returns line 244. Claim correct.

**9. ARV-001 rank 1, lig→CRBN iptm = 0.5086.**
Evidence: `confidence_ARV_001..._model_0.json`:
`pair_chains_iptm["2"]["1"]` = 0.5085741877555847 → rounds to 0.5086. Claim correct.

**10. ARV-007 rank 10, lig→CRBN iptm = 0.1932.**
Evidence: `confidence_ARV_007..._model_0.json`:
`pair_chains_iptm["2"]["1"]` = 0.1932487040758133 → rounds to 0.1932. Claim correct.

**11. ARV-471 reference JSON exists and contains lig→CRBN iptm = 0.2306.**
Evidence: File found at
`boltz_out/boltz_results_ARV471_ERalpha_CRBN_boltz_input/predictions/ARV471_ERalpha_CRBN_boltz_input/confidence_ARV471_ERalpha_CRBN_boltz_input_model_0.json`.
`pair_chains_iptm["2"]["1"]` = 0.23056241869926453 → rounds to 0.2306.
All other ARV471_REF fields checked: conf=0.4778 ✓, ptm=0.4550 ✓, iptm=0.3133 ✓,
lig_iptm=0.9065 ✓, protein_iptm=0.1604 ✓. All hardcoded values match the JSON.

**12. ARV-471 reference "54 HA" is correct.**
Evidence: rdkit from SMILES in `ARV471_ERalpha_CRBN_boltz_input.yaml` = 54 heavy atoms.

**13. No bare `except` clause in the script.**
Evidence: `grep -n "except" analyze_protac_series.py` returns no lines. No `try/except`
block of any kind exists in the script.

**14. No positional argument reversal in distance functions.**
Evidence: `dist(a, b)` (line 37) is `sqrt(sum((x-y)^2 ...))`, symmetric in a and b.
All calls (`min_lig_era`, `min_lig_crbn`, etc.) use `dist(p, q)` where p ∈ lig_xyz
and q ∈ target_chain. Since dist is symmetric, order is irrelevant. No reversal possible.

**15. `pair_chains_iptm["2"]["1"]` is the correct cooperativity proxy field.**
Evidence: Chain 2 = ligand (YAML C), chain 1 = CRBN (YAML B). `pair_chains_iptm["2"]["1"]`
is the cross-chain iptm measuring how well the model resolves the ligand-CRBN interface.
This is the intended lig→CRBN cooperativity proxy. Assignment is correct.

---

## Summary

| # | Finding | Severity | Affects ranking? |
|---|---------|----------|-----------------|
| 1 | HA table column wrong for all 10 compounds (formula underestimates by 6–12) | MAJOR | No |
| 2 | ARV-010 has HA=75 in table and HA=87 in limitation text — internal contradiction (87 is correct) | MAJOR | No |
| 3 | Cross-referenced results document `phase_09_protac_series_predictions.md` does not exist | MAJOR | No |
| 4 | Default-zero returns for absent JSON keys: silent rank-last rather than error | MAJOR | No (not triggered) |
| 5 | Unsorted `os.listdir()` selects prediction subdirectory: wrong dir if >1 present | MAJOR | No (not triggered) |

The cooperativity ranking itself (lig→CRBN iptm values, sort order, reference comparison) is
verified correct. All five findings are MAJOR rather than CRITICAL because none of them altered
the iptm values used for ranking in this run. They represent annotation errors and script
fragility that would need remediation before the script is re-used on new data.
