
import pandas as pd, numpy as np, json, matplotlib, matplotlib.pyplot as plt, matplotlib.patches as mpatches
matplotlib.use("Agg")
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# ── Docking pivot (already have pivot in namespace) ───────────────────────────
# Short→full name map for the 43-panel kinases we want to cross-reference
S2F = {
    "AurA":  "Aurora kinase A",
    "PDK1":  "3-phosphoinositide-dependent protein kinase 1",
    "FLT3":  "Receptor-type tyrosine-protein kinase FLT3",
    "BTK":   "Tyrosine-protein kinase BTK",
    "CDK2":  "Cyclin-dependent kinase 2",
    "FGFR1": "Fibroblast growth factor receptor 1",
}
F2S = {v: k for k, v in S2F.items()}

# BX912 experimental
bx912_exp = {
    "Aurora kinase A": 7.860,
    "MAP/microtubule affinity-regulating kinase 4": 6.471,
    "MAP/microtubule affinity-regulating kinase 3": 5.477,
    "Serine/threonine-protein kinase TBK1": 5.633,
}

bx_inf = results["BX912"].copy()
bx_inf["dock_pIC50"] = bx_inf["target_pref_name"].map(
    {F2S.get(t, t): pivot.loc["BX912", F2S.get(t, t)]
     for t in bx_inf["target_pref_name"] if F2S.get(t, t) in pivot.columns}
)
bx_inf["exp_pIC50"] = bx_inf["target_pref_name"].map(bx912_exp)
bx_inf["short"] = bx_inf["target_pref_name"].map(F2S).fillna(
    bx_inf["target_pref_name"].str.extract(r'\b([A-Z][A-Z0-9]{1,7})\b')[0].fillna(
        bx_inf["target_pref_name"].str.split().str[-2:].str.join(" ")))
bx_inf = bx_inf.sort_values("inferred_pIC50", ascending=False)
print("BX912 — full comparison table (top 20 by inferred pIC50):")
cols = ["target_pref_name","dock_pIC50","inferred_pIC50","exp_pIC50","n_analogs","best_Tc"]
print(bx_inf[cols].head(20).round(3).to_string(index=False))
print()

# ── Cross-compound summary: inferred pIC50 for AurA + novel off-targets ───────
novel_targets = [
    "Tyrosine-protein kinase JAK3",
    "Cytoplasmic tyrosine-protein kinase BMX",
    "Interleukin-1 receptor-associated kinase 4",
    "Inhibitor of nuclear factor kappa-B kinase subunit epsilon",
    "Tyrosine-protein kinase BTK",
    "Tyrosine-protein kinase ITK/TSK",
    "Aurora kinase A",
    "Serine/threonine-protein kinase TBK1",
    "Leucine-rich repeat serine/threonine-protein kinase 2",
    "Serine/threonine-protein kinase 17A",
    "MAP/microtubule affinity-regulating kinase 4",
]
target_labels = {
    "Tyrosine-protein kinase JAK3": "JAK3",
    "Cytoplasmic tyrosine-protein kinase BMX": "BMX",
    "Interleukin-1 receptor-associated kinase 4": "IRAK4",
    "Inhibitor of nuclear factor kappa-B kinase subunit epsilon": "IKKε",
    "Tyrosine-protein kinase BTK": "BTK",
    "Tyrosine-protein kinase ITK/TSK": "ITK",
    "Aurora kinase A": "AurA ★",
    "Serine/threonine-protein kinase TBK1": "TBK1",
    "Leucine-rich repeat serine/threonine-protein kinase 2": "LRRK2",
    "Serine/threonine-protein kinase 17A": "STK17A",
    "MAP/microtubule affinity-regulating kinase 4": "MARK4 ★",
}

compounds_order = ["BX912","EL2003A","EL2003A-A2U1","EL2003A-A4U1","EL5001A","EL5003A"]
matrix = pd.DataFrame(index=novel_targets, columns=compounds_order, dtype=float)
for cmp in compounds_order:
    r = results.get(cmp, pd.DataFrame())
    if len(r):
        r_idx = r.set_index("target_pref_name")["inferred_pIC50"]
        for t in novel_targets:
            if t in r_idx:
                matrix.loc[t, cmp] = round(r_idx[t], 2)

matrix.index = [target_labels[t] for t in novel_targets]
print("Cross-compound inferred pIC50 heatmap (★ = experimentally confirmed):")
print(matrix.to_string())
matrix.to_csv(f"{WS}/similarity_inference_matrix.csv")
print("\nSaved.")
