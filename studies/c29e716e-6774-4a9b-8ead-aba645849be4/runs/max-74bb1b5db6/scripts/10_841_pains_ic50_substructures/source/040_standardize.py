
import numpy as np
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem import inchi as rdInchi
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

# Standardize
lfc = rdMolStandardize.LargestFragmentChooser()
uncharger = rdMolStandardize.Uncharger()
te = rdMolStandardize.TautomerEnumerator()

def standardize_mol(mol):
    if mol is None: return None, ['parse_error']
    flags = []
    try:
        n_before = mol.GetNumAtoms()
        mol2 = lfc.choose(mol)
        if mol2.GetNumAtoms() != n_before: flags.append('salt_stripped')
        mol3 = rdMolStandardize.Cleanup(mol2)
        mol4 = uncharger.uncharge(mol3)
        mol5 = te.Canonicalize(mol4)
        return mol5, flags
    except Exception as e:
        return mol, [f'std_error:{e}']

results = []
for row in df2.itertuples():
    mol = row.Mol
    std_mol, flags = standardize_mol(mol)
    if std_mol is not None:
        smi = Chem.MolToSmiles(std_mol, canonical=True)
        ik  = rdInchi.MolToInchiKey(std_mol) or ''
        mw  = Descriptors.MolWt(std_mol)
        lp  = Descriptors.MolLogP(std_mol)
        hbd = Descriptors.NumHDonors(std_mol)
        hba = Descriptors.NumHAcceptors(std_mol)
        rotb= Descriptors.NumRotatableBonds(std_mol)
        ar  = sum(1 for ring in std_mol.GetRingInfo().AtomRings()
                  if all(std_mol.GetAtomWithIdx(a).GetIsAromatic() for a in ring))
    else:
        smi=ik=''
        mw=lp=hbd=hba=rotb=ar=None
    results.append({'std_flags':'|'.join(flags),'can_smiles':smi,'inchi_key':ik,
                    'MW':mw,'LogP':lp,'HBD':hbd,'HBA':hba,'RotB':rotb,'AromRings':ar,'std_mol':std_mol})

std_df2 = pd.DataFrame(results)
df2 = pd.concat([df2.reset_index(drop=True), std_df2], axis=1)
df2['pIC50_num'] = pd.to_numeric(df2['pIC50'], errors='coerce')

print(f"Standardised: {len(df2)}")
print(f"Salt-stripped: {df2['std_flags'].str.contains('salt_stripped').sum()}")
print(f"Errors: {df2['std_flags'].str.contains('error').sum()}")
print(f"\npIC50 range: {df2['pIC50_num'].min():.3f} – {df2['pIC50_num'].max():.3f}")
print(f"pIC50 ≥8 (≤10 nM): {(df2['pIC50_num']>=8).sum()}")
print(f"pIC50 7–8 (10–100 nM): {((df2['pIC50_num']>=7)&(df2['pIC50_num']<8)).sum()}")
print(f"pIC50 6–7 (0.1–1 µM): {((df2['pIC50_num']>=6)&(df2['pIC50_num']<7)).sum()}")
print(f"pIC50 <6 (>1 µM):     {(df2['pIC50_num']<6).sum()}")
print(f"\nSeries breakdown:")
print(df2.groupby('Serie')['pIC50_num'].describe().round(3).to_string())
