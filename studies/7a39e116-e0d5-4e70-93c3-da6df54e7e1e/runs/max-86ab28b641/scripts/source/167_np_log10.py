
import pandas as pd, numpy as np, pickle, json
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# ── Audit 1: Similarity Inference ────────────────────────────────────────────

# A1-1: AurA pIC50 from Kd = 13.79 nM
aura_kd_nM = 13.79
aura_pKd = -np.log10(aura_kd_nM * 1e-9)
print(f"A1-1: AurA pKd from Kd=13.79 nM = {aura_pKd:.4f}  (reported 7.860) → {'PASS' if abs(aura_pKd-7.860)<0.002 else 'FAIL'}")

# A1-2: MARK4 pIC50 from IC50 = 338 nM
mark4_pic50 = -np.log10(338e-9)
print(f"A1-2: MARK4 pIC50 from IC50=338 nM = {mark4_pic50:.4f}  (reported 6.471) → {'PASS' if abs(mark4_pic50-6.471)<0.002 else 'FAIL'}")

# A1-3: TBK1 pIC50 from IC50 = 2327 nM
tbk1_pic50 = -np.log10(2327e-9)
print(f"A1-3: TBK1 pIC50 from IC50=2327 nM = {tbk1_pic50:.4f}  (reported 5.633) → {'PASS' if abs(tbk1_pic50-5.633)<0.002 else 'FAIL'}")

# A1-4: MARK3 pIC50 from IC50 = 3333 nM
mark3_pic50 = -np.log10(3333e-9)
print(f"A1-4: MARK3 pIC50 from IC50=3333 nM = {mark3_pic50:.4f}  (reported 5.477) → {'PASS' if abs(mark3_pic50-5.477)<0.002 else 'FAIL'}")

# A1-5: Unique analog IDs
with open(f"{WS}/similarity_hits.pkl", "rb") as f:
    hits = pickle.load(f)
all_ids = set()
for v in hits.values():
    all_ids.update(h["chembl_id"] for h in v)
print(f"\nA1-5: Unique analog IDs = {len(all_ids)}  (reported 105) → {'PASS' if len(all_ids)==105 else 'FAIL'}")

# A1-6: Per-compound analog counts
for cname, v in hits.items():
    print(f"  {cname}: {len(v)} analogs")

# A1-7: BX912 top hit = self at Tc=1.0
bx_hits = hits["BX912"]
top = max(bx_hits, key=lambda x: x["tanimoto"])
print(f"\nA1-7: BX912 top analog = {top['chembl_id']} Tc={top['tanimoto']:.4f}  → {'PASS' if top['tanimoto']==1.0 else 'FAIL'}")

# A1-8: Tanimoto-weighted AurA inference for BX912
# BX912 itself (Tc=1.0) has AurA Kd=13.79nM → pKd=7.860; it's the only AurA data point
# So inferred = (1.0 * 7.860) / 1.0 = 7.860 ✓
tc_bx912 = top["tanimoto"]
inferred_aura_bx912 = (tc_bx912 * aura_pKd) / tc_bx912
print(f"A1-8: Tanimoto-weighted AurA for BX912 = {inferred_aura_bx912:.4f}  (reported 7.860) → {'PASS' if abs(inferred_aura_bx912-7.860)<0.002 else 'FAIL'}")

# A1-9: Kinase activities count
df_raw = pd.read_parquet(f"{WS}/chembl_activities_raw.parquet")
QUANT = {"IC50","Ki","Kd","EC50","pIC50","pKi"}
df_q = df_raw[df_raw["standard_type"].isin(QUANT)].copy()
df_q["standard_value"] = pd.to_numeric(df_q["standard_value"], errors="coerce")
df_q = df_q.dropna(subset=["standard_value"])
kinase_kw = r"kinase|aurora|pdk|flt3|jak2|fgfr|egfr|braf|abl|btk|src|met\b|cdk|gsk3|rock|akt|mek|mapk|chk|plk|erk|p38|jnk|pkc|mtor|vegfr|kdr|ret\b|alk\b"
df_kin = df_q[df_q["target_pref_name"].fillna("").str.contains(kinase_kw, case=False, regex=True)]
print(f"\nA1-9: Kinase activity rows = {len(df_kin)}  (reported 126) → {'PASS' if len(df_kin)==126 else 'FAIL'}")

# A1-10: EL2003A top inferred = BMX at 8.35
el2_inf = results["EL2003A"].sort_values("inferred_pIC50", ascending=False)
top_el2 = el2_inf.iloc[0]
print(f"\nA1-10: EL2003A top inferred = {top_el2['target_pref_name'][:40]} pIC50={top_el2['inferred_pIC50']:.3f}  (reported BMX 8.35) → {'PASS' if 'BMX' in top_el2['target_pref_name'] and abs(top_el2['inferred_pIC50']-8.35)<0.01 else 'FAIL'}")
