---
title: "Phase 3: task bmcy9smmz"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-5c6f9d06e5"
phase_index: 3
phase_id: "bmcy9smmz"
phase_goal: "task bmcy9smmz"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 3: task bmcy9smmz

## Summary

This phase set out to task bmcy9smmz. It completed 3 method steps, 284 output files.

## Objective

task bmcy9smmz

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
| EDEL-CRBN-0001_ent_ent_md.nc | NC | 3.6 MB | work | 16f968269ac0... |
| EDEL-CRBN-0001_ent_ent_md.rst7 | RST7 | 291.9 KB | structures | b985a36f4305... |
| EDEL-CRBN-0001_ent_md.nc | NC | 3.6 MB | work | faff78ec40e2... |
| EDEL-CRBN-0001_ent_md.rst7 | RST7 | 291.9 KB | structures | 645e00e11393... |
| EDEL-CRBN-0002_ent_ent_md.nc | NC | 3.6 MB | work | b2b7e1049f7f... |
| EDEL-CRBN-0002_ent_ent_md.rst7 | RST7 | 292.0 KB | structures | 1484108721bf... |
| EDEL-CRBN-0002_ent_md.nc | NC | 3.6 MB | work | fed540006e13... |
| EDEL-CRBN-0002_ent_md.rst7 | RST7 | 292.0 KB | structures | f6345487e7fc... |
| EDEL-CRBN-0003_ent_ent_md.nc | NC | 3.6 MB | work | 666c494cdae0... |
| EDEL-CRBN-0003_ent_ent_md.rst7 | RST7 | 292.0 KB | structures | 9e7c05cddb96... |
| EDEL-CRBN-0003_ent_md.nc | NC | 3.6 MB | work | 295805b2de71... |
| EDEL-CRBN-0003_ent_md.rst7 | RST7 | 292.0 KB | structures | 817a76edcca2... |
| EDEL-CRBN-0004_ent_ent_md.nc | NC | 3.6 MB | work | da4f042d8b95... |
| EDEL-CRBN-0004_ent_ent_md.rst7 | RST7 | 292.1 KB | structures | 81989ddd6df6... |
| EDEL-CRBN-0004_ent_md.nc | NC | 3.6 MB | work | 59a0d8e19802... |
| EDEL-CRBN-0004_ent_md.rst7 | RST7 | 292.1 KB | structures | a701f12cbb5a... |
| EDEL-CRBN-0005_ent_ent_md.nc | NC | 3.6 MB | work | 6d576d541f3a... |
| EDEL-CRBN-0005_ent_ent_md.rst7 | RST7 | 292.1 KB | structures | d9c1e3032449... |
| EDEL-CRBN-0005_ent_md.nc | NC | 3.6 MB | work | d27c3df671bd... |
| EDEL-CRBN-0005_ent_md.rst7 | RST7 | 292.1 KB | structures | f8e98f45317c... |
| EDEL-CRBN-0006_ent_ent_md.nc | NC | 3.6 MB | work | 7eb57eea7695... |
| EDEL-CRBN-0006_ent_ent_md.rst7 | RST7 | 292.2 KB | structures | 05c382964c51... |
| EDEL-CRBN-0006_ent_md.nc | NC | 3.6 MB | work | edab429dc07a... |
| EDEL-CRBN-0006_ent_md.rst7 | RST7 | 292.2 KB | structures | 9f38358b7e6f... |
| EDEL-CRBN-0007_ent_ent_md.nc | NC | 3.6 MB | work | 188c2bfb4011... |
| EDEL-CRBN-0007_ent_ent_md.rst7 | RST7 | 292.2 KB | structures | b36141ede012... |
| EDEL-CRBN-0007_ent_md.nc | NC | 3.6 MB | work | ccb0cddf1f2c... |
| EDEL-CRBN-0007_ent_md.rst7 | RST7 | 292.2 KB | structures | 1d2f2caf7ac2... |
| EDEL-CRBN-0008_ent_ent_md.nc | NC | 3.6 MB | work | 5dbde1eebc5b... |
| EDEL-CRBN-0008_ent_ent_md.rst7 | RST7 | 292.2 KB | structures | 9f6ad25e7d75... |
| EDEL-CRBN-0008_ent_md.nc | NC | 3.6 MB | work | b4fb4df7dd4e... |
| EDEL-CRBN-0008_ent_md.rst7 | RST7 | 292.2 KB | structures | da983c798193... |
| EDEL-CRBN-0009_ent_ent_md.nc | NC | 3.6 MB | work | 1a18f3829a65... |
| EDEL-CRBN-0009_ent_ent_md.rst7 | RST7 | 292.3 KB | structures | a3ef86f842c1... |
| EDEL-CRBN-0009_ent_md.nc | NC | 3.6 MB | work | b23d02ec6bdb... |
| EDEL-CRBN-0009_ent_md.rst7 | RST7 | 292.3 KB | structures | 759f48d6fe9f... |
| EDEL-CRBN-0010_ent_ent_md.nc | NC | 3.6 MB | work | a0c484d4c95d... |
| EDEL-CRBN-0010_ent_ent_md.rst7 | RST7 | 292.3 KB | structures | 713af6109bf2... |
| EDEL-CRBN-0010_ent_md.nc | NC | 3.6 MB | work | bc6a81fe9460... |
| EDEL-CRBN-0010_ent_md.rst7 | RST7 | 292.3 KB | structures | eef7739fa2c9... |
| EDEL-CRBN-0011_ent_ent_md.nc | NC | 3.6 MB | work | 0656fa836a92... |
| EDEL-CRBN-0011_ent_ent_md.rst7 | RST7 | 292.3 KB | structures | c0ce6e3b1bc4... |
| EDEL-CRBN-0011_ent_md.nc | NC | 3.6 MB | work | 92981595c59c... |
| EDEL-CRBN-0011_ent_md.rst7 | RST7 | 292.3 KB | structures | fc6914cd683a... |
| EDEL-CRBN-0012_ent_ent_md.nc | NC | 3.6 MB | work | 0656fa836a92... |
| EDEL-CRBN-0012_ent_ent_md.rst7 | RST7 | 292.3 KB | structures | c0ce6e3b1bc4... |
| EDEL-CRBN-0012_ent_md.nc | NC | 3.6 MB | work | 92981595c59c... |
| EDEL-CRBN-0012_ent_md.rst7 | RST7 | 292.3 KB | structures | fc6914cd683a... |
| EDEL-CRBN-0013_ent_ent_md.nc | NC | 3.6 MB | work | a66cb857ad80... |
| EDEL-CRBN-0013_ent_ent_md.rst7 | RST7 | 292.4 KB | structures | b6100a866254... |
| EDEL-CRBN-0013_ent_md.nc | NC | 3.6 MB | work | a2c7e30b9a9d... |
| EDEL-CRBN-0013_ent_md.rst7 | RST7 | 292.4 KB | structures | 268cf012720e... |
| EDEL-CRBN-0014_ent_ent_md.nc | NC | 3.6 MB | work | 9b2816fbaba1... |
| EDEL-CRBN-0014_ent_ent_md.rst7 | RST7 | 292.4 KB | structures | ffe1c38575a3... |
| EDEL-CRBN-0014_ent_md.nc | NC | 3.6 MB | work | cbe11018c8e2... |
| EDEL-CRBN-0014_ent_md.rst7 | RST7 | 292.4 KB | structures | b6e015c41cc1... |
| EDEL-CRBN-0015_ent_ent_md.nc | NC | 3.6 MB | work | 3e38bd4711ea... |
| EDEL-CRBN-0015_ent_ent_md.rst7 | RST7 | 292.4 KB | structures | 3ec1ad7facc9... |
| EDEL-CRBN-0015_ent_md.nc | NC | 3.6 MB | work | 31632c64a5bd... |
| EDEL-CRBN-0015_ent_md.rst7 | RST7 | 292.4 KB | structures | 45d6b42576d9... |
| EDEL-CRBN-0016_ent_ent_md.nc | NC | 3.6 MB | work | f9bd15ce5630... |
| EDEL-CRBN-0016_ent_ent_md.rst7 | RST7 | 292.5 KB | structures | 771f8c6ade13... |
| EDEL-CRBN-0016_ent_md.nc | NC | 3.6 MB | work | c27e3b81340c... |
| EDEL-CRBN-0016_ent_md.rst7 | RST7 | 292.5 KB | structures | fb7f09ff3abc... |
| slurm-21779205.log | LOG | 8.1 KB | work | de0bbfb4aaa0... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | faff78ec40e2... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 16f968269ac0... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | fed540006e13... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | b2b7e1049f7f... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 295805b2de71... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 666c494cdae0... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 59a0d8e19802... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | da4f042d8b95... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | d27c3df671bd... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 6d576d541f3a... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | edab429dc07a... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7eb57eea7695... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | ccb0cddf1f2c... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 188c2bfb4011... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | b4fb4df7dd4e... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 5dbde1eebc5b... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | b23d02ec6bdb... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 1a18f3829a65... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | bc6a81fe9460... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | a0c484d4c95d... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 92981595c59c... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 0656fa836a92... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 92981595c59c... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 0656fa836a92... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | a2c7e30b9a9d... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | a66cb857ad80... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | cbe11018c8e2... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 9b2816fbaba1... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 31632c64a5bd... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 3e38bd4711ea... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | c27e3b81340c... |
| md.nc | NC | 3.6 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | f9bd15ce5630... |
| 094_amber_env.py | PY | 1.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/source | 302801e75d34... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 0a2c456ea530... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | f412e56fcfc0... |
| _MMPBSA_complex.pdb | PDB | 492.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 80f427572d7e... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 20594f6db1d1... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | d5f153358897... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 76dd3837a59c... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 5139259610f3... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 7736ad49de35... |
| _MMPBSA_info | not recorded | 4.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 3e5849333d03... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 38.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 5518fe5f6ba9... |
| _MMPBSA_ligand.pdb | PDB | 2.6 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 433c159a881d... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 63006f6a3635... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 46d11ae3ea0f... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 8967417e84d2... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 915bb53b5562... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7825ce73cf8e... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | ee7645057dbf... |
| mmgbsa.in | IN | 111 B | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7f63d288f9cb... |
| reference.frc | FRC | 63.9 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/inputs | ac583d303467... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 4be2d12280f6... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | ab89eb361b41... |
| _MMPBSA_complex.pdb | PDB | 492.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 8d53509c4225... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 42ac2ff7b2e0... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 872474eee354... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | d0906a472003... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 3eea9201525f... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | dbb2144fc81b... |
| _MMPBSA_info | not recorded | 4.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | cbc0e6ff761c... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 38.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 2ede9e4f44b8... |
| _MMPBSA_ligand.pdb | PDB | 2.6 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 5786f813ffc4... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 66e9c582e1e0... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 85fcafa6fa84... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | bc6211bf230d... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | e44931ec83f9... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | b46441fbaa9e... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 65a5ad95c6db... |
| mmgbsa.in | IN | 111 B | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7f63d288f9cb... |
| reference.frc | FRC | 63.9 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/inputs | 5752b2659657... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | de6a12960e0b... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | eda8fe338a0c... |
| _MMPBSA_complex.pdb | PDB | 492.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | cdd492f1fb42... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7115a2758ee0... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 11d8d2ca297d... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 3d74307a84de... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | b86ff7879e01... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | c9956b4001ad... |
| _MMPBSA_info | not recorded | 4.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | d9c0f5e8ef72... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 38.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | b0bdcd765880... |
| _MMPBSA_ligand.pdb | PDB | 2.6 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 9a1d640a59bf... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 5e8853ccd12f... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | d0e1c337baa9... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 55d50f4dc7d7... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | a1a88766b068... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | c52c4a3029e7... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | be314478e231... |
| mmgbsa.in | IN | 111 B | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7f63d288f9cb... |
| reference.frc | FRC | 63.9 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/inputs | 29b66cec291c... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 5fa2da5e7c04... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 3c3c9a854aa1... |
| _MMPBSA_complex.pdb | PDB | 492.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 431f33c4030e... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 25928b6ea80a... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 78d45a2177d3... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | ef9b42dba36f... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 41f1ea4565c8... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 3d45d9c81819... |
| _MMPBSA_info | not recorded | 4.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 9051e74b985f... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 38.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 6f45f3719c2e... |
| _MMPBSA_ligand.pdb | PDB | 2.6 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 3c9bdce66128... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 67a7b7acf3d3... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 623bfd51a05d... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | a84eff43883c... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 95cf56a27d50... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | d56dc23f1024... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | bd9b59482955... |
| mmgbsa.in | IN | 111 B | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7f63d288f9cb... |
| reference.frc | FRC | 63.9 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/inputs | 4b144dd9db1b... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | c2674318eee9... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 9df3ea6efb7b... |
| _MMPBSA_complex.pdb | PDB | 492.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | bbe315d8df11... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 273a4e7fad37... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | acad3a672dd2... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | cf28c520d607... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | eb28529d8b9d... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 78bdfe863c2a... |
| _MMPBSA_info | not recorded | 4.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 318c30754e9b... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 40.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | f4d79000777b... |
| _MMPBSA_ligand.pdb | PDB | 2.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | f94c6cb41fc8... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | e17cfa2e6676... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 67d1fe25b284... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | c16b90245edd... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | f4852746e8e4... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | feefe63fd3e1... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 98ff4303f55b... |
| mmgbsa.in | IN | 111 B | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7f63d288f9cb... |
| reference.frc | FRC | 63.9 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/inputs | d1878c8bfc33... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 239c157db027... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | e4e0f7eb719d... |
| _MMPBSA_complex.pdb | PDB | 492.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 0285d1472adc... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 05e454b20939... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 8de9d64283c2... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 28822cbf5a89... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 54262bbc1592... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 7fc91f876223... |
| _MMPBSA_info | not recorded | 4.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | c8fd0ee8cd4d... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 40.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7dae7853cb96... |
| _MMPBSA_ligand.pdb | PDB | 2.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 17029460754b... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | cf5f31a7e1d6... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 2f6b7dd1bc82... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 8dbdabe775f1... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | f1623b747bef... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | d7527d286837... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 845686356e3a... |
| mmgbsa.in | IN | 111 B | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7f63d288f9cb... |
| reference.frc | FRC | 63.9 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/inputs | 18c61a9725dc... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 2feb08e20a6e... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | e13bb1e25a25... |
| _MMPBSA_complex.pdb | PDB | 492.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | b1e1c58e4f16... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 953929091193... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7a62d34e2181... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 04b973d8804e... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 5288f91c2f43... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | cd7f46a7c091... |
| _MMPBSA_info | not recorded | 4.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7baaa9f4ba9e... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 40.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | a572710e5a92... |
| _MMPBSA_ligand.pdb | PDB | 2.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 80b131f8c8c5... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | f17af022dabe... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | f21a6d56710c... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 27b42561459d... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | b3a426178c90... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 546271756b7d... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 937bfcc75c74... |
| mmgbsa.in | IN | 111 B | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7f63d288f9cb... |
| reference.frc | FRC | 63.9 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/inputs | 70b79627bf1a... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | ed333eaac5c2... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 8cb0cab6256a... |
| _MMPBSA_complex.pdb | PDB | 492.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 7451b1fa2dcb... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 0c0f75ffbc22... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | dd77216d4618... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 9ca108d9ac24... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 329f3cb06e37... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | b6e3440e6314... |
| _MMPBSA_info | not recorded | 4.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 31ed19fbf597... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 40.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 4ac12d7c0d10... |
| _MMPBSA_ligand.pdb | PDB | 2.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 87879af7a471... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 5ba40076b75b... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 98f4d67d3b0f... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 93c98c33d8cb... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 8098db790df9... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 9fea51d934cd... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | ddda0c0f49d7... |
| mmgbsa.in | IN | 111 B | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7f63d288f9cb... |
| reference.frc | FRC | 63.9 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/inputs | 56d51d5065a9... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 1da86d7b486d... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 6b105a760eaa... |
| _MMPBSA_complex.pdb | PDB | 492.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 25eddb3515b5... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 9edb889784f7... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | fce1c33f44a9... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 4728aa7d6eab... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 3a8b687e81fc... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 24053099b483... |
| _MMPBSA_info | not recorded | 4.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 5ef238c81303... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 39.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | fd2c816ffe43... |
| _MMPBSA_ligand.pdb | PDB | 2.6 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | a9560ddb0946... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | a50a4c759405... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 925a7e1a26c6... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | ef758a70c00e... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 29475ee60d8f... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | aa922d2b7ecb... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | eed17819aea4... |
| mmgbsa.in | IN | 111 B | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7f63d288f9cb... |
| reference.frc | FRC | 63.9 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/inputs | 94a02e0988da... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 874993fda7d8... |
| _MMPBSA_complex.pdb | PDB | 492.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | b2d987a9a0c2... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 1.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | ffa8c5c1b384... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.8 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 8e168a491c39... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.3 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | df9cf0b01e3c... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 4c525e7c3007... |
| _MMPBSA_gb.mdin | MDIN | 71 B | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 221e48a389dc... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 39.2 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 5e63995a0bc7... |
| _MMPBSA_ligand.pdb | PDB | 2.6 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 24f6873ef486... |
| _MMPBSA_normal_traj_cpptraj.out | OUT | 8.7 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 6a009a7f3845... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 0157a2282263... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/structures | 0ec8cea00fa9... |
| mmgbsa.in | IN | 111 B | 01_running_mmpbsa_py_on_32_lumi_trajectories/work | 7f63d288f9cb... |
| reference.frc | FRC | 1.9 MB | 01_running_mmpbsa_py_on_32_lumi_trajectories/inputs | 15a6bb740c8c... |
| 095_amber_env.py | PY | 3.5 KB | 01_running_mmpbsa_py_on_32_lumi_trajectories/source | 93483f94f136... |

## Verification

- 3 tool call(s) ran in this phase, 0 of which reported a failure.
- 284 file(s) were produced and registered, 284 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

This phase recorded no external tools or databases.
