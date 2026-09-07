---
title: "Phase 1: Full PDK1 docking campaign: receptor prep → docking → MD → MM/GBSA → report"
study_id: "7a39e116-e0d5-4e70-93c3-da6df54e7e1e"
run_id: "max-85e5f5fec1"
phase_index: 1
phase_id: "1"
phase_goal: "Full PDK1 docking campaign: receptor prep → docking → MD → MM/GBSA → report"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Full PDK1 docking campaign: receptor prep → docking → MD → MM/GBSA → report

## Summary

This phase set out to full PDK1 docking campaign: receptor prep → docking → MD → MM/GBSA → report. It completed 102 output files.

## Objective

Full PDK1 docking campaign: receptor prep → docking → MD → MM/GBSA → report

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

## Verification

- No tool call is on record for this phase.
- 102 file(s) were produced and registered, 102 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/pdbfixer:latest`
- Container Image: `registry.rayca.org/rayca-tools/protonation-state:latest`
- Container Image: `registry.rayca.org/rayca-tools/gnina:latest`
- Container Image: `registry.rayca.org/rayca-tools/gbsa:latest`

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
