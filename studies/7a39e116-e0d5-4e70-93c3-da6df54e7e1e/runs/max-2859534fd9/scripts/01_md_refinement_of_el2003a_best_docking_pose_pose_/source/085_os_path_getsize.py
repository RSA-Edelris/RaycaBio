
import os, glob

ART = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# Find the index.ndx written by last run
ndx_path = f"{ART}/index.ndx"
top_path  = f"{ART}/complex.top"
traj_path = f"{ART}/traj_com.xtc"
pdb_path  = f"{ART}/complex_reres.pdb"

for p in [ndx_path, top_path, traj_path, pdb_path]:
    sz = os.path.getsize(p) if os.path.exists(p) else 0
    print(f"  {os.path.basename(p):25s}  {'exists' if sz else 'MISSING':8s}  {sz:>10,} bytes")

# Read group names from index.ndx
print("\nIndex groups:")
with open(ndx_path) as fh:
    for i, ln in enumerate(fh):
        if ln.startswith('['):
            print(f"  group {i//1:2d}? → {ln.strip()}")
        if i > 200:
            break
