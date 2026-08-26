
# Step 5: Investigate CTX-1019480 vs EDS00490706 discordance + ADME landscape
ctx_row = ced_df[ced_df['Molecule Name']=='CTX-1019480'].iloc[0]
eds_row = asms_df[asms_df['EDS_Number']=='EDS00490706'].iloc[0]

print("EDS00490706 (ASMS rank 468, AS=0.0012):")
print(f"  SMILES: {eds_row['can_smiles']}")
print(f"  MW={eds_row['MW']:.0f}, LogP={eds_row['LogP']:.2f}")

print(f"\nCTX-1019480 (pIC50=6.37, IC50=430nM):")
print(f"  SMILES: {ctx_row['can_smiles']}")
print(f"  MW={ctx_row['MW']:.0f}, LogP={ctx_row['LogP']:.2f}")
print(f"  Solubility: {ctx_row.get('Pharmaron Solubility (PBS, pH 7.4): Aqueous Solubility - Batch Mean (uM)', 'N/A')}")
print(f"  RLM t1/2: {ctx_row.get('RLM: t1/2 - Batch Mean (Min)', 'N/A')}")
print(f"  HLM t1/2: {ctx_row.get('HLM: t1/2 - Batch Mean (Min)', 'N/A')}")

# ADME landscape across all Cedilla compounds
adme_cols = {
    'RLM_t12': 'RLM: t1/2 - Batch Mean (Min)',
    'HLM_t12': 'HLM: t1/2 - Batch Mean (Min)',
    'RLM_ER':  'RLM: ER (Hepatic extraction ratio) - Batch Mean',
    'HLM_ER':  'HLM: ER (Hepatic extraction ratio) - Batch Mean',
    'Sol':     'Pharmaron Solubility (PBS, pH 7.4): Aqueous Solubility - Batch Mean (uM)',
    'MDCK_AB': 'MDCK-WT 4% BSA: Papp (A-B) - Batch Mean (10-6, cm/s)',
    'Efflux':  'MDCK-WT 4% BSA: Efflux Ratio - Batch Mean',
}
for short, col in adme_cols.items():
    vals = pd.to_numeric(ced_df[col], errors='coerce').dropna()
    if len(vals):
        print(f"\n{short} (n={len(vals)}): mean={vals.mean():.2f}, median={vals.median():.2f}, min={vals.min():.2f}, max={vals.max():.2f}")

# Among top 30 by pIC50, ADME profile
ced_df['pIC50_num'] = pd.to_numeric(ced_df['pIC50'], errors='coerce')
top30 = ced_df.nlargest(30,'pIC50_num')
print(f"\nTop-30 Cedilla ADME summary:")
for short, col in adme_cols.items():
    vals = pd.to_numeric(top30[col], errors='coerce').dropna()
    if len(vals):
        print(f"  {short}: n={len(vals)}, mean={vals.mean():.2f}, median={vals.median():.2f}")
