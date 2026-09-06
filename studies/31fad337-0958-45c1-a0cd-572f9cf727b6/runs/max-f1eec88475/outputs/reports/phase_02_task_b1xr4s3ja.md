---
title: "Phase 2: task b1xr4s3ja"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-42cb9162e6"
phase_index: 2
phase_id: "b1xr4s3ja"
phase_goal: "task b1xr4s3ja"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 2: task b1xr4s3ja

## Summary

This phase set out to task b1xr4s3ja. It completed 1 method step, 4 output files.

## Objective

task b1xr4s3ja

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
| test_mmgbsa.py | PY | 4.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/source | 4d6610563fe5... |
| 047_feasibility_test_can_parameterise_ligand_gaff2_via.py | PY | 1.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/source | be8a84440068... |
| redock_list.json | JSON | 1.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 8182c0ca9f33... |
| redock_for_poses.py | PY | 3.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/source | 0e5a4bc6b8cb... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 4 file(s) were produced and registered, 4 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- Versions were not recorded for GNINA, Rayca Modulon. A methods section without a version is not reproducible.

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. J Cheminform. 2021;13:43. doi:10.1186/s13321-021-00522-2
