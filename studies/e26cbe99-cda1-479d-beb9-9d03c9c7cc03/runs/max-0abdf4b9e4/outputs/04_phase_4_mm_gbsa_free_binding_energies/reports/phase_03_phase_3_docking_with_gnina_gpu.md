---
title: "Phase 3: Phase 3 — Docking with gnina (GPU)"
study_id: "e26cbe99-cda1-479d-beb9-9d03c9c7cc03"
run_id: "max-7e8c57ab26"
phase_index: 3
phase_id: "3"
phase_goal: "Phase 3 — Docking with gnina (GPU)"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 3: Phase 3 — Docking with gnina (GPU)

## Summary

This phase set out to phase 3 — Docking with gnina (GPU). It completed 42 output files.

## Objective

Phase 3 — Docking with gnina (GPU)

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
| PB-20260903-4CI2_raw.pdb | PDB | 1.8 MB | 01_phase_1_protein_preparation_4ci2/inputs | c2902e096995... |
| 005_download_pdb_4ci2_inspect.py | PY | 1.3 KB | 01_phase_1_protein_preparation_4ci2/source | 3586b38d1b53... |
| 006_extract_lvy_lenalidomide_coordinates_pocket_centre.py | PY | 1.3 KB | 01_phase_1_protein_preparation_4ci2/source | 40b5dc0aeb55... |
| 007_confirm_all_missing_residues_his_tag_linker_there.py | PY | 1013 B | 01_phase_1_protein_preparation_4ci2/source | 83c8afb2fdea... |
| 008_re_parse_remark_465_directly_raw_pdb_lines.py | PY | 1.4 KB | 01_phase_1_protein_preparation_4ci2/inputs | a2ee0a77648f... |
| 009_full_missing_residue_list_chain_b.py | PY | 390 B | 01_phase_1_protein_preparation_4ci2/source | 355707be62e1... |
| 010_phase_1_launch_pdbfixer.py | PY | 1.1 KB | 01_phase_1_protein_preparation_4ci2/source | 6fa03be03dc2... |
| PB-20260903-4CI2_receptor.pdb | PDB | 1.9 MB | 01_phase_1_protein_preparation_4ci2/structures | 3631479233d0... |
| 011_phase_1_pdbfixer_process.py | PY | 2.0 KB | 01_phase_1_protein_preparation_4ci2/source | af54284430f9... |
| PB-20260903-4CI2_receptor_noH.pdb | PDB | 950.4 KB | 01_phase_1_protein_preparation_4ci2/structures | 79dde47e3da6... |
| 012_1_strip_h_receptor_fpocket.py | PY | 1.3 KB | 01_phase_1_protein_preparation_4ci2/source | 90d994b8f7ce... |
| 013_fpocket.py | PY | 1.0 KB | 01_phase_1_protein_preparation_4ci2/source | f90e6433de4e... |
| 014_pocket_characterisation_crystal_structure_pocket.py | PY | 3.0 KB | 01_phase_1_protein_preparation_4ci2/source | 99bbbcc5cc24... |
| protonation-state-results-2.json | JSON | 721 B | 01_phase_1_protein_preparation_4ci2/results | 690f3e56a4cf... |
| protonation-state-results-3.json | JSON | 751 B | 01_phase_1_protein_preparation_4ci2/results | 8daaaef9b18d... |
| protonation-state-results-4.json | JSON | 751 B | 01_phase_1_protein_preparation_4ci2/results | 4e5b545bcb6f... |
| protonation-state-results-5.json | JSON | 667 B | 01_phase_1_protein_preparation_4ci2/results | d7a54b495e8d... |
| protonation-state-results.json | JSON | 715 B | 01_phase_1_protein_preparation_4ci2/results | 4faf406c9adb... |
| 015_protonate_each_ligand_ph_7_4_via_dimorphite_dl.py | PY | 1.1 KB | 01_phase_1_protein_preparation_4ci2/source | 9f08f258fecd... |
| phase_01_phase_1_protein_preparation_4ci2.md | MD | 4.2 KB | 02_phase_2_ligand_preparation/reports | 921c9208f34c... |
| phase_02_phase_2_ligand_preparation.md | MD | 4.2 KB | 03_phase_3_docking_with_gnina_gpu/reports | b5c7fdfc7633... |
| lig_EDS01357518_ent1.sdf | SDF | 4.0 KB | 03_phase_3_docking_with_gnina_gpu/structures | 7c163a87c75f... |
| lig_EDS01357518_ent2.sdf | SDF | 4.0 KB | 03_phase_3_docking_with_gnina_gpu/structures | eb333c89f6c1... |
| lig_EDS01806218_ent1.sdf | SDF | 4.0 KB | 03_phase_3_docking_with_gnina_gpu/structures | 502fb30921be... |
| lig_EDS01806218_ent2.sdf | SDF | 4.0 KB | 03_phase_3_docking_with_gnina_gpu/structures | 8b1caed717ec... |
| lig_EDS01889984.sdf | SDF | 5.1 KB | 03_phase_3_docking_with_gnina_gpu/structures | 55bc31350849... |
| 016_split_enantio_structure_sdf_into_per_ligand_sdf.py | PY | 890 B | 03_phase_3_docking_with_gnina_gpu/source | 3cf652ca28ce... |
| PB-20260903-4CI2_receptor_trimmed.pdb | PDB | 179.1 KB | 03_phase_3_docking_with_gnina_gpu/structures | c22bb3cf89c2... |
| PB-20260903-4CI2_receptor_trimmed_noH.pdb | PDB | 90.4 KB | 03_phase_3_docking_with_gnina_gpu/structures | 44098f0ec487... |
| 017_trim_receptor_residues_within_20_pocket_centre.py | PY | 2.0 KB | 03_phase_3_docking_with_gnina_gpu/source | e64e59141c84... |
| 018_dock_all_5_ligands_gnina_gpu_top_5_poses_each.py | PY | 1.9 KB | 03_phase_3_docking_with_gnina_gpu/source | dfcb2613ed19... |
| 019_check_gnina_vina_binaries_path.py | PY | 1.5 KB | 03_phase_3_docking_with_gnina_gpu/source | d279167aa713... |
| gnina_docked.sdf.gz | GZ | 2.9 KB | 03_phase_3_docking_with_gnina_gpu/structures | 3399ca3ce8b8... |
| 020_check_converters.py | PY | 1.8 KB | 03_phase_3_docking_with_gnina_gpu/source | f593cf5e3bab... |
| 021_inspect_r_gnina_result_dict.py | PY | 1.4 KB | 03_phase_3_docking_with_gnina_gpu/source | 57d0c24a2504... |
| docked_EDS01357518_ent1.sdf.gz | GZ | 2.9 KB | 03_phase_3_docking_with_gnina_gpu/structures | 3399ca3ce8b8... |
| docked_EDS01357518_ent2.sdf.gz | GZ | 2.8 KB | 03_phase_3_docking_with_gnina_gpu/structures | 9995bc3bbb5e... |
| docked_EDS01806218_ent1.sdf.gz | GZ | 2.8 KB | 03_phase_3_docking_with_gnina_gpu/structures | 326c13253b29... |
| docked_EDS01806218_ent2.sdf.gz | GZ | 2.9 KB | 03_phase_3_docking_with_gnina_gpu/structures | 71a9ef9568c6... |
| docked_EDS01889984.sdf.gz | GZ | 2.9 KB | 03_phase_3_docking_with_gnina_gpu/structures | fda0b1994322... |
| gnina_docked.sdf.gz | GZ | 2.9 KB | 03_phase_3_docking_with_gnina_gpu/structures | fda0b1994322... |
| 022_read_gnina_gz.py | PY | 2.3 KB | 03_phase_3_docking_with_gnina_gpu/source | cab97949a6dd... |

## Verification

- No tool call is on record for this phase.
- 42 file(s) were produced and registered, 42 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/pdbfixer:latest`
- Container Image: `registry.rayca.org/rayca-tools/fpocket:latest`
- Container Image: `registry.rayca.org/rayca-tools/protonation-state:latest`
- Container Image: `registry.rayca.org/rayca-tools/gnina:latest`

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
