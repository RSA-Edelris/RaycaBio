
# Exact match by InChIKey
exact = lib_df[lib_df['inchi_key'].isin(set(ced_df['inchi_key']))]
print(f"Exact InChIKey matches: {len(exact)}")

if len(exact):
    # Merge to get Cedilla info
    merged = exact.merge(ced_df[['inchi_key','Molecule Name','pIC50','Pharmaron ADPGLO (CDK2/E1-25C): IC50 - Batch Mean (uM)']],
                         on='inchi_key', how='left')
    print(merged[['Compound_ID','inchi_key','can_smiles','Priority_tier','pIC50']].to_string())
else:
    print("No exact matches. Running near-duplicate check (Tanimoto ≥0.85)...")
    from rdkit.Chem import AllChem, DataStructs
    
    lib_fps = [AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(s), 2, 2048) 
               for s in lib_df['can_smiles']]
    ced_fps = [AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(s), 2, 2048) 
               for s in ced_df['can_smiles']]
    
    near_dups = []
    for i, (lfp, lrow) in enumerate(zip(lib_fps, lib_df.itertuples())):
        sims = DataStructs.BulkTanimotoSimilarity(lfp, ced_fps)
        best_j = max(range(len(sims)), key=lambda j: sims[j])
        best_sim = sims[best_j]
        if best_sim >= 0.85:
            crow = ced_df.iloc[best_j]
            near_dups.append({
                'lib_id': lrow.Compound_ID,
                'lib_smiles': lrow.can_smiles,
                'ced_name': crow['Molecule Name'],
                'ced_smiles': crow['can_smiles'],
                'tanimoto': round(best_sim, 3),
                'ced_pIC50': crow.get('pIC50','')
            })
    
    nd_df = pd.DataFrame(near_dups).sort_values('tanimoto', ascending=False)
    print(f"Near-duplicates (Tc ≥0.85): {len(nd_df)}")
    if len(nd_df):
        print(nd_df.to_string(index=False))
