
MW = {
    'MCUF651': 355, 'A317': 395, '7977': 388,
    'nipecotic_acid': 129.16, 'amino_F2_BT': 202.19, 'DMAE_Cl_HCl': 144.04,
    'A1_MCUF651': 313,
    'S_acetylpyrrolidine': 113.16, 'bromopyridine': 157.99,
    'A1_A317': 198, 'A2_A317': 277, 'A3_A317': 256,
    'picolyl_pyrrole_acid': 202.21, 'pyrrole_COOH': 111.10, 'picolyl_Cl_HCl': 164.04,
    'amino_Br_Me_pym': 188.04, 'Br_NO2_pyr': 203.01,
    'B1_7977': 324, 'ClF_Ph_BA': 174.97,
    'B2_7977': 390, 'B3_7977': 360, 'B4_7977': 388,
    'chloroacetamide': 93.51,
}
PRICE = {
    'K2CO3': 1, 'HATU': 40, 'DIPEA': 5, 'NBS': 5, 'thiourea': 1,
    'CDI': 20, 'Fe_powder': 2, 'AcOH_g': 1, 'chloroacetamide': 5,
    'Cs2CO3': 15, 'nipecotic_acid': 45, 'amino_F2_BT': 90, 'DMAE_Cl_HCl': 25,
    'S_acetylpyrrolidine': 130, 'bromopyridine': 15, 'Pd2dba3': 250,
    'BINAP_rac': 500, 'pyrrole_COOH': 35, 'picolyl_Cl_HCl': 30,
    'amino_Br_Me_pym': 75, 'Br_NO2_pyr': 40, 'ClF_Ph_BA': 50,
    'PdPPh3_4': 150,
}
SOURCE = {
    'K2CO3':'SIG','HATU':'SIG','DIPEA':'SIG','NBS':'SIG','thiourea':'SIG',
    'CDI':'SIG','Fe_powder':'SIG','AcOH_g':'SIG','chloroacetamide':'SIG',
    'Cs2CO3':'SIG','nipecotic_acid':'SIG','amino_F2_BT':'CB','DMAE_Cl_HCl':'SIG',
    'S_acetylpyrrolidine':'SIG','bromopyridine':'SIG','Pd2dba3':'SIG',
    'BINAP_rac':'SIG','pyrrole_COOH':'SIG','picolyl_Cl_HCl':'CB',
    'amino_Br_Me_pym':'CB','Br_NO2_pyr':'SIG','ClF_Ph_BA':'SIG','PdPPh3_4':'SIG',
}
LABOUR_RATE = 866

def mc(mass_mg, key):
    return mass_mg / 1000 * PRICE[key]

def col(crude_mg):
    return crude_mg / 1000 * 12 * 80 / 1000 * 1000 + 5

# ── MCUF651 Route A ──────────────────────────────────────────────────────────
y1, y2 = 0.72, 0.63
mmol_fin  = 100 / MW['MCUF651']
mmol_A1   = mmol_fin / y2
mmol_sm   = mmol_A1 / y1
sc        = mmol_sm * 1.25   # practical +25%

nip_mg    = sc * MW['nipecotic_acid']
bt_mg     = sc * MW['amino_F2_BT']
hatu_mg   = sc * 1.10 * 380.23
DIPEA_mg  = sc * 2.5 * 129.25
dmae_mg   = mmol_A1 * 1.3 * MW['DMAE_Cl_HCl']
A1_mg_out = mmol_sm * y1 * MW['A1_MCUF651']   # what is actually produced

rows_A = [
    ('(R)-Nipecotic acid',            nip_mg,   'nipecotic_acid', 'SIG', '1 g'),
    ('2-Amino-5,6-F₂-benzothiazole',  bt_mg,    'amino_F2_BT',    'CB',  '500 mg'),
    ('HATU',                          hatu_mg,  'HATU',           'SIG', '5 g'),
    ('DIPEA',                         DIPEA_mg, 'DIPEA',          'SIG', '100 mL'),
    ('2-(DMAE)Cl·HCl',                dmae_mg,  'DMAE_Cl_HCl',    'SIG', '5 g'),
    ('K₂CO₃',                         mmol_A1*2*138.21, 'K2CO3', 'SIG', '500 g'),
]

mat_A = sum(mc(r[1], r[2]) for r in rows_A)
pur_A = col(A1_mg_out) + 10   # step-1 column; step-2 aqueous wash only
lab_A_cd = 1.25
lab_A    = lab_A_cd * LABOUR_RATE
tot_A    = mat_A + pur_A + lab_A

print("MCUF651 Route A — 100 mg target")
print(f"  Yields: step1 {y1*100:.0f}%, step2 {y2*100:.0f}% → {y1*y2*100:.1f}% overall")
print(f"  mmol at SM stage: {sc:.3f} mmol  →  A1 intermediate: {A1_mg_out:.0f} mg  →  MCUF651: 100 mg")
print()
print(f"  {'Reagent':<36} {'mg':>8} {'EUR/g':>7} {'EUR':>8}  Supplier  Pack")
for name, mass_mg, key, sup, pk in rows_A:
    print(f"  {name:<36} {mass_mg:>8.1f} {PRICE[key]:>7.0f} {mc(mass_mg,key):>8.2f}  {sup:<8}  {pk}")
print(f"  {'DMF 5 mL':36} {'—':>8} {'':>7} {'0.08':>8}  SIG")
print(f"  {'MeCN 5 mL':36} {'—':>8} {'':>7} {'0.06':>8}  SIG")
print(f"  {'Reagent/solvent subtotal':36} {'':>8} {'':>7} {mat_A:>8.2f}")
print(f"  {'Column chromatography ×2':36} {'':>8} {'':>7} {pur_A:>8.2f}  EST")
print(f"  {'Labour {:.2f} cd × €{}/cd'.format(lab_A_cd, LABOUR_RATE):<36} {'':>8} {'':>7} {lab_A:>8.2f}")
print(f"  {'TOTAL':36} {'':>8} {'':>7} {tot_A:>8.2f}")
print(f"  Range: €{tot_A*0.85:.0f} – €{tot_A*1.30:.0f}")
