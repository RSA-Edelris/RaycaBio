---
title: "Phase 5: Interaction analysis and report"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-29bbc6604f"
phase_index: 5
phase_id: "5"
phase_goal: "Interaction analysis and report"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 5: Interaction analysis and report

## Summary

This phase set out to interaction analysis and report. It completed 3 method steps, 275 output files.

## Objective

Interaction analysis and report

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
| fpocket | software | not recorded | doi:10.1186/1471-2105-10-168 (unverified, check before use) | not recorded |
| Rayca Modulon | platform | not recorded | this platform | not recorded |
| numpy | software | 1.26.4 | doi:10.1038/s41586-020-2649-2 | https://numpy.org |
| OpenMM | software | 8.5.2 | doi:10.1371/journal.pcbi.1005659 | https://openmm.org |
| RCSB Protein Data Bank | database | not recorded | doi:10.1093/nar/28.1.235 | https://www.rcsb.org |
| pdbfixer | software | not recorded | no citation on record | https://github.com/openmm/pdbfixer |
| RDKit | software | 2023.9.6 | doi:10.5281/zenodo.591637 | https://www.rdkit.org |

### Procedure

#### 1. Receptor preparation and binding site definition

PDB structure 4CI2 was downloaded and chain B (CRBN) was isolated. Missing residues in internal loops were identified and modeled using PDBFixer. Hydrogens were added at pH 7.4 to establish correct protonation states for ionizable residues. The LVY ligand centroid was computed from atomic coordinates and used to define a docking box (24 Å × 24 Å × 24 Å). Site waters within 5 Å of the LVY centroid

**Rationale.** Accurate receptor preparation is critical for reliable docking. pH 7.4 protonation ensures physiologically relevant ionization states. Water retention at the binding site and cofactor inclusion preserve key interactions. Fpocket validation confirms the docking site is the most ligandable pocket on the protein.

| Field | Value |
| :--- | :--- |
| Inputs | 4CI2_raw.pdb, 4CI2_receptor_for_docking.pdb |
| Outputs | 4CI2_CRBN_full.pdb, 4CI2_receptor_for_docking.pdb, 4CI2_receptor_noh.pdb, 4CI2_LVY_ref.pdb |
| Tools | fpocket |
| Libraries | openmm, pdbfixer, numpy |
| Databases | RCSB PDB |
| Status | running |

Parameters:

```yaml
box_dimensions: 24 × 24 × 24 Å
pH: 7.4
water_selection_radius: 5 Å
```

#### 2. Ligand preparation and standardization

The CRBN_ID_enantio.sdf file containing 32 ligands was standardized by removing salts (keeping the largest fragment), normalizing functional groups, and selecting canonical tautomers using RDKit's tautomer enumerator. Explicit hydrogens were added during reading (removeHs=True parameter maintained valence). Molecular descriptors (molecular weight, H-bond donors/acceptors, rotatable bonds, cLogP) w

**Rationale.** Ligand standardization ensures consistent chemical representation across the series and removes counterions and artifact structures. Canonical tautomers represent the most stable form relevant to binding. Descriptor calculation provides physicochemical context for structure–activity interpretation.

| Field | Value |
| :--- | :--- |
| Inputs | CRBN_ID_enantio.sdf |
| Outputs | CRBN_ligands_prepared.sdf, CRBN_ligands_v2000.sdf |
| Libraries | rdkit |
| Status | running |

Parameters:

```yaml
sdf_format: V2000
tautomer_selection: canonical
```

#### 3. Molecular docking with gnina

All 32 ligands were docked against the prepared CRBN receptor using gnina with GPU acceleration. Docking parameters: LVY-centered box (X=84.800, Y=154.937, Z=13.242, 24×24×24 Å), numModes=5 (5 poses per ligand), CNN scoring with rescore mode. Seed=0 for reproducibility. Each docking run produced affinity scores (kcal/mol) and CNN-based scoring metrics.

**Rationale.** gnina combines traditional molecular docking with deep learning CNN scoring for improved pose ranking. GPU acceleration enables high-throughput screening. Multiple poses (5) per ligand capture conformational diversity and alternative binding modes.

| Field | Value |
| :--- | :--- |
| Inputs | 4CI2_receptor_for_docking.pdb |
| Libraries | modulon |
| Status | running |

Parameters:

```yaml
boxX: 84.800
boxY: 154.937
boxZ: 13.242
cnnScoring: rescore
depth: 24
height: 24
numModes: 5
seed: 0
width: 24
```

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
| phase_02_prepare_ligands_from_crbn_id_enantio_sdf.md | MD | 12.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/reports | cb93dba927f9... |
| lig1.sdf | SDF | 2.5 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 2736bde1164d... |
| lig10.sdf | SDF | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 9eeb9bd0cf6d... |
| lig11.sdf | SDF | 3.2 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 828d462c982b... |
| lig12.sdf | SDF | 3.2 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | fc923095cc64... |
| lig13.sdf | SDF | 3.2 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 8bed5a93ca10... |
| lig14.sdf | SDF | 3.2 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 020b19984474... |
| lig15.sdf | SDF | 3.2 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 5fd98b8ee7e7... |
| lig16.sdf | SDF | 3.2 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | c635d11ed217... |
| lig17.sdf | SDF | 3.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | e0c92bde452b... |
| lig18.sdf | SDF | 3.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 6f641024bab4... |
| lig19.sdf | SDF | 3.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 6c834e9c7e4b... |
| lig2.sdf | SDF | 2.5 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | f7a19d9ed171... |
| lig20.sdf | SDF | 3.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 16ecd99214f5... |
| lig21.sdf | SDF | 3.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | d643f048186c... |
| lig22.sdf | SDF | 3.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | e216909c7cb2... |
| lig23.sdf | SDF | 3.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 60717cdfd1dc... |
| lig24.sdf | SDF | 3.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 80a5dbaa26e8... |
| lig25.sdf | SDF | 3.5 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 58644ffbc409... |
| lig26.sdf | SDF | 3.5 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | af872720bd8a... |
| lig27.sdf | SDF | 3.5 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 39aa86acb8f8... |
| lig28.sdf | SDF | 3.5 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | a94fd717784f... |
| lig29.sdf | SDF | 3.5 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | f69f93e80491... |
| lig3.sdf | SDF | 2.7 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 3d52204ac4e2... |
| lig30.sdf | SDF | 3.5 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | f9ff062372b0... |
| lig31.sdf | SDF | 3.7 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 8442288a2ded... |
| lig32.sdf | SDF | 3.7 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 5201ce3261be... |
| lig4.sdf | SDF | 2.7 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 9c22eb29854a... |
| lig5.sdf | SDF | 2.7 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 75ad17a9705f... |
| lig6.sdf | SDF | 2.7 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 7eb44d2acd0b... |
| lig7.sdf | SDF | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | f07e15be50f6... |
| lig8.sdf | SDF | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | f5aded04c6c5... |
| lig9.sdf | SDF | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | ec565b03eeeb... |
| gnina_docked.sdf.gz | GZ | 2.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | d7193f49ded4... |
| 018_run_aidd_tool.py | PY | 621 B | 03_dock_all_32_ligands_with_gnina_gpu/source | a1fe0d3fec9e... |
| gnina_docked.sdf.gz | GZ | 2.7 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | dbcb4d4edeba... |
| 019_run_aidd_tool.py | PY | 601 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 1d04fe8d3a78... |
| gnina_docked.sdf.gz | GZ | 2.8 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 60f058d62788... |
| 020_run_aidd_tool.py | PY | 601 B | 03_dock_all_32_ligands_with_gnina_gpu/source | db6168f45863... |
| gnina_docked.sdf.gz | GZ | 2.8 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 8173aa0cd077... |
| 021_run_aidd_tool.py | PY | 600 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 914056c6b3bd... |
| gnina_docked.sdf.gz | GZ | 2.8 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 24fb6a5a5252... |
| 022_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | cf0f3e02f5c1... |
| gnina_docked.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 22b481f67c50... |
| 023_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | d9421efd1ba7... |
| gnina_docked.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 74d373396028... |
| 024_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 65dcd2cbdc69... |
| gnina_docked.sdf.gz | GZ | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | b9a6ec152c0b... |
| 025_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 58aaca27bd8f... |
| gnina_docked.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 0b7fdadb68b4... |
| 026_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | b9e1c5aecad7... |
| gnina_docked.sdf.gz | GZ | 2.8 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 69a488ad26ee... |
| 027_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 64400c24c1d9... |
| gnina_docked.sdf.gz | GZ | 2.8 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 411f07ef3c16... |
| 028_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 47b359d97eee... |
| gnina_docked.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 593d3bc5dcb5... |
| 029_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | b3d609ec2d06... |
| gnina_docked.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 6f537d31a1d4... |
| 030_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 090c1a29ea41... |
| gnina_docked.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | d0447ea3f27e... |
| 031_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 9bb31808ffea... |
| gnina_docked.sdf.gz | GZ | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 9b0d5d2736d7... |
| 032_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 74235a7e73b3... |
| gnina_docked.sdf.gz | GZ | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | d4d02a506413... |
| 033_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 7199d726bbbd... |
| gnina_docked.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 7aeac088924a... |
| 034_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | b732b2cfdfe5... |
| gnina_docked.sdf.gz | GZ | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | e5a18eaa37f0... |
| 035_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 3560aa1347f0... |
| gnina_docked.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 5b0d858edf97... |
| 036_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 7370eafc56fd... |
| gnina_docked.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | cde4eb125299... |
| 037_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | ec4b712d327a... |
| gnina_docked.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 6bc8368c09e7... |
| 038_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 2d069bdcf358... |
| gnina_docked.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | aa6cc228ebbe... |
| 039_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | cb47ed38e91e... |
| gnina_docked.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 6cb4482ef081... |
| 040_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 003c345437e3... |
| gnina_docked.sdf.gz | GZ | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 8ddaf24d7726... |
| 041_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 21654d94be2f... |
| gnina_docked.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | e653b2db2724... |
| 042_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 19cdfa270af4... |
| gnina_docked.sdf.gz | GZ | 3.2 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 836dcc643ca3... |
| 043_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | d85ac8f64325... |
| gnina_docked.sdf.gz | GZ | 3.3 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 3cff43861ee4... |
| 044_run_aidd_tool.py | PY | 602 B | 03_dock_all_32_ligands_with_gnina_gpu/source | c4bf336377ec... |
| gnina_docked.sdf.gz | GZ | 2.6 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | bb46d2dfd8d6... |
| 045_run_aidd_tool.py | PY | 473 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 3e030e9e9c1e... |
| 046_run_aidd_tool.py | PY | 635 B | 03_dock_all_32_ligands_with_gnina_gpu/source | e6d007ef35ad... |
| gnina_docked.sdf.gz | GZ | 2.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | bc1a63afe127... |
| input.json | JSON | 259 B | 03_dock_all_32_ligands_with_gnina_gpu/work | 50e93843cc62... |
| gnina_docked.sdf.gz | GZ | 0 B | 03_dock_all_32_ligands_with_gnina_gpu/structures | e3b0c44298fc... |
| 047_quick_test_no_rdkit_just_verify_run_python_healthy.py | PY | 145 B | 03_dock_all_32_ligands_with_gnina_gpu/source | b7ad4b5ed47b... |
| gnina_docked.sdf.gz | GZ | 2.6 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | cc08f9d20964... |
| gnina_docked.sdf.gz | GZ | 2.6 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 087da4f4e3d6... |
| output.json | JSON | 1.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/work | 93390250d93f... |
| 048_print.py | PY | 1.2 KB | 03_dock_all_32_ligands_with_gnina_gpu/source | 4e29417d20d5... |
| 049_check_what_keys_result_actually_has.py | PY | 319 B | 03_dock_all_32_ligands_with_gnina_gpu/source | 291e10e9b8d5... |
| docking_scores_all32.json | JSON | 4.7 KB | 03_dock_all_32_ligands_with_gnina_gpu/work | 955de4c871aa... |
| 050_open.py | PY | 2.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/source | 99f183673589... |
| EDEL-CRBN-0001_ent_poses.sdf.gz | GZ | 2.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | bc1a63afe127... |
| EDEL-CRBN-0001_poses.sdf.gz | GZ | 2.4 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | d7193f49ded4... |
| EDEL-CRBN-0002_ent_poses.sdf.gz | GZ | 2.6 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | bb46d2dfd8d6... |
| EDEL-CRBN-0002_poses.sdf.gz | GZ | 2.6 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 53cec9476b37... |
| EDEL-CRBN-0003_ent_poses.sdf.gz | GZ | 2.6 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | cc08f9d20964... |
| EDEL-CRBN-0003_poses.sdf.gz | GZ | 2.6 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | d0682e784e60... |
| EDEL-CRBN-0004_ent_poses.sdf.gz | GZ | 2.8 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 60f058d62788... |
| EDEL-CRBN-0004_poses.sdf.gz | GZ | 2.7 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | dbcb4d4edeba... |
| 051_os_makedirs.py | PY | 1.5 KB | 03_dock_all_32_ligands_with_gnina_gpu/source | ab0e546f47b0... |
| EDEL-CRBN-0005_ent_poses.sdf.gz | GZ | 2.8 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 24fb6a5a5252... |
| EDEL-CRBN-0005_poses.sdf.gz | GZ | 2.8 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 8173aa0cd077... |
| EDEL-CRBN-0006_ent_poses.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 74d373396028... |
| EDEL-CRBN-0006_poses.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 22b481f67c50... |
| EDEL-CRBN-0007_ent_poses.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 0b7fdadb68b4... |
| EDEL-CRBN-0007_poses.sdf.gz | GZ | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | b9a6ec152c0b... |
| EDEL-CRBN-0008_ent_poses.sdf.gz | GZ | 2.8 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 411f07ef3c16... |
| EDEL-CRBN-0008_poses.sdf.gz | GZ | 2.8 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 69a488ad26ee... |
| 052_dict.py | PY | 1.2 KB | 03_dock_all_32_ligands_with_gnina_gpu/source | d5ac8b93a508... |
| EDEL-CRBN-0009_ent_poses.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 6f537d31a1d4... |
| EDEL-CRBN-0009_poses.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 593d3bc5dcb5... |
| EDEL-CRBN-0010_ent_poses.sdf.gz | GZ | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 9b0d5d2736d7... |
| EDEL-CRBN-0010_poses.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | d0447ea3f27e... |
| EDEL-CRBN-0011_ent_poses.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 7aeac088924a... |
| EDEL-CRBN-0011_poses.sdf.gz | GZ | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | d4d02a506413... |
| EDEL-CRBN-0012_ent_poses.sdf.gz | GZ | 2.9 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 5b0d858edf97... |
| EDEL-CRBN-0012_poses.sdf.gz | GZ | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | e5a18eaa37f0... |
| 053_dict.py | PY | 1.2 KB | 03_dock_all_32_ligands_with_gnina_gpu/source | e24244267868... |
| EDEL-CRBN-0013_ent_poses.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 6bc8368c09e7... |
| EDEL-CRBN-0013_poses.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | cde4eb125299... |
| EDEL-CRBN-0014_ent_poses.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 6cb4482ef081... |
| EDEL-CRBN-0014_poses.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | aa6cc228ebbe... |
| EDEL-CRBN-0015_ent_poses.sdf.gz | GZ | 3.1 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | e653b2db2724... |
| EDEL-CRBN-0015_poses.sdf.gz | GZ | 3.0 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 8ddaf24d7726... |
| EDEL-CRBN-0016_ent_poses.sdf.gz | GZ | 3.3 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 3cff43861ee4... |
| EDEL-CRBN-0016_poses.sdf.gz | GZ | 3.2 KB | 03_dock_all_32_ligands_with_gnina_gpu/structures | 836dcc643ca3... |
| 054_dict.py | PY | 1.3 KB | 03_dock_all_32_ligands_with_gnina_gpu/source | 2be47effec3a... |
| phase_03_dock_all_32_ligands_with_gnina_gpu.md | MD | 31.1 KB | 04_mm_gbsa_on_best_docking_poses/reports | 44153fa671e4... |
| 055_check_available_python_packages_structure_analysis.py | PY | 550 B | 04_mm_gbsa_on_best_docking_poses/source | 03bf539fd147... |
| EDEL-CRBN-0001_ent_pose1.sdf | SDF | 2.9 KB | 04_mm_gbsa_on_best_docking_poses/structures | 427fc268f0c3... |
| EDEL-CRBN-0001_pose1.sdf | SDF | 2.9 KB | 04_mm_gbsa_on_best_docking_poses/structures | 6be029734b7c... |
| EDEL-CRBN-0002_ent_pose1.sdf | SDF | 3.1 KB | 04_mm_gbsa_on_best_docking_poses/structures | 4cb511813877... |
| EDEL-CRBN-0002_pose1.sdf | SDF | 3.1 KB | 04_mm_gbsa_on_best_docking_poses/structures | a509b1b6e0fb... |
| EDEL-CRBN-0003_ent_pose1.sdf | SDF | 3.1 KB | 04_mm_gbsa_on_best_docking_poses/structures | c24760a490fa... |
| EDEL-CRBN-0003_pose1.sdf | SDF | 3.1 KB | 04_mm_gbsa_on_best_docking_poses/structures | a20c48154302... |
| EDEL-CRBN-0004_ent_pose1.sdf | SDF | 3.3 KB | 04_mm_gbsa_on_best_docking_poses/structures | d2d00dcd0049... |
| EDEL-CRBN-0004_pose1.sdf | SDF | 3.3 KB | 04_mm_gbsa_on_best_docking_poses/structures | 093b79d31c88... |
| EDEL-CRBN-0005_ent_pose1.sdf | SDF | 3.3 KB | 04_mm_gbsa_on_best_docking_poses/structures | 2cf927295140... |
| EDEL-CRBN-0005_pose1.sdf | SDF | 3.3 KB | 04_mm_gbsa_on_best_docking_poses/structures | 0a9424b11f58... |
| EDEL-CRBN-0006_ent_pose1.sdf | SDF | 3.5 KB | 04_mm_gbsa_on_best_docking_poses/structures | 9057d9b04b09... |
| EDEL-CRBN-0006_pose1.sdf | SDF | 3.5 KB | 04_mm_gbsa_on_best_docking_poses/structures | 73e5cac918e9... |
| EDEL-CRBN-0007_ent_pose1.sdf | SDF | 3.5 KB | 04_mm_gbsa_on_best_docking_poses/structures | a266b1cfed01... |
| EDEL-CRBN-0007_pose1.sdf | SDF | 3.5 KB | 04_mm_gbsa_on_best_docking_poses/structures | a8912a3739fb... |
| EDEL-CRBN-0008_ent_pose1.sdf | SDF | 3.4 KB | 04_mm_gbsa_on_best_docking_poses/structures | 38568b5860cb... |
| EDEL-CRBN-0008_pose1.sdf | SDF | 3.4 KB | 04_mm_gbsa_on_best_docking_poses/structures | 941997ab74f1... |
| EDEL-CRBN-0009_ent_pose1.sdf | SDF | 3.6 KB | 04_mm_gbsa_on_best_docking_poses/structures | e156b7acbdb3... |
| EDEL-CRBN-0009_pose1.sdf | SDF | 3.6 KB | 04_mm_gbsa_on_best_docking_poses/structures | 908b21c7c7de... |
| EDEL-CRBN-0010_ent_pose1.sdf | SDF | 3.7 KB | 04_mm_gbsa_on_best_docking_poses/structures | 4e72cc01f9a3... |
| EDEL-CRBN-0010_pose1.sdf | SDF | 3.7 KB | 04_mm_gbsa_on_best_docking_poses/structures | da2cc7eb59a6... |
| EDEL-CRBN-0011_ent_pose1.sdf | SDF | 3.6 KB | 04_mm_gbsa_on_best_docking_poses/structures | 932197a90b11... |
| EDEL-CRBN-0011_pose1.sdf | SDF | 3.6 KB | 04_mm_gbsa_on_best_docking_poses/structures | 75b83d33e5ec... |
| EDEL-CRBN-0012_ent_pose1.sdf | SDF | 3.6 KB | 04_mm_gbsa_on_best_docking_poses/structures | 231b453bf874... |
| EDEL-CRBN-0012_pose1.sdf | SDF | 3.6 KB | 04_mm_gbsa_on_best_docking_poses/structures | aad59df2d291... |
| EDEL-CRBN-0013_ent_pose1.sdf | SDF | 3.8 KB | 04_mm_gbsa_on_best_docking_poses/structures | 2d953b60f51c... |
| EDEL-CRBN-0013_pose1.sdf | SDF | 3.8 KB | 04_mm_gbsa_on_best_docking_poses/structures | de0871c34a8e... |
| EDEL-CRBN-0014_ent_pose1.sdf | SDF | 3.8 KB | 04_mm_gbsa_on_best_docking_poses/structures | 01c374ad59c1... |
| EDEL-CRBN-0014_pose1.sdf | SDF | 3.8 KB | 04_mm_gbsa_on_best_docking_poses/structures | 25429adb3e30... |
| EDEL-CRBN-0015_ent_pose1.sdf | SDF | 3.8 KB | 04_mm_gbsa_on_best_docking_poses/structures | e5f203eb1daa... |
| EDEL-CRBN-0015_pose1.sdf | SDF | 3.8 KB | 04_mm_gbsa_on_best_docking_poses/structures | 6dc7b107e23a... |
| EDEL-CRBN-0016_ent_pose1.sdf | SDF | 4.0 KB | 04_mm_gbsa_on_best_docking_poses/structures | a86955b2d7a4... |
| EDEL-CRBN-0016_pose1.sdf | SDF | 4.0 KB | 04_mm_gbsa_on_best_docking_poses/structures | f87287e24592... |
| 056_extract_best_pose_molecule_1_each_sdf_gz_using.py | PY | 1.0 KB | 04_mm_gbsa_on_best_docking_poses/source | 51cd7067ba4d... |
| 057_parse_receptor_pdb_protein_only_no_ligand_h.py | PY | 2.9 KB | 04_mm_gbsa_on_best_docking_poses/source | 63c54434b9be... |
| interaction_utils.py | PY | 4.3 KB | 04_mm_gbsa_on_best_docking_poses/source | 0b57a6b12feb... |
| all_contacts.json | JSON | 75.4 KB | 04_mm_gbsa_on_best_docking_poses/work | 4ea8f62f6457... |
| 058_sys_path_insert.py | PY | 1.1 KB | 04_mm_gbsa_on_best_docking_poses/source | c53051182e43... |
| interaction_freq.json | JSON | 1.0 KB | 04_mm_gbsa_on_best_docking_poses/work | 578e333d4471... |
| 059_sys_path_insert.py | PY | 1.4 KB | 04_mm_gbsa_on_best_docking_poses/source | a96a5d11da8c... |
| phase_04_mm_gbsa_on_best_docking_poses.md | MD | 35.5 KB | 05_interaction_analysis_and_report/reports | 4bfb511d74fc... |

## Verification

- 3 tool call(s) ran in this phase, 0 of which reported a failure.
- 275 file(s) were produced and registered, 275 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/fpocket:latest`
- Container Image: `registry.rayca.org/rayca-tools/gnina:latest`

## Limitations

- No citation is on record for fpocket, so the versions used cannot be traced to a publication.
- Versions were not recorded for RCSB Protein Data Bank, Rayca Modulon, fpocket, pdbfixer. A methods section without a version is not reproducible.

## References

1. Eastman P, et al. OpenMM 7: Rapid development of high performance algorithms for molecular dynamics. PLoS Comput Biol. 2017;13:e1005659. doi:10.1371/journal.pcbi.1005659
   *For OpenMM 8 cite doi:10.1021/acs.jpcb.3c06662 in addition.*
2. Berman HM, et al. The Protein Data Bank. Nucleic Acids Res. 2000;28:235-242. doi:10.1093/nar/28.1.235
   *Cite the individual entry identifiers used, for example 6OIM, alongside this reference.*
3. pdbfixer version 1.12.0.
4. Landrum G, et al. RDKit: Open-source cheminformatics. doi:10.5281/zenodo.591637
   *The Zenodo DOI resolves to the latest release. Cite the DOI of the exact version used where possible.*

**Unverified candidate references.** These were matched automatically by name and have NOT been confirmed as the correct reference for the tool this study used. Two tools in different fields can share a name, so each must be checked before use.

- fpocket: Vincent Le Guilloux, Peter Schmidtke, Pierre Tufféry. Fpocket: An open source platform for ligand pocket detection. BMC Bioinformatics. 2009. doi:10.1186/1471-2105-10-168
