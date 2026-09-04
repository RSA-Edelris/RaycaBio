
result = dispatch('pykvfinder', {}, files={'pdbFile': pdb_content})
print(result.get('summary', '')[:800] if result else 'None')
pockets_kv = result.get('pockets', [])
print(f"n_pockets: {result.get('n_pockets')}")
for p in pockets_kv[:5]:
    print(p)
