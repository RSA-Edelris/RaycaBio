---
title: "Phase 1: Answer kinome questions and push to GitHub"
study_id: "7a39e116-e0d5-4e70-93c3-da6df54e7e1e"
run_id: "max-c495210d54"
phase_index: 1
phase_id: "1"
phase_goal: "Answer kinome questions and push to GitHub"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Answer kinome questions and push to GitHub

## Summary

This phase set out to answer kinome questions and push to GitHub. It completed 1 method step, 601 output files.

## Objective

Answer kinome questions and push to GitHub

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
| P922_Results.sdf | SDF | 2.1 KB | uploads | 299409b693e5... |
| 001_load_molecule.py | PY | 998 B | 01_generate_3d_conformers_for_pdk1_ligands_with_ena/source | f705d54b5d32... |
| 002_work_single_molecule_already_mol_add_explicit.py | PY | 1.6 KB | 01_generate_3d_conformers_for_pdk1_ligands_with_ena/source | b0b799aa4f31... |
| ligand_clean_PDK1.sdf | SDF | 5.1 KB | 01_generate_3d_conformers_for_pdk1_ligands_with_ena/structures | b62e04d09b8b... |
| 003_best_cid_38_best_energy_80_5413_mol_h_has_all_50.py | PY | 1.5 KB | 01_generate_3d_conformers_for_pdk1_ligands_with_ena/source | 991507fc79aa... |
| phase_01_generate_3d_conformers_for_pdk1_ligands_with_ena.md | MD | 2.4 KB | reports | 57356e14f0c6... |
| ligand_clean_PDK1_conformer_report.md | MD | 2.7 KB | reports | 21925abd7a73... |
| 1Z5M.pdb | PDB | 232.0 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 065a75313d20... |
| 004_fetch_1z5m_rcsb.py | PY | 1.4 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 302cede471e5... |
| 005_extract_li8_heavy_atom_coordinates_docking_box.py | PY | 1.7 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 475804f0b961... |
| 006_run_pdbfixer_build_missing_loop_ser231_asn240_add_h.py | PY | 949 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 6264d4fe0e0d... |
| protonation-state-results.json | JSON | 10.4 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/results | 603fa07f1ada... |
| 007_protonate_ligand_ph_7_4_using_dimorphite_dl_smiles.py | PY | 699 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | ece09d27d937... |
| 008_fix_pass_absolute_path_pdbfixer.py | PY | 808 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | ba8f8ecf7740... |
| 009_find_where_dispatch_looks_files_check_work.py | PY | 499 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 51c42c137ee0... |
| 1Z5M_receptor_pH7.4.pdb | PDB | 371.4 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | d55c22f5db02... |
| 010_decisions.py | PY | 2.1 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | fc5e9df04177... |
| 011_copy_ligand_work_gnina.py | PY | 1.6 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | c9dcba193bcc... |
| 012_check_if_pdbfixer_prepared_receptor_landed_artifact.py | PY | 691 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | e7e0cf41aff8... |
| 014_inspect_what_dispatch_run_aidd_tool_look_like.csv | CSV | 204 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | b8858935d88d... |
| 013_inspect_what_dispatch_run_aidd_tool_look_like.py | PY | 839 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | e516075aa288... |
| 014_dispatch.py | PY | 928 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | b5c88ee92964... |
| 015_inspect_dispatch_run_aidd_tool_properly.py | PY | 675 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | daab2a6457df... |
| gnina_docked.sdf.gz | GZ | 3.2 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | f8aae302a52a... |
| 016_dispatch.py | PY | 1.2 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 5242dc4fb8c7... |
| 017_check_full_result_dock_dict_raw_output.py | PY | 565 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/inputs | a0a70db237db... |
| 018_pull_scores_output_dict.py | PY | 1.7 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | a49728c227f4... |
| EL2003A-A2U1_all5poses.sdf | SDF | 17.7 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 4c0d7991044c... |
| pose_1.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | d5f5291c1509... |
| pose_2.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 99f92f9e248b... |
| pose_3.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | f53ae7edd9f7... |
| pose_4.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | b1dcd039a56b... |
| pose_5.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | da4ab06a0882... |
| 019_print_pose_table_without_strict_formatting.py | PY | 1.7 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 723c04c3d201... |
| 020_extract_full_score_table_sdf_properties.py | PY | 933 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 4978436009c8... |
| 021_read_raw_sdf_text_extract_properties_manually.py | PY | 260 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/inputs | 0a46b107ff21... |
| 022_parse_scores_raw_sdf_blocks.py | PY | 1.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/inputs | ace3dc309534... |
| pose_1.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 462264c82299... |
| 023_parse_scores_raw_sdf_blocks.py | PY | 1.6 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/inputs | 3d1337acd916... |
| 024_interaction_analysis_h_bonds_hydrophobic_contacts.py | PY | 3.3 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | fe4c7a0a02d6... |
| 025_interaction_frequency_statistics_across_all_5_poses.py | PY | 769 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | d616cf036dbe... |
| 026_mm_gbsa_via_openmm_implicit_solvent_ff14sb_gaff2.py | PY | 2.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | ac726cb2f158... |
| 027_check_what_s_actually_importable_openmmforcefields.py | PY | 303 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 069d8bb816ec... |
| 028_test_gafftemplategenerator_rdkit_mol_directly_no.py | PY | 612 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 260c449615a7... |
| 029_install_openff_toolkit_gafftemplategenerator_works.py | PY | 328 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 2e445be62214... |
| config.ini | INI | 252 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 5fa36870da8f... |
| pose_1.mol | MOL | 3.6 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 20cbc5b4c550... |
| 030_confirm_all_files_exist.py | PY | 1.6 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 2f8e4f92ad38... |
| clean_pose_1.sdf | SDF | 4.9 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 7c66c309c841... |
| BindingEnergy.csv | CSV | 377 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | 7b035e07a5d4... |
| Energy.csv | CSV | 344 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | 5cb684abc572... |
| clean_pose_1.mol | MOL | 5.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 822c5eef9f10... |
| complex.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 7943975c038f... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_receptor_prep_docking/work | 69c22607e9fc... |
| complex_reres.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 4503e186b802... |
| index.ndx | NDX | 151.2 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/work | 2a2d78b61922... |
| config.ini | INI | 252 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 09dac26d3377... |
| 031_create_clean_minimal_sdf_files_gbsa_no_extra.py | PY | 1.7 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 4879fe80b2fc... |
| BindingEnergy.csv | CSV | 701 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | b859d8fc6085... |
| Dec.csv | CSV | 1.7 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | 540dfa8a5655... |
| Energy.csv | CSV | 337 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | 40077cf65dd4... |
| clean_pose_1.mol | MOL | 5.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | ef8996d7adbb... |
| complex.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 0cfbbba3f67b... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_receptor_prep_docking/work | d23faf5aa6d1... |
| complex_reres.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | b00b1c3d4aa6... |
| clean_pose_2.mol | MOL | 0 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | e3b0c44298fc... |
| clean_pose_3.mol | MOL | 0 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | e3b0c44298fc... |
| clean_pose_4.mol | MOL | 0 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | e3b0c44298fc... |
| clean_pose_5.mol | MOL | 0 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | e3b0c44298fc... |
| 032_stage_all_5_clean_poses_receptor.py | PY | 1.3 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 388b348b3029... |
| 033_check_what_csv_files_available.py | PY | 539 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | b84a590f89d3... |
| 034_store_all_results.py | PY | 2.7 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 004de8bdf44c... |
| 035_read_raw_clean_pose_files_compare.py | PY | 1.2 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/inputs | 6dbca9466076... |
| clean_pose_1.sdf | SDF | 4.9 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 501fd256ca40... |
| clean_pose_2.sdf | SDF | 4.9 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 1bbf10a510f4... |
| clean_pose_3.sdf | SDF | 4.9 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 9a2d1cd3ec2d... |
| clean_pose_4.sdf | SDF | 4.9 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 41d0c0f61795... |
| clean_pose_5.sdf | SDF | 4.9 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 13ee7632606e... |
| 036_re_read_gnina_docked_sdf_art.py | PY | 1.9 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | e8f508acbb50... |
| BindingEnergy.csv | CSV | 368 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | 2dd4b713ff68... |
| Dec.csv | CSV | 1.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | 4ff2e03372af... |
| Energy.csv | CSV | 347 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | bdff1dc26b10... |
| clean_pose_2.mol | MOL | 5.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | d4e2bf0627b7... |
| complex.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 88067fde5c9d... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_receptor_prep_docking/work | c3233c30109b... |
| complex_reres.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 001bef6e7343... |
| Dec.csv | CSV | 2.0 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | 65598a7d78d2... |
| Energy.csv | CSV | 345 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | 80f8d76e5d69... |
| clean_pose_3.mol | MOL | 5.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 141ad9c69050... |
| complex.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 4f35ee3e6eb6... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_receptor_prep_docking/work | 3d6726d7f1cf... |
| complex_reres.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | d3ac8ffa08a0... |
| Dec.csv | CSV | 1.9 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | 49c2cbcec4db... |
| Energy.csv | CSV | 347 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | 1ab2b38dd93c... |
| clean_pose_4.mol | MOL | 5.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 24fd3500c4fd... |
| complex.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 4875fae890ee... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_receptor_prep_docking/work | 959b18b1b796... |
| complex_reres.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | dfdc22311fa7... |
| Dec.csv | CSV | 2.0 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | d8881c3994a3... |
| Energy.csv | CSV | 341 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/tables | 8a1ef2cb3639... |
| clean_pose_5.mol | MOL | 5.5 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | cd746b047ef4... |
| complex.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 4d1e3bd5f489... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_receptor_prep_docking/work | 6ddd0eb1c269... |
| complex_reres.pdb | PDB | 366.8 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/structures | 99f42c8046d7... |
| 037_range.py | PY | 2.1 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 96588fe822f5... |
| 038_full_mm_gbsa_table_pose_1_earlier_run_stored_gbsa.py | PY | 599 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 23be40e44bf1... |
| 039_check_if_interaction_data_still_scope_earlier.py | PY | 267 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 49491579841a... |
| 040_inspect_per_pose_interaction_details.py | PY | 269 B | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 777653aeb4e3... |
| 041_assemble_complete_data_summary_report.py | PY | 1.3 KB | 01_full_pdk1_docking_campaign_receptor_prep_docking/source | 53f865892069... |
| PDK1_docking_report.md | MD | 9.7 KB | reports | d51bc3093d41... |
| phase_01_full_pdk1_docking_campaign_receptor_prep_docking.md | MD | 14.6 KB | reports | 46b87c6dd72f... |
| phase_01_full_pdk1_docking_campaign.md | MD | 5.2 KB | reports | 892a6a298714... |
| P922_Results_2.sdf | SDF | 9.7 KB | uploads | a970665e5403... |
| 042_chem_sdmolsupplier.py | PY | 1.1 KB | 01_3d_conformer_generation_for_p922_results_2_sdf_5/source | f4333796140b... |
| ligand_clean_PDK1.sdf | SDF | 0 B | 01_3d_conformer_generation_for_p922_results_2_sdf_5/structures | e3b0c44298fc... |
| 043_best_3d_conformer.py | PY | 2.6 KB | 01_3d_conformer_generation_for_p922_results_2_sdf_5/source | 1bcd25cad100... |
| ligand_clean_PDK1.sdf | SDF | 27.3 KB | 01_3d_conformer_generation_for_p922_results_2_sdf_5/structures | 77751bcccee6... |
| 044_re_define_conformer_function_lost_between_calls.py | PY | 2.6 KB | 01_3d_conformer_generation_for_p922_results_2_sdf_5/source | 1113b9cffdcf... |
| ligand_clean_PDK1.sdf | SDF | 27.9 KB | 01_3d_conformer_generation_for_p922_results_2_sdf_5/structures | e4cd611f7bf2... |
| 045_get_mol_name.py | PY | 3.3 KB | 01_3d_conformer_generation_for_p922_results_2_sdf_5/source | 87f26952256c... |
| ligand_clean_PDK1_phase2_report.md | MD | 3.2 KB | reports | 21fd46bc0877... |
| phase_01_3d_conformer_generation_for_p922_results_2_sdf_5.md | MD | 2.7 KB | reports | 9406cb8417db... |
| phase_3d_conformer_generation_p922_results_2.md | MD | 2.9 KB | reports | 363c65ff23e8... |
| 046_os_path_join.py | PY | 1.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 9c1c052b97f8... |
| 047_search_all_scripts_subdirectories_box_center_params.py | PY | 738 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 0bc6d3cbe308... |
| 048_read_dispatch_script_succeeded_get_actual_cx_cy_cz.py | PY | 160 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | ccbffd138b11... |
| 049_open.py | PY | 117 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 355ecfc6ee54... |
| 050_re_extract_li8_centroid_original_1z5m.py | PY | 1.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 972c4751aaef... |
| 051_check_dimorphite_dl_availability_read_prior.py | PY | 190 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | f6df76681506... |
| 052_load_all_6_ligands_get_their_smiles.py | PY | 608 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 0d27b6e80699... |
| 053_chem_sdmolsupplier.py | PY | 591 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 0630e2900446... |
| protonation-state-results-2.json | JSON | 10.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/results | 82dcafaf7e63... |
| protonation-state-results-3.json | JSON | 10.3 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/results | 9938944f0311... |
| protonation-state-results-4.json | JSON | 11.3 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/results | e55c7bfbb7a7... |
| protonation-state-results-5.json | JSON | 5.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/results | ab7d77f3eb03... |
| protonation-state-results-6.json | JSON | 4.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/results | 967d2c028918... |
| protonation-state-results-7.json | JSON | 5.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/results | 9f3297c5c94e... |
| 054_protonate_all_6_ligands_ph_7_4_via_dispatch.py | PY | 715 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 303198a7fb5d... |
| gnina_all6_result.json | JSON | 1.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 7530ae03b131... |
| gnina_docked.sdf.gz | GZ | 15.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 2cd328aabfd6... |
| 055_print.py | PY | 1.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 02b16dfab168... |
| 056_read_raw_sdf_gzip.py | PY | 1.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/inputs | cac1f3c3eae4... |
| 057_inspect_all_property_keys_first_block_find_correct.py | PY | 305 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 823d40ffaf87... |
| 058_show_last_20_lines_block_1_find_score_fields.py | PY | 230 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | e98375527c19... |
| 059_re_parse_all_blocks_correct_field_names.py | PY | 1.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 98faa2b90c34... |
| 061_fix_sdf_property_tag_uses_field_one_space_not_fi.csv | CSV | 1.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | f8aa5183cc98... |
| 060_fix_sdf_property_tag_uses_field_one_space_not_field.py | PY | 1.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 27d0bad2f1c2... |
| BX912_5poses.sdf | SDF | 15.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | bdc82afacaed... |
| BX912_best.sdf | SDF | 3.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 5de6d50bf826... |
| EL2003A-A2U1_5poses.sdf | SDF | 17.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | b1b3cb437f9e... |
| EL2003A-A2U1_best.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | c403e5a393fa... |
| EL2003A-A4U1_5poses.sdf | SDF | 18.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | e290a93e1f14... |
| EL2003A-A4U1_best.sdf | SDF | 3.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 5352f63af6ff... |
| EL2003A_5poses.sdf | SDF | 17.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 9d36d448b35c... |
| EL2003A_best.sdf | SDF | 3.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 9152eee803b0... |
| EL5001A_5poses.sdf | SDF | 14.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | a3e2e2b5c3fc... |
| EL5001A_best.sdf | SDF | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 44d6a3bcf260... |
| EL5003A_5poses.sdf | SDF | 15.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | b1711e942fa9... |
| EL5003A_best.sdf | SDF | 3.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 968b34171497... |
| 061_os_makedirs.py | PY | 1.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 5eae9a7b1da5... |
| 062_read_successful_mm_gbsa_calculation_scripts_previous.py | PY | 402 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 266bf10a2941... |
| BX912_pose1.sdf | SDF | 3.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 5de6d50bf826... |
| BX912_pose2.sdf | SDF | 3.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | d50cea2fe5a8... |
| BX912_pose3.sdf | SDF | 3.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | a30208726161... |
| BX912_pose4.sdf | SDF | 3.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 338ebda8940d... |
| BX912_pose5.sdf | SDF | 3.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | a8b655aeeaed... |
| EL2003A-A2U1_pose1.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | c403e5a393fa... |
| EL2003A-A2U1_pose2.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | e9e5925ba1ab... |
| EL2003A-A2U1_pose3.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | f281f3636504... |
| EL2003A-A2U1_pose4.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 94934415693d... |
| EL2003A-A2U1_pose5.sdf | SDF | 3.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | ab9866292434... |
| EL2003A-A4U1_pose1.sdf | SDF | 3.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 5352f63af6ff... |
| EL2003A-A4U1_pose2.sdf | SDF | 3.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 0cb2f57f66e2... |
| EL2003A-A4U1_pose3.sdf | SDF | 3.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 2dd3d94ee910... |
| EL2003A-A4U1_pose4.sdf | SDF | 3.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | b7c38b60d606... |
| EL2003A-A4U1_pose5.sdf | SDF | 3.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 3929327c621c... |
| EL2003A_pose1.sdf | SDF | 3.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 9152eee803b0... |
| EL2003A_pose2.sdf | SDF | 3.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 6aaa581f5955... |
| EL2003A_pose3.sdf | SDF | 3.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 4486a426b769... |
| EL2003A_pose4.sdf | SDF | 3.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 5d9caa9aeb4c... |
| EL2003A_pose5.sdf | SDF | 3.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | c333cf38b4b2... |
| EL5001A_pose1.sdf | SDF | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 44d6a3bcf260... |
| EL5001A_pose2.sdf | SDF | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | cf5bf8e68db8... |
| EL5001A_pose3.sdf | SDF | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 20a7a0c31ce1... |
| EL5001A_pose4.sdf | SDF | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 133d527e873f... |
| EL5001A_pose5.sdf | SDF | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 86c0ea8969b6... |
| EL5003A_pose1.sdf | SDF | 3.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 968b34171497... |
| EL5003A_pose2.sdf | SDF | 3.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | cf803bf90ee4... |
| EL5003A_pose3.sdf | SDF | 3.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | a641ddf5f750... |
| EL5003A_pose4.sdf | SDF | 3.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 1daed84f4d04... |
| EL5003A_pose5.sdf | SDF | 3.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 5e6aa81af023... |
| gbsa_BX912.json | JSON | 6.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 70152692aff3... |
| gbsa_EL2003A-A2U1.json | JSON | 6.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 9a07684a9be7... |
| gbsa_EL2003A-A4U1.json | JSON | 6.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 8305eac40e04... |
| gbsa_EL2003A.json | JSON | 6.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | a0e0cf8ec226... |
| gbsa_EL5001A.json | JSON | 6.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 6313b30bc719... |
| gbsa_EL5003A.json | JSON | 6.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | ed3f6ee41278... |
| BX912_pose1.mol | MOL | 3.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 7775d3fc1d71... |
| Dec.csv | CSV | 1.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 29187641144f... |
| Energy.csv | CSV | 344 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 4cefa47c818d... |
| complex.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 6d51f4127d46... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 4c235ecfd92f... |
| complex_reres.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 2d87e5a84257... |
| index.ndx | NDX | 150.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | ae1f80c208a6... |
| BX912_pose2.mol | MOL | 3.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 7c2f16bb79ed... |
| Dec.csv | CSV | 2.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 04ab515e1d4a... |
| Energy.csv | CSV | 342 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | ae81bbc07e47... |
| complex.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 225cecd291a3... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 4c235ecfd92f... |
| complex_reres.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 08fa24d66812... |
| index.ndx | NDX | 150.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | ae1f80c208a6... |
| BX912_pose3.mol | MOL | 3.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | e9c52a272cfc... |
| Dec.csv | CSV | 1.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | e46187af1b3d... |
| Energy.csv | CSV | 340 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 6b45926a96a5... |
| complex.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 27c024d191cc... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 4c235ecfd92f... |
| complex_reres.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | e4c7fa4074cd... |
| index.ndx | NDX | 150.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | ae1f80c208a6... |
| BX912_pose4.mol | MOL | 3.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | a8e91b0b9891... |
| Dec.csv | CSV | 1.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 13aaf489d8e4... |
| Energy.csv | CSV | 349 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 6499e495119f... |
| complex.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | e5861f098bd6... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 4c235ecfd92f... |
| complex_reres.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | dd3e72ee375b... |
| index.ndx | NDX | 150.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | ae1f80c208a6... |
| BX912_pose5.mol | MOL | 3.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 5e7c3d6013b2... |
| Dec.csv | CSV | 1.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 883cdb800b1c... |
| Energy.csv | CSV | 344 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 797ed045b78d... |
| complex.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 831bdb893401... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | ec9c7269bf15... |
| complex_reres.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 6e26969244f4... |
| index.ndx | NDX | 150.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | ae1f80c208a6... |
| BindingEnergy.csv | CSV | 1.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 494eb72c5455... |
| Dec.csv | CSV | 1.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 277b41762f5d... |
| EL2003A-A2U1_pose1.mol | MOL | 3.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 792137ea92e9... |
| Energy.csv | CSV | 342 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 61051dfd34ac... |
| complex.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 0d6cea924b6a... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | b5c0149128fe... |
| complex_reres.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | bb3253e24a5d... |
| index.ndx | NDX | 150.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | cbb83deb668c... |
| Dec.csv | CSV | 1.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 0dcb38570fed... |
| EL2003A-A2U1_pose2.mol | MOL | 3.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | a523913512a4... |
| Energy.csv | CSV | 340 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 50af3a302bea... |
| complex.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | a8c6bf8ebab2... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f22e55243c26... |
| complex_reres.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 41edee88a27e... |
| index.ndx | NDX | 150.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | cbb83deb668c... |
| Dec.csv | CSV | 2.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 0cb9a1206a9c... |
| EL2003A-A2U1_pose3.mol | MOL | 3.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 7d4510326363... |
| Energy.csv | CSV | 346 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | daf47221773f... |
| complex.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 16b1a4cbd8eb... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f22e55243c26... |
| complex_reres.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 9691847c64b2... |
| index.ndx | NDX | 150.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | cbb83deb668c... |
| Dec.csv | CSV | 2.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 3415caef8133... |
| EL2003A-A2U1_pose4.mol | MOL | 3.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | be22a8604681... |
| Energy.csv | CSV | 342 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | a7164b95a044... |
| complex.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | f45c9e8f7399... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f22e55243c26... |
| complex_reres.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 7efae2183697... |
| index.ndx | NDX | 150.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | cbb83deb668c... |
| Dec.csv | CSV | 1.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 02fd1536f74d... |
| EL2003A-A2U1_pose5.mol | MOL | 3.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 032b31924612... |
| Energy.csv | CSV | 339 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 8d52f1fedbeb... |
| complex.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 3a381bc7837a... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f22e55243c26... |
| complex_reres.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | fd61f2e02c09... |
| index.ndx | NDX | 150.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | cbb83deb668c... |
| Dec.csv | CSV | 2.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | b50800150cb6... |
| EL2003A-A4U1_pose1.mol | MOL | 3.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 7a7db9532134... |
| Energy.csv | CSV | 344 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 968b0b0ba659... |
| complex.pdb | PDB | 365.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | ae3259ec03ad... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 273df6966d36... |
| complex_reres.pdb | PDB | 365.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | c61dcee1cdca... |
| index.ndx | NDX | 150.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | c2055b67307d... |
| Dec.csv | CSV | 1.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 8b5a61124c44... |
| EL2003A-A4U1_pose2.mol | MOL | 3.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 9c0120fbb81e... |
| Energy.csv | CSV | 343 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | a8332fb5ef66... |
| complex.pdb | PDB | 365.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 315c98ecf8a3... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 273df6966d36... |
| complex_reres.pdb | PDB | 365.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 9bebc6c269ca... |
| index.ndx | NDX | 150.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | c2055b67307d... |
| Dec.csv | CSV | 1.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 81e7eba28977... |
| EL2003A-A4U1_pose3.mol | MOL | 3.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 40cd8153a3f4... |
| Energy.csv | CSV | 348 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 6763f510a9ff... |
| complex.pdb | PDB | 365.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | cd90bfdd79a8... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 0a7431adee90... |
| complex_reres.pdb | PDB | 365.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 66e89572659d... |
| index.ndx | NDX | 150.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | c2055b67307d... |
| Dec.csv | CSV | 2.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 20ac3a2e3e0f... |
| EL2003A-A4U1_pose4.mol | MOL | 3.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | d41653362d61... |
| Energy.csv | CSV | 342 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 6c7db7f352f4... |
| complex.pdb | PDB | 365.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | f0f5f75e146c... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 0a7431adee90... |
| complex_reres.pdb | PDB | 365.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 4735f496b4ca... |
| index.ndx | NDX | 150.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | c2055b67307d... |
| Dec.csv | CSV | 2.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | f9df6e9806af... |
| EL2003A-A4U1_pose5.mol | MOL | 3.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 8153b6b880de... |
| Energy.csv | CSV | 345 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 161987034a02... |
| complex.pdb | PDB | 365.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 1c5370fe9d3a... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 0a7431adee90... |
| complex_reres.pdb | PDB | 365.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | ef2523aafb47... |
| index.ndx | NDX | 150.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | c2055b67307d... |
| Dec.csv | CSV | 2.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | fcf3f4015e21... |
| EL2003A_pose1.mol | MOL | 3.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | c8fb3c06c41c... |
| Energy.csv | CSV | 348 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | c4e4370f38fa... |
| complex.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 739f283efbd1... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 3a70c6327a45... |
| complex_reres.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | a3c941467aaf... |
| index.ndx | NDX | 150.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | edd9a4def35b... |
| Dec.csv | CSV | 1.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | b15a43cdd6a4... |
| EL2003A_pose2.mol | MOL | 3.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 82e057ea9388... |
| Energy.csv | CSV | 347 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 3b3f7d0ef2c3... |
| complex.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | ac497b6f9ea2... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 3a70c6327a45... |
| complex_reres.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | a982cebf96bc... |
| index.ndx | NDX | 150.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | edd9a4def35b... |
| Dec.csv | CSV | 1.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 66d057c32723... |
| EL2003A_pose3.mol | MOL | 3.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | df92bff7a852... |
| Energy.csv | CSV | 347 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 565694db3e90... |
| complex.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | b9c7cb0159c7... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 3a70c6327a45... |
| complex_reres.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 0c05139e7eaa... |
| index.ndx | NDX | 150.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | edd9a4def35b... |
| Dec.csv | CSV | 1.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | b3de3dba7cf0... |
| EL2003A_pose4.mol | MOL | 3.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | f15ec601d8e2... |
| Energy.csv | CSV | 342 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 9e1363b2c2a5... |
| complex.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 21b916f36ca5... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 9ec0ddd77e98... |
| complex_reres.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 8db979b0d8df... |
| index.ndx | NDX | 150.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | edd9a4def35b... |
| Dec.csv | CSV | 1.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | a884e96e154f... |
| EL2003A_pose5.mol | MOL | 3.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 294def1d4466... |
| Energy.csv | CSV | 350 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 9ffb782c9aed... |
| complex.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 0e343ae71852... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 9ec0ddd77e98... |
| complex_reres.pdb | PDB | 365.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | b1069037cb30... |
| index.ndx | NDX | 150.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | edd9a4def35b... |
| Dec.csv | CSV | 1.9 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | f6bb8984dd52... |
| EL5001A_pose1.mol | MOL | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | bbd76d5626a8... |
| Energy.csv | CSV | 342 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 977579dcaa71... |
| complex.pdb | PDB | 364.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 43d5ac1f4bc9... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 1910cf6ec05c... |
| complex_reres.pdb | PDB | 364.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | e27af0713338... |
| index.ndx | NDX | 150.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f0bef4e15045... |
| Dec.csv | CSV | 2.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | aad31fc2cd55... |
| EL5001A_pose2.mol | MOL | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 78acf050e0ca... |
| Energy.csv | CSV | 341 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 662471d0a512... |
| complex.pdb | PDB | 364.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | da3e2bb0aece... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 66ad542699ed... |
| complex_reres.pdb | PDB | 364.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 58c2d9301e27... |
| index.ndx | NDX | 150.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f0bef4e15045... |
| Dec.csv | CSV | 1.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 169649fec108... |
| EL5001A_pose3.mol | MOL | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 5f8691b911d9... |
| Energy.csv | CSV | 341 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | e256da4ed96a... |
| complex.pdb | PDB | 364.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | d9fd904db536... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 66ad542699ed... |
| complex_reres.pdb | PDB | 364.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | ad4ca462068d... |
| index.ndx | NDX | 150.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f0bef4e15045... |
| Dec.csv | CSV | 1.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 61cf6845b85a... |
| EL5001A_pose4.mol | MOL | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | c96147cf3207... |
| Energy.csv | CSV | 339 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | a6fbc6404431... |
| complex.pdb | PDB | 364.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 1fe8537a8f61... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 66ad542699ed... |
| complex_reres.pdb | PDB | 364.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | fb74a3f1871a... |
| index.ndx | NDX | 150.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f0bef4e15045... |
| Dec.csv | CSV | 1.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 2fbafacb33a2... |
| EL5001A_pose5.mol | MOL | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | e4ea76ddc4be... |
| Energy.csv | CSV | 338 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 2fc2455551b0... |
| complex.pdb | PDB | 364.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 0dda435f94b0... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 66ad542699ed... |
| complex_reres.pdb | PDB | 364.5 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | f6234f9c2d7e... |
| index.ndx | NDX | 150.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f0bef4e15045... |
| Dec.csv | CSV | 1.6 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | fc815770dd6e... |
| EL5003A_pose1.mol | MOL | 3.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 1bc4d335cde5... |
| Energy.csv | CSV | 336 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 49a65922b0ba... |
| complex.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | f3d6bb3dc0ef... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 93a17ffb4c81... |
| complex_reres.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 06c2ff1741a1... |
| index.ndx | NDX | 150.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f84869168c3b... |
| Dec.csv | CSV | 1.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | b7fc1a7f6352... |
| EL5003A_pose2.mol | MOL | 3.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 88ba02c3faa8... |
| Energy.csv | CSV | 341 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 42b2033f7671... |
| complex.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | b7804faff2ae... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 4c941d7d3307... |
| complex_reres.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | eea05ead267a... |
| index.ndx | NDX | 150.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f84869168c3b... |
| Dec.csv | CSV | 2.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | a42c92e73213... |
| EL5003A_pose3.mol | MOL | 3.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | d8aa2c0ac9d1... |
| Energy.csv | CSV | 344 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | d7589ac48e47... |
| complex.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 7347f5d7fc02... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 4c941d7d3307... |
| complex_reres.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 59bb64271489... |
| index.ndx | NDX | 150.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f84869168c3b... |
| Dec.csv | CSV | 1.3 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | d751270b7420... |
| EL5003A_pose4.mol | MOL | 3.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 3a1d4db8e7e0... |
| Energy.csv | CSV | 347 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 573607e6f628... |
| complex.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 5252a93ae2a9... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 4c941d7d3307... |
| complex_reres.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 568f9d10904f... |
| index.ndx | NDX | 150.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f84869168c3b... |
| Dec.csv | CSV | 1.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 42a8e8422d80... |
| EL5003A_pose5.mol | MOL | 3.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | bfab96ed726d... |
| Energy.csv | CSV | 341 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 5af82b3354d6... |
| complex.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | 323a90e197aa... |
| complex.top | TOP | 2.3 MB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 4c941d7d3307... |
| complex_reres.pdb | PDB | 364.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/structures | d86882c5b961... |
| index.ndx | NDX | 150.7 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | f84869168c3b... |
| 063_print.py | PY | 1.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 5be82fd1778a... |
| 064_parse_all_gbsa_results_merge_docking_scores.py | PY | 2.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | f4ef368195ac... |
| 065_sorted.py | PY | 607 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 55008d0e4449... |
| 066_inspect_one_gbsa_json_understand_structure.py | PY | 632 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | ead1237aade4... |
| 067_load_gnina_scores_json.py | PY | 347 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 300db9bbbe43... |
| 068_re_parse_docking_scores_gnina_docked_sdf_gz.py | PY | 2.3 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 393926c6fec1... |
| 069_fix_sort_ligand_names_longest_first_el2003a_a4u1.py | PY | 2.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 31baecaacdc0... |
| 071_load_all_gbsa_jsons_merge_into_full_table.csv | CSV | 2.1 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | a3f6afd17e55... |
| 070_load_all_gbsa_jsons_merge_into_full_table.py | PY | 1.3 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | adb47fd478bb... |
| 071_identify_best_pose_per_ligand_lowest_mm_gbsa.py | PY | 580 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | cf5137baa89b... |
| 072_interaction_analysis_parse_receptor_pdb_atoms.py | PY | 1.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 203b5ac32ca9... |
| 073_analyze_interactions.py | PY | 2.8 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | c61ec0e99d78... |
| 074_build_interaction_statistics_table.py | PY | 1.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 3a83411ea840... |
| full_docking_gbsa_table.csv | CSV | 79 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | cafd065e356b... |
| interactions_best_poses.json | JSON | 5.2 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/work | 60c5983046e1... |
| 075_save_interaction_data_json_reference.py | PY | 1.0 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/inputs | 776035f38cad... |
| full_docking_gbsa_table.csv | CSV | 2.4 KB | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/tables | 6e4399c36d0e... |
| 076_open.py | PY | 539 B | 01_full_pdk1_docking_campaign_all_6_ligands_from_li/source | 9aa638cbe939... |
| PDK1_docking_campaign_final_report.md | MD | 13.6 KB | reports | b201c8115e42... |
| phase_01_full_pdk1_docking_campaign_all_6_ligands_from_li.md | MD | 36.8 KB | reports | b9611df6b6b9... |
| 077_confirm_report_path_write_phase_document.py | PY | 339 B | source | 75dd78d6813b... |
| phase_01_full_pdk1_docking_campaign.md | MD | 5.0 KB | reports | 52b462f401c6... |
| 078_sorted.py | PY | 956 B | 01_export_merged_sdf_files_and_push_to_github_rsa_e/source | 43fee900d9a0... |
| 079_files.py | PY | 2.9 KB | 01_export_merged_sdf_files_and_push_to_github_rsa_e/source | ff09e5df41fe... |
| MD_PDK1.sdf | SDF | 19.6 KB | 01_export_merged_sdf_files_and_push_to_github_rsa_e/structures | 33a70dedbfdf... |
| docking_PDK1.sdf | SDF | 98.2 KB | 01_export_merged_sdf_files_and_push_to_github_rsa_e/structures | 2321e3c2b370... |
| 080_write_annotated_sdf.py | PY | 2.7 KB | 01_export_merged_sdf_files_and_push_to_github_rsa_e/source | f086092869f1... |
| phase_01_export_merged_sdf_files_and_push_to_github_rsa_e.md | MD | 2.4 KB | reports | c916c5ebccb0... |
| phase_export_sdf_github_push.md | MD | 2.8 KB | reports | 8cc5e069f0ea... |
| 081_print.py | PY | 448 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 6252691c2e96... |
| EL2003A_pose2.mol | MOL | 3.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 047cffee600f... |
| config.ini | INI | 255 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | b0249500951f... |
| 082_print.py | PY | 1.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 53bead50bb20... |
| EL2003A_pose2.mol | MOL | 3.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | a6430a7506e3... |
| complex.pdb | PDB | 365.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | c7cc3ceb530d... |
| complex.top | TOP | 2.3 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | 03a966f80fb1... |
| complex_reres.pdb | PDB | 365.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 518c51d3b209... |
| traj_com.xtc | XTC | 1.7 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | 3a92c74b225f... |
| config.ini | INI | 255 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | adce986a5ab3... |
| 083_print.py | PY | 1018 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | e429577ea703... |
| EL2003A_pose2.mol | MOL | 3.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | f829f01e122d... |
| complex.pdb | PDB | 365.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 481117b32262... |
| complex.top | TOP | 2.3 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | beeb83361d70... |
| complex_reres.pdb | PDB | 365.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 08d12eb4ab90... |
| traj_com.xtc | XTC | 1.7 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | a68c1a7276e3... |
| 084_print.py | PY | 1.0 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | fd5c0698cbf5... |
| 085_os_path_getsize.py | PY | 732 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 0106711ed396... |
| cpu_test.txt | TXT | 5 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/reports | d117fa006ba9... |
| slurm-21798812.log | LOG | 27 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | 8277b426b81d... |
| phase_md_refinement_EL2003A_lumi_cpu.md | MD | 3.0 KB | reports | f5fa7aaf9010... |
| slurm-21798843.log | LOG | 17.9 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | cbe176a13dd3... |
| phase_02_submit_amber_md_mm_gbsa_to_lumi_cpu_partition.md | MD | 5.7 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/reports | 7755fb2312ff... |
| audit_md_lumi_cpu_EL2003A.md | MD | 12.8 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/reports | 0f639fdc2738... |
| phase_03_task_a285dd498619c3c0c.md | MD | 5.8 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/reports | 6c646fb857c2... |
| audit_amber_md_mmpbsa_script.md | MD | 7.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/reports | 6e1b6a05225f... |
| 086_check_available_libraries_mm_gbsa_post_processing.py | PY | 390 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | de46fa662de6... |
| receptor_pH74_noH.pdb | PDB | 184.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 76a2981921f9... |
| 087_step_1_strip_all_h_atoms_receptor_fixes_hie_hd1.py | PY | 1.6 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 4aa2ddf3dad5... |
| 088_dispatch_easy_md_amber14sb_protein_openff_ligand_2.py | PY | 1.3 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | ef01511d7fc4... |
| cpu_test.txt | TXT | 644 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/reports | 1f96201c5a8a... |
| audit_md_lumi_cpu_EL2003A.md | MD | 16.0 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/reports | c3a63da4d6ef... |
| slurm-21798969.log | LOG | 529 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | 01989ceb40f4... |
| audit_amber_md_mmpbsa_script.md | MD | 10.2 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/reports | 64000d994560... |
| phase_03_failure_analysis_corrected_resubmission.md | MD | 6.6 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/reports | 071b31a18d5f... |
| 089_estimate_receptor_3d_extent_predict_simulation_box.py | PY | 1.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | ec3296260f96... |
| openfe_result.json | JSON | 6.8 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | 64a086426fd6... |
| 090_print.py | PY | 1.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 159740a47c2a... |
| EL2003A_pose2_3D.sdf | SDF | 3.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | fbb0d876a7b3... |
| 091_read_pose_sdf_preserving_all_h_atoms_3d_coords.py | PY | 1.4 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 5c0397b24d1b... |
| easymd_result2.json | JSON | 656 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | 1e09f2a1cfed... |
| 092_print.py | PY | 1.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | f06ad2b9d46d... |
| 093_check_what_s_available.py | PY | 801 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 600b351b7e5e... |
| 094_check_parmed_mdtraj_openmm.py | PY | 651 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | e2bf1fedfb14... |
| 095_subprocess_run.py | PY | 1.0 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 24267574ae76... |
| 096_structure.py | PY | 791 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | c4d45263db42... |
| 097_parmed_already_successfully_imported_grab_cached.py | PY | 1.0 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 1d6bc06f6ef2... |
| mmgbsa_calc.py | PY | 6.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | ff4ed6039155... |
| 098_run_mm_gbsa_script_subprocess_avoids_sandbox_code_py.py | PY | 743 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 435ea0c06ff4... |
| 099_find_all_python_executables_check_which_has_mdtraj.py | PY | 641 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 4a16869bb2e5... |
| complex.prmtop | PRMTOP | 3.4 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 30da94c6f099... |
| ligand.prmtop | PRMTOP | 25.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 5809a4300f94... |
| receptor.prmtop | PRMTOP | 3.3 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 466ac1c8f7cc... |
| 100_print.py | PY | 655 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 63eb072acc15... |
| mmgbsa_calc.py | PY | 6.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | cc00fceba596... |
| mmgbsa_result.json | JSON | 20.9 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | e7d32b40444e... |
| 101_print.py | PY | 623 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 01935d88d9f7... |
| 102_load_results.py | PY | 1.4 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 32c8fe9b148d... |
| MD_refinement_EL2003A_pose2.md | MD | 4.4 KB | reports | 885175d00e64... |
| phase_01_md_refinement_of_el2003a_best_docking_pose_pose_.md | MD | 6.8 KB | 02_submit_amber_md_mm_gbsa_to_lumi_cpu_partition/reports | 0b85916e9507... |
| audit_mmgbsa_md_refinement_EL2003A_pose2.md | MD | 13.5 KB | 02_submit_amber_md_mm_gbsa_to_lumi_cpu_partition/reports | d836a30a3600... |
| phase_03_task_ac481d76baf4e5e3c.md | MD | 7.0 KB | 02_submit_amber_md_mm_gbsa_to_lumi_cpu_partition/reports | 1538461ad6bd... |
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
| phase_extract_MD_final_pose_SDF_and_trajectory_video.md | MD | 5.5 KB | reports | de1f74587973... |
| audit_extract_MD_final_pose_SDF_and_video.md | MD | 12.9 KB | reports | 7ffb2e70e1ee... |
| phase_02_task_aeb2e0f5ca7e95c36.md | MD | 5.1 KB | reports | c43b5a66db1b... |
| extract_final_pose_sdf.py | PY | 5.1 KB | source | 0a7518ebc328... |
| EL2003A_pose2_MD_final.sdf | SDF | 3.4 KB | structures | 853fd92ac0b6... |
| 109_subprocess_run.py | PY | 398 B | source | 71cf647bdbf6... |
| make_traj_video.py | PY | 8.9 KB | source | ad47e036c7cd... |
| EL2003A_MD_final_frame.png | PNG | 322.8 KB | figures | 225094a65f0e... |
| EL2003A_MD_ligand_RMSD.png | PNG | 58.2 KB | figures | cff6b4ff67ab... |
| EL2003A_MD_trajectory.gif | GIF | 7.0 MB | figures | 5c55fec2b4cb... |
| 110_subprocess_run.py | PY | 380 B | source | ea81a081517c... |
| phase_extract_MD_final_pose_SDF_and_trajectory_video.md | MD | 9.1 KB | reports | e31c030f72e0... |
| recovery_audit_extract_MD_final_pose_SDF_and_video.md | MD | 4.8 KB | reports | 7491c1b99c99... |
| audit2_extract_MD_final_pose_SDF_and_video.md | MD | 9.8 KB | reports | 0052678d0f4a... |
| phase_03_task_a842a6f926ce6d35d.md | MD | 6.0 KB | reports | fd84bbfa5c32... |
| extract_final_pose_sdf.py | PY | 5.1 KB | source | aac6d68f0202... |
| make_traj_video.py | PY | 8.8 KB | source | 642c69f7f98e... |
| phase_extract_MD_final_pose_SDF_and_trajectory_video.md | MD | 9.1 KB | reports | 31acd1e07cc3... |
| phase_extract_MD_final_pose_SDF_and_trajectory_video.md | MD | 9.2 KB | reports | 4f68fb1602a4... |
| phase_extract_MD_final_pose_SDF_and_trajectory_video.md | MD | 9.2 KB | reports | c82bb58befb4... |
| recovery_audit_extract_MD_final_pose_SDF_and_video.md | MD | 4.8 KB | reports | 48c9eef6afa7... |
| recovery_audit_extract_MD_final_pose_SDF_and_video.md | MD | 4.8 KB | reports | f6154309e4da... |
| recovery_audit_extract_MD_final_pose_SDF_and_video.md | MD | 4.8 KB | reports | 799410e26551... |
| 111_subprocess_run.py | PY | 403 B | source | 32e3f34bfe78... |
| phase_extract_MD_final_pose_SDF_and_trajectory_video.md | MD | 10.8 KB | reports | 00d4c01a30ad... |
| phase_extract_MD_final_pose_SDF_and_trajectory_video.md | MD | 10.8 KB | reports | e2955da9c750... |
| phase_extract_MD_final_pose_SDF_and_trajectory_video.md | MD | 10.8 KB | reports | 9df14fe989ae... |
| audit_extract_MD_final_pose_SDF_and_video.md | MD | 14.7 KB | reports | 446334497214... |
| recovery_audit_extract_MD_final_pose_SDF_and_video.md | MD | 6.1 KB | reports | f2889af09dcc... |
| audit2_extract_MD_final_pose_SDF_and_video.md | MD | 11.3 KB | reports | c24bc061bcda... |
| ligand_smiles.json | JSON | 937 B | work | 41734fd60c2e... |
| 112_read_smiles_already_extracted.py | PY | 913 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 3b1849c8249f... |
| 113_dispatch.py | PY | 458 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 8b50d8357b81... |
| 114_agc_only_first_pdk1_s_home_family_fastest_interpret.py | PY | 486 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 0ec65c2ec5e7... |
| 115_open.py | PY | 693 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | f2dcc5404a7b... |
| 116_inspect_what_keys_came_back_find_csv.py | PY | 943 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | e7b5b9a3e1ef... |
| 117_pd_read_csv.py | PY | 229 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 9661a83e14e0... |
| 118_map_smiles_compound_name.py | PY | 627 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 06452fc58acc... |
| 119_dispatch.py | PY | 337 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 95830c34febf... |
| 120_print.py | PY | 355 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | e82527c0bdce... |
| 121_open.py | PY | 653 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | d84098d43547... |
| 122_test_can_pass_kinase_names_instead_kinase_families.py | PY | 527 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 10a95618faaa... |
| 123_clinical_off_target_panel_uniprot_accessions_covers.py | PY | 1.3 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 068f6712748d... |
| 124_remove_three_unknown_accessions_p49840_gsk3a_q96gd4.py | PY | 655 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 03c981e1d561... |
| 125_open.py | PY | 813 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 522eb67fc203... |
| 126_open.py | PY | 673 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 20887bcfcd29... |
| 127_batch_2_cmgc_core_cdk1_4_6_erk1_2_p38_jnk1.py | PY | 429 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | de90ce720723... |
| 128_open.py | PY | 1.0 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 6367d97643c4... |
| 129_open.py | PY | 996 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | b086e7866590... |
| 130_matplotlib_use.py | PY | 873 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 61973e98c3be... |
| 131_build_master_pivot_best_score_per_compound_kinase.py | PY | 985 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 849458208ddb... |
| kinome_heatmap.png | PNG | 256.3 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/figures | 8963126d795a... |
| 132_matplotlib_use.py | PY | 3.3 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 92d940638c50... |
| 133_per_compound_top_5_off_targets.py | PY | 1.8 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | ca72317b5d1f... |
| kinome_per_compound.png | PNG | 176.8 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/figures | 8d76967e9103... |
| 134_figure_2_per_compound_selectivity_bars_top_8_off.py | PY | 2.0 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 230a8cacd808... |
| kinome_selectivity_profile.md | MD | 11.7 KB | reports | 2eb68938ca84... |
| 135_check_report_file.py | PY | 179 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 303bd3d9fe8c... |
| kinome_selectivity_matrix.csv | CSV | 4.1 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/tables | ecf28dba71ba... |
| 136_shutil_copy2.py | PY | 399 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 88f606d37fe4... |
| phase_01_kinome_selectivity_profile_for_6_pdk1_ligands.md | MD | 6.8 KB | reports | df7d0040b698... |
| phase_kinome_selectivity_profile.md | MD | 8.9 KB | reports | aca63a019c73... |
| 137_csv_files_items.py | PY | 1.1 KB | source | c8579d4514d9... |
| 138_load_smiles_name_map.py | PY | 891 B | source | d07875e6a50e... |
| 139_verify_aura_universal_claim.py | PY | 1.2 KB | source | 65da14f6d79f... |
| 140_verify_compound_specific_off_targets.py | PY | 1.4 KB | source | f67803c883ea... |
| audit_kinome_selectivity_profile.md | MD | 6.9 KB | reports | a1252d116582... |
| phase_kinome_selectivity_profile.md | MD | 9.1 KB | reports | 5851440801dd... |
| phase_kinome_selectivity_profile.md | MD | 9.1 KB | reports | b5b705c50d2c... |
| phase_kinome_selectivity_profile_6_pdk1_ligands.md | MD | 7.5 KB | reports | da9e47dabc9c... |
| audit_kinome_selectivity_profile.md | MD | 9.4 KB | reports | 36924e170a68... |
| 141_bx912_vs_el2003a_per_kinase_delta.py | PY | 468 B | 01_compare_bx912_vs_el2003a_kinase_specificity/source | 8e0b2148b527... |
| 142_open.py | PY | 1.4 KB | 01_compare_bx912_vs_el2003a_kinase_specificity/source | 68ceccf09c92... |
| phase_01_compare_bx912_vs_el2003a_kinase_specificity.md | MD | 3.5 KB | reports | b93f7f954b4a... |
| phase_compare_bx912_vs_el2003a_kinase_specificity.md | MD | 6.1 KB | reports | 6c101d35a505... |
| audit_compare_bx912_vs_el2003a_kinase_specificity.md | MD | 4.0 KB | reports | fbeccc27a45c... |
| phase_01_compare_bx912_vs_el2003a_kinase_specificity.md | MD | 5.9 KB | reports | 59f43ff32aa4... |
| 143_print_full_43_kinase_6_compound_pivot_table.py | PY | 88 B | source | 6d53d1e45d4b... |
| 144_pivot_t_copy.py | PY | 5.1 KB | 01_save_kinome_selectivity_matrix_as_excel_file/source | b24d7f29bdcf... |
| 145_open.py | PY | 628 B | 01_save_kinome_selectivity_matrix_as_excel_file/source | 69ecabba22b9... |
| kinome_selectivity_matrix.xlsx | XLSX | 10.8 KB | 01_save_kinome_selectivity_matrix_as_excel_file/tables | 5d3c319655c8... |
| 146_copy.py | PY | 3.3 KB | 01_save_kinome_selectivity_matrix_as_excel_file/source | 6b29c8ffc419... |
| phase_01_save_kinome_selectivity_matrix_as_excel_file.md | MD | 3.7 KB | reports | bbc9ac1485e0... |
| phase_01_save_kinome_selectivity_matrix_as_excel_file.md | MD | 3.3 KB | reports | bcd00f01edd5... |
| audit_save_kinome_selectivity_matrix_as_excel_file.md | MD | 2.5 KB | reports | 7f8f6e15cf7c... |
| phase_save_kinome_selectivity_matrix_as_excel_file.md | MD | 2.3 KB | reports | aa048f967256... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 601 file(s) were produced and registered, 601 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No citation is on record for gbsa, so the versions used cannot be traced to a publication.
- Versions were not recorded for gbsa. A methods section without a version is not reproducible.

## References

**No citation on record:** gbsa.

These were used by this phase and are reported for completeness. A citation should be supplied before this material is used in a manuscript. They are listed rather than omitted because a methods section that hides a dependency is not reproducible.
