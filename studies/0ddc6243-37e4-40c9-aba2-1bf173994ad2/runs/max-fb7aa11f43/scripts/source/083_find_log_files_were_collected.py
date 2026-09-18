
import subprocess, pathlib

# Find the log files that were collected
base = pathlib.Path("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b")
for name in ["task_summary.txt", "slurm-22076147.log",
             "REF_85C_rep1.log", "CPD1_rep1.log"]:
    for p in base.rglob(name):
        print(f"\n=== {p} ===")
        print(p.read_text())
