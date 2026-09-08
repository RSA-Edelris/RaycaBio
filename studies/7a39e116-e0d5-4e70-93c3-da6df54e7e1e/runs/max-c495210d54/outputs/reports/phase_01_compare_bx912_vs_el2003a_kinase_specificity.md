---
title: "Phase 1: Compare BX912 vs EL2003A kinase specificity"
study_id: "7a39e116-e0d5-4e70-93c3-da6df54e7e1e"
run_id: "max-7307d91685"
phase_index: 1
phase_id: "1"
phase_goal: "Compare BX912 vs EL2003A kinase specificity"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Compare BX912 vs EL2003A kinase specificity

## Summary

This phase set out to compare BX912 vs EL2003A kinase specificity. It completed 1 method step, 2 output files.

## Objective

Compare BX912 vs EL2003A kinase specificity

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
| 141_bx912_vs_el2003a_per_kinase_delta.py | PY | 468 B | 01_compare_bx912_vs_el2003a_kinase_specificity/source | 8e0b2148b527... |
| 142_open.py | PY | 1.4 KB | 01_compare_bx912_vs_el2003a_kinase_specificity/source | 68ceccf09c92... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 2 file(s) were produced and registered, 2 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No citation is on record for gbsa, so the versions used cannot be traced to a publication.
- Versions were not recorded for gbsa. A methods section without a version is not reproducible.

## References

**No citation on record:** gbsa.

These were used by this phase and are reported for completeness. A citation should be supplied before this material is used in a manuscript. They are listed rather than omitted because a methods section that hides a dependency is not reproducible.
