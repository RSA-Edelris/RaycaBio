---
title: "Phase 1: Push ASMS SDF to RSA-Edelrsi/RaycaBio"
study_id: "c29e716e-6774-4a9b-8ead-aba645849be4"
run_id: "max-4b2db9839b"
phase_index: 1
phase_id: "1"
phase_goal: "Push ASMS SDF to RSA-Edelrsi/RaycaBio"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Push ASMS SDF to RSA-Edelrsi/RaycaBio

## Summary

This phase set out to push ASMS SDF to RSA-Edelrsi/RaycaBio. It completed 20 output files.

## Objective

Push ASMS SDF to RSA-Edelrsi/RaycaBio

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

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
