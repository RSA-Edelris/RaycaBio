
import pandas as pd, json

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
with open(f"{WS}/ligand_smiles.json") as f:
    lig_data = json.load(f)
smiles_to_name = {v['smiles']: k for k, v in lig_data.items()}

csvs = [f"{WS}/kd2_out/PDK1_{b}/docking_results/PDK1_{b}_vina_results.csv"
        for b in ("AGC","probe5","batch2","batch3","batch4")]
df_all = pd.concat([pd.read_csv(f) for f in csvs], ignore_index=True)
df_all['compound'] = df_all['SMILES'].map(smiles_to_name)
pivot = df_all.groupby(['compound','Kinase'])['avg_score'].max().unstack('Kinase')
print(f"Pivot: {pivot.shape}")
