---
title: "Phase 2: Submit Amber MD + MM-GBSA to LUMI CPU partition"
study_id: "7a39e116-e0d5-4e70-93c3-da6df54e7e1e"
run_id: "max-2b162eedac"
phase_index: 2
phase_id: "2"
phase_goal: "Submit Amber MD + MM-GBSA to LUMI CPU partition"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 2: Submit Amber MD + MM-GBSA to LUMI CPU partition

## Summary

This phase set out to submit Amber MD + MM-GBSA to LUMI CPU partition. It completed 1 method step, 21 output files.

## Objective

Submit Amber MD + MM-GBSA to LUMI CPU partition

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
| 081_print.py | PY | 448 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 6252691c2e96... |
| EL2003A_pose2.mol | MOL | 3.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 047cffee600f... |
| config.ini | INI | 255 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | b0249500951f... |
| 082_print.py | PY | 1.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 53bead50bb20... |
| EL2003A_pose2.mol | MOL | 3.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | a6430a7506e3... |
| complex.pdb | PDB | 365.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | c7cc3ceb530d... |
| complex.top | TOP | 2.3 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | 03a966f80fb1... |
| complex_reres.pdb | PDB | 365.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 518c51d3b209... |
| traj_com.xtc | XTC | 1.7 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | 3a92c74b225f... |
| config.ini | INI | 255 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | adce986a5ab3... |
| 083_print.py | PY | 1018 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | e429577ea703... |
| EL2003A_pose2.mol | MOL | 3.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | f829f01e122d... |
| complex.pdb | PDB | 365.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 481117b32262... |
| complex.top | TOP | 2.3 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | beeb83361d70... |
| complex_reres.pdb | PDB | 365.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 08d12eb4ab90... |
| traj_com.xtc | XTC | 1.7 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | a68c1a7276e3... |
| 084_print.py | PY | 1.0 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | fd5c0698cbf5... |
| 085_os_path_getsize.py | PY | 732 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 0106711ed396... |
| cpu_test.txt | TXT | 5 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/reports | d117fa006ba9... |
| slurm-21798812.log | LOG | 27 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | 8277b426b81d... |
| slurm-21798843.log | LOG | 17.9 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | cbe176a13dd3... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 21 file(s) were produced and registered, 21 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/gbsa:latest`

## Limitations

- No citation is on record for gbsa, so the versions used cannot be traced to a publication.
- Versions were not recorded for gbsa. A methods section without a version is not reproducible.

## References

**No citation on record:** gbsa.

These were used by this phase and are reported for completeness. A citation should be supplied before this material is used in a manuscript. They are listed rather than omitted because a methods section that hides a dependency is not reproducible.
