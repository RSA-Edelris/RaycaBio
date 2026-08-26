
# Understand reaction types and reagent categories
for name, df in dfs.items():
    print(f"\n=== {name} ===")
    if 'Reaction type' in df.columns:
        print("Reaction type:", df['Reaction type'].value_counts().to_dict())
    if 'Category' in df.columns:
        print("Category:", df['Category'].value_counts().to_dict())
    if 'KI/BB_Nature' in df.columns:
        print("Nature:", df['KI/BB_Nature'].value_counts().head(5).to_dict())
    print("Sample SMILES:", df['SMILES'].head(3).tolist())
