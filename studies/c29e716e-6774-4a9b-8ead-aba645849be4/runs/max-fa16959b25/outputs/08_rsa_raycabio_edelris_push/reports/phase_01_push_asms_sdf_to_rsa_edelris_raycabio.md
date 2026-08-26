---
title: "Phase 1: Push ASMS SDF to RSA-Edelris/RaycaBio"
study_id: "c29e716e-6774-4a9b-8ead-aba645849be4"
run_id: "max-1c44e6be7e"
phase_index: 1
phase_id: "1"
phase_goal: "Push ASMS SDF to RSA-Edelris/RaycaBio"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Push ASMS SDF to RSA-Edelris/RaycaBio

## Summary

This phase set out to push ASMS SDF to RSA-Edelris/RaycaBio. It completed 55 output files.

## Objective

Push ASMS SDF to RSA-Edelris/RaycaBio

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
| 001_step_1_read_sdf_inspect_structure.py | PY | 723 B | 01_asms_p841_pains_substructures/source | 84d905a9b804... |
| 002_sdmolsupplier.py | PY | 602 B | 01_asms_p841_pains_substructures/source | 6ce62ccc0d89... |
| 003_examine_activity_column_key_fields.py | PY | 429 B | 01_asms_p841_pains_substructures/source | 9d1397174540... |
| 004_step_2_structure_standardization_salt_removal.py | PY | 1.9 KB | 01_asms_p841_pains_substructures/source | c649b29bb2d8... |
| 005_print.py | PY | 123 B | 01_asms_p841_pains_substructures/source | 8f8d61bb7a4a... |
| 006_rdmolstandardize_largestfragmentchooser.py | PY | 2.2 KB | 01_asms_p841_pains_substructures/source | 07b5066aba3a... |
| 007_step_3_deduplication_across_classes.py | PY | 1.2 KB | 01_asms_p841_pains_substructures/source | 14122276e887... |
| 008_step_4_pains_filter_actives.py | PY | 1.7 KB | 01_asms_p841_pains_substructures/source | 507be482ba82... |
| 009_step_5_aggregator_reactive_frequent_hitter_checks.py | PY | 3.9 KB | 01_asms_p841_pains_substructures/source | b6785e4ed8a0... |
| 010_step_6_asms_specific_artefact_analysis_scaffold.py | PY | 2.1 KB | 01_asms_p841_pains_substructures/source | 86287c60846f... |
| 011_fix_convert_pd_numeric.py | PY | 1.9 KB | 01_asms_p841_pains_substructures/source | 5338de747c7c... |
| 012_step_7_decode_scaffold_analyze_r_groups_scaffold.py | PY | 1.5 KB | 01_asms_p841_pains_substructures/source | 6f9fa740c22f... |
| 013_step_8_propose_20_new_compounds_design_based_sar.py | PY | 6.3 KB | 01_asms_p841_pains_substructures/source | e137790ecccc... |
| 014_fix_flagged_compounds_revalidate_full_set_20.py | PY | 6.0 KB | 01_asms_p841_pains_substructures/source | 645a82ee11fd... |
| report.md | MD | 19.4 KB | unphased/reports | 0bd06043dcb3... |
| phase_01_asms_hit_triage_pipeline.md | MD | 3.1 KB | 01_asms_p841_pains_substructures/reports | 7041a481e92d... |
| P841_proposed_actives.sdf | SDF | 0 B | 03_rsa_roycabio_structure_github/structures | e3b0c44298fc... |
| 015_c1ccc2c.py | PY | 4.6 KB | 03_rsa_roycabio_structure_github/source | 290878ba55a9... |
| P841_proposed_actives.sdf | SDF | 68.8 KB | 03_rsa_roycabio_structure_github/structures | 2e14e9264fac... |
| 016_sdwriter.py | PY | 1.1 KB | 03_rsa_roycabio_structure_github/source | 798936ce525c... |
| phase_01_push_asms_sdf_to_rsa_edelrsi_raycabio.md | MD | 3.8 KB | 04_rsa_raycabio_edelrsi_push/reports | c763d467e852... |
| Cedilla_list.sdf | SDF | 1.1 MB | uploads | cca65c47728d... |
| P841_proposed_actives.sdf | SDF | 68.8 KB | uploads | 2e14e9264fac... |
| 017_rdmolstandardize_largestfragmentchooser.py | PY | 2.1 KB | 05_p841_structures_proposed_list/source | 93fca315c7de... |
| phase_01_cross_check_p841_proposed_actives_vs_cedilla_lis.md | MD | 1.7 KB | 05_p841_structures_proposed_list/reports | 4eb9a3c67689... |
| ASMS_active.sdf | SDF | 36.0 KB | uploads | 2e4ab976db8a... |
| 018_load_sdf.py | PY | 1.3 KB | 06_asms_analysis_compare_cedilla/source | c8d3d854d599... |
| 019_standardize_both_sets.py | PY | 3.2 KB | 06_asms_analysis_compare_cedilla/source | 9300cf01a6f8... |
| 020_step_1_which_pains_rule_dominates_cedilla.py | PY | 1.7 KB | 06_asms_analysis_compare_cedilla/source | 2d7927ad2af9... |
| 021_step_3_cedilla_sar_overview_pic50_landscape.py | PY | 1.2 KB | 06_asms_analysis_compare_cedilla/source | 5b9d5d275f4d... |
| 022_step_4_tanimoto_similarity_asms_actives_vs_cedilla.py | PY | 1.6 KB | 06_asms_analysis_compare_cedilla/source | 0b8f5c97c143... |
| 023_step_5_investigate_ctx_1019480_vs_eds00490706.py | PY | 1.9 KB | 06_asms_analysis_compare_cedilla/source | caee6d8e429a... |
| 024_step_6_top_20_cedilla_full_asms_vs_cedilla.py | PY | 1.8 KB | 06_asms_analysis_compare_cedilla/source | be1b3214adf9... |
| 025_fix_duplicates_cedilla_mcs_top_compounds.py | PY | 1.8 KB | 06_asms_analysis_compare_cedilla/source | 0cc17e87bf48... |
| 026_step_7_structural_analysis_top_cedilla_asms_actives.py | PY | 2.2 KB | 06_asms_analysis_compare_cedilla/source | ab598e93b5e3... |
| 027_step_8_complete_asms_vs_cedilla_comparison_table.py | PY | 1.3 KB | 06_asms_analysis_compare_cedilla/source | 284a5e2e5c34... |
| report_asms_vs_cedilla.md | MD | 13.6 KB | unphased/reports | c25bbdb1c0ed... |
| phase_01_asms_active_vs_cedilla_list_triage.md | MD | 2.8 KB | 06_asms_analysis_compare_cedilla/reports | b30433d94b63... |
| 05-Amidation_Amine_Acyl_chloride_38_unique_vs_acids.sdf | SDF | 42.7 KB | uploads | f47948e9e8d3... |
| 05-Amidation_Amine_Acyl_chloride_70.sdf | SDF | 80.4 KB | uploads | 3108628b9d49... |
| 01_RedAm_Amine_Aldehyde_169_PSR60-NBoc.sdf | SDF | 192.2 KB | uploads | 002546f7ee65... |
| 03-Amidation_Amine_Acid_353_PSR70-NBoc.sdf | SDF | 426.8 KB | uploads | fcc9354d47e8... |
| 04-Amidation_Acid_Amine _140.sdf | SDF | 152.0 KB | uploads | cb637a85eeb7... |
| 029_load_sdf.csv | CSV | 708 B | 07_asms_oc_c1ccc2ccncc2n1_create/tables | 8e4f2ed8783a... |
| 028_load_sdf.py | PY | 1.2 KB | 07_asms_oc_c1ccc2ccncc2n1_create/source | 276b95c3f92f... |
| 029_understand_reaction_types_reagent_categories.py | PY | 503 B | 07_asms_oc_c1ccc2ccncc2n1_create/source | 449923f45785... |
| 030_scaffold.py | PY | 1.7 KB | 07_asms_oc_c1ccc2ccncc2n1_create/source | 457873809ff1... |
| 031_enumerate_all_n_modified_intermediates_pool_n.py | PY | 1.8 KB | 07_asms_oc_c1ccc2ccncc2n1_create/source | 247aa3524642... |
| 032_asms_actives_smiles_prior_analysis.py | PY | 3.6 KB | 07_asms_oc_c1ccc2ccncc2n1_create/source | 4784c4572fb2... |
| 033_select_top_200_sort_asms_similarity_apply_diversity.py | PY | 374 B | 07_asms_oc_c1ccc2ccncc2n1_create/source | 037c0de4a96a... |
| 034_check_sim_1_0_hit.py | PY | 1.3 KB | 07_asms_oc_c1ccc2ccncc2n1_create/source | efc1ff9293d3... |
| 035_rebalanced_selection_top_170_amides_top_30_redam.py | PY | 1.5 KB | 07_asms_oc_c1ccc2ccncc2n1_create/source | 770146fa9508... |
| library_200.sdf | SDF | 606.6 KB | 07_asms_oc_c1ccc2ccncc2n1_create/structures | 01d9aeb2feb7... |
| 036_sdwriter.py | PY | 1.8 KB | 07_asms_oc_c1ccc2ccncc2n1_create/source | 440b686b5710... |
| phase_01_build_200_compound_library_from_scaffold.md | MD | 2.8 KB | 07_asms_oc_c1ccc2ccncc2n1_create/reports | 9ce982ea8997... |

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
