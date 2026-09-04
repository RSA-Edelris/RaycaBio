
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem

sdf_path = '/home/ubuntu/rayca-artifacts/d11115b837f31f763731fd31/files/Projets Custom.sdf'
suppl = Chem.SDMolSupplier(sdf_path, removeHs=True)

for i, mol in enumerate(suppl):
    if mol is None:
        continue
    mw = Descriptors.MolWt(mol)
    name = mol.GetProp('_Name') if mol.HasProp('_Name') else f'cpd_{i+1}'
    smi = Chem.MolToSmiles(mol)
    print(f"[{i+1}] {name}  MW={mw:.1f}  natoms={mol.GetNumAtoms()}")
    if mw > 1000:
        print(f"  SMILES: {smi}")
        print(f"  Props: {list(mol.GetPropsAsDict().keys())}")
