
VENV_PY = "/home/ubuntu/rayca-runtime/.venv/bin/python3"
BASE_STR = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"

verify = '''
from pathlib import Path
from rdkit import Chem
import json

BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

# ── 3D SDF ──────────────────────────────────────────────────────────────────
mols3d = list(Chem.SDMolSupplier(str(BASE/"final_calculation.sdf"), removeHs=False))
ok3d = [m for m in mols3d if m is not None]
print(f"3D SDF: {len(mols3d)} records, {len(ok3d)} valid (expected 22)")
assert len(ok3d) == 22, "FAIL: wrong count"

required_tags = ["SMILES_stereo","Docking_Affinity_kcal_mol","CNN_Affinity",
                 "MMGBSA_dG_kcal_mol","Interacting_Residues","HBond_Residues","N_Interactions"]
for mol in ok3d:
    name  = mol.GetProp("_Name")
    # check tags
    missing = [t for t in required_tags if not mol.HasProp(t)]
    # check 3D coords (z non-zero for most)
    conf = mol.GetConformer()
    zvals = [abs(conf.GetAtomPosition(i).z) for i in range(mol.GetNumAtoms())]
    has3d = max(zvals) > 0.01
    # check stereo in SMILES
    smiles = mol.GetProp("SMILES_stereo")
    stereo = "@" in smiles or "/" in smiles
    status = "OK" if not missing and has3d else "WARN"
    print(f"  {status} {name:28s} 3D={has3d} stereo={stereo} missing={missing}")

# ── 2D SDF ──────────────────────────────────────────────────────────────────
mols2d = list(Chem.SDMolSupplier(str(BASE/"final_calculation_2d.sdf")))
ok2d = [m for m in mols2d if m is not None]
print(f"\\n2D SDF: {len(mols2d)} records, {len(ok2d)} valid (expected 22)")
for mol in ok2d[:3]:
    conf = mol.GetConformer()
    z = [abs(conf.GetAtomPosition(i).z) for i in range(mol.GetNumAtoms())]
    print(f"  {mol.GetProp(\'_Name\'):28s} max_z={max(z):.4f} (should be ~0)")

# ── PDB ──────────────────────────────────────────────────────────────────────
pdb = (BASE/"final_pose.pdb").read_text().splitlines()
atom_lines  = [l for l in pdb if l.startswith("ATOM")]
hetatm_lines = [l for l in pdb if l.startswith("HETATM")]
ter_lines   = [l for l in pdb if l.startswith("TER")]
remark_lines = [l for l in pdb if l.startswith("REMARK")]
chains_used = sorted(set(l[21] for l in atom_lines+hetatm_lines))
print(f"\\nPDB: {len(atom_lines)} ATOM, {len(hetatm_lines)} HETATM, {len(ter_lines)} TER, {len(remark_lines)} REMARK")
print(f"     Chains: {chains_used}")
lvy = [l for l in hetatm_lines if "LVY" in l]
print(f"     LVY reference ligand: {len(lvy)} atoms")
lig = [l for l in hetatm_lines if "LIG" in l]
print(f"     Docked LIG records: {len(lig)}")
'''

import subprocess
r = subprocess.run([VENV_PY, "-c", verify], capture_output=True, text=True, cwd=BASE_STR)
print(r.stdout)
if r.returncode != 0:
    print("ERR:", r.stderr[-500:])
