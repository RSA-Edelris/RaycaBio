
import pandas as pd
import json

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

with open(f"{WS}/ligand_smiles.json") as f:
    lig_data = json.load(f)
smiles_to_name = {v['smiles']: k for k, v in lig_data.items()}

csv_files = [
    f"{WS}/kd2_out/PDK1_AGC/docking_results/PDK1_AGC_vina_results.csv",
    f"{WS}/kd2_out/PDK1_probe5/docking_results/PDK1_probe5_vina_results.csv",
    f"{WS}/kd2_out/PDK1_batch2/docking_results/PDK1_batch2_vina_results.csv",
    f"{WS}/kd2_out/PDK1_batch3/docking_results/PDK1_batch3_vina_results.csv",
    f"{WS}/kd2_out/PDK1_batch4/docking_results/PDK1_batch4_vina_results.csv",
]
df_all = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
df_all['compound'] = df_all['SMILES'].map(smiles_to_name)

pivot = (df_all
         .groupby(['compound', 'Kinase'])['avg_score']
         .max()
         .unstack('Kinase'))

# BX912 vs EL2003A: per-kinase delta (BX912 − EL2003A)
delta = (pivot.loc['BX912'] - pivot.loc['EL2003A']).sort_values(ascending=False)

print("BX912 vs EL2003A — pIC50 difference (BX912 − EL2003A, sorted)")
print(f"{'Kinase':22s}  {'BX912':7s}  {'EL2003A':8s}  {'Delta':7s}")
print("-" * 52)
for k, d in delta.items():
    flag = " <<<" if d >= 0.30 else (" <<" if d >= 0.15 else "")
    print(f"  {k:22s}  {pivot.loc['BX912',k]:.3f}    {pivot.loc['EL2003A',k]:.3f}    {d:+.3f}{flag}")
