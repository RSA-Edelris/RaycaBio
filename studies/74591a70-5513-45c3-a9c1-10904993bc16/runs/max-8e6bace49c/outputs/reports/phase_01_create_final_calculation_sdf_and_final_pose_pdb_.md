---
title: "Phase 1: Create final_calculation.sdf and final_pose.pdb with all docking/GBSA/pose results"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-8e6bace49c"
phase_index: 1
phase_id: "1"
phase_goal: "Create final_calculation.sdf and final_pose.pdb with all docking/GBSA/pose results"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Create final_calculation.sdf and final_pose.pdb with all docking/GBSA/pose results

## Summary

This phase set out to create final_calculation.sdf and final_pose.pdb with all docking/GBSA/pose results. It completed 10 method steps, 22 output files.

## Objective

Create final_calculation.sdf and final_pose.pdb with all docking/GBSA/pose results

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
| 146_path.py | PY | 1.0 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | facd5cb1b110... |
| 147_check_if_lvy_present_prepared_receptor_look_original.py | PY | 953 B | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | 03ab17111a76... |
| 148_preview_lvy_reference_receptor_first_5_lines.py | PY | 991 B | 01_create_final_calculation_sdf_and_final_pose_pdb_/inputs | 9440aa5c1137... |
| 149_path.py | PY | 649 B | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | 786d8607eca6... |
| build_final_outputs.py | PY | 7.7 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | b0fb2628779d... |
| final_calculation.sdf | SDF | 83.2 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/structures | 42b84764960b... |
| final_pose.pdb | PDB | 549.8 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/structures | a1563422d1e5... |
| 150_subprocess_run.py | PY | 460 B | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | 4c05624d6ba3... |
| build_final_outputs.py | PY | 7.6 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | 587afd70460d... |
| build_final_outputs.py | PY | 8.6 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | 51f27399fc46... |
| build_final_outputs.py | PY | 7.8 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | 69df25eb54a3... |
| build_final_outputs.py | PY | 7.9 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | 6c25b6badc92... |
| build_final_outputs.py | PY | 8.1 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | 30f875494b58... |
| final_calculation_2d.sdf | SDF | 83.2 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/structures | edc516a84bcc... |
| 151_subprocess_run.py | PY | 408 B | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | fb2dcbed0942... |
| 152_path.py | PY | 1.9 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | 70092839f9fc... |
| 153_path.py | PY | 679 B | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | f7e734f22fc0... |
| build_final_outputs.py | PY | 8.3 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | f220e42e44ad... |
| final_calculation.sdf | SDF | 76.4 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/structures | cdc25ee6cce0... |
| final_calculation_2d.sdf | SDF | 76.4 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/structures | a9af2f012732... |
| 154_subprocess_run.py | PY | 493 B | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | 290bbbf40a36... |
| 155_path.py | PY | 3.2 KB | 01_create_final_calculation_sdf_and_final_pose_pdb_/source | eb6a7640a6b0... |

## Verification

- 10 tool call(s) ran in this phase, 0 of which reported a failure.
- 22 file(s) were produced and registered, 22 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No citation is on record for prolif, so the versions used cannot be traced to a publication.
- Versions were not recorded for GNINA, MDAnalysis, prolif. A methods section without a version is not reproducible.

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. J Cheminform. 2021;13:43. doi:10.1186/s13321-021-00522-2
2. Landrum G, et al. RDKit: Open-source cheminformatics. doi:10.5281/zenodo.591637
   *The Zenodo DOI resolves to the latest release. Cite the DOI of the exact version used where possible.*

**Unverified candidate references.** These were matched automatically by name and have NOT been confirmed as the correct reference for the tool this study used. Two tools in different fields can share a name, so each must be checked before use.

- prolif: Cédric Bouysset, Sébastien Fiorucci. ProLIF: a library to encode molecular interactions as fingerprints. Journal of Cheminformatics. 2021. doi:10.1186/s13321-021-00548-6
