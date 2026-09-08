
import json, pandas as pd, numpy as np, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
with open(f"{WS}/ligand_smiles.json") as fh:
    ligs = json.load(fh)
smiles_to_name = {v["smiles"]: k for k, v in ligs.items()}

# Load all result CSVs
parts = {}
runs  = ["PDK1_AGC","PDK1_probe5","PDK1_batch2","PDK1_batch3","PDK1_batch4"]
for run in runs:
    path = f"{WS}/kd2_out/{run}/docking_results/{run}_vina_results.csv"
    df   = pd.read_csv(path)
    df["compound"] = df["SMILES"].map(smiles_to_name)
    parts[run] = df

df_all = pd.concat(parts.values(), ignore_index=True)
print(f"Total rows: {len(df_all)}")
print("Unique kinases:", df_all["Kinase"].nunique(), "–", sorted(df_all["Kinase"].unique()))
