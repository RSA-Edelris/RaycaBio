---
title: "Phase 1: Kinome selectivity profile for 6 PDK1 ligands"
study_id: "7a39e116-e0d5-4e70-93c3-da6df54e7e1e"
run_id: "max-c0850e7424"
phase_index: 1
phase_id: "1"
phase_goal: "Kinome selectivity profile for 6 PDK1 ligands"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Kinome selectivity profile for 6 PDK1 ligands

## Summary

This phase set out to kinome selectivity profile for 6 PDK1 ligands. It completed 1 method step, 29 output files.

## Objective

Kinome selectivity profile for 6 PDK1 ligands

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
| gbsa | software | not recorded | no citation on record | not recorded |

### Procedure

#### 1. Molecular dynamics refinement and binding free energy calculation

EL2003A pose 2 (the best MM-GBSA pose) was refined using GROMACS molecular dynamics simulation with Generalized Born implicit solvent (GBSA) method. The system was simulated for 1 ns (500000 steps) with 50000 equilibration steps, using AMBER03 force field for protein and GAFF2 for ligand with Gasteiger charges. Binding free energy was recalculated following MD refinement.

**Rationale.** Molecular dynamics refinement improves the geometric and energetic accuracy of docked poses by allowing the system to sample conformational space and relax into local energy minima, providing more realistic binding free energy estimates.

| Field | Value |
| :--- | :--- |
| Inputs | EL2003A_pose2.sdf, 1Z5M_receptor_pH7.4.pdb |
| Outputs | best_dG_kcal_per_mol |
| Tools | gbsa |
| Status | running |

Parameters:

```yaml
boxType: dodecahedron
conc: 0.15
decompose: True
eqsteps: 50000
gpu: True
ligandCharge: gas
ligandForceField: gaff2
method: gb
mode: md
nframe: 100
nsteps: 500000
proteinForceField: amber03
```

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| ligand_smiles.json | JSON | 937 B | work | 41734fd60c2e... |
| 112_read_smiles_already_extracted.py | PY | 913 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 3b1849c8249f... |
| 113_dispatch.py | PY | 458 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 8b50d8357b81... |
| 114_agc_only_first_pdk1_s_home_family_fastest_interpret.py | PY | 486 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 0ec65c2ec5e7... |
| 115_open.py | PY | 693 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | f2dcc5404a7b... |
| 116_inspect_what_keys_came_back_find_csv.py | PY | 943 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | e7b5b9a3e1ef... |
| 117_pd_read_csv.py | PY | 229 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 9661a83e14e0... |
| 118_map_smiles_compound_name.py | PY | 627 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 06452fc58acc... |
| 119_dispatch.py | PY | 337 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 95830c34febf... |
| 120_print.py | PY | 355 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | e82527c0bdce... |
| 121_open.py | PY | 653 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | d84098d43547... |
| 122_test_can_pass_kinase_names_instead_kinase_families.py | PY | 527 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 10a95618faaa... |
| 123_clinical_off_target_panel_uniprot_accessions_covers.py | PY | 1.3 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 068f6712748d... |
| 124_remove_three_unknown_accessions_p49840_gsk3a_q96gd4.py | PY | 655 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 03c981e1d561... |
| 125_open.py | PY | 813 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 522eb67fc203... |
| 126_open.py | PY | 673 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 20887bcfcd29... |
| 127_batch_2_cmgc_core_cdk1_4_6_erk1_2_p38_jnk1.py | PY | 429 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | de90ce720723... |
| 128_open.py | PY | 1.0 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 6367d97643c4... |
| 129_open.py | PY | 996 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | b086e7866590... |
| 130_matplotlib_use.py | PY | 873 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 61973e98c3be... |
| 131_build_master_pivot_best_score_per_compound_kinase.py | PY | 985 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 849458208ddb... |
| kinome_heatmap.png | PNG | 256.3 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/figures | 8963126d795a... |
| 132_matplotlib_use.py | PY | 3.3 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 92d940638c50... |
| 133_per_compound_top_5_off_targets.py | PY | 1.8 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | ca72317b5d1f... |
| kinome_per_compound.png | PNG | 176.8 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/figures | 8d76967e9103... |
| 134_figure_2_per_compound_selectivity_bars_top_8_off.py | PY | 2.0 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 230a8cacd808... |
| 135_check_report_file.py | PY | 179 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 303bd3d9fe8c... |
| kinome_selectivity_matrix.csv | CSV | 4.1 KB | 01_kinome_selectivity_profile_for_6_pdk1_ligands/tables | ecf28dba71ba... |
| 136_shutil_copy2.py | PY | 399 B | 01_kinome_selectivity_profile_for_6_pdk1_ligands/source | 88f606d37fe4... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 29 file(s) were produced and registered, 29 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/kinasedocker2:latest`

## Limitations

- No citation is on record for gbsa, so the versions used cannot be traced to a publication.
- Versions were not recorded for gbsa. A methods section without a version is not reproducible.

## References

**No citation on record:** gbsa.

These were used by this phase and are reported for completeness. A citation should be supplied before this material is used in a manuscript. They are listed rather than omitted because a methods section that hides a dependency is not reproducible.
