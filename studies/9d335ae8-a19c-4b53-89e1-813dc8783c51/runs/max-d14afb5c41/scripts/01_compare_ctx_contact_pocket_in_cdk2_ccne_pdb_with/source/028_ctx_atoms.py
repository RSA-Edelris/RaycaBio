
import numpy as np
from scipy.spatial import cKDTree

# CTX atoms
ctx_atoms = [a for a in hetatm if a['resn'] == 'CTX']
print(f"CTX: {len(ctx_atoms)} heavy atoms, chain {ctx_atoms[0]['chain']}, resseq {ctx_atoms[0]['resseq']}")
ctx_names = [a['name'] for a in ctx_atoms]
print("Atom names:", ctx_names)

ctx_xyz = np.array([[a['x'], a['y'], a['z']] for a in ctx_atoms])
ctx_centroid = ctx_xyz.mean(axis=0)
print(f"CTX centroid: {ctx_centroid.round(2)}")

# All protein atoms (ATOM records)
prot_atoms = [a for a in atoms if a['rec'] == 'ATOM']
prot_xyz   = np.array([[a['x'], a['y'], a['z']] for a in prot_atoms])

# Build tree on protein; query with CTX coords
tree = cKDTree(prot_xyz)
contacts = tree.query_ball_point(ctx_xyz, r=4.5)
contact_idx = set(i for c in contacts for i in c)

# Unique residues in contact shell
ctx_pocket = {}
for i in contact_idx:
    a = prot_atoms[i]
    key = (a['chain'], a['resseq'], a['resn'])
    ctx_pocket[key] = True

ctx_pocket_sorted = sorted(ctx_pocket.keys(), key=lambda x: (x[0], x[1]))
print(f"\n{len(ctx_pocket_sorted)} residues within 4.5 Å of CTX:")
for chain, resseq, resn in ctx_pocket_sorted:
    print(f"  Chain {chain}  {resn}{resseq}")
