---
title: "Phase 3: Write phase report: PROTAC series ternary complex predictions"
study_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-dc9d0c6539"
phase_index: 3
phase_id: "4"
phase_goal: "Write phase report: PROTAC series ternary complex predictions"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 3: Write phase report: PROTAC series ternary complex predictions

## Summary

Synthesised all computations from phases 1–2 of this run into `phase_09_protac_series_predictions.md` — the primary deliverable for the PROTAC series ternary complex prediction task. The report contains: job provenance, cooperativity ranking table (10 compounds vs ARV-471 reference), surface lysine analysis (LYS171/LYS196 distances to CRBN Cα for each model_0), five evidence-limit statements, a Verification section, and an Audit note explaining the output recovery from the Lustre working directory.

## Objective

Write phase report: PROTAC series ternary complex predictions

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |

### Procedure

All numbers in the report were computed directly from:
- `boltz_series/<ARV_NNN>/boltz_results_*/predictions/*/confidence_*_model_0.json` (10 files)
- `boltz_series/<ARV_NNN>/boltz_results_*/predictions/*/*_model_0.pdb` (10 files)
- `boltz_out/.../confidence_ARV471_ERalpha_CRBN_boltz_input_model_0.json` (reference)

No numbers were inherited from prior session summaries or estimates. The Verification
section of the report was written after the numbers were confirmed by two independent
extraction scripts. The report was written as `phase_09_protac_series_predictions.md` in
the session root directory.

## Results

`phase_09_protac_series_predictions.md` (session root) — primary deliverable. Contains:
- Table 1: cooperativity ranking for 10 compounds with conf, lig_iptm, lig→CRBN iptm, prot_iptm, ERα–CRBN centroid distance, ligand span, Δ vs ARV-471
- Table 2: LYS171 and LYS196 NZ→nearest CRBN Cα distance for all 10 compounds
- Surface lysine conclusion: ARV-001 only (LYS171 at 16.8 Å, lig→CRBN iptm 0.509)
- Five explicit evidence limits
- Verification and Audit sections

### Output Artifacts

**Table A.** Files produced by this phase.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| slurm-6534300.log | LOG | 25.3 KB | work | 54adb59b8a4d... |
| phase_01_task_bymr9kz1y.md | MD | 3.4 KB | reports | 57eaf0447b34... |
| phase_02_collect_confidence_scores_and_rank_by_cooperativ.md | MD | 3.7 KB | 03_task_4/reports | f7d3d7222c03... |
| phase_09_protac_series_predictions.md | MD | 8.1 KB | 03_task_4/reports | a761906db6e1... |

## Verification

**Report numbers cross-checked against raw output.** The lig→CRBN iptm values in Table 1
of `phase_09_protac_series_predictions.md` were compared against the inline script output
printed directly in the session (two independent extractions). All 10 values match exactly.

**Surface lysine distances were computed from PDB files, not estimated.** The LYS171/196
NZ atom positions were extracted by name from the ATOM records of each model_0 PDB. The
nearest CRBN Cα distance was the minimum over the full 469-residue CRBN chain (confirmed
by the script output showing per-compound results for all five target lysines including
buried ones as controls).

**Report file is present.** `phase_09_protac_series_predictions.md` exists in the session
root at the time this audit was written (confirmed by file listing).

**Verification section included in report.** The report contains a Verification section
with seven distinct check points: JSON parse success, chain index assignment, NZ atom
presence, Cα centroid distances, ARV-471 reference value, ETKDGv3 warning, and
independent reproducibility check.

## Limitations

- The report covers model_0 only. Models 1 and 2 per compound were not synthesised.
- All evidence limits in the report apply to the report itself; none are hedges against
  the reporting quality.

## References

- Passaro S, Corso G, Wohlwend J et al. Boltz-2: Towards Accurate and Efficient Binding
  Affinity Prediction. bioRxiv 2025. doi:10.1101/2025.06.14.659707
