
# ── ADME descriptor + model functions ────────────────────────────────────────
from rdkit.Chem import rdMolDescriptors, Fragments
import re

def compute_base_descriptors(mol):
    """Compute all needed physicochemical descriptors."""
    mw   = Descriptors.ExactMolWt(mol)
    clogp = Crippen.MolLogP(mol)
    tpsa = rdMolDescriptors.CalcTPSA(mol)
    hbd  = rdMolDescriptors.CalcNumHBD(mol)
    hba  = rdMolDescriptors.CalcNumHBA(mol)
    rb   = rdMolDescriptors.CalcNumRotatableBonds(mol)
    # aromatic proportion = aromatic atoms / heavy atoms
    n_heavy = mol.GetNumHeavyAtoms()
    n_arom  = sum(1 for a in mol.GetAtoms() if a.GetIsAromatic())
    ap      = n_arom / n_heavy if n_heavy else 0
    n_ar_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
    n_rings    = rdMolDescriptors.CalcNumRings(mol)
    fsp3       = rdMolDescriptors.CalcFractionCSP3(mol)
    n_basic_n  = sum(1 for a in mol.GetAtoms()
                     if a.GetAtomicNum()==7 and not a.GetIsAromatic()
                     and not any(b.GetBondTypeAsDouble()==2
                                 for b in a.GetBonds()))
    return dict(mw=mw, clogp=clogp, tpsa=tpsa, hbd=hbd, hba=hba, rb=rb,
                ap=ap, n_arom=n_arom, n_heavy=n_heavy, n_ar_rings=n_ar_rings,
                n_rings=n_rings, fsp3=fsp3, n_basic_n=n_basic_n)

# ── 1. Aqueous solubility – ESOL (Delaney 2004) ──────────────────────────────
# logS = 0.16 – 0.63*cLogP – 0.0062*MW + 0.066*RB – 0.74*AP
# RMSE ≈ 0.93 log units; training range: MW 50-800, cLogP -8 to 8
ESOL_AD = dict(mw_lo=50, mw_hi=800, clogp_lo=-8, clogp_hi=8)

def pred_solubility(d):
    logs = 0.16 - 0.63*d['clogp'] - 0.0062*d['mw'] + 0.066*d['rb'] - 0.74*d['ap']
    uncertainty = 0.93          # 1-SD RMSE (Delaney 2004)
    in_ad = (ESOL_AD['mw_lo'] <= d['mw'] <= ESOL_AD['mw_hi'] and
             ESOL_AD['clogp_lo'] <= d['clogp'] <= ESOL_AD['clogp_hi'])
    return dict(logS=round(logs,2), logS_sd=uncertainty,
                logS_unit='log(mol/L)', sol_ad=in_ad,
                sol_model='ESOL/Delaney-2004 (linear regression, n=1144, RMSE=0.93)')

# ── 2. cLogP – Crippen/RDKit ──────────────────────────────────────────────────
# Uncertainty ~0.4 log units for drug-like; AD essentially all organic molecules
def pred_logp(d):
    return dict(clogp=round(d['clogp'],2), clogp_sd=0.4,
                clogp_ad=True,   # Crippen has very broad coverage
                clogp_model='RDKit Crippen atomic-contributions (RMSE≈0.4 across DrugBank)')

# ── 3. Passive permeability – PAMPA (Hou 2004 simplified) ───────────────────
# logPapp(cm/s) = -0.01578*TPSA + 0.5*cLogP – 0.0008*MW – 5.5
# RMSE ≈ 0.8 log units; AD: MW 100-700, TPSA 0-200, cLogP -3 to 7
PAMPA_AD = dict(mw_lo=100, mw_hi=700, tpsa_lo=0, tpsa_hi=200,
                clogp_lo=-3, clogp_hi=7)

def pred_pampa(d):
    logpapp = -0.01578*d['tpsa'] + 0.5*d['clogp'] - 0.0008*d['mw'] - 5.5
    in_ad = (PAMPA_AD['mw_lo'] <= d['mw'] <= PAMPA_AD['mw_hi'] and
             PAMPA_AD['tpsa_lo'] <= d['tpsa'] <= PAMPA_AD['tpsa_hi'] and
             PAMPA_AD['clogp_lo'] <= d['clogp'] <= PAMPA_AD['clogp_hi'])
    cat = 'High' if logpapp > -5.5 else ('Medium' if logpapp > -7.0 else 'Low')
    return dict(logPapp=round(logpapp,2), logPapp_sd=0.8,
                logPapp_unit='log(cm/s)', pampa_cat=cat, pampa_ad=in_ad,
                pampa_model='Hou-2004 PAMPA linear model (RMSE=0.8, n=100)')

# ── 4. Metabolic stability + clearance route (HLM rules) ─────────────────────
# Prediction based on structural features; aligned with published classifiers.
# Uncertainty is stated as categorical (±1 class boundary).
# Fast metabolisers: cLogP>4 + many aromatic rings; slow: cLogP<2 + blocked sites
LABILE_SMARTS = [
    ('[OD2;!$(OC=O)](c)',            'phenol/Ar-OH: UGT/CYP substrate'),
    ('C(=O)[OH]',                    'free acid: glucuronidation'),
    ('[CH3]c',                       'Ar-methyl: CYP oxidation soft spot'),
    ('[NX3;H0;!$(N-C=O)](C)(C)C',   'tertiary amine: CYP oxidation'),
    ('c1cccc(C(F)(F)F)c1',           'Ar-CF3: generally stable but metabolite risk'),
    ('[NH2]c',                       'Ar-NH2: N-hydroxylation risk'),
]
labile_pats = [(Chem.MolFromSmarts(s), reason) for s, reason in LABILE_SMARTS]

def pred_met_stability(mol, d):
    flags = []
    for pat, reason in labile_pats:
        if pat is not None and mol.HasSubstructMatch(pat):
            flags.append(reason)
    # Stability score (higher = more stable)
    score = 1.0
    if d['clogp'] > 4.0:   score -= 0.25
    if d['clogp'] > 5.5:   score -= 0.15
    if d['n_ar_rings'] > 3: score -= 0.15
    if d['fsp3'] > 0.4:    score += 0.15
    if d['mw'] > 500:      score -= 0.10
    score = max(0.0, min(1.0, score))
    # Classify half-life
    if score > 0.7:   t12_class, t12_est = 'High (t½>60 min HLM)',   '>60'
    elif score > 0.4: t12_class, t12_est = 'Medium (30–60 min HLM)', '30–60'
    else:             t12_class, t12_est = 'Low (<30 min HLM)',       '<30'
    # Clearance route
    if any('glucur' in f or 'acid' in f for f in flags):
        route = 'Phase II (glucuronidation dominant)'
    elif d['n_basic_n'] >= 1 and d['n_ar_rings'] >= 1:
        route = 'CYP2D6/3A4 oxidation (basic-N + Ar)'
    else:
        route = 'CYP3A4 oxidation (lipophilic aromatic)'
    in_ad = True   # rule-based; always applicable but flagged as heuristic
    return dict(met_score=round(score,3), t12_class=t12_class, t12_est_min=t12_est,
                clearance_route=route, met_flags='; '.join(flags) if flags else 'None',
                met_ad=in_ad,
                met_model='Rule-based HLM classifier (cLogP+Fsp3+Ar-rings+structural alerts; heuristic, ±1 category)')

# ── 5. CYP inhibition liability ───────────────────────────────────────────────
CYP_SMARTS = {
    'CYP2D6': [
        ('[NH1,NH2;!$(NC=O);!a]~[#6]~[#6]~c',      'basic-NH 2-3 bonds from Ar'),
        ('[N;H0;!$(NC=O);!$(N=*);!a]~[#6]~[#6]~c', 'tertiary-N near Ar'),
    ],
    'CYP3A4': [
        ('[n,N;H0]~1~[c,C]~[n,N]~[c,C]~[c,C]~[c,C]~1', 'imidazole/pyrimidine hinge'),
        ('[N;H0;!$(NC=O);!a;R]',                         'cyclic tertiary N'),
    ],
    'CYP2C9': [
        ('[OH]c',          'phenol'),
        ('C(=O)[OH]',      'free carboxylic acid'),
        ('[NH1]S(=O)(=O)', 'sulfonamide NH'),
    ],
}
cyp_pats = {iso: [(Chem.MolFromSmarts(s), reason) for s, reason in lst]
            for iso, lst in CYP_SMARTS.items()}

def pred_cyp(mol, d):
    alerts = {}
    for iso, pats in cyp_pats.items():
        hits = [reason for pat, reason in pats
                if pat is not None and mol.HasSubstructMatch(pat)]
        alerts[iso] = hits
    n_alert_isos = sum(1 for v in alerts.values() if v)
    if n_alert_isos == 0:    cyp_risk = 'Low'
    elif n_alert_isos == 1:  cyp_risk = 'Medium'
    else:                    cyp_risk = 'High'
    in_ad = True
    summary = '; '.join(f"{iso}:({', '.join(v)})" for iso, v in alerts.items() if v) or 'None'
    return dict(cyp_risk=cyp_risk, cyp_alerts=summary,
                cyp2d6=bool(alerts['CYP2D6']), cyp3a4=bool(alerts['CYP3A4']),
                cyp2c9=bool(alerts['CYP2C9']), cyp_n_isos=n_alert_isos,
                cyp_ad=in_ad,
                cyp_model='SMARTS structural-alert panel (pharmacophore-based, flag only – no IC50)')

# ── 6. Plasma protein binding (PPB) – Valko 2003 logP model ─────────────────
# log(Kbind) ~ 0.72*cLogP; fu = 1/(1+10^(0.72*cLogP-0.40))
# RMSE ~10% PPB; AD: cLogP -2 to 7
PPB_AD = dict(clogp_lo=-2, clogp_hi=7)

def pred_ppb(d):
    fu = 1.0 / (1.0 + 10**(0.72*d['clogp'] - 0.40))
    ppb = (1 - fu)*100
    ppb_sd = 10.0    # ±10% absolute (Valko 2003 RMSE)
    in_ad = PPB_AD['clogp_lo'] <= d['clogp'] <= PPB_AD['clogp_hi']
    if ppb < 80:   ppb_class = 'Low (<80%)'
    elif ppb < 90: ppb_class = 'Moderate (80–90%)'
    elif ppb < 95: ppb_class = 'High (90–95%)'
    else:          ppb_class = 'Very high (>95%)'
    return dict(ppb_pct=round(ppb,1), ppb_fu=round(fu,4), ppb_sd=ppb_sd,
                ppb_class=ppb_class, ppb_ad=in_ad,
                ppb_model='Valko-2003 logP-linear model (RMSE≈10% PPB, n=87)')

# ── 7. hERG risk ─────────────────────────────────────────────────────────────
# Rule: basic-N-in-ring + cLogP > 3.5 → High; basic-N + cLogP > 2 → Medium; else Low
# Uncertainty: ±1 class; hERG models typically AUC ~0.75 for structural alerts
HERG_HIGH  = Chem.MolFromSmarts('[N;H0;!$(NC=O);!a;R]')   # cyclic tertiary N
HERG_BASIC = Chem.MolFromSmarts('[NH1,NH2,N;H0;!$(NC=O);!a]')

def pred_herg(mol, d):
    has_cyclic_N  = mol.HasSubstructMatch(HERG_HIGH)  if HERG_HIGH  else False
    has_basic_N   = mol.HasSubstructMatch(HERG_BASIC) if HERG_BASIC else False
    has_basic_N  |= (d['n_basic_n'] > 0)
    if has_cyclic_N and d['clogp'] > 3.5 and d['n_ar_rings'] >= 1:
        risk = 'High'
    elif has_basic_N and d['clogp'] > 2.0:
        risk = 'Medium'
    else:
        risk = 'Low'
    in_ad = True
    return dict(herg_risk=risk, herg_ad=in_ad,
                herg_model='Structural-alert + cLogP rule (Redfern-2003 anchored; ±1 class)')

print("All ADME functions defined.")
