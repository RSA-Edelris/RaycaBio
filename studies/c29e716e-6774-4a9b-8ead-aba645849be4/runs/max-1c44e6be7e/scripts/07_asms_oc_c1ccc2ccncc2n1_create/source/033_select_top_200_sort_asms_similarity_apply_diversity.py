
# Select top 200: sort by ASMS similarity, apply diversity (max ~3 per R1, max ~5 per R2)
prod_df = pd.DataFrame(products).sort_values('asms_sim', ascending=False)
print(f"Similarity distribution:")
print(prod_df['asms_sim'].describe())
print(f"\nTop 10 similarity: {prod_df['asms_sim'].head(10).tolist()}")
print(f"rxn_type counts:\n{prod_df['rxn_type'].value_counts()}")
