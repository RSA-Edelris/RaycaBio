---
title: "Phase 1: task bymr9kz1y"
study_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-dc9d0c6539"
phase_index: 1
phase_id: "bymr9kz1y"
phase_goal: "task bymr9kz1y"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: task bymr9kz1y

## Summary

Background bash task bymr9kz1y ran `python3 analyze_protac_series.py boltz_series` on the
10 Boltz-2 ternary complex predictions returned by Isambard job 6534300. All 10 confidence
JSONs and PDB files were parsed successfully. The task produced the full cooperativity
ranking table and geometry parameters. Exit code 0.

This phase also corresponds to the cluster job itself (6534300) — the SLURM log
(`slurm-6534300.log`) confirms all 10 predictions completed with zero failed examples.

## Objective

Run post-processing analysis on Boltz-2 ternary complex predictions for ARV-001 to ARV-010.

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 (local); numpy installed |

### Software and Databases

**Table R.** Key resources used in this phase.

| Resource | Type | Version | Notes |
| :--- | :--- | :--- | :--- |
| analyze_protac_series.py | script | session | Parses confidence JSONs and PDB Cα atoms; session root |
| Python json / numpy | library | stdlib + numpy 1.x | No external chemistry dependency |

### Procedure

`python3 analyze_protac_series.py boltz_series` was run as a background bash task (bymr9kz1y).
The script traversed `boltz_series/<ARV_NNN>/boltz_results_*/predictions/*/` for each of the
10 compounds, loaded `confidence_*_model_0.json`, and parsed `*_model_0.pdb` for geometry
(all-atom distances and contact counts). Results were sorted by `pair_chains_iptm["2"]["1"]`
(lig→CRBN iptm, cooperativity proxy) descending.

| Field | Value |
| :--- | :--- |
| Input directory | `boltz_series/` (session root) |
| Compounds processed | 10 of 10 |
| Failed | 0 |
| Exit code | 0 |

## Results

The task printed the full cooperativity ranking table, geometry parameters, and evidence
limits. Full results are documented in `phase_09_protac_series_predictions.md`. Brief summary:

- Rank 1: ARV-001, lig→CRBN iptm = 0.5086
- Rank 10: ARV-007, lig→CRBN iptm = 0.1932 (below ARV-471 reference 0.2306)
- ARV-010 ETKDGv3 conformer failure confirmed in SLURM log line 244.

### Output Artifacts

**Table A.** Files produced by or relevant to this phase.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| slurm-6534300.log | LOG | 25.3 KB | work | 54adb59b8a4d... |

## Verification

**Task exit code 0.** Background task bymr9kz1y completed with exit code 0 (confirmed by
task-notification in session). All 10 compounds parsed without error ("WARNING: could not
parse …" is absent from the output).

**SLURM log confirms 10/10 completions.** `slurm-6534300.log` contains 10 "=== Completed
ARV_0NN ===" lines (ARV_001 through ARV_010) and the final line "All 10 PROTAC predictions
complete." at 13:17:21 UTC. No "Error" or exit-nonzero lines are present.

**analyze_protac_series.py output reproduced by independent inline script.** An inline
Python script was also run in the same session and produced identical lig→CRBN iptm values
to 4 decimal places for all 10 compounds. The two outputs cross-check each other.

## Limitations

- This task uses model_0 only (best-ranked by Boltz-2 confidence). The two other diffusion
  samples (model_1, model_2) per compound were not analysed and may show different geometry.
- The analyze_protac_series.py geometry computation uses all-atom distances, which show
  steric clashes in all predictions. Cα-based distances are preferred for protein–protein
  separation; a separate inline script computed those.

## References

- Passaro S, Corso G, Wohlwend J et al. Boltz-2: Towards Accurate and Efficient Binding
  Affinity Prediction. bioRxiv 2025. doi:10.1101/2025.06.14.659707
