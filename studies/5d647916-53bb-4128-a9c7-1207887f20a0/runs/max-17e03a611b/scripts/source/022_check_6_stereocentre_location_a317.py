
from rdkit import Chem
from rdkit.Chem import Descriptors

# ── CHECK 6: Stereocentre location in A317 ─────────────────────────────────
smi_a317 = "O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1"
mol = Chem.MolFromSmiles(smi_a317)

print("A317 stereocentres:")
from rdkit.Chem import rdMolDescriptors
chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
print(f"  Chiral centers: {chiral_centers}")

# Identify the stereocentre atom
for idx, cfg in chiral_centers:
    a = mol.GetAtomWithIdx(idx)
    print(f"\n  Atom idx {idx}: symbol={a.GetSymbol()}, config={cfg}")
    print(f"  In ring: {a.IsInRing()}")
    ri = mol.GetRingInfo()
    rings_with_atom = [r for r in ri.AtomRings() if idx in r]
    print(f"  Rings containing atom {idx}: {rings_with_atom}")
    for ring in rings_with_atom:
        syms = [mol.GetAtomWithIdx(x).GetSymbol() for x in ring]
        print(f"    Ring {ring}: size={len(ring)}, atoms={syms}")
    
    # Is it on thiazole (5-ring with S and N) or pyrrolidine (5-ring with N only)?
    for ring in rings_with_atom:
        syms = [mol.GetAtomWithIdx(x).GetSymbol() for x in ring]
        if 'S' in syms and 'N' in syms:
            print(f"    --> This atom is in the THIAZOLE ring")
        elif 'N' in syms and 'S' not in syms and 'O' not in syms and len(ring)==5:
            print(f"    --> This atom is in the PYRROLIDINE ring")
    
    print(f"  Neighbors: {[(nb.GetIdx(), nb.GetSymbol(), nb.GetIsAromatic()) for nb in a.GetNeighbors()]}")

# Also check: is thiazole C4 aromatic (sp2)?
print("\n--- Checking thiazole C4 aromaticity ---")
# Find thiazole ring
for ring in mol.GetRingInfo().AtomRings():
    syms = [mol.GetAtomWithIdx(x).GetSymbol() for x in ring]
    if 'S' in syms and 'N' in syms and len(ring)==5:
        print(f"Thiazole ring: {list(zip(ring, syms))}")
        for atom_idx in ring:
            a = mol.GetAtomWithIdx(atom_idx)
            print(f"  idx={atom_idx} {a.GetSymbol()} aromatic={a.GetIsAromatic()} hybridization={a.GetHybridization()}")
