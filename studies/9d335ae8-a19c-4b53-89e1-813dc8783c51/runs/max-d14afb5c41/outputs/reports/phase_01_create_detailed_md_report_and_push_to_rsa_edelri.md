---
title: "Phase 1: Create detailed MD report and push to RSA-Edelris/RaycaBio GitHub"
study_id: "9d335ae8-a19c-4b53-89e1-813dc8783c51"
run_id: "max-49b0de58e8"
phase_index: 1
phase_id: "1"
phase_goal: "Create detailed MD report and push to RSA-Edelris/RaycaBio GitHub"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Create detailed MD report and push to RSA-Edelris/RaycaBio GitHub

## Summary

This phase set out to create detailed MD report and push to RSA-Edelris/RaycaBio GitHub. It completed 61 output files.

## Objective

Create detailed MD report and push to RSA-Edelris/RaycaBio GitHub

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
| CRBN.pdb | PDB | 473.5 KB | uploads | b2658693e443... |
| 001_check_what_lvy_print_all_hetatm_lvy.py | PY | 546 B | 01_identify_crbn_main_and_allosteric_pockets_from_c/source | e0fcd72925d7... |
| 002_parse_pdb_manually_extract_all_atom_hetatm_records.py | PY | 1.4 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/source | 56c12ba20ae7... |
| 003_main_pocket_residues_within_4_5_any_lvy_atom.py | PY | 1.6 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/source | 602fc57b4a9d... |
| 004_grid_based_cavity_detection_fpocket_lite_approach.py | PY | 1.7 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/source | 7155cd76f05e... |
| 005_cluster_probe_points_dbscan_eps_3_min_samples_5.py | PY | 1.3 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/source | 59e4d630f591... |
| 007_ligsite_style_pocket_detection_each_grid_point_c.csv | CSV | 112 B | 01_identify_crbn_main_and_allosteric_pockets_from_c/tables | b9843609f4cf... |
| 006_ligsite_style_pocket_detection_each_grid_point_cast.py | PY | 1.9 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/source | 474915142e4f... |
| 007_fix_count_one_hit_per_direction_6_directions_total.py | PY | 1.6 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/source | c8bc750252b4... |
| 008_approach_6_6_burial_aggressive_sub_clustering_map.py | PY | 1.2 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/source | 034f5d30523f... |
| 009_map_each_cluster_s_probe_points_surrounding_protein.py | PY | 1.3 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/source | 6ea209f21fab... |
| CRBN_pockets.png | PNG | 419.5 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/figures | 0aadbdd12e25... |
| 010_matplotlib_use.py | PY | 4.9 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/source | 6095d48e2dbf... |
| CRBN_pockets_annotated.png | PNG | 559.0 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/figures | 444cf50a1ab2... |
| 011_matplotlib_use.py | PY | 6.4 KB | 01_identify_crbn_main_and_allosteric_pockets_from_c/source | d4a995195b25... |
| phase_01_identify_crbn_main_and_allosteric_pockets_from_c.md | MD | 3.8 KB | reports | de08b76ac6c8... |
| CRBN_pocket_analysis.md | MD | 5.6 KB | reports | 4577dacf5a2a... |
| phase_crbn_pocket_detection.md | MD | 3.6 KB | reports | b3073980a4b7... |
| 012_probe_biotite_graphics_api.py | PY | 676 B | 01_generate_cartoon_protein_image_with_colored_pock/source | 44aab3530bd7... |
| 013_load_structure_biotite_compute_secondary_structure.py | PY | 846 B | 01_generate_cartoon_protein_image_with_colored_pock/source | ea0fca985427... |
| 014_build_per_residue_c_table_sse_labels_struc_annotate.py | PY | 1.1 KB | 01_generate_cartoon_protein_image_with_colored_pock/source | d9f463b08d90... |
| 015_matplotlib_use.py | PY | 2.4 KB | 01_generate_cartoon_protein_image_with_colored_pock/source | 0dfeb568ffb4... |
| 016_segment_sse_trace.py | PY | 876 B | 01_generate_cartoon_protein_image_with_colored_pock/source | 1765a454e05a... |
| cartoon_utils.py | PY | 3.9 KB | 01_generate_cartoon_protein_image_with_colored_pock/source | 2a52851c4478... |
| 017_write_cartoon_renderer_file_functions_survive_across.py | PY | 4.2 KB | 01_generate_cartoon_protein_image_with_colored_pock/source | 3ebbc3cf1d70... |
| CRBN_cartoon_pockets.png | PNG | 512.1 KB | 01_generate_cartoon_protein_image_with_colored_pock/figures | 33d1c05cc82a... |
| 018_sys_path_insert.py | PY | 7.6 KB | 01_generate_cartoon_protein_image_with_colored_pock/source | 0819f7450f0b... |
| phase_01_generate_cartoon_protein_image_with_colored_pock.md | MD | 3.0 KB | reports | f1687c43fafa... |
| phase_crbn_cartoon_visualization.md | MD | 3.6 KB | reports | 1bcc31458242... |
| dpCDK2-CCNE1_without ligand.pdb | PDB | 382.2 KB | uploads | d15445ab73d9... |
| 019_open.py | PY | 1.5 KB | 01_pocket_analysis_and_cartoon_visualization_for_dp/source | 1bcc7d90956b... |
| 020_ligsite_pocket_detection_full_complex_both_chains.py | PY | 1.6 KB | 01_pocket_analysis_and_cartoon_visualization_for_dp/source | 9887294008f1... |
| 021_map_clusters_surrounding_protein_residues.py | PY | 869 B | 01_pocket_analysis_and_cartoon_visualization_for_dp/source | 58eb5200651b... |
| 022_main_pocket_anchor_canonical_cdk2_key_residues_6.py | PY | 1.8 KB | 01_pocket_analysis_and_cartoon_visualization_for_dp/source | f24523f88410... |
| 023_broader_main_pocket_5_any_atom_anchor_residues.py | PY | 761 B | 01_pocket_analysis_and_cartoon_visualization_for_dp/source | 248de15fbfae... |
| 024_bpdb_pdbfile_read.py | PY | 2.0 KB | 01_pocket_analysis_and_cartoon_visualization_for_dp/source | a34913ab61d8... |
| CDK2_CCNE1_cartoon_pockets.png | PNG | 823.5 KB | 01_pocket_analysis_and_cartoon_visualization_for_dp/figures | 88cf53075869... |
| 025_sys_path_insert.py | PY | 7.0 KB | 01_pocket_analysis_and_cartoon_visualization_for_dp/source | 53b621630ca8... |
| phase_01_pocket_analysis_and_cartoon_visualization_for_dp.md | MD | 2.9 KB | reports | c039598a4120... |
| CDK2_CCNE1_pocket_analysis.md | MD | 6.1 KB | reports | 59cb01d4c8cd... |
| 026_verify_cartoon_image_exists_recap_pocket_residues.py | PY | 465 B | source | ed3d54cd2312... |
| phase_cdk2_ccne1_pocket_analysis.md | MD | 5.5 KB | reports | 0838f1248836... |
| CDK2-CCNE.pdb | PDB | 765.8 KB | uploads | 03723ab01213... |
| 027_open.py | PY | 1.2 KB | 01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/source | b9ca3c9c1e6a... |
| 028_ctx_atoms.py | PY | 1.2 KB | 01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/source | d1dc6afe6949... |
| 029_pockets_dpcdk2_ccne1_analysis_main_atp_pocket_chain.py | PY | 2.5 KB | 01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/source | 2770015e545d... |
| 030_matplotlib_use.py | PY | 2.5 KB | 01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/source | 77b895e23259... |
| CDK2_CTX_vs_pockets.png | PNG | 599.9 KB | 01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/figures | f48ef7517d36... |
| 031_sys_path_insert.py | PY | 5.8 KB | 01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/source | 2bb8eebaca76... |
| phase_ctx_pocket_comparison.md | MD | 4.2 KB | reports | 31a5bb267700... |
| phase_01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with.md | MD | 2.6 KB | reports | 27eb795fdeea... |
| 032_pocket_druggability_descriptors_each_pocket_collect.py | PY | 3.9 KB | 01_druggability_assessment_for_all_pockets_across_c/source | eec92ed412d4... |
| drug_utils.py | PY | 1.5 KB | 01_druggability_assessment_for_all_pockets_across_c/source | 3baf9c74d895... |
| 033_write_helper_disk_persists_across_calls.py | PY | 3.3 KB | 01_druggability_assessment_for_all_pockets_across_c/source | 522a9effad44... |
| 035_sys_path_insert.csv | CSV | 646 B | 01_druggability_assessment_for_all_pockets_across_c/tables | 079955fd2e38... |
| 034_sys_path_insert.py | PY | 3.5 KB | 01_druggability_assessment_for_all_pockets_across_c/source | c00ac9c81709... |
| druggability_all_pockets.png | PNG | 164.2 KB | 01_druggability_assessment_for_all_pockets_across_c/figures | aaae53fc8f17... |
| 035_sys_path_insert.py | PY | 5.4 KB | 01_druggability_assessment_for_all_pockets_across_c/source | aa99bbe4dbe9... |
| phase_01_druggability_assessment_for_all_pockets_across_c.md | MD | 2.8 KB | reports | 8af9037397fb... |
| phase_druggability_all_pockets.md | MD | 3.9 KB | reports | ddc7317ae2e3... |
| pocket_analysis_full_report.md | MD | 11.7 KB | reports | 9e77752f7a40... |

## Verification

- No tool call is on record for this phase.
- 61 file(s) were produced and registered, 61 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
