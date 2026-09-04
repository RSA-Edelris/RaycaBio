---
title: "Phase 1: Run MM-GBSA single-point free energy calculation for Cpd32 R and Cpd16 R"
study_id: "8b0911d7-7cc1-48cd-ae66-83c2c10d0be3"
run_id: "max-f0a7095298"
phase_index: 1
phase_id: "1"
phase_goal: "Run MM-GBSA single-point free energy calculation for Cpd32 R and Cpd16 R"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Run MM-GBSA single-point free energy calculation for Cpd32 R and Cpd16 R

## Summary

This phase set out to run MM-GBSA single-point free energy calculation for Cpd32 R and Cpd16 R. It completed 4 method steps, 42 output files.

## Objective

Run MM-GBSA single-point free energy calculation for Cpd32 R and Cpd16 R

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
| mmgbsa_calc.py | PY | 9.3 KB | source | e3384829c131... |
| mmgbsa_calc.py | PY | 9.3 KB | source | 5bd4841b1b05... |
| mmgbsa_calc.py | PY | 9.3 KB | source | c8e118e31b33... |
| mmgbsa_calc.py | PY | 9.2 KB | source | 993d9367b264... |
| 048_subprocess_run.py | PY | 474 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | b6cc47a6d88d... |
| mmgbsa_calc.py | PY | 9.4 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 49c06a956b19... |
| mmgbsa_calc.py | PY | 9.4 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 2b725eaec64b... |
| 049_subprocess_run.py | PY | 486 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 13b44cd94cf2... |
| 050_check_what_s_installed_could_provide_molecule.py | PY | 823 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 4a21352cd11c... |
| 051_subprocess_run.py | PY | 645 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 4de0aa3c401f... |
| 052_subprocess_run.py | PY | 491 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 8a8f2e08eed8... |
| 053_subprocess_run.py | PY | 442 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 682ecf26e77a... |
| mmgbsa_calc.py | PY | 11.2 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | b5b6acdf0d7a... |
| 054_subprocess_run.py | PY | 486 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 164ec1d07bf0... |
| 055_tempfile_mkdtemp.py | PY | 934 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | d9cfdc9069a3... |
| 056_inspect_atoms_first_hie_residue_res_30_receptor_pdb.py | PY | 1020 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | bd8ac5b44d53... |
| 057_check_actual_unique_residue_names_receptor_pdb.py | PY | 775 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | b7565ef9d518... |
| 059_collect_all_his_residue_atoms.csv | CSV | 459 B | 01_run_mm_gbsa_single_point_free_energy_calculation/tables | 31a7dc4ac32f... |
| 058_collect_all_his_residue_atoms.py | PY | 648 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 503a65637b1f... |
| 9C56_receptor_amber.pdb | PDB | 358.5 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/structures | 9810e26f23ae... |
| 059_his_atoms_items.py | PY | 1.4 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | a23289e5e121... |
| 060_tempfile_mkdtemp.py | PY | 923 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 48e753e4fbdf... |
| mmgbsa_calc.py | PY | 11.2 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 80aa4fbfa241... |
| 061_subprocess_run.py | PY | 488 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 1f4b47237a99... |
| mmgbsa_calc.py | PY | 12.1 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 67b8c25b59c0... |
| mmgbsa_calc.py | PY | 13.0 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | d25836799f04... |
| mmgbsa_calc.py | PY | 13.0 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | a673e4eca043... |
| mmgbsa_calc.py | PY | 13.1 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 9bb91ee880e4... |
| 062_subprocess_run.py | PY | 488 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | a8ae99db0086... |
| 063_cn1c.py | PY | 1.5 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 45b056f56b92... |
| 064_cn1c.py | PY | 1.6 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | c27d8b258d56... |
| test_antechamber16.py | PY | 1.1 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 5a88c87d68cf... |
| mmgbsa_calc.py | PY | 13.3 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 1710084f22aa... |
| mmgbsa_calc.py | PY | 13.3 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 30613a1091c9... |
| 065_subprocess_run.py | PY | 488 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | cbcae9b6a2e1... |
| mmgbsa_calc.py | PY | 13.7 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 96c886756690... |
| 066_subprocess_run.py | PY | 402 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 67e8ae802c56... |
| mmgbsa_calc.py | PY | 15.6 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 56dd006444d2... |
| mmgbsa_calc.py | PY | 15.8 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 7bf8b3e736b1... |
| mmgbsa_calc.py | PY | 15.8 KB | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 70c17ea6d18f... |
| mmgbsa_results.json | JSON | 538 B | 01_run_mm_gbsa_single_point_free_energy_calculation/work | 99ab58137c9b... |
| 067_subprocess_run.py | PY | 438 B | 01_run_mm_gbsa_single_point_free_energy_calculation/source | 11053cfe42cd... |

## Verification

- 4 tool call(s) ran in this phase, 0 of which reported a failure.
- 42 file(s) were produced and registered, 42 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- Versions were not recorded for AutoDock Vina, RCSB Protein Data Bank. A methods section without a version is not reproducible.

## References

1. Berman HM, et al. The Protein Data Bank. Nucleic Acids Res. 2000;28:235-242. doi:10.1093/nar/28.1.235
   *Cite the individual entry identifiers used, for example 6OIM, alongside this reference.*
2. Landrum G, et al. RDKit: Open-source cheminformatics. doi:10.5281/zenodo.591637
   *The Zenodo DOI resolves to the latest release. Cite the DOI of the exact version used where possible.*
3. Eberhardt J, Santos-Martins D, Tillack AF, Forli S. AutoDock Vina 1.2.0: New Docking Methods, Expanded Force Field, and Python Bindings. J Chem Inf Model. 2021;61:3891-3898. doi:10.1021/acs.jcim.1c00203
