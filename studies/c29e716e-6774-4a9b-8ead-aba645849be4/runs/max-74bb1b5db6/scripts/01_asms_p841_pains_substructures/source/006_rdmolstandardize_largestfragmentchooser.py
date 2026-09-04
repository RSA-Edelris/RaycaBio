
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem import inchi as rdInchi, Descriptors

lfc = rdMolStandardize.LargestFragmentChooser()
uncharger = rdMolStandardize.Uncharger()
te = rdMolStandardize.TautomerEnumerator()

def standardize_mol(mol):
    if mol is None:
        return None, ['parse_error']
    flags = []
    try:
        # Largest fragment (salt removal)
        n_before = mol.GetNumAtoms()
        mol2 = lfc.choose(mol)
        if mol2.GetNumAtoms() != n_before:
            flags.append('salt_stripped')
        # Cleanup valence/charge
        mol3 = rdMolStandardize.Cleanup(mol2)
        # Uncharge
        mol4 = uncharger.uncharge(mol3)
        # Canonical tautomer
        mol5 = te.Canonicalize(mol4)
        return mol5, flags
    except Exception as e:
        return mol, [f'std_error:{e}']

results = []
for row in df.itertuples():
    mol = row.Mol
    std_mol, flags = standardize_mol(mol)
    if std_mol is not None:
        smi = Chem.MolToSmiles(std_mol, canonical=True)
        inchi_key = rdInchi.MolToInchiKey(std_mol) or ''
        mw = Descriptors.MolWt(std_mol)
        hbd = Descriptors.NumHDonors(std_mol)
        hba = Descriptors.NumHAcceptors(std_mol)
        logp = Descriptors.MolLogP(std_mol)
        rotb = Descriptors.NumRotatableBonds(std_mol)
        rings = std_mol.GetRingInfo().NumRings()
        arom_rings = sum(1 for ring in std_mol.GetRingInfo().AtomRings() 
                        if all(std_mol.GetAtomWithIdx(a).GetIsAromatic() for a in ring))
    else:
        smi = inchi_key = ''
        mw = hbd = hba = logp = rotb = rings = arom_rings = None
    results.append({'std_flags': '|'.join(flags), 'can_smiles': smi,
                    'inchi_key': inchi_key, 'MW': mw, 'HBD': hbd, 'HBA': hba,
                    'LogP': logp, 'RotB': rotb, 'Rings': rings, 'AromRings': arom_rings,
                    'std_mol': std_mol})

std_df = pd.DataFrame(results)
df = pd.concat([df.reset_index(drop=True), std_df], axis=1)
print(f"Done. Salt-stripped: {df['std_flags'].str.contains('salt_stripped').sum()}")
print(f"Errors: {df['std_flags'].str.contains('error').sum()}")
print(f"Actives: {(df['HIT P841']=='Active').sum()}")
