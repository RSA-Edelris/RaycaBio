
result = dispatch('pykvfinder', {}, files={'structure': pdb_content})
print(result.get('summary', '')[:500] if result else 'None')
print(result.get('n_pockets') if result else 'None')
pockets_kv = result.get('pockets', [])
for p in pockets_kv[:5]:
    print(p)
