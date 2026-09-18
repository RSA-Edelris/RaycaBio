---
title: "Phase 2: Prepare receptor and dock CRBN_lig_results_2.sdf into ternary complex"
study_id: "0ddc6243-37e4-40c9-aba2-1bf173994ad2"
run_id: "max-b1dc357bbc"
phase_index: 2
phase_id: "2"
phase_goal: "Prepare receptor and dock CRBN_lig_results_2.sdf into ternary complex"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 2: Prepare receptor and dock CRBN_lig_results_2.sdf into ternary complex

## Summary

This phase set out to prepare receptor and dock CRBN_lig_results_2.sdf into ternary complex. It completed 39 output files.

## Objective

Prepare receptor and dock CRBN_lig_results_2.sdf into ternary complex

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
| 030_step_1_read_sdf_inspect_compounds.py | PY | 1.0 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 7a74a076b09c... |
| 031_5hxb_crystal_characterisation_resolution_space_group.py | PY | 2.4 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 13576d0c3c53... |
| 032_missing_residues_full_contact_analysis_bridging.py | PY | 3.1 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | fe3e84719650... |
| 033_per_atom_contact_mapping_bsa_waters_pocket_sub_sites.py | PY | 2.4 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 3c3a2bd3cf1e... |
| 034_bsa_proxy_waters_pocket_unoccupied_subsites.py | PY | 3.2 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 48f5920f282a... |
| 035_receptor_preparation_extract_crbn_gspt1_add_h_define.py | PY | 2.8 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | fed40f3bb306... |
| 85C_crystal.pdb | PDB | 2.7 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | b796821bce17... |
| receptor_CRBN_GSPT1.pdb | PDB | 616.0 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | 44bbdc527293... |
| 036_os_makedirs.py | PY | 1.9 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | cf3167629c5e... |
| docking_box.txt | TXT | 86 B | 01_characterise_5hxb_crystal_structure_and_85c_bind/reports | 6a70f4dd47da... |
| receptor_prep_choices.txt | TXT | 1.6 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/reports | 41bcd089c832... |
| 037_recompute_lig_z_still_scope.py | PY | 2.5 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 35190f7e5de3... |
| lig_00_Compound_1.sdf | SDF | 2.1 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | 98d6bf3a71c1... |
| lig_01_Compound_4.sdf | SDF | 1.9 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | 275534d542e1... |
| lig_02_Compound_7.sdf | SDF | 2.2 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | e748ee22eeef... |
| lig_03_Compound_8.sdf | SDF | 1.9 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | 3d3bf435db17... |
| lig_04_Compound_9.sdf | SDF | 2.1 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | e889d000668b... |
| lig_05_Compound_10.sdf | SDF | 2.4 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | a32cbb81202d... |
| lig_06_Compound_11.sdf | SDF | 2.3 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | 2f0a7464de3c... |
| lig_07_Compound_12.sdf | SDF | 2.4 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | 6cc13af9a523... |
| 038_split_8_compound_sdf_into_individual_files_gnina.py | PY | 940 B | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 91a982bcfecf... |
| gnina_docked.sdf.gz | GZ | 5.6 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | afc960d084f7... |
| 039_lig_fname_replace.py | PY | 1.6 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | d7cd3a5d8c89... |
| 040_inspect_actual_structure_one_result.py | PY | 772 B | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 1638d0820e45... |
| lig_00_Compound_1_poses.sdf | SDF | 28.6 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | e56639f5421f... |
| lig_01_Compound_4_poses.sdf | SDF | 26.5 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | 4d2b8cf4fb1c... |
| lig_02_Compound_7_poses.sdf | SDF | 30.0 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | a3d2b9206b61... |
| lig_03_Compound_8_poses.sdf | SDF | 25.6 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | 4ee4fd990dd2... |
| lig_04_Compound_9_poses.sdf | SDF | 29.3 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | 1733d077065e... |
| lig_05_Compound_10_poses.sdf | SDF | 32.4 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | 1465fb0943cd... |
| lig_06_Compound_11_poses.sdf | SDF | 30.9 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | e8309958ae41... |
| lig_07_Compound_12_poses.sdf | SDF | 33.1 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/structures | 23affadd218c... |
| 041_os_makedirs.py | PY | 2.6 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 11472f5bb409... |
| 042_gemmi_read_structure.py | PY | 1.7 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 0fd00ac7968b... |
| 043_min_dist.py | PY | 2.1 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 1831324a021e... |
| 044_min_dist.py | PY | 2.5 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 68511cc1be31... |
| 045_min_dist.py | PY | 2.6 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | dbed5bcffa16... |
| 046_min_dist.py | PY | 2.2 KB | 01_characterise_5hxb_crystal_structure_and_85c_bind/source | 7446c2f74f54... |
| phase_01_characterise_5hxb_crystal_structure_and_85c_bind.md | MD | 6.7 KB | 02_prepare_receptor_and_dock_crbn_lig_results_2_sdf/reports | c9c26bd08767... |

## Verification

- No tool call is on record for this phase.
- 39 file(s) were produced and registered, 39 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/gnina:latest`

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
