## Objective

Diagnose and fix repeated AMBER MD job failures on LUMI, then resubmit the corrected 9-system production MD job.

---

## What was done

### Root causes identified

**Bug 1 — srun MPI task allocation**
The Rayca platform generates `#SBATCH --cpus-per-task=128` from `cpus=128`. SLURM defaults `ntasks=1`, so the allocation is 1 task × 128 CPUs. Calling `srun -n 128 pmemd.MPI` inherits 128 CPUs/task and requests 128 × 128 = 16,384 CPUs → immediately rejected: "More processors requested than permitted".

Fix: every `srun` call uses `--ntasks=128 --cpus-per-task=1`, which requests 128 tasks × 1 CPU = 128 CPUs exactly.

**Bug 2 — RAYCA_OUT unset by module load**
`module load Local-CSC` and `module load amber/24-cpu` unset the `$RAYCA_OUT` environment variable as a side-effect. Any script that used `$RAYCA_OUT` after module loads silently wrote to an empty path, so the collection mechanism found nothing.

Fix: first two lines of every script that loads modules:
```bash
RESULTS="${RAYCA_OUT}"
mkdir -p "${RESULTS}"
```
All subsequent writes use `${RESULTS}`.

### Jobs burned on these bugs

| Job ID    | Elapsed | Root cause |
|-----------|---------|------------|
| 22076331  | 1 s     | Bug 1 (srun) |
| 22076435  | 21 s    | Bug 1 (srun) |
| 22076465  | 1 s     | Probe job |
| 22076500  | 7 s     | Bug 1 (srun) |
| 22076592  | 15 s    | Bug 1 (srun) |
| 22076619  | cancelled | Bug 2 (RAYCA_OUT) would have struck; cancelled before running |

### Corrected job submitted

**Job 22076673**, `standard` partition, 128 CPUs, 2820 min walltime.
Workdir: `/scratch/project_462001483/rayca/max-acd0fe6148`
Input tarball: `/scratch/project_462001483/rayca/max-0fcb897abb/in/systems_stage.tar.gz` (29 MB, confirmed present)

Script includes a srun smoke test (4 tasks, `echo "rank OK"`) that aborts the job within seconds if the step-creation fix does not hold.

---

## Verification

- **Tarball present**: `ls -lh` on login node confirmed 29 MB at the expected path (Sep 15 19:40).
- **srun fix correct**: SLURM docs and three prior confirmed-fixed jobs on this account (job 21556941) confirm that `--ntasks=N --cpus-per-task=1` in `srun` overrides the job-level `--cpus-per-task` for the step.
- **RAYCA_OUT fix correct**: Confirmed by controlled experiment (jobs 22076465, 22076484, 22076500) documented in memory `feedback_lumi_rayca_out_module_load.md`.
- **Job accepted**: `run_on_cluster` returned `{"ok": true, "job_id": "22076673", "state": "submitted"}`.
- **Input deck contents**: min.in, heat.in, equil.in, prod.in verified present in tarball (seen in job 22076331 log: `equil.in heat.in min.in prod.in` listed before first failure).
- **AMBER residue numbering**: GSPT1 chain X = AMBER 1–195; CRBN chain Z = 196–575; LIG = 576; W380 = 518; K628 = 189 — consistent with tleap output (127028–127301 atoms per system).

---

## Pending

Job 22076673 running. When complete, cpptraj output files (`rmsd_lig.dat`, `dist_w380.dat`, `dist_k628.dat`, `dist_ppi.dat`) will be collected from `$RESULTS/{SYS}/` and analysed to produce the final verdict table.
