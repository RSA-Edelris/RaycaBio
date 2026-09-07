
import subprocess, os, json, shutil
from pathlib import Path

WORK = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
AMBER = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"
MMGBSA_DIR = f"{WORK}/mmgbsa"
os.makedirs(MMGBSA_DIR, exist_ok=True)

# Check Amber tools
for tool in ["antechamber", "parmchk2", "tleap", "pdb4amber", "sander", "MMPBSA.py"]:
    p = Path(f"{AMBER}/{tool}")
    print(f"{tool}: {'OK' if p.exists() else 'MISSING'}")

# Inspect receptor (noh version for tleap)
rec_noh = f"{WORK}/4CI2_receptor_noh.pdb"
print(f"\nReceptor noh exists: {Path(rec_noh).exists()}, size: {Path(rec_noh).stat().st_size} bytes")

# Count atoms and check ZN
zn_lines = []
res_names = set()
with open(rec_noh) as f:
    for line in f:
        if line.startswith(("ATOM","HETATM")):
            resname = line[17:20].strip()
            res_names.add(resname)
            if resname in ("ZN", "ZN2"):
                zn_lines.append(line.rstrip())
print(f"Unique residue names: {sorted(res_names)}")
print(f"ZN lines:\n" + "\n".join(zn_lines))

# List best_poses
poses = sorted(Path(f"{WORK}/best_poses").glob("*.sdf"))
print(f"\nBest poses: {len(poses)}")
print("First 3:", [p.name for p in poses[:3]])

# Load ligand names
with open(f"{WORK}/docking_scores_all32.json") as f:
    scores = json.load(f)
names = list(scores.keys())
print(f"\nLigand names ({len(names)}):", names[:4], "...")
