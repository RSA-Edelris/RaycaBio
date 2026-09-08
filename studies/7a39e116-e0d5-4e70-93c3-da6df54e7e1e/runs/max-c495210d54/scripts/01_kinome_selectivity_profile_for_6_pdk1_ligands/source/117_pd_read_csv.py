
import pandas as pd

CSV = f"{WS}/kd2_out/PDK1_AGC/docking_results/PDK1_AGC_vina_results.csv"
df_agc = pd.read_csv(CSV)
print("Shape:", df_agc.shape)
print("Columns:", df_agc.columns.tolist())
print(df_agc.head(10).to_string())
