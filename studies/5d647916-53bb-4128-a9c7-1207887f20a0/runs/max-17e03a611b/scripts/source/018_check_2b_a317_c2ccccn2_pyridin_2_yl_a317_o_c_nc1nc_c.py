
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

# ── CHECK 2b: A317 — is c2ccccn2 pyridin-2-yl? ──────────────────────────────
# A317: O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1
# Fragment: the pyrrolidine N connects to c2ccccn2
# Isolated pyridine ring from fragment
smi_frag = "Nc1ccccn1"  # 2-aminopyridine — attachment at C2 (adjacent to N)
smi_frag2 = "Nc1ccncc1"  # 4-aminopyridine — attachment at C4
smi_a317 = "O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1"

mol_a317 = Chem.MolFromSmiles(smi_a317)
print("A317 SMILES valid:", mol_a317 is not None)

# Find the pyridine N that is NOT in a heterocyclic ring containing S
# and identify which carbon of the pyridine the pyrrolidine N attaches to
if mol_a317:
    ri = mol_a317.GetRingInfo()
    print("Ring sizes:", sorted([len(r) for r in ri.AtomRings()]))
    
    # Find all N atoms
    n_atoms = [a for a in mol_a317.GetAtoms() if a.GetSymbol()=='N']
    print(f"N atom indices: {[(a.GetIdx(), a.GetIsAromatic()) for a in n_atoms]}")
    
    # The pyrrolidine N: non-aromatic N bonded to ring carbons
    pyrrolidine_N = [a for a in n_atoms if not a.GetIsAromatic() and 
                     any(nb.GetIsAromatic() for nb in a.GetNeighbors())]
    print(f"Pyrrolidine N candidates (non-aromatic, bonded to aromatic C): {[a.GetIdx() for a in pyrrolidine_N]}")
    
    # More precisely: non-aromatic N in a ring (pyrrolidine) that is also bonded to an aromatic ring
    for a in n_atoms:
        if not a.GetIsAromatic():
            ring_membership = [r for r in ri.AtomRings() if a.GetIdx() in r]
            aromatic_neighbors = [nb for nb in a.GetNeighbors() if nb.GetIsAromatic()]
            if ring_membership and aromatic_neighbors:
                print(f"  Pyrrolidine N idx={a.GetIdx()}, in rings: {ring_membership}")
                for nb in aromatic_neighbors:
                    print(f"    Bonded to aromatic atom idx={nb.GetIdx()} sym={nb.GetSymbol()}")
                    # What ring does that aromatic atom belong to?
                    pyridine_ring = [r for r in ri.AtomRings() 
                                     if nb.GetIdx() in r and 'N' in 
                                     [mol_a317.GetAtomWithIdx(x).GetSymbol() for x in r]]
                    if pyridine_ring:
                        print(f"    That aromatic atom is in ring(s): {pyridine_ring}")
                        ring = pyridine_ring[0]
                        syms_in_ring = [mol_a317.GetAtomWithIdx(x).GetSymbol() for x in ring]
                        print(f"    Ring atom symbols: {syms_in_ring}")
                        # Find pyridine N in this ring
                        py_N = [x for x in ring if mol_a317.GetAtomWithIdx(x).GetSymbol()=='N' 
                                and mol_a317.GetAtomWithIdx(x).GetIsAromatic()]
                        if py_N:
                            py_N_idx = py_N[0]
                            attach_C_idx = nb.GetIdx()
                            # Bond distance from attachment C to pyridine N
                            # In a 6-membered ring they can be 1,2,3 bonds apart (1=ortho/2-position, 2=meta/3, 3=para/4)
                            # Find shortest path within ring
                            ring_list = list(ring)
                            pos_attach = ring_list.index(attach_C_idx)
                            pos_N = ring_list.index(py_N_idx)
                            dist1 = abs(pos_attach - pos_N)
                            dist2 = len(ring_list) - dist1
                            min_dist = min(dist1, dist2)
                            print(f"    Pyridine N idx={py_N_idx}, attachment C idx={attach_C_idx}")
                            print(f"    Min ring distance (bonds): {min_dist} → position: {min_dist+1}-yl")
