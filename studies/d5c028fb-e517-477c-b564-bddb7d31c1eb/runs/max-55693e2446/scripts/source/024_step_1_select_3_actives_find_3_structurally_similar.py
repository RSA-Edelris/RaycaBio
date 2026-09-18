
# Step 1: Select 3 actives + find 3 structurally similar inactives from ASMS.sdf

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, AllChem, Descriptors
import numpy as np

SDF_PATH = '/home/ubuntu/rayca-artifacts/58e70b8d6c265c53a41c3467/files/ASMS.sdf'

# Load all compounds, keeping SMILES for speed
print("Loading ASMS.sdf …")
actives_data, inactives_data = [], []
supp = Chem.SDMolSupplier(SDF_PATH, removeHs=True, sanitize=True)
for m in supp:
    if m is None:
        continue
    hit = m.GetProp('HIT P841') if m.HasProp('HIT P841') else ''
    cid = m.GetProp('_Name') if m.HasProp('_Name') else ''
    smi = Chem.MolToSmiles(m)
    try:
        as_r = float(m.GetProp('AS_ratio')) if m.HasProp('AS_ratio') else 0.0
    except ValueError:
        as_r = 0.0
    if hit == 'Active':
        actives_data.append((cid, smi, as_r, m))
    else:
        inactives_data.append((cid, smi, m))

actives_data.sort(key=lambda x: -x[2])
print(f"Actives: {len(actives_data)}, Inactives: {len(inactives_data)}")

# Pick 3 actives: highest AS ratio, smallest MW (EDS00444974), best docking
target_actives = ['EDS00495858', 'EDS00480994', 'EDS00444974']
sel_actives = [(c,s,r,m) for c,s,r,m in actives_data if c in target_actives]
print("\nSelected actives:")
for c,s,r,m in sel_actives:
    print(f"  {c}  AS={r:.4f}  MW={Descriptors.ExactMolWt(m):.0f}  {s[:60]}")
