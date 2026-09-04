
from rdkit import Chem

# ── CHECK 2d: 7877 — oxazolo[4,5-c]pyridine? ──────────────────────────────
# Full 7877: Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1
# Fused fragment: c2cnc3occ(...)c3c2

smi_7877 = "Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1"
mol = Chem.MolFromSmiles(smi_7877)
print("7877 SMILES valid:", mol is not None)

if mol:
    ri = mol.GetRingInfo()
    ring_sizes_atoms = [(list(r), len(r)) for r in ri.AtomRings()]
    print("Ring sizes:", sorted([r[1] for r in ring_sizes_atoms]))
    
    for ring, sz in ring_sizes_atoms:
        syms = [mol.GetAtomWithIdx(a).GetSymbol() for a in ring]
        n_count = syms.count('N')
        o_count = syms.count('O')
        print(f"  {sz}-ring {ring}: {syms}  N={n_count} O={o_count}")
    
    # Find the 5-membered ring containing O
    print("\n--- Fused 5+6 ring with O in 5-ring ---")
    for ring5, sz5 in ring_sizes_atoms:
        if sz5 != 5: continue
        syms5 = [mol.GetAtomWithIdx(a).GetSymbol() for a in ring5]
        if 'O' not in syms5: continue
        
        for ring6, sz6 in ring_sizes_atoms:
            if sz6 != 6: continue
            junctions = [a for a in ring5 if a in ring6]
            if len(junctions) == 2:
                syms6 = [mol.GetAtomWithIdx(a).GetSymbol() for a in ring6]
                print(f"Fused pair found:")
                print(f"  5-ring: {list(zip(ring5, syms5))}")
                print(f"  6-ring: {list(zip(ring6, syms6))}")
                print(f"  Junction atoms: {junctions} = {[mol.GetAtomWithIdx(j).GetSymbol() for j in junctions]}")
                
                # CRITICAL: Does the 5-ring contain N?
                n_in_5 = syms5.count('N')
                o_in_5 = syms5.count('O')
                print(f"  5-ring composition: N={n_in_5}, O={o_in_5}, C={syms5.count('C')}")
                if n_in_5 == 0 and o_in_5 == 1:
                    print("  *** 5-ring has O but NO N → FURAN ring, NOT oxazole! ***")
                elif n_in_5 == 1 and o_in_5 == 1:
                    print("  5-ring has both O and N → oxazole")
                
                # Find N in 6-ring (pyridine N)
                py_N_in_6 = [a for a in ring6 if mol.GetAtomWithIdx(a).GetSymbol()=='N']
                print(f"  N in 6-ring: {py_N_in_6}")
                
                # Distance from O in 5-ring to each junction
                o_in_5ring = [a for a in ring5 if mol.GetAtomWithIdx(a).GetSymbol()=='O']
                ring5_list = list(ring5)
                for o_idx in o_in_5ring:
                    for j in junctions:
                        pos_o = ring5_list.index(o_idx)
                        pos_j = ring5_list.index(j)
                        d = abs(pos_o - pos_j)
                        d = min(d, len(ring5_list)-d)
                        print(f"  O(idx {o_idx}) to junction {j}: {d} bonds in 5-ring")
                
                # Distance from each junction to pyridine N
                ring6_list = list(ring6)
                for j in junctions:
                    for py_n in py_N_in_6:
                        pos_j = ring6_list.index(j)
                        pos_n = ring6_list.index(py_n)
                        d = abs(pos_j - pos_n)
                        d = min(d, len(ring6_list)-d)
                        print(f"  Junction {j}({mol.GetAtomWithIdx(j).GetSymbol()}) to py-N {py_n}: {d} bonds in 6-ring")
