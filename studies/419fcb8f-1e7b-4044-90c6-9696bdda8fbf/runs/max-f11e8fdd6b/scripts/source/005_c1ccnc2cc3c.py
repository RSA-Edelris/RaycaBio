
from rdkit import Chem
from rdkit.Chem import Draw, AllChem
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import rdMolDescriptors
import os

compounds = {
    "Target": "O=C1CCNc2cc3c(cc2CN1CC1CC1)OCO3",
    "SM-1 2-nitropiperonal": "O=Cc1cc2c(cc1[N+](=O)[O-])OCO2",
    "SM-2 CpCH2NH2": "NCC1CC1",
    "SM-4 N-Boc-bAla": "CC(C)(C)OC(=O)NCCC(=O)O",
    "SM-6 2-aminopiperonal": "O=Cc1cc2c(cc1N)OCO2",
    "SM-7 2-bromopiperonal": "O=Cc1cc2c(cc1Br)OCO2",
    "Piperonal SM-1star": "O=Cc1ccc2c(c1)OCO2",
    "Int-A1 reductive-am": "O=[N+]([O-])c1cc2c(cc1CNCC1CC1)OCO2",
    "Int-A2 N-Boc": "CC(C)(C)OC(=O)N(Cc1cc2c(cc1[N+](=O)[O-])OCO2)CC1CC1",
    "Int-A3 aniline": "CC(C)(C)OC(=O)N(Cc1cc2c(cc1N)OCO2)CC1CC1",
    "Int-A4 amide": "CC(C)(C)OC(=O)NCCC(=O)Nc1cc2c(cc1CN(CC3CC3)C(=O)OC(C)(C)C)OCO2",
    "Int-A5 open-chain": "NCCC(=O)Nc1cc2c(cc1CNCC1CC1)OCO2",
    "Int-B1 acetal": "Nc1cc2c(cc1C3OCCO3)OCO2",
    "Int-B2 acrylamide": "C=CC(=O)Nc1cc2c(cc1C3OCCO3)OCO2",
    "Int-B3 aza-Michael": "O=C(CCNCC1CC1)Nc1cc2c(cc1C3OCCO3)OCO2",
    "Int-B4 aldehyde-free": "O=Cc1cc2c(cc1NC(=O)CCNCC3CC3)OCO2",
    "Int-C1 BnOH": "OCc1cc2c(cc1Br)OCO2",
    "Int-C2 BnCl": "ClCc1cc2c(cc1Br)OCO2",
    "Int-C3 2nd-amine": "Brc1cc2c(cc1CNCC1CC1)OCO2",
    "Int-C4 Boc-amide": "CC(C)(C)OC(=O)NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1",
    "Int-C5 BH-precursor": "NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1",
}

mols, failed = {}, []
for name, smi in compounds.items():
    mol = Chem.MolFromSmiles(smi)
    if mol:
        AllChem.Compute2DCoords(mol)
        mol.SetProp("_Name", name)
        mols[name] = mol
    else:
        failed.append(name)

print(f"OK: {len(mols)}  FAILED: {failed}")

# Write SDF (ChemSketch imports SDF natively)
writer = Chem.SDWriter("route_structures.sdf")
for name, mol in mols.items():
    writer.write(mol)
writer.close()
print("SDF written: route_structures.sdf")
