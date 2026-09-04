---
title: "Phase 1: IC50 estimation for 20 proposed compounds"
study_id: "c29e716e-6774-4a9b-8ead-aba645849be4"
run_id: "max-1b3ebc666a"
phase_index: 1
phase_id: "1"
phase_goal: "IC50 estimation for 20 proposed compounds"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: IC50 estimation for 20 proposed compounds

## Summary

This phase set out to iC50 estimation for 20 proposed compounds. It completed 79 output files.

## Objective

IC50 estimation for 20 proposed compounds

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
| 050_open.py | PY | 594 B | 12_ic50_structures_estimate/source | abb2691fef0b... |
| 051_rayca_tools_aidd_tool_schema.py | PY | 70 B | 12_ic50_structures_estimate/source | 65561a250980... |
| 052_memory_about.py | PY | 59 B | 12_ic50_structures_estimate/source | d909165a7240... |
| 053_memory_about.py | PY | 57 B | 12_ic50_structures_estimate/source | 6822fc07b3c3... |
| 054_run_fpocket_target_pdb.py | PY | 490 B | 12_ic50_structures_estimate/source | 999ca5f0490c... |
| 055_dispatch.py | PY | 262 B | 12_ic50_structures_estimate/source | 84eed8e1a302... |
| 056_dispatch.py | PY | 254 B | 12_ic50_structures_estimate/source | 427d46a05133... |
| 057_memory_about.py | PY | 62 B | 12_ic50_structures_estimate/source | d9c8c95785bd... |
| 058_pdbfile_input_field_not_file_upload.py | PY | 419 B | 12_ic50_structures_estimate/inputs | 4e1ac638f661... |
| 059_pdb_too_large_inline_arg_pass_file.py | PY | 524 B | 12_ic50_structures_estimate/source | be24e06abfaf... |
| anchor.sdf | SDF | 4.1 KB | 12_ic50_structures_estimate/structures | a2637585c1ac... |
| 060_strip_waters_pdb.py | PY | 1.1 KB | 12_ic50_structures_estimate/source | 6d507fbcf216... |
| target_clean.pdb | PDB | 363.2 KB | 12_ic50_structures_estimate/structures | a378d351ac02... |
| 061_blind_docking_anchor_compound_find_binding_site.py | PY | 852 B | 12_ic50_structures_estimate/source | 9f5b1ea38494... |
| 062_open.py | PY | 797 B | 12_ic50_structures_estimate/source | b7f5560034c0... |
| gnina_docked.sdf.gz | GZ | 4.1 KB | 12_ic50_structures_estimate/work | 741db605ea86... |
| 063_open.py | PY | 764 B | 12_ic50_structures_estimate/source | cc8851cf547a... |
| 064_read_docked_sdf_output.py | PY | 293 B | 12_ic50_structures_estimate/source | f1d18180db8b... |
| 065_parse_all_poses_gnina_output_sdf.py | PY | 1.2 KB | 12_ic50_structures_estimate/source | 0a68fee120db... |
| all_35_ligands.sdf | SDF | 173.3 KB | 12_ic50_structures_estimate/structures | 3b665d02d047... |
| 066_all_35_compounds_15_known_actives_20_proposed.py | PY | 4.0 KB | 12_ic50_structures_estimate/source | cdeb3ceda13b... |
| 067_focused_docking_all_35_ligands_box_center_top_blind.py | PY | 766 B | 12_ic50_structures_estimate/source | 88b7e8e8ff39... |
| dock_helper.py | PY | 2.5 KB | 12_ic50_structures_estimate/source | e949fbea2d85... |
| 068_write_docking_helper_function_file_persists_across.py | PY | 2.9 KB | 12_ic50_structures_estimate/source | b0aa7e0452c7... |
| 069_make_sdf.py | PY | 2.2 KB | 12_ic50_structures_estimate/source | 62a8936f4c60... |
| 070_memory_about.py | PY | 69 B | 12_ic50_structures_estimate/source | 39f34678b187... |
| autodock-vina-results.json | JSON | 481 B | 12_ic50_structures_estimate/work | 271a6dd0971f... |
| 071_test_autodock_vina_one_compound_ligandsmiles_input.py | PY | 735 B | 12_ic50_structures_estimate/inputs | 56371ab8689c... |
| 072_open.py | PY | 377 B | 12_ic50_structures_estimate/source | 51f314e10987... |
| autodock-vina-results-2.json | JSON | 506 B | 12_ic50_structures_estimate/work | f9dd034caf53... |
| autodock-vina-results-3.json | JSON | 505 B | 12_ic50_structures_estimate/work | 77098ac6701a... |
| autodock-vina-results-4.json | JSON | 507 B | 12_ic50_structures_estimate/work | 1bb5e86e98d7... |
| autodock-vina-results-5.json | JSON | 504 B | 12_ic50_structures_estimate/work | 95db2db9c670... |
| autodock-vina-results-6.json | JSON | 493 B | 12_ic50_structures_estimate/work | f9d67340a830... |
| docking_results.json | JSON | 552 B | 12_ic50_structures_estimate/work | 5db5ec9df123... |
| 073_dock_one.py | PY | 1.6 KB | 12_ic50_structures_estimate/source | b4d8bb0bf424... |
| 074_sorted.py | PY | 430 B | 12_ic50_structures_estimate/source | e3b4a3029202... |
| 075_sorted.py | PY | 1.5 KB | 12_ic50_structures_estimate/source | 7ee96a264f6c... |
| 076_sorted.py | PY | 1016 B | 12_ic50_structures_estimate/source | 52b1fa1a2901... |
| autodock-vina-results-10.json | JSON | 503 B | 12_ic50_structures_estimate/work | 849b825cfef2... |
| autodock-vina-results-7.json | JSON | 497 B | 12_ic50_structures_estimate/work | be6264a4a45f... |
| autodock-vina-results-8.json | JSON | 495 B | 12_ic50_structures_estimate/work | 6be985e3a588... |
| autodock-vina-results-9.json | JSON | 504 B | 12_ic50_structures_estimate/work | dcdb32213a11... |
| 077_dock_read.py | PY | 1.3 KB | 12_ic50_structures_estimate/source | 3f0530f8695c... |
| autodock-vina-results-11.json | JSON | 494 B | 12_ic50_structures_estimate/work | 86a90c987034... |
| autodock-vina-results-12.json | JSON | 502 B | 12_ic50_structures_estimate/work | 6a0a171fce51... |
| autodock-vina-results-13.json | JSON | 493 B | 12_ic50_structures_estimate/work | 4eb0c4c6b1c9... |
| autodock-vina-results-14.json | JSON | 488 B | 12_ic50_structures_estimate/work | 26a8278ac626... |
| autodock-vina-results-15.json | JSON | 501 B | 12_ic50_structures_estimate/work | 535652f2c9d9... |
| autodock-vina-results-16.json | JSON | 497 B | 12_ic50_structures_estimate/work | e2d7ab0da014... |
| autodock-vina-results-17.json | JSON | 505 B | 12_ic50_structures_estimate/work | f5954e21a185... |
| 078_dock_read.py | PY | 1.3 KB | 12_ic50_structures_estimate/source | d6605bc7186b... |
| autodock-vina-results-18.json | JSON | 504 B | 12_ic50_structures_estimate/work | bbcba6b2917c... |
| autodock-vina-results-19.json | JSON | 492 B | 12_ic50_structures_estimate/work | 02c308844fa3... |
| autodock-vina-results-20.json | JSON | 492 B | 12_ic50_structures_estimate/work | dbe49694d262... |
| autodock-vina-results-21.json | JSON | 495 B | 12_ic50_structures_estimate/work | 73d0f876c4bd... |
| autodock-vina-results-22.json | JSON | 508 B | 12_ic50_structures_estimate/work | 5ae88d96e785... |
| 079_dock_read.py | PY | 1.4 KB | 12_ic50_structures_estimate/source | 47a5c7488ee8... |
| autodock-vina-results-23.json | JSON | 498 B | 12_ic50_structures_estimate/work | 4ff529c0bccf... |
| autodock-vina-results-24.json | JSON | 498 B | 12_ic50_structures_estimate/work | e11257cfb4eb... |
| autodock-vina-results-25.json | JSON | 487 B | 12_ic50_structures_estimate/work | dc98756d3166... |
| autodock-vina-results-26.json | JSON | 495 B | 12_ic50_structures_estimate/work | c6716c4be7a9... |
| autodock-vina-results-27.json | JSON | 498 B | 12_ic50_structures_estimate/work | 19a7115b1bf5... |
| 080_dock_read.py | PY | 1.3 KB | 12_ic50_structures_estimate/source | 2c519a8d4118... |
| autodock-vina-results-28.json | JSON | 500 B | 12_ic50_structures_estimate/work | cd572438fb5f... |
| autodock-vina-results-29.json | JSON | 500 B | 12_ic50_structures_estimate/work | 275def8a94c5... |
| autodock-vina-results-30.json | JSON | 507 B | 12_ic50_structures_estimate/work | bf3781b72db8... |
| autodock-vina-results-31.json | JSON | 489 B | 12_ic50_structures_estimate/work | b953a38e372f... |
| autodock-vina-results-32.json | JSON | 497 B | 12_ic50_structures_estimate/work | a5ed684248ad... |
| 081_dock_read.py | PY | 1.4 KB | 12_ic50_structures_estimate/source | 21a6b5a23946... |
| autodock-vina-results-33.json | JSON | 497 B | 12_ic50_structures_estimate/work | a366b4e3a550... |
| autodock-vina-results-34.json | JSON | 494 B | 12_ic50_structures_estimate/work | f060fd8055fe... |
| autodock-vina-results-35.json | JSON | 498 B | 12_ic50_structures_estimate/work | 7bd34a652505... |
| 082_dock_read.py | PY | 1.3 KB | 12_ic50_structures_estimate/source | 3cfbe287f472... |
| 083_known_actives_name_smiles_ratio.py | PY | 250 B | 12_ic50_structures_estimate/source | 77f10b79ec0f... |
| 084_calibration_using_known_actives.py | PY | 1.7 KB | 12_ic50_structures_estimate/source | d11d3e6f4943... |
| 085_ic50_proxy.py | PY | 2.0 KB | 12_ic50_structures_estimate/source | 5a4a46bc3556... |
| ic50_report.md | MD | 4.6 KB | 12_ic50_structures_estimate/reports | 9f9ecf1defab... |
| 086_cal_ic50.py | PY | 3.8 KB | 12_ic50_structures_estimate/source | dff26afa2bc9... |

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
