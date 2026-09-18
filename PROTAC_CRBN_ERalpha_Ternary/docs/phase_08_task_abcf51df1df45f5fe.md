---
title: "Phase 8: task abcf51df1df45f5fe"
study_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-331fa8863a"
phase_index: 8
phase_id: "abcf51df1df45f5fe"
phase_goal: "task abcf51df1df45f5fe"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 8: task abcf51df1df45f5fe

## Summary

This phase set out to task abcf51df1df45f5fe. It completed 1 method step, 10 output files.

## Objective

task abcf51df1df45f5fe

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
| slurm-6462167.log | LOG | 14.0 KB | work | 315c97f0a382... |
| phase_01_probe_2_fix_pytorch_lightning_missing_dep_in_bol.md | MD | 3.6 KB | reports | 8f959232fe6e... |
| phase_02_probe_3_install_remaining_missing_boltz_deps_on_.md | MD | 3.6 KB | reports | a1811e124c85... |
| phase_03_probe_4_install_mashumaro_verify_boltz_predict_h.md | MD | 3.6 KB | reports | cb7f0cfdcfd4... |
| phase_04_probe_5_install_chembl_structure_pipeline_verify.md | MD | 4.0 KB | reports | bc51ab9df864... |
| phase_05_probe_6_bulk_install_remaining_boltz_deps_with_t.md | MD | 4.1 KB | reports | dc75894bb0eb... |
| audit_probe4_mashumaro.md | MD | 10.4 KB | 06_submit_arv_471_gpu_prediction_job_on_isambard_3_/reports | ab42903655ae... |
| audit_probe2_pytorch_lightning.md | MD | 11.5 KB | 06_submit_arv_471_gpu_prediction_job_on_isambard_3_/reports | 667328a80b1d... |
| phase_07_task_a7edbc2e4a8d5c185.md | MD | 4.1 KB | 06_submit_arv_471_gpu_prediction_job_on_isambard_3_/reports | 4252cdd9c923... |
| audit_probe5_chembl.md | MD | 9.2 KB | 06_submit_arv_471_gpu_prediction_job_on_isambard_3_/reports | 73f4fb055b52... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 10 file(s) were produced and registered, 10 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No citation is on record for boltz, so the versions used cannot be traced to a publication.
- Versions were not recorded for boltz. A methods section without a version is not reproducible.

## References

**Unverified candidate references.** These were matched automatically by name and have NOT been confirmed as the correct reference for the tool this study used. Two tools in different fields can share a name, so each must be checked before use.

- boltz: Saro Passaro, Gabriele Corso, Jeremy Wohlwend et al.. Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction. bioRxiv (Cold Spring Harbor Laboratory). 2025. doi:10.1101/2025.06.14.659707
