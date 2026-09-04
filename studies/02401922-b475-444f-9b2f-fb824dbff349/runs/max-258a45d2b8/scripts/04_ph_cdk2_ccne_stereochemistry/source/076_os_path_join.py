
import subprocess, os
from rdkit import Chem
from rdkit.Chem import AllChem

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
ligands_dir = os.path.join(wd, "ligands_3d")
os.makedirs(ligands_dir, exist_ok=True)

vina_bin = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/vina"

# Step 1: obabel protonate all at pH 7.4, get SDF with 3D coords
# obabel can add H at pH 7.4 and generate 3D with --gen3d
std_sdf = os.path.join(wd, "all_std_neutral.sdf")
prot_sdf = os.path.join(wd, "all_protonated_3d.sdf")

r = subprocess.run(
    ['/usr/bin/obabel', std_sdf, '-O', prot_sdf, '-p', '7.4', '--gen3d', '--best'],
    capture_output=True, text=True
)
print("obabel stdout:", r.stdout[:500])
print("obabel stderr:", r.stderr[:500])
print("RC:", r.returncode)
if os.path.exists(prot_sdf):
    print(f"Output: {os.path.getsize(prot_sdf)//1024} KB")
