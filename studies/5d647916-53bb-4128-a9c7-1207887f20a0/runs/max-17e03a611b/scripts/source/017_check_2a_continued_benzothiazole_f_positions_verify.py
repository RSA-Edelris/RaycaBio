
from rdkit import Chem
from rdkit.Chem import Descriptors
import json

# ── CHECK 2a continued: benzothiazole F positions ──────────────────────────
# Verify 4,6-difluoro vs other positions
smi_het = "Nc1nc2c(F)cc(F)cc2s1"
mol = Chem.MolFromSmiles(smi_het)
ri = mol.GetRingInfo()
five_ring = None
six_ring = None
for ring in ri.AtomRings():
    syms = [mol.GetAtomWithIdx(a).GetSymbol() for a in ring]
    if 'S' in syms:
        five_ring = ring
    else:
        six_ring = ring
print("5-membered ring atoms (benzothiazole ring):", five_ring)
print("6-membered ring atoms (benzo ring):", six_ring)

# In benzothiazole: S=1, C2(amino)=1, N3, C3a(junc), C4, C5, C6, C7, C7a(junc)
# Five ring: C1(S-C2 side), N3, C3a, C7a = let's map manually
s_idx = [a for a in five_ring if mol.GetAtomWithIdx(a).GetSymbol()=='S'][0]
n_idx_five = [a for a in five_ring if mol.GetAtomWithIdx(a).GetSymbol()=='N'][0]
print(f"S atom idx: {s_idx}, N atom idx (5-ring): {n_idx_five}")

# Junction atoms = in both rings
junctions = [a for a in five_ring if a in six_ring]
print(f"Junction atoms: {junctions}")

# C2 (bonded to S and N in 5-ring) 
c2_candidates = [a for a in five_ring if a not in junctions and mol.GetAtomWithIdx(a).GetSymbol()=='C']
print(f"C2 candidates (in 5-ring only, not junction): {c2_candidates}")
c2 = c2_candidates[0]
c2_atom = mol.GetAtomWithIdx(c2)
c2_neighbors_syms = [(nb.GetIdx(), nb.GetSymbol()) for nb in c2_atom.GetNeighbors()]
print(f"C2 (idx {c2}) neighbors: {c2_neighbors_syms}")

# Now trace the 6-membered ring from each junction:
# In benzothiazole, going from C3a (junction bonded to N3) around the 6-ring
# C4-C5-C6-C7-C7a
j_bonded_to_N = [j for j in junctions 
                  if any(nb.GetIdx()==n_idx_five for nb in mol.GetAtomWithIdx(j).GetNeighbors())]
j_bonded_to_S = [j for j in junctions 
                  if any(nb.GetIdx()==s_idx for nb in mol.GetAtomWithIdx(j).GetNeighbors())]
print(f"Junction bonded to N (=C3a): {j_bonded_to_N}")
print(f"Junction bonded to S (=C7a): {j_bonded_to_S}")

c3a = j_bonded_to_N[0]
c7a = j_bonded_to_S[0]

# Traverse 6-ring from C3a to C7a (not via junction bond)
# Order: C3a, C4, C5, C6, C7, C7a
ring_order = [c3a]
prev = None
current = c3a
for _ in range(5):
    neighbors_in_ring = [a for a in six_ring if a != current and a != prev 
                         and any(nb.GetIdx()==a for nb in mol.GetAtomWithIdx(current).GetNeighbors())]
    # Pick the one that's not going backward
    for nb_idx in neighbors_in_ring:
        if nb_idx != prev:
            ring_order.append(nb_idx)
            prev = current
            current = nb_idx
            break

print(f"\nBenzo ring traversal from C3a: {ring_order}")
for pos, idx in enumerate(ring_order):
    a = mol.GetAtomWithIdx(idx)
    has_F = any(nb.GetSymbol()=='F' for nb in a.GetNeighbors())
    pos_name = {0:'C3a',1:'C4',2:'C5',3:'C6',4:'C7',5:'C7a'}.get(pos, f'pos{pos}')
    print(f"  {pos_name} (idx {idx}): F={has_F}")
