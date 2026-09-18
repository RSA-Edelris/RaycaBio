---
title: "Phase 4: task a804f8dfd4119b554"
study_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-dc9d0c6539"
phase_index: 4
phase_id: "a804f8dfd4119b554"
phase_goal: "task a804f8dfd4119b554"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 4: task a804f8dfd4119b554

## Summary

This phase set out to task a804f8dfd4119b554. It completed 1 method step, 10 output files.

## Objective

task a804f8dfd4119b554

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
| slurm-6534300.log | LOG | 25.3 KB | work | 54adb59b8a4d... |
| phase_01_task_bymr9kz1y.md | MD | 3.4 KB | reports | 57eaf0447b34... |
| phase_02_collect_confidence_scores_and_rank_by_cooperativ.md | MD | 3.7 KB | 03_task_4/reports | f7d3d7222c03... |
| phase_09_protac_series_predictions.md | MD | 8.1 KB | 03_task_4/reports | a761906db6e1... |
| phase_03_write_phase_report_protac_series_ternary_complex.md | MD | 3.9 KB | reports | 89f171f1917f... |
| phase_09_protac_series_predictions.md | MD | 11.3 KB | reports | c4464d700d24... |
| phase_01_task_bymr9kz1y.md | MD | 4.0 KB | reports | 25776914a705... |
| phase_02_collect_confidence_scores_and_rank_by_cooperativ.md | MD | 4.7 KB | reports | f5d6beaa897b... |
| phase_03_write_phase_report_protac_series_ternary_complex.md | MD | 4.3 KB | reports | ab577523e905... |
| audit_phase_01_task_bymr9kz1y.md | MD | 10.3 KB | reports | 1fa5761d70b9... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 10 file(s) were produced and registered, 10 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No citation is on record for boltz, so the versions used cannot be traced to a publication.
- Versions were not recorded for boltz. A methods section without a version is not reproducible.

## References

**Unverified candidate references.** These were matched automatically by name and have NOT been confirmed as the correct reference for the tool this study used. Two tools in different fields can share a name, so each must be checked before use.

- boltz: Saro Passaro, Gabriele Corso, Jeremy Wohlwend et al.. Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction. bioRxiv (Cold Spring Harbor Laboratory). 2025. doi:10.1101/2025.06.14.659707
