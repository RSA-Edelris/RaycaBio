
# ── Re-apply MPO with same functions (redefined here since they were dropped) ─

def clamp(v, lo, hi): return max(lo, min(hi, v))

def linear_des(v, lo_bad, hi_good):
    if v <= lo_bad:  return 0.0
    if v >= hi_good: return 1.0
    return (v - lo_bad) / (hi_good - lo_bad)

def trapezoid_des(v, lo0, lo1, hi1, hi0):
    if v <= lo0 or v >= hi0:  return 0.0
    if lo1 <= v <= hi1:       return 1.0
    if v < lo1: return (v - lo0) / (lo1 - lo0)
    return (hi0 - v) / (hi0 - hi1)

WEIGHTS = {'sol':1.5,'logp':1.0,'perm':1.5,'met':1.5,'cyp':1.5,'ppb':0.5,'herg':2.0,'mw':0.5}
TOTAL_W = sum(WEIGHTS.values())

def compute_mpo(row):
    d = {
        'sol':  linear_des(row['sol_logS'], -5.5, -3.0),
        'logp': trapezoid_des(row['clogp'], 0.0, 2.0, 4.0, 5.5),
        'perm': linear_des(row['pampa_logPapp'], -7.0, -5.5),
        'met':  float(row['met_met_score']),
        'cyp':  {'Low':1.0,'Medium':0.5,'High':0.0}.get(row['cyp_cyp_risk'],0.0),
        'ppb':  1.0 if row['ppb_ppb_fu']>=0.05 else (0.7 if row['ppb_ppb_fu']>=0.01 else 0.3),
        'herg': {'Low':1.0,'Medium':0.5,'High':0.0}.get(row['herg_herg_risk'],0.0),
        'mw':   trapezoid_des(row['mw'], 200, 400, 650, 850),
    }
    mpo = sum(WEIGHTS[k]*v for k,v in d.items()) / TOTAL_W
    return round(mpo, 4), d

HARD_FILTERS = {
    'solubility':   ('sol_logS',        lambda v: v >= -5.5,   'logS < -5.5 (< 3 µM)'),
    'permeability': ('pampa_pampa_cat', lambda v: v != 'Low',  'PAMPA Low permeability'),
    'hERG':         ('herg_herg_risk',  lambda v: v != 'High', 'hERG High risk'),
    'CYP':          ('cyp_cyp_risk',    lambda v: v != 'High', 'CYP High multi-isoform risk'),
}

for row in rows_fixed:
    mpo, des = compute_mpo(row)
    row['mpo_score']     = mpo
    row['des_breakdown'] = des
    fails = [label for fname,(field,test,label) in HARD_FILTERS.items() if not test(row[field])]
    row['filter_fails']  = '; '.join(fails)
    row['passes_filter'] = len(fails) == 0

shortlist = sorted([r for r in rows_fixed if r['passes_filter']], key=lambda r: -r['mpo_score'])
rejected  = [r for r in rows_fixed if not r['passes_filter']]
override_candidates = [r for r in rejected
                       if len(r['filter_fails'].split(';'))==1 and r['mpo_score']>=0.55]

print(f"Pass filters: {len(shortlist)}  Rejected: {len(rejected)}")
print(f"Top-5 MPO   : {[r['mpo_score'] for r in shortlist[:5]]}")
print(f"Rank-96 MPO : {shortlist[95]['mpo_score']}")
print(f"\nRejection reasons:")
all_fails = [f.strip() for r in rejected for f in r['filter_fails'].split(';')]
for reason, cnt in Counter(all_fails).most_common():
    print(f"  {cnt:3d}  {reason}")
print(f"\nOverride candidates (1 fail, MPO≥0.55): {len(override_candidates)}")

# ── Re-export results.sdf ────────────────────────────────────────────────────
from rdkit.Chem import SDWriter
top96 = shortlist[:96]
out_path = '/home/ubuntu/rayca-sessions/2e509818-0885-4168-a643-391abced7c93-8c1a5f76c087/results.sdf'
writer = SDWriter(out_path)

for rank, row in enumerate(top96, 1):
    mol = Chem.RWMol(row['mol'])
    AllChem.Compute2DCoords(mol)
    def sp(k, v): mol.SetProp(k, str(v))
    sp('Rank',            rank)
    sp('CR_ID',           row['cr_id'])
    sp('Acid_Name',       row['acid_name'])
    sp('SMILES',          row['smiles'])
    sp('MPO_Score',       f"{row['mpo_score']:.4f}")
    sp('MW',              f"{row['mw']:.2f}")
    sp('cLogP',           f"{row['clogp']:.2f} ± 0.40")
    sp('TPSA',            f"{row['tpsa']:.1f}")
    sp('HBD',             str(row['hbd']))
    sp('HBA',             str(row['hba']))
    sp('RotBonds',        str(row['rb']))
    sp('Fsp3',            f"{row['fsp3']:.3f}")
    sp('NumArRings',      str(row['n_ar_rings']))
    sp('logS_ESOL',       f"{row['sol_logS']:.2f} ± {row['sol_logS_sd']:.2f} log(mol/L)")
    sp('logS_AD',         'In' if row['sol_sol_ad'] else 'Out')
    sp('logS_model',      row['sol_sol_model'])
    sp('logPapp_PAMPA',   f"{row['pampa_logPapp']:.2f} ± {row['pampa_logPapp_sd']:.2f} log(cm/s)")
    sp('logPapp_class',   row['pampa_pampa_cat'])
    sp('logPapp_AD',      'In' if row['pampa_pampa_ad'] else 'Out')
    sp('logPapp_model',   row['pampa_pampa_model'])
    sp('MetStab_score',   f"{row['met_met_score']:.3f}")
    sp('MetStab_t12',     row['met_t12_class'])
    sp('Clearance_route', row['met_clearance_route'])
    sp('Met_alerts',      row['met_met_flags'])
    sp('MetStab_model',   row['met_met_model'])
    sp('CYP_risk',        row['cyp_cyp_risk'])
    sp('CYP_alerts',      row['cyp_cyp_alerts'])
    sp('CYP2D6_flag',     str(row['cyp_cyp2d6']))
    sp('CYP3A4_flag',     str(row['cyp_cyp3a4']))
    sp('CYP2C9_flag',     str(row['cyp_cyp2c9']))
    sp('CYP_model',       row['cyp_cyp_model'])
    sp('PPB_pct',         f"{row['ppb_ppb_pct']:.1f} ± 10 %")
    sp('PPB_fu',          f"{row['ppb_ppb_fu']:.4f}")
    sp('PPB_class',       row['ppb_ppb_class'])
    sp('PPB_AD',          'In' if row['ppb_ppb_ad'] else 'Out')
    sp('PPB_model',       row['ppb_ppb_model'])
    sp('hERG_risk',       row['herg_herg_risk'])
    sp('hERG_model',      row['herg_herg_model'])
    db = row['des_breakdown']
    for k in ('sol','logp','perm','met','cyp','ppb','herg','mw'):
        sp(f'des_{k}', f"{db[k]:.3f}")
    writer.write(mol)

writer.close()
import os
print(f"\nresults.sdf rewritten: {os.path.getsize(out_path):,} bytes, {len(top96)} compounds")
