---
title: "Phase 5: Write docking report with figures and table"
study_id: "8b0911d7-7cc1-48cd-ae66-83c2c10d0be3"
run_id: "max-857321d628"
phase_index: 5
phase_id: "5"
phase_goal: "Write docking report with figures and table"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 5: Write docking report with figures and table

## Summary

This phase set out to write docking report with figures and table. It completed 4 method steps, 75 output files.

## Objective

Write docking report with figures and table

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

**Table R.** Key resources used in this phase. Versions are as reported by the running environment; identifiers follow the FORCE11 software citation principles.

| Resource | Type | Version | Identifier | Source |
| :--- | :--- | :--- | :--- | :--- |
| numpy | software | 1.26.4 | doi:10.1038/s41586-020-2649-2 | https://numpy.org |
| RDKit | software | 2023.9.6 | doi:10.5281/zenodo.591637 | https://www.rdkit.org |

### Procedure

#### 1. Binding site identification from co-crystal ligand

The binding pocket was identified by parsing the FRJ co-crystal ligand coordinates from the input PDB structure and identifying all receptor residues within 5 Å of any FRJ heavy atom.

**Rationale.** Co-crystal ligand position defines the allosteric binding site for subsequent docking calculations.

| Field | Value |
| :--- | :--- |
| Inputs | 9C56.pdb |
| Libraries | numpy |
| Status | running |

Parameters:

```yaml
distance_cutoff_angstrom: 5.0
```

#### 2. Ligand preparation with stereochemistry preservation and protonation at pH 7.4

Four ligands (EDS00760714-1/2, EDS00760778-1/2) were extracted from V3000 SDF format, converted to V2000 format with 3D coordinate generation, and processed with RDKit to preserve stereochemistry. Ligand properties (MW, logP, HBA, HBD, rotatable bonds, stereocenters) were calculated.

**Rationale.** Proper protonation state at pH 7.4 and 3D geometry are essential for accurate docking. Stereochemistry preservation is critical for enantiomer differentiation.

| Field | Value |
| :--- | :--- |
| Inputs | P965_EDELRIS_2 Hits w enantiomers.sdf |
| Libraries | rdkit |
| Status | running |

Parameters:

```yaml
format_input: V3000
format_output: V2000
isomericSmiles: True
removeHs: True
```

#### 3. Molecular docking with AutoDock Vina

Four ligands were docked against the PTPN2 allosteric binding site using AutoDock Vina with a search box centered at the FRJ co-crystal position (28.48, 12.33, 4.22 Å) with dimensions 22×28×24 Å. Five binding poses per ligand were generated with exhaustiveness 16.

**Rationale.** AutoDock Vina scoring provides binding affinity estimates and multiple poses to identify the best binding orientation. Multiple poses assess pose stability and variability.

| Field | Value |
| :--- | :--- |
| Inputs | 9C56_receptor.pdb, ligands/EDS00760714-1.sdf, ligands/EDS00760714-2.sdf, ligands/EDS00760778-1.sdf |
| Status | running |

Parameters:

```yaml
boxX: 28.48
boxY: 12.33
boxZ: 4.22
depth: 24
exhaustiveness: 16
height: 28
num_modes: 5
width: 22
```

#### 4. Enantiomer ranking by docking affinity

Docking affinities for enantiomer pairs were compared to identify the active enantiomer for each compound series. Compound 32 (R) showed the strongest binding (ΔG = -7.0 kcal/mol), followed by Compound 32 (S) (ΔG = -6.7 kcal/mol), establishing R-enantiomer preference in the 32 series.

**Rationale.** Enantiomers typically bind with different affinities; more favorable scoring indicates the stereoisomer preferred by the target binding site.

| Field | Value |
| :--- | :--- |
| Status | running |

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| 006_os_path_join.py | PY | 2.2 KB | source | 68e6ff97652f... |
| phase_01_pocket_analysis_from_frj_co_crystal_python_chara.md | MD | 5.3 KB | reports | 7be9fc84e30e... |
| ligands_v2000.sdf | SDF | 23.2 KB | structures | 1591af43d9e7... |
| 008_os_path_join.py | PY | 550 B | source | fafdbbf0ff4d... |
| 007_parse_all_4_ligands_sdf_extract_3d_coords_stereo.py | PY | 1.6 KB | source | 1a92a2177a68... |
| ligand_meta.json | JSON | 1.7 KB | work | e48295b9fce6... |
| EDS00760714-1.sdf | SDF | 5.2 KB | structures | 099a155210aa... |
| EDS00760714-2.sdf | SDF | 5.1 KB | structures | ff2c7e978eb0... |
| EDS00760778-1.sdf | SDF | 5.6 KB | structures | d47b0d4125f5... |
| EDS00760778-2.sdf | SDF | 5.5 KB | structures | d4f4378f4214... |
| 009_chem_sdmolsupplier.py | PY | 2.1 KB | source | 8c2c0abc3623... |
| 010_full_ligand_preparation_one_cell_write_files_no_mol.py | PY | 2.9 KB | source | ae13599401c2... |
| prep_ligands.py | PY | 4.5 KB | source | 075c725193df... |
| 011_os_path_join.py | PY | 342 B | source | dea9bccffefa... |
| ligand_meta.json | JSON | 2.4 KB | work | b4782df2c8b0... |
| EDS00760714-1.sdf | SDF | 4.8 KB | structures | d0ecb7233772... |
| EDS00760714-2.sdf | SDF | 4.8 KB | structures | 9b239d983d08... |
| EDS00760778-1.sdf | SDF | 5.2 KB | structures | b6faf51dd7eb... |
| EDS00760778-2.sdf | SDF | 5.2 KB | structures | 4589d5330e7a... |
| 012_print.py | PY | 301 B | source | ab58c2bdd5bc... |
| phase_02_prepare_4_ligands_at_ph_7_4_and_generate_conform.md | MD | 6.6 KB | reports | cb245b9e8974... |
| autodock-vina-results.json | JSON | 428 B | work | a1ba6ea11366... |
| 013_run_aidd_tool.py | PY | 826 B | source | 68af6f1e3ead... |
| 014_check_saved_results_file.py | PY | 240 B | source | 15ab99e87936... |
| 015_check_result_output_rmsd_data.py | PY | 76 B | source | 4175fab84b1b... |
| 016_list_workspace_files_related_autodock.py | PY | 341 B | source | dd0d6ad68416... |
| 017_os_walk.py | PY | 387 B | source | 5ed61bec369b... |
| autodock-vina-results-2.json | JSON | 428 B | work | 0294be2eeb68... |
| 018_run_aidd_tool.py | PY | 984 B | source | a8d38102c3cc... |
| 019_glob_glob.py | PY | 737 B | source | f0eeef18c2db... |
| draw_2d.py | PY | 1.5 KB | inputs | cbaae32a3b99... |
| 020_run_aidd_tool.py | PY | 690 B | source | c390be53e727... |
| EDS00760714-1_2d.png | PNG | 14.2 KB | figures | 491c36086988... |
| EDS00760714-2_2d.png | PNG | 14.3 KB | figures | 1dd4068dd88e... |
| EDS00760778-1_2d.png | PNG | 14.8 KB | figures | 7ff060740eb1... |
| EDS00760778-2_2d.png | PNG | 14.9 KB | figures | 7cde20e259f4... |
| ligands_grid_2d.png | PNG | 73.7 KB | figures | 4671bc69bd98... |
| autodock-vina-results-3.json | JSON | 428 B | work | 07a777fa6b62... |
| 021_open.py | PY | 199 B | source | c9393ff4b563... |
| 022_run_aidd_tool.py | PY | 1.0 KB | source | 5cf5092f4e8c... |
| analyze_poses.py | PY | 5.9 KB | source | 2b3d86574e84... |
| autodock-vina-results-4.json | JSON | 428 B | work | 4b73708daf91... |
| 023_check_full_output_staged_files.py | PY | 380 B | source | 40044c76ab68... |
| 024_print.py | PY | 40 B | source | f55808fe9608... |
| make_figures.py | PY | 7.3 KB | source | 596e5ee7e7d4... |
| 025_result_get.py | PY | 56 B | source | b3b0878cf20b... |
| enantiomer_comparison.png | PNG | 30.3 KB | figures | 9b4f4c36b163... |
| pocket_residues.png | PNG | 47.0 KB | figures | 260a25af92f3... |
| poses_scatter.png | PNG | 46.7 KB | figures | 396262a617e6... |
| score_comparison.png | PNG | 44.5 KB | figures | 9803d722a062... |
| 026_result_special_dict_s_iterate_items_carefully.py | PY | 507 B | source | 287d56a87b7a... |
| 027_print.py | PY | 469 B | source | 073003cc545e... |
| 028_poses_pdbqt_path_inside_container_check_json_results.py | PY | 676 B | source | 9517bc075499... |
| 029_search_pdbqt_files_around_workdir.py | PY | 331 B | source | 5a1cf2d0f6a4... |
| 030_check_what_close_other_session_tools.py | PY | 243 B | source | ad6c3ac31ce7... |
| generate_report.py | PY | 14.0 KB | source | 56fbffe2de2b... |
| 031_list_all_available_globals_might_help_retrieve.py | PY | 336 B | source | ea6122a43315... |
| 032_print.py | PY | 104 B | source | 9b74dd5306e9... |
| 033_print.py | PY | 60 B | source | 836bee83d4ba... |
| 034_inspect_getsource.py | PY | 78 B | source | 30432e703d18... |
| 035_print.py | PY | 23 B | source | ea2f5a7a2898... |
| 036_print.py | PY | 23 B | source | 71729b4184e4... |
| 037_print.py | PY | 24 B | source | 8caa1424d336... |
| 038_inspect_getsource.py | PY | 110 B | source | fe542e0e58a1... |
| 039_find_where_output_files_handled_dispatch_source.py | PY | 126 B | source | 9bbd0155a831... |
| 040_search_pdbqt_file_extraction_patterns_dispatch.py | PY | 327 B | source | ace1ee5d55e9... |
| 041_look_section_around_files_written_understand_where.py | PY | 96 B | source | a3547486531c... |
| docking_report.md | MD | 407.2 KB | reports | 3d52c20ff358... |
| 042_find_returned_files_population.py | PY | 105 B | source | 399cc85a00fb... |
| generate_report.py | PY | 14.0 KB | source | ff11c8e36cf9... |
| docking_report.md | MD | 407.2 KB | reports | 8af2fcb33c84... |
| 043_check_full_output_dict_docking_run.py | PY | 198 B | source | f8d2f7e33892... |
| 044_read_saved_results_json.py | PY | 227 B | source | 1963c2744f05... |
| 045_find_main_dispatch_function.py | PY | 94 B | source | ee75390c0e5c... |
| 046_find_ssh_docker_run_part_dispatch.py | PY | 152 B | source | 6905ffbb7e25... |

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

1. Landrum G, et al. RDKit: Open-source cheminformatics. doi:10.5281/zenodo.591637
   *The Zenodo DOI resolves to the latest release. Cite the DOI of the exact version used where possible.*
