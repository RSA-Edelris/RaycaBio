---
title: "Phase 3: task ac481d76baf4e5e3c"
study_id: "7a39e116-e0d5-4e70-93c3-da6df54e7e1e"
run_id: "max-e29a3d15c1"
phase_index: 3
phase_id: "ac481d76baf4e5e3c"
phase_goal: "task ac481d76baf4e5e3c"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 3: task ac481d76baf4e5e3c

## Summary

This phase set out to task ac481d76baf4e5e3c. It completed 1 method step, 29 output files.

## Objective

task ac481d76baf4e5e3c

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
| phase_03_task_a285dd498619c3c0c.md | MD | 5.8 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/reports | 6c646fb857c2... |
| 086_check_available_libraries_mm_gbsa_post_processing.py | PY | 390 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | de46fa662de6... |
| receptor_pH74_noH.pdb | PDB | 184.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 76a2981921f9... |
| 087_step_1_strip_all_h_atoms_receptor_fixes_hie_hd1.py | PY | 1.6 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 4aa2ddf3dad5... |
| 089_estimate_receptor_3d_extent_predict_simulation_box.py | PY | 1.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | ec3296260f96... |
| openfe_result.json | JSON | 6.8 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | 64a086426fd6... |
| 090_print.py | PY | 1.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 159740a47c2a... |
| EL2003A_pose2_3D.sdf | SDF | 3.1 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | fbb0d876a7b3... |
| 091_read_pose_sdf_preserving_all_h_atoms_3d_coords.py | PY | 1.4 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 5c0397b24d1b... |
| easymd_result2.json | JSON | 656 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | 1e09f2a1cfed... |
| 092_print.py | PY | 1.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | f06ad2b9d46d... |
| 093_check_what_s_available.py | PY | 801 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 600b351b7e5e... |
| 094_check_parmed_mdtraj_openmm.py | PY | 651 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | e2bf1fedfb14... |
| 095_subprocess_run.py | PY | 1.0 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 24267574ae76... |
| 096_structure.py | PY | 791 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | c4d45263db42... |
| 097_parmed_already_successfully_imported_grab_cached.py | PY | 1.0 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 1d6bc06f6ef2... |
| mmgbsa_calc.py | PY | 6.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | ff4ed6039155... |
| 098_run_mm_gbsa_script_subprocess_avoids_sandbox_code_py.py | PY | 743 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 435ea0c06ff4... |
| 099_find_all_python_executables_check_which_has_mdtraj.py | PY | 641 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 4a16869bb2e5... |
| complex.prmtop | PRMTOP | 3.4 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 30da94c6f099... |
| ligand.prmtop | PRMTOP | 25.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 5809a4300f94... |
| receptor.prmtop | PRMTOP | 3.3 MB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/structures | 466ac1c8f7cc... |
| 100_print.py | PY | 655 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 63eb072acc15... |
| mmgbsa_calc.py | PY | 6.5 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | cc00fceba596... |
| mmgbsa_result.json | JSON | 20.9 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/work | e7d32b40444e... |
| 101_print.py | PY | 623 B | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 01935d88d9f7... |
| 102_load_results.py | PY | 1.4 KB | 01_md_refinement_of_el2003a_best_docking_pose_pose_/source | 32c8fe9b148d... |
| phase_01_md_refinement_of_el2003a_best_docking_pose_pose_.md | MD | 6.8 KB | 02_submit_amber_md_mm_gbsa_to_lumi_cpu_partition/reports | 0b85916e9507... |
| audit_mmgbsa_md_refinement_EL2003A_pose2.md | MD | 13.5 KB | 02_submit_amber_md_mm_gbsa_to_lumi_cpu_partition/reports | d836a30a3600... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 29 file(s) were produced and registered, 29 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/easy-md:latest`
- Container Image: `registry.rayca.org/rayca-tools/openfe:latest`

## Limitations

- No citation is on record for gbsa, so the versions used cannot be traced to a publication.
- Versions were not recorded for gbsa. A methods section without a version is not reproducible.

## References

**No citation on record:** gbsa.

These were used by this phase and are reported for completeness. A citation should be supplied before this material is used in a manuscript. They are listed rather than omitted because a methods section that hides a dependency is not reproducible.
