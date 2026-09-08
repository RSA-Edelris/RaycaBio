
import json, pandas as pd, numpy as np, os, glob

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

with open(f"{WS}/ligand_smiles.json") as fh:
    ligs = json.load(fh)

smiles_list    = [v["smiles"] for v in ligs.values()]
smiles_to_name = {v["smiles"]: k for k, v in ligs.items()}

df_agc = pd.read_csv(f"{WS}/kd2_out/PDK1_AGC/docking_results/PDK1_AGC_vina_results.csv")
df_agc["compound"] = df_agc["SMILES"].map(smiles_to_name)

existing = glob.glob(f"{WS}/kd2_out/**/docking_results/*.csv", recursive=True)
for f in existing:
    print(os.path.getsize(f), f)

print("Ready. smiles_list len:", len(smiles_list))
