---
title: "Phase 1: task btgnat4b7"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-c3fda373b8"
phase_index: 1
phase_id: "btgnat4b7"
phase_goal: "task btgnat4b7"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: task btgnat4b7

## Summary

This phase set out to task btgnat4b7. It completed 1 method step, 16 output files.

## Objective

task btgnat4b7

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
| GNINA | software | not recorded | doi:10.1186/s13321-021-00522-2 | https://github.com/gnina/gnina |
| Rayca Modulon | platform | not recorded | this platform | not recorded |

### Procedure

#### 1. Molecular docking of ligands to CDK2

A series of 80 ligands with identifiers CTX-1020903 through CTX-1020767 were docked against a CDK2 receptor structure using GNINA with CNN-based scoring. Each ligand was docked into a defined binding box (center: 30.57, 5.37, -25.8; dimensions: 35 × 30 × 31 Ų) with 5 binding modes generated per ligand using an exhaustiveness setting of 8 and random seed 42.

**Rationale.** Structure-based virtual screening using deep learning-enhanced docking to identify potential CDK2 inhibitors from a compound library and rank them by binding affinity and CNN scores.

| Field | Value |
| :--- | :--- |
| Inputs | receptor_raw.pdb |
| Tools | gnina |
| Libraries | modulon |
| Status | running |

Parameters:

```yaml
boxX: 30.57
boxY: 5.37
boxZ: -25.8
cnnScoring: rescore
depth: 31
exhaustiveness: 8
gpu: True
height: 30
numModes: 5
seed: 42
width: 35
```

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| nc_docking_results.json | JSON | 408 B | work | 6c6dfbfb952d... |
| gnina_docked.sdf.gz | GZ | 5.9 KB | structures | 9db05855dd42... |
| 085_subprocess_run.py | PY | 422 B | source | c25cdb5c4d06... |
| dock_nc_compounds.py | PY | 3.9 KB | source | ee7db87d42ac... |
| dock_nc_run.log | LOG | 0 B | work | e3b0c44298fc... |
| mmgbsa_nc_compounds.py | PY | 5.1 KB | source | 552c42048e65... |
| build_complex_pdb.py | PY | 4.0 KB | source | 31b3c3ab3f0f... |
| dock_nc_run.log | LOG | 251 B | work | b46cc0c02847... |
| nc_docking_results.json | JSON | 327 B | work | 918f0f307726... |
| NC-001_best_pose.sdf | SDF | 3.7 KB | structures | b19e76644088... |
| dock_nc_run.log | LOG | 502 B | work | 0372d080c767... |
| nc_docking_results.json | JSON | 652 B | work | bbe6df06a74e... |
| NC-002_best_pose.sdf | SDF | 3.7 KB | structures | 9ecfc67f96b4... |
| gnina_docked.sdf.gz | GZ | 5.9 KB | structures | 416f6f8254d8... |
| dock_nc_run.log | LOG | 754 B | work | 8d4e2a5d41a5... |
| NC-003_best_pose.sdf | SDF | 3.6 KB | structures | de89c0097444... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 16 file(s) were produced and registered, 16 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- Versions were not recorded for GNINA, Rayca Modulon. A methods section without a version is not reproducible.

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. J Cheminform. 2021;13:43. doi:10.1186/s13321-021-00522-2
