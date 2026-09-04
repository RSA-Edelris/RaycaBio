---
title: "Phase 1: Build combined PDB with docked poses and FRJ reference"
study_id: "8b0911d7-7cc1-48cd-ae66-83c2c10d0be3"
run_id: "max-9bebf062a5"
phase_index: 1
phase_id: "1"
phase_goal: "Build combined PDB with docked poses and FRJ reference"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Build combined PDB with docked poses and FRJ reference

## Summary

This phase set out to build combined PDB with docked poses and FRJ reference. It completed 4 method steps, 25 output files.

## Objective

Build combined PDB with docked poses and FRJ reference

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
| RCSB Protein Data Bank | database | not recorded | doi:10.1093/nar/28.1.235 | https://www.rcsb.org |
| RDKit | software | 2023.9.6 | doi:10.5281/zenodo.591637 | https://www.rdkit.org |
| AutoDock Vina | software | not recorded | doi:10.1021/acs.jcim.1c00203 | https://vina.scripps.edu |

### Procedure

#### 1. Pocket identification from co-crystal ligand

Identified ligandable binding pocket by parsing the FRJ co-crystal ligand from the input PDB structure (9C56.pdb), calculating its centroid, and identifying all protein residues within 5 Å distance as pocket residues.

**Rationale.** Localizing the allosteric binding site using the known co-crystal ligand position ensures docking is targeted to the functionally relevant pocket.

| Field | Value |
| :--- | :--- |
| Inputs | 9C56.pdb |
| Libraries | numpy |
| Databases | RCSB PDB |
| Status | running |

Parameters:

```yaml
pocket_radius_angstrom: 5.0
```

#### 2. Ligand preparation with stereochemistry and pH adjustment

Parsed four enantiomeric ligands from V3000 SDF input, converted to V2000 format using Open Babel, extracted stereochemical information and calculated molecular properties (MW, cLogP, HBA, HBD, rotatable bonds). Ligands were prepared with 3D coordinates preserved from the input structures.

**Rationale.** Proper stereochemical representation and 3D structure preservation are critical for accurate enantiomer discrimination in docking. Format conversion ensures compatibility with downstream tools.

| Field | Value |
| :--- | :--- |
| Inputs | P965_EDELRIS_2 Hits w enantiomers.sdf |
| Outputs | ligands_v2000.sdf |
| Libraries | rdkit |
| Status | running |

Parameters:

```yaml
isomericSmiles: True
removeHs: True
sanitize: True
v3000_to_v2000_conversion: True
```

#### 3. Molecular docking with AutoDock-Vina

Performed rigid-receptor docking of four ligands against the PTPN2 allosteric site using AutoDock-Vina with a 22 × 28 × 24 Å³ docking box centered at the FRJ co-crystal ligand centroid (28.48, 12.33, 4.22). Generated 5 binding poses per ligand with exhaustiveness parameter 16.

**Rationale.** AutoDock-Vina enables rapid multi-pose sampling for binding affinity prediction and ranking of enantiomers. Box dimensions and positioning based on co-crystal pocket analysis ensure relevant conformational sampling.

| Field | Value |
| :--- | :--- |
| Inputs | 9C56_receptor.pdb, EDS00760714-1.sdf, EDS00760714-2.sdf, EDS00760778-1.sdf |
| Tools | autodock-vina |
| Status | running |

Parameters:

```yaml
box_center_x: 28.48
box_center_y: 12.33
box_center_z: 4.22
box_dimensions_x: 22
box_dimensions_y: 28
box_dimensions_z: 24
exhaustiveness: 16
ligand_format: sdf
num_modes: 5
receptor_file: 9C56_receptor.pdb
```

#### 4. Enantiomer activity assessment

Compared docking affinity scores between enantiomeric pairs to identify the active enantiomer. Cpd16 R (EDS00760778-1) showed superior binding affinity (−7.3 kcal/mol) compared to the corresponding S enantiomer, and Cpd32 R (EDS00760714-1) showed superior binding affinity (−7.0 kcal/mol) compared to Cpd32 S.

**Rationale.** Differential binding affinity between enantiomers reveals stereochemical selectivity at the allosteric site and identifies which stereoisomer is the active form.

| Field | Value |
| :--- | :--- |
| Status | running |

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| phase_06_task_af9c910da6f35bb93.md | MD | 9.9 KB | reports | f8782b0f0b8c... |
| dock_and_build_complex.py | PY | 7.8 KB | source | d0cfd8a42577... |
| 9C56_receptor.pdbqt | PDBQT | 220.4 KB | structures | fbf2cd1d68db... |
| PTPN2_9C56_docked_poses.pdb | PDB | 372.0 KB | structures | 99c7dadfdae6... |
| EDS00760714-1.pdbqt | PDBQT | 2.9 KB | structures | 16f78dab9508... |
| EDS00760714-1_poses.pdbqt | PDBQT | 15.8 KB | structures | 56845c2a7f32... |
| EDS00760714-1_results.json | JSON | 179 B | work | e9765f67c2c0... |
| EDS00760714-2.pdbqt | PDBQT | 2.9 KB | structures | 917b70f0aa83... |
| EDS00760714-2_poses.pdbqt | PDBQT | 15.8 KB | structures | 1b63f16d15eb... |
| EDS00760714-2_results.json | JSON | 179 B | work | 000176d363d9... |
| EDS00760778-1.pdbqt | PDBQT | 3.0 KB | structures | f2f1513b2aa0... |
| EDS00760778-1_poses.pdbqt | PDBQT | 16.0 KB | structures | e570dcf12b9c... |
| EDS00760778-1_results.json | JSON | 179 B | work | 6fb5d79baaf5... |
| EDS00760778-2.pdbqt | PDBQT | 3.0 KB | structures | 3a914cb21c90... |
| EDS00760778-2_poses.pdbqt | PDBQT | 16.0 KB | structures | b8f1b70d6bb3... |
| EDS00760778-2_results.json | JSON | 179 B | work | 3f622c52e895... |
| docking_report.md | MD | 428.2 KB | reports | ffb951e6482a... |
| enantiomer_comparison.png | PNG | 32.5 KB | figures | d15aa1bee0b4... |
| poses_scatter.png | PNG | 57.8 KB | figures | 071334338990... |
| score_comparison.png | PNG | 46.7 KB | figures | 8ff3e6ce1c4f... |
| EDS00760714-1_best_complex.pdb | PDB | 360.9 KB | structures | 670567c7c77f... |
| EDS00760714-2_best_complex.pdb | PDB | 360.9 KB | structures | b55bf01e53b4... |
| EDS00760778-1_best_complex.pdb | PDB | 360.9 KB | structures | 219dda87ebd2... |
| EDS00760778-2_best_complex.pdb | PDB | 360.9 KB | structures | 53bb3e6afa6a... |
| pose_analysis.json | JSON | 7.3 KB | work | 3935eac971ff... |

## Verification

- 4 tool call(s) ran in this phase, 0 of which reported a failure.
- 25 file(s) were produced and registered, 25 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- Versions were not recorded for AutoDock Vina, RCSB Protein Data Bank. A methods section without a version is not reproducible.

## References

1. Berman HM, et al. The Protein Data Bank. Nucleic Acids Res. 2000;28:235-242. doi:10.1093/nar/28.1.235
   *Cite the individual entry identifiers used, for example 6OIM, alongside this reference.*
2. Landrum G, et al. RDKit: Open-source cheminformatics. doi:10.5281/zenodo.591637
   *The Zenodo DOI resolves to the latest release. Cite the DOI of the exact version used where possible.*
3. Eberhardt J, Santos-Martins D, Tillack AF, Forli S. AutoDock Vina 1.2.0: New Docking Methods, Expanded Force Field, and Python Bindings. J Chem Inf Model. 2021;61:3891-3898. doi:10.1021/acs.jcim.1c00203
