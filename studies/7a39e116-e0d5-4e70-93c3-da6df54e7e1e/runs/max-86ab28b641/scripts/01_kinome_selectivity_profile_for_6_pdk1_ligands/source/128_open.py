
import json, pandas as pd, numpy as np, os

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
with open(f"{WS}/ligand_smiles.json") as fh:
    ligs = json.load(fh)
smiles_list    = [v["smiles"] for v in ligs.values()]
smiles_to_name = {v["smiles"]: k for k, v in ligs.items()}

df_b2 = pd.read_csv(f"{WS}/kd2_out/PDK1_batch2/docking_results/PDK1_batch2_vina_results.csv")
df_b2["compound"] = df_b2["SMILES"].map(smiles_to_name)
print("Batch2 rows:", len(df_b2))
print(df_b2.groupby(["compound","Kinase"])["avg_score"].max()
      .unstack("Kinase").round(2).to_string())

# Immediately dispatch batch 3: TK kinases
batch3 = ["P35968","P11362","P08581","P12931","Q06187","O60674","P36888"]
# KDR/VEGFR2, FGFR1, MET, SRC, BTK, JAK2, FLT3
r3 = dispatch("kinasedocker2", {
    "smiles":           smiles_list,
    "accessions":       batch3,
    "docking_engine":   "vina",
    "scoring_function": "DNN",
    "run_name":         "PDK1_batch3",
})
print("\nBatch3 rc:", r3.get("returncode", r3.get("rc","?")))
