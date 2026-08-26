
# Step 5: Aggregator, reactive, frequent hitter checks + ASMS-specific artefacts
from rdkit.Chem import rdMolDescriptors, Fragments
from rdkit.Chem.Draw import rdMolDraw2D

# Known aggregating substructure SMARTS (Shoichet lab aggregator markers)
aggregator_smarts = {
    'long_aliphatic_chain': '[CH2][CH2][CH2][CH2][CH2][CH2]',
    'catechol': 'c1cc(O)c(O)cc1',
    'galloyl': 'c1c(O)c(O)c(O)cc1',
    'rhodanine': 'O=C1NC(=S)SC1',
    'Michael_acceptor_enone': 'C=CC(=O)[!N]',
    'aldehyde': '[CH]=O',
    'quinone': 'O=C1C=CC(=O)C=C1',
    'epoxide': '[C@H]1O[C@@H]1',
    'acyl_halide': 'C(=O)[F,Cl,Br,I]',
    'anhydride': 'C(=O)OC(=O)',
    'isocyanate': 'N=C=O',
    'maleimide': 'O=C1CC(=O)N1',
    'thiol_reactive_disulfide': 'SSC',
    'alpha_halo_ketone': 'C(=O)C[Cl,Br,I]',
    'aniline_prone_to_oxidation': 'c1ccc(N)cc1',  # primary aniline
    'hydrazine': 'NN',
    'hydroxamic_acid': 'C(=O)NO',
    'metal_chelator_catechol': 'Oc1ccccc1O',
    'acrylate': 'C=CC(=O)O',
    'vinyl_sulfone': 'C=CS(=O)(=O)',
}

reactive_smarts = {
    'Michael_acceptor_alpha_beta': '[C;X3]=[C;X3][C;X3](=O)',
    'aldehyde': '[CX3H1](=O)',
    'epoxide': 'C1OC1',
    'acyl_halide': '[C](=O)[Cl,Br,I,F]',
    'sulfonyl_halide': 'S(=O)(=O)[Cl,Br,F]',
    'isocyanate': '[N]=[C]=[O]',
    'isothiocyanate': '[N]=[C]=[S]',
    'acid_chloride': 'C(=O)Cl',
    'nitroso': '[N]=O',
    'diazo': '[N+]#[N-]',
}

# Compile patterns
compiled_agg = {k: Chem.MolFromSmarts(v) for k, v in aggregator_smarts.items() if Chem.MolFromSmarts(v)}
compiled_rxn = {k: Chem.MolFromSmarts(v) for k, v in reactive_smarts.items() if Chem.MolFromSmarts(v)}

def check_structural_alerts(mol):
    agg_hits = [k for k, patt in compiled_agg.items() if mol.HasSubstructMatch(patt)]
    rxn_hits = [k for k, patt in compiled_rxn.items() if mol.HasSubstructMatch(patt)]
    return agg_hits, rxn_hits

actives[['agg_alerts', 'reactive_alerts']] = actives['std_mol'].apply(
    lambda m: pd.Series(check_structural_alerts(m)) if m else pd.Series([[], []])
)

# ASMS-specific artefact checks
# 1. Early eluters (RT < 1.0 min): likely very polar, may not bind specifically
# 2. AS ratio analysis: very high AS ratios may indicate aggregation or non-specific binding
# 3. Check if molecule is a potential dimer/oligomer of another compound
# 4. Colloidal aggregator prediction: MW>400 + LogP>3 + multiple aromatic rings

def aggregation_risk(row):
    """Heuristic aggregation risk for ASMS"""
    score = 0
    reasons = []
    if row['MW'] and row['MW'] > 400:
        score += 1
    if row['LogP'] and row['LogP'] > 3.0:
        score += 1
        reasons.append(f'LogP={row["LogP"]:.1f}')
    if row['AromRings'] and row['AromRings'] >= 3:
        score += 1
        reasons.append(f'{row["AromRings"]} arom rings')
    return score, reasons

actives['agg_risk_score'], actives['agg_risk_reasons'] = zip(
    *actives.apply(aggregation_risk, axis=1)
)

print("=== ACTIVE MOLECULE ARTEFACT ANALYSIS ===\n")
for _, row in actives.sort_values('Hit_rank').iterrows():
    issues = []
    if row['has_PAINS']:
        issues.append(f"PAINS:{row['filter_flags']['PAINS']}")
    if row['has_Brenk']:
        issues.append(f"Brenk:{row['filter_flags']['Brenk']}")
    if row['agg_alerts']:
        issues.append(f"AggAlert:{row['agg_alerts']}")
    if row['reactive_alerts']:
        issues.append(f"Reactive:{row['reactive_alerts']}")
    if row['agg_risk_score'] >= 2:
        issues.append(f"AggRisk(score={row['agg_risk_score']}:{row['agg_risk_reasons']})")
    
    # ASMS artefact: very low AS ratio = weak binder, check RT
    rt = float(row['RTmin']) if row['RTmin'] else None
    as_ratio = float(row['AS ratio']) if row['AS ratio'] else None
    
    print(f"{row['EDS_Number']} | rank={row['Hit_rank']} | AS={as_ratio:.4f} | RT={rt} | MW={row['MW']:.0f} | LogP={row['LogP']:.1f}")
    if issues:
        print(f"  FLAGS: {'; '.join(issues)}")
    else:
        print(f"  FLAGS: clean")
