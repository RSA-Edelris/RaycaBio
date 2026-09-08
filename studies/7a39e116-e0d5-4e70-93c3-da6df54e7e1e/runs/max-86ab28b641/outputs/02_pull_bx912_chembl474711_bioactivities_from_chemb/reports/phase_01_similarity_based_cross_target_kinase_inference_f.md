---
title: "Phase 1: Similarity-based cross-target kinase inference for 6 PDK1 ligands"
study_id: "7a39e116-e0d5-4e70-93c3-da6df54e7e1e"
run_id: "max-d1ca3df0ba"
phase_index: 1
phase_id: "1"
phase_goal: "Similarity-based cross-target kinase inference for 6 PDK1 ligands"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Similarity-based cross-target kinase inference for 6 PDK1 ligands

## Summary

This phase set out to similarity-based cross-target kinase inference for 6 PDK1 ligands. It completed 1 method step, 33 output files.

## Objective

Similarity-based cross-target kinase inference for 6 PDK1 ligands

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
| phase_02_task_a3bc1d448863929a1.md | MD | 3.3 KB | 01_similarity_based_cross_target_kinase_inference_f/reports | 82f6b7e6e971... |
| 147_open.py | PY | 239 B | 01_similarity_based_cross_target_kinase_inference_f/source | 6e120539f6a3... |
| chembl-results-2.json | JSON | 396 B | 01_similarity_based_cross_target_kinase_inference_f/results | 130016ab227e... |
| chembl-results-3.json | JSON | 398 B | 01_similarity_based_cross_target_kinase_inference_f/results | 2b8d6ffbbf6f... |
| chembl-results-4.json | JSON | 412 B | 01_similarity_based_cross_target_kinase_inference_f/results | 8d81c268f03f... |
| chembl-results-5.json | JSON | 372 B | 01_similarity_based_cross_target_kinase_inference_f/results | c67e9575543f... |
| chembl-results-6.json | JSON | 406 B | 01_similarity_based_cross_target_kinase_inference_f/results | f4ab38838d8e... |
| chembl-results.json | JSON | 388 B | 01_similarity_based_cross_target_kinase_inference_f/results | f4d07b436a51... |
| chembl_similarity_hits.pkl | PKL | 96 B | 01_similarity_based_cross_target_kinase_inference_f/work | 94bc107b9cb6... |
| 148_step_1_chembl_similarity_search_all_6_compounds_run.py | PY | 1.4 KB | 01_similarity_based_cross_target_kinase_inference_f/source | b59178f4a6f0... |
| 149_open.py | PY | 517 B | 01_similarity_based_cross_target_kinase_inference_f/source | 434da0d04726... |
| 150_step_1_find_bx912_chembl_pull_all_kinase.py | PY | 1.6 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | 9e3ff033828a... |
| 151_chembl_get.py | PY | 1.0 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | fed23e91e710... |
| 152_step_2_pull_all_similarity_hits_all_6_compounds.py | PY | 2.4 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | 0afee514c659... |
| similarity_hits.pkl | PKL | 6.5 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/work | 991bf217d384... |
| 153_chembl_get_all_pages.py | PY | 2.2 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | 06e6b49b4c2c... |
| chembl_activities_raw.parquet | PARQUET | 636 B | 01_chembl_container_tool_uses_a_38_compound_baked_s/inputs | 8b67fb02ed63... |
| 154_chembl_activities_batch.py | PY | 2.0 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | 61862712bf31... |
| 155_chembl3916849.py | PY | 1.3 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | e636c04755aa... |
| chembl_activities_raw.parquet | PARQUET | 116.1 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/inputs | 5ab53a5c8e48... |
| 156_pull_activities_batch.py | PY | 1.7 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | 22504ea8ee2a... |
| 157_pd_read_parquet.py | PY | 2.8 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | d5ffeeb25810... |
| 158_pd_read_parquet.py | PY | 1.3 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | 9bfe55430a7b... |
| 159_pd_read_parquet.py | PY | 2.7 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | a8f4e934633f... |
| tanimoto_inference_results.pkl | PKL | 7.4 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/work | edde987ecb39... |
| 160_chembl_get.py | PY | 1.6 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | 83fd8efcfe7d... |
| 161_chembl_get_all.py | PY | 2.2 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | e7400130a07b... |
| 162_open.py | PY | 4.0 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | 1eab3e766799... |
| similarity_inference_matrix.csv | CSV | 322 B | 01_chembl_container_tool_uses_a_38_compound_baked_s/tables | 06b33f0ce88b... |
| 163_matplotlib_use.py | PY | 3.6 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | fe340da5f191... |
| bx912_docking_vs_inference_vs_exp.png | PNG | 48.6 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/figures | 34e3fa8be157... |
| similarity_inference_heatmap.png | PNG | 106.8 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/figures | fa3c215fac07... |
| 164_matplotlib_use.py | PY | 4.5 KB | 01_chembl_container_tool_uses_a_38_compound_baked_s/source | 163676d9df48... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 33 file(s) were produced and registered, 33 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/chembl:latest`

## Limitations

- No citation is on record for gbsa, so the versions used cannot be traced to a publication.
- Versions were not recorded for gbsa. A methods section without a version is not reproducible.

## References

**No citation on record:** gbsa.

These were used by this phase and are reported for completeness. A citation should be supplied before this material is used in a manuscript. They are listed rather than omitted because a methods section that hides a dependency is not reproducible.
