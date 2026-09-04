---
title: "Phase 1: Retrosynthetic analysis — MCUF651, A317, 7977"
study_id: "8309667e-a164-44d9-ac9b-ce1096db0a98"
run_id: "max-39390f1cf2"
phase_index: 1
phase_id: "1"
phase_goal: "Retrosynthetic analysis — MCUF651, A317, 7977"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Retrosynthetic analysis — MCUF651, A317, 7977

## Summary

This phase set out to retrosynthetic analysis — MCUF651, A317, 7977. It completed 18 output files.

## Objective

Retrosynthetic analysis — MCUF651, A317, 7977

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

No method records were captured for this phase, so the procedure cannot be stated. This is a gap in the record, not a phase that did no work.
## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| 001_chem_sdmolsupplier.py | PY | 836 B | 01_retrosynthetic_analysis_mcuf651_a317_7977/source | 71e5fa5d4603... |
| aizyn_results.json | JSON | 269.8 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/work | d4fedf22b3d6... |
| aizynthfinder-results-2.json | JSON | 81.5 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/results | 57d01fc47538... |
| aizynthfinder-results-3.json | JSON | 90.7 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/results | 05a52e8d1625... |
| aizynthfinder-results.json | JSON | 25.1 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/results | 4bc9a0892dbb... |
| 002_nc2nc3c.py | PY | 1.0 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/source | dd87c50ecb87... |
| 003_inspect_top_level_keys_route_structure_each_result.py | PY | 705 B | 01_retrosynthetic_analysis_mcuf651_a317_7977/source | 9a127768e39e... |
| 004_extract_compact_summary_routes_without_dumping_whole.py | PY | 2.7 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/source | 0c418ea2b583... |
| 005_extract_all_routes.py | PY | 3.7 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/source | ac5c35e2dd06... |
| rsgpt-results-2.json | JSON | 2.9 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/results | ca8f059fc9cc... |
| rsgpt-results-3.json | JSON | 3.0 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/results | 883cb215c5cc... |
| rsgpt-results-4.json | JSON | 2.6 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/results | c0acd630c92a... |
| rsgpt-results-5.json | JSON | 1.5 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/results | 856b06677f58... |
| rsgpt-results-6.json | JSON | 1.9 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/results | 8c696e15e1d2... |
| rsgpt-results-7.json | JSON | 2.8 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/results | 0aabda26499a... |
| rsgpt-results.json | JSON | 2.7 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/results | 07e79ab636a6... |
| rsgpt_results.json | JSON | 21.3 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/work | 84c8dcb2aaa3... |
| 006_nc2nc3c.py | PY | 1.5 KB | 01_retrosynthetic_analysis_mcuf651_a317_7977/source | de251ba4ace2... |

## Verification

- No tool call is on record for this phase.
- 18 file(s) were produced and registered, 18 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/aizynthfinder:latest`
- Container Image: `registry.rayca.org/rayca-tools/rsgpt:latest`

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
