---
title: "Phase 1: Dock 84 CDK2-CyclinE1 ligands via batched run_python"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-0072625358"
phase_index: 1
phase_id: "1"
phase_goal: "Dock 84 CDK2-CyclinE1 ligands via batched run_python"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Dock 84 CDK2-CyclinE1 ligands via batched run_python

## Summary

This phase set out to dock 84 CDK2-CyclinE1 ligands via batched run_python. It completed 1 method step, 77 output files.

## Objective

Dock 84 CDK2-CyclinE1 ligands via batched run_python

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
| gnina_docked.sdf.gz | GZ | 3.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 2fdfb91c7779... |
| 019_run_aidd_tool.py | PY | 863 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 132ac86130b2... |
| 020_check_what_s_already_completed_workflow_journal.py | PY | 1.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 4373b467528d... |
| docking_checkpoint.json | JSON | 396 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 266ae39c21e2... |
| 021_pathlib_path.py | PY | 2.0 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 36d45edaa8e8... |
| docking_checkpoint.json | JSON | 3.6 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 887e4e7772fa... |
| gnina_docked.sdf.gz | GZ | 3.3 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | a2a6f104e95a... |
| 022_str.py | PY | 1.8 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 8c48e732d80f... |
| gnina_docked.sdf.gz | GZ | 3.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 9ca55062d1cf... |
| 023_inspect_checkpoint_see_what_actually_came_back.py | PY | 773 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | f3a2b0314386... |
| docking_checkpoint.json | JSON | 14.8 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 9af93e3912c3... |
| gnina_docked.sdf.gz | GZ | 3.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | f85201c1a2a8... |
| 024_correct_field_mapping_results_live_under_r_output.py | PY | 2.2 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 206596e82f4b... |
| 025_compute_what_still_needs_docking.py | PY | 265 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 60a0cfe64a85... |
| docking_checkpoint.json | JSON | 29.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 3f5ed0e5349f... |
| gnina_docked.sdf.gz | GZ | 4.0 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | bbd317475a76... |
| 026_dock_one.py | PY | 1.6 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | d902b7d16d9d... |
| 027_dock_one.py | PY | 1.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | c843672979ec... |
| 028_path.py | PY | 2.2 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | e204f4f4fd7c... |
| docking_checkpoint.json | JSON | 44.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | b3a7f1f4ddcb... |
| gnina_docked.sdf.gz | GZ | 4.2 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | d5eb994519df... |
| 029_dock_one.py | PY | 1.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | ed9f3bbef66d... |
| 030_dock_one.py | PY | 1.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 88fbac38e219... |
| 031_write_persistent_setup_file_once_reload_start_each.py | PY | 3.9 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | b9638b30914e... |
| dock_setup.py | PY | 3.6 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | df498aa4ddc9... |
| 032_path.py | PY | 230 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 26af206c443e... |
| docking_checkpoint.json | JSON | 57.5 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 9779baaaa2ef... |
| gnina_docked.sdf.gz | GZ | 3.8 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | a3ee4937fd4b... |
| 033_exec.py | PY | 378 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 47a57aad78c3... |
| docking_checkpoint.json | JSON | 72.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 67f410c52188... |
| gnina_docked.sdf.gz | GZ | 3.0 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | c272d8daacc8... |
| 034_exec.py | PY | 378 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | f5a287ae5cc2... |
| docking_checkpoint.json | JSON | 83.2 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | ce2f67cee20a... |
| gnina_docked.sdf.gz | GZ | 3.6 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | aa00ffbf1484... |
| 035_exec.py | PY | 346 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 85c180b1459d... |
| docking_results.json | JSON | 82.0 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 4295cbdffe90... |
| 036_path.py | PY | 896 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | f87b0ecedc66... |
| gnina_docked.sdf.gz | GZ | 3.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | ee5f6c8b20e5... |
| 037_path.py | PY | 2.3 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 9cde563951c6... |
| 038_path.py | PY | 819 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | f1c7fb25f18f... |
| pose_map.json | JSON | 2.9 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 43cbd6ca94cf... |
| CTX-1019473_poses.sdf | SDF | 18.4 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 916485372c15... |
| CTX-1019613_poses.sdf | SDF | 20.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 42bc963239a4... |
| CTX-1019757_poses.sdf | SDF | 20.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 0ebc242808ae... |
| CTX-1019813_poses.sdf | SDF | 19.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 90986d3fe3e4... |
| CTX-1020441_poses.sdf | SDF | 20.6 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | b3c1f524606a... |
| CTX-1020456_poses.sdf | SDF | 20.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 4e51302fb83e... |
| CTX-1020521_poses.sdf | SDF | 22.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 2eae1211812b... |
| CTX-1020555_poses.sdf | SDF | 19.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | ff1d83fbfd8b... |
| CTX-1020562_poses.sdf | SDF | 21.8 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 652fa50b441a... |
| CTX-1020696_poses.sdf | SDF | 19.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 5e74f5ea0707... |
| CTX-1020732_poses.sdf | SDF | 19.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 893fb5e402b8... |
| CTX-1020743_poses.sdf | SDF | 20.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 84a1ca1e0100... |
| CTX-1020745_poses.sdf | SDF | 20.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 219ffb149ec4... |
| CTX-1020748_poses.sdf | SDF | 20.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 1b7e6a8e015e... |
| CTX-1020751_poses.sdf | SDF | 18.8 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 67cf2bd435f6... |
| CTX-1020752_poses.sdf | SDF | 20.5 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | d273ff568033... |
| CTX-1020753_poses.sdf | SDF | 20.5 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 5c591f9096d5... |
| CTX-1020800_poses.sdf | SDF | 20.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 1a93b0336fe6... |
| CTX-1020811_poses.sdf | SDF | 20.5 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | ce7177300780... |
| CTX-1020903_poses.sdf | SDF | 20.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/structures | 65802fcde86e... |
| 039_path.py | PY | 1.9 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | b17b9ab3d59e... |
| docking_results.json | JSON | 82.5 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | d8f0c79bcb1c... |
| 040_path.py | PY | 555 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 5c8cb235610a... |
| energy_results.json | JSON | 14.4 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 1b5a8b56458a... |
| 041_exec.py | PY | 128 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 7a608ec728c5... |
| 042_path.py | PY | 2.2 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | b0d846d0e1ac... |
| 043_print.py | PY | 148 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 73e767a713a7... |
| interaction_fingerprints.json | JSON | 8.8 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 8e0e1ccf443f... |
| interaction_stats.json | JSON | 2.7 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | b8d32a987ffd... |
| run_interactions.py | PY | 3.8 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | a2932d60fdd1... |
| interaction_fingerprints.json | JSON | 15.1 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 0a73052598fd... |
| interaction_stats.json | JSON | 4.8 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/work | 19077206941e... |
| 044_path.py | PY | 1.2 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 0a9f361368d8... |
| 045_find_phase_directories_any_existing_phase_documents.py | PY | 439 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | e9a30c44ddb3... |
| 046_path.py | PY | 628 B | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/source | 591ee3729928... |
| phase_05_dock_84_ligands_batched_run_python.md | MD | 10.0 KB | 01_dock_84_cdk2_cycline1_ligands_via_batched_run_py/reports | 299e79d11204... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 77 file(s) were produced and registered, 77 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/gnina:latest`

## Limitations

- Versions were not recorded for GNINA, Rayca Modulon. A methods section without a version is not reproducible.

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. J Cheminform. 2021;13:43. doi:10.1186/s13321-021-00522-2
