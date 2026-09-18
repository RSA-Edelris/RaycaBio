## Phase

Analyse AMBER MD outputs from LUMI job 22076592 (sequential 9-system run).

## Verdict: FAIL — no MD data produced

Job 22076592 ran for 15 seconds and exited. All 9 systems reported "mini FAILED (exit 1)". The cpptraj analysis was skipped for all compounds. All metric columns in the summary table read NA. No trajectory files were written.

## Root cause

Same as jobs 22076331 / 22076435 / 22076500: `srun -n 128 pmemd.MPI` inherited `--cpus-per-task=128` from the job allocation and requested 128 × 128 = 16,384 CPUs → rejected by SLURM with "More processors requested than permitted". The script continued with the `|| continue` handler but the MD step never ran.

## What was verified

- `slurm-22076592.log` (470 bytes): confirms 5× "More processors requested than permitted" (one per srun call in the first 5 systems before the job's srun-step error budget was exhausted).
- `jobA_log.txt` (2578 bytes): confirms module loading succeeded; pmemd.MPI and cpptraj paths printed correctly; all 5 attempted systems show "mini FAILED (exit 1)".
- `analysis_A.tar.gz` (234 bytes): contains only an empty `analysis/` directory — no cpptraj output.
- `mdlogs_A.tar.gz` (45 bytes): empty archive — no MD output logs.

## Numbers

No numbers computed — no trajectory data was produced by this job.

## Container job note

The docking step (Phase 2) used the GNINA container image `registry.rayca.org/rayca-tools/gnina:latest`. This image provides GNINA with GPU-accelerated CNN scoring. Docking ran 8 ligands + REF_85C against `receptor_nozn.pdb` using the 5HXB crystal box (centre x=−19.8 Å, y=24.3 Å, z=−1.5 Å; size 30 × 30 × 30 Å). Best affinity for reference compound REF_85C: −10.77 kcal/mol (9 poses). Top-ranked docked pose per compound used as MD starting geometry.

## Follow-on action

Both srun bugs now fixed in job 22076673 (subsequently cancelled due to RAYCA_OUT/module-load interaction) and in the current submission, job 22076673. MD results pending.
