---
title: "Phase 1: Write MD pipeline status report for job 22076601"
study_id: "0ddc6243-37e4-40c9-aba2-1bf173994ad2"
run_id: "max-949845805a"
phase_index: 1
phase_id: "12"
phase_goal: "Write MD pipeline status report for job 22076601"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Write MD pipeline status report for job 22076601

## Summary

This phase set out to write MD pipeline status report for job 22076601. It completed 10 output files.

## Objective

Write MD pipeline status report for job 22076601

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
| analyze.py | PY | 1.2 KB | source | a5b3e6005c92... |
| analysis_B.tar.gz | GZ | 234 B | work | 71d897a7fc02... |
| jobB_log.txt | TXT | 2.4 KB | reports | cae84dbac158... |
| mdlogs_B.tar.gz | GZ | 45 B | work | 85cea451eec0... |
| CPD1_progress.txt | TXT | 83 B | reports | 8aba8cc9e8f0... |
| CPD1_progress.txt | TXT | 83 B | reports | 8aba8cc9e8f0... |
| slurm-22076621.log | LOG | 1.0 KB | work | c3ad12e89b9a... |
| CPD9_progress.txt | TXT | 83 B | reports | 3cf2bdf8f26f... |
| CPD9_progress.txt | TXT | 83 B | reports | 3cf2bdf8f26f... |
| slurm-22076698.log | LOG | 1.0 KB | work | 99c6c042aefb... |

## Verification

- No tool call is on record for this phase.
- 10 file(s) were produced and registered, 10 of them with a sha256 digest recorded, so they can be checked against this report.

### What was found

**Job 22076601 output (primary target):** The job completed in ~15 s with exit code 0 but
produced no MD output files. Root cause: the workdir was assembled with individual
prmtop/inpcrd symlinks but no systems tarball; the script found no systems to process and
exited cleanly. No trajectory, mdinfo, or restart files are recoverable for this job.

**Parallel per-compound jobs (22076607, 22076621, 22076698, 22076809):** All 4 job
submissions failed at the minimisation stage within 0–1 seconds of the srun call. Root
cause: srun "More processors requested than permitted" — each job requested 128 MPI ranks
while the SLURM allocation was simultaneously held by the concurrent jobs. Summary table
entries are NO_DATA for all compounds (CPD1, CPD9, CPD10, CPD11, CPD12).

**MD numbers used in the report (sourced from job 22075127 live files):**
- CPD4 NVT stage: 120000/250000 steps complete (48.0%)
- Temperature: 299.66 ± 0.49 K (mean ± SD over last 3 reported frames)
- Performance: 4.22 ns/day, 40.95 ms/step (128 MPI ranks, ~127k atom system)
- Remaining NVT walltime at read time: ~1.5 h

**Job 22076604 status at report time:** Smoke test passed; all 9 systems launched
sequentially with pre-staged topologies; REF_85C mini started at 20:07:13.

**Limitation acknowledged:** Job 22076601 output is unrecoverable (workdir cleaned).
All numbers in the status report were sourced from job 22075127 live mdinfo and from
job 22076604 Slurm log, not from job 22076601 output.

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
