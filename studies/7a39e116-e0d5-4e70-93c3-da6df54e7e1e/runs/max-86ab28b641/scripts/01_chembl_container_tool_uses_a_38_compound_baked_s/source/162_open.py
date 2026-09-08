
import pandas as pd, numpy as np, json, pickle
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# ── Rebuild docking pivot ─────────────────────────────────────────────────────
csvs = [f"{WS}/kd2_out/PDK1_{b}/docking_results/PDK1_{b}_vina_results.csv"
        for b in ("AGC","probe5","batch2","batch3","batch4")]
with open(f"{WS}/ligand_smiles.json") as fh:
    lig_data = json.load(fh)
smiles_to_name = {v["smiles"]: k for k, v in lig_data.items()}
import pandas as pd
df_all = pd.concat([pd.read_csv(c) for c in csvs], ignore_index=True)
df_all["compound"] = df_all["SMILES"].map(smiles_to_name)
pivot = df_all.groupby(["compound","Kinase"])["avg_score"].max().unstack("Kinase")  # shape (6,43)

# ── BX912 experimental measurements from ChEMBL ──────────────────────────────
bx912_exp = {
    "Aurora kinase A":                         7.860,   # Kd 13.79 nM
    "MAP/microtubule affinity-regulating kinase 4": 6.471,  # IC50 338 nM
    "MAP/microtubule affinity-regulating kinase 3": 5.477,  # IC50 3333 nM
    "Serine/threonine-protein kinase TBK1":    5.633,   # IC50 2327 nM
}

# ── Kinase name mapping: docking short → ChEMBL full ─────────────────────────
dock_to_chembl = {
    "AurA":  "Aurora kinase A",
    "PDK1":  "3-phosphoinositide-dependent protein kinase 1",
    "FLT3":  "Receptor-type tyrosine-protein kinase FLT3",
    "JAK2":  "Tyrosine-protein kinase JAK2",
    "FGFR1": "Fibroblast growth factor receptor 1",
    "BRAF":  "Serine/threonine-protein kinase B-raf",
    "CDK4":  "Cyclin-dependent kinase 4",
    "BTK":   "Tyrosine-protein kinase BTK",
    "CDK2":  "Cyclin-dependent kinase 2",
    "ABL1":  "Tyrosine-protein kinase ABL1",
}
chembl_to_dock = {v: k for k, v in dock_to_chembl.items()}

# ── Build comparison for BX912 (best-supported compound) ─────────────────────
rows = []

# A: docking targets in our 43-kinase panel
for kin43 in pivot.columns:
    dock_val = pivot.loc["BX912", kin43] if "BX912" in pivot.index else np.nan
    full_name = dock_to_chembl.get(kin43, "")
    inferred = np.nan
    if full_name and full_name in results.get("BX912", pd.DataFrame()).set_index("target_pref_name")["inferred_pIC50"].to_dict():
        inferred = results["BX912"].set_index("target_pref_name")["inferred_pIC50"][full_name]
    exp = bx912_exp.get(full_name, np.nan)
    rows.append({"kinase": kin43, "chembl_name": full_name,
                 "dock_pIC50": round(dock_val,3) if pd.notna(dock_val) else np.nan,
                 "inferred_pIC50": round(inferred,3) if pd.notna(inferred) else np.nan,
                 "exp_pIC50": exp,
                 "source": "docking_panel"})

# B: inferred targets NOT in 43-kinase panel
bx_inferred = results.get("BX912", pd.DataFrame())
for _, irow in bx_inferred.iterrows():
    cn = irow["target_pref_name"]
    kin_short = chembl_to_dock.get(cn, None)
    if kin_short and kin_short in pivot.columns:
        continue  # already covered above
    exp = bx912_exp.get(cn, np.nan)
    rows.append({"kinase": cn.split()[-1] if not kin_short else kin_short,
                 "chembl_name": cn,
                 "dock_pIC50": np.nan,
                 "inferred_pIC50": round(irow["inferred_pIC50"],3),
                 "exp_pIC50": exp,
                 "source": "inference_only"})

df_comp = pd.DataFrame(rows).sort_values("inferred_pIC50", ascending=False, na_position="last")
df_comp["n_analogs"] = df_comp["chembl_name"].map(
    bx_inferred.set_index("target_pref_name")["n_analogs"].to_dict()).fillna(0)

print("BX912 — Docking vs. Similarity Inference vs. Experimental (top 25 by inferred pIC50):")
print(df_comp[df_comp["inferred_pIC50"].notna()].head(25)[
    ["kinase","dock_pIC50","inferred_pIC50","exp_pIC50","n_analogs","source"]
].to_string(index=False))
