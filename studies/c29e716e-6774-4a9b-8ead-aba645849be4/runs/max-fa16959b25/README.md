# Study: c29e716e-6774-4a9b-8ead-aba645849be4

> WARNING: This study has NOT been reviewed. Results are unreviewed model output and must not be cited or relied upon without independent verification.

## Run Identity

- Run ID: `max-fa16959b25`
- Published: 2026-08-26T11:06:04Z
- Review: not reviewed

## Tools and Environment

- No tool version information recorded.

## Outputs

Files included in this repository:

- `outputs/01_asms_p841_pains_substructures/reports/phase_01_asms_hit_triage_pipeline.md` (3206 bytes)
- `outputs/03_rsa_roycabio_structure_github/structures/P841_proposed_actives(2).sdf` (70418 bytes)
- `outputs/03_rsa_roycabio_structure_github/structures/P841_proposed_actives.sdf` (0 bytes)
- `outputs/04_rsa_raycabio_edelrsi_push/reports/phase_01_push_asms_sdf_to_rsa_edelrsi_raycabio.md` (3856 bytes)
- `outputs/05_p841_structures_proposed_list/reports/phase_01_cross_check_p841_proposed_actives_vs_cedilla_lis.md` (1765 bytes)
- `outputs/06_asms_analysis_compare_cedilla/reports/phase_01_asms_active_vs_cedilla_list_triage.md` (2816 bytes)
- `outputs/07_asms_oc_c1ccc2ccncc2n1_create/reports/phase_01_build_200_compound_library_from_scaffold.md` (2828 bytes)
- `outputs/07_asms_oc_c1ccc2ccncc2n1_create/structures/library_200.sdf` (621133 bytes)
- `outputs/07_asms_oc_c1ccc2ccncc2n1_create/tables/029_load_sdf.csv` (708 bytes)
- `outputs/08_rsa_raycabio_edelris_push/reports/phase_01_push_asms_sdf_to_rsa_edelris_raycabio.md` (7726 bytes)
- `outputs/09_002_200_compounds_library/reports/phase_01_cross_check_002_library_200_vs_cedilla_list.md` (1808 bytes)
- `outputs/11_rsa_raycabio_structures_write/structures/P841_proposed_20(2).sdf` (69417 bytes)
- `outputs/unphased/reports/report.md` (19847 bytes)
- `outputs/unphased/reports/report_asms_vs_cedilla.md` (13946 bytes)
- `outputs/unphased/reports/report_sorted_841_train.md` (19199 bytes)
- `outputs/uploads/01_RedAm_Amine_Aldehyde_169_PSR60-NBoc.sdf` (196823 bytes)
- `outputs/uploads/03-Amidation_Amine_Acid_353_PSR70-NBoc.sdf` (437001 bytes)
- `outputs/uploads/04-Amidation_Acid_Amine _140.sdf` (155614 bytes)
- `outputs/uploads/05-Amidation_Amine_Acyl_chloride_38_unique_vs_acids.sdf` (43675 bytes)
- `outputs/uploads/05-Amidation_Amine_Acyl_chloride_70.sdf` (82331 bytes)
- `outputs/uploads/ASMS_active.sdf` (36869 bytes)
- `outputs/uploads/Cedilla_list.sdf` (1138987 bytes)
- `outputs/uploads/Sorted_841_train.dwar` (16172 bytes)
- `outputs/uploads/Sorted_841_train.sdf` (135543 bytes)

## Scripts

- `scripts/01_asms_p841_pains_substructures/source/001_step_1_read_sdf_inspect_structure.py`
- `scripts/01_asms_p841_pains_substructures/source/002_sdmolsupplier.py`
- `scripts/01_asms_p841_pains_substructures/source/003_examine_activity_column_key_fields.py`
- `scripts/01_asms_p841_pains_substructures/source/004_step_2_structure_standardization_salt_removal.py`
- `scripts/01_asms_p841_pains_substructures/source/005_print.py`
- `scripts/01_asms_p841_pains_substructures/source/006_rdmolstandardize_largestfragmentchooser.py`
- `scripts/01_asms_p841_pains_substructures/source/007_step_3_deduplication_across_classes.py`
- `scripts/01_asms_p841_pains_substructures/source/008_step_4_pains_filter_actives.py`
- `scripts/01_asms_p841_pains_substructures/source/009_step_5_aggregator_reactive_frequent_hitter_checks.py`
- `scripts/01_asms_p841_pains_substructures/source/010_step_6_asms_specific_artefact_analysis_scaffold.py`
- `scripts/01_asms_p841_pains_substructures/source/011_fix_convert_pd_numeric.py`
- `scripts/01_asms_p841_pains_substructures/source/012_step_7_decode_scaffold_analyze_r_groups_scaffold.py`
- `scripts/01_asms_p841_pains_substructures/source/013_step_8_propose_20_new_compounds_design_based_sar.py`
- `scripts/01_asms_p841_pains_substructures/source/014_fix_flagged_compounds_revalidate_full_set_20.py`
- `scripts/03_rsa_roycabio_structure_github/source/015_c1ccc2c.py`
- `scripts/03_rsa_roycabio_structure_github/source/016_sdwriter.py`
- `scripts/05_p841_structures_proposed_list/source/017_rdmolstandardize_largestfragmentchooser.py`
- `scripts/06_asms_analysis_compare_cedilla/source/018_load_sdf.py`
- `scripts/06_asms_analysis_compare_cedilla/source/019_standardize_both_sets.py`
- `scripts/06_asms_analysis_compare_cedilla/source/020_step_1_which_pains_rule_dominates_cedilla.py`
- `scripts/06_asms_analysis_compare_cedilla/source/021_step_3_cedilla_sar_overview_pic50_landscape.py`
- `scripts/06_asms_analysis_compare_cedilla/source/022_step_4_tanimoto_similarity_asms_actives_vs_cedilla.py`
- `scripts/06_asms_analysis_compare_cedilla/source/023_step_5_investigate_ctx_1019480_vs_eds00490706.py`
- `scripts/06_asms_analysis_compare_cedilla/source/024_step_6_top_20_cedilla_full_asms_vs_cedilla.py`
- `scripts/06_asms_analysis_compare_cedilla/source/025_fix_duplicates_cedilla_mcs_top_compounds.py`
- `scripts/06_asms_analysis_compare_cedilla/source/026_step_7_structural_analysis_top_cedilla_asms_actives.py`
- `scripts/06_asms_analysis_compare_cedilla/source/027_step_8_complete_asms_vs_cedilla_comparison_table.py`
- `scripts/07_asms_oc_c1ccc2ccncc2n1_create/source/028_load_sdf.py`
- `scripts/07_asms_oc_c1ccc2ccncc2n1_create/source/029_understand_reaction_types_reagent_categories.py`
- `scripts/07_asms_oc_c1ccc2ccncc2n1_create/source/030_scaffold.py`
- `scripts/07_asms_oc_c1ccc2ccncc2n1_create/source/031_enumerate_all_n_modified_intermediates_pool_n.py`
- `scripts/07_asms_oc_c1ccc2ccncc2n1_create/source/032_asms_actives_smiles_prior_analysis.py`
- `scripts/07_asms_oc_c1ccc2ccncc2n1_create/source/033_select_top_200_sort_asms_similarity_apply_diversity.py`
- `scripts/07_asms_oc_c1ccc2ccncc2n1_create/source/034_check_sim_1_0_hit.py`
- `scripts/07_asms_oc_c1ccc2ccncc2n1_create/source/035_rebalanced_selection_top_170_amides_top_30_redam.py`
- `scripts/07_asms_oc_c1ccc2ccncc2n1_create/source/036_sdwriter.py`
- `scripts/09_002_200_compounds_library/source/037_load_inchikeys.py`
- `scripts/09_002_200_compounds_library/source/038_exact_match_inchikey.py`
- `scripts/10_841_pains_ic50_substructures/source/039_sdmolsupplier.py`
- `scripts/10_841_pains_ic50_substructures/source/040_standardize.py`
- `scripts/10_841_pains_ic50_substructures/source/041_deduplication.py`
- `scripts/10_841_pains_ic50_substructures/source/042_full_dataset_sorted_pic50_examine_top_15_structure.py`
- `scripts/10_841_pains_ic50_substructures/source/043_examine_target_protein_class_pdb.py`
- `scripts/10_841_pains_ic50_substructures/source/044_full_smiles_pic50_ranked_need_understand_all_r1_r2.py`
- `scripts/10_841_pains_ic50_substructures/source/045_correlate_physicochemical_properties_pic50_clean_non.py`
- `scripts/10_841_pains_ic50_substructures/source/046_build_validate_20_new_proposals_key_sar_best_r1_3_cl.py`
- `scripts/10_841_pains_ic50_substructures/source/047_replace_b4_e3_better_sized_compounds_write_final.py`
- `scripts/11_rsa_raycabio_structures_write/source/048_c1ccc2c.py`
- `scripts/11_rsa_raycabio_structures_write/source/049_sdwriter.py`
- `scripts/source/001_step_1_read_sdf_inspect_structure.py`
- `scripts/source/002_sdmolsupplier.py`
- `scripts/source/003_examine_activity_column_key_fields.py`
- `scripts/source/004_step_2_structure_standardization_salt_removal.py`
- `scripts/source/005_print.py`
- `scripts/source/006_rdmolstandardize_largestfragmentchooser.py`
- `scripts/source/007_step_3_deduplication_across_classes.py`
- `scripts/source/008_step_4_pains_filter_actives.py`
- `scripts/source/009_step_5_aggregator_reactive_frequent_hitter_checks.py`
- `scripts/source/010_step_6_asms_specific_artefact_analysis_scaffold.py`
- `scripts/source/011_fix_convert_pd_numeric.py`
- `scripts/source/012_step_7_decode_scaffold_analyze_r_groups_scaffold.py`
- `scripts/source/013_step_8_propose_20_new_compounds_design_based_sar.py`
- `scripts/source/014_fix_flagged_compounds_revalidate_full_set_20.py`
- `scripts/source/015_c1ccc2c.py`
- `scripts/source/016_sdwriter.py`
- `scripts/source/017_rdmolstandardize_largestfragmentchooser.py`
- `scripts/source/018_load_sdf.py`
- `scripts/source/019_standardize_both_sets.py`
- `scripts/source/020_step_1_which_pains_rule_dominates_cedilla.py`
- `scripts/source/021_step_3_cedilla_sar_overview_pic50_landscape.py`
- `scripts/source/022_step_4_tanimoto_similarity_asms_actives_vs_cedilla.py`
- `scripts/source/023_step_5_investigate_ctx_1019480_vs_eds00490706.py`
- `scripts/source/024_step_6_top_20_cedilla_full_asms_vs_cedilla.py`
- `scripts/source/025_fix_duplicates_cedilla_mcs_top_compounds.py`
- `scripts/source/026_step_7_structural_analysis_top_cedilla_asms_actives.py`
- `scripts/source/027_step_8_complete_asms_vs_cedilla_comparison_table.py`
- `scripts/source/028_load_sdf.py`
- `scripts/source/029_understand_reaction_types_reagent_categories.py`
- `scripts/source/030_scaffold.py`
- `scripts/source/031_enumerate_all_n_modified_intermediates_pool_n.py`
- `scripts/source/032_asms_actives_smiles_prior_analysis.py`
- `scripts/source/033_select_top_200_sort_asms_similarity_apply_diversity.py`
- `scripts/source/034_check_sim_1_0_hit.py`
- `scripts/source/035_rebalanced_selection_top_170_amides_top_30_redam.py`
- `scripts/source/036_sdwriter.py`
- `scripts/source/037_load_inchikeys.py`
- `scripts/source/038_exact_match_inchikey.py`
- `scripts/source/039_sdmolsupplier.py`
- `scripts/source/040_standardize.py`
- `scripts/source/041_deduplication.py`
- `scripts/source/042_full_dataset_sorted_pic50_examine_top_15_structure.py`
- `scripts/source/043_examine_target_protein_class_pdb.py`
- `scripts/source/044_full_smiles_pic50_ranked_need_understand_all_r1_r2.py`
- `scripts/source/045_correlate_physicochemical_properties_pic50_clean_non.py`
- `scripts/source/046_build_validate_20_new_proposals_key_sar_best_r1_3_cl.py`
- `scripts/source/047_replace_b4_e3_better_sized_compounds_write_final.py`
- `scripts/source/048_c1ccc2c.py`
- `scripts/source/049_sdwriter.py`

## Inputs

- No inputs recorded.

## Limitations and Caveats

- This study has not been reviewed. The results are raw model output.
- Reproducibility depends on the availability of the tool images listed above.

## Provenance

Full provenance chain is in `PROVENANCE.json`. It includes: which operations were model-generated, which were reviewed, by whom, and what was approved.
