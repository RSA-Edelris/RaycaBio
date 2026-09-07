---
title: "Phase 1: Run MM-GBSA analysis on EDS01806218_ent2 10 ns MD trajectory"
study_id: "e26cbe99-cda1-479d-beb9-9d03c9c7cc03"
run_id: "max-ae6ca6b486"
phase_index: 1
phase_id: "1"
phase_goal: "Run MM-GBSA analysis on EDS01806218_ent2 10 ns MD trajectory"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Run MM-GBSA analysis on EDS01806218_ent2 10 ns MD trajectory

## Summary

This phase set out to run MM-GBSA analysis on EDS01806218_ent2 10 ns MD trajectory. It completed 18 output files.

## Objective

Run MM-GBSA analysis on EDS01806218_ent2 10 ns MD trajectory

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
| em.gro | GRO | 1.3 MB | structures | 7af41fb61d56... |
| npt_eq.gro | GRO | 1.9 MB | structures | 3826d9fd6c73... |
| npt_prod.edr | EDR | 669.5 KB | work | 89c084828ecf... |
| npt_prod.gro | GRO | 1.9 MB | structures | 289f2e51bbc4... |
| npt_prod.xtc | XTC | 102.3 MB | work | 95628fef49cd... |
| slurm-6294174.log | LOG | 2.8 MB | work | 8d92d29e0576... |
| cpptraj_strip.in | IN | 420 B | work | 0b0e51e847b1... |
| prod_nowater.nc | NC | 26.7 MB | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/work | e90cca3b58e1... |
| 104_print.py | PY | 720 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | 6179dd88c1b2... |
| 105_print.py | PY | 773 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | 239818b07110... |
| mmpbsa.in | IN | 200 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/work | b3fad6177065... |
| _MMPBSA_gb.mdin | MDIN | 72 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/work | 272627c4eb0a... |
| 106_print.py | PY | 699 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | 20ac7d785867... |
| mmpbsa_results.dat | DAT | 5.9 KB | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/work | 181f2b38a1d5... |
| reference.frc | FRC | 94.9 MB | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/inputs | cbb6dd1c817a... |
| 107_print.py | PY | 672 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | 0bde05cdc998... |
| 108_open.py | PY | 66 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | e080aebe768f... |
| 109_open.py | PY | 566 B | 01_run_mm_gbsa_analysis_on_eds01806218_ent2_10_ns_m/source | 6401886d60e2... |

## Verification

- No tool call is on record for this phase.
- 18 file(s) were produced and registered, 18 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
