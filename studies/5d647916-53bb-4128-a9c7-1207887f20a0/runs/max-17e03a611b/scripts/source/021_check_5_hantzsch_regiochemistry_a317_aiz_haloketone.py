
from rdkit import Chem

# ── CHECK 5: Hantzsch regiochemistry for A317 AiZ haloketone ──────────────
# AiZ proposed: O=C(CBr)[C@H]1CCCN1c1ccccn1
# Claim: "would give C5- not C4-substituted thiazole"
# The target A317 has pyrrolidinyl group at C4 of thiazole.

# Key SMILES: O=C(CBr)[C@H]1CCCN1c1ccccn1
smi_haloketone = "O=C(CBr)[C@H]1CCCN1c1ccccn1"
mol_hk = Chem.MolFromSmiles(smi_haloketone)
print("Haloketone SMILES valid:", mol_hk is not None)

if mol_hk:
    print("Atoms:")
    for a in mol_hk.GetAtoms():
        subs = [(nb.GetIdx(), nb.GetSymbol()) for nb in a.GetNeighbors()]
        print(f"  idx={a.GetIdx()} sym={a.GetSymbol()} charge={a.GetFormalCharge()} "
              f"Hs={a.GetTotalNumHs()} neighbors={subs}")
    
    # Identify the carbonyl carbon (C=O)
    carbonyl_C = None
    alpha_C_br = None
    for a in mol_hk.GetAtoms():
        if a.GetSymbol() == 'C':
            # Has double bond to O?
            for bond in a.GetBonds():
                if bond.GetBondTypeAsDouble() == 2.0:
                    other = bond.GetOtherAtom(a)
                    if other.GetSymbol() == 'O':
                        carbonyl_C = a.GetIdx()
            # Has Br neighbor?
            for nb in a.GetNeighbors():
                if nb.GetSymbol() == 'Br':
                    alpha_C_br = a.GetIdx()
    
    print(f"\nCarbonyl C idx: {carbonyl_C}")
    print(f"Alpha-C (bearing Br) idx: {alpha_C_br}")
    
    # What substituents does each carry?
    if carbonyl_C is not None:
        c_atom = mol_hk.GetAtomWithIdx(carbonyl_C)
        print(f"\nCarbonyl C (idx {carbonyl_C}) neighbors:")
        for nb in c_atom.GetNeighbors():
            print(f"  {nb.GetIdx()} {nb.GetSymbol()} (in_ring={nb.IsInRing()})")
    
    if alpha_C_br is not None:
        a_atom = mol_hk.GetAtomWithIdx(alpha_C_br)
        print(f"\nAlpha-C/Br (idx {alpha_C_br}) neighbors:")
        for nb in a_atom.GetNeighbors():
            print(f"  {nb.GetIdx()} {nb.GetSymbol()} (in_ring={nb.IsInRing()})")

# Hantzsch rule statement:
print("\n--- Hantzsch rule ---")
print("In Hantzsch 2-aminothiazole synthesis from alpha-haloketone R1-C(=O)-CH2Br + thiourea:")
print("  alpha-C (bearing Br) → C5 of thiazole (unsubstituted if R2=H)")
print("  Carbonyl C (bearing R1) → C4 of thiazole (carries substituent R1)")
print()
print("For O=C(CBr)[C@H]1CCCN1c1ccccn1:")
print("  alpha-C = CH2Br (no large substituent) → C5 (will have H after ring formation)")
print("  Carbonyl C = C(=O) bearing [C@H]1CCCN1c1ccccn1 (pyrrolidinyl group) → C4")
print()
print("In target A317: pyrrolidinyl group IS at C4 of thiazole.")
print("Conclusion: AiZ haloketone gives CORRECT regioisomer (C4-pyrrolidinyl)")
print("=> Phase-1 claim that AiZ gives 'wrong regioisomer (C5 not C4)' is INCORRECT")
