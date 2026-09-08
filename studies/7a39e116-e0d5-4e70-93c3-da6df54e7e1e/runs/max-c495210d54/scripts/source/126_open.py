
import json, pandas as pd, numpy as np, os, glob

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
with open(f"{WS}/ligand_smiles.json") as fh:
    ligs = json.load(fh)
smiles_list    = [v["smiles"] for v in ligs.values()]
smiles_to_name = {v["smiles"]: k for k, v in ligs.items()}

# Read probe5 results
probe_csv = f"{WS}/kd2_out/PDK1_probe5/docking_results/PDK1_probe5_vina_results.csv"
df_probe  = pd.read_csv(probe_csv)
df_probe["compound"] = df_probe["SMILES"].map(smiles_to_name)
print("Probe5 rows:", len(df_probe))
print(df_probe.groupby(["compound","Kinase"])["avg_score"].max()
      .unstack("Kinase").round(2).to_string())
