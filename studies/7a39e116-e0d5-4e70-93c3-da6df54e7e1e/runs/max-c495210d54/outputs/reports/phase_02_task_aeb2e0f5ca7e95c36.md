---
title: "Phase 2: task aeb2e0f5ca7e95c36"
study_id: "7a39e116-e0d5-4e70-93c3-da6df54e7e1e"
run_id: "max-2859534fd9"
phase_index: 2
phase_id: "aeb2e0f5ca7e95c36"
phase_goal: "task aeb2e0f5ca7e95c36"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 2: task aeb2e0f5ca7e95c36

## Summary

This phase set out to task aeb2e0f5ca7e95c36. It completed 1 method step, 17 output files.

## Objective

task aeb2e0f5ca7e95c36

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
| gbsa | software | not recorded | no citation on record | not recorded |

### Procedure

#### 1. Molecular dynamics refinement and binding free energy calculation

EL2003A pose 2 (the best MM-GBSA pose) was refined using GROMACS molecular dynamics simulation with Generalized Born implicit solvent (GBSA) method. The system was simulated for 1 ns (500000 steps) with 50000 equilibration steps, using AMBER03 force field for protein and GAFF2 for ligand with Gasteiger charges. Binding free energy was recalculated following MD refinement.

**Rationale.** Molecular dynamics refinement improves the geometric and energetic accuracy of docked poses by allowing the system to sample conformational space and relax into local energy minima, providing more realistic binding free energy estimates.

| Field | Value |
| :--- | :--- |
| Inputs | EL2003A_pose2.sdf, 1Z5M_receptor_pH7.4.pdb |
| Outputs | best_dG_kcal_per_mol |
| Tools | gbsa |
| Status | running |

Parameters:

```yaml
boxType: dodecahedron
conc: 0.15
decompose: True
eqsteps: 50000
gpu: True
ligandCharge: gas
ligandForceField: gaff2
method: gb
mode: md
nframe: 100
nsteps: 500000
proteinForceField: amber03
```

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| 103_print.py | PY | 469 B | 01_extract_final_md_pose_sdf_and_create_trajectory_/source | 9c115ab0a31b... |
| extract_final_pose_sdf.py | PY | 3.4 KB | 01_extract_final_md_pose_sdf_and_create_trajectory_/source | 621b2f9cf942... |
| make_traj_video.py | PY | 8.8 KB | 01_extract_final_md_pose_sdf_and_create_trajectory_/source | 2667390ce6d2... |
| EL2003A_pose2_MD_final.sdf | SDF | 3.4 KB | 01_extract_final_md_pose_sdf_and_create_trajectory_/structures | 0f941903d323... |
| 104_first.py | PY | 470 B | 01_extract_final_md_pose_sdf_and_create_trajectory_/source | 97b52a732ef4... |
| extract_final_pose_sdf.py | PY | 4.8 KB | 01_extract_final_md_pose_sdf_and_create_trajectory_/source | 087697de66ee... |
| EL2003A_pose2_MD_final.sdf | SDF | 3.4 KB | 01_extract_final_md_pose_sdf_and_create_trajectory_/structures | 440112a808d6... |
| 105_subprocess_run.py | PY | 436 B | 01_extract_final_md_pose_sdf_and_create_trajectory_/source | 1fee130c3168... |
| 106_print.py | PY | 498 B | 01_extract_final_md_pose_sdf_and_create_trajectory_/source | d7c1d9a90155... |
| make_traj_video.py | PY | 8.5 KB | 01_extract_final_md_pose_sdf_and_create_trajectory_/source | 9ca6a69cf937... |
| EL2003A_MD_final_frame.png | PNG | 322.4 KB | 01_extract_final_md_pose_sdf_and_create_trajectory_/figures | 412e4504cce9... |
| EL2003A_MD_ligand_RMSD.png | PNG | 57.1 KB | 01_extract_final_md_pose_sdf_and_create_trajectory_/figures | 7d353b9025d3... |
| EL2003A_MD_trajectory.gif | GIF | 7.0 MB | 01_extract_final_md_pose_sdf_and_create_trajectory_/figures | 5558e028dc3b... |
| 107_print.py | PY | 449 B | 01_extract_final_md_pose_sdf_and_create_trajectory_/source | 29307636ae16... |
| 108_os_path_getsize.py | PY | 379 B | 01_extract_final_md_pose_sdf_and_create_trajectory_/source | 4c9c8477d52f... |
| phase_01_extract_final_md_pose_sdf_and_create_trajectory_.md | MD | 5.1 KB | reports | 87d2a8f51367... |
| audit_extract_MD_final_pose_SDF_and_video.md | MD | 12.9 KB | reports | 7ffb2e70e1ee... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 17 file(s) were produced and registered, 17 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No citation is on record for gbsa, so the versions used cannot be traced to a publication.
- Versions were not recorded for gbsa. A methods section without a version is not reproducible.

## References

**No citation on record:** gbsa.

These were used by this phase and are reported for completeness. A citation should be supplied before this material is used in a manuscript. They are listed rather than omitted because a methods section that hides a dependency is not reproducible.
