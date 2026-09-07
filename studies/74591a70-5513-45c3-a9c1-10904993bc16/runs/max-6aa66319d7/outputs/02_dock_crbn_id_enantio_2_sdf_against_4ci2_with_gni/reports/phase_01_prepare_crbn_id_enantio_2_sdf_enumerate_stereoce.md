---
title: "Phase 1: Prepare CRBN_ID_enantio_2.sdf: enumerate stereocenters and generate 3D conformers"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-6aa66319d7"
phase_index: 1
phase_id: "1"
phase_goal: "Prepare CRBN_ID_enantio_2.sdf: enumerate stereocenters and generate 3D conformers"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Prepare CRBN_ID_enantio_2.sdf: enumerate stereocenters and generate 3D conformers

## Summary

This phase set out to prepare CRBN_ID_enantio_2.sdf: enumerate stereocenters and generate 3D conformers. It completed 3 method steps, 39 output files.

## Objective

Prepare CRBN_ID_enantio_2.sdf: enumerate stereocenters and generate 3D conformers

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

## Verification

- 3 tool call(s) ran in this phase, 0 of which reported a failure.
- 39 file(s) were produced and registered, 39 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

This phase recorded no external tools or databases.
