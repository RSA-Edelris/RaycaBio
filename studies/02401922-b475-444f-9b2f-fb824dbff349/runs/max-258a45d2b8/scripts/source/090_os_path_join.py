
import os, re

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
results_dir = os.path.join(wd, "docking_results")
log = os.path.join(wd, "missing_docking.log")

with open(log) as f:
    content = f.read()
print("Log tail:")
print(content[-800:])

def lig_num(f):
    m = re.search(r'lig(\d+)_out', f)
    return int(m.group(1)) if m else 0

done = sorted([lig_num(f) for f in os.listdir(results_dir) if f.endswith('_out.pdbqt')])
missing = [n for n in range(1,85) if n not in done]
print(f"\nDone: {len(done)}/84, Missing: {len(missing)}: {missing}")
