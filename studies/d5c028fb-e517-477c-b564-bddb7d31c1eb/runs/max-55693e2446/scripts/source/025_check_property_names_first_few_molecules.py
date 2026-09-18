
# Check property names on the first few molecules
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, AllChem, Descriptors, DataStructs
import numpy as np

# Check existing session data first
print("All_cpds type:", type(all_cpds) if 'all_cpds' in dir() else "not in scope")

# Check what properties the first active has from raw SDF
SDF_PATH = '/home/ubuntu/rayca-artifacts/58e70b8d6c265c53a41c3467/files/ASMS.sdf'
supp2 = Chem.SDMolSupplier(SDF_PATH, removeHs=True, sanitize=True)
for m in supp2:
    if m is None:
        continue
    props = m.GetPropsAsDict()
    print("First mol props:", list(props.keys()))
    print("Values:", {k:v for k,v in props.items()})
    break
