
from rdkit import Chem
from rdkit.Chem import SDMolSupplier, inchi as rdInchi
import pandas as pd

lib_path = "/home/ubuntu/rayca-artifacts/01def6985d02e054243c1afc/files/002_library_200.sdf"
ced_path = "/home/ubuntu/rayca-artifacts/01def6985d02e054243c1afc/files/Cedilla_list.sdf"

def load_inchikeys(path):
    rows = []
    for mol in SDMolSupplier(path, sanitize=True, removeHs=True):
        if mol is None:
            continue
        ik = rdInchi.MolToInchiKey(mol) or ''
        smi = Chem.MolToSmiles(mol, canonical=True)
        props = mol.GetPropsAsDict()
        rows.append({'inchi_key': ik, 'can_smiles': smi, **props})
    return pd.DataFrame(rows)

lib_df = load_inchikeys(lib_path)
ced_df = load_inchikeys(ced_path)

print(f"002_library_200: {len(lib_df)} molecules")
print(f"Cedilla_list:    {len(ced_df)} molecules")
print(f"\nLib columns:     {list(lib_df.columns)}")
print(f"Cedilla columns: {list(ced_df.columns)}")
