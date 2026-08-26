
from rdkit import Chem
from rdkit.Chem import SDMolSupplier, Descriptors
import pandas as pd

files = {
    'acyl_cl_38':   '/home/ubuntu/rayca-artifacts/01def6985d02e054243c1afc/files/05-Amidation_Amine_Acyl_chloride_38_unique_vs_acids.sdf',
    'acyl_cl_70':   '/home/ubuntu/rayca-artifacts/01def6985d02e054243c1afc/files/05-Amidation_Amine_Acyl_chloride_70.sdf',
    'redAm_ald_169':'/home/ubuntu/rayca-artifacts/01def6985d02e054243c1afc/files/01_RedAm_Amine_Aldehyde_169_PSR60-NBoc.sdf',
    'amid_acid_353':'/home/ubuntu/rayca-artifacts/01def6985d02e054243c1afc/files/03-Amidation_Amine_Acid_353_PSR70-NBoc.sdf',
    'acid_amine_140':'/home/ubuntu/rayca-artifacts/01def6985d02e054243c1afc/files/04-Amidation_Acid_Amine _140.sdf',
}

def load_sdf(path, label):
    suppl = SDMolSupplier(path, sanitize=True, removeHs=True)
    rows = []
    for mol in suppl:
        if mol is None: continue
        props = mol.GetPropsAsDict()
        props['Mol'] = mol
        props['SMILES'] = Chem.MolToSmiles(mol)
        props['_source'] = label
        rows.append(props)
    df = pd.DataFrame(rows)
    print(f"{label}: {len(df)} mols | cols: {[c for c in df.columns if c not in ('Mol','SMILES','_source')][:8]}")
    return df

dfs = {k: load_sdf(v, k) for k, v in files.items()}
