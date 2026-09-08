
import json

# Load SMILES-to-name map
with open(f"{WS}/ligand_smiles.json") as f:
    lig_data = json.load(f)
smiles_to_name = {v['smiles']: k for k, v in lig_data.items()}

# Map compound names
df_all['compound'] = df_all['SMILES'].map(smiles_to_name)
print("Unmapped SMILES:", df_all[df_all['compound'].isna()]['SMILES'].unique())

# Build pivot: max avg_score per compound-kinase pair
pivot = (df_all
         .groupby(['compound', 'Kinase'])['avg_score']
         .max()
         .unstack('Kinase'))

print(f"\nPivot shape: {pivot.shape}")
print(f"Compounds: {list(pivot.index)}")

# --- Verify PDK1 scores ---
print("\n--- PDK1 engagement ---")
pdk1_scores = pivot['PDK1'].sort_values()
for compound, score in pdk1_scores.items():
    print(f"  {compound}: {score:.3f}")
print(f"  Mean: {pdk1_scores.mean():.3f}")
print(f"  Weakest: {pdk1_scores.idxmin()} = {pdk1_scores.min():.3f}")
