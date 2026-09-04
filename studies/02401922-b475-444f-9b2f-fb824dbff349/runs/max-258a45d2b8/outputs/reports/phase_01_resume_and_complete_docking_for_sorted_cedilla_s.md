---
title: "Phase 1: Resume and complete docking for Sorted_Cedilla.sdf — all 84 compounds"
study_id: "02401922-b475-444f-9b2f-fb824dbff349"
run_id: "max-e09953def0"
phase_index: 1
phase_id: "1"
phase_goal: "Resume and complete docking for Sorted_Cedilla.sdf — all 84 compounds"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Resume and complete docking for Sorted_Cedilla.sdf — all 84 compounds

## Summary

This phase set out to resume and complete docking for Sorted_Cedilla.sdf — all 84 compounds. It completed 4 method steps, 84 output files.

## Objective

Resume and complete docking for Sorted_Cedilla.sdf — all 84 compounds

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
| RDKit | software | 2023.9.6 | doi:10.5281/zenodo.591637 | https://www.rdkit.org |

### Procedure

#### 1. Ligand standardization and preparation

Ligand structures from Sorted_Cedilla.sdf were standardized by removing hydrogens, selecting the largest fragment, canonicalizing tautomers, and retaining formal charges. Stereochemistry was assessed by enumerating chiral centers. Standardized neutral molecules were then protonated at pH 7.4 using OpenBabel with 3D coordinate generation.

**Rationale.** Standardization ensures consistent molecular representations and removes salt/counter-ion artifacts. pH 7.4 protonation matches physiological conditions for binding assays. 3D coordinates are required for docking.

| Field | Value |
| :--- | :--- |
| Inputs | Sorted_Cedilla.sdf |
| Outputs | all_std_neutral.sdf, all_protonated_3d.sdf |
| Libraries | rdkit |
| Status | running |

Parameters:

```yaml
pH: 7.4
```

#### 2. Ligand preparation for docking

Protonated 3D ligands were split into individual SDF files and converted to PDBQT format with Gasteiger partial charges for docking compatibility.

**Rationale.** AutoDock Vina requires PDBQT format with atom type and partial charge information. Individual files enable batch docking processing.

| Field | Value |
| :--- | :--- |
| Inputs | all_protonated_3d.sdf |
| Status | running |

Parameters:

```yaml
partial_charge_method: gasteiger
```

#### 3. Molecular docking with AutoDock Vina

All standardized and protonated ligands were docked against the CDK2-CCNE receptor using AutoDock Vina in batch mode. The binding site was defined by a cubic search box centered at (30.0, 3.4, -24.8) with dimensions 25×25×25 Å. Up to 5 binding poses per ligand were generated with exhaustiveness parameter 8.

**Rationale.** Vina docking explores the ligand conformational and translational space to identify energetically favorable binding modes. Multiple poses per ligand capture potential alternative binding arrangements. The search box parameters were established in prior work on this target.

| Field | Value |
| :--- | :--- |
| Inputs | receptor.pdbqt |
| Status | running |

Parameters:

```yaml
center_x: 30.0
center_y: 3.4
center_z: -24.8
energy_range: 3
exhaustiveness: 8
num_modes: 5
size_x: 25
size_y: 25
size_z: 25
```

#### 4. Docking result collection and ranking

Docking scores were extracted from PDBQT output files using regex parsing of REMARK VINA RESULT lines. Compounds were ranked by best (lowest) binding score across all 84 ligands docked.

**Rationale.** Score extraction and ranking identifies the most favorable binders and enables identification of compounds for downstream MM/GBSA refinement.

| Field | Value |
| :--- | :--- |
| Inputs | Sorted_Cedilla.sdf |
| Libraries | rdkit |
| Status | running |

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| lig34_out.pdbqt | PDBQT | 20.6 KB | structures | 5492a61fd3f0... |
| lig35_out.pdbqt | PDBQT | 21.2 KB | structures | f66fe7528e6b... |
| lig36_out.pdbqt | PDBQT | 20.6 KB | structures | 0b624d2c61f0... |
| lig37_out.pdbqt | PDBQT | 18.2 KB | structures | 236631a82760... |
| lig38_out.pdbqt | PDBQT | 18.8 KB | structures | ec5cc8ee6fc5... |
| lig39_out.pdbqt | PDBQT | 16.8 KB | structures | 57a0bc039162... |
| lig40_out.pdbqt | PDBQT | 20.2 KB | structures | 3c9f80f560e2... |
| lig41_out.pdbqt | PDBQT | 19.7 KB | structures | 59775803856b... |
| lig42_out.pdbqt | PDBQT | 16.6 KB | structures | 5858e6f82a8b... |
| lig43_out.pdbqt | PDBQT | 20.4 KB | structures | 1e5d90feff28... |
| lig44_out.pdbqt | PDBQT | 17.6 KB | structures | cc804442732f... |
| lig45_out.pdbqt | PDBQT | 18.0 KB | structures | 853bb6e2d6ea... |
| lig46_out.pdbqt | PDBQT | 19.9 KB | structures | a1f51b46a86c... |
| lig47_out.pdbqt | PDBQT | 21.0 KB | structures | 71a713fe9c28... |
| lig48_out.pdbqt | PDBQT | 19.9 KB | structures | 1e5e737050e6... |
| lig49_out.pdbqt | PDBQT | 19.2 KB | structures | ef3e1f6bfe1d... |
| lig50_out.pdbqt | PDBQT | 20.7 KB | structures | e774d1928262... |
| lig51_out.pdbqt | PDBQT | 16.2 KB | structures | d86c522631f5... |
| lig52_out.pdbqt | PDBQT | 16.6 KB | structures | 5fc7dcc3f2b7... |
| lig53_out.pdbqt | PDBQT | 20.4 KB | structures | b422840ef3eb... |
| lig54_out.pdbqt | PDBQT | 20.6 KB | structures | 87100f970225... |
| lig55_out.pdbqt | PDBQT | 21.0 KB | structures | 3fb6b912e0d4... |
| lig56_out.pdbqt | PDBQT | 18.4 KB | structures | 76c2685b7ed5... |
| lig57_out.pdbqt | PDBQT | 19.9 KB | structures | 99c79762e4b8... |
| lig58_out.pdbqt | PDBQT | 23.1 KB | structures | 7f1c2926ca04... |
| lig59_out.pdbqt | PDBQT | 20.4 KB | structures | f0243848a68a... |
| lig60_out.pdbqt | PDBQT | 21.0 KB | structures | f903177010c9... |
| lig61_out.pdbqt | PDBQT | 23.9 KB | structures | 4ce01c6251e6... |
| lig62_out.pdbqt | PDBQT | 9.3 KB | structures | 99c137d197bf... |
| lig63_out.pdbqt | PDBQT | 18.9 KB | structures | 300174405013... |
| lig64_out.pdbqt | PDBQT | 20.6 KB | structures | 9b1810fbe36d... |
| lig65_out.pdbqt | PDBQT | 16.8 KB | structures | dae9205c76d1... |
| lig66_out.pdbqt | PDBQT | 17.1 KB | structures | ade61989df10... |
| lig67_out.pdbqt | PDBQT | 21.6 KB | structures | 4d05ea943e03... |
| lig68_out.pdbqt | PDBQT | 20.7 KB | structures | 3dff97ef014f... |
| lig69_out.pdbqt | PDBQT | 21.4 KB | structures | 0553e2986522... |
| lig70_out.pdbqt | PDBQT | 20.7 KB | structures | d2b7963a9fc9... |
| lig71_out.pdbqt | PDBQT | 21.4 KB | structures | b46d9dd632a3... |
| lig72_out.pdbqt | PDBQT | 20.0 KB | structures | 73ded9926614... |
| lig73_out.pdbqt | PDBQT | 22.4 KB | structures | 7983b44919e0... |
| lig74_out.pdbqt | PDBQT | 20.3 KB | structures | fd29d8823d8e... |
| lig75_out.pdbqt | PDBQT | 16.5 KB | structures | ff6a6eacf336... |
| lig76_out.pdbqt | PDBQT | 21.0 KB | structures | 75f7fc8e0486... |
| lig77_out.pdbqt | PDBQT | 20.3 KB | structures | b3aec8391b72... |
| lig78_out.pdbqt | PDBQT | 19.4 KB | structures | a1ec16958be2... |
| lig79_out.pdbqt | PDBQT | 21.0 KB | structures | 2800d0098ec7... |
| lig80_out.pdbqt | PDBQT | 16.8 KB | structures | f66659704aa5... |
| lig81_out.pdbqt | PDBQT | 17.2 KB | structures | 6b011d805f2a... |
| lig82_out.pdbqt | PDBQT | 19.2 KB | structures | 462b75ec4d1b... |
| lig83_out.pdbqt | PDBQT | 17.2 KB | structures | c2d00aa2257e... |
| lig84_out.pdbqt | PDBQT | 21.0 KB | structures | 3a7c0c857b93... |
| missing_docking.log | LOG | 698 B | work | 82593eedff33... |
| slurm-6157320.log | LOG | 106 B | work | 1c935dd32ed2... |
| 090_os_path_join.py | PY | 588 B | source | afd188c4d0ba... |
| docking_scores.json | JSON | 16.9 KB | work | b39e83b613d2... |
| 091_os_path_join.py | PY | 2.1 KB | source | e044074faadb... |
| 093_os_path_join.csv | CSV | 319 B | tables | 6472e66bb424... |
| 092_os_path_join.py | PY | 953 B | source | 00f8852665dc... |
| min.in | IN | 84 B | work | 7d46f7fc082b... |
| mmpbsa.in | IN | 80 B | work | dcacb158ac1c... |
| run_mmgbsa.py | PY | 5.1 KB | source | 3eb4b6e64ede... |
| 093_session.py | PY | 5.8 KB | source | 74459cf7c1af... |
| ANTECHAMBER_AC.AC | AC | 9.3 KB | work | 012afbd4d5aa... |
| ANTECHAMBER_AC.AC0 | AC0 | 9.3 KB | work | 1a67bf4afe22... |
| ANTECHAMBER_BOND_TYPE.AC | AC | 9.3 KB | work | 1a67bf4afe22... |
| ANTECHAMBER_BOND_TYPE.AC0 | AC0 | 9.3 KB | work | dfc12255bed7... |
| ATOMTYPE.INF | INF | 19.6 KB | work | 0d3aab239c8c... |
| sqm.in | IN | 4.5 KB | work | 2b38f95e0131... |
| sqm.out | OUT | 8.0 KB | work | 7cbf820d168f... |
| mmgbsa_run.log | LOG | 36 B | work | 55f910ad070e... |
| 095_os_path_join.csv | CSV | 148 B | tables | 5a4cbd0d2021... |
| 094_os_path_join.py | PY | 481 B | source | 8e943a73286d... |
| sqm.out | OUT | 8.2 KB | work | 6f9acb7712f4... |
| 096_open.csv | CSV | 4.6 KB | tables | 2a9bdbd7124c... |
| 095_open.py | PY | 1.5 KB | source | 2cf868a77d27... |
| 096_os_path_join.py | PY | 3.3 KB | source | b1ba7cff73e0... |
| sqm.out | OUT | 8.3 KB | work | e7f350438d15... |
| sqm.out | OUT | 8.6 KB | work | d11789154e87... |
| 097_os_path_join.py | PY | 216 B | source | 782835f0bc88... |
| 098_build_sar_insight_top_vs_bottom_analysis.py | PY | 1.2 KB | source | 6657eef098cd... |
| sqm.out | OUT | 8.7 KB | work | 297126e8b495... |
| sqm.out | OUT | 9.0 KB | work | 07f726280133... |
| score_table.json | JSON | 18.3 KB | work | 6c92f1ebd17c... |
| 099_build_full_84_compound_score_table_string_report.py | PY | 1.3 KB | source | 5cd451f4ed84... |

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

1. Landrum G, et al. RDKit: Open-source cheminformatics. doi:10.5281/zenodo.591637
   *The Zenodo DOI resolves to the latest release. Cite the DOI of the exact version used where possible.*
