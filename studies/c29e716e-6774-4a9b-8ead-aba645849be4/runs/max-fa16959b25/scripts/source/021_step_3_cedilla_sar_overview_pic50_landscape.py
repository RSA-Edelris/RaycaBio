
# Step 3: Cedilla SAR overview + pIC50 landscape
ced_pic50 = pd.to_numeric(ced_df['pIC50'], errors='coerce')
print("Cedilla pIC50 distribution:")
print(ced_pic50.describe())
print(f"\nCompounds with pIC50 data: {ced_pic50.notna().sum()}/267")
print(f"pIC50 >= 7 (IC50 <= 100 nM): {(ced_pic50>=7).sum()}")
print(f"pIC50 6–7  (100–1000 nM):     {((ced_pic50>=6)&(ced_pic50<7)).sum()}")
print(f"pIC50 5–6  (1–10 uM):         {((ced_pic50>=5)&(ced_pic50<6)).sum()}")
print(f"pIC50 < 5  (> 10 uM):         {(ced_pic50<5).sum()}")

# Top 10 Cedilla compounds by pIC50
top_ced = ced_df[ced_pic50.notna()].assign(pIC50_num=ced_pic50).nlargest(10,'pIC50_num')
print("\nTop 10 Cedilla by pIC50:")
cols = ['Molecule Name','pIC50_num','MW','LogP','pains','brenk',
        'Pharmaron Caliper Assay (CDK2/CCNE1): IC50 - Batch Mean (uM)']
print(top_ced[cols].to_string(index=False))

# The bridge compound
bridge = ced_df[ced_df['Molecule Name']=='CTX-1017233']
print("\n--- Bridge compound CTX-1017233 = EDS00480994 ---")
for col in ced_df.columns:
    val = bridge[col].iloc[0]
    if val and str(val).strip() and col not in ('Mol','std_mol','can_smiles','inchi_key'):
        print(f"  {col}: {val}")
