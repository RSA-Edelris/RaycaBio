
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
import os

sdf_path = "/home/ubuntu/rayca-artifacts/fec3a540149a0d0fc51a148c/files/Sorted_Cedilla.sdf"
print(f"File size: {os.path.getsize(sdf_path)/1024:.1f} KB")

suppl = Chem.SDMolSupplier(sdf_path, removeHs=False, sanitize=True)
mols = [m for m in suppl if m is not None]
failed = sum(1 for m in suppl if m is None)

print(f"Molecules loaded: {len(mols)}, failed: {failed}")

for i, mol in enumerate(mols):
    name = mol.GetProp('_Name') if mol.HasProp('_Name') else f'mol_{i}'
    mw = Descriptors.MolWt(mol)
    smi = Chem.MolToSmiles(mol)
    nc = Chem.GetFormalCharge(mol)
    print(f"  {i+1:3d}. {name:50s}  MW={mw:7.1f}  q={nc:+d}  SMILES={smi[:80]}")
