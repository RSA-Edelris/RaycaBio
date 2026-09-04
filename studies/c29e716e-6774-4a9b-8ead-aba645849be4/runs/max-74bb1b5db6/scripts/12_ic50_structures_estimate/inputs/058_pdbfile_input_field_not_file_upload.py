
# pdbFile is an INPUT field, not a file upload
result = dispatch('pykvfinder', {'pdbFile': pdb_content})
print(f"n_cavities: {result.get('n_cavities')}")
print(result.get('summary', '')[:600])
vols = result.get('volume', {})
areas = result.get('area', {})
residues = result.get('residues', {})
print("Volumes:", list(vols.items())[:5] if vols else 'none')
print("Areas:", list(areas.items())[:5] if areas else 'none')
