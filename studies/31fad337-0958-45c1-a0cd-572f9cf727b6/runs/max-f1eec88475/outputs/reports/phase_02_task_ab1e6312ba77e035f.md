---
title: "Phase 2: task ab1e6312ba77e035f"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-be77e6af28"
phase_index: 2
phase_id: "ab1e6312ba77e035f"
phase_goal: "task ab1e6312ba77e035f"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 2: task ab1e6312ba77e035f

## Summary

This phase set out to task ab1e6312ba77e035f. It completed 1 method step, 41 output files.

## Objective

task ab1e6312ba77e035f

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
| CTX-1020667_docking_result.json | JSON | 1.0 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/work | 01b739264d2f... |
| 069_path.py | PY | 1.1 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/source | e8dc244673c3... |
| 070_out_path_read_text.py | PY | 455 B | 01_re_dock_and_mm_gbsa_ctx_1020667/source | f7fa0ffa428f... |
| gnina_docked.sdf.gz | GZ | 5.9 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/structures | 5fb99e7a3854... |
| 071_path.py | PY | 1.2 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/source | a0126c079667... |
| 072_result_still_scope_extract_poses_safely.py | PY | 483 B | 01_re_dock_and_mm_gbsa_ctx_1020667/source | 5565b10e2d26... |
| 073_check_output_file_field_find_docked_sdf.py | PY | 468 B | 01_re_dock_and_mm_gbsa_ctx_1020667/source | f42ed9f22a72... |
| 074_path.py | PY | 2.2 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/source | b87fa6116d25... |
| CTX-1020667_mmgbsa_result.json | JSON | 476 B | 01_re_dock_and_mm_gbsa_ctx_1020667/work | c9f1f5ce47e7... |
| extract_and_addH_667.py | PY | 1.3 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/source | ca86e707f4e2... |
| CTX-1020667_best_pose.sdf | SDF | 4.1 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/structures | 58a6f28f714e... |
| CTX-1020667_best_pose_H.sdf | SDF | 6.5 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/structures | 62d1bee816b7... |
| BindingEnergy.csv | CSV | 383 B | 01_re_dock_and_mm_gbsa_ctx_1020667/tables | 84cea76febc7... |
| CTX-1020667_best_pose_H.mol | MOL | 6.4 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/structures | d4395f87c3cc... |
| Energy.csv | CSV | 340 B | 01_re_dock_and_mm_gbsa_ctx_1020667/tables | cb826799f25b... |
| complex.pdb | PDB | 717.9 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/structures | 1b53070458ae... |
| complex.top | TOP | 4.6 MB | 01_re_dock_and_mm_gbsa_ctx_1020667/work | d7d181698d53... |
| complex_reres.pdb | PDB | 717.9 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/structures | 2034db25c82c... |
| 075_path.py | PY | 3.2 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/source | d025a4dc978e... |
| CTX-1020667_mmgbsa_result.json | JSON | 481 B | 01_re_dock_and_mm_gbsa_ctx_1020667/work | 615d76a8da52... |
| BindingEnergy.csv | CSV | 390 B | 01_re_dock_and_mm_gbsa_ctx_1020667/tables | 4b5012f1dc40... |
| CTX-1020667_best_pose_H.mol | MOL | 6.4 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/structures | 2cbe6d4eb397... |
| Energy.csv | CSV | 350 B | 01_re_dock_and_mm_gbsa_ctx_1020667/tables | ef2143ced8e0... |
| complex.pdb | PDB | 717.9 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/structures | 8a16e90462c6... |
| complex.top | TOP | 4.6 MB | 01_re_dock_and_mm_gbsa_ctx_1020667/work | d9533179128b... |
| complex_reres.pdb | PDB | 717.9 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/structures | 233fcac0922f... |
| 076_path.py | PY | 2.3 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/source | 4d3322d82857... |
| mmgbsa_results.json | JSON | 31.3 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/work | 60e8a9b2c8c7... |
| 077_path.py | PY | 1.8 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/source | 5be55b4a9b59... |
| CDK2_CyclinE1_Docking_Report.md | MD | 25.2 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/reports | 09406da42c20... |
| CDK2_CyclinE1_Docking_Report.md | MD | 25.7 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/reports | 1667910aa7af... |
| CDK2_CyclinE1_Docking_Report.md | MD | 25.7 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/reports | 0249ef342da1... |
| CDK2_CyclinE1_Docking_Report.md | MD | 25.8 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/reports | 330c35ae080d... |
| CDK2_CyclinE1_Docking_Report.md | MD | 25.8 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/reports | 572100f58d80... |
| CDK2_CyclinE1_Docking_Report.md | MD | 26.0 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/reports | a796a969595e... |
| CDK2_CyclinE1_Docking_Report.md | MD | 26.0 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/reports | 43301e7d35b1... |
| phase_01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin.md | MD | 58.8 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/reports | 7e9264324326... |
| phase_01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin.md | MD | 58.8 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/reports | c89b2374badf... |
| phase_01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin.md | MD | 59.1 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/reports | 85ec00235e1d... |
| phase_03_mmgbsa_83_cdk2_cycline1_compounds.md | MD | 10.4 KB | 01_re_dock_and_mm_gbsa_ctx_1020667/reports | 8c0e3dd1bb7f... |
| phase_01_re_dock_and_mm_gbsa_ctx_1020667.md | MD | 7.2 KB | reports | 96950af2d867... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 41 file(s) were produced and registered, 41 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/gnina:latest`
- Container Image: `registry.rayca.org/rayca-tools/gbsa:latest`

## Limitations

- Versions were not recorded for GNINA, Rayca Modulon. A methods section without a version is not reproducible.

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. J Cheminform. 2021;13:43. doi:10.1186/s13321-021-00522-2
