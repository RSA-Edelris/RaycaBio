
# ── MPO desirability functions ────────────────────────────────────────────────
# Rationale for weights: PPI stabilisers bind large hydrophobic interfaces;
#   they sit at MW 400-650 and cLogP 2-4, tolerate moderate PPB,
#   still need cell permeability (intracellular target), and carry
#   the same safety obligations (hERG, CYP) as any clinical candidate.

WEIGHTS = {
    'sol':  1.5,   # Cell-assay solubility is critical — cannot test below ~10 µM
    'logp': 1.0,   # Moderate: cLogP 2-4 preferred but 4-5 accepted for PPI
    'perm': 1.5,   # Cell permeability needed for intracellular PPI target
    'met':  1.5,   # HLM stability; feeds in-vivo window
    'cyp':  1.5,   # Multi-isoform CYP inhibition → pharmacokinetic interactions
    'ppb':  0.5,   # Lower weight: high PPB expected + acceptable for PPI probes
    'herg': 2.0,   # Cardiac safety: hard penalise
    'mw':   0.5,   # Informational: larger accepted for PPI but not a gate
}
TOTAL_W = sum(WEIGHTS.values())  # 10.0

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def linear_des(v, lo_bad, hi_good):
    """Linearly maps v from 0 (at lo_bad) to 1 (at hi_good)."""
    if v <= lo_bad:  return 0.0
    if v >= hi_good: return 1.0
    return (v - lo_bad) / (hi_good - lo_bad)

def trapezoid_des(v, lo0, lo1, hi1, hi0):
    """Trapezoidal desirability: 0 outside [lo0,hi0], 1 inside [lo1,hi1]."""
    if v <= lo0 or v >= hi0:  return 0.0
    if lo1 <= v <= hi1:       return 1.0
    if v < lo1: return (v - lo0) / (lo1 - lo0)
    return (hi0 - v) / (hi0 - hi1)

def des_sol(logs):
    return linear_des(logs, -5.5, -3.0)

def des_logp(clogp):
    # optimal 2–4 for PPI; d=0 at ≤0 or ≥5.5
    return trapezoid_des(clogp, 0.0, 2.0, 4.0, 5.5)

def des_perm(logpapp):
    return linear_des(logpapp, -7.0, -5.5)

def des_met(met_score):
    return float(met_score)

def des_cyp(risk):
    return {'Low': 1.0, 'Medium': 0.5, 'High': 0.0}.get(risk, 0.0)

def des_ppb(fu):
    if fu >= 0.05:   return 1.0
    if fu >= 0.01:   return 0.7
    return 0.3

def des_herg(risk):
    return {'Low': 1.0, 'Medium': 0.5, 'High': 0.0}.get(risk, 0.0)

def des_mw(mw):
    # 400–650 ideal; 0 at <200 or >850
    return trapezoid_des(mw, 200, 400, 650, 850)

def compute_mpo(row):
    d = {
        'sol':  des_sol(row['sol_logS']),
        'logp': des_logp(row['clogp']),
        'perm': des_perm(row['pampa_logPapp']),
        'met':  des_met(row['met_met_score']),
        'cyp':  des_cyp(row['cyp_cyp_risk']),
        'ppb':  des_ppb(row['ppb_ppb_fu']),
        'herg': des_herg(row['herg_herg_risk']),
        'mw':   des_mw(row['mw']),
    }
    mpo = sum(WEIGHTS[k]*v for k,v in d.items()) / TOTAL_W
    return round(mpo, 4), d

# ── Apply MPO + filters ───────────────────────────────────────────────────────
HARD_FILTERS = {
    'solubility':   ('sol_logS',        lambda v: v >= -5.5,    'logS < -5.5 (< 3 µM)'),
    'permeability': ('pampa_pampa_cat', lambda v: v != 'Low',   'PAMPA Low permeability'),
    'hERG':         ('herg_herg_risk',  lambda v: v != 'High',  'hERG High risk'),
    'CYP':          ('cyp_cyp_risk',    lambda v: v != 'High',  'CYP High multi-isoform risk'),
}

for row in rows:
    mpo, des_breakdown = compute_mpo(row)
    row['mpo_score']     = mpo
    row['des_breakdown'] = des_breakdown
    # Hard filters
    failed_filters = []
    for fname, (field, test, label) in HARD_FILTERS.items():
        if not test(row[field]):
            failed_filters.append(label)
    row['filter_fails']  = '; '.join(failed_filters)
    row['passes_filter'] = len(failed_filters) == 0

# ── Shortlist: passing compounds, ranked by MPO ───────────────────────────────
shortlist = sorted([r for r in rows if r['passes_filter']],
                   key=lambda r: -r['mpo_score'])
rejected  = [r for r in rows if not r['passes_filter']]

# ── Structural override list: rejected by ≤1 property but borderline ─────────
override_candidates = [r for r in rejected
                       if len(r['filter_fails'].split(';')) == 1
                       and r['mpo_score'] >= 0.55]

print(f"Total scored      : {len(rows)}")
print(f"Pass all filters  : {len(shortlist)}")
print(f"Rejected          : {len(rejected)}")
print(f"Override candidates (1 fail, MPO≥0.55): {len(override_candidates)}")
print(f"\nTop-5 MPO scores  : {[r['mpo_score'] for r in shortlist[:5]]}")
print(f"Bottom-5 MPO (shortlist): {[r['mpo_score'] for r in shortlist[-5:]]}")
print(f"\nRejection reason breakdown:")
from collections import Counter
all_fails = [f.strip() for r in rejected for f in r['filter_fails'].split(';')]
for reason, cnt in Counter(all_fails).most_common():
    print(f"  {cnt:3d}  {reason}")
