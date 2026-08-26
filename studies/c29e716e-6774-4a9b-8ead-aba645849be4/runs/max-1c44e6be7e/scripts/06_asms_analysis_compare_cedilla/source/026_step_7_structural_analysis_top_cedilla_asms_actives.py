
# Step 7: Structural analysis of top Cedilla + ASMS actives gap analysis
# Look at top 5 Cedilla SMILES + compare to closest ASMS actives
top5_names = ['CTX-1020903','CTX-1020667','CTX-1019480','CTX-1020747','CTX-1020518','CTX-1020810','CTX-1020516']
print("Top Cedilla SMILES (for SAR analysis):")
for name in top5_names:
    row = ced_dedup[ced_dedup['Molecule Name']==name]
    if len(row):
        r = row.iloc[0]
        print(f"\n{name} | pIC50={r['pIC50_num']:.2f} | MW={r['MW']:.0f} | LogP={r['LogP']:.2f}")
        print(f"  SMILES: {r['can_smiles']}")

# EDS00495858 best ASMS hit - novelty vs program
print("\n\nEDS00495858 (top ASMS, AS=0.172, no Cedilla equivalent):")
r = asms_df[asms_df['EDS_Number']=='EDS00495858'].iloc[0]
print(f"  SMILES: {r['can_smiles']}")
print(f"  MW={r['MW']:.0f}, LogP={r['LogP']:.2f}")

# Sim to top Cedilla
from rdkit.Chem import AllChem, DataStructs
def get_fp(mol):
    return AllChem.GetMorganFingerprintAsBitVect(mol, 2, 2048) if mol else None

asms_top_fp = get_fp(asms_df[asms_df['EDS_Number']=='EDS00495858']['std_mol'].iloc[0])
for name in top5_names:
    row = ced_dedup[ced_dedup['Molecule Name']==name]
    if len(row):
        cfp = get_fp(row.iloc[0]['std_mol'])
        sim = DataStructs.TanimotoSimilarity(asms_top_fp, cfp) if cfp else 0
        print(f"  Sim(EDS00495858, {name}) = {sim:.3f}")

# What fraction of Cedilla chemical space has solubility > 10 uM?
sol_col = 'Pharmaron Solubility (PBS, pH 7.4): Aqueous Solubility - Batch Mean (uM)'
sol_vals = pd.to_numeric(ced_dedup[sol_col], errors='coerce').dropna()
print(f"\nCedilla solubility distribution (n={len(sol_vals)}):")
print(f"  > 100 uM (good): {(sol_vals>100).sum()}")
print(f"  10–100 uM (ok):  {((sol_vals>=10)&(sol_vals<=100)).sum()}")
print(f"  1–10 uM (poor):  {((sol_vals>=1)&(sol_vals<10)).sum()}")
print(f"  < 1 uM (insoluble): {(sol_vals<1).sum()}")

# pIC50 vs solubility: do potent compounds have worse solubility?
sol_known = ced_dedup[['pIC50_num',sol_col]].copy()
sol_known[sol_col] = pd.to_numeric(sol_known[sol_col], errors='coerce')
sol_known = sol_known.dropna()
corr = sol_known.corr().loc['pIC50_num', sol_col]
print(f"\nCorrelation pIC50 vs solubility: {corr:.3f}")
