
# Step 2: Structure standardization — salt removal, canonical SMILES, InChI for dedup
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem import inchi as rdInchi
from rdkit.Chem import Descriptors

standardizer = rdMolStandardize.Standardizer()
salt_remover = rdMolStandardize.FragmentRemover()
uncharger = rdMolStandardize.Uncharger()
tautomer_enumerator = rdMolStandardize.TautomerEnumerator()

def standardize_mol(mol):
    """Return (std_mol, flags) where flags is list of issues."""
    if mol is None:
        return None, ['parse_error']
    flags = []
    try:
        # Remove salts / largest fragment
        mol_clean = salt_remover.remove(mol)
        if mol_clean.GetNumAtoms() != mol.GetNumAtoms():
            flags.append('salt_stripped')
        # Uncharge
        mol_uncharged = uncharger.uncharge(mol_clean)
        # Canonical tautomer
        mol_taut = tautomer_enumerator.Canonicalize(mol_uncharged)
        # Standardize
        mol_std = standardizer.standardize(mol_taut)
        return mol_std, flags
    except Exception as e:
        return mol, [f'std_error:{e}']

results = []
for i, row in df.iterrows():
    mol = row['Mol']
    std_mol, flags = standardize_mol(mol)
    if std_mol is not None:
        smi = Chem.MolToSmiles(std_mol, canonical=True)
        inchi_key = rdInchi.MolToInchiKey(std_mol) or ''
        mw = Descriptors.MolWt(std_mol)
    else:
        smi = ''
        inchi_key = ''
        mw = None
    results.append({
        'std_flags': '|'.join(flags),
        'can_smiles': smi,
        'inchi_key': inchi_key,
        'MW': mw,
        'std_mol': std_mol
    })

std_df = pd.DataFrame(results)
df = pd.concat([df.reset_index(drop=True), std_df], axis=1)

print(f"Standardized {len(df)} molecules")
print(f"Salt-stripped: {df['std_flags'].str.contains('salt_stripped').sum()}")
print(f"Errors: {df['std_flags'].str.contains('error').sum()}")
print(f"Empty SMILES: {(df['can_smiles']=='').sum()}")
