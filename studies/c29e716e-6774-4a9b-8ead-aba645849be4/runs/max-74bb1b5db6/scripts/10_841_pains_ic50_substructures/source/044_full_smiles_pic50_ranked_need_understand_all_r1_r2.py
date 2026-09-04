
# Full SMILES + pIC50 ranked — need to understand all R1/R2 variation
print("=== FULL RANKED LIST ===\n")
for _, row in df2.sort_values('pIC50_num', ascending=False).iterrows():
    flag = f" [PAINS:{row['pains_flag']}]" if row['pains_flag'] else " [clean]"
    print(f"{row['pIC50_num']:.3f}  {row['Serie'][:8]:<8}  {row['Molecule Name']:<14}{flag}")
    print(f"       {row['can_smiles']}")
    print()
