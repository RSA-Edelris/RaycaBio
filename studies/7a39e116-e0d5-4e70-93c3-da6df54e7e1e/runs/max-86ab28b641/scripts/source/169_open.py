
import pandas as pd, numpy as np, json, pickle
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

csvs = [f"{WS}/kd2_out/PDK1_{b}/docking_results/PDK1_{b}_vina_results.csv"
        for b in ("AGC","probe5","batch2","batch3","batch4")]
with open(f"{WS}/ligand_smiles.json") as fh:
    smiles_to_name = {v["smiles"]: k for k, v in json.load(fh).items()}
df_all = pd.concat([pd.read_csv(c) for c in csvs], ignore_index=True)
df_all["compound"] = df_all["SMILES"].map(smiles_to_name)
pivot = df_all.groupby(["compound","Kinase"])["avg_score"].max().unstack("Kinase")

COMPOUNDS = ["BX912","EL2003A","EL2003A-A2U1","EL2003A-A4U1","EL5001A","EL5003A"]

# ── Docking: common kinases (all 6) with mean >= 6.9 ────────────────────────
present_all = pivot.notna().all(axis=0)
dock_common = pivot.loc[:, present_all]
means = dock_common.mean()
strong = means[means >= 6.9].sort_values(ascending=False)
print("Docking — kinases ≥6.9 mean pIC50 across all 6:")
for k in strong.index:
    vals = dock_common[k]
    row = "  ".join([f"{c[:6]}={vals[c]:.2f}" for c in COMPOUNDS])
    print(f"  {k:8s}  mean={vals.mean():.3f}  min={vals.min():.3f}   {row}")

# ── Inference: common to all 6 ───────────────────────────────────────────────
with open(f"{WS}/tanimoto_inference_results.pkl","rb") as f:
    results = pickle.load(f)

all_targets = set()
for r in results.values():
    all_targets.update(r["target_pref_name"].tolist())

inf_mat = pd.DataFrame(index=sorted(all_targets), columns=COMPOUNDS, dtype=float)
for cmp in COMPOUNDS:
    r = results.get(cmp, pd.DataFrame())
    if len(r):
        r2 = r.set_index("target_pref_name")["inferred_pIC50"]
        inf_mat[cmp] = r2

inf_common = inf_mat[inf_mat.notna().all(axis=1)].copy()
inf_common["mean"] = inf_common[COMPOUNDS].mean(axis=1)
inf_common["min"]  = inf_common[COMPOUNDS].min(axis=1)
print(f"\nInference — kinases with values for ALL 6 compounds ({len(inf_common)}):")
for t in inf_common.sort_values("mean", ascending=False).index:
    row = inf_common.loc[t]
    print(f"  {t[:55]:55s}  mean={row['mean']:.2f}  min={row['min']:.2f}")
