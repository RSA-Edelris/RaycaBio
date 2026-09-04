
def mc(mass_mg, key):
    return mass_mg / 1000 * PRICE[key]
def col(crude_mg):
    return crude_mg / 1000 * 12 * 80 / 1000 * 1000 + 5

# ── 7977 Route B ★ RECOMMENDED ───────────────────────────────────────────────
# SNAr(60%) → Suzuki(75%) → Fe-reduction(85%) → CDI-cyclisation(70%) → N-alkylation(65%)
y1,y2,y3,y4,y5 = 0.60, 0.75, 0.85, 0.70, 0.65
mmol_fin = 100 / MW['7977']
mmol_B4  = mmol_fin / y5
mmol_B3  = mmol_B4  / y4
mmol_B2  = mmol_B3  / y3
mmol_B1  = mmol_B2  / y2
mmol_sm  = mmol_B1  / y1
sc       = mmol_sm * 1.20   # +20%

pym_mg   = sc * MW['amino_Br_Me_pym']
nopyr_mg = sc * 1.05 * MW['Br_NO2_pyr']
k2co3_1  = sc * 2.0 * 138.21
BA_mg    = mmol_B1 * 1.10 * MW['ClF_Ph_BA']
Pd4_mg   = mmol_B1 * 0.05 * 1155.6
k2co3_2  = mmol_B1 * 2.0  * 138.21
Fe_mg    = mmol_B2 * 3.0  * 55.85
CDI_mg   = mmol_B3 * 1.20 * 162.15
CAm_mg   = mmol_B4 * 1.20 * 93.51
k2co3_5  = mmol_B4 * 2.0  * 138.21

B1_out = mmol_sm * y1 * MW['B1_7977']
B2_out = mmol_B1 * y2 * MW['B2_7977']
B3_out = mmol_B2 * y3 * MW['B3_7977']
B4_out = mmol_B3 * y4 * MW['B4_7977']

rows_7977 = [
    ('2-Amino-4-bromo-5-Me-pyrimidine',  pym_mg,   'amino_Br_Me_pym','CB','500 mg','1–4 wk'),
    ('3-Bromo-2-nitropyridine',          nopyr_mg, 'Br_NO2_pyr',     'SIG','5 g',  '1–2 d'),
    ('K₂CO₃ (steps 1+5)',                k2co3_1+k2co3_5,'K2CO3',   'SIG','500 g','1 d'),
    ('(2-Cl-4-F-Ph)boronic acid',        BA_mg,    'ClF_Ph_BA',      'SIG','5 g',  '1–3 d'),
    ('Pd(PPh₃)₄',                        Pd4_mg,   'PdPPh3_4',       'SIG','1 g',  '2–5 d'),
    ('Fe powder',                        Fe_mg,    'Fe_powder',       'SIG','500 g','1–2 d'),
    ('CDI',                              CDI_mg,   'CDI',             'SIG','25 g', '1–2 d'),
    ('Chloroacetamide',                  CAm_mg,   'chloroacetamide', 'SIG','100 g','1–2 d'),
]

mat_7977  = sum(mc(r[1],r[2]) for r in rows_7977)
# purification: each step gets column; step3 Fe may crystallise
pur_7977  = col(B1_out) + col(B2_out) + col(B3_out)*0.5 + col(B4_out) + col(100)
sol_7977  = 0.15+0.10+0.05+0.09+0.06   # DMF dioxane EtOH/AcOH THF DMF
lab_7977_cd = 2.5   # SNAr 0.6 + Suzuki 0.65 + Fe-red 0.35 + CDI 0.30 + N-alk 0.60
lab_7977  = lab_7977_cd * LABOUR_RATE
tot_7977  = mat_7977 + sol_7977 + pur_7977 + lab_7977

print("7977 Route B ★ — 100 mg target")
print(f"  Yields: {y1*100:.0f}%/SNAr→{y2*100:.0f}%/Suzuki→{y3*100:.0f}%/Fe-red→{y4*100:.0f}%/CDI→{y5*100:.0f}%/N-alk = {y1*y2*y3*y4*y5*100:.1f}% overall")
print(f"  SM scale: {sc:.3f} mmol  B1={B1_out:.0f}mg  B2={B2_out:.0f}mg  B3={B3_out:.0f}mg  B4={B4_out:.0f}mg  7977=100mg")
print()
print(f"  {'Reagent':<36} {'mg':>8} {'EUR/g':>7} {'EUR':>8}  Src   Lead")
for name,mass,key,sup,pk,lead in rows_7977:
    print(f"  {name:<36} {mass:>8.1f} {PRICE[key]:>7.0f} {mc(mass,key):>8.2f}  {sup:<5} {lead}")
print(f"  {'Solvents (DMF/dioxane/EtOH/THF)':36} {'—':>8} {'':>7} {sol_7977:>8.2f}  SIG")
print(f"  {'Reagent/solvent subtotal':36} {'':>8} {'':>7} {mat_7977+sol_7977:>8.2f}")
print(f"  {'Purification (5 steps, 4 columns)':36} {'':>8} {'':>7} {pur_7977:>8.2f}  EST")
print(f"  {'Labour {:.1f} cd × €{}/cd'.format(lab_7977_cd, LABOUR_RATE):<36} {'':>8} {'':>7} {lab_7977:>8.2f}")
print(f"  {'TOTAL':36} {'':>8} {'':>7} {tot_7977:>8.2f}")
print(f"  Range: €{tot_7977*0.82:.0f} – €{tot_7977*1.35:.0f}")
print()
print("  Critical-path lead time: 2-amino-4-bromo-5-Me-pyrimidine, 1–4 wk (CB make-on-demand risk)")
print()

# ── PROGRAMME SUMMARY ────────────────────────────────────────────────────────
print("═"*60)
print("PROGRAMME SUMMARY")
print("═"*60)
print(f"  {'':12} {'Route':8} {'Steps':6} {'OY%':5} {'Mat+Pur':>10} {'Labour':>10} {'Total':>10}")
print(f"  {'MCUF651':12} {'A':8} {2:6} {'45%':5} {tot_A-lab_A:>10.0f} {lab_A:>10.0f} {tot_A:>10.0f}")
print(f"  {'A317':12} {'A':8} {4:6} {'15.5%':5} {tot_A317-lab_A317:>10.0f} {lab_A317:>10.0f} {tot_A317:>10.0f}")
print(f"  {'7977':12} {'B★':8} {5:6} {'22.1%':5} {tot_7977-lab_7977:>10.0f} {lab_7977:>10.0f} {tot_7977:>10.0f}")
grand = tot_A + tot_A317 + tot_7977
print(f"  {'ALL THREE':12} {'':8} {'':6} {'':5} {(tot_A+tot_A317+tot_7977)-(lab_A+lab_A317+lab_7977):>10.0f} {lab_A+lab_A317+lab_7977:>10.0f} {grand:>10.0f}")
print()
print(f"  Grand total (all three, sequential chemist): €{grand:.0f}")
print(f"  Range: €{grand*0.83:.0f} – €{grand*1.33:.0f}")
