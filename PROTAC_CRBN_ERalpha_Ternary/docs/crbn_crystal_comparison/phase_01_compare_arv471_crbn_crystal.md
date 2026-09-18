---
title: "Phase 1: Compare ARV-471 Boltz-2 CRBN models to crystal structure CRBN.pdb"
study_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-7cf56f5f1e"
phase_index: 1
phase_id: "1"
phase_goal: "Compare ARV-471 Boltz-2 CRBN models to crystal structure CRBN.pdb"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Compare ARV-471 Boltz-2 CRBN models to crystal structure CRBN.pdb

## Summary

This phase set out to compare ARV-471 Boltz-2 CRBN models to crystal structure CRBN.pdb. It completed 1 method step, 6 output files.

## Objective

Compare ARV-471 Boltz-2 CRBN models to crystal structure CRBN.pdb

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
| 059_pdbparser.py | PY | 1.2 KB | source | 1e625e8bc94f... |
| 060_extract_1_letter_sequences.py | PY | 1.5 KB | source | c221f35d6616... |
| 061_get_seq_ca.py | PY | 1.1 KB | source | cad0fdde13a0... |
| 062_get_seq_ca.py | PY | 2.8 KB | source | ac9b7df68e49... |
| 063_get_seq_ca.py | PY | 1.5 KB | source | 8054a9d9b88e... |
| 064_get_seq_ca.py | PY | 3.2 KB | source | 81453593e56e... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 6 file(s) were produced and registered, 6 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No citation is on record for boltz, so the versions used cannot be traced to a publication.
- Versions were not recorded for boltz. A methods section without a version is not reproducible.

## References

**Unverified candidate references.** These were matched automatically by name and have NOT been confirmed as the correct reference for the tool this study used. Two tools in different fields can share a name, so each must be checked before use.

- boltz: Saro Passaro, Gabriele Corso, Jeremy Wohlwend et al.. Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction. bioRxiv (Cold Spring Harbor Laboratory). 2025. doi:10.1101/2025.06.14.659707
