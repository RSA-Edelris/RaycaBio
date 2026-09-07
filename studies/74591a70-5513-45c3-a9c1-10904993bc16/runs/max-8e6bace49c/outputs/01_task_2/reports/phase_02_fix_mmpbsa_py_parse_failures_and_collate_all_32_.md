---
title: "Phase 2: Fix MMPBSA.py parse failures and collate all 32 results"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-87b48fba63"
phase_index: 2
phase_id: "1"
phase_goal: "Fix MMPBSA.py parse failures and collate all 32 results"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 2: Fix MMPBSA.py parse failures and collate all 32 results

## Summary

This phase set out to fix MMPBSA.py parse failures and collate all 32 results. It completed 3 method steps, 362 output files.

## Objective

Fix MMPBSA.py parse failures and collate all 32 results

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
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 4cd9eb68bc2b... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | d2ec03aca0c3... |
| _MMPBSA_complex.pdb | PDB | 491.8 KB | structures | c7609dabda20... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 31734f5f2d5d... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | e689e5de93a6... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.7 KB | structures | e8180e80d8b5... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.1 KB | structures | 7a2a365c3859... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | 836a183bcda8... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 6075b2d34462... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 33.3 KB | work | 35896d8f75c7... |
| _MMPBSA_ligand.pdb | PDB | 2.2 KB | structures | dc1c7091f9b5... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | a7fc6f22284d... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | 1ccf1d191152... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | a6db6dd5465f... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 0248a7712501... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | ac2706012029... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 00406a9f18e1... |
| reference.frc | FRC | 125.6 MB | inputs | f13bd59c99ea... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 2c07529a1da7... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | af7295973ed2... |
| _MMPBSA_complex.pdb | PDB | 491.9 KB | structures | 6b30338a9b29... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 1d4c0af50efa... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 3c78169897dc... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.7 KB | structures | 3d6758962481... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.2 KB | structures | 743eae8ce3f5... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | 369abd9e8db2... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 99a01d7f3bc3... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 35.7 KB | work | 96259777e02a... |
| _MMPBSA_ligand.pdb | PDB | 2.4 KB | structures | 9f49bf9de819... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 097fdf952318... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | 4a8780e93ebf... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | d2822a6b7954... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | a830ba161f61... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | b447e0ba54d8... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | d961f5626796... |
| reference.frc | FRC | 125.6 MB | inputs | c9f406393643... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 6eae331755a6... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | 0061ae955fa6... |
| _MMPBSA_complex.pdb | PDB | 491.9 KB | structures | fd2b9a25f87b... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 86936162024a... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 9dec6998845f... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.7 KB | structures | 9cec378d1e14... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.2 KB | structures | 75ebf08bb6a9... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | 8a016c9bd138... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 2954a30ab17a... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 35.7 KB | work | 25fabdc933b9... |
| _MMPBSA_ligand.pdb | PDB | 2.4 KB | structures | 35abd4474bae... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 4e3733fefec4... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | cbe610d70bbb... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | fe19d87c87b8... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 4972140824ab... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | d0b40cf32638... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | a0cc0fbd3e5d... |
| reference.frc | FRC | 125.6 MB | inputs | 35c2cc723534... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 81238e79f8b1... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | c6652898e10c... |
| _MMPBSA_complex.pdb | PDB | 491.9 KB | structures | a85261930466... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | b1978d3d874c... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | c22040ab57d6... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.7 KB | structures | 0c389e94de5f... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.2 KB | structures | f90f5b348ce1... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | f33bc222e78e... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 2ec2be100fbb... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 35.7 KB | work | b23d97fe3a3e... |
| _MMPBSA_ligand.pdb | PDB | 2.4 KB | structures | 436f6f795d34... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 22f3914d25f9... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | 42163469318e... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | 9f9e4b990627... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 7230fc47b618... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | 34707559bdb7... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | ba788986ec29... |
| reference.frc | FRC | 125.6 MB | inputs | 07dd727df676... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 01b2f10f4da1... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | 61ebcfc62b66... |
| _MMPBSA_complex.pdb | PDB | 491.9 KB | structures | 81cb8b3f3d2b... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | f26f8c8b165f... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | b9db01d308cd... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.7 KB | structures | 42e62e033574... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.2 KB | structures | 6512f78aa1c3... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | c3fea9b87c9c... |
| _MMPBSA_info | not recorded | 4.1 KB | work | a85534fffe10... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 35.7 KB | work | 824816e70c1f... |
| _MMPBSA_ligand.pdb | PDB | 2.4 KB | structures | 4b5fc3ee325c... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | da17f1e60a92... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | 3a357f525f0f... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | f30cfeccda91... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 33996d7d416c... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | c63ba1cb1ab0... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 37c6dfa2e7ef... |
| reference.frc | FRC | 125.6 MB | inputs | 064d895aa349... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 80e13aa9df13... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 28e05272ca7b... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | ecaaac05569b... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 2960d7501343... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 763ba96705f3... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | 5a4e25441337... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | 814296d385f5... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 14d1e621a768... |
| reference.frc | FRC | 125.7 MB | inputs | adef5625e7c1... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 0eafbed02ff7... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | a5d0bb55ddd1... |
| _MMPBSA_complex.pdb | PDB | 492.4 KB | structures | 66df8bf2a392... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | a5e8581c901f... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 30e0c8b9ca67... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 222.0 KB | structures | 2419a37eecca... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.4 KB | structures | 5aa794a7a352... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | 39353cda44e6... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 4033dc97842d... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 42.8 KB | work | a38907fd8ae7... |
| _MMPBSA_ligand.pdb | PDB | 2.9 KB | structures | d329300ece52... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | d228800b0169... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | 2740831a73b8... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | 0a7cd6c5a759... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 0bb4772746e1... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | cabdfbe449a6... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 4c10cfd5161a... |
| reference.frc | FRC | 126.4 MB | inputs | 9d91c427f2db... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 52932596219e... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | 601bb92defa1... |
| _MMPBSA_complex.pdb | PDB | 492.4 KB | structures | 087e7ab445c6... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 03b70ddf2aac... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 6bfa4ab5e688... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 222.0 KB | structures | 1fc7a1a555d7... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.4 KB | structures | 6cb794b51062... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | 3074cd258b02... |
| _MMPBSA_info | not recorded | 4.1 KB | work | bcb00cfcb3fe... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 42.8 KB | work | f0f73a21123e... |
| _MMPBSA_ligand.pdb | PDB | 2.9 KB | structures | 2b8e61e84a1a... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | f7b5bcdc8ae0... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | 97f51a410ab7... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | 3d81d41a5cd7... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | e09fad6d42f9... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | 336ba8c3c5fe... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | ed94cef231dc... |
| reference.frc | FRC | 126.4 MB | inputs | 0f674fe1b526... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 3a9e52b92206... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | 24f5fdbc2b9a... |
| _MMPBSA_complex.pdb | PDB | 492.3 KB | structures | a526710f7332... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 37a9423431e1... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 8f6a3d30bafe... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.9 KB | structures | ddaed80a560d... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.3 KB | structures | c8278ffee32d... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | b1a954c23baf... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 63ca089e9f68... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 41.6 KB | work | 5ee2ef212e8b... |
| _MMPBSA_ligand.pdb | PDB | 2.8 KB | structures | 5982dc0de733... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | f32807642feb... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | fa6f0181f775... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | f547df61686a... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 36ca9f8f6998... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | 71a1ed4b674b... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 3c0222c7244c... |
| reference.frc | FRC | 126.3 MB | inputs | c54057492d22... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | c4ac5a3544c9... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | bac4647c8df7... |
| _MMPBSA_complex.pdb | PDB | 492.3 KB | structures | d91e88fd14c7... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 8347ff84b358... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | a20ee4a4f4a3... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.9 KB | structures | 290ad25c2104... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.3 KB | structures | b84cd35adedd... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | 5ea958b77d39... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 15bdf4bb8c88... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 41.6 KB | work | ab009a543cec... |
| _MMPBSA_ligand.pdb | PDB | 2.8 KB | structures | eb11951afda7... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | df67c80635df... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | c447554c690f... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | 2f58035a70ab... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | f172af733008... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | dd6a40232afd... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 3f0f901dacfe... |
| reference.frc | FRC | 125.7 MB | inputs | 7d8678138c64... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | aa7ead2d57be... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | 24f5fdbc2b9a... |
| _MMPBSA_complex.pdb | PDB | 492.3 KB | structures | a526710f7332... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 8dbc9792d22a... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 8f6a3d30bafe... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.9 KB | structures | ddaed80a560d... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.3 KB | structures | c8278ffee32d... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | b1a954c23baf... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 1b30c288eb1d... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 41.6 KB | work | 5ee2ef212e8b... |
| _MMPBSA_ligand.pdb | PDB | 2.8 KB | structures | 5982dc0de733... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 26869b1d1d24... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | fa6f0181f775... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | f547df61686a... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 36ca9f8f6998... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | 0e0e42471430... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 3c0222c7244c... |
| reference.frc | FRC | 125.7 MB | inputs | 53c8cd0fc708... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 85e56ae0366f... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | bac4647c8df7... |
| _MMPBSA_complex.pdb | PDB | 492.3 KB | structures | d91e88fd14c7... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 6d05fb4fd7ab... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | a20ee4a4f4a3... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 221.9 KB | structures | 290ad25c2104... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.3 KB | structures | b84cd35adedd... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | 5ea958b77d39... |
| _MMPBSA_info | not recorded | 4.1 KB | work | d74965a5e3db... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 41.6 KB | work | ab009a543cec... |
| _MMPBSA_ligand.pdb | PDB | 2.8 KB | structures | eb11951afda7... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 5c3cf5129fc5... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | c447554c690f... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | 2f58035a70ab... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | f172af733008... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | f35190628f8a... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 3f0f901dacfe... |
| reference.frc | FRC | 125.7 MB | inputs | 9b3fe8fedd03... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | a257cbc6c5a9... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | 35ff1947ccbe... |
| _MMPBSA_complex.pdb | PDB | 492.5 KB | structures | f14d2a3a1da6... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 2b46280ac996... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 09d1ae24e5b9... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 222.0 KB | structures | 603902550d03... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.4 KB | structures | 53eff164eb7e... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | 77b8c5585d22... |
| _MMPBSA_info | not recorded | 4.1 KB | work | ed468d9cc22b... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 44.0 KB | work | 4b7e1ffc31c4... |
| _MMPBSA_ligand.pdb | PDB | 3.0 KB | structures | 132385168910... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 32b8932ba71b... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | f9bf7a1b9a08... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | 999de87bd52d... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | a3c334c54de0... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | 35cb781a29b5... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 5ed3d55ee441... |
| reference.frc | FRC | 126.4 MB | inputs | 607e2b296a33... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | ca7f8474662d... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | 2e7881e63311... |
| _MMPBSA_complex.pdb | PDB | 492.5 KB | structures | 90a1c9e250f0... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 2faca8ffe817... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 66300af9662a... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 222.0 KB | structures | e4a109a0b90e... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.4 KB | structures | 3cfd197c06be... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | 99cee5debeda... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 91429f3cd832... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 44.0 KB | work | 5d91baf37793... |
| _MMPBSA_ligand.pdb | PDB | 3.0 KB | structures | 2863d1d33502... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | aeb8fa4c5c3a... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | ec83e6f03918... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | 40dc2b01632a... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | fd95298c3b12... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | 91d74cc7ad0e... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 87600afe4472... |
| reference.frc | FRC | 126.4 MB | inputs | 36bff5a55077... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 3ca33af2ca21... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | e6c7f0f9be7e... |
| _MMPBSA_complex.pdb | PDB | 492.5 KB | structures | 5775f110a2ca... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 259a0b5e24fa... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 7cdeb5940f88... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 222.0 KB | structures | 4a5d3c435fcd... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.4 KB | structures | 2d2136af5bac... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | b45b2a1697db... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 84df9d875553... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 44.0 KB | work | 66328829b3f3... |
| _MMPBSA_ligand.pdb | PDB | 3.0 KB | structures | 64e479e2e292... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 79684294df6b... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | d02e97ad0dce... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | 28133c90017f... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 100f5a2d6675... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | 9e13188ed98d... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 2b44ac0b1d55... |
| reference.frc | FRC | 125.7 MB | inputs | ec1c56f8ff4a... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 4426c40cc148... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | 009e04244e24... |
| _MMPBSA_complex.pdb | PDB | 492.5 KB | structures | e9014e8a5201... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | fd8df11601b8... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 27f675a97aa0... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 222.0 KB | structures | 21fd6a3a6ee4... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.4 KB | structures | 29871fdc5c05... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | 064b24268bde... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 0ce54c8c0a15... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 44.0 KB | work | 63eb3b6e1497... |
| _MMPBSA_ligand.pdb | PDB | 3.0 KB | structures | fa1346dd1abc... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | e79fb7838ed3... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | b5473747463c... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | a2b2af43380f... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 5072536f8b20... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | f23220cba8e9... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 06b6815c42fb... |
| reference.frc | FRC | 125.7 MB | inputs | 3b660a804c49... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | c308add0f706... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | b22b32a7b386... |
| _MMPBSA_complex.pdb | PDB | 492.5 KB | structures | f3c895195928... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 62367d78b235... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 0a56f2b379de... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 222.0 KB | structures | 56d1fb61e79c... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.4 KB | structures | 96b652d1d106... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | e0901d63c5ab... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 451f0e691cc5... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 44.0 KB | work | bb6f48b530e5... |
| _MMPBSA_ligand.pdb | PDB | 3.0 KB | structures | a44647a6c882... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 89578fafd44a... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | 8177bbebcf50... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | 22d7ec1d596f... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 83d3141e8a04... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | 494edbc8c926... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | 456744910b26... |
| reference.frc | FRC | 125.7 MB | inputs | bd7b996102ed... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 8d738788760f... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | 98bf386f3683... |
| _MMPBSA_complex.pdb | PDB | 492.5 KB | structures | 268eabbcebfa... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | 83b7a85a057d... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 22bf40d666d4... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 222.0 KB | structures | 20baa603a22e... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.4 KB | structures | a3a2b8b22b7c... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | c86a2ed42352... |
| _MMPBSA_info | not recorded | 4.1 KB | work | ca080bb42e1a... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 44.0 KB | work | 2b658b758a03... |
| _MMPBSA_ligand.pdb | PDB | 3.0 KB | structures | e572b6b3dcce... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 9c8761fcfd82... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | 5bc8f8bc9d77... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | cf3f0fd842f2... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 0686b4e0d15d... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | 59796fbaac30... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | af7b11ac7249... |
| reference.frc | FRC | 125.7 MB | inputs | 627b98d16e71... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | d21a255f5a80... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | a056656cac4a... |
| _MMPBSA_complex.pdb | PDB | 492.6 KB | structures | 0d17e185d31d... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | eb244e084960... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | bd54092654e5... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 222.1 KB | structures | c1afd9f1b521... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.5 KB | structures | 829c534096e7... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | 2b56bc106f72... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 0d5a8ad768e8... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 46.4 KB | work | f4dd29c9e937... |
| _MMPBSA_ligand.pdb | PDB | 3.1 KB | structures | 10b221cd80d7... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 0eccae06810a... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | 6ceecad87498... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | a41eaffcd10e... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | 4d1b17ea1d68... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | 62ebc2032e7b... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | bf0225451dbf... |
| reference.frc | FRC | 125.7 MB | inputs | f715df15ad8c... |
| FINAL_RESULTS_MMPBSA.dat | DAT | 4.3 KB | work | 05d3fd1d2ef4... |
| _MMPBSA_complex.mdcrd.0 | 0 | 7.2 MB | work | 55a8e5ed00cb... |
| _MMPBSA_complex.pdb | PDB | 492.6 KB | structures | 309d1e7a5908... |
| _MMPBSA_complex_gb.mdout.0 | 0 | 56.9 KB | work | ab5c0c737d55... |
| _MMPBSA_complex_gb_surf.dat.0 | 0 | 1.1 KB | work | 4af51bca9081... |
| _MMPBSA_dummycomplex.inpcrd | INPCRD | 222.1 KB | structures | 5e9d0b50005d... |
| _MMPBSA_dummyligand.inpcrd | INPCRD | 1.5 KB | structures | 71a06992075e... |
| _MMPBSA_dummyreceptor.inpcrd | INPCRD | 220.7 KB | structures | aaa50757824c... |
| _MMPBSA_info | not recorded | 4.1 KB | work | 2ddab07375b7... |
| _MMPBSA_ligand.mdcrd.0 | 0 | 46.4 KB | work | d26b68f5b38e... |
| _MMPBSA_ligand.pdb | PDB | 3.1 KB | structures | a39d2070c8c0... |
| _MMPBSA_ligand_gb.mdout.0 | 0 | 56.8 KB | work | 093547c16a9e... |
| _MMPBSA_ligand_gb_surf.dat.0 | 0 | 1.1 KB | work | c7d19db59308... |
| _MMPBSA_receptor.mdcrd.0 | 0 | 7.2 MB | work | 0d22e377c20f... |
| _MMPBSA_receptor.pdb | PDB | 489.5 KB | structures | b78419b7142f... |
| _MMPBSA_receptor_gb.mdout.0 | 0 | 56.9 KB | work | fa33f1829a36... |
| _MMPBSA_receptor_gb_surf.dat.0 | 0 | 1.1 KB | work | e4ad99cb7308... |
| reference.frc | FRC | 125.7 MB | inputs | f44082530d54... |
| mmgbsa_results.json | JSON | 3.8 KB | work | f058989b91c8... |
| mmpbsa_run.log | LOG | 55.4 KB | work | c1d566edd7aa... |
| 096_parse_mmpbsa.py | PY | 1.6 KB | 01_task_2/source | 2a068df0a5bb... |
| mmgbsa_results.json | JSON | 12.2 KB | 01_task_2/work | 6e857c332d56... |
| 097_path.py | PY | 1.8 KB | 01_task_2/source | 41db51ee69b1... |
| combined_results.json | JSON | 7.5 KB | 01_task_2/work | b445d1a13ab7... |
| 098_path.py | PY | 1.7 KB | 01_task_2/source | 374d392e3204... |
| 099_open.py | PY | 357 B | 01_task_2/source | 90eaa72aed23... |
| combined_results.json | JSON | 7.5 KB | 01_task_2/work | a7a8b3a771d9... |
| 100_path.py | PY | 1.7 KB | 01_task_2/source | 59917acfca31... |
| phase5_mmgbsa_free_binding_energies.md | MD | 6.3 KB | 01_task_2/reports | 5f4d1f5dd3f5... |

## Verification

- 3 tool call(s) ran in this phase, 0 of which reported a failure.
- 362 file(s) were produced and registered, 362 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

This phase recorded no external tools or databases.
