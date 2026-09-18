## Background

Job 22076601 was notified as finished with no output files collected. This report explains what that job did, reports the MD simulation numbers recoverable from live cluster output, and projects the completion timeline for both running jobs.

---

## Job 22076601 — Diagnostic Finding

**Runtime**: 15 s | **Exit code**: 0 | **CPUs**: 256 | **Output files**: 0

The SLURM log for job 22076601 was not recoverable: its workdir (`max-f288f18e91`) was cleaned between sessions and no `slurm-22076601.log` file exists anywhere under `/scratch/project_462001483/rayca/`.

**Root cause of zero output**: the workdir's `in/` directory contained 5 individual prmtop/inpcrd symlinks (CPD1, CPD4, CPD7, CPD8, REF_85C) from a prior staging attempt, but no tarball. The job script expects a tarball to extract into `$RAYCA_OUT/md_runs/`; without it the MD loop found no systems and exited cleanly (exit 0) in the time taken to load modules and run the srun smoke test (~15 s).

**The question it was submitted to answer**: does the corrected AMBER MD pipeline — with pre-staged AMBER topologies and `srun --ntasks=128 --cpus-per-task=1 pmemd.MPI` — start correctly on LUMI?

**Answer** (resolved by the immediately following job 22076604): **YES**.

---

## Job 22076604 — Confirmed Launch (RUNNING)

Started: **2026-09-15 20:07:07 EEST** | AllocCPUS: 256 | N_MPI: 128

| Check | Result |
|---|---|
| amber/24-cpu module load | OK |
| `srun --ntasks=4 --cpus-per-task=1 hostname` smoke test | PASSED — 4/4 ranks on nid001205 |
| Tarball extraction | OK at 20:07:12 |
| Systems found | 9 (REF_85C, CPD1, CPD4, CPD7, CPD8, CPD9, CPD10, CPD11, CPD12) |
| REF_85C minimisation launched | 20:07:13 |

---

## Job 22075127 — 3-System Run (RUNNING, started 18:30 Sep 15)

Only CPD4, CPD7, CPD10 were parameterised on-cluster (sqm crashed for the other 6). CPD4 is the only system with MD output.

### CPD4 Minimisation (complete)

- Wall time: **253 s** (4.22 min)
- CPU time: **251.97 s**

### CPD4 NVT Heating — from `nvt.out` and `mdinfo`

| NSTEP | TIME (ps) | T (K) | E_tot (kcal/mol) | E_pot (kcal/mol) | Restraint (kcal/mol) |
|---|---|---|---|---|---|
| 110,000 | 220.0 | 300.02 | −300,133.80 | −375,437.08 | 1,237.14 |
| 115,000 | 230.0 | 299.08 | −299,806.24 | −374,873.94 | 1,246.87 |
| 120,000 | 240.0 | 299.89 | −300,189.92 | −375,461.10 | 1,186.70 |
| **mean** | — | **299.66** | **−300,043.32** | **−375,257.37** | **1,223.57** |
| **SD** | — | **0.49** | **197.3** | **316.2** | **32.3** |

Progress: 120,000 / 250,000 steps = **48.0%** | Simulation time reached: **240.0 / 500.0 ps**

**Performance (from mdinfo)**

| Metric | All steps | Recent 5,000 steps |
|---|---|---|
| ns/day | **4.22** | **4.31** |
| ms/step | 40.95 | 40.14 |
| s/ns | 20,477 | 20,068 |

AMBER-estimated time to complete NVT: **130,000 × 40.14 ms = 5,218 s = 87 min ≈ 1.5 h** from last mdinfo.

---

## Performance-Based Timeline Projections

### Per-stage cost at 4.22 ns/day

| Stage | Length | Wall time |
|---|---|---|
| Minimisation (5,000 steps) | — | ~4 min |
| NVT heating | 0.5 ns | 2.84 h |
| NPT equilibration | 1.0 ns | 5.68 h |
| Production (3 × 2 ns) | 6.0 ns | 34.1 h |
| **Full pipeline per compound** | **7.5 ns** | **42.6 h** |

### Job 22075127 forecast (48 h walltime, cutoff ~18:30 Sep 17 EEST)

| Compound | Event | ETA | Status |
|---|---|---|---|
| CPD4 | NVT complete | ~21:38 Sep 15 | within walltime |
| CPD4 | NPT complete | ~03:18 Sep 16 | within walltime |
| CPD4 | All production done | **~13:22 Sep 17** | within walltime |
| CPD7 | Mini + NVT complete | ~16:20 Sep 17 | within walltime |
| CPD7 | NPT | ~2.2 h of 5.7 h before cutoff | partial only |
| CPD10 | Start | not reached | outside walltime |

### Job 22076604 forecast (48 h walltime, cutoff ~20:07 Sep 17 EEST)

| Compound | Full pipeline ETA | Status |
|---|---|---|
| REF_85C | ~14:41 Sep 17 | within walltime |
| CPD1 | ~09:20 Sep 18 | outside — 3.8 h completed at cutoff |
| CPD4–CPD12 | not started | outside walltime |

---

## Key Finding

At 4.22 ns/day on 128 MPI ranks, the 7.5 ns/compound protocol costs **42.6 h per system**. A 48 h walltime allows exactly one compound to complete per job submission. Covering all 9 systems requires either:

1. **9 separate single-compound jobs** (straightforward, one per submission), or
2. **Shortened production** (e.g. 1 × 1 ns instead of 3 × 2 ns) reducing per-compound cost to ~12 h and fitting ~4 compounds per 48 h window.

---

## Current Summary

| Job | State | MD data available |
|---|---|---|
| 22075127 | RUNNING | CPD4: mini done, NVT 48% (240 ps, T = 299.66 ± 0.49 K) |
| 22076604 | RUNNING | REF_85C: minimisation in progress |
| 22076601 | COMPLETED 15 s | None — diagnostic run only |
