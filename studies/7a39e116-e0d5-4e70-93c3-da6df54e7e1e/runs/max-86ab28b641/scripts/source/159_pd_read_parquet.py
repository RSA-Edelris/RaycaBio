
import pandas as pd, numpy as np, pickle
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# ── Rebuild cleaned kinase activity table ────────────────────────────────────
df_raw = pd.read_parquet(f"{WS}/chembl_activities_raw.parquet")
QUANT = {"IC50","Ki","Kd","EC50","pIC50","pKi"}
df = df_raw[df_raw["standard_type"].isin(QUANT)].copy()
df["standard_value"] = pd.to_numeric(df["standard_value"], errors="coerce")
df = df.dropna(subset=["standard_value"])

def to_picso(row):
    v, u, st = row["standard_value"], str(row.get("standard_units","nM")).strip().lower(), row["standard_type"]
    if st in ("pIC50","pKi"): return v
    if v <= 0: return np.nan
    mult = {"nm":1e-9,"um":1e-6,"mm":1e-3,"m":1.0}.get(u, 1e-9)
    return -np.log10(v * mult)

df["pIC50"] = df.apply(to_picso, axis=1)
df = df[(df["pIC50"] >= 3) & (df["pIC50"] <= 12)].copy()

# Kinase filter — include Aurora explicitly
kinase_kw = r"kinase|aurora|pdk|flt3|jak2|fgfr|egfr|braf|abl|btk|src|met\b|cdk|gsk3|rock|akt|mek|mapk|chk|plk|erk|p38|jnk|pkc|mtor|vegfr|kdr|ret\b|alk\b"
df_kin = df[df["target_pref_name"].fillna("").str.contains(kinase_kw, case=False, regex=True)].copy()
print(f"Kinase activities for inference: {len(df_kin)}")

# ── Tanimoto-weighted cross-target inference ──────────────────────────────────
# For each query compound, for each kinase:
#   inferred_pIC50 = sum(Tc_i * pIC50_i) / sum(Tc_i)  over all analogs with data

results = {}
for query, hits in all_hits.items():
    tc_map = {h["chembl_id"]: h["tanimoto"] for h in hits if h["tanimoto"] > 0}
    # Merge with kinase activities
    sub = df_kin[df_kin["molecule_chembl_id"].isin(tc_map)].copy()
    sub["tanimoto"] = sub["molecule_chembl_id"].map(tc_map)
    # Per-target: weighted mean + max pIC50 + n analogs
    agg = sub.groupby("target_pref_name").apply(
        lambda g: pd.Series({
            "inferred_pIC50": (g["tanimoto"] * g["pIC50"]).sum() / g["tanimoto"].sum(),
            "max_pIC50":      g["pIC50"].max(),
            "n_analogs":      g["molecule_chembl_id"].nunique(),
            "mean_Tc":        g["tanimoto"].mean(),
            "best_Tc":        g["tanimoto"].max(),
        })
    ).reset_index()
    agg = agg.sort_values("inferred_pIC50", ascending=False)
    results[query] = agg
    print(f"\n{query} — top inferred kinase off-targets:")
    print(agg[["target_pref_name","inferred_pIC50","max_pIC50","n_analogs","best_Tc"]].head(8).to_string(index=False))

import pickle
with open(f"{WS}/tanimoto_inference_results.pkl", "wb") as f:
    pickle.dump(results, f)
