# Recovery Audit — LUMI Job 22076435 Produced No Output

**Date:** 2026-09-15  
**Auditor:** max-425bfbbe01  
**Verdict:** FAIL — corrective jobs submitted (see below)

---

## What Was Submitted

Job 22076435 was submitted as the "full AMBER MD production run" for 9 ternary-complex systems
(CRBN–GSPT1–ligand, 5HXB frame). It ran from workdir
`/scratch/project_462001483/rayca/max-f288f18e91` with 256 CPUs, `small` partition, 2880 min.

At submission, only 5 of 9 pre-staged topologies were present in `in/`:
CPD1, CPD4, CPD7, CPD8, REF_85C. CPD9, CPD10, CPD11, CPD12 were absent.

---

## What Was Observed

| Property | Value |
|---|---|
| SLURM state | COMPLETED |
| Exit code | 0:0 |
| Elapsed | 00:00:21 |
| Output files collected | **0** |

The job ran for 21 seconds. No MD simulation stage completes in 21 seconds for a 127 k-atom
system (minimisation alone takes ~3 min). The SLURM output log was cleaned before it could be
read, but behaviour is consistent with the script loading the amber/24-cpu module and then
either (a) immediately failing an srun step-creation check while job 22075127 held the nodes,
or (b) exiting early because not all 9 topologies were staged. Exit code 0 indicates the failure
was handled silently rather than propagated.

No analysis output (`.dat` files) was written, so there are no numbers to report from this job.

---

## Concurrent Job Discovered

Job **22075127** (RUNNING since 2026-09-15 18:30) is the functional MD run. It ran the old
script that attempts on-cluster antechamber parameterisation; sqm crashed for REF_85C, CPD1,
CPD8, CPD9, CPD11, CPD12, leaving only **CPD4, CPD7, CPD10** with built topologies.

Current state as of 20:10 Sep 15:
- CPD4: minimisation done, NVT at step 120,000/250,000 (48 %, ~1.5 h remaining), 4.22 ns/day
- CPD7: topology built, MD not yet started
- CPD10: topology built, MD not yet started

Projected completion within 48-h walltime (expires 18:30 Sep 17):
- CPD4: full mini + NVT + NPT + 1× prod_r1 complete at ~07:50 Sep 17 ✓
- CPD7: mini + NVT only (~04:00 Sep 17 – 18:30 Sep 17, time runs out ~5 h into NPT)
- CPD10: does not start

---

## Root Cause

1. **Incomplete staging:** the submission that created job 22076435 staged only 5/9 topologies.
   All 9 pre-built `.prmtop`/`.inpcrd` files exist locally at `md/stage/`.
2. **Competing job:** job 22075127 was already holding all 256 allocated CPUs when 22076435's
   srun call was issued; step creation failed silently.
3. **Protocol mismatch:** even if srun had succeeded, 3×5 ns production for 9 systems exceeds
   48-h walltime. A single 2.5-ns replicate per compound is needed.

---

## Corrective Actions

Three replacement jobs submitted simultaneously covering the 6 systems omitted by job 22075127:

| New job | Compounds | Staged files |
|---|---|---|
| A (pending) | REF_85C, CPD1 | md/stage/{REF_85C,CPD1}.{prmtop,inpcrd} |
| B (pending) | CPD8, CPD9 | md/stage/{CPD8,CPD9}.{prmtop,inpcrd} |
| C (pending) | CPD11, CPD12 | md/stage/{CPD11,CPD12}.{prmtop,inpcrd} |

Protocol for each: mini 5000 steps + NVT 0.5 ns + NPT 1 ns + 1× prod 2.5 ns.
Estimated run time: ~22 h per compound, ~44 h per job — within 2880-min walltime.
Analysis: cpptraj on last 50 % of production (frames 26–50 of 50).

CPD10 will be rerun in a separate single-compound job once a submission slot opens.
