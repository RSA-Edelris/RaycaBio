---
title: "Phase 4: Probe 5 — install chembl_structure_pipeline, verify boltz predict --help"
study_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-331fa8863a"
phase_index: 4
phase_id: "4"
phase_goal: "Probe 5 — install chembl_structure_pipeline, verify boltz predict --help"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 4: Probe 5 — install chembl_structure_pipeline, verify boltz predict --help

## Summary

This phase set out to probe 5 — install chembl_structure_pipeline, verify boltz predict --help. It completed 1 method step, 4 output files.

## Objective

Probe 5 — install chembl_structure_pipeline, verify boltz predict --help

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

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 4 file(s) were produced and registered, 4 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No citation is on record for boltz, so the versions used cannot be traced to a publication.
- Versions were not recorded for boltz. A methods section without a version is not reproducible.

## References

**Unverified candidate references.** These were matched automatically by name and have NOT been confirmed as the correct reference for the tool this study used. Two tools in different fields can share a name, so each must be checked before use.

- boltz: Saro Passaro, Gabriele Corso, Jeremy Wohlwend et al.. Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction. bioRxiv (Cold Spring Harbor Laboratory). 2025. doi:10.1101/2025.06.14.659707
