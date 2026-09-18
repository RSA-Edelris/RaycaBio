
import subprocess, os, pathlib

SESSION = pathlib.Path("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b")
LIG_DIR  = SESSION / "md" / "ligands"
PARAM_DIR = SESSION / "md" / "param"
PARAM_DIR.mkdir(parents=True, exist_ok=True)

LIGS = ["REF_85C","CPD1","CPD4","CPD7","CPD8","CPD9","CPD10","CPD11","CPD12"]

# Verify all SDF files present and check atom counts
from rdkit import Chem
print("Ligand SDF check:")
for lig in LIGS:
    sdf = LIG_DIR / f"{lig}_top.sdf"
    if sdf.exists():
        mol = next(Chem.SDMolSupplier(str(sdf), removeHs=False), None)
        nat = mol.GetNumAtoms() if mol else "PARSE_ERR"
        print(f"  {lig:<10}: {nat} atoms (with H)")
    else:
        print(f"  {lig:<10}: MISSING")
