
import pandas as pd
import os
import glob

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# Load all raw docking result CSVs
csv_files = {
    'AGC':    f"{WS}/kd2_out/PDK1_AGC/docking_results/PDK1_AGC_vina_results.csv",
    'probe5': f"{WS}/kd2_out/PDK1_probe5/docking_results/PDK1_probe5_vina_results.csv",
    'batch2': f"{WS}/kd2_out/PDK1_batch2/docking_results/PDK1_batch2_vina_results.csv",
    'batch3': f"{WS}/kd2_out/PDK1_batch3/docking_results/PDK1_batch3_vina_results.csv",
    'batch4': f"{WS}/kd2_out/PDK1_batch4/docking_results/PDK1_batch4_vina_results.csv",
}

dfs = []
for name, path in csv_files.items():
    if os.path.exists(path):
        df = pd.read_csv(path)
        df['batch'] = name
        dfs.append(df)
        print(f"{name}: {len(df)} rows, cols: {list(df.columns)[:6]}")
    else:
        print(f"MISSING: {path}")

df_all = pd.concat(dfs, ignore_index=True)
print(f"\nTotal rows: {len(df_all)}")
print(f"Kinases: {df_all['Kinase'].nunique()}")
print(f"SMILES (compounds): {df_all['SMILES'].nunique()}")
