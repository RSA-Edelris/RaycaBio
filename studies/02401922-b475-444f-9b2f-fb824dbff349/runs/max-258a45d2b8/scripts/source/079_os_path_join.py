
import subprocess, os, re, time
from rdkit import Chem

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
ligands_dir = os.path.join(wd, "ligands_3d")
results_dir = os.path.join(wd, "docking_results")
os.makedirs(results_dir, exist_ok=True)

vina_bin = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/vina"
receptor_pdbqt = os.path.join(wd, "receptor.pdbqt")

# Build index: lig number -> compound name
# obabel split preserves order; names are in SDF title line
import re as _re
def get_sdf_name(sdf_path):
    with open(sdf_path) as f:
        return f.readline().strip()

# Sort numerically: lig1.sdf, lig2.sdf, ...
def sdf_num(f):
    m = _re.search(r'lig(\d+)\.sdf', f)
    return int(m.group(1)) if m else 0

sdf_files = sorted([f for f in os.listdir(ligands_dir) if f.endswith('.sdf')], key=sdf_num)
print(f"SDF files to process: {len(sdf_files)}")
print("First 5 names:")
for f in sdf_files[:5]:
    name = get_sdf_name(os.path.join(ligands_dir, f))
    print(f"  {f} -> {name}")
