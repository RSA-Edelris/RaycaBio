
from rdkit.Chem import rdChemReactions

# Amidation: aliphatic NH (not amide, not aromatic) + COOH -> amide
# N idx=2 is the only eligible NH
rxn_smarts = '[NH1;!$(N-C=O);!$(N-S=O);!a:1].[C:2](=O)[OH]>>[N:1][C:2]=O'
rxn = AllChem.ReactionFromSmarts(rxn_smarts)

# Load acids with names
supplier = Chem.SDMolSupplier(acid_path, removeHs=True)
records = []   # list of dicts: mol, name, cr_id
for mol in supplier:
    if mol is None:
        continue
    name = ''
    for prop in ['Dotmatics_CR', 'Article', 'CAS', '_Name']:
        if mol.HasProp(prop):
            v = mol.GetProp(prop).strip()
            if v:
                name = v
                break
    cr_id = mol.GetProp('Dotmatics_CR') if mol.HasProp('Dotmatics_CR') else name
    records.append({'acid_mol': mol, 'acid_name': name, 'cr_id': cr_id})

print(f"Acids loaded: {len(records)}")

# Run reaction
products = []
failed = []
for rec in records:
    try:
        prods = rxn.RunReactants((amine, rec['acid_mol']))
        if not prods:
            failed.append(rec['cr_id'])
            continue
        prod = prods[0][0]
        Chem.SanitizeMol(prod)
        smi = Chem.MolToSmiles(prod)
        products.append({
            'mol': prod,
            'smiles': smi,
            'acid_name': rec['acid_name'],
            'cr_id': rec['cr_id'],
        })
    except Exception as e:
        failed.append(rec['cr_id'])

print(f"Products formed : {len(products)}")
print(f"Reaction failed : {len(failed)}")
if failed[:5]:
    print(f"  First failures: {failed[:5]}")
# Spot-check
for p in products[:3]:
    print(f"  {p['cr_id']}: {p['smiles'][:80]}")
