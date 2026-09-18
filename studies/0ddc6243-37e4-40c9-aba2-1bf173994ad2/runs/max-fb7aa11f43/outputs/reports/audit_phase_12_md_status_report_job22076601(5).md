---
title: "Audit: Phase 12 — Write MD pipeline status report for job 22076601"
study_id: "0ddc6243-37e4-40c9-aba2-1bf173994ad2"
run_id: "max-949845805a"
phase_id: "12"
audit_date: "2026-09-15"
auditor: "claude-sonnet-4-6"
---

# Audit: Phase 12 — Write MD pipeline status report for job 22076601

## Phase goal

Write an MD pipeline status report answering the question: what did LUMI job 22076601
return and what is the current state of the MD pipeline across all 9 ternary systems?

## Inputs examined

| Source | Content | Recoverable? |
| :--- | :--- | :--- |
| LUMI job 22076601 output | None — workdir cleaned, no files staged | No |
| LUMI job 22075127 live mdinfo | CPD4 NVT step 120000/250000, T=299.89 K | Yes |
| LUMI job 22075127 nvt.out | Last 3 frames: T=300.02, 299.08, 299.89 K | Yes |
| LUMI job 22076604 Slurm log | 9-system sequential run launched, REF_85C mini at 20:07:13 | Yes |
| Parallel compound logs (22076607/621/698/809) | All mini FAILED exit 1, srun over-allocation | Yes |

## Key findings reported

### CPD4 NVT (only compound with running MD at report time)

| Metric | Value | Source |
| :--- | :--- | :--- |
| Steps completed | 120000 / 250000 (48.0%) | mdinfo NSTEP field |
| Simulation time | 240.000 ps | mdinfo TIME field |
| Temperature (last frame) | 299.89 K | mdinfo TEMP field |
| Temperature mean ± SD | 299.66 ± 0.51 K | sample SD from 3 frames (300.02, 299.08, 299.89 K) |
| Total energy | −300189.92 kcal/mol | mdinfo Etot |
| Potential energy | −375461.10 kcal/mol | mdinfo EPtot |
| Restraint energy | 1186.70 kcal/mol | mdinfo RESTRAINT |
| Performance | 4.22 ns/day | mdinfo ns/day field |
| Step time | 40.95 ms/step (20474 s/ns) | mdinfo ns/day field (86400÷4.22); stated mdinfo value 20068 was a transcription error |
| ETA to NVT completion | ~1.5 h from read time | mdinfo estimate |

### Pipeline completeness at report time

| System | Parameterised | Mini | NVT | NPT | Prod |
| :--- | :--- | :--- | :--- | :--- | :--- |
| REF_85C | Yes (staged) | Started 20:07:13 in job 22076604 | — | — | — |
| CPD1 | Yes (staged) | FAILED (job 22076621, srun) | — | — | — |
| CPD4 | Yes (job 22075127) | Done | 48% complete | — | — |
| CPD7 | Yes (job 22075127) | Done (tleap only, no MD) | — | — | — |
| CPD8 | Yes (staged) | — | — | — | — |
| CPD9 | Yes (staged) | FAILED (job 22076698, srun) | — | — | — |
| CPD10 | Yes (job 22075127) | FAILED (job 22076607, srun) | — | — | — |
| CPD11 | Yes (staged) | FAILED (job 22076607, srun) | — | — | — |
| CPD12 | Yes (staged) | FAILED (job 22076809, srun) | — | — | — |

### Performance bottleneck

Full 7.5 ns/compound pipeline at 4.22 ns/day = 42.7 h/compound (7.5÷4.22×24 = 42.654 h).
With a 48 h LUMI `small` partition walltime, only 1 compound completes per job submission.
Note: the 4.22 ns/day figure is a single mid-NVT snapshot for CPD4; it should be treated
as an order-of-magnitude bound until measurements from multiple stages and systems are
available.

## Root cause: job 22076601 produced no output

Job 22076601 ran for ~15 s and exited 0. The workdir contained individual prmtop/inpcrd
symlinks but no systems tarball. The job script expected a tarball to extract into
`$RAYCA_OUT/md_runs/`; finding no tarball it found no systems and exited cleanly without
writing any output files. The workdir was subsequently cleaned and cannot be recovered.

This root cause was identified by examining job 22076601's Slurm log and the job script
structure, then confirmed by comparing against the successful job 22076604 which used a
properly assembled tarball.

## Limitations

1. **Job 22076601 output unrecoverable.** All MD numbers in the status report were
   sourced from the live job 22075127 mdinfo and from the job 22076604 Slurm log.
   This is acknowledged in the report and in the phase Verification section.

2. **Temperature mean computed from 3 frames only.** The SD of 0.51 K (sample SD from
   frames at 300.02, 299.08, 299.89 K) is indicative but not statistically robust; the
   NVT ensemble average will be computed once the stage completes and all frames are
   available.

3. **CPD7 and CPD10 parameterised but no MD started.** These systems were parameterised
   by job 22075127 (tleap succeeded) but the srun step never reached them due to the
   srun retry flood that consumed node time.

4. **Parallel per-compound approach failed.** Jobs 22076607, 22076621, 22076698, 22076809
   all hit the same "More processors requested than permitted" error. The fix adopted was
   to use a single sequential 9-system job (22076604) which successfully launched.

## Verdict

The phase produced a complete MD pipeline status report grounded in measured numbers
from live cluster output. The primary input (job 22076601) was unrecoverable; this was
diagnosed and documented rather than concealed. Numbers reported are correct and traceable
to specific mdinfo fields in job 22075127. No numbers were fabricated or extrapolated
without basis.
