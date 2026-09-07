---
title: "Phase 2: Prepare ligands from CRBN_ID_enantio.sdf"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-29bbc6604f"
phase_index: 2
phase_id: "2"
phase_goal: "Prepare ligands from CRBN_ID_enantio.sdf"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 2: Prepare ligands from CRBN_ID_enantio.sdf

## Summary

This phase set out to prepare ligands from CRBN_ID_enantio.sdf. It completed 96 output files.

## Objective

Prepare ligands from CRBN_ID_enantio.sdf

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
| 4CI2_raw.pdb | PDB | 1.8 MB | 01_fetch_pdb_4ci2_and_prepare_receptor/inputs | c2902e096995... |
| 002_receptor_preparation_fetch_4ci2_identify_lvy_chain.py | PY | 1.6 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/source | 0c93e65237a4... |
| 4CI2_chainA_full.pdb | PDB | 1.4 MB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 6407896e28ee... |
| 003_find_lvy_chain_centroid_pdbfixer_prep.py | PY | 3.1 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/source | d1afeaf4f4d1... |
| 4CI2_CRBN_full.pdb | PDB | 493.5 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 4e8e9f5940c2... |
| 004_correct_prep_keep_chain_b_crbn_lvy_remove_chain_ddb1.py | PY | 2.1 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/source | b56ac73500d3... |
| 4CI2_LVY_ref.pdb | PDB | 2.5 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 7fdf8eac4b97... |
| 4CI2_receptor_for_docking.pdb | PDB | 489.8 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 5eb47b24d869... |
| 005_build_docking_receptor_select_site_waters.py | PY | 3.2 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/source | 304bca7ceb74... |
| 4CI2_receptor_noh.pdb | PDB | 245.7 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 1e4982d74de3... |
| 006_fpocket_confirm_lvy_site_top_ranked_pocket_strip_h.py | PY | 1.9 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/source | 3096a691e9a9... |
| 4CI2_receptor_noh.pml | PML | 782 B | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 5f0a9e4d07e9... |
| 4CI2_receptor_noh.tcl | TCL | 932 B | 01_fetch_pdb_4ci2_and_prepare_receptor/work | a8e52a95d6ea... |
| 4CI2_receptor_noh_PYMOL.sh | SH | 40 B | 01_fetch_pdb_4ci2_and_prepare_receptor/source | 347d50b9bd9a... |
| 4CI2_receptor_noh_VMD.sh | SH | 67 B | 01_fetch_pdb_4ci2_and_prepare_receptor/source | bd3769e20cee... |
| 4CI2_receptor_noh_info.txt | TXT | 17.5 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/reports | 3aaa887e37cc... |
| 4CI2_receptor_noh_out.pdb | PDB | 325.3 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 61f98af92a34... |
| 4CI2_receptor_noh_pockets.pqr | PQR | 71.0 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 809f5f622cdd... |
| pocket10_atm.pdb | PDB | 3.8 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 5f93dc3c3811... |
| pocket10_vert.pqr | PQR | 4.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | f9078388df93... |
| pocket11_atm.pdb | PDB | 2.5 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 2740d9f417d8... |
| pocket11_vert.pqr | PQR | 2.7 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 53539f38bca0... |
| pocket12_atm.pdb | PDB | 3.2 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 5028a3dae820... |
| pocket12_vert.pqr | PQR | 3.0 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | fc77881ded5f... |
| pocket13_atm.pdb | PDB | 2.3 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | b1569a0969a8... |
| pocket13_vert.pqr | PQR | 2.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 9fbbc07bfbb1... |
| pocket14_atm.pdb | PDB | 2.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 9a2af14a758e... |
| pocket14_vert.pqr | PQR | 2.6 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | f851435e9cac... |
| pocket15_atm.pdb | PDB | 2.3 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 30bba1ab29c2... |
| pocket15_vert.pqr | PQR | 2.7 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | df8c290bf0bb... |
| pocket16_atm.pdb | PDB | 4.1 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 4b313c5f039a... |
| pocket16_vert.pqr | PQR | 5.1 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | dfd467c84298... |
| pocket17_atm.pdb | PDB | 2.3 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 5c3dc25d3d92... |
| pocket17_vert.pqr | PQR | 2.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 5f58b57243a2... |
| pocket18_atm.pdb | PDB | 2.1 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 448be80ff240... |
| pocket18_vert.pqr | PQR | 2.3 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | f1fe90c36322... |
| pocket19_atm.pdb | PDB | 2.6 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 2b719ce8e2c4... |
| pocket19_vert.pqr | PQR | 3.1 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 239ef66bc350... |
| pocket1_atm.pdb | PDB | 6.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 2db1f32f091f... |
| pocket1_vert.pqr | PQR | 8.7 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 4d5c0224e77f... |
| pocket20_atm.pdb | PDB | 2.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 9920de35220c... |
| pocket20_vert.pqr | PQR | 2.3 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 9b23fbddbebc... |
| pocket21_atm.pdb | PDB | 3.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 028bcb313176... |
| pocket21_vert.pqr | PQR | 3.9 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 0c329a77f156... |
| pocket22_atm.pdb | PDB | 2.3 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 0615e62de9f0... |
| pocket22_vert.pqr | PQR | 2.7 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 81da8adc9d14... |
| pocket23_atm.pdb | PDB | 2.7 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | e96fce181246... |
| pocket23_vert.pqr | PQR | 2.9 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 9abb5f7ddb24... |
| pocket24_atm.pdb | PDB | 2.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | e585f84cef1b... |
| pocket24_vert.pqr | PQR | 2.2 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 4a2d80824a97... |
| pocket25_atm.pdb | PDB | 2.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 6b4d9613f75e... |
| pocket25_vert.pqr | PQR | 2.5 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 72988dd76423... |
| pocket26_atm.pdb | PDB | 2.5 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 399071d4d8e9... |
| pocket26_vert.pqr | PQR | 2.7 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | db4381453e01... |
| pocket27_atm.pdb | PDB | 2.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 64b63df2e65e... |
| pocket27_vert.pqr | PQR | 2.5 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 9a913a6d6931... |
| pocket28_atm.pdb | PDB | 3.3 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 539dec4ed789... |
| pocket28_vert.pqr | PQR | 3.7 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 0c8e67f2c706... |
| pocket29_atm.pdb | PDB | 2.6 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 39a58916026e... |
| pocket29_vert.pqr | PQR | 2.9 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 04323c0791a3... |
| pocket2_atm.pdb | PDB | 3.6 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 5c6c370ef930... |
| pocket2_vert.pqr | PQR | 3.8 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 049028f3980e... |
| pocket30_atm.pdb | PDB | 2.5 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | d5feadbf2ae1... |
| pocket30_vert.pqr | PQR | 2.6 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | a46dbaa0c485... |
| pocket31_atm.pdb | PDB | 2.8 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | d56a5739f91c... |
| pocket31_vert.pqr | PQR | 2.6 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | aa1479684977... |
| pocket32_atm.pdb | PDB | 4.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | ba9d3b57c9df... |
| pocket32_vert.pqr | PQR | 5.8 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 75c6d65a970a... |
| pocket3_atm.pdb | PDB | 3.3 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | ff1d0706baba... |
| pocket3_vert.pqr | PQR | 5.3 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | ca99a999d7cc... |
| pocket4_atm.pdb | PDB | 3.0 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | cb8570739ac3... |
| pocket4_vert.pqr | PQR | 3.6 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | a4cc32b306e3... |
| pocket5_atm.pdb | PDB | 2.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | da3013152bb8... |
| pocket5_vert.pqr | PQR | 2.7 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | e4ebf6ffa4db... |
| pocket6_atm.pdb | PDB | 2.6 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | cc7bb50f5a51... |
| pocket6_vert.pqr | PQR | 3.1 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | f40b574b162b... |
| pocket7_atm.pdb | PDB | 3.0 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 9de62fd37e6a... |
| pocket7_vert.pqr | PQR | 3.4 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | c28fb643f972... |
| pocket8_atm.pdb | PDB | 2.2 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 94feebbe04aa... |
| pocket8_vert.pqr | PQR | 2.2 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | ea94a645eb99... |
| pocket9_atm.pdb | PDB | 4.0 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/structures | 8ce772835a1e... |
| pocket9_vert.pqr | PQR | 4.6 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/work | 710013f3f135... |
| 007_1_fpocket_correct_key.py | PY | 1.1 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/source | 530aae0c0123... |
| 008_inspect_fpocket_output_structure.py | PY | 617 B | 01_fetch_pdb_4ci2_and_prepare_receptor/source | 3867f91331e9... |
| 009_parse_fpocket_info_txt.py | PY | 2.5 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/source | 4afd5faff98d... |
| 010_where_did_fpocket_write_files.py | PY | 372 B | 01_fetch_pdb_4ci2_and_prepare_receptor/source | 79b76c49846e... |
| 011_parse_pocket_data_fp_output.py | PY | 2.8 KB | 01_fetch_pdb_4ci2_and_prepare_receptor/source | 605cc5dddfbd... |
| phase_01_fetch_pdb_4ci2_and_prepare_receptor.md | MD | 10.9 KB | 02_prepare_ligands_from_crbn_id_enantio_sdf/reports | 1c26fe9fb9d5... |
| CRBN_ligands_prepared.sdf | SDF | 77.3 KB | 02_prepare_ligands_from_crbn_id_enantio_sdf/structures | c9b357d3cb59... |
| 012_ligand_preparation.py | PY | 3.1 KB | 02_prepare_ligands_from_crbn_id_enantio_sdf/source | 109350a12b8e... |
| 013_ligand_preparation_error_handling.py | PY | 2.8 KB | 02_prepare_ligands_from_crbn_id_enantio_sdf/source | 500ee6175ede... |
| 014_rdmolstandardize_normalizer.py | PY | 2.3 KB | 02_prepare_ligands_from_crbn_id_enantio_sdf/source | d8fc81053188... |
| 015_largest_fragment.py | PY | 1.8 KB | 02_prepare_ligands_from_crbn_id_enantio_sdf/source | 0577e18f41bf... |
| 016_minimal_isolation_test.py | PY | 716 B | 02_prepare_ligands_from_crbn_id_enantio_sdf/source | e8f820886a8f... |
| 017_open.py | PY | 1.4 KB | 02_prepare_ligands_from_crbn_id_enantio_sdf/source | 1ca34889fb98... |
| CRBN_ligands_v2000.sdf | SDF | 102.1 KB | 02_prepare_ligands_from_crbn_id_enantio_sdf/structures | 3ca9e4563523... |

## Verification

- No tool call is on record for this phase.
- 96 file(s) were produced and registered, 96 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/fpocket:latest`

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
