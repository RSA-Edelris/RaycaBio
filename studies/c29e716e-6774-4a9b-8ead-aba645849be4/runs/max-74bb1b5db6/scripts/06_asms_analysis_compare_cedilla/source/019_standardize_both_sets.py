
# Standardize both sets
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem import inchi as rdInchi
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
import numpy as np

lfc = rdMolStandardize.LargestFragmentChooser()
uncharger = rdMolStandardize.Uncharger()
te = rdMolStandardize.TautomerEnumerator()

def standardize_and_describe(df, smiles_col):
    results = []
    for row in df.itertuples():
        mol = row.Mol
        if mol is None:
            results.append({'can_smiles':'','inchi_key':'','MW':None,'LogP':None,'HBD':None,'HBA':None,'RotB':None,'AromRings':None,'std_flags':'parse_error','std_mol':None})
            continue
        flags = []
        try:
            n_before = mol.GetNumAtoms()
            mol2 = lfc.choose(mol)
            if mol2.GetNumAtoms() != n_before: flags.append('salt_stripped')
            mol3 = rdMolStandardize.Cleanup(mol2)
            mol4 = uncharger.uncharge(mol3)
            mol5 = te.Canonicalize(mol4)
        except:
            mol5 = mol; flags.append('std_error')
        smi = Chem.MolToSmiles(mol5, canonical=True)
        ik  = rdInchi.MolToInchiKey(mol5) or ''
        mw  = Descriptors.MolWt(mol5)
        lp  = Descriptors.MolLogP(mol5)
        hbd = Descriptors.NumHDonors(mol5)
        hba = Descriptors.NumHAcceptors(mol5)
        rotb= Descriptors.NumRotatableBonds(mol5)
        ar  = sum(1 for ring in mol5.GetRingInfo().AtomRings()
                  if all(mol5.GetAtomWithIdx(a).GetIsAromatic() for a in ring))
        results.append({'can_smiles':smi,'inchi_key':ik,'MW':mw,'LogP':lp,
                        'HBD':hbd,'HBA':hba,'RotB':rotb,'AromRings':ar,
                        'std_flags':'|'.join(flags),'std_mol':mol5})
    return pd.DataFrame(results)

asms_std = standardize_and_describe(asms_df, 'Smiles')
ced_std  = standardize_and_describe(ced_df, 'SMILES')

asms_df = pd.concat([asms_df.reset_index(drop=True), asms_std], axis=1)
ced_df  = pd.concat([ced_df.reset_index(drop=True), ced_std], axis=1)

print(f"ASMS_active standardized: {len(asms_df)}  salt_stripped={asms_std['std_flags'].str.contains('salt').sum()}")
print(f"Cedilla    standardized: {len(ced_df)}  salt_stripped={ced_std['std_flags'].str.contains('salt').sum()}")

# PAINS/Brenk catalogs
params_p = FilterCatalogParams()
params_p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A)
params_p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_B)
params_p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_C)
pains_cat = FilterCatalog(params_p)
params_b = FilterCatalogParams()
params_b.AddCatalog(FilterCatalogParams.FilterCatalogs.BRENK)
brenk_cat = FilterCatalog(params_b)

def flag_mol(mol):
    if mol is None: return '', ''
    p = pains_cat.GetFirstMatch(mol)
    b = brenk_cat.GetFirstMatch(mol)
    return (p.GetDescription() if p else ''), (b.GetDescription() if b else '')

asms_df['pains'], asms_df['brenk'] = zip(*asms_df['std_mol'].apply(flag_mol))
ced_df['pains'],  ced_df['brenk']  = zip(*ced_df['std_mol'].apply(flag_mol))

print(f"\nASMS_active  PAINS:{(asms_df['pains']!='').sum()}  Brenk:{(asms_df['brenk']!='').sum()}")
print(f"Cedilla      PAINS:{(ced_df['pains']!='').sum()}    Brenk:{(ced_df['brenk']!='').sum()}")
