
# Full dataset sorted by pIC50 — examine top 15 and structure patterns
print("=== ALL 57 COMPOUNDS SORTED BY pIC50 ===\n")
cols = ['Molecule Name','Serie','pIC50_num','MW','LogP','HBD','HBA','RotB','pains_flag','can_smiles']
print(df2[cols].sort_values('pIC50_num', ascending=False).head(15).to_string(max_colwidth=80))

print("\n\n=== PHYSICOCHEMICAL SUMMARY BY SERIES ===")
print(df2.groupby('Serie')[['pIC50_num','MW','LogP','HBD','HBA','RotB','AromRings']].describe().round(2).to_string())
