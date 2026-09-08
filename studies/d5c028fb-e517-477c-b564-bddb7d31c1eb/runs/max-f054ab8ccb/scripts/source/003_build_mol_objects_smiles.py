
from rdkit import Chem
from rdkit.Chem import AllChem, rdFMCS
from rdkit.Chem.Scaffolds import MurckoScaffold

# Build mol objects from SMILES
mols = []
for a in actives_sorted:
    m = Chem.MolFromSmiles(a['smiles'])
    if m:
        m.SetProp('_Name', a['name'])
        mols.append(m)
print(f"Mols built: {len(mols)}")

# MCS of all 15
res = rdFMCS.FindMCS(
    mols,
    bondCompare=rdFMCS.BondCompare.CompareOrderExact,
    atomCompare=rdFMCS.AtomCompare.CompareElements,
    ringMatchesRingOnly=True,
    completeRingsOnly=True,
    timeout=30
)
print(f"\nMCS (all 15): {res.smartsString}")
print(f"  atoms={res.numAtoms}  bonds={res.numBonds}")

mcs_mol = Chem.MolFromSmarts(res.smartsString)

# Murcko scaffolds
print("\n=== Murcko scaffolds ===")
scaffolds = {}
for m, a in zip(mols, actives_sorted):
    try:
        sc = MurckoScaffold.GetScaffoldForMol(m)
        sc_smi = Chem.MolToSmiles(sc)
        scaffolds.setdefault(sc_smi, []).append(a['name'])
    except:
        pass

for sc, names in sorted(scaffolds.items(), key=lambda x: -len(x[1])):
    print(f"  ({len(names)} cmpds) {sc}")
    for n in names:
        print(f"    {n}")
