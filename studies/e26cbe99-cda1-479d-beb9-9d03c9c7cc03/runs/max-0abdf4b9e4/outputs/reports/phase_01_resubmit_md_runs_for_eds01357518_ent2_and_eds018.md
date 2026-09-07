---
title: "Phase 1: Resubmit MD runs for EDS01357518_ent2 and EDS01806218_ent1"
study_id: "e26cbe99-cda1-479d-beb9-9d03c9c7cc03"
run_id: "max-75e964e6b5"
phase_index: 1
phase_id: "1"
phase_goal: "Resubmit MD runs for EDS01357518_ent2 and EDS01806218_ent1"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Resubmit MD runs for EDS01357518_ent2 and EDS01806218_ent1

## Summary

This phase set out to resubmit MD runs for EDS01357518_ent2 and EDS01806218_ent1. It completed 1 method step, 519 output files.

## Objective

Resubmit MD runs for EDS01357518_ent2 and EDS01806218_ent1

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

#### 1. Molecular dynamics simulation of protein-ligand complexes

Energy minimisation, NPT equilibration, and NPT production MD simulations were performed on two protein-ligand complexes (CRBN-EDS01357518_ent2 and CRBN-EDS01806218_ent1) using GROMACS 2026.1-mpi with GPU acceleration.

**Rationale.** MD simulation allows characterisation of the dynamic behaviour and stability of protein-ligand complexes at physiological conditions.

| Field | Value |
| :--- | :--- |
| Inputs | em.mdp, npt_eq.mdp, prod.mdp, complex.gro, complex.top, index.ndx |
| Outputs | em.gro, npt_eq.gro, npt_prod.gro, npt_prod.xtc, npt_prod.edr |
| Status | running |

Parameters:

```yaml
nonbonded_scheme: gpu
omp_threads: 8
pme_scheme_em: cpu
pme_scheme_equilibration: gpu
pme_scheme_production: gpu
```

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| enantio.sdf | SDF | 5.9 KB | uploads | 5290a1ce4a42... |
| 001_chem_sdmolsupplier.py | PY | 714 B | 01_generate_enantiomers_and_3d_conformers_for_enant/source | 0c2f2a28995f... |
| 002_create_enantiomer.py | PY | 1.5 KB | 01_generate_enantiomers_and_3d_conformers_for_enant/source | b6b073f4a6ea... |
| enantio_structure.sdf | SDF | 21.2 KB | 01_generate_enantiomers_and_3d_conformers_for_enant/structures | 2ba43665d84f... |
| 003_create_enantiomer.py | PY | 3.2 KB | 01_generate_enantiomers_and_3d_conformers_for_enant/source | dec2247e2c13... |
| phase_01_generate_enantiomers_and_3d_conformers_for_enant.md | MD | 2.3 KB | reports | de469b127c7d... |
| phase_enantiomer_conformers.md | MD | 3.2 KB | reports | b8e18432fd29... |
| 004_center.py | PY | 1.4 KB | source | b9bd3077df4c... |
| PB-20260903-4CI2_raw.pdb | PDB | 1.8 MB | 01_phase_1_protein_preparation_4ci2/inputs | c2902e096995... |
| 005_download_pdb_4ci2_inspect.py | PY | 1.3 KB | 01_phase_1_protein_preparation_4ci2/source | 3586b38d1b53... |
| 006_extract_lvy_lenalidomide_coordinates_pocket_centre.py | PY | 1.3 KB | 01_phase_1_protein_preparation_4ci2/source | 40b5dc0aeb55... |
| 007_confirm_all_missing_residues_his_tag_linker_there.py | PY | 1013 B | 01_phase_1_protein_preparation_4ci2/source | 83c8afb2fdea... |
| 008_re_parse_remark_465_directly_raw_pdb_lines.py | PY | 1.4 KB | 01_phase_1_protein_preparation_4ci2/inputs | a2ee0a77648f... |
| 009_full_missing_residue_list_chain_b.py | PY | 390 B | 01_phase_1_protein_preparation_4ci2/source | 355707be62e1... |
| 010_phase_1_launch_pdbfixer.py | PY | 1.1 KB | 01_phase_1_protein_preparation_4ci2/source | 6fa03be03dc2... |
| PB-20260903-4CI2_receptor.pdb | PDB | 1.9 MB | 01_phase_1_protein_preparation_4ci2/structures | 3631479233d0... |
| 011_phase_1_pdbfixer_process.py | PY | 2.0 KB | 01_phase_1_protein_preparation_4ci2/source | af54284430f9... |
| PB-20260903-4CI2_receptor_noH.pdb | PDB | 950.4 KB | 01_phase_1_protein_preparation_4ci2/structures | 79dde47e3da6... |
| 012_1_strip_h_receptor_fpocket.py | PY | 1.3 KB | 01_phase_1_protein_preparation_4ci2/source | 90d994b8f7ce... |
| 013_fpocket.py | PY | 1.0 KB | 01_phase_1_protein_preparation_4ci2/source | f90e6433de4e... |
| 014_pocket_characterisation_crystal_structure_pocket.py | PY | 3.0 KB | 01_phase_1_protein_preparation_4ci2/source | 99bbbcc5cc24... |
| protonation-state-results-2.json | JSON | 721 B | 01_phase_1_protein_preparation_4ci2/results | 690f3e56a4cf... |
| protonation-state-results-3.json | JSON | 751 B | 01_phase_1_protein_preparation_4ci2/results | 8daaaef9b18d... |
| protonation-state-results-4.json | JSON | 751 B | 01_phase_1_protein_preparation_4ci2/results | 4e5b545bcb6f... |
| protonation-state-results-5.json | JSON | 667 B | 01_phase_1_protein_preparation_4ci2/results | d7a54b495e8d... |
| protonation-state-results.json | JSON | 715 B | 01_phase_1_protein_preparation_4ci2/results | 4faf406c9adb... |
| 015_protonate_each_ligand_ph_7_4_via_dimorphite_dl.py | PY | 1.1 KB | 01_phase_1_protein_preparation_4ci2/source | 9f08f258fecd... |
| phase_01_phase_1_protein_preparation_4ci2.md | MD | 4.2 KB | 02_phase_2_ligand_preparation/reports | 921c9208f34c... |
| phase_02_phase_2_ligand_preparation.md | MD | 4.2 KB | 03_phase_3_docking_with_gnina_gpu/reports | b5c7fdfc7633... |
| lig_EDS01357518_ent1.sdf | SDF | 4.0 KB | 03_phase_3_docking_with_gnina_gpu/structures | 7c163a87c75f... |
| lig_EDS01357518_ent2.sdf | SDF | 4.0 KB | 03_phase_3_docking_with_gnina_gpu/structures | eb333c89f6c1... |
| lig_EDS01806218_ent1.sdf | SDF | 4.0 KB | 03_phase_3_docking_with_gnina_gpu/structures | 502fb30921be... |
| lig_EDS01806218_ent2.sdf | SDF | 4.0 KB | 03_phase_3_docking_with_gnina_gpu/structures | 8b1caed717ec... |
| lig_EDS01889984.sdf | SDF | 5.1 KB | 03_phase_3_docking_with_gnina_gpu/structures | 55bc31350849... |
| 016_split_enantio_structure_sdf_into_per_ligand_sdf.py | PY | 890 B | 03_phase_3_docking_with_gnina_gpu/source | 3cf652ca28ce... |
| PB-20260903-4CI2_receptor_trimmed.pdb | PDB | 179.1 KB | 03_phase_3_docking_with_gnina_gpu/structures | c22bb3cf89c2... |
| PB-20260903-4CI2_receptor_trimmed_noH.pdb | PDB | 90.4 KB | 03_phase_3_docking_with_gnina_gpu/structures | 44098f0ec487... |
| 017_trim_receptor_residues_within_20_pocket_centre.py | PY | 2.0 KB | 03_phase_3_docking_with_gnina_gpu/source | e64e59141c84... |
| 018_dock_all_5_ligands_gnina_gpu_top_5_poses_each.py | PY | 1.9 KB | 03_phase_3_docking_with_gnina_gpu/source | dfcb2613ed19... |
| 019_check_gnina_vina_binaries_path.py | PY | 1.5 KB | 03_phase_3_docking_with_gnina_gpu/source | d279167aa713... |
| gnina_docked.sdf.gz | GZ | 2.9 KB | 03_phase_3_docking_with_gnina_gpu/structures | 3399ca3ce8b8... |
| 020_check_converters.py | PY | 1.8 KB | 03_phase_3_docking_with_gnina_gpu/source | f593cf5e3bab... |
| 021_inspect_r_gnina_result_dict.py | PY | 1.4 KB | 03_phase_3_docking_with_gnina_gpu/source | 57d0c24a2504... |
| docked_EDS01357518_ent1.sdf.gz | GZ | 2.9 KB | 03_phase_3_docking_with_gnina_gpu/structures | 3399ca3ce8b8... |
| docked_EDS01357518_ent2.sdf.gz | GZ | 2.8 KB | 03_phase_3_docking_with_gnina_gpu/structures | 9995bc3bbb5e... |
| docked_EDS01806218_ent1.sdf.gz | GZ | 2.8 KB | 03_phase_3_docking_with_gnina_gpu/structures | 326c13253b29... |
| docked_EDS01806218_ent2.sdf.gz | GZ | 2.9 KB | 03_phase_3_docking_with_gnina_gpu/structures | 71a9ef9568c6... |
| docked_EDS01889984.sdf.gz | GZ | 2.9 KB | 03_phase_3_docking_with_gnina_gpu/structures | fda0b1994322... |
| gnina_docked.sdf.gz | GZ | 2.9 KB | 03_phase_3_docking_with_gnina_gpu/structures | fda0b1994322... |
| 022_read_gnina_gz.py | PY | 2.3 KB | 03_phase_3_docking_with_gnina_gpu/source | cab97949a6dd... |
| phase_03_phase_3_docking_with_gnina_gpu.md | MD | 6.8 KB | 04_phase_4_mm_gbsa_free_binding_energies/reports | 9114929dad6b... |
| poses_EDS01357518_ent1.sdf | SDF | 15.9 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | 91f8323f447f... |
| poses_EDS01357518_ent2.sdf | SDF | 15.9 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | a6233d55b8a1... |
| poses_EDS01806218_ent1.sdf | SDF | 16.1 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | 1c19b6a9e08d... |
| poses_EDS01806218_ent2.sdf | SDF | 16.1 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | fc30343d6557... |
| poses_EDS01889984.sdf | SDF | 16.0 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | ac77f4c03d1f... |
| 023_write_combined_poses_sdf_best_pose_complex_pdb_per.py | PY | 2.5 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | 6daea2f63a84... |
| 024_test_openmmforcefields_gaff2_rdkit.py | PY | 1.4 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | 750e4608b0b7... |
| 025_print.py | PY | 542 B | 04_phase_4_mm_gbsa_free_binding_energies/source | 28ed2e3865a3... |
| 026_test_gafftemplategenerator_rdkit_mol.py | PY | 1.3 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | 7fdc3dfd8864... |
| 027_check_antechamber.py | PY | 2.0 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | 397b9593ed4a... |
| 029_wrapper.csv | CSV | 265 B | 04_phase_4_mm_gbsa_free_binding_energies/tables | 82c5d4139067... |
| 028_wrapper.py | PY | 2.7 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | f03ada21f351... |
| 029_redefine_wrapper_cannot_persist_across_calls.py | PY | 3.7 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | e278b4956461... |
| PB-20260903-4CI2_receptor_trimmed_fixed.pdb | PDB | 179.1 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | ab7bb242d3d5... |
| 030_fix_trimmed_receptor_pdb_remove_ter_records_have_no.py | PY | 1.4 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | d086a1dff4d1... |
| 031_helpers.py | PY | 3.5 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | 1b626a1823fb... |
| PB-20260903-4CI2_receptor_trimmed_noH_fixed.pdb | PDB | 90.3 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | 161f31b63e4d... |
| 032_init.py | PY | 3.9 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | ee05c625aadd... |
| PB-20260903-4CI2_receptor_trimmed_capped.pdb | PDB | 179.3 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | ed7a0bcd974e... |
| 033_print.py | PY | 3.8 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | ba0f768b1372... |
| 034_init.py | PY | 5.7 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | e28e25d75751... |
| lig_pose_EDS01357518_ent1.pdb | PDB | 6.8 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | 68e71132d55e... |
| lig_pose_EDS01357518_ent2.pdb | PDB | 6.8 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | 868d968f7fa2... |
| lig_pose_EDS01806218_ent1.pdb | PDB | 6.9 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | f3fa6c98bb8b... |
| lig_pose_EDS01806218_ent2.pdb | PDB | 6.9 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | 1acc17295fd1... |
| lig_pose_EDS01889984.pdb | PDB | 6.9 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | d49a34bdb981... |
| 035_init.py | PY | 5.3 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | f9e3158d2e09... |
| 036_init.py | PY | 4.5 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | e697910f4406... |
| complex_EDS01357518_ent1.pdb | PDB | 181.9 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | f8b0fd7105c0... |
| complex_EDS01357518_ent2.pdb | PDB | 181.9 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | d6ea5359a48b... |
| complex_EDS01806218_ent1.pdb | PDB | 181.9 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | ba96dffa4133... |
| complex_EDS01806218_ent2.pdb | PDB | 181.9 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | 7f1312f4085c... |
| complex_EDS01889984.pdb | PDB | 181.9 KB | 04_phase_4_mm_gbsa_free_binding_energies/structures | 8379c284f0b4... |
| 037_generate_protein_ligand_complex_pdb_files_5_best.py | PY | 2.7 KB | 04_phase_4_mm_gbsa_free_binding_energies/source | 67f98fcca7d3... |
| phase_04_phase_4_mm_gbsa_free_binding_energies.md | MD | 10.9 KB | 05_phase_5_report/reports | 60558b3569f0... |
| 038_compute_key_contacts_residues_within_4_5_each_best.py | PY | 2.1 KB | 05_phase_5_report/source | 9d09b3be5e55... |
| final_results.json | JSON | 711 B | 05_phase_5_report/work | 3b8d1688fb05... |
| 039_build_concise_summary_dict_report_writer.py | PY | 1.2 KB | 05_phase_5_report/source | c52d17e04386... |
| phase_04_docking_and_binding_energies_final_report.md | MD | 10.0 KB | reports | 51f04e950879... |
| 040_close_phase_5_final_report_document.py | PY | 1.8 KB | 05_phase_5_report/source | a5427adc7690... |
| phase_05_phase_5_report.md | MD | 11.3 KB | reports | cb8ff2b5d3f4... |
| phase_01_protein_preparation_4ci2_document.md | MD | 4.0 KB | reports | e630d1b8284e... |
| 041_phase_1_audit_protein_preparation.py | PY | 1.7 KB | source | 38798d4546ae... |
| audit_all_phases.md | MD | 5.3 KB | reports | 6b6fa725f768... |
| 042_open.py | PY | 1.1 KB | 01_build_interactive_docking_viewer_html/source | dbd3a89e489b... |
| 043_open.py | PY | 2.5 KB | 01_build_interactive_docking_viewer_html/source | e1a2a453a8f0... |
| docking_viewer.html | HTML | 275.8 KB | 01_build_interactive_docking_viewer_html/reports | f36452908cc3... |
| 044_js_str.py | PY | 16.6 KB | 01_build_interactive_docking_viewer_html/source | fd177a63b32c... |
| docking_viewer.html | HTML | 275.6 KB | 01_build_interactive_docking_viewer_html/reports | 6677259fbe7a... |
| 045_fix_two_issues_generated_html_1_addlabel_must_use_3.py | PY | 1.9 KB | 01_build_interactive_docking_viewer_html/source | 2cbe8e4efc1e... |
| phase_01_build_interactive_docking_viewer_html.md | MD | 2.4 KB | reports | abf393d4e2c1... |
| 046_os_path_getsize.py | PY | 1.8 KB | source | e3c7c50b335d... |
| 047_crbn.py | PY | 3.3 KB | source | 52e4521020a9... |
| crystal_lvy.pdb | PDB | 1.5 KB | 01_add_crystal_ligand_lvy_to_docking_viewer/structures | beb48c77927a... |
| 048_open.py | PY | 980 B | 01_add_crystal_ligand_lvy_to_docking_viewer/source | 2757936095cb... |
| docking_viewer.html | HTML | 278.3 KB | 01_add_crystal_ligand_lvy_to_docking_viewer/reports | dd305ceaf680... |
| 049_js_str.py | PY | 3.8 KB | 01_add_crystal_ligand_lvy_to_docking_viewer/source | 1386eba5ab89... |
| 050_open.py | PY | 4.3 KB | 01_add_crystal_ligand_lvy_to_docking_viewer/source | 60a9bde6c3ed... |
| phase_01_add_crystal_ligand_lvy_to_docking_viewer.md | MD | 2.3 KB | reports | 15f4296795d8... |
| docking_viewer.html | HTML | 279.7 KB | reports | de44b1418344... |
| audit_add_crystal_lvy.md | MD | 5.0 KB | reports | 8342023fa1fc... |
| 051_open.py | PY | 2.4 KB | source | 92de2bf363df... |
| audit_add_crystal_lvy.md | MD | 10.3 KB | reports | b7134b9f8abf... |
| phase_02_task_a8485ebdc3d70decb.md | MD | 2.5 KB | 03_update_viewer_with_dynamic_per_ligand_contact_re/reports | e7d2968b6336... |
| 052_build_contacts_js_object.py | PY | 2.0 KB | 03_update_viewer_with_dynamic_per_ligand_contact_re/source | 6b7bffd82ff8... |
| docking_viewer.html | HTML | 286.0 KB | 03_update_viewer_with_dynamic_per_ligand_contact_re/reports | f678849839f5... |
| 053_open.py | PY | 7.2 KB | 03_update_viewer_with_dynamic_per_ligand_contact_re/source | b6c08d1929a8... |
| 054_os_path_getsize.py | PY | 3.5 KB | 03_update_viewer_with_dynamic_per_ligand_contact_re/source | 25a558be214d... |
| phase_03_update_viewer_with_dynamic_per_ligand_contact_re.md | MD | 3.3 KB | reports | 51ca77d65aaa... |
| audit_add_crystal_lvy.md | MD | 10.3 KB | reports | 2ffa8fcd910c... |
| 055_audit_add_crystal_ligand_lvy_docking_viewer_phase.py | PY | 1.0 KB | source | 0e7424e07813... |
| 056_audit_independent_auditor_subagent_phase_task.py | PY | 933 B | source | 8d124545531c... |
| 057_open.py | PY | 2.6 KB | source | 19593d3e9749... |
| 058_atoms.py | PY | 2.1 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | da291be3fc6e... |
| 059_ring_centroid_normal.py | PY | 3.4 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | 24a6a0e926c9... |
| 060_crystal_lvy_interactions.py | PY | 2.9 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | 60d88031f3a0... |
| 061_build_interactions_js_constant.py | PY | 1.1 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | 0e73e3f72e6a... |
| 062_open.py | PY | 1.0 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | 571a4ab705e2... |
| 063_find_end_rebuildscene_look_final_render_closing.py | PY | 762 B | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | 4fb9fa5196b7... |
| 064_find_actual_btn_crystal_button_html_not_comment.py | PY | 706 B | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | a2adda8d96e5... |
| 065_js_str.py | PY | 2.9 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | 814c26518f5f... |
| 066_verify_each_insertion_point_unique.py | PY | 860 B | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | 295a159dd291... |
| 067_h2_replace.py | PY | 2.6 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | 654cf7cdb4f2... |
| docking_viewer.html | HTML | 292.1 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/reports | 0b41daf53f89... |
| 068_open.py | PY | 1.3 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | 595fb79718f9... |
| phase_01_add_interaction_lines_hbond_pistack.md | MD | 3.6 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/reports | e219564debaa... |
| 069_lines.py | PY | 3.8 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/source | 1890e9dcb61b... |
| audit_add_interactions.md | MD | 2.9 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/reports | bd609bf6fd3a... |
| phase_02_task_a509223b32b97a0c2.md | MD | 3.5 KB | 01_add_interaction_lines_h_bonds_pi_stacking_to_vie/reports | ee82b5f9367c... |
| phase_01_add_interaction_lines_h_bonds_pi_stacking_to_vie.md | MD | 3.8 KB | reports | 794fffba18ff... |
| phase_03_task_a3ba35eec6910be35.md | MD | 3.7 KB | reports | a5e7997440b6... |
| 070_importlib_import_module.py | PY | 583 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 193d233a354d... |
| 071_subprocess_run.py | PY | 972 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | d004c35b1f74... |
| 072_check_ambertools_executables_available.py | PY | 768 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | e2f49087deab... |
| ligand_best.sdf | SDF | 3.2 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | dabb1167a7a9... |
| 073_os_makedirs.py | PY | 1.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 985fb2d65ba2... |
| ligand.mol2 | MOL2 | 6.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | edde8ac71d44... |
| ligand_h.sdf | SDF | 5.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 6f4caed70626... |
| sqm.in | IN | 3.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 27e40d997b18... |
| sqm.out | OUT | 15.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | c85ac3299bfa... |
| sqm.pdb | PDB | 4.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | fc0e0355f663... |
| 074_add_explicit_hydrogens_write_proper_3d_sdf.py | PY | 1.2 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | d70c486d40b9... |
| ligand.frcmod | FRCMOD | 5.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 123185a015ca... |
| receptor_tleap.pdb | PDB | 90.2 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | d0d8c0a30887... |
| 075_parmchk2_generate_missing_gaff2_parameters.py | PY | 1.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 6c9bf5cb40d0... |
| complex.inpcrd | INPCRD | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 18f0c151bf41... |
| complex.prmtop | PRMTOP | 5.1 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | c18f1c1e650a... |
| complex_solvated.pdb | PDB | 2.3 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 0c9297d31c05... |
| leap.log | LOG | 27.2 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 7e70de8d2f62... |
| tleap.in | IN | 1000 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 5e5de02acae0... |
| 076_write_tleap_input_script.py | PY | 1.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/inputs | 3e31feccafb5... |
| 077_convert_amber_topology_gromacs.py | PY | 826 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | ebd589283fb1... |
| complex.gro | GRO | 1.3 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 7ff8165e714b... |
| complex.top | TOP | 1.2 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 0dcada7cb2f2... |
| run_parmed.py | PY | 735 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 8e0f117541dd... |
| 078_write_standalone_parmed_conversion_script.py | PY | 1.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | b9ded2bc5495... |
| em.mdp | MDP | 301 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 82c2d9778e64... |
| index.ndx | NDX | 675.5 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 4f1f4eec3645... |
| npt_eq.mdp | MDP | 787 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 6e0005b4afc3... |
| prod.mdp | MDP | 770 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 50c534d3f17b... |
| 079_write_gromacs_mdp_files.py | PY | 2.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | eb7274d9c304... |
| #index.ndx.1# | 1# | 675.5 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 4f1f4eec3645... |
| em.tpr | TPR | 921.2 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 42ec10ee8b90... |
| index.ndx | NDX | 837.2 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | feb1fa998e22... |
| mdout.mdp | MDP | 11.4 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | df30e3057a59... |
| 080_create_custom_index_protein_lig_water_ions.py | PY | 1.5 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | af47b57f3978... |
| 081_verify_all_files_stage_exist_get_sizes.py | PY | 560 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 861761b21d24... |
| 082_check_analysis_tools_post_md_mm_gbsa.py | PY | 1.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 06a48ec00239... |
| test_cpptraj.in | IN | 262 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 1046e35d92a7... |
| 083_check_what_cpptraj_supports_mmpbsa.py | PY | 1.0 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 9b3a0867be19... |
| 084_run_ante_mmpbsa_py_create_stripped_prmtop_files_s.py | PY | 1.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 846aca363e2f... |
| complex_nowater.prmtop | PRMTOP | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | e90329c17cc8... |
| ligand.prmtop | PRMTOP | 52.0 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 6704e7351d7d... |
| receptor.prmtop | PRMTOP | 995.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | b2bc7b66cd22... |
| 085_set_amberhome_conda_env_root.py | PY | 859 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 63cc2f6b4146... |
| cpptraj_strip.in | IN | 436 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 02ffe00bb3b3... |
| mmpbsa.in | IN | 460 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | eb756f44e93a... |
| run_mmpbsa.sh | SH | 710 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 54c76cf91f7d... |
| 086_mmpbsa_input_file.py | PY | 2.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/inputs | 3acfda20fede... |
| phase_md_10ns_EDS01806218_ent2.md | MD | 6.2 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/reports | 34ce42afbb2a... |
| 087_ai_hpc.py | PY | 6.5 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | d6c04d299abb... |
| 089_open.csv | CSV | 250 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/tables | 130e0f9cbad1... |
| 088_open.py | PY | 1.2 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | d34e926f1f68... |
| complex.inpcrd | INPCRD | 82.9 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 656c2fd5b9be... |
| complex.prmtop | PRMTOP | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | a39fa642f247... |
| leap.log | LOG | 14.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | c7e15f7d7166... |
| lig.frcmod | FRCMOD | 4.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | be42d8dffc25... |
| lig.mol2 | MOL2 | 6.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 0cab9a59dbbc... |
| lig_h.sdf | SDF | 5.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | cf03a4aaa419... |
| sqm.in | IN | 3.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 5053735be8db... |
| sqm.out | OUT | 16.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 9180a273670c... |
| sqm.pdb | PDB | 4.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | c463fc0c5479... |
| tleap.in | IN | 726 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | f44fa42d3561... |
| complex.inpcrd | INPCRD | 82.9 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 5629fcd73e3e... |
| complex.prmtop | PRMTOP | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 5010d47be6ad... |
| leap.log | LOG | 14.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | f1a7a06f1820... |
| lig.frcmod | FRCMOD | 4.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | be42d8dffc25... |
| lig.mol2 | MOL2 | 6.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | dfef3e75129f... |
| lig_h.sdf | SDF | 5.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 08d4886d4929... |
| sqm.in | IN | 3.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 8796afab56f6... |
| sqm.out | OUT | 16.4 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 72771913d08a... |
| sqm.pdb | PDB | 4.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | bbee33717e87... |
| tleap.in | IN | 726 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 3db43434450b... |
| complex.inpcrd | INPCRD | 82.9 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 23fb2baac658... |
| complex.prmtop | PRMTOP | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 71d83c08a7f0... |
| leap.log | LOG | 15.2 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 2346a5722f65... |
| lig.frcmod | FRCMOD | 5.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 38504d025076... |
| lig.mol2 | MOL2 | 6.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 35d1c6b12a67... |
| lig_h.sdf | SDF | 5.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | b3392c44c358... |
| sqm.in | IN | 3.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | d64b7b0ecea7... |
| sqm.out | OUT | 15.4 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 4dd4bf813586... |
| sqm.pdb | PDB | 4.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | a097155e90ae... |
| tleap.in | IN | 726 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | baceedad0cda... |
| complex.inpcrd | INPCRD | 82.9 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 434c967308c6... |
| complex.prmtop | PRMTOP | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 0004c0f0c201... |
| leap.log | LOG | 15.2 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | a66dc3bb6111... |
| lig.frcmod | FRCMOD | 5.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 38504d025076... |
| lig.mol2 | MOL2 | 6.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | dd488eb02463... |
| lig_h.sdf | SDF | 5.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 86dac6ff3c57... |
| sqm.in | IN | 3.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 32bce9661d7a... |
| sqm.out | OUT | 15.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 00cd332c4875... |
| sqm.pdb | PDB | 4.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | f4be21c4d330... |
| tleap.in | IN | 726 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 8f9c2ebc85dd... |
| complex.inpcrd | INPCRD | 82.9 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 49ac7107c762... |
| complex.prmtop | PRMTOP | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 0fd2c17680ea... |
| leap.log | LOG | 14.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 29b5427aef1c... |
| lig.frcmod | FRCMOD | 5.0 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 3c09f6ec2814... |
| lig.mol2 | MOL2 | 6.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 9ea51ed7780f... |
| lig_h.sdf | SDF | 5.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 36d2c5a3631c... |
| sqm.in | IN | 3.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | ce32237b2542... |
| sqm.out | OUT | 16.0 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 44a5125d6c44... |
| sqm.pdb | PDB | 4.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | fc007569c5db... |
| tleap.in | IN | 706 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 1b8462593c65... |
| 090_os_makedirs.csv | CSV | 270 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/tables | 393ea502aab3... |
| 089_os_makedirs.py | PY | 2.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | c440b869cec6... |
| 090_subprocess_run.py | PY | 984 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 416fe03f9ae3... |
| 091_subprocess_run.py | PY | 263 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 8d95ba9dafe0... |
| cpptraj_single.in | IN | 378 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 789219b3d29f... |
| lig.prmtop | PRMTOP | 48.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | f1df75064316... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | b70a9bc462ef... |
| cpptraj_single.in | IN | 378 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 99ab21c33028... |
| lig.prmtop | PRMTOP | 48.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 7703c439d007... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 52b1301b339e... |
| cpptraj_single.in | IN | 378 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 870934f3d3e1... |
| lig.prmtop | PRMTOP | 49.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 138bfeffd97b... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 8e643f91123a... |
| cpptraj_single.in | IN | 378 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 3d510f30139e... |
| lig.prmtop | PRMTOP | 49.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 14d55db7a696... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | c3709908ef85... |
| cpptraj_single.in | IN | 363 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 3cb6046f885f... |
| lig.prmtop | PRMTOP | 52.5 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 3d0042d4360d... |
| rec.prmtop | PRMTOP | 995.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | ef93d8252ae6... |
| 092_subprocess_run.py | PY | 922 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | b62840c2831d... |
| 093_open.py | PY | 1.2 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 4e5affdbbdf6... |
| 094_print.py | PY | 148 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 5bc05869a474... |
| cpptraj_single.in | IN | 382 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 11fca66d202c... |
| mmpbsa_single.in | IN | 122 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 1040577e9df6... |
| single.nc | NC | 27.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | d29df1e2245d... |
| cpptraj_single.in | IN | 382 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 746d4bc36138... |
| mmpbsa_single.in | IN | 122 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 1040577e9df6... |
| single.nc | NC | 27.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 2079d19f4cf9... |
| cpptraj_single.in | IN | 382 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 8db1420b2211... |
| mmpbsa_single.in | IN | 122 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 1040577e9df6... |
| single.nc | NC | 27.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 3b89d177513c... |
| cpptraj_single.in | IN | 382 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | a55a2b6ba587... |
| mmpbsa_single.in | IN | 122 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 1040577e9df6... |
| single.nc | NC | 27.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 41417c21d569... |
| cpptraj_single.in | IN | 367 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 0ea16f19bf49... |
| mmpbsa_single.in | IN | 122 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 1040577e9df6... |
| single.nc | NC | 27.7 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 896da56d8804... |
| 095_open.py | PY | 2.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 08a8dafb604d... |
| 096_subprocess_run.py | PY | 898 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 8f49df2afcdb... |
| complex.prmtop | PRMTOP | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 89b2a1671111... |
| leap.log | LOG | 28.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 931957d9083e... |
| tleap_mbondi2.in | IN | 754 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 5daf1b452a89... |
| complex.prmtop | PRMTOP | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 0cfb837915cf... |
| leap.log | LOG | 28.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 9f8d70177053... |
| tleap_mbondi2.in | IN | 754 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | e17e4292e0d1... |
| complex.prmtop | PRMTOP | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 01c993074f93... |
| leap.log | LOG | 30.4 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 7a35be89386c... |
| tleap_mbondi2.in | IN | 754 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | c2f07d150bb3... |
| complex.prmtop | PRMTOP | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | a16fba18dd67... |
| leap.log | LOG | 30.4 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | baa5c03dc133... |
| tleap_mbondi2.in | IN | 754 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 02d171ddfbd7... |
| complex.prmtop | PRMTOP | 1.0 MB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | cef3f5ea079f... |
| leap.log | LOG | 28.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 6456e50c9c5f... |
| tleap_mbondi2.in | IN | 734 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 1f06b6fba30f... |
| 097_open.py | PY | 1.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | a480c8173fbf... |
| lig.prmtop | PRMTOP | 48.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 1dbe22690fa9... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | a589af108ef7... |
| lig.prmtop | PRMTOP | 48.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 4dde7b3e3b63... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 36c1d311edb8... |
| lig.prmtop | PRMTOP | 49.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 0fe942d959ea... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 28a1915106a2... |
| lig.prmtop | PRMTOP | 49.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | a9f0619b71e2... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | e912ffb62f4e... |
| lig.prmtop | PRMTOP | 52.5 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | d30c233967d1... |
| rec.prmtop | PRMTOP | 995.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 61b5dc8c7c4d... |
| 098_os_remove.py | PY | 2.5 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 8e21025b9875... |
| lig.prmtop | PRMTOP | 48.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | b1d4b1a6fb5c... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | e940fc668528... |
| 099_os_remove.py | PY | 755 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 748759029a26... |
| lig.prmtop | PRMTOP | 48.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | ac9ae3981f5b... |
| mmgbsa_result.dat | DAT | 5.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 19de5d924988... |
| mmpbsa_single.in | IN | 87 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | c9732e52b916... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | d6533df84b56... |
| reference.frc | FRC | 487.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/inputs | 750ecebce6de... |
| lig.prmtop | PRMTOP | 48.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | d9f24a1a9052... |
| mmgbsa_result.dat | DAT | 5.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | 4b8214123c9f... |
| mmpbsa_single.in | IN | 87 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | c9732e52b916... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 8d1a2946c6c0... |
| reference.frc | FRC | 487.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/inputs | 6335e110d223... |
| lig.prmtop | PRMTOP | 49.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 9d9972c7925e... |
| mmgbsa_result.dat | DAT | 5.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | b4cb5d13b0d0... |
| mmpbsa_single.in | IN | 87 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | c9732e52b916... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 38e808fb4790... |
| reference.frc | FRC | 487.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/inputs | 1fc7b81588aa... |
| lig.prmtop | PRMTOP | 49.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | d25bb19f89e1... |
| mmgbsa_result.dat | DAT | 5.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | dff47bc1311e... |
| mmpbsa_single.in | IN | 87 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | c9732e52b916... |
| rec.prmtop | PRMTOP | 993.1 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 4ad2671b456d... |
| reference.frc | FRC | 487.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/inputs | 2ddb8f4d606f... |
| lig.prmtop | PRMTOP | 52.5 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 8152e1e1724f... |
| mmgbsa_result.dat | DAT | 5.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | bf01dab04a0b... |
| mmpbsa_single.in | IN | 87 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/work | c9732e52b916... |
| rec.prmtop | PRMTOP | 995.8 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/structures | 870d621be6a8... |
| reference.frc | FRC | 487.3 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/inputs | 0a6ead193c43... |
| 100_present.py | PY | 2.4 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 9453f693aa61... |
| 101_open.py | PY | 407 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | d12c9f1556d3... |
| 102_open.py | PY | 214 B | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 2c29e315cb3a... |
| 103_open.py | PY | 1.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/source | 5765feb2825f... |
| phase_05_binding_free_energy_summary.md | MD | 4.8 KB | reports | 8626c39f2872... |
| phase_md_10ns_EDS01806218_ent2.md | MD | 7.6 KB | 01_run_10_ns_md_simulation_of_best_ligand_crbn_pock/reports | 367515d75580... |
| slurm-6284357.log | LOG | 3.9 KB | work | cd1925ebd78c... |
| slurm-6292928.log | LOG | 3.4 KB | work | 1530601879d0... |
| slurm-6293949.log | LOG | 2.1 KB | work | 4f892d76d66f... |
| slurm-6294042.log | LOG | 3.8 KB | work | 65bc45b34b43... |
| em.gro | GRO | 1.3 MB | structures | 7af41fb61d56... |
| npt_eq.gro | GRO | 1.9 MB | structures | 3826d9fd6c73... |
| npt_prod.edr | EDR | 669.5 KB | work | 89c084828ecf... |
| npt_prod.gro | GRO | 1.9 MB | structures | 289f2e51bbc4... |
| npt_prod.xtc | XTC | 102.3 MB | work | 95628fef49cd... |
| slurm-6294174.log | LOG | 2.8 MB | work | 8d92d29e0576... |
| cpptraj_strip.in | IN | 420 B | work | 0b0e51e847b1... |
| prod_nowater.nc | NC | 26.7 MB | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/work | e90cca3b58e1... |
| 104_print.py | PY | 720 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | 6179dd88c1b2... |
| 105_print.py | PY | 773 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | 239818b07110... |
| mmpbsa.in | IN | 200 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/work | b3fad6177065... |
| _MMPBSA_gb.mdin | MDIN | 72 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/work | 272627c4eb0a... |
| 106_print.py | PY | 699 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | 20ac7d785867... |
| mmpbsa_results.dat | DAT | 5.9 KB | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/work | 181f2b38a1d5... |
| reference.frc | FRC | 94.9 MB | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/inputs | cbb6dd1c817a... |
| 107_print.py | PY | 672 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | 0bde05cdc998... |
| 108_open.py | PY | 66 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | e080aebe768f... |
| 109_open.py | PY | 566 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | 6401886d60e2... |
| phase_01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m.md | MD | 3.4 KB | reports | ecaf6b9a8df0... |
| phase_md_mmpbsa_EDS01806218_ent2.md | MD | 5.6 KB | reports | 00cbba329bc6... |
| audit_md_mmpbsa_EDS01806218_ent2.md | MD | 2.1 KB | reports | b2d23c8ef88f... |
| phase_md_mmpbsa_EDS01806218_ent2.md | MD | 5.8 KB | reports | 388cbd335480... |
| audit_md_mmpbsa_EDS01806218_ent2.md | MD | 3.0 KB | reports | 6e5c5fcfbb5e... |
| complex.gro | GRO | 1.3 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 40eed8ffb9ce... |
| complex.inpcrd | INPCRD | 1.0 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 7eb6a29684e6... |
| complex.prmtop | PRMTOP | 5.1 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 20be74324e9c... |
| complex.top | TOP | 1.2 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | da31087b7aee... |
| complex_nowater.prmtop | PRMTOP | 1022.7 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 550afbfe1821... |
| complex_solvated.pdb | PDB | 2.3 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 76110e27bee5... |
| em.tpr | TPR | 919.3 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 5c287f21552d... |
| index.ndx | NDX | 675.0 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 45b581e92cd2... |
| index_tmp.ndx | NDX | 675.0 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 45b581e92cd2... |
| leap.log | LOG | 26.3 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | e24ee6337bce... |
| ligand.frcmod | FRCMOD | 4.7 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | fec3464ca409... |
| ligand.mol2 | MOL2 | 6.6 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 64bc65e1033f... |
| ligand.prmtop | PRMTOP | 50.9 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | d7bee88d69aa... |
| ligand_h.sdf | SDF | 5.1 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 7b4e2e2dc2c6... |
| mmpbsa.in | IN | 181 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 30cc258379cf... |
| receptor.prmtop | PRMTOP | 995.9 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 4602306295d8... |
| run_parmed.py | PY | 724 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/source | 764c6a144f9a... |
| sqm.in | IN | 3.3 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | e6a8a1e52643... |
| sqm.out | OUT | 16.2 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 674b24ebbc61... |
| sqm.pdb | PDB | 4.7 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 6c4156e00d4d... |
| tleap.in | IN | 1000 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | ce836defadf3... |
| complex.gro | GRO | 1.3 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 02167fe6759c... |
| complex.inpcrd | INPCRD | 1.0 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | bd5e2aa5329c... |
| complex.prmtop | PRMTOP | 5.1 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | a6c149622d9c... |
| complex.top | TOP | 1.2 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 6533c66632c9... |
| complex_nowater.prmtop | PRMTOP | 1022.7 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 257ee695ffa5... |
| complex_solvated.pdb | PDB | 2.3 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 6ed000c8ad22... |
| em.tpr | TPR | 919.5 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 8295a5603665... |
| index.ndx | NDX | 675.4 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 50e568b9ebaa... |
| index_tmp.ndx | NDX | 675.4 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 50e568b9ebaa... |
| leap.log | LOG | 26.2 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | fd72d3506290... |
| ligand.frcmod | FRCMOD | 4.7 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | fec3464ca409... |
| ligand.mol2 | MOL2 | 6.6 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 555c48de2f6c... |
| ligand.prmtop | PRMTOP | 50.9 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 23aba1aa4e9b... |
| ligand_h.sdf | SDF | 5.1 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 1361881ba3bd... |
| mmpbsa.in | IN | 181 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 30cc258379cf... |
| receptor.prmtop | PRMTOP | 995.9 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | f120c94d72cb... |
| run_parmed.py | PY | 724 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/source | 55297fe2892b... |
| sqm.in | IN | 3.3 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 358490c1534d... |
| sqm.out | OUT | 16.4 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 29e794e29804... |
| sqm.pdb | PDB | 4.7 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 762dc568ce2d... |
| tleap.in | IN | 1000 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 4a0ecd1ea84d... |
| complex.gro | GRO | 1.3 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | ea594ab60b61... |
| complex.inpcrd | INPCRD | 1.0 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 5c48f3529fc0... |
| complex.prmtop | PRMTOP | 5.1 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 36433ab57609... |
| complex.top | TOP | 1.2 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | a54ad041741c... |
| complex_nowater.prmtop | PRMTOP | 1.0 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 7b2ffb8f78cd... |
| complex_solvated.pdb | PDB | 2.3 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 5b6fa75b8d71... |
| em.tpr | TPR | 921.0 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 54640d0cd487... |
| index.ndx | NDX | 675.2 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 61de7c140256... |
| index_tmp.ndx | NDX | 675.2 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 61de7c140256... |
| leap.log | LOG | 27.1 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | b5b49d54f49a... |
| ligand.mol2 | MOL2 | 6.6 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 603b152e8e9c... |
| ligand.prmtop | PRMTOP | 52.0 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 4ceca115283c... |
| ligand_h.sdf | SDF | 5.1 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | c6f4cb177df6... |
| mmpbsa.in | IN | 181 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 30cc258379cf... |
| receptor.prmtop | PRMTOP | 995.8 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | de0b47b71431... |
| run_parmed.py | PY | 724 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/source | 9190e922ffbc... |
| sqm.in | IN | 3.3 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | f98f7cfabe23... |
| sqm.out | OUT | 15.4 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 282e3d33f6a2... |
| sqm.pdb | PDB | 4.7 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 481353e69228... |
| tleap.in | IN | 1000 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 95173334479f... |
| complex.gro | GRO | 1.3 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 8b1c7b82163b... |
| complex.inpcrd | INPCRD | 1.0 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 3d35379eac89... |
| complex.prmtop | PRMTOP | 5.1 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 81570c7b9149... |
| complex.top | TOP | 1.2 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | a052211cdc0c... |
| complex_nowater.prmtop | PRMTOP | 1.0 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 488aab573db1... |
| complex_solvated.pdb | PDB | 2.3 MB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | fb6929b831d2... |
| em.tpr | TPR | 922.2 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 3231adb94935... |
| index.ndx | NDX | 675.0 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 45b581e92cd2... |
| index_tmp.ndx | NDX | 675.0 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 45b581e92cd2... |
| leap.log | LOG | 26.2 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 413a0591594f... |
| ligand.frcmod | FRCMOD | 5.0 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | ff1d9628527d... |
| ligand.mol2 | MOL2 | 6.6 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 68a089c18cb8... |
| ligand.prmtop | PRMTOP | 55.4 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | cd9487c35d8d... |
| ligand_h.sdf | SDF | 5.1 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | c58f6decc615... |
| mmpbsa.in | IN | 181 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 30cc258379cf... |
| receptor.prmtop | PRMTOP | 998.7 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | aac1e0d333ef... |
| run_parmed.py | PY | 704 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/source | 00c795e03eae... |
| sqm.in | IN | 3.3 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 788d1ecfba9a... |
| sqm.out | OUT | 15.9 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | dc9d043a96d3... |
| sqm.pdb | PDB | 4.7 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/structures | 2cc7fce934f8... |
| tleap.in | IN | 975 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 15377e633db5... |
| mdout.mdp | MDP | 11.4 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | ec7cf7fd3dbb... |
| 110_os_makedirs.py | PY | 10.2 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/source | ffc3cbfc07ba... |
| 111_subprocess_run.py | PY | 323 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/source | 064f959d6901... |
| #index.ndx.1# | 1# | 675.0 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 45b581e92cd2... |
| index.ndx | NDX | 836.6 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 5a4c8d351c49... |
| #index.ndx.1# | 1# | 675.4 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 50e568b9ebaa... |
| index.ndx | NDX | 837.0 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 4a9b85578e1a... |
| #index.ndx.1# | 1# | 675.2 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 61de7c140256... |
| index.ndx | NDX | 836.8 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | c2ddadf923e9... |
| #index.ndx.1# | 1# | 675.0 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 45b581e92cd2... |
| index.ndx | NDX | 836.6 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/work | 5a4c8d351c49... |
| 112_rebuild_correct_index_files_all_4_compounds_groups_1.py | PY | 855 B | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/source | 0b877e3ab54a... |
| phase_md_mmpbsa_4compounds_prep.md | MD | 5.0 KB | reports | 46099b88e146... |
| audit_md_mmpbsa_4compounds_prep.md | MD | 3.8 KB | 01_run_md_mm_gbsa_on_eds01357518_ent1_eds01357518_e/reports | cf8aff106b7b... |
| em.6300385.gro | GRO | 1.3 MB | structures | e4b3484beca1... |
| npt_eq.6300385.gro | GRO | 1.9 MB | structures | 6e830c40bbb7... |
| npt_prod.6300385.edr | EDR | 669.5 KB | work | 901c5e6525aa... |
| npt_prod.6300385.gro | GRO | 1.9 MB | structures | 5cfe7cf531ce... |
| npt_prod.6300385.xtc | XTC | 102.2 MB | work | 706fd349fbb3... |
| slurm-6300385.log | LOG | 2.9 MB | work | 258bfd536cf8... |
| slurm-6300401.log | LOG | 2.9 MB | work | 183f2a1f70ef... |
| slurm-6300420.log | LOG | 3.0 MB | work | cc954ea0655d... |
| slurm-6300478.log | LOG | 2.7 MB | work | 03605760d95b... |
| phase_md_EDS01357518_ent1.md | MD | 3.3 KB | reports | 468f0318d0ed... |
| phase_01_write_md_phase_report_for_eds01357518_ent1_job_6.md | MD | 2.4 KB | reports | b701e5b89302... |
| phase_02_task_a39d4f764a9b440e4.md | MD | 2.4 KB | reports | f06bafb7bca0... |
| em.6304913.gro | GRO | 1.3 MB | structures | 71ba058d8159... |
| npt_eq.6304913.gro | GRO | 1.9 MB | structures | 4a514c3e27e3... |
| npt_prod.6304913.edr | EDR | 669.5 KB | work | 5696063cd3d1... |
| npt_prod.6304913.gro | GRO | 1.9 MB | structures | aa4299adbd96... |
| npt_prod.6304913.xtc | XTC | 102.2 MB | work | 11fb6eb170e4... |
| slurm-6304901.log | LOG | 350.2 KB | work | 2f3631ef3f24... |
| slurm-6304910.6304901-2.log | LOG | 2.9 MB | work | faa3672f98d0... |
| slurm-6304910.6304901.log | LOG | 510.0 KB | work | 03aba3da6a1e... |
| slurm-6304910.6304913.log | LOG | 2.9 MB | work | faa3672f98d0... |
| slurm-6304910.log | LOG | 399.9 KB | work | e390cbcc8305... |
| slurm-6304913.6304901-2.log | LOG | 3.0 MB | work | 86c047092da2... |
| slurm-6304913.6304901.log | LOG | 1005.2 KB | work | 4e8a1ce68b12... |
| slurm-6304913.6304913.log | LOG | 3.0 MB | work | 86c047092da2... |
| slurm-6304913.log | LOG | 448.0 KB | work | e45f85470539... |
| phase_md_EDS01889984.md | MD | 4.9 KB | reports | 508bde2c1462... |
| cpptraj_strip.in | IN | 347 B | work | 2f9b517cf2a7... |
| cpptraj_strip.in | IN | 372 B | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/work | 6886d29a54e5... |
| prod_nowater.nc | NC | 26.7 MB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/work | b5fc1a58d54e... |
| cpptraj_strip.in | IN | 362 B | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/work | dfbeca33686c... |
| prod_nowater.nc | NC | 26.7 MB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/work | 2aa36254338a... |
| 113_open.py | PY | 1002 B | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/source | 54c1665c253a... |
| 114_run_mmpbsa.py | PY | 1.4 KB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/source | 97be2acf99ae... |
| 115_find_where_mmpbsa_py_lives_infer_amberhome.py | PY | 348 B | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/source | 1d136d97d163... |
| mmpbsa_results.dat | DAT | 5.9 KB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/work | 5a8593d16a64... |
| reference.frc | FRC | 94.9 MB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/inputs | 49ac842972f5... |
| mmpbsa_results.dat | DAT | 5.9 KB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/work | 705e25070657... |
| reference.frc | FRC | 95.0 MB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/inputs | f76dbabbd862... |
| 116_os_environ_copy.py | PY | 1.4 KB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/source | 82a64458206c... |
| 117_os_path_exists.py | PY | 1006 B | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/source | 00d1258bf6b0... |
| npt_prod_EDS01889984.edr | EDR | 669.5 KB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/work | e2c57ff9581b... |
| npt_prod_EDS01889984.gro | GRO | 1.9 MB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/structures | 1605ec1eec81... |
| npt_prod_EDS01889984.xtc | XTC | 102.2 MB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/work | a6570dff6d30... |
| slurm-6306623.log | LOG | 2.5 MB | 01_mm_gbsa_for_eds01357518_ent1_and_eds01889984/work | a12cc23d2f9c... |
| phase_mmgbsa_EDS01357518_ent1_EDS01889984.md | MD | 6.0 KB | reports | d68c344db123... |
| slurm-6307560.log | LOG | 301 B | work | b4c82133748c... |
| slurm-6307571.log | LOG | 301 B | work | f5a6d809c7e3... |
| phase_md_resubmit_EDS01357518_ent2_EDS01806218_ent1.md | MD | 3.5 KB | reports | 8ce23af8fc8b... |
| phase_mmgbsa_EDS01357518_ent1_EDS01889984.md | MD | 7.4 KB | reports | 977b5fdc57b2... |
| phase_md_resubmit_EDS01357518_ent2_EDS01806218_ent1.md | MD | 4.5 KB | reports | 2beaa95c09cf... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 519 file(s) were produced and registered, 519 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

This phase recorded no external tools or databases.
