
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
import os

sdf_path = "/home/ubuntu/rayca-artifacts/d11115b837f31f763731fd31/files/Projets Custom.sdf"

suppl = Chem.SDMolSupplier(sdf_path, removeHs=False, sanitize=True)

results = []
for i, mol in enumerate(suppl):
    if mol is None:
        print(f"Molecule {i+1}: PARSE FAILED")
        continue
    name = mol.GetProp('name') if mol.HasProp('name') else f"compound_{i+1}"
    try:
        smi = Chem.MolToSmiles(mol, isomericSmiles=True)
        mw = Descriptors.MolWt(mol)
        ha = mol.GetNumHeavyAtoms()
        rb = Descriptors.NumRotatableBonds(mol)
        hbd = Descriptors.NumHDonors(mol)
        hba = Descriptors.NumHAcceptors(mol)
        results.append({
            'name': name,
            'smiles': smi,
            'MW': round(mw, 1),
            'HA': ha,
            'RB': rb,
            'HBD': hbd,
            'HBA': hba,
        })
        print(f"[{i+1}] {name}  MW={mw:.1f}  HA={ha}  RB={rb}")
        print(f"     SMILES: {smi}")
        print()
    except Exception as e:
        print(f"[{i+1}] {name}: ERROR - {e}")
