
from rdkit.Chem import rdMolDescriptors, Descriptors
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

# ---- Physicochemical properties ----
def physchem(mol):
    return {
        'MW':    round(Descriptors.ExactMolWt(mol), 2),
        'cLogP': round(Descriptors.MolLogP(mol), 2),
        'HBD':   rdMolDescriptors.CalcNumHBD(mol),
        'HBA':   rdMolDescriptors.CalcNumHBA(mol),
        'TPSA':  round(rdMolDescriptors.CalcTPSA(mol), 1),
        'RotBonds': rdMolDescriptors.CalcNumRotatableBonds(mol),
        'RingCount': rdMolDescriptors.CalcNumRings(mol),
        'ArRings': rdMolDescriptors.CalcNumAromaticRings(mol),
        'HeavyAtoms': mol.GetNumHeavyAtoms(),
    }

# ---- PAINS filter (A+B+C) ----
params_pains = FilterCatalogParams()
params_pains.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A)
params_pains.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_B)
params_pains.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_C)
pains_cat = FilterCatalog(params_pains)

# ---- BRENK (reactive/unwanted) filter ----
params_brenk = FilterCatalogParams()
params_brenk.AddCatalog(FilterCatalogParams.FilterCatalogs.BRENK)
brenk_cat = FilterCatalog(params_brenk)

# ---- NIH filter ----
params_nih = FilterCatalogParams()
params_nih.AddCatalog(FilterCatalogParams.FilterCatalogs.NIH)
nih_cat = FilterCatalog(params_nih)

# ---- Known aggregator substructures (rule-based) ----
# Common aggregators: long alkyl chains, polyaromatics, amphiphilics
aggregator_smarts = [
    ('[CH2][CH2][CH2][CH2][CH2][CH2][CH2][CH2]', 'long_alkyl_chain_C8+'),
    ('c1cc2ccc3cccc4ccc(c1)c2c34',               'pyrene_scaffold'),
    ('c1ccc2c(c1)ccc1ccccc12',                    'anthracene'),
    ('c1ccc2c(c1)cccc2',                           'naphthalene'),
    ('[NH2+]',                                     'ammonium_quaternary'),
]
agg_pats = [(Chem.MolFromSmarts(s), name) for s, name in aggregator_smarts if Chem.MolFromSmarts(s)]

# ---- Reactive substructures ----
reactive_smarts = [
    ('[C;!R](=O)[F,Cl,Br,I]',      'acid_halide'),
    ('[CX3](=O)[OX2][CX3](=O)',     'anhydride'),
    ('[N;!R]=[N+]=[N-]',            'azide'),
    ('C1OC1',                        'epoxide'),
    ('[N;!R]=[C;!R]=O',              'isocyanate'),
    ('[N;!R]=[C;!R]=S',              'isothiocyanate'),
    ('[CX3]=[CX3][CX3]=O',          'michael_acceptor_vinyl_ketone'),
    ('[CX3]=[CX3][CX3]=S',          'michael_acceptor_vinyl_thione'),
    ('[S;X2][S;X2]',                 'disulfide'),
    ('[O;X2][O;X2]',                 'peroxide'),
    ('[C;!R]=[C;!R][C;!R](=O)[O;H]','alpha_beta_unsatd_acid'),
    ('[CX4][F,Cl,Br,I]',            'alkyl_halide'),
    ('[c][F,Cl,Br,I]',              'aryl_halide'),  # note: aryl halides can be reactive but also just substituted arenes
    ('[N;R0][N;R0]',                 'hydrazine_aliphatic'),
    ('[OH][OH]',                     'hydroxylamine_peroxide'),
    ('[CX3](=O)[OX2H]',             'carboxylic_acid'),  # not reactive per se but note
]
react_pats = [(Chem.MolFromSmarts(s), name) for s, name in reactive_smarts if Chem.MolFromSmarts(s)]

# ---- Assess each active ----
print(f"{'ID':<14} {'MW':>6} {'cLogP':>6} {'HBD':>4} {'HBA':>4} {'TPSA':>6} {'Rot':>4} {'Rings':>6} PAINS  BRENK NIH  REACT/AGG")
print("-"*120)

results = []
for r in std_actives:
    mol = r['mol']
    pc = physchem(mol)
    
    # PAINS
    pains_matches = list(pains_cat.GetMatches(mol))
    pains_str = '; '.join(e.GetDescription() for e in pains_matches) if pains_matches else '-'
    
    # BRENK
    brenk_matches = list(brenk_cat.GetMatches(mol))
    brenk_str = '; '.join(e.GetDescription() for e in brenk_matches) if brenk_matches else '-'
    
    # NIH
    nih_matches = list(nih_cat.GetMatches(mol))
    nih_str = '; '.join(e.GetDescription() for e in nih_matches) if nih_matches else '-'
    
    # Reactive
    react_hits = [name for pat, name in react_pats if mol.HasSubstructMatch(pat)]
    react_str = '; '.join(react_hits) if react_hits else '-'
    
    # Aggregators
    agg_hits = [name for pat, name in agg_pats if mol.HasSubstructMatch(pat)]
    agg_str = '; '.join(agg_hits) if agg_hits else '-'
    
    r['pc'] = pc
    r['pains'] = pains_str
    r['brenk'] = brenk_str
    r['nih'] = nih_str
    r['react'] = react_str
    r['agg'] = agg_str
    results.append(r)
    
    print(f"{r['EDS_Number']:<14} {pc['MW']:>6.0f} {pc['cLogP']:>6.2f} {pc['HBD']:>4} {pc['HBA']:>4} {pc['TPSA']:>6.1f} {pc['RotBonds']:>4} {pc['RingCount']:>3}/{pc['ArRings']} "
          f"P:{pains_str[:20]:20s} B:{brenk_str[:20]:20s} N:{nih_str[:8]:8s} R:{react_str}")
