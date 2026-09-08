
import sys, importlib.util

# Reload the fixed adme_models module from disk
if "adme_models" in sys.modules:
    del sys.modules["adme_models"]
spec = importlib.util.spec_from_file_location(
    "adme_models",
    "/home/ubuntu/rayca-sessions/2e509818-0885-4168-a643-391abced7c93-8c1a5f76c087/adme_models.py")
adme = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adme)
sys.modules["adme_models"] = adme

# Verify fix: first product should now have n_basic_n=0 (all N are amides or aromatic)
mol0 = products[0]['mol']
d0   = adme.compute_base_descriptors(mol0)
print(f"Fix verification — n_basic_n for first product: {d0['n_basic_n']} (expected 0 for pure amide scaffold)")
print(f"  SMILES: {products[0]['smiles']}")

# Re-score all products with corrected module
rows_fixed = []
errors = []
for p in products:
    mol = p['mol']
    try:
        d    = adme.compute_base_descriptors(mol)
        sol  = adme.pred_solubility(d)
        pam  = adme.pred_pampa(d)
        met  = adme.pred_met_stability(mol, d)
        cyp  = adme.pred_cyp(mol, d)
        ppb  = adme.pred_ppb(d)
        herg = adme.pred_herg(mol, d)
        row  = dict(cr_id=p['cr_id'], acid_name=p['acid_name'],
                    smiles=p['smiles'], mol=mol)
        row.update(d)
        row.update({f"sol_{k}":  v for k,v in sol.items()})
        row.update({f"pampa_{k}": v for k,v in pam.items()})
        row.update({f"met_{k}":  v for k,v in met.items()})
        row.update({f"cyp_{k}":  v for k,v in cyp.items()})
        row.update({f"ppb_{k}":  v for k,v in ppb.items()})
        row.update({f"herg_{k}": v for k,v in herg.items()})
        rows_fixed.append(row)
    except Exception as e:
        errors.append((p['cr_id'], str(e)))

print(f"\nScored: {len(rows_fixed)}, errors: {len(errors)}")
if errors:
    print("Errors:", errors)
if len(rows_fixed) != len(products):
    raise AssertionError(f"Row count mismatch: {len(rows_fixed)} scored vs {len(products)} products")

from collections import Counter
print("\nhERG after fix:", dict(Counter(r['herg_herg_risk'] for r in rows_fixed)))
print("ClearRoute after fix:", dict(Counter(r['met_clearance_route'] for r in rows_fixed)))
