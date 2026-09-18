## What failed

LUMI job 22076147 (128 CPUs, standard partition) ran for 7 seconds and produced no MD output. All 9 systems failed at minimisation with:

```
srun: error: Unable to create step for job 22076147: More processors requested than permitted
```

## Root cause

The job script launched 9 background subshells (`&`) at nearly the same time, each containing `srun -n 64`. All 9 `srun` calls were dispatched to SLURM within ~3 seconds of one another. SLURM on LUMI Cray nodes does not queue job steps — it either grants them immediately or rejects them. With 128 CPUs allocated, at most 2 × 64-core steps could have succeeded, but all 9 arrived simultaneously before any step had time to start and release slots. SLURM saw 9 × 64 = 576 requested cores against a 128-core allocation and rejected every step.

## Design assumption that was wrong

"Only 2 will run concurrently because the others will block on `srun`." This is correct on systems where `srun` blocks and re-attempts. On LUMI with Cray MPICH, `srun` fails immediately when resources are unavailable. No queuing, no retry.

## Fix applied

Job 22076275 uses sequential execution:

```bash
for sys in "${SYSTEMS[@]}"; do
    cd "$RUNDIR"
    srun -n 128 pmemd.MPI -O -i min.in ...
    srun -n 128 pmemd.MPI -O -i heat.in ...
    srun -n 128 pmemd.MPI -O -i equil.in ...
    srun -n 128 pmemd.MPI -O -i prod.in ...
    # cpptraj analysis inline
done
```

One system runs at a time. All 128 cores assigned to a single `srun` step. SLURM step contention is impossible.

## Expected runtime

With 128 MPI tasks on a ~127k-atom TIP3P system:
- Minimisation (10k cycles): ~10–20 min
- Heating (100 ps, 50k steps): ~20–40 min
- Equilibration (200 ps, 100k steps): ~40–80 min
- Production (1 ns, 500k steps): ~1.5–3 h
- Per-system total: ~2.5–4.5 h
- 9 systems sequential: ~22–40 h → within 48 h walltime

## Job IDs

| Job | Outcome |
|---|---|
| 22076021 | Failed: `SLURM_NTASKS` unbound variable (set -e) |
| 22076147 | Failed: srun step contention (9 × 64 cores simultaneously) |
| 22076275 | Submitted — sequential, srun -n 128 |
