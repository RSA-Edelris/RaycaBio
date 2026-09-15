# Study: 9d335ae8-a19c-4b53-89e1-813dc8783c51

> WARNING: This study has NOT been reviewed. Results are unreviewed model output and must not be cited or relied upon without independent verification.

## Run Identity

- Run ID: `max-49b0de58e8`
- Published: 2026-09-15T12:09:43Z
- Review: not reviewed

## Tools and Environment

- No tool version information recorded.

## Outputs

Files included in this repository:

- `outputs/01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/figures/CDK2_CTX_vs_pockets.png` (614275 bytes)
- `outputs/01_druggability_assessment_for_all_pockets_across_c/figures/druggability_all_pockets.png` (168090 bytes)
- `outputs/01_druggability_assessment_for_all_pockets_across_c/tables/035_sys_path_insert.csv` (646 bytes)
- `outputs/01_generate_cartoon_protein_image_with_colored_pock/figures/CRBN_cartoon_pockets.png` (524401 bytes)
- `outputs/01_identify_crbn_main_and_allosteric_pockets_from_c/figures/CRBN_pockets.png` (429574 bytes)
- `outputs/01_identify_crbn_main_and_allosteric_pockets_from_c/figures/CRBN_pockets_annotated.png` (572454 bytes)
- `outputs/01_identify_crbn_main_and_allosteric_pockets_from_c/tables/007_ligsite_style_pocket_detection_each_grid_point_c.csv` (112 bytes)
- `outputs/01_pocket_analysis_and_cartoon_visualization_for_dp/figures/CDK2_CCNE1_cartoon_pockets.png` (843294 bytes)
- `outputs/reports/CDK2_CCNE1_pocket_analysis.md` (6270 bytes)
- `outputs/reports/CRBN_pocket_analysis.md` (5751 bytes)
- `outputs/reports/phase_01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with.md` (2688 bytes)
- `outputs/reports/phase_01_druggability_assessment_for_all_pockets_across_c.md` (2867 bytes)
- `outputs/reports/phase_01_generate_cartoon_protein_image_with_colored_pock.md` (3037 bytes)
- `outputs/reports/phase_01_identify_crbn_main_and_allosteric_pockets_from_c.md` (3871 bytes)
- `outputs/reports/phase_01_pocket_analysis_and_cartoon_visualization_for_dp.md` (2960 bytes)
- `outputs/reports/phase_cdk2_ccne1_pocket_analysis.md` (5616 bytes)
- `outputs/reports/phase_crbn_cartoon_visualization.md` (3713 bytes)
- `outputs/reports/phase_crbn_pocket_detection.md` (3660 bytes)
- `outputs/reports/phase_ctx_pocket_comparison.md` (4282 bytes)
- `outputs/reports/phase_druggability_all_pockets.md` (3958 bytes)
- `outputs/reports/pocket_analysis_full_report.md` (11963 bytes)
- `outputs/uploads/CDK2-CCNE.pdb` (784165 bytes)
- `outputs/uploads/CRBN.pdb` (484841 bytes)
- `outputs/uploads/dpCDK2-CCNE1_without ligand.pdb` (391397 bytes)

## Scripts

- `scripts/01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/source/027_open.py`
- `scripts/01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/source/028_ctx_atoms.py`
- `scripts/01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/source/029_pockets_dpcdk2_ccne1_analysis_main_atp_pocket_chain.py`
- `scripts/01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/source/030_matplotlib_use.py`
- `scripts/01_compare_ctx_contact_pocket_in_cdk2_ccne_pdb_with/source/031_sys_path_insert.py`
- `scripts/01_druggability_assessment_for_all_pockets_across_c/source/032_pocket_druggability_descriptors_each_pocket_collect.py`
- `scripts/01_druggability_assessment_for_all_pockets_across_c/source/033_write_helper_disk_persists_across_calls.py`
- `scripts/01_druggability_assessment_for_all_pockets_across_c/source/034_sys_path_insert.py`
- `scripts/01_druggability_assessment_for_all_pockets_across_c/source/035_sys_path_insert.py`
- `scripts/01_druggability_assessment_for_all_pockets_across_c/source/drug_utils.py`
- `scripts/01_generate_cartoon_protein_image_with_colored_pock/source/012_probe_biotite_graphics_api.py`
- `scripts/01_generate_cartoon_protein_image_with_colored_pock/source/013_load_structure_biotite_compute_secondary_structure.py`
- `scripts/01_generate_cartoon_protein_image_with_colored_pock/source/014_build_per_residue_c_table_sse_labels_struc_annotate.py`
- `scripts/01_generate_cartoon_protein_image_with_colored_pock/source/015_matplotlib_use.py`
- `scripts/01_generate_cartoon_protein_image_with_colored_pock/source/016_segment_sse_trace.py`
- `scripts/01_generate_cartoon_protein_image_with_colored_pock/source/017_write_cartoon_renderer_file_functions_survive_across.py`
- `scripts/01_generate_cartoon_protein_image_with_colored_pock/source/018_sys_path_insert.py`
- `scripts/01_generate_cartoon_protein_image_with_colored_pock/source/cartoon_utils.py`
- `scripts/01_identify_crbn_main_and_allosteric_pockets_from_c/source/001_check_what_lvy_print_all_hetatm_lvy.py`
- `scripts/01_identify_crbn_main_and_allosteric_pockets_from_c/source/002_parse_pdb_manually_extract_all_atom_hetatm_records.py`
- `scripts/01_identify_crbn_main_and_allosteric_pockets_from_c/source/003_main_pocket_residues_within_4_5_any_lvy_atom.py`
- `scripts/01_identify_crbn_main_and_allosteric_pockets_from_c/source/004_grid_based_cavity_detection_fpocket_lite_approach.py`
- `scripts/01_identify_crbn_main_and_allosteric_pockets_from_c/source/005_cluster_probe_points_dbscan_eps_3_min_samples_5.py`
- `scripts/01_identify_crbn_main_and_allosteric_pockets_from_c/source/006_ligsite_style_pocket_detection_each_grid_point_cast.py`
- `scripts/01_identify_crbn_main_and_allosteric_pockets_from_c/source/007_fix_count_one_hit_per_direction_6_directions_total.py`
- `scripts/01_identify_crbn_main_and_allosteric_pockets_from_c/source/008_approach_6_6_burial_aggressive_sub_clustering_map.py`
- `scripts/01_identify_crbn_main_and_allosteric_pockets_from_c/source/009_map_each_cluster_s_probe_points_surrounding_protein.py`
- `scripts/01_identify_crbn_main_and_allosteric_pockets_from_c/source/010_matplotlib_use.py`
- `scripts/01_identify_crbn_main_and_allosteric_pockets_from_c/source/011_matplotlib_use.py`
- `scripts/01_pocket_analysis_and_cartoon_visualization_for_dp/source/019_open.py`
- `scripts/01_pocket_analysis_and_cartoon_visualization_for_dp/source/020_ligsite_pocket_detection_full_complex_both_chains.py`
- `scripts/01_pocket_analysis_and_cartoon_visualization_for_dp/source/021_map_clusters_surrounding_protein_residues.py`
- `scripts/01_pocket_analysis_and_cartoon_visualization_for_dp/source/022_main_pocket_anchor_canonical_cdk2_key_residues_6.py`
- `scripts/01_pocket_analysis_and_cartoon_visualization_for_dp/source/023_broader_main_pocket_5_any_atom_anchor_residues.py`
- `scripts/01_pocket_analysis_and_cartoon_visualization_for_dp/source/024_bpdb_pdbfile_read.py`
- `scripts/01_pocket_analysis_and_cartoon_visualization_for_dp/source/025_sys_path_insert.py`
- `scripts/cartoon_utils.py`
- `scripts/drug_utils.py`
- `scripts/source/001_check_what_lvy_print_all_hetatm_lvy.py`
- `scripts/source/002_parse_pdb_manually_extract_all_atom_hetatm_records.py`
- `scripts/source/003_main_pocket_residues_within_4_5_any_lvy_atom.py`
- `scripts/source/004_grid_based_cavity_detection_fpocket_lite_approach.py`
- `scripts/source/005_cluster_probe_points_dbscan_eps_3_min_samples_5.py`
- `scripts/source/006_ligsite_style_pocket_detection_each_grid_point_cast.py`
- `scripts/source/007_fix_count_one_hit_per_direction_6_directions_total.py`
- `scripts/source/008_approach_6_6_burial_aggressive_sub_clustering_map.py`
- `scripts/source/009_map_each_cluster_s_probe_points_surrounding_protein.py`
- `scripts/source/010_matplotlib_use.py`
- `scripts/source/011_matplotlib_use.py`
- `scripts/source/012_probe_biotite_graphics_api.py`
- `scripts/source/013_load_structure_biotite_compute_secondary_structure.py`
- `scripts/source/014_build_per_residue_c_table_sse_labels_struc_annotate.py`
- `scripts/source/015_matplotlib_use.py`
- `scripts/source/016_segment_sse_trace.py`
- `scripts/source/017_write_cartoon_renderer_file_functions_survive_across.py`
- `scripts/source/018_sys_path_insert.py`
- `scripts/source/019_open.py`
- `scripts/source/020_ligsite_pocket_detection_full_complex_both_chains.py`
- `scripts/source/021_map_clusters_surrounding_protein_residues.py`
- `scripts/source/022_main_pocket_anchor_canonical_cdk2_key_residues_6.py`
- `scripts/source/023_broader_main_pocket_5_any_atom_anchor_residues.py`
- `scripts/source/024_bpdb_pdbfile_read.py`
- `scripts/source/025_sys_path_insert.py`
- `scripts/source/026_verify_cartoon_image_exists_recap_pocket_residues.py`
- `scripts/source/027_open.py`
- `scripts/source/028_ctx_atoms.py`
- `scripts/source/029_pockets_dpcdk2_ccne1_analysis_main_atp_pocket_chain.py`
- `scripts/source/030_matplotlib_use.py`
- `scripts/source/031_sys_path_insert.py`
- `scripts/source/032_pocket_druggability_descriptors_each_pocket_collect.py`
- `scripts/source/033_write_helper_disk_persists_across_calls.py`
- `scripts/source/034_sys_path_insert.py`
- `scripts/source/035_sys_path_insert.py`

## Inputs

- No inputs recorded.

## Limitations and Caveats

- This study has not been reviewed. The results are raw model output.
- Reproducibility depends on the availability of the tool images listed above.

## Provenance

Full provenance chain is in `PROVENANCE.json`. It includes: which operations were model-generated, which were reviewed, by whom, and what was approved.
