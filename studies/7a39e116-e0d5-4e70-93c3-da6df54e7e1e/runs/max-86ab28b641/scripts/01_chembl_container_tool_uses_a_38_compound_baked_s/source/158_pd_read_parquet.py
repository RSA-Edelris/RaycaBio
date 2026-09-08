
import pandas as pd, numpy as np, pickle
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# ── Check AurA specifically ───────────────────────────────────────────────────
df_full = pd.read_parquet(f"{WS}/chembl_activities_raw.parquet")
aura_mask = df_full["target_pref_name"].fillna("").str.contains("aurora", case=False)
print("AurA rows in raw data:", aura_mask.sum())
print(df_full[aura_mask][["molecule_chembl_id","target_pref_name","standard_type",
                            "standard_value","standard_units"]].to_string())

# ── Check for KinomeScan / DiscoverX assay descriptions ─────────────────────
assay_desc_col = [c for c in df_full.columns if "desc" in c.lower() or "assay" in c.lower()]
print("\nAssay-related columns:", assay_desc_col)

for col in assay_desc_col:
    ks_mask = df_full[col].fillna("").str.contains("KinomeScan|DiscoverX|PKIS|kinase scan", case=False, na=False)
    if ks_mask.any():
        print(f"\nKinomeScan entries in '{col}':")
        print(df_full[ks_mask][[col,"molecule_chembl_id","target_pref_name",
                                 "standard_type","standard_value"]].head(10).to_string())
