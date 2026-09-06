---
title: "Phase 1: Prepare 3D SDF files for NC-001 to NC-010 from SMILES"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-4cd09bc504"
phase_index: 1
phase_id: "1"
phase_goal: "Prepare 3D SDF files for NC-001 to NC-010 from SMILES"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Prepare 3D SDF files for NC-001 to NC-010 from SMILES

## Summary

This phase set out to prepare 3D SDF files for NC-001 to NC-010 from SMILES. It completed 1 method step, 29 output files.

## Objective

Prepare 3D SDF files for NC-001 to NC-010 from SMILES

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
| NC-001.sdf | SDF | 3.5 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 7a0d697f1959... |
| NC-002.sdf | SDF | 3.5 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 1b959e57aff7... |
| NC-003.sdf | SDF | 3.3 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 9cf0adcf3baa... |
| NC-004.sdf | SDF | 3.5 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 58d2c833c1d1... |
| NC-005.sdf | SDF | 3.3 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 9536a3c7fc80... |
| NC-006.sdf | SDF | 3.4 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | d60c6931af3b... |
| NC-007.sdf | SDF | 3.4 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 9026916dea8c... |
| NC-008.sdf | SDF | 3.4 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | b81700b9e160... |
| NC-009.sdf | SDF | 3.6 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 12c77ab2a41f... |
| NC-010.sdf | SDF | 3.4 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | d0f77bd655fa... |
| 078_path.py | PY | 2.2 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/source | 936cbb5f79b8... |
| 079_check_rdkit_version_basic_import.py | PY | 193 B | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/source | 78467101858b... |
| 080_print.py | PY | 21 B | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/source | 4660ab1ff310... |
| 081_sys_path_insert.py | PY | 271 B | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/source | 5865b2b8af18... |
| test_toluene.sdf | SDF | 671 B | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 3849656f42fb... |
| prepare_nc_ligands.py | PY | 2.3 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/source | 1079fc03d21e... |
| 082_path.py | PY | 2.1 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/source | ea82f8119399... |
| 083_test_sdwriter_simple_molecule.py | PY | 716 B | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/source | 75d5f9385016... |
| 084_test_basic_moltomolblock_without_3d.py | PY | 227 B | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/source | c573cb84d152... |
| NC-001.sdf | SDF | 3.5 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | e539fcaa67c6... |
| NC-002.sdf | SDF | 3.5 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | c74c435d4831... |
| NC-003.sdf | SDF | 3.3 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | c84d3deb7243... |
| NC-004.sdf | SDF | 3.5 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 3d2501ade2be... |
| NC-005.sdf | SDF | 3.3 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | b199b4e5942b... |
| NC-006.sdf | SDF | 3.4 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 24ca6811e994... |
| NC-007.sdf | SDF | 3.4 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | dbc99eaa1570... |
| NC-008.sdf | SDF | 3.4 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 9dbcf6af4401... |
| NC-009.sdf | SDF | 3.6 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | d27ec919c5d9... |
| NC-010.sdf | SDF | 3.4 KB | 01_prepare_3d_sdf_files_for_nc_001_to_nc_010_from_s/structures | 6d55abeb1edc... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 29 file(s) were produced and registered, 29 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- Versions were not recorded for GNINA, Rayca Modulon. A methods section without a version is not reproducible.

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. J Cheminform. 2021;13:43. doi:10.1186/s13321-021-00522-2
