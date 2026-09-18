
import os, glob

# Find the slurm log for 22076694
results_dir = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b"

# Find all relevant files
for root, dirs, files in os.walk(results_dir):
    for f in files:
        if "22076694" in f or "22076619" in f or f in ("CPD8_progress.txt", "logfile", "min.out", "min.mdinfo", "progress.log"):
            p = os.path.join(root, f)
            print(f"{len(open(p,'rb').read()):8d}  {p}")
