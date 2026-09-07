---
title: "Phase 1: Create annotated SDF and push session to GitHub"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-2e9ef516f5"
phase_index: 1
phase_id: "1"
phase_goal: "Create annotated SDF and push session to GitHub"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Create annotated SDF and push session to GitHub

## Summary

This phase set out to create annotated SDF and push session to GitHub. It completed 3 method steps, 2 output files.

## Objective

Create annotated SDF and push session to GitHub

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
| CRBN_32_ligands_docking_GBSA.sdf | SDF | 119.6 KB | 01_create_annotated_sdf_and_push_session_to_github/structures | 51b07a71be70... |
| 101_open.py | PY | 1.8 KB | 01_create_annotated_sdf_and_push_session_to_github/source | c45def01569b... |

## Verification

- 3 tool call(s) ran in this phase, 0 of which reported a failure.
- 2 file(s) were produced and registered, 2 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

This phase recorded no external tools or databases.
