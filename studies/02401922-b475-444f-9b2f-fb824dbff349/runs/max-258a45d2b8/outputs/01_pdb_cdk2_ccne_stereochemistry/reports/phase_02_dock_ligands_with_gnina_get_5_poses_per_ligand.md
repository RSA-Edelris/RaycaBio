---
title: "Phase 2: Dock ligands with gnina, get 5 poses per ligand"
study_id: "02401922-b475-444f-9b2f-fb824dbff349"
run_id: "max-e87c3d4aff"
phase_index: 2
phase_id: "2"
phase_goal: "Dock ligands with gnina, get 5 poses per ligand"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 2: Dock ligands with gnina, get 5 poses per ligand

## Summary

This phase set out to dock ligands with gnina, get 5 poses per ligand. It completed 31 output files.

## Objective

Dock ligands with gnina, get 5 poses per ligand

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

This phase used no external software or databases that the record identifies by name.

### Procedure

No method records were captured for this phase, so the procedure cannot be stated. This is a gap in the record, not a phase that did no work.
## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| 001_aidd_tool_schema.py | PY | 106 B | 01_pdb_cdk2_ccne_stereochemistry/source | 634a51806c91... |
| 002_check_available_tools_receptor_ligand_prep.py | PY | 443 B | 01_pdb_cdk2_ccne_stereochemistry/source | d0e2db5139a5... |
| receptor_raw.pdb | PDB | 364.1 KB | 01_pdb_cdk2_ccne_stereochemistry/inputs | 78add4a6bf12... |
| 003_receptor_preparation_keep_chains_b_9_structural.py | PY | 1.4 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 1598f4ef49d0... |
| receptor_prepared.pdb | PDB | 733.0 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | b167ba582764... |
| 004_run_pdbfixer_fix_missing_atoms_add_h_ph_7_4.py | PY | 1.0 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 43dd28e4a945... |
| 005_ligand_preparation_1_load_sdf_2d_v3000_standardize.py | PY | 831 B | 01_pdb_cdk2_ccne_stereochemistry/source | 3e8ef59305d4... |
| 006_standardize_remove_fragments_salts_normalize.py | PY | 1.4 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 8916a4c8d6c5... |
| ligand_3d_raw.sdf | SDF | 6.0 KB | 01_pdb_cdk2_ccne_stereochemistry/inputs | c649d31336e7... |
| ligand_prepared.sdf | SDF | 6.8 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | d8cd79864a03... |
| 007_generate_3d_coords_etkdg_protonate_ph_7_4_via_obabel.py | PY | 976 B | 01_pdb_cdk2_ccne_stereochemistry/source | 8b031eb93a85... |
| ctx_ref.pdb | PDB | 5.7 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 201f9b8dcc6c... |
| ctx_ref.sdf | SDF | 6.8 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 079c666a4360... |
| 008_extract_ctx_pdb_sdf_reference_docking.py | PY | 957 B | 01_pdb_cdk2_ccne_stereochemistry/inputs | a5a357d429d2... |
| phase_01_prepare_cdk2_ccne_receptor_and_standardize_ligan.md | MD | 3.2 KB | 01_pdb_cdk2_ccne_stereochemistry/reports | cad9d4bb32f4... |
| 009_dispatch_both_gnina_jobs_parallel_1_dock_prepared.py | PY | 1.0 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 1dc57c9b3d35... |
| 010_dispatch.py | PY | 705 B | 01_pdb_cdk2_ccne_stereochemistry/source | ffe9e9959f39... |
| 011_clean_up_stale_gnina_container.py | PY | 836 B | 01_pdb_cdk2_ccne_stereochemistry/source | 14466cb1f3a3... |
| 012_remove_full_container_id.py | PY | 523 B | 01_pdb_cdk2_ccne_stereochemistry/source | 78503590e479... |
| 013_time_sleep.py | PY | 599 B | 01_pdb_cdk2_ccne_stereochemistry/source | 8a76e38dba3c... |
| 014_check_what_built_functions_available_namespace.py | PY | 666 B | 01_pdb_cdk2_ccne_stereochemistry/source | d26511fce7a5... |
| 015_try_once_more_after_longer_wait_container_might_have.py | PY | 785 B | 01_pdb_cdk2_ccne_stereochemistry/source | bf9418fabaab... |
| 016_check_local_gnina_binary_cpu_fallback.py | PY | 902 B | 01_pdb_cdk2_ccne_stereochemistry/source | 0eb0a531d4f1... |
| receptor.pdbqt | PDBQT | 439.7 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 70376b623721... |
| 017_check_vina_version.py | PY | 651 B | 01_pdb_cdk2_ccne_stereochemistry/source | ee5533caf3c9... |
| ctx_ref.pdbqt | PDBQT | 3.8 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 59cb84492d51... |
| ligand.pdbqt | PDBQT | 3.8 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | c3fd48824a8d... |
| 018_prepare_ligand_pdbqt_meeko_handles_rotatable_bonds.py | PY | 1.1 KB | 01_pdb_cdk2_ccne_stereochemistry/source | df27d2d26629... |
| docked_poses.pdbqt | PDBQT | 20.1 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 9c2c8dd33d01... |
| 019_run_vina_dock_ligand_5_modes.py | PY | 671 B | 01_pdb_cdk2_ccne_stereochemistry/source | 6893c0be8b0c... |
| 020_score_ctx_crystal_pose_score_only.py | PY | 949 B | 01_pdb_cdk2_ccne_stereochemistry/source | f0d9d74afa86... |

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
