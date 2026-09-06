---
title: "Phase 4: task a9a39ae9227ad366c"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-72315b3a90"
phase_index: 4
phase_id: "a9a39ae9227ad366c"
phase_goal: "task a9a39ae9227ad366c"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 4: task a9a39ae9227ad366c

## Summary

This phase set out to task a9a39ae9227ad366c. It completed 1 method step, 13 output files.

## Objective

task a9a39ae9227ad366c

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
| 010_run_aidd_tool.py | PY | 657 B | source | 3e22c23bf4b6... |
| phase_01_task_af635c98a0a324864.md | MD | 3.0 KB | reports | 99cd0ab9ba95... |
| 011_run_aidd_tool.py | PY | 656 B | source | 3e8b505ac3af... |
| 012_run_aidd_tool.py | PY | 642 B | source | 41a20aeaeba5... |
| gnina_docked.sdf.gz | GZ | 3.2 KB | structures | eb8082b33d87... |
| phase_02_task_a5c415557dfea3252.md | MD | 3.3 KB | reports | 60227640d445... |
| 013_run_aidd_tool.py | PY | 641 B | source | 28814c2b6fe0... |
| gnina_docked.sdf.gz | GZ | 3.3 KB | structures | 6c89bd9dc2ba... |
| gnina_docked.sdf.gz | GZ | 3.6 KB | structures | 3f3498dfd1a0... |
| 014_run_aidd_tool.py | PY | 641 B | source | d0ecef0fa6d1... |
| 015_run_aidd_tool.py | PY | 657 B | source | b2a46579a47a... |
| gnina_docked.sdf.gz | GZ | 3.6 KB | 03_task_wkld1xz7a/structures | c7939d4cbb97... |
| audit_phase01_af635c98.md | MD | 14.4 KB | 03_task_wkld1xz7a/reports | 15eb927cd16a... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 13 file(s) were produced and registered, 13 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/gnina:latest`

## Limitations

- Versions were not recorded for GNINA, Rayca Modulon. A methods section without a version is not reproducible.

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. J Cheminform. 2021;13:43. doi:10.1186/s13321-021-00522-2
