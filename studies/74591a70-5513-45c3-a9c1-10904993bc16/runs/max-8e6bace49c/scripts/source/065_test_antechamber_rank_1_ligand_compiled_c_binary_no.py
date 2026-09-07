
# Test antechamber on the rank-1 ligand (compiled C binary, no Python dep)
import subprocess, os
from pathlib import Path

WORK  = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
AMBER = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"
MMDIR = f"{WORK}/mmgbsa"

test_name = "EDEL-CRBN-0005_ent"
lig_dir   = f"{MMDIR}/{test_name}"
os.makedirs(lig_dir, exist_ok=True)

sdf = f"{WORK}/best_poses/{test_name}_pose1.sdf"
mol2 = f"{lig_dir}/lig.mol2"

# antechamber is a compiled C binary — PYTHONPATH doesn't matter
r = subprocess.run(
    [f"{AMBER}/antechamber",
     "-i", sdf,   "-fi", "sdf",
     "-o", mol2,  "-fo", "mol2",
     "-c", "bcc", "-s", "2",
     "-at", "gaff2", "-nc", "0",
     "-m", "1", "-rn", "LIG"],
    cwd=lig_dir, capture_output=True, text=True,
    timeout=600
)
print("antechamber returncode:", r.returncode)
print("stdout:", r.stdout[:400])
print("stderr:", r.stderr[:400])
if Path(mol2).exists():
    print(f"mol2 written: {Path(mol2).stat().st_size} bytes")
