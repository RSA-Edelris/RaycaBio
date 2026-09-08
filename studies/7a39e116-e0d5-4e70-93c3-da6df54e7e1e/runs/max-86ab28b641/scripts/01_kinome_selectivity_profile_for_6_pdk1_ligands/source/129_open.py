
import json, pandas as pd, numpy as np, os

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
with open(f"{WS}/ligand_smiles.json") as fh:
    ligs = json.load(fh)
smiles_list    = [v["smiles"] for v in ligs.values()]
smiles_to_name = {v["smiles"]: k for k, v in ligs.items()}

df_b3 = pd.read_csv(f"{WS}/kd2_out/PDK1_batch3/docking_results/PDK1_batch3_vina_results.csv")
df_b3["compound"] = df_b3["SMILES"].map(smiles_to_name)
print("Batch3 rows:", len(df_b3))
print(df_b3.groupby(["compound","Kinase"])["avg_score"].max()
      .unstack("Kinase").round(2).to_string())

# Final batch: CHEK1, CHEK2, PLK1, MEK1, BRAF, CSNK1D
batch4 = ["O14757","O96017","P53350","Q02750","P15056","P48730"]
r4 = dispatch("kinasedocker2", {
    "smiles":           smiles_list,
    "accessions":       batch4,
    "docking_engine":   "vina",
    "scoring_function": "DNN",
    "run_name":         "PDK1_batch4",
})
print("\nBatch4 rc:", r4.get("returncode", r4.get("rc","?")))
