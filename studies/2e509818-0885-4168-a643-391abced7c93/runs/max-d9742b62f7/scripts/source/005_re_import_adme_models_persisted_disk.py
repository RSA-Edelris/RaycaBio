
import sys, importlib.util
# Re-import adme_models (persisted on disk)
spec = importlib.util.spec_from_file_location(
    "adme_models",
    "/home/ubuntu/rayca-sessions/2e509818-0885-4168-a643-391abced7c93-8c1a5f76c087/adme_models.py")
adme = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adme)

# ── Score all products ───────────────────────────────────────────────────────
rows = []
for p in products:
    mol = p['mol']
    try:
        d = adme.compute_base_descriptors(mol)
        sol  = adme.pred_solubility(d)
        pam  = adme.pred_pampa(d)
        met  = adme.pred_met_stability(mol, d)
        cyp  = adme.pred_cyp(mol, d)
        ppb  = adme.pred_ppb(d)
        herg = adme.pred_herg(mol, d)
        row  = dict(cr_id=p['cr_id'], acid_name=p['acid_name'],
                    smiles=p['smiles'], mol=mol)
        row.update(d)
        row.update({f"sol_{k}": v for k,v in sol.items()})
        row.update({f"pampa_{k}": v for k,v in pam.items()})
        row.update({f"met_{k}": v for k,v in met.items()})
        row.update({f"cyp_{k}": v for k,v in cyp.items()})
        row.update({f"ppb_{k}": v for k,v in ppb.items()})
        row.update({f"herg_{k}": v for k,v in herg.items()})
        rows.append(row)
    except Exception as e:
        print(f"ERROR {p['cr_id']}: {e}")

print(f"Scored {len(rows)} compounds")

# ── Check AD coverage ────────────────────────────────────────────────────────
n_sol_in  = sum(1 for r in rows if r['sol_sol_ad'])
n_pam_in  = sum(1 for r in rows if r['pampa_pampa_ad'])
n_ppb_in  = sum(1 for r in rows if r['ppb_ppb_ad'])
print(f"  AD coverage: ESOL {n_sol_in}/{len(rows)} | PAMPA {n_pam_in}/{len(rows)} | PPB {n_ppb_in}/{len(rows)}")

# MW range
mws = [r['mw'] for r in rows]
print(f"  MW range: {min(mws):.0f}–{max(mws):.0f} Da  (mean {sum(mws)/len(mws):.0f})")

# hERG distribution
from collections import Counter
print("  hERG:", dict(Counter(r['herg_herg_risk'] for r in rows)))
print("  CYP risk:", dict(Counter(r['cyp_cyp_risk'] for r in rows)))
print("  Met t1/2:", dict(Counter(r['met_t12_class'] for r in rows)))
print("  PAMPA cat:", dict(Counter(r['pampa_pampa_cat'] for r in rows)))
