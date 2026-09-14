
# V3000 might need special handling; try with sanitize=False first, then check version
from rdkit import Chem
print("RDKit version:", Chem.rdBase.rdkitVersion)

sdf_path = "/home/ubuntu/rayca-artifacts/1320c8c41b74f89c8a917762/files/Protacs.sdf"

# Try ForwardSDMolSupplier which handles V3000
with open(sdf_path, 'rb') as f:
    suppl = Chem.ForwardSDMolSupplier(f, removeHs=True, sanitize=False)
    mols = []
    for mol in suppl:
        if mol is not None:
            try:
                Chem.SanitizeMol(mol)
                mols.append(mol)
            except Exception as e:
                print(f"Sanitize error: {e}")
                mols.append(mol)

print(f"Parsed {len(mols)} molecules")
for mol in mols:
    name = mol.GetProp("_Name").strip() if mol.HasProp("_Name") else "?"
    print(name, mol.GetNumHeavyAtoms())
