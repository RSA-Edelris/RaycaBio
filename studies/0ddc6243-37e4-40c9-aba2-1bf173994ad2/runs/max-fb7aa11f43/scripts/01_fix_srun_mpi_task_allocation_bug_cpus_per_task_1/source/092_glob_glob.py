
import glob, os

base = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b"
logs = glob.glob(f"{base}/**/slurm-22076500.log", recursive=True)
print("Found:", logs)
for p in logs:
    print(f"\n=== {p} ===")
    with open(p) as f:
        print(f.read())
