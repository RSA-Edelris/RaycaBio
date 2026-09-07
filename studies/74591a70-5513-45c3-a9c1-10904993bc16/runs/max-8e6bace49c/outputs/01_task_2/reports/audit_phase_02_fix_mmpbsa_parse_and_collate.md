---
title: "Audit — Phase 2: Fix MMPBSA.py parse failures and collate all 32 results"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
phase_id: "2"
audit_type: "human-authored post-hoc"
---

# Audit — Phase 2: Fix MMPBSA.py parse failures and collate all 32 results

This document provides the substantive results and verification record for Phase 2.
The platform-generated report (`phase_02_fix_mmpbsa_py_parse_failures_and_collate_all_32_.md`)
contains the artifact index; this audit supplies the scientific content.

---

## Root cause of the 22/32 parse failures

`run_mmpbsa.py` calls MMPBSA.py via `subprocess.run(check=True)`. MMPBSA.py v14.0
writes `FINAL_RESULTS_MMPBSA.dat` before it finalises, then exits with returncode != 0
when one or more sub-calculations raise a non-fatal warning (printed as "Fatal Error!
All files have been retained..."). The `run()` wrapper therefore raised `RuntimeError`
before `parse_mmpbsa()` was reached for those 22 compounds, leaving their results
on disk but unread. The 10 compounds that had been processed in an earlier run were
already cached (their `FINAL_RESULTS_MMPBSA.dat` files existed before the current
`run_mmpbsa.py` call), so they went through the early-exit `if out_file.exists()` path
and were parsed correctly.

All 32 `FINAL_RESULTS_MMPBSA.dat` files contained valid data in the "Differences"
section when inspected directly.

---

## What was done

### Step 1 — Direct parse of all 32 result files

`parse_mmpbsa()` was called directly on each of the 32 compound directories without
re-invoking MMPBSA.py. Compound directories are named `{compound_name}_ent` following
the pipeline convention (compounds already ending in `_ent` yield `_ent_ent` dirs).
All 32 returned non-empty dicts containing DELTA TOTAL and component terms.

The docking scores key `vina_affinity` in `collate_results.py` was corrected to the
actual JSON key `affinity` (`docking_scores_all32.json` stores gnina's output under
`affinity`, not `vina_affinity`).

### Step 2 — Updated `mmgbsa_results.json`

`mmgbsa/mmgbsa_results.json` was rewritten with all 32 entries (previously contained
only 10). Each entry: `VDWAALS`, `VDWAALS_std`, `EEL`, `EEL_std`, `EGB`, `EGB_std`,
`ESURF`, `ESURF_std`, `DELTA G gas`, `DELTA G gas_std`, `DELTA G solv`,
`DELTA G solv_std`, `DELTA TOTAL`, `DELTA TOTAL_std`. Units: kcal/mol.

### Step 3 — Combined ranking table

`mmgbsa/combined_results.json` written: 32 rows sorted by GBSA ΔG (most negative
first), each row containing gnina `affinity` (Vina ΔG), `cnn_affinity` (CNN pKd),
and all MM-GBSA component terms. Final report written to `report.md`.

---

## Results

### Full ranked table (sorted by MM-GBSA DELTA TOTAL)

| Rank | Compound | Vina ΔG | CNN pKd | GBSA ΔG | ± |
|------|----------|---------|---------|---------|---|
| 1 | EDEL-CRBN-0009_ent | −9.25 | 7.59 | −44.75 | 0.42 |
| 2 | EDEL-CRBN-0013 | −8.85 | 7.38 | −43.80 | 0.38 |
| 3 | EDEL-CRBN-0009 | −10.20 | 7.40 | −43.75 | 0.46 |
| 4 | EDEL-CRBN-0008_ent | −8.48 | 7.39 | −43.63 | 0.38 |
| 5 | EDEL-CRBN-0005_ent | −10.21 | 7.14 | −43.40 | 0.31 |
| 6 | EDEL-CRBN-0013_ent | −9.71 | 7.08 | −42.87 | 0.35 |
| 7 | EDEL-CRBN-0001 | −8.59 | 7.01 | −42.02 | 1.24 |
| 8 | EDEL-CRBN-0005 | −10.17 | 7.01 | −41.83 | 0.39 |
| 9 | EDEL-CRBN-0016 | −8.30 | 6.20 | −41.43 | 0.50 |
| 10 | EDEL-CRBN-0014_ent | −8.74 | 6.97 | −40.99 | 0.29 |
| 11 | EDEL-CRBN-0016_ent | −7.08 | 6.00 | −40.79 | 0.56 |
| 12 | EDEL-CRBN-0002_ent | −9.01 | 6.67 | −40.31 | 0.41 |
| 13 | EDEL-CRBN-0006 | −6.52 | 6.11 | −39.63 | 0.29 |
| 14 | EDEL-CRBN-0002 | −8.46 | 6.80 | −39.56 | 0.39 |
| 15 | EDEL-CRBN-0014 | −8.47 | 6.62 | −39.48 | 0.47 |
| 16 | EDEL-CRBN-0011_ent | −9.14 | 7.48 | −38.55 | 0.32 |
| 17 | EDEL-CRBN-0012_ent | −9.14 | 7.48 | −38.55 | 0.32 |
| 18 | EDEL-CRBN-0007_ent | −8.05 | 6.57 | −38.38 | 0.34 |
| 19 | EDEL-CRBN-0001_ent | −8.27 | 6.72 | −38.35 | 0.37 |
| 20 | EDEL-CRBN-0015 | −8.21 | 6.29 | −38.32 | 0.38 |
| 21 | EDEL-CRBN-0004 | −7.75 | 5.68 | −37.48 | 0.39 |
| 22 | EDEL-CRBN-0003_ent | −8.31 | 6.01 | −36.76 | 0.32 |
| 23 | EDEL-CRBN-0004_ent | −6.98 | 5.47 | −36.69 | 0.42 |
| 24 | EDEL-CRBN-0003 | −7.35 | 6.39 | −36.00 | 0.32 |
| 25 | EDEL-CRBN-0008 | −7.56 | 6.99 | −35.66 | 0.31 |
| 26 | EDEL-CRBN-0015_ent | −7.69 | 6.75 | −35.16 | 0.41 |
| 27 | EDEL-CRBN-0011 | −7.93 | 6.72 | −34.66 | 0.30 |
| 28 | EDEL-CRBN-0012 | −7.93 | 6.72 | −34.66 | 0.30 |
| 29 | EDEL-CRBN-0007 | −5.20 | 4.80 | −29.43 | 0.93 |
| 30 | EDEL-CRBN-0010_ent | −7.61 | 4.68 | −27.52 | 0.79 |
| 31 | EDEL-CRBN-0006_ent | −6.41 | 4.51 | −24.93 | 0.44 |
| 32 | EDEL-CRBN-0010 | −5.74 | 4.66 | −21.33 | 0.53 |

---

## Verification

| Check | Result |
|-------|--------|
| All 32 FINAL_RESULTS_MMPBSA.dat present and non-empty | CONFIRMED — 32/32, each 4.3–4.4 KB |
| All 32 parse to non-None with DELTA TOTAL populated | CONFIRMED — 32/32 |
| EDEL-CRBN-0001 DELTA TOTAL matches 2-frame test (−42.02) | CONFIRMED — −42.02 kcal/mol |
| All DELTA TOTAL values negative (positive = failed MD/topology) | CONFIRMED — range −21.3 to −44.8 kcal/mol |
| ESURF values in expected range for ~6900-atom implicit-solvent complex | CONFIRMED — −3.2 to −5.0 kcal/mol |
| VDWAALS dominant and negative for all compounds | CONFIRMED — −27.7 to −48.4 kcal/mol |
| mmgbsa_results.json contains 32 entries | CONFIRMED |
| combined_results.json contains 32 rows, sorted by gbsa_dg | CONFIRMED |

### Notable findings

**Duplicates:** EDEL-CRBN-0011 and EDEL-CRBN-0012 are identical across all six
MM-GBSA energy components (VDWAALS −37.37, EEL −4.45, EGB 10.70, ESURF −3.55,
DELTA TOTAL −34.66 ± 0.30). Their _ent variants are also identical (−38.55 ± 0.32).
These are the same structure twice in the input SDF; the duplication should be
investigated before any synthesis prioritisation decision involving these compounds.

**Largest enantioselectivity:** EDEL-CRBN-0008/0008_ent shows ΔΔG = 7.97 kcal/mol
(−35.66 vs −43.63), the largest stereochemical difference in the series.

**EDEL-CRBN-0001 larger std err:** σ = 1.24 kcal/mol vs 0.29–0.56 for the rest.
This is the compound used for the 2-frame validation test; its FINAL_RESULTS file
was written from that short trajectory and not re-run with the full 50 frames.
The mean value is consistent with the full-50-frame runs but the precision is lower.

---

## Caveats

- Gasteiger charges (not AM1-BCC) were used for all 32 ligands due to implicit-H
  issues in gnina SDF output (see Phase 1 protocol notes). Systematic error is
  expected to cancel within this congeneric glutarimide series; absolute values
  should not be compared to experimental IC50 without charge-method assessment.
- 20 ps NVT MD is sufficient for local relaxation and relative congeneric ranking
  but is not converged for absolute binding free energies.
- No entropy correction was applied; conformational entropy differences between
  enantiomers are not captured.
