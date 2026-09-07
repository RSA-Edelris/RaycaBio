---
title: "Phase 1: Convert MM-GBSA ΔG to apparent Ki and report IC50 context"
study_id: "e26cbe99-cda1-479d-beb9-9d03c9c7cc03"
run_id: "max-c2150b873b"
phase_index: 1
phase_id: "1"
phase_goal: "Convert MM-GBSA ΔG to apparent Ki and report IC50 context"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Convert MM-GBSA ΔG to apparent Ki and report IC50 context

## Summary

This phase set out to convert MM-GBSA ΔG to apparent Ki and report IC50 context. It completed 1 method step, 1 output file.

## Objective

Convert MM-GBSA ΔG to apparent Ki and report IC50 context

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
| 123_print.py | PY | 1.6 KB | 01_convert_mm_gbsa_g_to_apparent_ki_and_report_ic50/source | eb5e8eb2bb2f... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 1 file(s) were produced and registered, 1 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

This phase recorded no external tools or databases.
