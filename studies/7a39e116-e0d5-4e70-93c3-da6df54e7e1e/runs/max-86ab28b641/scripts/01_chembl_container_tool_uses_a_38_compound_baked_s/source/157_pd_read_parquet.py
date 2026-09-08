
import pandas as pd, numpy as np, json

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# ── 1. Load raw activities ────────────────────────────────────────────────────
df = pd.read_parquet(f"{WS}/chembl_activities_raw.parquet")

# ── 2. Keep only quantitative single-point potency types ─────────────────────
QUANT_TYPES = {"IC50", "Ki", "Kd", "EC50", "pIC50", "pKi", "Kb"}
df = df[df["standard_type"].isin(QUANT_TYPES)].copy()
print(f"After type filter: {len(df)} rows, types: {df['standard_type'].value_counts().to_dict()}")

# ── 3. Keep only numeric values ───────────────────────────────────────────────
df["standard_value"] = pd.to_numeric(df["standard_value"], errors="coerce")
df = df.dropna(subset=["standard_value"])
print(f"After value filter: {len(df)} rows")

# ── 4. Convert to pIC50 ───────────────────────────────────────────────────────
# Assume nM unless standard_units says M
def to_pIC50(row):
    v = row["standard_value"]
    u = str(row.get("standard_units", "nM")).strip().lower()
    st = row["standard_type"]
    if st in ("pIC50", "pKi"):
        return v   # already log scale
    if v <= 0:
        return np.nan
    # Convert to molar
    if u in ("nm", "nm (ki)"):
        v_M = v * 1e-9
    elif u == "um":
        v_M = v * 1e-6
    elif u == "mm":
        v_M = v * 1e-3
    elif u == "m":
        v_M = v
    else:
        v_M = v * 1e-9  # assume nM
    return -np.log10(v_M)

df["pIC50"] = df.apply(to_pIC50, axis=1)
df = df.dropna(subset=["pIC50"])
# Clip to plausible range
df = df[(df["pIC50"] >= 3) & (df["pIC50"] <= 12)]
print(f"After pIC50 conversion: {len(df)} rows, range {df['pIC50'].min():.2f}–{df['pIC50'].max():.2f}")

# ── 5. Filter to kinase targets ───────────────────────────────────────────────
kinase_kw = ["kinase", "aurora", "pdk", "flt3", "jak2", "fgfr", "egfr", "braf", "abl",
             "btk", "src", "met", "cdk", "gsk3", "rock", "akt", "mek", "mapk",
             "chk", "plk", "erk", "p38", "jnk", "pkcalpha", "pkc", "mtor", "vegfr",
             "kdr", "ret", "alk", "ros"]
tn = df["target_pref_name"].fillna("").str.lower()
kinase_mask = tn.str.contains("|".join(kinase_kw), regex=True)
df_kin = df[kinase_mask].copy()
print(f"\nKinase activities: {len(df_kin)}")
print("Kinase targets found:\n", df_kin["target_pref_name"].value_counts().head(20).to_string())
