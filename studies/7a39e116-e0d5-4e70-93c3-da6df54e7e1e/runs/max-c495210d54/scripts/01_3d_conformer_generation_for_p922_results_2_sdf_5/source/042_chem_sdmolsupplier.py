
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions
import os

sdf_path = '/home/ubuntu/rayca-artifacts/cacaa3ede77705c5b065320a/files/P922_Results_2.sdf'
suppl = Chem.SDMolSupplier(sdf_path, removeHs=False, sanitize=True)
mols = [m for m in suppl if m is not None]
print(f"Loaded {len(mols)} molecules\n")

stereo_summary = []

for mol in mols:
    name = mol.GetProp('_Name') if mol.HasProp('_Name') else 'unnamed'
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    chiral = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
    unspec = [(i, s) for i, s in chiral if s == '?']
    spec   = [(i, s) for i, s in chiral if s != '?']
    smiles = Chem.MolToSmiles(mol)
    stereo_summary.append({
        'name': name, 'chiral': chiral, 'unspec': unspec, 'spec': spec, 'smiles': smiles
    })
    print(f"{name}")
    print(f"  SMILES: {smiles}")
    print(f"  All chiral centers: {chiral}")
    print(f"  Specified (R/S): {spec}")
    print(f"  Unspecified (racemic '?'): {unspec}")
    print()
