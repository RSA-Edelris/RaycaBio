
from rdkit import Chem
from rdkit.Chem import SDMolSupplier, Descriptors
from rdkit.Chem import inchi as rdInchi
import pandas as pd

sdf_path = "/home/ubuntu/rayca-artifacts/01def6985d02e054243c1afc/files/Sorted_841_train.sdf"

suppl = SDMolSupplier(sdf_path, sanitize=True, removeHs=True)
rows = []
for mol in suppl:
    if mol is None:
        rows.append({'Mol': None, '_parse_error': True})
        continue
    props = mol.GetPropsAsDict()
    props['Mol'] = mol
    rows.append(props)

df2 = pd.DataFrame(rows)
print(f"Total: {len(df2)}")
print(f"Columns: {list(df2.columns)}")
for col in df2.columns:
    if col not in ['Mol', '_parse_error']:
        print(f"\n--- {col} ---")
        print(df2[col].value_counts().head(10))
