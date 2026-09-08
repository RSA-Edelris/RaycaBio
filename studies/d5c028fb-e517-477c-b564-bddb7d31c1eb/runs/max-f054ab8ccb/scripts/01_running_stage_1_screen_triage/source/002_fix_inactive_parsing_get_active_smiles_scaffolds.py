
# Fix inactive parsing + get active SMILES / scaffolds
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, AllChem, rdFMCS
from rdkit.Chem.Scaffolds import MurckoScaffold
import statistics

# ---- Print active SMILES ranked by AS ratio ----
print("=== ACTIVES ranked by AS ratio (primary potency signal) ===")
actives_sorted = sorted(actives, key=lambda x: -x['as1'])
for i, a in enumerate(actives_sorted):
    print(f"  [{i+1}] {a['name']}  AS1={a['as1']:.4f}  AS2={a['as2']:.4f}  MW={a['mw']:.0f}  logP={a['logp']:.2f}  HBD={a['hbd']}")
    print(f"       SMILES: {a['smiles']}")
    print()

# ---- Property ranges ----
print("=== Property summary (actives, n=15) ===")
for key, label in [('mw','MW'), ('logp','logP'), ('hbd','HBD'), ('hba','HBA'),
                   ('tpsa','TPSA'), ('rot','RotB'), ('hac','HAC')]:
    vals = [a[key] for a in actives]
    print(f"  {label}: min={min(vals):.1f}  max={max(vals):.1f}  median={statistics.median(vals):.1f}")
