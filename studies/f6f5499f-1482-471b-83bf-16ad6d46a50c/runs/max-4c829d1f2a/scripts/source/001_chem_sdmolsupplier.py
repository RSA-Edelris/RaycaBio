
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
import pandas as pd

suppl = Chem.SDMolSupplier('/home/ubuntu/rayca-artifacts/faa585e0ffd53b0a98ea5bca/files/HTE_Edelris.sdf', removeHs=False)
mols = [m for m in suppl if m is not None]
print(f"Total molecules: {len(mols)}")

# Get all property names
all_props = set()
for m in mols:
    all_props.update(m.GetPropsAsDict().keys())
print(f"\nProperties available: {sorted(all_props)}")
