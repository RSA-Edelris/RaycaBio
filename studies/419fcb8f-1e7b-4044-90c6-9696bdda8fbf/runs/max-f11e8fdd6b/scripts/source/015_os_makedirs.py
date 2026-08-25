
import subprocess, os, glob

os.makedirs("chemdraw_export/cdxml", exist_ok=True)
os.makedirs("chemdraw_export/rdf",   exist_ok=True)

# ── 1. CDXML: convert each MOL block from SDF individually ────────────────
from rdkit import Chem
from rdkit.Chem import AllChem

smiles = {
    "Target":   "O=C1CCNc2cc3c(cc2CN1CC1CC1)OCO3",
    "SM-1":     "O=Cc1cc2c(cc1[N+](=O)[O-])OCO2",
    "SM-2":     "NCC1CC1",
    "SM-4":     "CC(C)(C)OC(=O)NCCC(=O)O",
    "SM-6":     "O=Cc1cc2c(cc1N)OCO2",
    "SM-7":     "O=Cc1cc2c(cc1Br)OCO2",
    "Int-A1":   "O=[N+]([O-])c1cc2c(cc1CNCC1CC1)OCO2",
    "Int-A2":   "CC(C)(C)OC(=O)N(Cc1cc2c(cc1[N+](=O)[O-])OCO2)CC1CC1",
    "Int-A3":   "CC(C)(C)OC(=O)N(Cc1cc2c(cc1N)OCO2)CC1CC1",
    "Int-A4":   "CC(C)(C)OC(=O)NCCC(=O)Nc1cc2c(cc1CN(CC3CC3)C(=O)OC(C)(C)C)OCO2",
    "Int-A5":   "NCCC(=O)Nc1cc2c(cc1CNCC1CC1)OCO2",
    "Int-B1":   "Nc1cc2c(cc1C3OCCO3)OCO2",
    "Int-B2":   "C=CC(=O)Nc1cc2c(cc1C3OCCO3)OCO2",
    "Int-B3":   "O=C(CCNCC1CC1)Nc1cc2c(cc1C3OCCO3)OCO2",
    "Int-B4":   "O=Cc1cc2c(cc1NC(=O)CCNCC3CC3)OCO2",
    "Int-C1":   "OCc1cc2c(cc1Br)OCO2",
    "Int-C2":   "ClCc1cc2c(cc1Br)OCO2",
    "Int-C3":   "Brc1cc2c(cc1CNCC1CC1)OCO2",
    "Int-C4":   "CC(C)(C)OC(=O)NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1",
    "Int-C5":   "NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1",
}

mols = {}
for k, s in smiles.items():
    m = Chem.MolFromSmiles(s)
    AllChem.Compute2DCoords(m)
    mols[k] = m

# Write individual .mol then convert to .cdxml via obabel
cdxml_ok, cdxml_fail = [], []
for name, mol in mols.items():
    mol_path  = f"/tmp/{name}.mol"
    cdxml_path = f"chemdraw_export/cdxml/{name}.cdxml"
    mol.SetProp("_Name", name)
    with open(mol_path, "w") as f:
        f.write(Chem.MolToMolBlock(mol))
    r = subprocess.run(
        ["obabel", mol_path, "-O", cdxml_path, "--gen2D"],
        capture_output=True, text=True
    )
    if os.path.exists(cdxml_path) and os.path.getsize(cdxml_path) > 0:
        cdxml_ok.append(name)
    else:
        cdxml_fail.append((name, r.stderr.strip()))

print(f"CDXML: {len(cdxml_ok)} OK  |  {len(cdxml_fail)} FAILED: {cdxml_fail}")
