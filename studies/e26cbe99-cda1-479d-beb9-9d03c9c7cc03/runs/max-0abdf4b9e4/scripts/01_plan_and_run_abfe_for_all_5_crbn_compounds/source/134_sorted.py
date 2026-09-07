
import os, subprocess

BASE = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

# List EDS01357518_ent2 prep directory
d = f"{BASE}/md_EDS01357518_ent2"
files = sorted(os.listdir(d))
print(f"md_EDS01357518_ent2/ ({len(files)} files):")
for f in files:
    fp = f"{d}/{f}"
    size = os.path.getsize(fp) if os.path.isfile(fp) else 0
    flag = "DIR" if os.path.isdir(fp) else f"{size//1024} KB"
    print(f"  {f}  ({flag})")
