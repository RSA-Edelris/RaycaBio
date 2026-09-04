
# PDB too large for inline arg — pass as file
result = dispatch('pykvfinder', {}, files={'pdbFile': pdb_content})
print(f"n_cavities: {result.get('n_cavities')}")
print(result.get('summary', '')[:600])
vols = result.get('volume', {})
print("Volumes (top 5):", list(vols.items())[:5] if vols else 'none')
depth = result.get('max_depth', {})
hydrop = result.get('avg_hydropathy', {})
print("Max depth:", list(depth.items())[:5] if depth else 'none')
print("Avg hydropathy:", list(hydrop.items())[:5] if hydrop else 'none')
