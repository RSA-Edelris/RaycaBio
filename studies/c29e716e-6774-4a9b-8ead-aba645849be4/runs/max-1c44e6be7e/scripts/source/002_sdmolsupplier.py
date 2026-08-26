
from rdkit import Chem
from rdkit.Chem import SDMolSupplier
import pandas as pd

sdf_path = "/home/ubuntu/rayca-artifacts/11507a0e2f5e69d5dfa40a62/files/ASMS.sdf"

suppl = SDMolSupplier(sdf_path, sanitize=True, removeHs=True)
rows = []
for mol in suppl:
    if mol is None:
        rows.append({'Mol': None, '_parse_error': True})
        continue
    props = mol.GetPropsAsDict()
    props['Mol'] = mol
    rows.append(props)

df = pd.DataFrame(rows)
print(f"Total: {len(df)}  |  Parse errors: {df['_parse_error'].sum() if '_parse_error' in df.columns else 0}")
print(f"Columns: {list(df.columns)}")
