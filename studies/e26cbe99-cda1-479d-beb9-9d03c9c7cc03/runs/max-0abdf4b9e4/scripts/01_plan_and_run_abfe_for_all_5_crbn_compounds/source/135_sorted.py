
import os, glob

BASE = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

# Find slurm log files to see prior job scripts
logs = sorted(glob.glob(f"{BASE}/slurm-*.log"))
print(f"Slurm logs: {[os.path.basename(l) for l in logs]}")

# Read the most recent successful one (not 6321629 which failed)
for log in logs:
    if "6321629" not in log:
        print(f"\n--- {os.path.basename(log)} (first 60 lines) ---")
        with open(log) as f:
            lines = f.readlines()[:60]
        for l in lines:
            print(l, end="")
        break
