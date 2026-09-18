---
title: "Phase 1: Hit-to-lead cycle: triage → site characterisation → SAR → analogue design → docking → ADME → ranked list"
study_id: "d5c028fb-e517-477c-b564-bddb7d31c1eb"
run_id: "max-bc05ae8ea0"
phase_index: 1
phase_id: "1"
phase_goal: "Hit-to-lead cycle: triage → site characterisation → SAR → analogue design → docking → ADME → ranked list"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Hit-to-lead cycle: triage → site characterisation → SAR → analogue design → docking → ADME → ranked list

## Summary

This phase set out to hit-to-lead cycle: triage → site characterisation → SAR → analogue design → docking → ADME → ranked list. It completed 35 output files.

## Objective

Hit-to-lead cycle: triage → site characterisation → SAR → analogue design → docking → ADME → ranked list

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
| 001_chem_sdmolsupplier.py | PY | 2.2 KB | 01_running_stage_1_screen_triage/source | 4ee2b2ad8ac4... |
| 002_fix_inactive_parsing_get_active_smiles_scaffolds.py | PY | 987 B | 01_running_stage_1_screen_triage/source | da1a768aa35c... |
| 003_build_mol_objects_smiles.py | PY | 1.1 KB | 01_running_stage_1_screen_triage/source | 82217e9274ce... |
| 004_open.py | PY | 2.2 KB | 01_running_stage_1_screen_triage/source | d54a862d6357... |
| 005_precise_h_bond_analysis_donor_acceptor_pairs_within.py | PY | 2.4 KB | 01_running_stage_1_screen_triage/source | 959eb3c0cf46... |
| 006_13_15_thn_actives_exclude_eds00492874_eds00492986.py | PY | 1.0 KB | 01_running_stage_1_screen_triage/source | 350cd5b0ea67... |
| 007_explicit_designed_analogue_smiles_template_core_o_c.py | PY | 6.8 KB | 01_running_stage_1_screen_triage/source | 736cf91c30b2... |
| ligands_3d.sdf | SDF | 273.4 KB | 01_running_stage_1_screen_triage/structures | cdac8d49e048... |
| receptor_stripped.pdb | PDB | 363.1 KB | 01_running_stage_1_screen_triage/structures | 82142ae2541e... |
| 008_write_all_compounds_sdf_etkdg_3d_coords_includes_15.py | PY | 2.5 KB | 01_running_stage_1_screen_triage/source | 09d056ac091f... |
| 009_run_aidd_tool.py | PY | 1.4 KB | 01_running_stage_1_screen_triage/source | c4910f711a03... |
| 010_write_actives_only_sdf.py | PY | 974 B | 01_running_stage_1_screen_triage/source | c061cd328c4a... |
| 011_check_what_variables_available_prior_session.py | PY | 474 B | 01_running_stage_1_screen_triage/source | 1a887523ab28... |
| 013_check_results_directory_any_gnina_output.csv | CSV | 760 B | 01_running_stage_1_screen_triage/tables | 3e19b3c10f4c... |
| 012_check_results_directory_any_gnina_output.py | PY | 331 B | 01_running_stage_1_screen_triage/source | 98dda07d0415... |
| 013_check_structure_all_cpds.py | PY | 282 B | 01_running_stage_1_screen_triage/source | d5443cf2c7d5... |
| 014_read_back_sdf_get_names.py | PY | 402 B | 01_running_stage_1_screen_triage/source | 3856d84aa777... |
| batch_actives.sdf | SDF | 78.3 KB | 01_running_stage_1_screen_triage/structures | 928ed1504b26... |
| batch_des1.sdf | SDF | 96.2 KB | 01_running_stage_1_screen_triage/structures | 7e626392f45c... |
| batch_des2.sdf | SDF | 98.9 KB | 01_running_stage_1_screen_triage/structures | b9b39a5435c3... |
| 015_list.py | PY | 754 B | 01_running_stage_1_screen_triage/source | 218a66190d22... |
| gnina_docked.sdf.gz | GZ | 69.4 KB | 01_running_stage_1_screen_triage/structures | 0b7cfeeafa56... |
| 016_run_aidd_tool.py | PY | 455 B | 01_running_stage_1_screen_triage/source | 7b8a2ac45422... |
| gnina_docked.sdf.gz | GZ | 70.4 KB | 01_running_stage_1_screen_triage/structures | fa364e8a1600... |
| 017_run_aidd_tool.py | PY | 753 B | 01_running_stage_1_screen_triage/source | 5e373abf1cff... |
| actives_docked.sdf.gz | GZ | 70.4 KB | 01_running_stage_1_screen_triage/structures | fa364e8a1600... |
| 018_shutil_copy.py | PY | 857 B | 01_running_stage_1_screen_triage/source | be91dc5591ac... |
| des1_docked.sdf.gz | GZ | 91.3 KB | 01_running_stage_1_screen_triage/structures | 5bb88505a4dd... |
| des2_docked.sdf.gz | GZ | 92.3 KB | 01_running_stage_1_screen_triage/structures | 9fcbe1b332df... |
| gnina_docked.sdf.gz | GZ | 92.3 KB | 01_running_stage_1_screen_triage/structures | 9fcbe1b332df... |
| 019_dict.py | PY | 950 B | 01_running_stage_1_screen_triage/source | 841753ad85a4... |
| 020_parse_docked.py | PY | 1.4 KB | 01_running_stage_1_screen_triage/source | 6421187669ef... |
| 021_list.py | PY | 2.1 KB | 01_running_stage_1_screen_triage/source | 4241da32aa89... |
| 022_merge_docking_scores_adme.py | PY | 1.1 KB | 01_running_stage_1_screen_triage/source | e0e6dac6ad12... |
| 023_build_r_group_annotation_dict_source.py | PY | 2.9 KB | 01_running_stage_1_screen_triage/source | f836db89c35e... |

## Verification

- No tool call is on record for this phase.
- 35 file(s) were produced and registered, 35 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/gnina:latest`

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
