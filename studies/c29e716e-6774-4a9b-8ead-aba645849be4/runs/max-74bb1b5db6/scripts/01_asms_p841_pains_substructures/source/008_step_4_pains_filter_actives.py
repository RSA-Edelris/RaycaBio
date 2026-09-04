
# Step 4: PAINS filter on actives
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

params_pains = FilterCatalogParams()
params_pains.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A)
params_pains.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_B)
params_pains.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_C)
pains_catalog = FilterCatalog(params_pains)

params_brenk = FilterCatalogParams()
params_brenk.AddCatalog(FilterCatalogParams.FilterCatalogs.BRENK)
brenk_catalog = FilterCatalog(params_brenk)

params_nih = FilterCatalogParams()
params_nih.AddCatalog(FilterCatalogParams.FilterCatalogs.NIH)
nih_catalog = FilterCatalog(params_nih)

def check_filters(mol):
    flags = {}
    if mol is None:
        return flags
    # PAINS
    entry = pains_catalog.GetFirstMatch(mol)
    if entry:
        flags['PAINS'] = entry.GetDescription()
    # Brenk (reactive/undesirable)
    entry = brenk_catalog.GetFirstMatch(mol)
    if entry:
        flags['Brenk'] = entry.GetDescription()
    # NIH
    entry = nih_catalog.GetFirstMatch(mol)
    if entry:
        flags['NIH'] = entry.GetDescription()
    return flags

actives['filter_flags'] = actives['std_mol'].apply(check_filters)
actives['has_PAINS'] = actives['filter_flags'].apply(lambda x: 'PAINS' in x)
actives['has_Brenk'] = actives['filter_flags'].apply(lambda x: 'Brenk' in x)
actives['has_NIH'] = actives['filter_flags'].apply(lambda x: 'NIH' in x)

print("Filter results on 15 actives:")
print(f"PAINS hits: {actives['has_PAINS'].sum()}")
print(f"Brenk hits: {actives['has_Brenk'].sum()}")
print(f"NIH hits:   {actives['has_NIH'].sum()}")
print()
for _, row in actives.iterrows():
    if row['filter_flags']:
        print(f"{row['EDS_Number']}: {row['filter_flags']}")
