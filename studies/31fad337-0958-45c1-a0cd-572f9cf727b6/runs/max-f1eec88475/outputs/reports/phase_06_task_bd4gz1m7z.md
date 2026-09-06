---
title: "Phase 6: task bd4gz1m7z"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-c3fda373b8"
phase_index: 6
phase_id: "bd4gz1m7z"
phase_goal: "task bd4gz1m7z"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 6: task bd4gz1m7z

## Summary

This phase set out to task bd4gz1m7z. It completed 1 method step, 39 output files.

## Objective

task bd4gz1m7z

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
| gnina_docked.sdf.gz | GZ | 5.5 KB | structures | a850d0541e64... |
| phase_01_task_btgnat4b7.md | MD | 3.9 KB | reports | eae46c8ef5ba... |
| dock_nc_run.log | LOG | 1006 B | work | 10ef9dca7fca... |
| nc_docking_results.json | JSON | 1.3 KB | work | 292214c9a658... |
| NC-004_best_pose.sdf | SDF | 3.7 KB | structures | a4de1302565f... |
| gnina_docked.sdf.gz | GZ | 5.9 KB | 02_task_bs278bt9z/structures | 5c823efcb545... |
| dock_nc_run.log | LOG | 1.2 KB | 02_task_bs278bt9z/work | d95b0b341832... |
| nc_docking_results.json | JSON | 1.6 KB | 02_task_bs278bt9z/work | 9ab055442474... |
| NC-005_best_pose.sdf | SDF | 3.7 KB | 02_task_bs278bt9z/structures | 81e0d2c3b5d4... |
| gnina_docked.sdf.gz | GZ | 5.8 KB | 02_task_bs278bt9z/structures | 3e84f7612fc8... |
| dock_nc_run.log | LOG | 1.5 KB | 02_task_bs278bt9z/work | d36e8fa84ba1... |
| nc_docking_results.json | JSON | 1.9 KB | 02_task_bs278bt9z/work | 7c948d0abc91... |
| NC-006_best_pose.sdf | SDF | 3.7 KB | 02_task_bs278bt9z/structures | 7b69d60ede71... |
| gnina_docked.sdf.gz | GZ | 5.7 KB | 02_task_bs278bt9z/structures | 328b757e18a2... |
| dock_nc_run.log | LOG | 1.7 KB | 02_task_bs278bt9z/work | 30235d605b29... |
| nc_docking_results.json | JSON | 2.2 KB | 02_task_bs278bt9z/work | 5fb7d52fdadd... |
| NC-007_best_pose.sdf | SDF | 3.7 KB | 02_task_bs278bt9z/structures | 2525f060f4c1... |
| dock_nc_run.log | LOG | 2.6 KB | 02_task_bs278bt9z/work | 943da236b368... |
| nc_docking_results.json | JSON | 3.2 KB | 02_task_bs278bt9z/work | 80c0f5b9a5d2... |
| NC-008_best_pose.sdf | SDF | 3.7 KB | 02_task_bs278bt9z/structures | e25a1ea9b24f... |
| NC-009_best_pose.sdf | SDF | 3.8 KB | 02_task_bs278bt9z/structures | 3912de810483... |
| NC-010_best_pose.sdf | SDF | 3.7 KB | 02_task_bs278bt9z/structures | 8846fcb8d460... |
| gnina_docked.sdf.gz | GZ | 5.8 KB | 02_task_bs278bt9z/structures | 4a2183f30cdd... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 39 file(s) were produced and registered, 39 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- Versions were not recorded for GNINA, Rayca Modulon. A methods section without a version is not reproducible.

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. J Cheminform. 2021;13:43. doi:10.1186/s13321-021-00522-2
