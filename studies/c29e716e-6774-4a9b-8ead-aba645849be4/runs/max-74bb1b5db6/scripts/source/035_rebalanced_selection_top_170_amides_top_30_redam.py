
# Rebalanced selection: top 170 amides + top 30 RedAm (by similarity)
amide_pool = prod_df[prod_df['rxn_type']=='amide'].copy()
amine_pool = prod_df[prod_df['rxn_type']=='amine'].copy()

def diverse_select(pool, n, max_per_r1=3, max_per_r2=4):
    r1_c, r2_c = {}, {}
    sel = []
    for _, row in pool.iterrows():
        if len(sel) >= n: break
        r1, r2 = row['r1_smi'], row['r2_smi']
        r1_c.setdefault(r1, 0); r2_c.setdefault(r2, 0)
        if r1_c[r1] >= max_per_r1: continue
        if r2_c[r2] >= max_per_r2: continue
        r1_c[r1] += 1; r2_c[r2] += 1
        sel.append(row)
    return pd.DataFrame(sel)

amide_sel = diverse_select(amide_pool, 170, max_per_r1=3, max_per_r2=4)
amine_sel = diverse_select(amine_pool,  30, max_per_r1=2, max_per_r2=3)

sel_df = pd.concat([amide_sel, amine_sel], ignore_index=True)
sel_df = sel_df.sort_values('asms_sim', ascending=False).reset_index(drop=True)
sel_df['compound_id'] = [f'LIB{i+1:03d}' for i in range(len(sel_df))]

print(f"Final library: {len(sel_df)}")
print(f"Amide/Amine: {sel_df['rxn_type'].value_counts().to_dict()}")
print(f"Unique R1: {sel_df['r1_smi'].nunique()}, Unique R2: {sel_df['r2_smi'].nunique()}")
print(f"ASMS sim: min={sel_df['asms_sim'].min():.3f}, mean={sel_df['asms_sim'].mean():.3f}")
print(f"MW: {sel_df['MW'].min():.0f}–{sel_df['MW'].max():.0f} (mean {sel_df['MW'].mean():.0f})")
print(f"LogP: {sel_df['LogP'].min():.1f}–{sel_df['LogP'].max():.1f}")
print(f"\nTop 10 compounds:")
print(sel_df[['compound_id','smiles','rxn_type','MW','LogP','asms_sim']].head(10).to_string())
