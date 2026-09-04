
# Run fpocket on Target.pdb
with open(pdb_path) as f:
    pdb_content = f.read()

fp_result = dispatch('fpocket', {}, files={'structure': pdb_content})
print("fpocket done")
print(f"n_pockets: {fp_result.get('n_pockets')}")
print(f"top_pocket_score: {fp_result.get('top_pocket_score')}")
print(f"top_pocket_druggability: {fp_result.get('top_pocket_druggability')}")

# Show top 5 pockets
pockets = fp_result.get('pockets', [])
print(f"\nTop 5 pockets:")
for p in pockets[:5]:
    print(p)
