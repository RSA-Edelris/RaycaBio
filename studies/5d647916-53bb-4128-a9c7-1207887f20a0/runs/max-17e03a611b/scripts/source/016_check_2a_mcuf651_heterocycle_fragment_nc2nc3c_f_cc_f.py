
from rdkit import Chem
from rdkit.Chem import AllChem
import json

# ── CHECK 2a: MCUF651 heterocycle ──────────────────────────────────────────
# Fragment: Nc2nc3c(F)cc(F)cc3s2  (the 2-amino heterocycle from Route 1 leaf)
smi_mcuf651_het = "Nc1nc2c(F)cc(F)cc2s1"
mol = Chem.MolFromSmiles(smi_mcuf651_het)
print("MCUF651 heterocycle leaf SMILES valid:", mol is not None)
if mol:
    ri = mol.GetRingInfo()
    print("  Ring sizes:", [len(r) for r in ri.AtomRings()])
    # Identify atoms in each ring
    for i, ring in enumerate(ri.AtomRings()):
        syms = [mol.GetAtomWithIdx(a).GetSymbol() for a in ring]
        print(f"  Ring {i}: atoms {ring}, symbols {syms}")
    # Check for S and N in same ring (benzothiazole signature)
    for ring in ri.AtomRings():
        syms = set(mol.GetAtomWithIdx(a).GetSymbol() for a in ring)
        if 'S' in syms and 'N' in syms:
            print("  5-membered ring contains S and N → benzothiazole confirmed")
    # Check fluorine positions
    print("  Atoms and positions:")
    for a in mol.GetAtoms():
        subs = [nb.GetSymbol() for nb in a.GetNeighbors()]
        print(f"    idx={a.GetIdx()} sym={a.GetSymbol()} arom={a.GetIsAromatic()} neighbors={subs}")
