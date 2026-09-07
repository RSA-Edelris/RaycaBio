---
title: "Phase 8: task bt3i0n9lx"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-6aa66319d7"
phase_index: 8
phase_id: "bt3i0n9lx"
phase_goal: "task bt3i0n9lx"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 8: task bt3i0n9lx

## Summary

This phase set out to task bt3i0n9lx. It completed 3 method steps, 145 output files.

## Objective

task bt3i0n9lx

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

#### 1. Binding free energy calculation by MM-GBSA

Single-trajectory MM-GBSA calculations were performed on snapshots from the molecular dynamics trajectory using MMPBSA.py, computing molecular mechanical energy and generalized Born solvation free energy to estimate ΔG_MM-GBSA for each ligand.

**Rationale.** End-point free energy method to estimate ligand binding affinity from MD ensemble, combining gas-phase force field energies with implicit solvent effects.

| Field | Value |
| :--- | :--- |
| Outputs | mmgbsa_results.csv |
| Status | running |

Parameters:

```yaml
implicit_solvent: igb=5
trajectory_type: single-trajectory
```

#### 2. Ligand parameterization and receptor-ligand topology preparation

Ligand structures were converted to MOL2 format using antechamber with Gasteiger partial charges and GAFF2 force field, missing parameters were generated with parmchk2, and receptor-ligand complexes were assembled into AMBER topology and coordinate files using tleap with ff14SB for the protein.

**Rationale.** Standard AMBER workflow to prepare molecular systems for implicit solvent simulations, establishing force field parameters and system topology necessary for subsequent dynamics.

| Field | Value |
| :--- | :--- |
| Inputs | 4CI2_receptor_noh.pdb, best_poses/{name}_pose1.sdf |
| Status | running |

Parameters:

```yaml
antechamber_charge_method: gas
antechamber_force_field: gaff2
parmchk2_force_field: gaff2
protein_force_field: ff14SB
```

#### 3. Geometry optimization and molecular dynamics in implicit solvent

Minimization (500 steps) and molecular dynamics (10000 steps) simulations were performed on each complex using sander in implicit solvent (igb=5 OBC) with a cutoff of 12.0 Å, temperature 300K maintained with Langevin thermostat, and SHAKE constraints on hydrogen-containing bonds.

**Rationale.** Equilibration of docked poses and sampling of conformational space in implicit solvent to establish a trajectory for subsequent energy calculations.

| Field | Value |
| :--- | :--- |
| Status | running |

Parameters:

```yaml
cutoff: 12.0
gamma_ln: 2.0
implicit_solvent_model: igb=5
md_nstlim: 10000
md_timestep: 0.002
minimization_maxcyc: 500
minimization_ncyc: 200
ntc: 2
ntf: 2
temperature: 300.0
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
| mmgbsa2_run.log | LOG | 2.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | 2a897fce9b46... |
| sqm.out | OUT | 6.3 KB | 03_run_mm_gbsa_on_best_docking_poses_and_write_fina/work | d6d62b038372... |

## Verification

- 3 tool call(s) ran in this phase, 0 of which reported a failure.
- 145 file(s) were produced and registered, 145 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/gnina:latest`

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

This phase recorded no external tools or databases.
