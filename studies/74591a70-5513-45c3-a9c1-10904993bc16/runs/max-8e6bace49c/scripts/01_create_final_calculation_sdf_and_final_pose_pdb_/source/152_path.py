
from pathlib import Path
BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

# ── Verify final_calculation.sdf (3D) ───────────────────────────────────────
import subprocess
VENV_PY = "/home/ubuntu/rayca-runtime/.venv/bin/python3"

verify_code = '''
from pathlib import Path
from rdkit import Chem

BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

# 3D SDF
suppl = list(Chem.SDMolSupplier(str(BASE/"final_calculation.sdf"), removeHs=False))
print(f"3D SDF: {len(suppl)} molecules loaded")
for mol in suppl:
    if mol is None: print("  FAIL: None mol")
    else:
        name = mol.GetProp("_Name")
        smiles = mol.GetProp("SMILES_stereo") if mol.HasProp("SMILES_stereo") else "MISSING"
        dg = mol.GetProp("MMGBSA_dG_kcal_mol") if mol.HasProp("MMGBSA_dG_kcal_mol") else "MISSING"
        dock = mol.GetProp("Docking_Affinity_kcal_mol") if mol.HasProp("Docking_Affinity_kcal_mol") else "MISSING"
        nint = mol.GetProp("N_Interactions") if mol.HasProp("N_Interactions") else "MISSING"
        conf3d = mol.GetConformer()
        p0 = conf3d.GetAtomPosition(0)
        z_nonzero = abs(p0.z) > 0.01
        print(f"  {name:28s} dock={dock:6}  dG={dg:>10}  int={nint:2}  3D={z_nonzero}  stereo_chars={'@' in smiles or '/' in smiles}")

# 2D SDF
suppl2d = list(Chem.SDMolSupplier(str(BASE/"final_calculation_2d.sdf")))
print(f"\\n2D SDF: {len(suppl2d)} molecules loaded")
for mol in suppl2d[:3]:
    if mol:
        name = mol.GetProp("_Name")
        conf = mol.GetConformer()
        p0 = conf.GetAtomPosition(0)
        print(f"  {name}: z0={p0.z:.3f} (should be ~0 for 2D)")
'''

r = subprocess.run([VENV_PY, "-c", verify_code], capture_output=True, text=True,
                   cwd=str(BASE))
print(r.stdout[:3000])
if r.returncode != 0:
    print("ERR:", r.stderr[-500:])
