
import glob, os

base = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b"
targets = ["*22076592*", "*analysis_A*", "*jobA_log*", "*mdlogs_A*", "*slurm-22076592*"]
found = set()
for pat in targets:
    found.update(glob.glob(f"{base}/**/{pat}", recursive=True))
for f in sorted(found):
    print(f"{os.path.getsize(f):>10d}  {f}")
