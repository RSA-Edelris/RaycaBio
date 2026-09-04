
# Enumerate all N-modified intermediates
# Pool N-reagents: acyl_cl_38 + acyl_cl_70 + amid_acid_353 → acylation; redAm_ald_169 → RedAm

def apply_rxn_single(rxn, scaffold, reagent_mol):
    """Apply reaction, return canonical SMILES or None."""
    try:
        prods = rxn.RunReactants((scaffold, reagent_mol))
        if not prods:
            return None
        p = prods[0][0]
        Chem.SanitizeMol(p)
        return Chem.MolToSmiles(p)
    except:
        return None

n_intermediates = []  # list of dicts: {smiles, reagent_smiles, rxn_type, reagent_id}

# Acylation (acyl chlorides + acids)
for src in ('acyl_cl_38', 'acyl_cl_70', 'amid_acid_353'):
    for _, row in dfs[src].iterrows():
        smi = apply_rxn_single(rxn_n_acyl, scaffold, row['Mol'])
        if smi:
            n_intermediates.append({
                'n_smi': smi,
                'r1_smi': row['SMILES'],
                'r1_id': row.get('Dotmatics_CR', ''),
                'rxn_type': 'amide',
                'r1_source': src
            })

# Reductive amination (aldehydes)
for _, row in dfs['redAm_ald_169'].iterrows():
    smi = apply_rxn_single(rxn_n_redAm, scaffold, row['Mol'])
    if smi:
        n_intermediates.append({
            'n_smi': smi,
            'r1_smi': row['SMILES'],
            'r1_id': row.get('Dotmatics_CR', ''),
            'rxn_type': 'amine',
            'r1_source': 'redAm_ald_169'
        })

print(f"N-intermediates generated: {len(n_intermediates)}")
print(f"  Amide: {sum(1 for x in n_intermediates if x['rxn_type']=='amide')}")
print(f"  Amine (RedAm): {sum(1 for x in n_intermediates if x['rxn_type']=='amine')}")

# Deduplicate by SMILES
seen = set()
n_intermediates_dedup = []
for x in n_intermediates:
    if x['n_smi'] not in seen:
        seen.add(x['n_smi'])
        n_intermediates_dedup.append(x)
print(f"After dedup: {len(n_intermediates_dedup)}")
