---
title: "Phase 1: Analyse constrained prediction results and write report"
study_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-e2e820ee4d"
phase_index: 1
phase_id: "2"
phase_goal: "Analyse constrained prediction results and write report"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Analyse constrained prediction results and write report

## Summary

This phase set out to analyse constrained prediction results and write report. It completed 1 method step, 11 output files.

## Objective

Analyse constrained prediction results and write report

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

**Table R.** Key resources used in this phase. Versions are as reported by the running environment; identifiers follow the FORCE11 software citation principles.

| Resource | Type | Version | Identifier | Source |
| :--- | :--- | :--- | :--- | :--- |
| boltz | software | not recorded | doi:10.1101/2025.06.14.659707 (unverified, check before use) | not recorded |

### Procedure

#### 1. Structure prediction of PROTAC-mediated protein–protein complex using diffusion-based generative modeling

Boltz-2 structure prediction was performed to model the bridging geometry of ARV-471 PROTAC bound to estrogen receptor alpha (ERalpha, chain A, 258 amino acids) and cereblon (CRBN, chain B, 469 amino acids). The prediction was executed with 3 diffusion samples in PDB output format, seed 42, and no multiple sequence alignment, generating 3 candidate poses ranked by confidence score.

**Rationale.** Boltz-2 is a diffusion-based deep learning model designed for complex structure prediction, including protein–protein interfaces and small-molecule bridging. This approach enables de novo prediction of PROTAC-induced ternary complex geometry without requiring experimental structures or homology templates.

| Field | Value |
| :--- | :--- |
| Inputs | ARV471_ERalpha_CRBN_boltz_input.yaml |
| Libraries | boltz |
| Status | running |

Parameters:

```yaml
diffusion_samples: 3
num_workers: 0
output_format: pdb
recycling_steps: 1
seed: 42
```

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| 046_range.csv | CSV | 4.5 KB | 01_analyse_constrained_prediction_results_and_write/tables | cb42f06687a0... |
| 045_range.py | PY | 1.2 KB | 01_analyse_constrained_prediction_results_and_write/source | c975864243b9... |
| 046_ranking_model_0_lig_crbn_boltz_2_s_top_ranked.py | PY | 1.6 KB | 01_analyse_constrained_prediction_results_and_write/source | f2e95f192078... |
| 047_check_actual_keys_one_json_see_correct_field_names.py | PY | 332 B | 01_analyse_constrained_prediction_results_and_write/source | e6a37ada741b... |
| 048_range.py | PY | 2.1 KB | 01_analyse_constrained_prediction_results_and_write/source | 0a2681f50615... |
| 049_parse_pdb_atoms.py | PY | 2.3 KB | 01_analyse_constrained_prediction_results_and_write/source | dd9f6551799e... |
| 050_spot_check_read_first_80_last_100_atom_lines_arv_001.py | PY | 1.4 KB | 01_analyse_constrained_prediction_results_and_write/source | 61349575e681... |
| 051_parse_pdb_atoms.py | PY | 1.8 KB | 01_analyse_constrained_prediction_results_and_write/source | f69899ee3c41... |
| 052_parse_pdb_atoms.py | PY | 2.7 KB | 01_analyse_constrained_prediction_results_and_write/source | 6919d2fdc9d3... |
| 053_pull_per_chain_self_iptm_cross_chain_values_all_m0.py | PY | 1.4 KB | 01_analyse_constrained_prediction_results_and_write/source | d291bd3419ab... |
| phase_02_constrained_protac_predictions_no_op_tensorboard.md | MD | 4.8 KB | 01_analyse_constrained_prediction_results_and_write/reports | 0c435ffdd89f... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 11 file(s) were produced and registered, 11 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No citation is on record for boltz, so the versions used cannot be traced to a publication.
- Versions were not recorded for boltz. A methods section without a version is not reproducible.

## References

**Unverified candidate references.** These were matched automatically by name and have NOT been confirmed as the correct reference for the tool this study used. Two tools in different fields can share a name, so each must be checked before use.

- boltz: Saro Passaro, Gabriele Corso, Jeremy Wohlwend et al.. Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction. bioRxiv (Cold Spring Harbor Laboratory). 2025. doi:10.1101/2025.06.14.659707
