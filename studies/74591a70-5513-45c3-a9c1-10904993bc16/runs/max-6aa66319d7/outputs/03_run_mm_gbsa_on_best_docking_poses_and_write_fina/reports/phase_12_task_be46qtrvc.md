---
title: "Phase 12: task be46qtrvc"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-6aa66319d7"
phase_index: 12
phase_id: "be46qtrvc"
phase_goal: "task be46qtrvc"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 12: task be46qtrvc

## Summary

This phase set out to task be46qtrvc. It completed 10 method steps, 462 output files.

## Objective

task be46qtrvc

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
| GNINA | software | not recorded | doi:10.1186/s13321-021-00522-2 | https://github.com/gnina/gnina |
| MDAnalysis | software | not recorded | doi:10.25080/Majora-629e541a-00e | not recorded |
| prolif | software | not recorded | doi:10.1186/s13321-021-00548-6 (unverified, check before use) | not recorded |
| RDKit | software | 2023.9.6 | doi:10.5281/zenodo.591637 | https://www.rdkit.org |

### Procedure

#### 1. Ligand structure preparation and stereoisomer enumeration

Input SDF file (CRBN_lig_results_2.sdf) containing 8 racemic compounds with STERAC1 annotations was converted from V3000 to V2000 format using obabel. RDKit EnumerateStereoisomers was applied to enumerate all undefined stereocenters (onlyUnassigned=True, unique=True, maxIters=32), with stereochemistry explicitly cleared prior to enumeration to override legacy STERAC1 markings.

**Rationale.** Enumeration of all enantiomers is necessary to explore the full stereochemical space for binding affinity prediction. Clearing prior stereo annotations ensures the algorithm considers all unassigned centers.

| Field | Value |
| :--- | :--- |
| Inputs | CRBN_lig_results_2.sdf |
| Outputs | CRBN_lig_results_2_v2000.sdf |
| Libraries | rdkit |
| Status | running |

Parameters:

```yaml
stereo_enumeration_onlyUnassigned: True
stereo_enumeration_unique: True
```

#### 2. 3D conformer generation and ligand protonation

For each stereoisomer, a single 3D conformer was generated using RDKit ETKDG v3 (randomSeed=42). Single-point energy was calculated using UFF force field without minimisation to avoid runtime overhead. Ligands were then protonated at pH 7.4 using obabel (-p 7.4) to reflect physiological conditions.

**Rationale.** 3D conformers are required for molecular docking. ETKDG is a fast distance-geometry method suitable for docking preparation. Protonation at pH 7.4 ensures ligand ionization state matches binding conditions.

| Field | Value |
| :--- | :--- |
| Inputs | CRBN_lig_results_2_v2000.sdf |
| Outputs | CRBN_ID_enantio_2.sdf |
| Libraries | rdkit |
| Status | running |

Parameters:

```yaml
etkdg_randomSeed: 42
force_field: UFF
protonation_pH: 7.4
```

#### 3. Ligand file splitting for docking

Multi-compound SDF file (CRBN_ID_enantio_2.sdf) was split into individual SDF files by compound name for compatibility with gnina docking tool.

**Rationale.** gnina accepts single-ligand SDF files; multi-compound SDFs require preprocessing.

| Field | Value |
| :--- | :--- |
| Inputs | CRBN_ID_enantio_2.sdf |
| Status | running |

#### 4. Molecular docking with gnina

All 22 stereoisomers were docked against PDB structure 4CI2 using gnina with CNN-based pose refinement (cnnScoring='rescore'). Docking box was centered on the LVY ligand reference site (85.06, 154.79, 13.38) with dimensions 22.0 Å. Five binding poses per ligand were generated (numModes=5, seed=42). Vina ΔG and CNN pKd scores were collected for each pose.

**Rationale.** Structure-based docking predicts binding modes and affinity. CNN rescoring refines poses using learned protein-ligand interaction patterns. Box constraint to the LVY site (rather than whole interface) focuses exploration on the known binding pocket.

| Field | Value |
| :--- | :--- |
| Inputs | 4CI2_receptor_for_docking.pdb |
| Outputs | docking2_results.json |
| Tools | gnina |
| Status | running |

Parameters:

```yaml
boxX: 85.06
boxY: 154.79
boxZ: 13.38
cnnScoring: rescore
depth: 22.0
height: 22.0
numModes: 5
seed: 42
width: 22.0
```

#### 5. Best pose extraction and ranking

Best docking pose (top-ranked by Vina ΔG) was extracted from each compound's multi-pose SDF file. All poses were ranked by Vina affinity (ΔG in kcal/mol) and compared to experimental EC50 values from the original compound summary.

**Rationale.** Ranking by thermodynamic score identifies most promising binders; comparison to experimental activity validates predictive model.

| Field | Value |
| :--- | :--- |
| Inputs | docking2_results.json, CRBN_enantio2_summary.json |
| Outputs | docking2_ranked.json |
| Status | running |

#### 6. Results ranking and reporting

All 22 compounds were ranked by Vina docking affinity (ΔG in kcal/mol). Ranked table was generated showing compound name, parent compound ID, Vina ΔG, CNN pKd, and experimental EC50 (µM) from the original summary. Best poses were extracted to best_poses2_top1/ for downstream analysis and visualization.

**Rationale.** Integrated ranking table consolidates docking scores and experimental validation data for easy comparison of predicted vs. observed potency.

| Field | Value |
| :--- | :--- |
| Inputs | docking2_results.json, CRBN_enantio2_summary.json |
| Outputs | docking2_ranked.json |
| Status | running |

#### 7. MM-GBSA free energy scoring

Single-frame MM-GBSA endpoint scoring was performed on all 22 best docked poses using AMBER tools (ff14SB + GAFF2). Generalized Born solvation (igb=5, saltcon=0.100) was used for implicit-solvent calculation. MMFF force field was not used; instead AMBER united-atom force field parameters were used for all calculations. Complex (protein+ligand), protein-alone, and ligand-alone AMBER topologies were

**Rationale.** MM-GBSA provides physics-based free energy estimates by combining molecular mechanics (bonded and non-bonded van der Waals) with continuum solvation. igb=5 is a fast generalized Born model; endpoint approximation (single frame, no trajectory) is suitable for rapid screening.

| Field | Value |
| :--- | :--- |
| Outputs | mmgbsa2_results.json |
| Status | running |

Parameters:

```yaml
force_field_ligand: GAFF2
force_field_protein: ff14SB
frame_selection: endpoint
gb_model: igb=5
salt_concentration: 0.100
```

#### 8. Protein-ligand interaction fingerprinting

ProLIF (prolif) interaction fingerprints were computed for all 22 best docked poses. Binding-site protein residues were selected as all atoms within 8 Å (or 12 Å fallback) of the ligand centroid to avoid converting large receptor regions to RDKit molecules. Interaction types detected: HBDonor, HBAcceptor, Hydrophobic, PiStacking, PiCation, CationPi, Anionic, Cationic, MetalAcceptor. Residue × inte

**Rationale.** Interaction fingerprints characterize ligand-binding mode in terms of specific protein-ligand contacts. Residue-level frequency analysis identifies key pharmacophore features and conserved binding interactions.

| Field | Value |
| :--- | :--- |
| Inputs | 4CI2_receptor_for_docking.pdb |
| Outputs | interaction_fingerprints.json |
| Libraries | rdkit, MDAnalysis, prolif |
| Status | running |

Parameters:

```yaml
binding_site_cutoff_Angstrom: 8.0
binding_site_fallback_cutoff_Angstrom: 12.0
```

#### 9. Ligand parameterization for MM-GBSA

Each docked ligand (best pose SDF) was parameterized for AMBER using antechamber with GAFF2 force field and Gasteiger partial charges (faster than AM1BCC for 30-38 heavy atom compounds). MOL2 files and frcmod parameter files were generated. Formal charge was determined via RDKit for each ligand.

**Rationale.** GAFF2 is a general small-molecule force field compatible with ff14SB protein parameters. Gasteiger charges provide rapid parameterization suitable for high-throughput scoring.

| Field | Value |
| :--- | :--- |
| Status | running |

Parameters:

```yaml
atom_type: gaff2
charge_method: gas
force_field: GAFF2
```

#### 10. Receptor structure preparation for MM-GBSA

Receptor PDB (4CI2_receptor_for_docking.pdb) was cleaned for AMBER/GAFF2 topology generation. Histidine residues were renamed based on protonation state (HID for δ-protonated, HIE for ε-protonated) by detecting presence of HD1 and HE2 atoms. Water molecules and crystallographic ions were removed. AMBER ff14SB force field topology and coordinate files were generated using tleap with implicit solven

**Rationale.** AMBER requires explicit HIS naming (HID/HIE/HIP) rather than generic HIS; protonation state affects charge and atom type assignment. Implicit-solvent MM-GBSA does not require water model parameters.

| Field | Value |
| :--- | :--- |
| Outputs | mmgbsa2/receptor_amber.pdb |
| Status | running |

Parameters:

```yaml
force_field: ff14SB
solvent_model: implicit
```

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| 103_path.py | PY | 1.8 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | 8c31c948645c... |
| CRBN_lig_results_2_v2000.sdf | SDF | 26.4 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/structures | bbcef059c72f... |
| 104_check_protonation_tools_rdkit_capabilities.py | PY | 1.4 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | baf9e510de0a... |
| 105_subprocess_run.py | PY | 709 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | dc0b17d13c49... |
| prep_enantio2.py | PY | 7.7 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | b72456373dfc... |
| 106_sdmolsupplier.py | PY | 797 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | a7c364677356... |
| 107_subprocess_run.py | PY | 371 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | 5e7dda9ee62e... |
| CRBN_ID_enantio_2.sdf | SDF | 0 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/structures | e3b0c44298fc... |
| 108_full_preparation_one_cell_avoids_cross_cell_pickle.py | PY | 5.9 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | f400b660314f... |
| 109_re_import_rdkit_fresh_previous_import_restored_mols.py | PY | 4.2 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | c2c411852562... |
| CRBN_ID_enantio_2.sdf | SDF | 43.2 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/structures | 58e1b5bf3d36... |
| CRBN_enantio2_stage1.sdf | SDF | 42.7 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/structures | 90f5ce44653b... |
| CRBN_enantio2_summary.json | JSON | 1.2 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/work | 81d9cf540b61... |
| 110_allchem_chem_sdmolsupplier_path_base_out_sdf_v2000.py | PY | 3.9 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | 25696bc8b2d1... |
| 111_allchem_chem_sdmolsupplier_path_base_out_sdf_v2000.py | PY | 3.0 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | 187db917fb73... |
| 112_path.py | PY | 717 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | 29735e2da901... |
| 113_print.py | PY | 259 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | 20e207e6b630... |
| prep_enantio2.py | PY | 5.9 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | 1b80c1c1fabe... |
| CRBN_ID_enantio_2.sdf | SDF | 47.1 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/structures | 461dd8a4d34b... |
| CRBN_enantio2_summary.json | JSON | 1.4 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/work | fe5b930e46f2... |
| 114_subprocess_run.py | PY | 388 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | bc189e32ab73... |
| prep_enantio2.py | PY | 6.0 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | 7a8a4756c34a... |
| CRBN_enantio2_stage1.sdf | SDF | 20.2 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/structures | e3b0c44298fc... |
| 115_subprocess_run.py | PY | 383 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | 422c83df2633... |
| prep_enantio2.py | PY | 6.0 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | ee313001cca9... |
| prep_enantio2.log | LOG | 0 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/work | cef3960a4691... |
| CRBN_enantio2_stage1.sdf | SDF | 11.1 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/structures | 6dc81fcd4c53... |
| prep_enantio2.log | LOG | 229 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/work | 2d46147614cd... |
| prep_enantio2.log | LOG | 264 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/work | 018b663fb6f3... |
| CRBN_enantio2_stage1.sdf | SDF | 20.2 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/structures | 8060cc8218f3... |
| prep_enantio2.py | PY | 6.0 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | 52dc78144ef7... |
| prep_enantio2.log | LOG | 0 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/work | d6d9edb753e3... |
| CRBN_enantio2_stage1.sdf | SDF | 11.1 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/structures | e4c417417c86... |
| prep_enantio2.py | PY | 6.0 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/source | f8389fa05f07... |
| prep_enantio2.log | LOG | 0 B | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/work | b4d6f50dcd2d... |
| CRBN_ID_enantio_2.sdf | SDF | 124.2 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/structures | 4b40b1728d54... |
| CRBN_enantio2_stage1.sdf | SDF | 112.9 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/structures | 4f1ec08136a8... |
| CRBN_enantio2_summary.json | JSON | 3.8 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/work | 4184972982db... |
| prep_enantio2.log | LOG | 3.9 KB | 01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce/work | 31c347dd7889... |
| phase_01_prepare_crbn_id_enantio_2_sdf_enumerate_stereoce.md | MD | 8.7 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/reports | 2f488e830534... |
| Compound_10_ent1.sdf | SDF | 6.2 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | a239dee3eb8b... |
| Compound_10_ent2.sdf | SDF | 6.2 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | ed67f983089b... |
| Compound_11_ent1.sdf | SDF | 5.8 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | c3e7fa83038d... |
| Compound_11_ent2.sdf | SDF | 5.8 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | b216649502bf... |
| Compound_12_ent1.sdf | SDF | 6.5 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | bae5d76b0b01... |
| Compound_12_ent2.sdf | SDF | 6.5 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 14230e6ee34f... |
| Compound_1_ent1.sdf | SDF | 6.3 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 4ce6f91da36a... |
| Compound_1_ent2.sdf | SDF | 6.3 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 48dbce9eb7e1... |
| Compound_4_s1.sdf | SDF | 5.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 261b81acd9e4... |
| Compound_4_s12.sdf | SDF | 5.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | b043666fef0e... |
| Compound_4_s13.sdf | SDF | 5.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 2be21ae1d969... |
| Compound_4_s16.sdf | SDF | 5.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 837388a2d13c... |
| Compound_4_s4.sdf | SDF | 5.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 789b3b9bf3b3... |
| Compound_4_s5.sdf | SDF | 5.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | d0bec676e160... |
| Compound_4_s8.sdf | SDF | 5.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 29d0ae5d1ba3... |
| Compound_4_s9.sdf | SDF | 5.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | f515b7896691... |
| Compound_7_ent1.sdf | SDF | 6.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 0e6303a72b88... |
| Compound_7_ent2.sdf | SDF | 6.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 0afdc5229241... |
| Compound_8_ent1.sdf | SDF | 5.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 515b1cbb3f78... |
| Compound_8_ent2.sdf | SDF | 5.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 0da43a5e515c... |
| Compound_9_ent1.sdf | SDF | 6.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | efeb7142a2b2... |
| Compound_9_ent2.sdf | SDF | 6.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | a6b5d4ec8793... |
| 116_path.py | PY | 704 B | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/source | a316fa479eb5... |
| docking2_results.json | JSON | 399 B | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/work | dd3b3a005414... |
| 117_path.py | PY | 1.8 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/source | 89d6f3cf445c... |
| 118_path.py | PY | 670 B | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/source | 5b9746e16069... |
| 119_path.py | PY | 967 B | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/source | bc66bb192319... |
| 120_print_full_dispatch_result_diagnosis.py | PY | 423 B | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/source | 92a9912e3a42... |
| gnina_docked.sdf.gz | GZ | 3.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 962db84a11e3... |
| 121_path.py | PY | 1.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/source | a7b9da5a9563... |
| Compound_1_ent1_poses.sdf | SDF | 16.7 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | e1a137088c85... |
| Compound_1_ent2_poses.sdf | SDF | 16.7 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 984e61c6b941... |
| Compound_4_s12_poses.sdf | SDF | 15.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 45afd4dbd367... |
| Compound_4_s1_poses.sdf | SDF | 15.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 2fb89a634a93... |
| Compound_4_s4_poses.sdf | SDF | 15.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 8990d7ba7922... |
| Compound_4_s5_poses.sdf | SDF | 15.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 35d2475772c9... |
| Compound_4_s8_poses.sdf | SDF | 15.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 1c52806d20a1... |
| Compound_4_s9_poses.sdf | SDF | 15.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 98da3a6e6bca... |
| docking2_results.json | JSON | 7.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/work | ebae55855bef... |
| gnina_docked.sdf.gz | GZ | 2.7 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | ea303ca5d9ea... |
| 122_path.py | PY | 2.2 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/source | b42d5c40b41b... |
| Compound_10_ent1_poses.sdf | SDF | 18.3 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 1fc4f95e6d3f... |
| Compound_10_ent2_poses.sdf | SDF | 18.3 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 9b4c586b8250... |
| Compound_11_ent1_poses.sdf | SDF | 17.5 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 95baf8442ee5... |
| Compound_11_ent2_poses.sdf | SDF | 17.5 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | ae808f185374... |
| Compound_12_ent1_poses.sdf | SDF | 18.8 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | b81b234effba... |
| Compound_12_ent2_poses.sdf | SDF | 18.8 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 677913850227... |
| Compound_4_s13_poses.sdf | SDF | 15.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | b83bb986fbda... |
| Compound_4_s16_poses.sdf | SDF | 15.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 7af0c6b5151b... |
| Compound_7_ent1_poses.sdf | SDF | 17.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 842525848d6f... |
| Compound_7_ent2_poses.sdf | SDF | 17.0 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | cd377e85a8f4... |
| Compound_8_ent1_poses.sdf | SDF | 15.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | e9fca62ec980... |
| Compound_8_ent2_poses.sdf | SDF | 15.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | e785ce3183c4... |
| Compound_9_ent1_poses.sdf | SDF | 17.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | bceaa6292467... |
| Compound_9_ent2_poses.sdf | SDF | 17.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | ee78df8107e3... |
| docking2_results.json | JSON | 19.6 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/work | 9663e3501d23... |
| gnina_docked.sdf.gz | GZ | 3.5 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | f457eb49ecc5... |
| 123_path.py | PY | 2.3 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/source | 6db7dbd56ff1... |
| Compound_10_ent1_pose1.sdf | SDF | 3.5 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | a28c0188f7b4... |
| Compound_10_ent2_pose1.sdf | SDF | 3.5 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 365d7275bf53... |
| Compound_11_ent1_pose1.sdf | SDF | 3.4 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 92946f96bc21... |
| Compound_11_ent2_pose1.sdf | SDF | 3.4 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 7759eb07915a... |
| Compound_12_ent1_pose1.sdf | SDF | 3.6 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 1147b1e1ed7a... |
| Compound_12_ent2_pose1.sdf | SDF | 3.6 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 4c757d558b2f... |
| Compound_1_ent1_pose1.sdf | SDF | 3.2 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 643f0a05107b... |
| Compound_1_ent2_pose1.sdf | SDF | 3.2 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 4991563f3879... |
| Compound_4_s12_pose1.sdf | SDF | 2.9 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | a766276f0766... |
| Compound_4_s13_pose1.sdf | SDF | 2.9 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 4c1777214b92... |
| Compound_4_s16_pose1.sdf | SDF | 2.9 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 1746b32c4bcc... |
| Compound_4_s1_pose1.sdf | SDF | 2.9 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | c45e51a3276e... |
| Compound_4_s4_pose1.sdf | SDF | 2.9 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 9236f5e47a1e... |
| Compound_4_s5_pose1.sdf | SDF | 2.9 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 438dc9d9c124... |
| Compound_4_s8_pose1.sdf | SDF | 2.9 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 18dc6e3d9124... |
| Compound_4_s9_pose1.sdf | SDF | 2.9 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | b04ac4192ebb... |
| Compound_7_ent1_pose1.sdf | SDF | 3.3 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 5dbaaae50dd1... |
| Compound_7_ent2_pose1.sdf | SDF | 3.3 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 9f02eea4e203... |
| Compound_8_ent1_pose1.sdf | SDF | 2.9 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 21cb4a0ef5da... |
| Compound_8_ent2_pose1.sdf | SDF | 2.9 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 25f36cf706c0... |
| Compound_9_ent1_pose1.sdf | SDF | 3.3 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 3c9d65109f40... |
| Compound_9_ent2_pose1.sdf | SDF | 3.3 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/structures | 9780b10367f5... |
| docking2_ranked.json | JSON | 3.1 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/work | ccb359f50861... |
| 124_path.py | PY | 1.7 KB | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/source | efb703c1201e... |
| 125_check_if_ambertools_mmpbsa_py_available_locally.py | PY | 272 B | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/source | da0ea3e9208d... |
| 126_path.py | PY | 854 B | 02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni/source | ce2fa226578a... |
| phase_02_dock_crbn_id_enantio_2_sdf_against_4ci2_with_gni.md | MD | 19.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/reports | f77af903cefe... |
| run_mmgbsa2.py | PY | 7.6 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 9e1b65d35591... |
| ANTECHAMBER_AC.AC | AC | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 89f982009290... |
| ANTECHAMBER_AC.AC0 | AC0 | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 8fe1c613962f... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 8fe1c613962f... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 8fe1c613962f... |
| ATOMTYPE.INF | INF | 7.0 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 6fefc5874396... |
| sqm.in | IN | 2.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 86a853e28f2f... |
| sqm.out | OUT | 2.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 2b1d5b988f92... |
| leap.log | LOG | 13.0 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 31a75ec74d5e... |
| receptor.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| receptor_protein.pdb | PDB | 489.6 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 5b75f948c64f... |
| tleap_rec.in | IN | 403 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 4731449ea920... |
| mmgbsa2_run.log | LOG | 111 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | f01506401375... |
| sqm.out | OUT | 5.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | aaebc67bee1f... |
| 127_check_if_prolif_mdanalysis_available.py | PY | 392 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | d24afbb8a6a1... |
| sqm.out | OUT | 6.0 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 12bd1538da26... |
| run_interactions.py | PY | 4.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | b392c0f8650c... |
| sqm.out | OUT | 6.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | ad446e754d93... |
| mmgbsa2_run.log | LOG | 2.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | c1de2bd9ff9b... |
| sqm.out | OUT | 6.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | d6d62b038372... |
| interaction_analysis.log | LOG | 441 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | d2297563afa3... |
| ANTECHAMBER_AM1BCC_PRE.AC | AC | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 871c96f9a699... |
| sqm.pdb | PDB | 3.0 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 780a672af681... |
| phase_08_task_bt3i0n9lx.md | MD | 21.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/reports | 6e510cd9da00... |
| sqm.out | OUT | 5.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | e6a96389bf94... |
| sqm.out | OUT | 6.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | ae04677b7c2b... |
| 128_path.py | PY | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | a530797c46ec... |
| phase_09_task_bvh8nqsvc.md | MD | 22.0 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/reports | 511516608efd... |
| run_mmgbsa2.py | PY | 7.7 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 0217295c33be... |
| run_interactions.py | PY | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 6419100f1d75... |
| ANTECHAMBER_GAS.AC | AC | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 89f982009290... |
| ANTECHAMBER_GAS_AT.AC | AC | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | fc7e1700449b... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 386 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 837f7ed5fc2b... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3ab2ad5f2d87... |
| lig.frcmod | FRCMOD | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3524f8ca4bdf... |
| lig.mol2 | MOL2 | 4.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | d1729fc61765... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | f5b6e7f0596c... |
| ANTECHAMBER_AC.AC | AC | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | c97a8d12b87b... |
| ANTECHAMBER_AC.AC0 | AC0 | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 40c7f4cc4080... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 40c7f4cc4080... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 40c7f4cc4080... |
| ANTECHAMBER_GAS.AC | AC | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | c97a8d12b87b... |
| ANTECHAMBER_GAS_AT.AC | AC | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 0e9e5220bb49... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 386 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | e7acaab2cd94... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3a62d7fa2b9b... |
| lig.frcmod | FRCMOD | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3524f8ca4bdf... |
| lig.mol2 | MOL2 | 4.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 972b4a235982... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 6868c74dc5ca... |
| ANTECHAMBER_AC.AC | AC | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | dc2381d4ed04... |
| ANTECHAMBER_AC.AC0 | AC0 | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 6dab2c6f51fd... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 6dab2c6f51fd... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 6dab2c6f51fd... |
| ANTECHAMBER_GAS.AC | AC | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | dc2381d4ed04... |
| ANTECHAMBER_GAS_AT.AC | AC | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 937e131fd872... |
| ATOMTYPE.INF | INF | 6.7 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 4f009c226713... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 386 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | bd10a4fda9ef... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 64f1e4cc5e52... |
| lig.frcmod | FRCMOD | 4.6 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | b6ae56dc1e4b... |
| lig.mol2 | MOL2 | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | a4df249988b9... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 0005c5631ccb... |
| ANTECHAMBER_AC.AC | AC | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | d390ed96cf90... |
| ANTECHAMBER_AC.AC0 | AC0 | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 1a585025611c... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 1a585025611c... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 1a585025611c... |
| ANTECHAMBER_GAS.AC | AC | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | d390ed96cf90... |
| ANTECHAMBER_GAS_AT.AC | AC | 4.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 9c1899960373... |
| ATOMTYPE.INF | INF | 6.7 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 4f009c226713... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 386 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 5444f01a567c... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | f24d5bdc0e15... |
| lig.frcmod | FRCMOD | 4.6 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | b6ae56dc1e4b... |
| lig.mol2 | MOL2 | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | f83a4478dd13... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 178e7d7f7e00... |
| ANTECHAMBER_AC.AC | AC | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 40a044fc45c3... |
| ANTECHAMBER_AC.AC0 | AC0 | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 88b4a94d06b9... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 88b4a94d06b9... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 88b4a94d06b9... |
| ANTECHAMBER_GAS.AC | AC | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 40a044fc45c3... |
| ANTECHAMBER_GAS_AT.AC | AC | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | c0de00cf1446... |
| ATOMTYPE.INF | INF | 7.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 0d249c2b377a... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 386 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 4ab97ae2f81d... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | fd24a80305a6... |
| lig.frcmod | FRCMOD | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | adec3a09aed4... |
| lig.mol2 | MOL2 | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 8ca4be7d885a... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | db5216932311... |
| ANTECHAMBER_AC.AC | AC | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 474531fedf5c... |
| ANTECHAMBER_AC.AC0 | AC0 | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 1015770adf7b... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 1015770adf7b... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 1015770adf7b... |
| ANTECHAMBER_GAS.AC | AC | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 474531fedf5c... |
| ANTECHAMBER_GAS_AT.AC | AC | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | eab459350ee0... |
| ATOMTYPE.INF | INF | 7.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 0d249c2b377a... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 386 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 5bc08e5a8d1f... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | a482cb841e0e... |
| lig.frcmod | FRCMOD | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | adec3a09aed4... |
| lig.mol2 | MOL2 | 4.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 18bf5ee58301... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | ac3561a5008d... |
| ANTECHAMBER_AC.AC | AC | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 3211009f2b8c... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 0c844731f460... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 0c844731f460... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 0c844731f460... |
| ANTECHAMBER_GAS.AC | AC | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 3211009f2b8c... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | c7953e257a5a... |
| ATOMTYPE.INF | INF | 6.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 41aec34e74c9... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 383 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 629930eb1b21... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | eca5308b24af... |
| lig.frcmod | FRCMOD | 5.0 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | e0ec59720f27... |
| lig.mol2 | MOL2 | 3.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | ed8d3b6ce34b... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | d1707740c7ee... |
| ANTECHAMBER_AC.AC | AC | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 26d09af5a920... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | f1fc40aa2663... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | f1fc40aa2663... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | f1fc40aa2663... |
| ANTECHAMBER_GAS.AC | AC | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 26d09af5a920... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | d9234af0a3a0... |
| ATOMTYPE.INF | INF | 6.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 41aec34e74c9... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 383 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 5826a34e7aed... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | d0cab967d42e... |
| lig.frcmod | FRCMOD | 5.0 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | e0ec59720f27... |
| lig.mol2 | MOL2 | 3.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e442be674fed... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | bfd9e7a1b604... |
| ANTECHAMBER_AC.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 66de6fe32723... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 890f8a0eea2c... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 890f8a0eea2c... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | c36314794630... |
| ANTECHAMBER_GAS.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 66de6fe32723... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 6c4b0ed23ecb... |
| ATOMTYPE.INF | INF | 8.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | affe38725ca1... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 377 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | d2499bfee8c6... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | ada9986d2485... |
| lig.frcmod | FRCMOD | 2.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3ed7326ded7d... |
| lig.mol2 | MOL2 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | c131aeda03a4... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 717b5732feba... |
| ANTECHAMBER_AC.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | da3f38efb094... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | fa8ac2fef055... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | fa8ac2fef055... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | f3d41cf236a3... |
| ANTECHAMBER_GAS.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | da3f38efb094... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 6d0b76ec488b... |
| ATOMTYPE.INF | INF | 8.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | affe38725ca1... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 380 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | ab82f44b9a4b... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 22e2cd8b945c... |
| lig.frcmod | FRCMOD | 2.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3ed7326ded7d... |
| lig.mol2 | MOL2 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | c5c1011eb109... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | c2b658fffbcb... |
| ANTECHAMBER_AC.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 95e06e72838d... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | c508e8deb4a2... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | c508e8deb4a2... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 9c16724987a3... |
| ANTECHAMBER_GAS.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 95e06e72838d... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 847d53afba79... |
| ATOMTYPE.INF | INF | 8.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | affe38725ca1... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 380 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | a8761728cb92... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | e6bb27db76f0... |
| lig.frcmod | FRCMOD | 2.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3ed7326ded7d... |
| lig.mol2 | MOL2 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | a8ca7d73556b... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | e2070bdf8ddb... |
| ANTECHAMBER_AC.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | bf53a2e6a53b... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 956cbd5369e1... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 956cbd5369e1... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 8bed9573646b... |
| ANTECHAMBER_GAS.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | bf53a2e6a53b... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 85b4da723536... |
| ATOMTYPE.INF | INF | 8.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | affe38725ca1... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 380 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 4d7642fd0280... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | e0a1fb756576... |
| lig.frcmod | FRCMOD | 2.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3ed7326ded7d... |
| lig.mol2 | MOL2 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | a1d4d7f88635... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | f409dd15be5b... |
| ANTECHAMBER_AC.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | b3a35a577654... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 66fca9cd877e... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 66fca9cd877e... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 31777508619d... |
| ANTECHAMBER_GAS.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | b3a35a577654... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 30fbd15e8fbe... |
| ATOMTYPE.INF | INF | 8.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | affe38725ca1... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 377 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 0434d043d8e2... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 6aac8b3ed658... |
| lig.frcmod | FRCMOD | 2.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3ed7326ded7d... |
| lig.mol2 | MOL2 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 33379d1989fe... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | bbdb051503de... |
| ANTECHAMBER_AC.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 4e6051e52438... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 3f5b4cb04b93... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 3f5b4cb04b93... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 01350cd2e971... |
| ANTECHAMBER_GAS.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 4e6051e52438... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | b6908647b714... |
| ATOMTYPE.INF | INF | 8.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | affe38725ca1... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 377 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 7d9abeefaaba... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 553382411165... |
| lig.frcmod | FRCMOD | 2.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3ed7326ded7d... |
| lig.mol2 | MOL2 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 73b9b527269f... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 46dce5cddb80... |
| ANTECHAMBER_AC.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 7ae4278817e5... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | f64597790482... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | f64597790482... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 70d6729d4dae... |
| ANTECHAMBER_GAS.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 7ae4278817e5... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 75a5bbe9eb1e... |
| ATOMTYPE.INF | INF | 8.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | affe38725ca1... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 377 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | cc70c2ee6ba2... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 4a0016ef4570... |
| lig.frcmod | FRCMOD | 2.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3ed7326ded7d... |
| lig.mol2 | MOL2 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 2f1d3bc77372... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 8ab1b3f49f42... |
| ANTECHAMBER_AC.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | cf68a4028437... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | ab310f19c990... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | ab310f19c990... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 1e2eeaaf0541... |
| ANTECHAMBER_GAS.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | cf68a4028437... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | fd3973b5420b... |
| ATOMTYPE.INF | INF | 8.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | affe38725ca1... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 377 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 35786000ff57... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 04eb7877b3f5... |
| lig.frcmod | FRCMOD | 2.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3ed7326ded7d... |
| lig.mol2 | MOL2 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | b4a2797423ec... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | bb58ae6ca74d... |
| ANTECHAMBER_AC.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 61a99199f393... |
| ANTECHAMBER_AC.AC0 | AC0 | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 298c64c4db40... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 298c64c4db40... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 298c64c4db40... |
| ANTECHAMBER_GAS.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 61a99199f393... |
| ANTECHAMBER_GAS_AT.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 785e933b853d... |
| ATOMTYPE.INF | INF | 6.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | a153b0f9030b... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 383 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | a4aebfc2ceab... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 3684bb9284c4... |
| lig.frcmod | FRCMOD | 4.0 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 6607e75e83d0... |
| lig.mol2 | MOL2 | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 1851341a1c61... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 0f52f8484e57... |
| ANTECHAMBER_AC.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 7ffda8e0d322... |
| ANTECHAMBER_AC.AC0 | AC0 | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 18ba018d7e75... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 18ba018d7e75... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 18ba018d7e75... |
| ANTECHAMBER_GAS.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 7ffda8e0d322... |
| ANTECHAMBER_GAS_AT.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 90766aa27af3... |
| ATOMTYPE.INF | INF | 6.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | a153b0f9030b... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 383 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 9c17028b23e0... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 0a6770fb35e0... |
| lig.frcmod | FRCMOD | 4.0 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 6607e75e83d0... |
| lig.mol2 | MOL2 | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | fcdccbcdc5ea... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 253e0d8ea492... |
| ANTECHAMBER_AC.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | ab824b8f32d5... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | f20c8435a3af... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | f20c8435a3af... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | f20c8435a3af... |
| ANTECHAMBER_GAS.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | ab824b8f32d5... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | ff115600df38... |
| ATOMTYPE.INF | INF | 5.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | a595674b1981... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 383 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 9c4f7445039d... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 8a995025ae44... |
| lig.frcmod | FRCMOD | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 6de2f2bea4fe... |
| lig.mol2 | MOL2 | 3.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | ae2bc38ff4b8... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 448b0c90e346... |
| ANTECHAMBER_AC.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | c60096daa441... |
| ANTECHAMBER_AC.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e7d8b08ae4e8... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e7d8b08ae4e8... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e7d8b08ae4e8... |
| ANTECHAMBER_GAS.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | c60096daa441... |
| ANTECHAMBER_GAS_AT.AC | AC | 3.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 216be31997b2... |
| ATOMTYPE.INF | INF | 5.8 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | a595674b1981... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 383 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | d731cc741f1f... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | d8f2588b2fb9... |
| lig.frcmod | FRCMOD | 4.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 6de2f2bea4fe... |
| lig.mol2 | MOL2 | 3.4 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 5630df083f91... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 0e9725c41837... |
| ANTECHAMBER_AC.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 7d92080c0826... |
| ANTECHAMBER_AC.AC0 | AC0 | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | a0ad1a732c6c... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | a0ad1a732c6c... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | a0ad1a732c6c... |
| ANTECHAMBER_GAS.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 7d92080c0826... |
| ANTECHAMBER_GAS_AT.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 146bc758b198... |
| ATOMTYPE.INF | INF | 6.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 8d458acc464a... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 383 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 0d4ffaebaebd... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 6802c68f9ea6... |
| lig.frcmod | FRCMOD | 4.7 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | b2a49d417768... |
| lig.mol2 | MOL2 | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | a62322d0af20... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | dbaff1932553... |
| ANTECHAMBER_AC.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 82512f92019a... |
| ANTECHAMBER_AC.AC0 | AC0 | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 00b9f2a29ed6... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 00b9f2a29ed6... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 00b9f2a29ed6... |
| ANTECHAMBER_GAS.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 82512f92019a... |
| ANTECHAMBER_GAS_AT.AC | AC | 4.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 726f7d0801b6... |
| ATOMTYPE.INF | INF | 6.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 8d458acc464a... |
| complex.prmtop | PRMTOP | 0 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | e3b0c44298fc... |
| cpptraj.in | IN | 383 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 4b4391a1d604... |
| leap.log | LOG | 16.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 63aca7357960... |
| lig.frcmod | FRCMOD | 4.7 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | b2a49d417768... |
| lig.mol2 | MOL2 | 3.9 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | f797656a7aad... |
| tleap.in | IN | 1.2 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 062cc4e248b1... |
| mmgbsa2_results.json | JSON | 5.5 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 49ad9ca65ac1... |
| phase_11_task_bk04326pc.md | MD | 22.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/reports | bfa825c4cd63... |
| 129_os_environ_copy.py | PY | 707 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 663a1bd9408a... |
| 130_fix_his_naming_receptor_pdb_without_pdb4amber.py | PY | 1.6 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 4401acc1e86b... |
| receptor_amber.pdb | PDB | 489.6 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 5a434f37334a... |
| 131_write_fixed_receptor_pdb_corrected_his_hid_hie.py | PY | 1.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 7d87bf398f5e... |
| leap.log | LOG | 24.7 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | a56d2fdd5144... |
| tleap_rec.in | IN | 401 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 644dc9b363c9... |
| 132_os_environ_copy.py | PY | 1.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 1dd89b1ae637... |
| 133_check_all_atoms_nmet_47.py | PY | 1.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 3a1433e72295... |
| leap.log | LOG | 31.1 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 5893ba2c4100... |
| tleap_rec.in | IN | 375 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 357c6574df03... |
| 134_os_environ_copy.py | PY | 1.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | c99a8d46aa46... |
| 135_subprocess_run.py | PY | 911 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 7e39cf602885... |
| 136_subprocess_run.py | PY | 270 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 208175fbf43b... |
| leap.log | LOG | 37.6 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 09012338dc52... |
| receptor.inpcrd | INPCRD | 220.6 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 81c898c0a5e0... |
| receptor.prmtop | PRMTOP | 2.6 MB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | 447d54fa3928... |
| receptor_amber.pdb | PDB | 489.6 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/structures | d2f8c24bc907... |
| 137_os_environ_copy.py | PY | 2.0 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 4e827e4efc03... |
| run_mmgbsa2.py | PY | 7.7 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | f753d2db1af8... |
| run_mmgbsa2.py | PY | 7.7 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 83783b2f2e8d... |
| run_mmgbsa2.py | PY | 7.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 50d502dca234... |
| run_mmgbsa2.py | PY | 7.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 747b8c970fc5... |
| mmgbsa2_results.json | JSON | 2 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | cb565abe8a25... |
| 138_path.py | PY | 756 B | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/source | 2a6df1e967e7... |
| mmgbsa2_run.log | LOG | 1.0 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | a214d0243a92... |

## Verification

- 10 tool call(s) ran in this phase, 0 of which reported a failure.
- 462 file(s) were produced and registered, 462 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/gnina:latest`

## Limitations

- No citation is on record for prolif, so the versions used cannot be traced to a publication.
- Versions were not recorded for GNINA, MDAnalysis, prolif. A methods section without a version is not reproducible.

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. J Cheminform. 2021;13:43. doi:10.1186/s13321-021-00522-2
2. Landrum G, et al. RDKit: Open-source cheminformatics. doi:10.5281/zenodo.591637
   *The Zenodo DOI resolves to the latest release. Cite the DOI of the exact version used where possible.*

**Unverified candidate references.** These were matched automatically by name and have NOT been confirmed as the correct reference for the tool this study used. Two tools in different fields can share a name, so each must be checked before use.

- prolif: Cédric Bouysset, Sébastien Fiorucci. ProLIF: a library to encode molecular interactions as fingerprints. Journal of Cheminformatics. 2021. doi:10.1186/s13321-021-00548-6
