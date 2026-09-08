
# --- Verify AurA universal claim ---
print("--- AurA across all 6 compounds ---")
aura_scores = pivot['AurA']
for compound, score in aura_scores.items():
    print(f"  {compound}: {score:.3f}")
print(f"  Min: {aura_scores.min():.3f}  Max: {aura_scores.max():.3f}  Mean: {aura_scores.mean():.3f}  CV: {aura_scores.std()/aura_scores.mean():.3f}")
universal_threshold = 6.90
print(f"  All >= {universal_threshold}? {(aura_scores >= universal_threshold).all()}")

# --- Check which other kinases meet universal threshold (>=6.90 in ALL 6) ---
print(f"\n--- Universal off-targets (pIC50 >= {universal_threshold} in ALL 6 compounds) ---")
for k in pivot.columns:
    if (pivot[k] >= universal_threshold).all():
        print(f"  {k}: min={pivot[k].min():.3f} mean={pivot[k].mean():.3f}")

# --- Top kinases by mean pIC50 ---
print("\n--- Top 12 kinases by mean pIC50 ---")
mean_scores = pivot.mean().sort_values(ascending=False)
print(f"{'Kinase':20s}  {'Mean':6s}  {'Delta_PDK1':10s}  {'CV':6s}")
pdk1_mean = pivot['PDK1'].mean()
for k, m in mean_scores.head(12).items():
    cv = pivot[k].std() / pivot[k].mean()
    print(f"  {k:20s}  {m:.3f}  {m - pdk1_mean:+.3f}       {cv:.3f}")
