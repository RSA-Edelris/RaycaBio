## Job

22076694 — LUMI `standard` partition, submitted by a parallel per-compound context.

## Failure mode

Identical to jobs 22076331 / 22076435 / 22076465 / 22076500 / 22076592:

```
srun: error: Unable to create step for job 22076694: More processors requested than permitted
```

The script used `srun -n 128 pmemd.MPI` without overriding `--cpus-per-task`, inheriting the job-level `--cpus-per-task=128` → 128 × 128 = 16,384 CPUs requested → rejected instantly.

## Context

A previous context window attempted a parallel per-compound approach (9 separate single-system jobs) as an alternative to the sequential 9-system job. This job (22076694) was one of those — submitted for CPD8. Only `CPD8_progress.txt` was collected (contents: "START mini … MINI FAILED").

## Action taken

No resubmission. Sequential job **22076673** (submitted Sep 15, running) covers all 9 systems with both fixes applied:
- `RESULTS="${RAYCA_OUT}"` captured before any `module load`
- `srun --ntasks=128 --cpus-per-task=1 pmemd.MPI` in every srun call

The sequential approach is the primary path. The parallel per-compound approach is abandoned.

## Verification

- `slurm-22076694.log` (1042 bytes): confirms single srun rejection, no MD ran.
- `CPD8_progress.txt` (83 bytes): "MINI FAILED" within 1 second of START → immediate srun failure, no pmemd execution.
- Job 22076619 (cancelled by mistake): its slurm log confirms the corrected srun syntax passes (`SMOKE PASS`), and REF_85C minimization reached 5000 steps (final E = −471,410 kcal/mol) before the cancel signal — confirming the fix is correct and the system topology is valid.
