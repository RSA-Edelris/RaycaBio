
from rdkit import Chem
from rdkit.Chem import Descriptors
import pandas as pd
from collections import defaultdict

suppl = Chem.SDMolSupplier(
    '/home/ubuntu/rayca-artifacts/faa585e0ffd53b0a98ea5bca/files/HTE_Edelris_2.sdf',
    removeHs=False
)
mols2 = [m for m in suppl if m is not None]
print(f"Total molecules: {len(mols2)}")

all_props = set()
for m in mols2:
    all_props.update(m.GetPropsAsDict().keys())
print(f"Properties: {sorted(all_props)}\n")

records = []
for i, m in enumerate(mols2):
    props = m.GetPropsAsDict()
    smi = Chem.MolToSmiles(m)
    records.append({
        'idx': i,
        'name': props.get('MOL_NAME', ''),
        'cas':  props.get('CAS_NUMBER', ''),
        'role': props.get('Role', ''),
        'smiles': smi,
        'mw': round(Descriptors.MolWt(m), 1)
    })

df2 = pd.DataFrame(records)
print(df2[['idx','name','smiles','mw']].to_string())
