
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors, Descriptors

# The 13/15 THN actives (exclude EDS00492874, EDS00492986 which are the succinamide series)
# Identify the universal THN core: N1CCc2ccc(C(=O)N)nc21 or the reverse notation
# Use the MCS SMARTS we found earlier (15-atom core) to identify matches

# SMARTS for the THN bicyclic core + two amide carbonyls  
# (derived from MCS, adapted to SMARTS syntax)
core_smarts = '[#6:1](=O)-[#7:2]1-[#6]-[#6]-[#6:3]2:[#6](-[#6]-1):[#7]:[#6:4](:[#6]:[#6]:2)-[#6:5](=O)-[#7:6]'
core_q = Chem.MolFromSmarts(core_smarts)

print("Testing core SMARTS match on actives:")
thn_actives = [a for a in actives_sorted if a['name'] not in ('EDS00492874','EDS00492986')]
matched = 0
for a in thn_actives:
    m = Chem.MolFromSmiles(a['smiles'])
    if m and m.HasSubstructMatch(core_q):
        matched += 1
        print(f"  ✓ {a['name']}  AS1={a['as1']:.4f}")
    else:
        print(f"  ✗ {a['name']}  AS1={a['as1']:.4f}  (no match)")
print(f"\nMatched {matched}/{len(thn_actives)} THN actives")
