
from rdkit import Chem

# Strip stereo slashes from B54 SMILES — the /C=C/ notation caused the
# tool framework to misinterpret the SMILES string as a file path
b54_smi_stereo = "O=C(Nc1nc(/C=C/c2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1"
mol = Chem.MolFromSmiles(b54_smi_stereo)
b54_canon = Chem.MolToSmiles(mol, isomericSmiles=False)
print(f"Original:  {b54_smi_stereo}")
print(f"Canonical: {b54_canon}")
print(f"Slashes present: {'/' in b54_canon}")
