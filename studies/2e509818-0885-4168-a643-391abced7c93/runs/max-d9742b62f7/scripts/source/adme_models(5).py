
import warnings
warnings.filterwarnings("ignore")
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, Crippen

ESOL_AD  = dict(mw_lo=50,  mw_hi=800, clogp_lo=-8, clogp_hi=8)
PAMPA_AD = dict(mw_lo=100, mw_hi=700, tpsa_lo=0, tpsa_hi=200, clogp_lo=-3, clogp_hi=7)
PPB_AD   = dict(clogp_lo=-2, clogp_hi=7)

def compute_base_descriptors(mol):
    mw   = Descriptors.ExactMolWt(mol)
    clogp= Crippen.MolLogP(mol)
    tpsa = rdMolDescriptors.CalcTPSA(mol)
    hbd  = rdMolDescriptors.CalcNumHBD(mol)
    hba  = rdMolDescriptors.CalcNumHBA(mol)
    rb   = rdMolDescriptors.CalcNumRotatableBonds(mol)
    n_heavy  = mol.GetNumHeavyAtoms()
    n_arom   = sum(1 for a in mol.GetAtoms() if a.GetIsAromatic())
    ap       = n_arom / n_heavy if n_heavy else 0
    n_ar_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
    n_rings    = rdMolDescriptors.CalcNumRings(mol)
    fsp3       = rdMolDescriptors.CalcFractionCSP3(mol)
    # Exclude amide N: check that no neighbouring C carries a C=O (double bond to O)
    n_basic_n  = sum(1 for a in mol.GetAtoms()
                     if a.GetAtomicNum()==7 and not a.GetIsAromatic()
                     and not any(b.GetBondTypeAsDouble()==2 for b in a.GetBonds())
                     and not any(nb.GetAtomicNum()==6 and
                                 any(b2.GetBondTypeAsDouble()==2 for b2 in nb.GetBonds())
                                 for nb in a.GetNeighbors()))
    return dict(mw=mw, clogp=clogp, tpsa=tpsa, hbd=hbd, hba=hba, rb=rb,
                ap=ap, n_arom=n_arom, n_heavy=n_heavy,
                n_ar_rings=n_ar_rings, n_rings=n_rings, fsp3=fsp3,
                n_basic_n=n_basic_n)

def pred_solubility(d):
    logs = 0.16 - 0.63*d["clogp"] - 0.0062*d["mw"] + 0.066*d["rb"] - 0.74*d["ap"]
    in_ad = (ESOL_AD["mw_lo"]<=d["mw"]<=ESOL_AD["mw_hi"] and
             ESOL_AD["clogp_lo"]<=d["clogp"]<=ESOL_AD["clogp_hi"])
    return dict(logS=round(logs,2), logS_sd=0.93, logS_unit="log(mol/L)",
                sol_ad=in_ad,
                sol_model="ESOL/Delaney-2004 (linear, n=1144, RMSE=0.93 log-units)")

def pred_pampa(d):
    logpapp = -0.01578*d["tpsa"] + 0.5*d["clogp"] - 0.0008*d["mw"] - 5.5
    in_ad = (PAMPA_AD["mw_lo"]<=d["mw"]<=PAMPA_AD["mw_hi"] and
             PAMPA_AD["tpsa_lo"]<=d["tpsa"]<=PAMPA_AD["tpsa_hi"] and
             PAMPA_AD["clogp_lo"]<=d["clogp"]<=PAMPA_AD["clogp_hi"])
    cat = "High" if logpapp>-5.5 else ("Medium" if logpapp>-7.0 else "Low")
    return dict(logPapp=round(logpapp,2), logPapp_sd=0.8,
                logPapp_unit="log(cm/s)", pampa_cat=cat, pampa_ad=in_ad,
                pampa_model="Hou-2004 PAMPA linear (RMSE=0.8, n=100)")

LABILE_PATS = [
    (Chem.MolFromSmarts("[OD2;!$(OC=O)](c)"),           "phenol: UGT/CYP"),
    (Chem.MolFromSmarts("C(=O)[OH]"),                   "free acid: glucuronidation"),
    (Chem.MolFromSmarts("[CH3]c"),                       "Ar-CH3: CYP soft spot"),
    (Chem.MolFromSmarts("[NX3;H0;!$(NC=O)](C)(C)C"),    "tert-amine: CYP"),
    (Chem.MolFromSmarts("[NH2]c"),                       "Ar-NH2: N-hydroxylation"),
    (Chem.MolFromSmarts("c1cccc(C(F)(F)F)c1"),          "Ar-CF3: oxidative metabolite risk"),
]

def pred_met_stability(mol, d):
    flags = [r for pat, r in LABILE_PATS if pat and mol.HasSubstructMatch(pat)]
    s = 1.0
    if d["clogp"] > 4.0:    s -= 0.25
    if d["clogp"] > 5.5:    s -= 0.15
    if d["n_ar_rings"] > 3: s -= 0.15
    if d["fsp3"] > 0.4:     s += 0.15
    if d["mw"] > 500:       s -= 0.10
    s = max(0.0, min(1.0, s))
    if s > 0.7:   t12, t12e = "High (t½>60 min HLM)",   ">60"
    elif s > 0.4: t12, t12e = "Medium (30-60 min HLM)", "30-60"
    else:         t12, t12e = "Low (<30 min HLM)",       "<30"
    if any("glucur" in f or "acid" in f for f in flags):
        route = "Phase-II (glucuronidation)"
    elif d["n_basic_n"]>=1 and d["n_ar_rings"]>=1:
        route = "CYP2D6/3A4 (basic-N + Ar)"
    else:
        route = "CYP3A4 (lipophilic Ar)"
    return dict(met_score=round(s,3), t12_class=t12, t12_est_min=t12e,
                clearance_route=route,
                met_flags="; ".join(flags) if flags else "None",
                met_ad=True,
                met_model="Rule-based HLM classifier (cLogP+Fsp3+Ar-rings+alerts; heuristic ±1 class)")

CYP_PATS = {
    "CYP2D6": [
        (Chem.MolFromSmarts("[NH1,NH2;!$(NC=O);!a]~[#6]~[#6]~c"), "basic-NH near Ar"),
        (Chem.MolFromSmarts("[N;H0;!$(NC=O);!$(N=*);!a]~[#6]~[#6]~c"), "tert-N near Ar"),
    ],
    "CYP3A4": [
        (Chem.MolFromSmarts("[n,N;H0]1[c,C][n,N][c,C][c,C][c,C]1"), "imidazole/pyrimidine"),
        (Chem.MolFromSmarts("[N;H0;!$(NC=O);!a;R]"), "cyclic tert-N"),
    ],
    "CYP2C9": [
        (Chem.MolFromSmarts("[OH]c"),           "phenol"),
        (Chem.MolFromSmarts("C(=O)[OH]"),       "free COOH"),
        (Chem.MolFromSmarts("[NH1]S(=O)(=O)"), "sulfonamide NH"),
    ],
}

def pred_cyp(mol, d):
    alerts = {iso: [r for pat, r in pats if pat and mol.HasSubstructMatch(pat)]
              for iso, pats in CYP_PATS.items()}
    n = sum(1 for v in alerts.values() if v)
    risk = "Low" if n==0 else ("Medium" if n==1 else "High")
    summ = "; ".join(f"{i}:({', '.join(v)})" for i,v in alerts.items() if v) or "None"
    return dict(cyp_risk=risk, cyp_alerts=summ,
                cyp2d6=bool(alerts["CYP2D6"]),
                cyp3a4=bool(alerts["CYP3A4"]),
                cyp2c9=bool(alerts["CYP2C9"]),
                cyp_n_isos=n, cyp_ad=True,
                cyp_model="SMARTS alert panel (pharmacophore-based; flag only – no IC50 predicted)")

def pred_ppb(d):
    fu  = 1.0 / (1.0 + 10**(0.72*d["clogp"] - 0.40))
    ppb = (1-fu)*100
    in_ad = PPB_AD["clogp_lo"]<=d["clogp"]<=PPB_AD["clogp_hi"]
    cls = ("Low (<80%)" if ppb<80 else
           "Moderate (80-90%)" if ppb<90 else
           "High (90-95%)" if ppb<95 else "Very high (>95%)")
    return dict(ppb_pct=round(ppb,1), ppb_fu=round(fu,4), ppb_sd=10.0,
                ppb_class=cls, ppb_ad=in_ad,
                ppb_model="Valko-2003 logP-linear (RMSE≈10% PPB, n=87)")

HERG_CYCLIC = Chem.MolFromSmarts("[N;H0;!$(NC=O);!a;R]")
HERG_BASIC  = Chem.MolFromSmarts("[N;!$(NC=O);!a]")

def pred_herg(mol, d):
    cyc = HERG_CYCLIC and mol.HasSubstructMatch(HERG_CYCLIC)
    bas = bool(HERG_BASIC and mol.HasSubstructMatch(HERG_BASIC))
    if cyc and d["clogp"]>3.5 and d["n_ar_rings"]>=1:
        risk = "High"
    elif bas and d["clogp"]>2.0:
        risk = "Medium"
    else:
        risk = "Low"
    return dict(herg_risk=risk, herg_ad=True,
                herg_model="Structural-alert + cLogP heuristic (thresholds from general hERG SAR literature; ±1 class)")
