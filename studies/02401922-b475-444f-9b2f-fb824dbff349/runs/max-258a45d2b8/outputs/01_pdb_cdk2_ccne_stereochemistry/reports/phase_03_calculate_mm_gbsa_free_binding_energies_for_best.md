---
title: "Phase 3: Calculate MM/GBSA free binding energies for best poses"
study_id: "02401922-b475-444f-9b2f-fb824dbff349"
run_id: "max-e87c3d4aff"
phase_index: 3
phase_id: "3"
phase_goal: "Calculate MM/GBSA free binding energies for best poses"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 3: Calculate MM/GBSA free binding energies for best poses

## Summary

This phase set out to calculate MM/GBSA free binding energies for best poses. It completed 11 method steps, 139 output files.

## Objective

Calculate MM/GBSA free binding energies for best poses

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
| meeko | software | not recorded | doi:10.1021/acs.jcim.5c02271 (unverified, check before use) | https://github.com/forlilab/meeko |
| RCSB Protein Data Bank | database | not recorded | doi:10.1093/nar/28.1.235 | https://www.rcsb.org |
| RDKit | software | 2023.9.6 | doi:10.5281/zenodo.591637 | https://www.rdkit.org |

### Procedure

#### 1. Binding site definition from CTX crystal coordinates

The docking box was defined using the CTX ligand coordinates from the PDB structure. The CTX centroid was calculated as (31.99, 4.68, -26.16) Å. A cubic box of 25 × 25 × 25 Å was positioned at this center, encompassing the CTX ligand binding site. This site-specific definition restricts docking to the experimentally validated binding pocket rather than the full protein interface.

**Rationale.** Using crystal ligand coordinates to define the search space ensures that docking focuses on the relevant binding site, improves computational efficiency, and enables direct comparison with the known CTX binding mode.

| Field | Value |
| :--- | :--- |
| Inputs | CDK2-CCNE.pdb |
| Databases | RCSB PDB |
| Status | running |

Parameters:

```yaml
box_center_x_angstrom: 31.99
box_center_y_angstrom: 4.68
box_center_z_angstrom: -26.16
```

#### 2. Receptor preparation and protonation

CDK2-CCNE receptor was prepared by extracting protein chains A and B, retaining 9 structural water molecules within 4 Å of the CTX ligand binding site (residues HOH 58, 187, 115, 5, 227, 207, 122, 11, 229). The structure was protonated at pH 7.4 using PDBFixer, which added missing atoms and assigned protonation states to ionizable residues. The CTX ligand was removed from the receptor for use as a

**Rationale.** Proper protonation at physiological pH is essential for accurate binding predictions. Retaining crystallographic waters in the binding site preserves structurally important hydration and accounts for water-mediated interactions.

| Field | Value |
| :--- | :--- |
| Inputs | CDK2-CCNE.pdb |
| Outputs | receptor_prepared.pdb |
| Databases | RCSB PDB |
| Status | running |

Parameters:

```yaml
pH: 7.4
waters_retained: 9
```

#### 3. Ligand standardization and protonation

Ligands from the input SDF file were standardized by removing salts and counter-ions (largest fragment selection), normalizing functional groups, and identifying the canonical tautomer. Stereochemistry was assessed; unspecified stereocenters were enumerated. The ligand was then converted to 3D coordinates using ETKDG conformer generation, followed by MMFF optimization. Protonation was performed at

**Rationale.** Standardization resolves chemical inconsistencies across compound sets. Canonical tautomerization and stereoisomer enumeration ensure chemically valid conformations. pH-dependent protonation reflects binding conditions in aqueous buffer.

| Field | Value |
| :--- | :--- |
| Inputs | Ligand.sdf |
| Outputs | ligand_prepared.sdf |
| Libraries | rdkit |
| Status | running |

Parameters:

```yaml
conformer_generation: ETKDG
pH: 7.4
```

#### 4. Receptor parameterization for docking

The prepared receptor PDB was converted to PDBQT format using Open Babel with Gasteiger partial charge assignment and removal of non-polar hydrogens, generating the docking-compatible receptor file.

**Rationale.** PDBQT format and Gasteiger charges are required for Vina docking calculations. Charge assignment enables electrostatic interactions in the scoring function.

| Field | Value |
| :--- | :--- |
| Inputs | receptor_prepared.pdb |
| Outputs | receptor.pdbqt |
| Status | running |

Parameters:

```yaml
charge_model: gasteiger
remove_nonpolar_h: True
```

#### 5. Ligand parameterization for docking

Prepared ligand was converted to PDBQT format using Meeko, which assigned rotatable bonds, Gasteiger partial charges, and handled protonation state consistent with pH 7.4. The ligand formal charge was determined (+1) from the protonated SMILES and used in parameterization.

**Rationale.** Meeko PDBQT generation is compatible with Vina and explicitly models rotatable bonds and partial charges necessary for accurate binding pose prediction.

| Field | Value |
| :--- | :--- |
| Inputs | ligand_prepared.sdf |
| Outputs | ligand.pdbqt |
| Libraries | meeko |
| Status | running |

#### 6. Reference ligand parameterization

The CTX reference ligand was extracted from the crystal structure and converted to PDBQT format using Meeko with the same parameters as the test ligand (pH 7.4, Gasteiger charges) to enable direct comparison of binding scores.

**Rationale.** Parameterizing CTX identically to the test ligands ensures that any differences in docking scores reflect ligand differences rather than parameterization artifacts.

| Field | Value |
| :--- | :--- |
| Inputs | ctx_ref.sdf |
| Outputs | ctx_ref.pdbqt |
| Libraries | meeko |
| Status | running |

#### 7. Molecular docking with AutoDock Vina

The prepared ligand was docked into the CDK2-CCNE binding site using AutoDock Vina with the CTX-derived box definition (center 31.99, 4.68, -26.16 Å; size 25×25×25 Å). Docking was performed with 5 binding modes requested, exhaustiveness 16, energy range 5 kcal/mol, CPU parallelization across 4 threads, and random seed 42. The reference CTX ligand was scored in its crystal pose using the same box.

**Rationale.** Vina docking generates multiple binding poses ranked by predicted binding affinity. The CTX crystal-pose score serves as a benchmark to validate that the protocol correctly recognizes the known binder.

| Field | Value |
| :--- | :--- |
| Inputs | receptor.pdbqt, ligand.pdbqt, ctx_ref.pdbqt |
| Outputs | docked_poses.pdbqt |
| Status | running |

Parameters:

```yaml
cpu: 4
energy_range_kcal_mol: 5
exhaustiveness: 16
num_modes: 5
seed: 42
```

#### 8. Docking pose extraction and annotation

All 5 docked poses were extracted from the Vina output PDBQT file and converted to SDF format using Meeko's RDKitMolCreate module. Each pose was annotated with its rank number and Vina affinity score. The best pose (rank 1) was also exported as PDB format for subsequent structural analysis.

**Rationale.** SDF format preserves 3D coordinates and enables visualization and analysis with standard cheminformatics tools. Annotation with scores allows tracking of pose quality.

| Field | Value |
| :--- | :--- |
| Outputs | docked_poses_all5.sdf, best_pose.pdb |
| Status | running |

#### 9. Interaction analysis between docked ligand and receptor

Contact analysis between the best docked pose and the prepared receptor was performed by geometric criteria: hydrogen bonds identified as N-O or O-N contacts at distance < 3.5 Å; hydrophobic contacts identified as C-C distances < 4.5 Å. Protein-ligand proximity was mapped by parsing atomic coordinates and residue identifiers from the PDB structures.

**Rationale.** Geometric contact analysis provides a simple, interpretable description of the binding mode complementary to docking scores and is comparable across different ligands and to the CTX reference interaction pattern.

| Field | Value |
| :--- | :--- |
| Inputs | best_pose.pdb, receptor_prepared.pdb |
| Status | running |

Parameters:

```yaml
hbond_distance_cutoff_angstrom: 3.5
hydrophobic_distance_cutoff_angstrom: 4.5
```

#### 10. Reference CTX crystal interaction analysis

Hydrogen bonding interactions in the CTX crystal structure were identified using the same geometric criteria applied to the docked poses (N/O contacts < 3.5 Å). This reference interaction profile was used to compare against the docked ligand binding modes.

**Rationale.** Quantifying the CTX crystal interactions establishes a baseline for evaluating whether docked ligands recapitulate known favorable interactions with the binding site.

| Field | Value |
| :--- | :--- |
| Inputs | ctx_ref.pdb, receptor_prepared.pdb |
| Status | running |

Parameters:

```yaml
hbond_distance_cutoff_angstrom: 3.5
```

#### 11. Ligand antechamber parameterization for MM-GBSA

The best docked pose ligand was parameterized using antechamber with AM1-BCC charge model, GAFF2 force field, and net charge +1. Missing GAFF2 parameters were determined using parmchk2. The ligand residue was named 'LIG' for subsequent Amber system building.

**Rationale.** AM1-BCC charges and GAFF2 are standard for small-molecule MM-GBSA calculations, providing consistent parameterization with Amber tools.

| Field | Value |
| :--- | :--- |
| Inputs | best_pose_lig.pdb |
| Outputs | ligand.mol2, ligand.frcmod, ligand_docked.mol2 |
| Status | running |

Parameters:

```yaml
charge_model: AM1-BCC
force_field: gaff2
net_charge: 1
```

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| 001_aidd_tool_schema.py | PY | 106 B | 01_pdb_cdk2_ccne_stereochemistry/source | 634a51806c91... |
| 002_check_available_tools_receptor_ligand_prep.py | PY | 443 B | 01_pdb_cdk2_ccne_stereochemistry/source | d0e2db5139a5... |
| receptor_raw.pdb | PDB | 364.1 KB | 01_pdb_cdk2_ccne_stereochemistry/inputs | 78add4a6bf12... |
| 003_receptor_preparation_keep_chains_b_9_structural.py | PY | 1.4 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 1598f4ef49d0... |
| receptor_prepared.pdb | PDB | 733.0 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | b167ba582764... |
| 004_run_pdbfixer_fix_missing_atoms_add_h_ph_7_4.py | PY | 1.0 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 43dd28e4a945... |
| 005_ligand_preparation_1_load_sdf_2d_v3000_standardize.py | PY | 831 B | 01_pdb_cdk2_ccne_stereochemistry/source | 3e8ef59305d4... |
| 006_standardize_remove_fragments_salts_normalize.py | PY | 1.4 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 8916a4c8d6c5... |
| ligand_3d_raw.sdf | SDF | 6.0 KB | 01_pdb_cdk2_ccne_stereochemistry/inputs | c649d31336e7... |
| ligand_prepared.sdf | SDF | 6.8 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | d8cd79864a03... |
| 007_generate_3d_coords_etkdg_protonate_ph_7_4_via_obabel.py | PY | 976 B | 01_pdb_cdk2_ccne_stereochemistry/source | 8b031eb93a85... |
| ctx_ref.pdb | PDB | 5.7 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 201f9b8dcc6c... |
| ctx_ref.sdf | SDF | 6.8 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 079c666a4360... |
| 008_extract_ctx_pdb_sdf_reference_docking.py | PY | 957 B | 01_pdb_cdk2_ccne_stereochemistry/inputs | a5a357d429d2... |
| phase_01_prepare_cdk2_ccne_receptor_and_standardize_ligan.md | MD | 3.2 KB | 01_pdb_cdk2_ccne_stereochemistry/reports | cad9d4bb32f4... |
| 009_dispatch_both_gnina_jobs_parallel_1_dock_prepared.py | PY | 1.0 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 1dc57c9b3d35... |
| 010_dispatch.py | PY | 705 B | 01_pdb_cdk2_ccne_stereochemistry/source | ffe9e9959f39... |
| 011_clean_up_stale_gnina_container.py | PY | 836 B | 01_pdb_cdk2_ccne_stereochemistry/source | 14466cb1f3a3... |
| 012_remove_full_container_id.py | PY | 523 B | 01_pdb_cdk2_ccne_stereochemistry/source | 78503590e479... |
| 013_time_sleep.py | PY | 599 B | 01_pdb_cdk2_ccne_stereochemistry/source | 8a76e38dba3c... |
| 014_check_what_built_functions_available_namespace.py | PY | 666 B | 01_pdb_cdk2_ccne_stereochemistry/source | d26511fce7a5... |
| 015_try_once_more_after_longer_wait_container_might_have.py | PY | 785 B | 01_pdb_cdk2_ccne_stereochemistry/source | bf9418fabaab... |
| 016_check_local_gnina_binary_cpu_fallback.py | PY | 902 B | 01_pdb_cdk2_ccne_stereochemistry/source | 0eb0a531d4f1... |
| receptor.pdbqt | PDBQT | 439.7 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 70376b623721... |
| 017_check_vina_version.py | PY | 651 B | 01_pdb_cdk2_ccne_stereochemistry/source | ee5533caf3c9... |
| ctx_ref.pdbqt | PDBQT | 3.8 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 59cb84492d51... |
| ligand.pdbqt | PDBQT | 3.8 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | c3fd48824a8d... |
| 018_prepare_ligand_pdbqt_meeko_handles_rotatable_bonds.py | PY | 1.1 KB | 01_pdb_cdk2_ccne_stereochemistry/source | df27d2d26629... |
| docked_poses.pdbqt | PDBQT | 20.1 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 9c2c8dd33d01... |
| 019_run_vina_dock_ligand_5_modes.py | PY | 671 B | 01_pdb_cdk2_ccne_stereochemistry/source | 6893c0be8b0c... |
| 020_score_ctx_crystal_pose_score_only.py | PY | 949 B | 01_pdb_cdk2_ccne_stereochemistry/source | f0d9d74afa86... |
| phase_02_dock_ligands_with_gnina_get_5_poses_per_ligand.md | MD | 5.1 KB | 01_pdb_cdk2_ccne_stereochemistry/reports | 612edebd5bd3... |
| docked_poses_all5.sdf | SDF | 0 B | 01_pdb_cdk2_ccne_stereochemistry/structures | e3b0c44298fc... |
| 021_convert_docked_pdbqt_sdf_meeko_run_plip_style_h_bond.py | PY | 996 B | 01_pdb_cdk2_ccne_stereochemistry/source | a12b60ee38b9... |
| 022_check_rdkitmolcreate_api.py | PY | 433 B | 01_pdb_cdk2_ccne_stereochemistry/source | 47790aed0519... |
| best_pose.pdb | PDB | 11.0 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 5347845314d6... |
| docked_poses_all5.sdf | SDF | 30.9 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 1d7f5f2b5b31... |
| 023_chem_sdwriter.py | PY | 886 B | 01_pdb_cdk2_ccne_stereochemistry/source | b9f9fe9b43e5... |
| 024_analyze_interactions_best_docked_pose_vs_receptor_h.py | PY | 2.6 KB | 01_pdb_cdk2_ccne_stereochemistry/source | b2684e885545... |
| 025_ctx_crystal_interactions_redefine_helper.py | PY | 1.7 KB | 01_pdb_cdk2_ccne_stereochemistry/source | bbe47104baf1... |
| ANTECHAMBER_AC.AC | AC | 8.2 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 6505a7874f82... |
| ANTECHAMBER_AC.AC0 | AC0 | 8.2 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 8ed75875bfdf... |
| ANTECHAMBER_AM1BCC.AC | AC | 8.2 KB | 01_pdb_cdk2_ccne_stereochemistry/work | fc7fbb102053... |
| ANTECHAMBER_AM1BCC_PRE.AC | AC | 8.2 KB | 01_pdb_cdk2_ccne_stereochemistry/work | a86b575ce7ab... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 8.2 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 8ed75875bfdf... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 8.2 KB | 01_pdb_cdk2_ccne_stereochemistry/work | d0330694e1de... |
| ATOMTYPE.INF | INF | 17.2 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 8a9ec48b75dd... |
| ligand.mol2 | MOL2 | 7.8 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 30da28714d06... |
| 026_step_1_determine_ligand_net_charge_protonated_smiles.py | PY | 1.1 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 79eefdfae249... |
| sqm.in | IN | 4.0 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 57022107f0dd... |
| sqm.out | OUT | 18.9 KB | 01_pdb_cdk2_ccne_stereochemistry/work | abe7b055edfd... |
| sqm.pdb | PDB | 5.6 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 565063c755df... |
| leap.log | LOG | 16.9 KB | 01_pdb_cdk2_ccne_stereochemistry/work | b81738498a05... |
| ligand.frcmod | FRCMOD | 6.1 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 0b676ecd266a... |
| 027_parmchk2_missing_gaff2_parameters.py | PY | 1.2 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 9c6e8ec7a284... |
| tleap.in | IN | 535 B | 01_pdb_cdk2_ccne_stereochemistry/work | 31a08d50f061... |
| 028_fix_create_docked_pose_mol2_correct_gaff2_atom_types.py | PY | 2.1 KB | 01_pdb_cdk2_ccne_stereochemistry/source | aca65185b67f... |
| ANTECHAMBER_AC.AC | AC | 8.6 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 6bd01f8144df... |
| ANTECHAMBER_AC.AC0 | AC0 | 8.6 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 4d34e1973d97... |
| ANTECHAMBER_AM1BCC.AC | AC | 8.6 KB | 01_pdb_cdk2_ccne_stereochemistry/work | c1904b6fa44e... |
| ANTECHAMBER_AM1BCC_PRE.AC | AC | 8.6 KB | 01_pdb_cdk2_ccne_stereochemistry/work | c5b52f4e77ca... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 8.6 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 4d34e1973d97... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 8.6 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 2a3360849293... |
| ATOMTYPE.INF | INF | 14.6 KB | 01_pdb_cdk2_ccne_stereochemistry/work | aacf470391e1... |
| best_pose_lig.pdb | PDB | 11.0 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 2eb39e23a9d3... |
| ligand_docked.mol2 | MOL2 | 8.1 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | d82798ca3b17... |
| 029_fix_unl_lig_best_pose_pdb_run_antechamber_directly.py | PY | 881 B | 01_pdb_cdk2_ccne_stereochemistry/source | 4b3f7ad1a591... |
| sqm.in | IN | 4.0 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 4677d897081a... |
| sqm.out | OUT | 20.1 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 81e2448c1eb6... |
| sqm.pdb | PDB | 5.6 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | b95c6e7cb4d5... |
| complex.pdb | PDB | 738.6 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 908ad8fba87d... |
| leap.log | LOG | 33.0 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 9a52e312e0c1... |
| ligand_docked.frcmod | FRCMOD | 3.7 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 384b6c53b5a4... |
| 030_parmchk2_docked_mol2_tleap_complex.py | PY | 1.6 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 17f8e320b134... |
| tleap2.in | IN | 419 B | 01_pdb_cdk2_ccne_stereochemistry/work | 7961fc935c4b... |
| 031_show_leap_log_errors.py | PY | 238 B | 01_pdb_cdk2_ccne_stereochemistry/source | 1a868deb8d8c... |
| 032_find_all_unique_residue_names_complex_pdb.py | PY | 567 B | 01_pdb_cdk2_ccne_stereochemistry/source | a27ad06a0aed... |
| 033_print_full_tleap2_output_diagnose.py | PY | 68 B | 01_pdb_cdk2_ccne_stereochemistry/source | 82144329766b... |
| complex.prmtop | PRMTOP | 0 B | 01_pdb_cdk2_ccne_stereochemistry/work | e3b0c44298fc... |
| leap.log | LOG | 44.8 KB | 01_pdb_cdk2_ccne_stereochemistry/work | a0fa37ba35f3... |
| receptor_nowater.pdb | PDB | 730.8 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 4d1bc904f8e4... |
| 034_load_ligand_mol2_directly_skip_loadpdb_ligand_use.py | PY | 1.4 KB | 01_pdb_cdk2_ccne_stereochemistry/source | ca9bf4ca7ca2... |
| tleap3.in | IN | 350 B | 01_pdb_cdk2_ccne_stereochemistry/work | 499da02ff66f... |
| leap.log | LOG | 54.7 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 7ec1e6cffa2b... |
| receptor_amber.pdb | PDB | 363.3 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 83347e19d101... |
| receptor_amber_nonprot.pdb | PDB | 0 B | 01_pdb_cdk2_ccne_stereochemistry/structures | e3b0c44298fc... |
| receptor_amber_renum.txt | TXT | 13.8 KB | 01_pdb_cdk2_ccne_stereochemistry/reports | 2e2694e2affd... |
| receptor_amber_sslink | not recorded | 0 B | 01_pdb_cdk2_ccne_stereochemistry/work | e3b0c44298fc... |
| 035_pdb4amber_cleans_receptor_amber_renames_atoms.py | PY | 1.2 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 2cc1026ae529... |
| tleap4.in | IN | 348 B | 01_pdb_cdk2_ccne_stereochemistry/work | 4251f7308a0e... |
| 036_show_full_leap4_log_around_error.py | PY | 308 B | 01_pdb_cdk2_ccne_stereochemistry/source | b54b40929526... |
| leap.log | LOG | 64.0 KB | 01_pdb_cdk2_ccne_stereochemistry/work | ad3a18f65a6f... |
| receptor_noh.pdb | PDB | 363.3 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | 83347e19d101... |
| 037_strip_all_h_receptor_amber_pdb_including_polar_h.py | PY | 1.4 KB | 01_pdb_cdk2_ccne_stereochemistry/source | c910bc4169d5... |
| tleap5.in | IN | 363 B | 01_pdb_cdk2_ccne_stereochemistry/work | 27e93a918bbb... |
| leap.log | LOG | 73.8 KB | 01_pdb_cdk2_ccne_stereochemistry/work | a65c49bbdbdb... |
| receptor_noh2.pdb | PDB | 363.2 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | d76cd176d7e1... |
| 038_fix_1_drop_addhydrogens_not_valid_cmd_tleap_adds_h.py | PY | 1.9 KB | 01_pdb_cdk2_ccne_stereochemistry/source | da2b6cd6bdba... |
| tleap6.in | IN | 341 B | 01_pdb_cdk2_ccne_stereochemistry/work | 7e2f79bb7010... |
| ligand_corrected.mol2 | MOL2 | 7.1 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | f6b30b3fe8a3... |
| 040_strategy_read_ligand_mol2_correct_gaff2_sdf_temp.csv | CSV | 126 B | 01_pdb_cdk2_ccne_stereochemistry/tables | cacf9dcbdb1a... |
| 039_strategy_read_ligand_mol2_correct_gaff2_sdf_template.py | PY | 2.7 KB | 01_pdb_cdk2_ccne_stereochemistry/source | f23d578c39a7... |
| complex.inpcrd | INPCRD | 331.8 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 3ae1a640b93b... |
| complex.prmtop | PRMTOP | 3.9 MB | 01_pdb_cdk2_ccne_stereochemistry/work | 77ba0d1f5db9... |
| leap.log | LOG | 102.8 KB | 01_pdb_cdk2_ccne_stereochemistry/work | d3c68da46932... |
| ligand_amber.inpcrd | INPCRD | 2.6 KB | 01_pdb_cdk2_ccne_stereochemistry/work | c421ed0b9641... |
| ligand_amber.prmtop | PRMTOP | 44.9 KB | 01_pdb_cdk2_ccne_stereochemistry/work | e93028b29153... |
| ligand_corrected.frcmod | FRCMOD | 6.1 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 0b676ecd266a... |
| receptor.inpcrd | INPCRD | 329.2 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 6907b375623e... |
| receptor.prmtop | PRMTOP | 3.8 MB | 01_pdb_cdk2_ccne_stereochemistry/work | 42de669b7b98... |
| 040_generate_frcmod_corrected_mol2_run_tleap.py | PY | 1.2 KB | 01_pdb_cdk2_ccne_stereochemistry/source | a671e820d3f2... |
| tleap7.in | IN | 347 B | 01_pdb_cdk2_ccne_stereochemistry/work | 72591c84e313... |
| mmpbsa.in | IN | 108 B | 01_pdb_cdk2_ccne_stereochemistry/work | eef92bcf8877... |
| 041_write_mmpbsa_py_input_single_frame_igb_5_gb_obc2.py | PY | 695 B | 01_pdb_cdk2_ccne_stereochemistry/inputs | 3065b41a0244... |
| FINAL_RESULTS_MMGBSA.dat | DAT | 3.9 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 0ee1b8e3993d... |
| reference.frc | FRC | 1.9 MB | 01_pdb_cdk2_ccne_stereochemistry/inputs | 1a1dbb5daae1... |
| 042_find_amberhome_tleap_location.py | PY | 830 B | 01_pdb_cdk2_ccne_stereochemistry/source | afc38bb64963... |
| 043_open.py | PY | 65 B | 01_pdb_cdk2_ccne_stereochemistry/source | 9b9bf7900275... |
| 044_verify_atom_order_mismatch_compare_element_sequences.py | PY | 1.1 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 01ce40b81160... |
| 045_use_rdkit_substructure_match_map_docked_pose_atom.py | PY | 3.0 KB | 01_pdb_cdk2_ccne_stereochemistry/source | ef0f4149072a... |
| complex.inpcrd | INPCRD | 331.8 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 03f8e3f184bc... |
| complex.prmtop | PRMTOP | 3.9 MB | 01_pdb_cdk2_ccne_stereochemistry/work | 47f1d2808b62... |
| leap.log | LOG | 115.0 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 6e698e3daad3... |
| ligand_amber.inpcrd | INPCRD | 2.6 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 368b7d333627... |
| ligand_amber.prmtop | PRMTOP | 44.9 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 80091d2875ca... |
| ligand_mapped.frcmod | FRCMOD | 6.1 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 0b676ecd266a... |
| ligand_mapped.mol2 | MOL2 | 7.2 KB | 01_pdb_cdk2_ccne_stereochemistry/structures | d5458ffbed7b... |
| receptor.prmtop | PRMTOP | 3.8 MB | 01_pdb_cdk2_ccne_stereochemistry/work | b3244aa23c17... |
| 046_write_correctly_mapped_mol2_template_topology.py | PY | 1.9 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 2316ecfe1b5b... |
| tleap8.in | IN | 341 B | 01_pdb_cdk2_ccne_stereochemistry/work | ac0885d2731d... |
| complex_min.rst7 | RST7 | 218.6 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 17a3943794fb... |
| mdinfo | not recorded | 409 B | 01_pdb_cdk2_ccne_stereochemistry/work | acdef3b31d46... |
| min.in | IN | 310 B | 01_pdb_cdk2_ccne_stereochemistry/work | 0f915727d306... |
| min.out | OUT | 7.3 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 5d21feefa49a... |
| 047_short_energy_minimization_500_sd_1000_cg_no_periodic.py | PY | 1.4 KB | 01_pdb_cdk2_ccne_stereochemistry/source | 4755ee671466... |
| FINAL_RESULTS_MMGBSA.dat | DAT | 3.9 KB | 01_pdb_cdk2_ccne_stereochemistry/work | 796a42805d2d... |
| reference.frc | FRC | 3.8 MB | 01_pdb_cdk2_ccne_stereochemistry/inputs | ef2b5dce4f91... |
| 048_subprocess_run.py | PY | 884 B | 01_pdb_cdk2_ccne_stereochemistry/source | 4104d86afa9e... |
| 049_open.py | PY | 983 B | 01_pdb_cdk2_ccne_stereochemistry/source | 34855e25fc8f... |

## Limitations

- No citation is on record for meeko, so the versions used cannot be traced to a publication.
- Versions were not recorded for RCSB Protein Data Bank, meeko. A methods section without a version is not reproducible.

## References

1. Berman HM, et al. The Protein Data Bank. Nucleic Acids Res. 2000;28:235-242. doi:10.1093/nar/28.1.235
   *Cite the individual entry identifiers used, for example 6OIM, alongside this reference.*
2. Landrum G, et al. RDKit: Open-source cheminformatics. doi:10.5281/zenodo.591637
   *The Zenodo DOI resolves to the latest release. Cite the DOI of the exact version used where possible.*

**Unverified candidate references.** These were matched automatically by name and have NOT been confirmed as the correct reference for the tool this study used. Two tools in different fields can share a name, so each must be checked before use.

- meeko: Diogo Santos‐Martins, Yiran He, Jérôme Eberhardt et al.. Meeko: Molecule Parametrization and Software Interoperability for Docking and Beyond. Journal of Chemical Information and Modeling. 2025. doi:10.1021/acs.jcim.5c02271
