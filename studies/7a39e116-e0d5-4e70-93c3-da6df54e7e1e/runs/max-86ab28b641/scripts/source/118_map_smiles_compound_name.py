
import json, pandas as pd, numpy as np

# Map SMILES → compound name
with open(f"{WS}/ligand_smiles.json") as fh:
    ligs = json.load(fh)

smiles_to_name = {v["smiles"]: k for k, v in ligs.items()}
smiles_list    = [v["smiles"] for v in ligs.values()]

# Label AGC frame
df_agc["compound"] = df_agc["SMILES"].map(smiles_to_name)

# Per compound × kinase best score
agc_pivot = (df_agc
             .groupby(["compound", "Kinase"])["avg_score"]
             .max()
             .unstack("Kinase")
             .fillna(np.nan))

print("AGC pivot (n kinases =", agc_pivot.shape[1], ")")
print(agc_pivot.round(2).to_string())
