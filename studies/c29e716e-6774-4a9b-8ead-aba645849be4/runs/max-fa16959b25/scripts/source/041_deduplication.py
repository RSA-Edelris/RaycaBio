
# Deduplication
print(f"Duplicates (same InChIKey): {df2.duplicated('inchi_key').sum()}")

# PAINS / Brenk
params_p = FilterCatalogParams()
params_p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A)
params_p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_B)
params_p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_C)
pains_cat = FilterCatalog(params_p)

params_b = FilterCatalogParams()
params_b.AddCatalog(FilterCatalogParams.FilterCatalogs.BRENK)
brenk_cat = FilterCatalog(params_b)

def get_flags(mol):
    if mol is None: return '', ''
    p = pains_cat.GetFirstMatch(mol)
    b = brenk_cat.GetFirstMatch(mol)
    return (p.GetDescription() if p else ''), (b.GetDescription() if b else '')

df2['pains_flag'], df2['brenk_flag'] = zip(*df2['std_mol'].apply(get_flags))
print(f"PAINS hits: {(df2['pains_flag']!='').sum()}")
print(f"Brenk hits: {(df2['brenk_flag']!='').sum()}")
print()
print("PAINS detail:")
print(df2[df2['pains_flag']!=''][['Molecule Name','Serie','pIC50_num','pains_flag']].to_string())
print("\nBrenk detail:")
print(df2[df2['brenk_flag']!=''][['Molecule Name','Serie','pIC50_num','brenk_flag']].to_string())
