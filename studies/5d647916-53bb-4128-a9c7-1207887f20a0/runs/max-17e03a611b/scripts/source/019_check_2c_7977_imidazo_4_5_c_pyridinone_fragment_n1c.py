
from rdkit import Chem

# ── CHECK 2c: 7977 — imidazo[4,5-c]pyridinone? ─────────────────────────────
# Fragment: n1c(=O)n(CC(N)=O)c2cnccc21
# Full 7977: Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21

smi_7977 = "Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21"
mol = Chem.MolFromSmiles(smi_7977)
print("7977 SMILES valid:", mol is not None)

if mol:
    ri = mol.GetRingInfo()
    ring_sizes = [(list(r), len(r)) for r in ri.AtomRings()]
    print("Ring sizes:", [r[1] for r in ring_sizes])
    
    # Find the fused 5+6 ring system containing N,N (imidazole + pyridine)
    fused_5 = None
    fused_6 = None
    for ring, sz in ring_sizes:
        syms = [mol.GetAtomWithIdx(a).GetSymbol() for a in ring]
        if sz == 5:
            n_count = syms.count('N')
            o_count = syms.count('O')
            print(f"  5-ring {ring}: {syms} (N={n_count}, O={o_count})")
            if n_count >= 2:
                fused_5 = ring
        elif sz == 6:
            syms_set = set(syms)
            n_in_ring = syms.count('N')
            print(f"  6-ring {ring}: {syms} (N={n_in_ring})")
    
    print()
    # Now specifically analyze the imidazo-pyridine fused system
    for ring, sz in ring_sizes:
        syms = [mol.GetAtomWithIdx(a).GetSymbol() for a in ring]
        if sz == 5 and syms.count('N') == 2:
            five_r = ring
            # Get the junction atoms shared with a 6-membered ring
            for ring6, sz6 in ring_sizes:
                if sz6 == 6:
                    junctions = [a for a in five_r if a in ring6]
                    if len(junctions) == 2:
                        print(f"Fused pair: 5-ring {five_r} + 6-ring {ring6}")
                        syms5 = [mol.GetAtomWithIdx(a).GetSymbol() for a in five_r]
                        syms6 = [mol.GetAtomWithIdx(a).GetSymbol() for a in ring6]
                        print(f"  5-ring atoms: {list(zip(five_r, syms5))}")
                        print(f"  6-ring atoms: {list(zip(ring6, syms6))}")
                        print(f"  Junction atoms: {junctions} = {[mol.GetAtomWithIdx(j).GetSymbol() for j in junctions]}")
                        
                        # Find N in 6-ring (pyridine N)
                        py_N_in_6 = [a for a in ring6 if mol.GetAtomWithIdx(a).GetSymbol()=='N']
                        print(f"  N in 6-ring (pyridine N): {py_N_in_6}")
                        
                        # Measure distance from each junction to pyridine N within the 6-ring
                        for j in junctions:
                            ring6_list = list(ring6)
                            pos_j = ring6_list.index(j)
                            for py_n in py_N_in_6:
                                pos_n = ring6_list.index(py_n)
                                d = abs(pos_j - pos_n)
                                d = min(d, len(ring6_list) - d)
                                print(f"    Junction {j}({mol.GetAtomWithIdx(j).GetSymbol()}) to py-N {py_n}: {d} bonds in 6-ring")
                        
                        # In imidazo[4,5-c]pyridine: one junction is 2 bonds from pyridine N
                        # In imidazo[4,5-b]pyridine: one junction is 1 bond from pyridine N
                        
                        # Check carbonyl in 5-ring
                        for a in five_r:
                            atom = mol.GetAtomWithIdx(a)
                            for nb in atom.GetNeighbors():
                                if nb.GetSymbol()=='O' and mol.GetBondBetweenAtoms(a, nb.GetIdx()).GetBondTypeAsDouble()==2.0:
                                    print(f"  Carbonyl at idx {a} (position in 5-ring)")
