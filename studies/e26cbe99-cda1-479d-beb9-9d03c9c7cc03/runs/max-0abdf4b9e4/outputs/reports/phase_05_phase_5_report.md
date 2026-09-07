---
title: "Phase 5: Phase 5 — Report"
study_id: "e26cbe99-cda1-479d-beb9-9d03c9c7cc03"
run_id: "max-7e8c57ab26"
phase_index: 5
phase_id: "5"
phase_goal: "Phase 5 — Report"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 5: Phase 5 — Report

## Summary

This phase set out to phase 5 — Report. It completed 82 output files.

## Objective

Phase 5 — Report

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
| 040_close_phase_5_final_report_document.py | PY | 1.8 KB | 05_phase_5_report/source | a5427adc7690... |

## Verification

- No tool call is on record for this phase.
- 82 file(s) were produced and registered, 82 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/pdbfixer:latest`
- Container Image: `registry.rayca.org/rayca-tools/fpocket:latest`
- Container Image: `registry.rayca.org/rayca-tools/protonation-state:latest`
- Container Image: `registry.rayca.org/rayca-tools/gnina:latest`

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
