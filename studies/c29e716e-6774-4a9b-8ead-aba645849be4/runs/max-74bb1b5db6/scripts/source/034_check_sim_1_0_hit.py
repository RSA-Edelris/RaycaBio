
# Check the sim=1.0 hit
perfect = prod_df[prod_df['asms_sim'] == 1.0]
print("Perfect match:", perfect[['smiles','r1_smi','r2_smi','rxn_type']].to_string())

# Diversity-controlled selection: max 3 per R1, max 5 per R2
# Prioritize: high similarity, balance amide/amine, ensure diversity

r1_counts = {}
r2_counts = {}
selected = []
TARGET = 200
# Tier 1: top by similarity with diversity constraints
for _, row in prod_df.iterrows():
    if len(selected) >= TARGET:
        break
    r1 = row['r1_smi']
    r2 = row['r2_smi']
    r1_counts.setdefault(r1, 0)
    r2_counts.setdefault(r2, 0)
    # Allow max 3 per R1, max 4 per R2
    if r1_counts[r1] >= 3:
        continue
    if r2_counts[r2] >= 4:
        continue
    r1_counts[r1] += 1
    r2_counts[r2] += 1
    selected.append(row)

sel_df = pd.DataFrame(selected).reset_index(drop=True)
print(f"\nSelected: {len(sel_df)} compounds")
print(f"Unique R1 groups: {sel_df['r1_smi'].nunique()}")
print(f"Unique R2 groups: {sel_df['r2_smi'].nunique()}")
print(f"rxn_type: {sel_df['rxn_type'].value_counts().to_dict()}")
print(f"ASMS sim: min={sel_df['asms_sim'].min():.3f}, mean={sel_df['asms_sim'].mean():.3f}, max={sel_df['asms_sim'].max():.3f}")
print(f"MW: {sel_df['MW'].min():.0f}–{sel_df['MW'].max():.0f}, mean={sel_df['MW'].mean():.0f}")
print(f"LogP: {sel_df['LogP'].min():.1f}–{sel_df['LogP'].max():.1f}")
