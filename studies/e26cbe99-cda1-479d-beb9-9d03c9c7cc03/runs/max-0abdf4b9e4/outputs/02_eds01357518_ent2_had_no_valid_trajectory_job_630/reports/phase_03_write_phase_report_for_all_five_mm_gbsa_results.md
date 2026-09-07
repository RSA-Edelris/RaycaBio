---
title: "Phase 3: Write phase report for all five MM-GBSA results"
study_id: "e26cbe99-cda1-479d-beb9-9d03c9c7cc03"
run_id: "max-4728b51b97"
phase_index: 3
phase_id: "3"
phase_goal: "Write phase report for all five MM-GBSA results"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 3: Write phase report for all five MM-GBSA results

## Summary

This phase set out to write phase report for all five MM-GBSA results. It completed 1 method step, 13 output files.

## Objective

Write phase report for all five MM-GBSA results

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

#### 1. Molecular dynamics simulation of protein-ligand complexes

Energy minimisation, NPT equilibration, and NPT production MD simulations were performed on two protein-ligand complexes (CRBN-EDS01357518_ent2 and CRBN-EDS01806218_ent1) using GROMACS 2026.1-mpi with GPU acceleration.

**Rationale.** MD simulation allows characterisation of the dynamic behaviour and stability of protein-ligand complexes at physiological conditions.

| Field | Value |
| :--- | :--- |
| Inputs | em.mdp, npt_eq.mdp, prod.mdp, complex.gro, complex.top, index.ndx |
| Outputs | em.gro, npt_eq.gro, npt_prod.gro, npt_prod.xtc, npt_prod.edr |
| Status | running |

Parameters:

```yaml
nonbonded_scheme: gpu
omp_threads: 8
pme_scheme_em: cpu
pme_scheme_equilibration: gpu
pme_scheme_production: gpu
```

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| cpptraj_strip.in | IN | 377 B | 01_strip_and_run_mm_gbsa_for_eds01806218_ent1/work | 5bcdc0c0d26e... |
| cpptraj_strip.in | IN | 386 B | 01_strip_and_run_mm_gbsa_for_eds01806218_ent1/work | ed6988348395... |
| prod_nowater.nc | NC | 26.7 MB | 01_strip_and_run_mm_gbsa_for_eds01806218_ent1/work | 825c6ff742e5... |
| 118_compounds_items.py | PY | 1.5 KB | 01_strip_and_run_mm_gbsa_for_eds01806218_ent1/source | 2903bd3ede20... |
| 119_open.py | PY | 440 B | 01_strip_and_run_mm_gbsa_for_eds01806218_ent1/source | d7abca29b0fa... |
| 120_root.py | PY | 833 B | 01_strip_and_run_mm_gbsa_for_eds01806218_ent1/source | d0a810e1c6ad... |
| mmpbsa_results.dat | DAT | 5.9 KB | 01_strip_and_run_mm_gbsa_for_eds01806218_ent1/work | 4382244ecde0... |
| reference.frc | FRC | 94.9 MB | 01_strip_and_run_mm_gbsa_for_eds01806218_ent1/inputs | e581d8bbe9c5... |
| 121_os_environ_copy.py | PY | 864 B | 01_strip_and_run_mm_gbsa_for_eds01806218_ent1/source | 41005f8a58d3... |
| 122_open.py | PY | 612 B | 01_strip_and_run_mm_gbsa_for_eds01806218_ent1/source | f135ccd4c847... |
| phase_01_strip_and_run_mm_gbsa_for_eds01806218_ent1.md | MD | 3.5 KB | 02_strip_and_run_mm_gbsa_for_eds01357518_ent2/reports | 4d785590739c... |
| phase_mmgbsa_EDS01806218_ent1.md | MD | 5.6 KB | 02_eds01357518_ent2_had_no_valid_trajectory_job_630/reports | 7e78034c17a6... |
| slurm-6321629.log | LOG | 120 B | 02_eds01357518_ent2_had_no_valid_trajectory_job_630/work | 962702151a70... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 13 file(s) were produced and registered, 13 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

This phase recorded no external tools or databases.
