---
title: "Phase 9: task bg261joc1"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-c3fda373b8"
phase_index: 9
phase_id: "bg261joc1"
phase_goal: "task bg261joc1"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 9: task bg261joc1

## Summary

This phase set out to task bg261joc1. It completed 1 method step, 112 output files.

## Objective

task bg261joc1

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
| phase_06_task_bd4gz1m7z.md | MD | 5.7 KB | 02_task_bs278bt9z/reports | a38b91ab2a39... |
| phase_07_task_2.md | MD | 5.7 KB | 02_task_bs278bt9z/reports | bc57f95000a0... |
| nc_mmgbsa_run.log | LOG | 0 B | 02_task_bs278bt9z/work | e3b0c44298fc... |
| NC-001_best_pose_H.sdf | SDF | 6.3 KB | 02_task_bs278bt9z/structures | 34fae4a126e7... |
| NC-002_best_pose_H.sdf | SDF | 6.3 KB | 02_task_bs278bt9z/structures | 0b1b6b44fc80... |
| NC-003_best_pose_H.sdf | SDF | 6.0 KB | 02_task_bs278bt9z/structures | 6323fdbf7954... |
| NC-004_best_pose_H.sdf | SDF | 6.6 KB | 02_task_bs278bt9z/structures | c541b587fd04... |
| NC-005_best_pose_H.sdf | SDF | 6.1 KB | 02_task_bs278bt9z/structures | dc2df20eec0d... |
| NC-006_best_pose_H.sdf | SDF | 6.0 KB | 02_task_bs278bt9z/structures | f9272f4437b6... |
| NC-007_best_pose_H.sdf | SDF | 6.1 KB | 02_task_bs278bt9z/structures | 6b5491cb790f... |
| NC-008_best_pose_H.sdf | SDF | 6.2 KB | 02_task_bs278bt9z/structures | 3d705e005bfc... |
| NC-009_best_pose_H.sdf | SDF | 6.7 KB | 02_task_bs278bt9z/structures | 15c0182b0606... |
| NC-010_best_pose_H.sdf | SDF | 6.3 KB | 02_task_bs278bt9z/structures | 20256a170136... |
| phase_nc_docking_mmgbsa.md | MD | 6.1 KB | 02_task_bs278bt9z/reports | 20889ddd5c69... |
| nc_mmgbsa_results.json | JSON | 346 B | 02_task_bs278bt9z/work | 930e19b00e68... |
| nc_mmgbsa_run.log | LOG | 565 B | 02_task_bs278bt9z/work | deb87f9406a4... |
| BindingEnergy.csv | CSV | 375 B | 02_task_bs278bt9z/tables | b052c6cfca5f... |
| Energy.csv | CSV | 348 B | 02_task_bs278bt9z/tables | c30fe42ff1d8... |
| NC-001_best_pose_H.mol | MOL | 6.7 KB | 02_task_bs278bt9z/structures | 71db29d39dc0... |
| complex.pdb | PDB | 718.2 KB | 02_task_bs278bt9z/structures | 9694852fa587... |
| complex.top | TOP | 4.6 MB | 02_task_bs278bt9z/work | 2bd0fb3ac581... |
| complex_reres.pdb | PDB | 718.2 KB | 02_task_bs278bt9z/structures | eff2a1b27115... |
| nc_mmgbsa_results.json | JSON | 3.0 KB | 02_task_bs278bt9z/work | 4f3377f77f20... |
| nc_mmgbsa_run.log | LOG | 1.2 KB | 02_task_bs278bt9z/work | edcee1dd285d... |
| BindingEnergy.csv | CSV | 367 B | 02_task_bs278bt9z/tables | 44a0e64d51cf... |
| Energy.csv | CSV | 348 B | 02_task_bs278bt9z/tables | da6cbb7b5288... |
| NC-002_best_pose_H.mol | MOL | 6.7 KB | 02_task_bs278bt9z/structures | 13af5efc8cbf... |
| complex.pdb | PDB | 718.2 KB | 02_task_bs278bt9z/structures | 3784e00219ba... |
| complex.top | TOP | 4.6 MB | 02_task_bs278bt9z/work | a062f36c8039... |
| complex_reres.pdb | PDB | 718.2 KB | 02_task_bs278bt9z/structures | d21f3adf9527... |
| Energy.csv | CSV | 351 B | 02_task_bs278bt9z/tables | 6c89fa7516a4... |
| NC-003_best_pose_H.mol | MOL | 6.4 KB | 02_task_bs278bt9z/structures | ce674c2f751d... |
| complex.pdb | PDB | 717.9 KB | 02_task_bs278bt9z/structures | 29867eb2d903... |
| complex.top | TOP | 4.6 MB | 02_task_bs278bt9z/work | 72dfacfe566f... |
| complex_reres.pdb | PDB | 717.9 KB | 02_task_bs278bt9z/structures | 25b9bc2e8968... |
| Energy.csv | CSV | 341 B | 02_task_bs278bt9z/tables | 3bd531e0f5aa... |
| NC-004_best_pose_H.mol | MOL | 7.0 KB | 02_task_bs278bt9z/structures | ba82d5596bdd... |
| complex.pdb | PDB | 718.4 KB | 02_task_bs278bt9z/structures | d4ba8942a96e... |
| complex.top | TOP | 4.6 MB | 02_task_bs278bt9z/work | 315afbca6066... |
| complex_reres.pdb | PDB | 718.4 KB | 02_task_bs278bt9z/structures | 3e996d444484... |
| Energy.csv | CSV | 347 B | 02_task_bs278bt9z/tables | 00645f609059... |
| NC-005_best_pose_H.mol | MOL | 6.5 KB | 02_task_bs278bt9z/structures | 8ea2ce21d0be... |
| complex.pdb | PDB | 717.9 KB | 02_task_bs278bt9z/structures | b19158e38e9e... |
| complex.top | TOP | 4.6 MB | 02_task_bs278bt9z/work | 18105665183a... |
| complex_reres.pdb | PDB | 717.9 KB | 02_task_bs278bt9z/structures | 05a058131a92... |
| Energy.csv | CSV | 342 B | 02_task_bs278bt9z/tables | d3cdbb898bc5... |
| NC-006_best_pose_H.mol | MOL | 6.4 KB | 02_task_bs278bt9z/structures | 25af617d2315... |
| complex.pdb | PDB | 717.9 KB | 02_task_bs278bt9z/structures | 3ae407d9a5dd... |
| complex.top | TOP | 4.6 MB | 02_task_bs278bt9z/work | 754038cf5771... |
| complex_reres.pdb | PDB | 717.9 KB | 02_task_bs278bt9z/structures | a31a61f45c98... |
| Energy.csv | CSV | 342 B | 02_task_bs278bt9z/tables | d4e18eae4953... |
| NC-007_best_pose_H.mol | MOL | 6.5 KB | 02_task_bs278bt9z/structures | 0fe14ddfc9fd... |
| complex.pdb | PDB | 717.9 KB | 02_task_bs278bt9z/structures | a87c560a8a56... |
| complex.top | TOP | 4.6 MB | 02_task_bs278bt9z/work | babf4f5a9b16... |
| complex_reres.pdb | PDB | 717.9 KB | 02_task_bs278bt9z/structures | b3e33d7f3a6b... |
| Energy.csv | CSV | 340 B | 02_task_bs278bt9z/tables | 0b0db148ceb2... |
| NC-008_best_pose_H.mol | MOL | 6.7 KB | 02_task_bs278bt9z/structures | ba792309aaef... |
| complex.pdb | PDB | 718.1 KB | 02_task_bs278bt9z/structures | ada1acac6be6... |
| complex.top | TOP | 4.6 MB | 02_task_bs278bt9z/work | 0bdbfed244ab... |
| complex_reres.pdb | PDB | 718.1 KB | 02_task_bs278bt9z/structures | fc6ed17cb365... |
| Energy.csv | CSV | 340 B | 02_task_bs278bt9z/tables | c63d4a3179d2... |
| NC-009_best_pose_H.mol | MOL | 7.1 KB | 02_task_bs278bt9z/structures | 9665b7d5d37c... |
| complex.pdb | PDB | 718.5 KB | 02_task_bs278bt9z/structures | 92dea52e11ed... |
| complex.top | TOP | 4.6 MB | 02_task_bs278bt9z/work | 65c801bd2918... |
| complex_reres.pdb | PDB | 718.5 KB | 02_task_bs278bt9z/structures | 01221fcb3fca... |
| nc_mmgbsa_results.json | JSON | 3.3 KB | 02_task_bs278bt9z/work | baa68cc2a9c1... |
| nc_mmgbsa_run.log | LOG | 1.5 KB | 02_task_bs278bt9z/work | b74f1d44a1f3... |
| BindingEnergy.csv | CSV | 379 B | 02_task_bs278bt9z/tables | f608b44cd1a2... |
| Energy.csv | CSV | 340 B | 02_task_bs278bt9z/tables | 9c393ec20a88... |
| NC-010_best_pose_H.mol | MOL | 6.7 KB | 02_task_bs278bt9z/structures | cc24ecfd8f98... |
| complex.pdb | PDB | 718.2 KB | 02_task_bs278bt9z/structures | 1ae449be2cfd... |
| complex.top | TOP | 4.6 MB | 02_task_bs278bt9z/work | 1ab3efe1eded... |
| complex_reres.pdb | PDB | 718.2 KB | 02_task_bs278bt9z/structures | a92251ce155b... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 112 file(s) were produced and registered, 112 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- Versions were not recorded for GNINA, Rayca Modulon. A methods section without a version is not reproducible.

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. J Cheminform. 2021;13:43. doi:10.1186/s13321-021-00522-2
