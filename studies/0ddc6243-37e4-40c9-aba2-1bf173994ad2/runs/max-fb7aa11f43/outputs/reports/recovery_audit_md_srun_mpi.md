## Summary

Three AMBER MD submission attempts (SLURM jobs 22076331, 22076435, 22076465) all failed within seconds of starting with the error:

```
srun: error: Unable to create step for job XXXXXXXX: More processors requested than permitted
```

The production MD job should have run for ~47 hours over 9 ternary complex systems. All input data (solvated AMBER topologies for REF_85C, CPD1, CPD4, CPD7, CPD8, CPD9, CPD10, CPD11, CPD12) was correctly staged in `/scratch/project_462001483/rayca/max-0fcb897abb/in/systems_stage.tar.gz` (29 MB, confirmed present).

---

## Root Cause

The SLURM job header used:
```
#SBATCH --cpus-per-task=128
```
with no explicit `--ntasks`. SLURM defaulted to `ntasks=1`, allocating **1 task slot × 128 CPUs = 128 CPUs total**.

The script then called:
```bash
srun -n 128 pmemd.MPI ...
```

This tries to create 128 MPI task steps. Each step inherits `--cpus-per-task=128` from the job allocation → requests **128 × 128 = 16,384 CPUs** → rejected immediately by SLURM.

---

## Job History

| Job ID    | Elapsed | Exit | Failure mode |
|-----------|---------|------|--------------|
| 22076331  | 1 s     | 1    | srun step rejected (cpus-per-task bug) |
| 22076435  | 21 s    | 0    | Same bug; exit 0 recorded by scheduler |
| 22076465  | 1 s     | 0    | Metadata/probe job, not the MD run |

---

## Fix Applied

Override the per-step CPU count in every `srun` call:
```bash
srun --ntasks=128 --cpus-per-task=1 pmemd.MPI ...
```

This allocates 128 MPI ranks × 1 CPU each = 128 CPUs = exactly what the job holds.

Additional hardening:
- Smoke-test `srun` with 4 tasks at job start; abort fast if the fix does not hold
- Each MD phase uses `|| { echo FAILED; continue; }` so a single-system failure does not abort the remaining 8 systems

---

## Recovery Plan

Resubmit with corrected srun flags using the existing tarball. Expected runtime ~47 h on 128 CPUs (`standard` partition, 2820 min walltime).
