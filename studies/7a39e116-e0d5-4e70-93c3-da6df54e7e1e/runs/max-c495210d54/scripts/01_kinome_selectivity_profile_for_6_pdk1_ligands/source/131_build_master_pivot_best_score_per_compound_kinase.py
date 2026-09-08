
# Build master pivot: best score per (compound, kinase)
pivot = (df_all
         .groupby(["compound","Kinase"])["avg_score"]
         .max()
         .unstack("Kinase"))

compounds = ["BX912","EL2003A","EL2003A-A2U1","EL2003A-A4U1","EL5001A","EL5003A"]
pivot = pivot.reindex(compounds)

# Kinase summary stats
kin_mean = pivot.mean()
kin_std  = pivot.std()
kin_cv   = kin_std / kin_mean   # coefficient of variation

# PDK1 mean as reference
pdk1_mean = kin_mean["PDK1"]
print(f"PDK1 mean pIC50 across 6 compounds: {pdk1_mean:.2f}")

# All off-targets sorted by mean score descending
offtargets = kin_mean.drop("PDK1").sort_values(ascending=False)
print("\nAll kinases by mean pIC50 (6 compounds):")
summary = pd.DataFrame({
    "mean_pIC50": kin_mean.drop("PDK1"),
    "std":        kin_std.drop("PDK1"),
    "cv":         kin_cv.drop("PDK1"),
    "delta_vs_PDK1": kin_mean.drop("PDK1") - pdk1_mean,
}).sort_values("mean_pIC50", ascending=False)
print(summary.round(3).to_string())
