
from rdkit import Chem
from rdkit.Chem import SDMolSupplier, Descriptors
from rdkit.Chem import inchi as rdInchi
import pandas as pd

asms_path = "/home/ubuntu/rayca-artifacts/01def6985d02e054243c1afc/files/ASMS_active.sdf"
ced_path  = "/home/ubuntu/rayca-artifacts/01def6985d02e054243c1afc/files/Cedilla_list.sdf"

def load_sdf(path, label):
    suppl = SDMolSupplier(path, sanitize=True, removeHs=True)
    rows = []
    for mol in suppl:
        if mol is None:
            rows.append({'Mol': None, '_parse_error': True, '_source': label})
            continue
        props = mol.GetPropsAsDict()
        props['Mol'] = mol
        props['_source'] = label
        rows.append(props)
    return pd.DataFrame(rows)

asms_df = load_sdf(asms_path, 'ASMS_active')
ced_df  = load_sdf(ced_path,  'Cedilla')

print(f"ASMS_active: {len(asms_df)} mols")
print(f"  columns: {[c for c in asms_df.columns if c not in ('Mol','_source')]}")
for c in asms_df.columns:
    if c not in ('Mol','_source','_parse_error'):
        print(f"  {c}: {asms_df[c].iloc[0]}")

print(f"\nCedilla: {len(ced_df)} mols")
print(f"  columns: {[c for c in ced_df.columns if c not in ('Mol','_source')]}")
for c in ced_df.columns:
    if c not in ('Mol','_source','_parse_error'):
        print(f"  {c}: {ced_df[c].iloc[0] if len(ced_df) else 'N/A'}")
