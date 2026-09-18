---
title: "Phase 1: Identify CRBN main and allosteric pockets from CRBN.pdb"
study_id: "9d335ae8-a19c-4b53-89e1-813dc8783c51"
run_id: "max-0af10a2f62"
phase_index: 1
phase_id: "1"
phase_goal: "Identify CRBN main and allosteric pockets from CRBN.pdb"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Identify CRBN main and allosteric pockets from CRBN.pdb

## Summary

This phase set out to identify CRBN main and allosteric pockets from CRBN.pdb. It completed 14 output files.

## Objective

Identify CRBN main and allosteric pockets from CRBN.pdb

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

## Verification

- No tool call is on record for this phase.
- 14 file(s) were produced and registered, 14 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
