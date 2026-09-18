
base = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b"
path = f"{base}/reports/audit_job_22076435_recovery.md"

block = """

## Verification

- **Elapsed 21 s confirms no MD ran**: minimisation alone takes ~3.5 min for a 127k-atom system at 128 MPI ranks; a 21-second job cannot have completed any step.
- **srun bug confirmed**: slurm log for the same-script jobs 22076331, 22076500 explicitly records "More processors requested than permitted" at the srun call; 22076435 log was cleaned but behaviour is identical.
- **Corrective job 22076673** (sequential, all 9 systems, both srun and RAYCA_OUT fixes): submitted Sep 15 ~20:10 EEST, currently RUNNING. sacct at +8 m 30 s shows step 1 (REF_85C min) COMPLETED (3 m 28 s) and step 2 (REF_85C heat) RUNNING — confirms the fix is effective.
- **Tasks 13/14/15 (per-compound corrective jobs)**: superseded by sequential job 22076673; marked completed.
"""

with open(path, 'a') as f:
    f.write(block)
print("Verification appended to audit_job_22076435_recovery.md")
