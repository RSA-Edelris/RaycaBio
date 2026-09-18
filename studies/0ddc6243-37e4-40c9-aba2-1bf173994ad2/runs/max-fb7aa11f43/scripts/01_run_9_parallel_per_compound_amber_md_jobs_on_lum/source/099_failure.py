
base = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b"

verification_blocks = {
    f"{base}/progress.txt": """

=== VERIFICATION ===
Checked: all 9 systems show MINI_FAIL. Root cause confirmed as srun step-creation failure
(job 22076601, script had srun -n 128 without --cpus-per-task=1 override). No MD data
produced. Superseded by job 22076673 which has both fixes applied and is currently running
(REF_85C step 2/4 active as of 2026-09-15 ~20:18 EEST). Verified: this file was written by
the analysis pass on job 22076601 outputs. Contents match slurm-22076611.log (srun rejection).
""",
    f"{base}/run_start.txt": """

=== VERIFICATION ===
Checked: RESULTS path points to max-243812cde4/out/job-22076601. Confirmed module loads
completed (pmemd and cpptraj paths are valid amber/24-cpu paths). RESULTS was captured before
module loads in this script — capture was correct. However, pmemd.MPI srun calls used
-n 128 without --cpus-per-task=1, so all srun steps failed. The RESULTS path itself was
never written to because no MD completed.
""",
    f"{base}/summary_table.txt": """

=== VERIFICATION ===
All NO_DATA entries confirmed — no cpptraj .dat files were produced by job 22076601 because
every pmemd.MPI step failed with "More processors requested than permitted". These are not
partial results: zero trajectory frames exist for any compound from this job. Replacement
job 22076673 is running and will populate these metrics when complete.
""",
    f"{base}/CPD7_progress.txt": """
=== VERIFICATION ===
CPD7 MINI FAILED at 20:11:27 EEST 2026. This is a parallel per-compound job (not 22076673).
Failed with same srun --cpus-per-task bug. Zero MD steps executed. Not retried — sequential
job 22076673 covers CPD7 with fixed srun flags.
""",
    f"{base}/job-22076647/CPD7_progress.txt": """
=== VERIFICATION ===
CPD7 MINI FAILED at 20:11:27 EEST 2026. This is a parallel per-compound job (not 22076673).
Failed with same srun --cpus-per-task bug. Zero MD steps executed. Not retried — sequential
job 22076673 covers CPD7 with fixed srun flags.
""",
}

for path, block in verification_blocks.items():
    with open(path, 'a') as f:
        f.write(block)
    print(f"Appended verification to {path.split('/')[-2]}/{path.split('/')[-1]}")
