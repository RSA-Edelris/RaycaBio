
from rdkit import Chem

raw_smiles = "OC=1C=C2C([C@H]([C@H](CC2)C3=CC=CC=C3)C4=CC=C(C=C4)N5CCC(CN6CCN(CC6)C=7C=C8C(=CC7)C(=O)N(C8)[C@@H]9C(=O)NC(=O)CC9)CC5)=CC1"

mol = Chem.MolFromSmiles(raw_smiles)
if mol is None:
    print("ERROR: RDKit could not parse the SMILES")
else:
    canonical = Chem.MolToSmiles(mol)
    print("Parsed OK, heavy atoms:", mol.GetNumHeavyAtoms())
    print("Canonical SMILES:", canonical)
