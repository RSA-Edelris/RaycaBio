
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors

sdf_path = "/home/ubuntu/rayca-artifacts/1320c8c41b74f89c8a917762/files/Protacs.sdf"
suppl = Chem.SDMolSupplier(sdf_path, removeHs=True)

results = []
for mol in suppl:
    if mol is None:
        results.append(("NONE", "PARSE_ERROR", 0, 0))
        continue
    name = mol.GetProp("_Name").strip() if mol.HasProp("_Name") else "?"
    smiles = Chem.MolToSmiles(mol, canonical=True)
    ha = mol.GetNumHeavyAtoms()
    bonds = mol.GetNumBonds()
    results.append((name, smiles, ha, bonds))

for name, smi, ha, bonds in results:
    print(f"NAME: {name}")
    print(f"  ATOMS: {ha}, BONDS: {bonds}")
    print(f"  SMILES: {smi}")
    print()
