
def mc(mass_mg, key):
    return mass_mg / 1000 * PRICE[key]

def col(crude_mg):
    return crude_mg / 1000 * 12 * 80 / 1000 * 1000 + 5

# ── A317 Route A ─────────────────────────────────────────────────────────────
# Steps: Buchwald(65%) → alpha-Br(70%) → Hantzsch(62%) → amide(55%)
# + parallel picolylpyrrole acid synthesis (70%)
y1,y2,y3,y4 = 0.65, 0.70, 0.62, 0.55
mmol_fin = 100 / MW['A317']                     # 0.253 mmol
mmol_A3  = mmol_fin / y4                         # input to step4
mmol_A2  = mmol_A3  / y3                         # input to step3
mmol_A1  = mmol_A2  / y2                         # input to step2
mmol_sm  = mmol_A1  / y1                         # SM input
sc       = mmol_sm * 1.20                        # +20%

acpyr_mg = sc * MW['S_acetylpyrrolidine']
brpyr_mg = sc * 1.05 * MW['bromopyridine']
Pd_mg    = sc * 0.02 * 915.67   # Pd2(dba)3, 2 mol%
BP_mg    = sc * 0.04 * 622.67   # BINAP, 4 mol%
Cs2_mg   = sc * 2.0  * 325.82
NBS_mg   = mmol_A1 * 1.05 * 177.99
thio_mg  = mmol_A2 * 1.20 * 76.12
hatu2_mg = mmol_A3 * 1.10 * 380.23
DIPEA2_mg= mmol_A3 * 2.5  * 129.25

# picolylpyrrole acid (parallel, 70% yield, 1.05eq relative to step4 input)
mmol_pic = mmol_A3 / 0.70 * 1.05
pyC_mg   = mmol_pic * MW['pyrrole_COOH']
piclCl_mg= mmol_pic * MW['picolyl_Cl_HCl']

# intermediate masses produced
A1_out = mmol_sm * y1 * MW['A1_A317']
A2_out = mmol_A1 * y2 * MW['A2_A317']
A3_out = mmol_A2 * y3 * MW['A3_A317']
pic_out= mmol_pic * 0.70 * MW['picolyl_pyrrole_acid']

rows_A317_step1 = [
    ('(S)-2-Acetylpyrrolidine',      acpyr_mg,'S_acetylpyrrolidine','SIG','1 g',     '2–3 wk'),
    ('2-Bromopyridine',              brpyr_mg,'bromopyridine',      'SIG','100 mL',  '1–2 d'),
    ('Pd₂(dba)₃',                   Pd_mg,   'Pd2dba3',           'SIG','1 g',     '2–5 d'),
    ('(±)-BINAP',                    BP_mg,   'BINAP_rac',         'SIG','1 g',     '2–5 d'),
    ('Cs₂CO₃',                       Cs2_mg,  'Cs2CO3',            'SIG','500 g',   '1–2 d'),
]
rows_A317_step2 = [('NBS', NBS_mg,'NBS','SIG','50 g','1–2 d')]
rows_A317_step3 = [('Thiourea', thio_mg,'thiourea','SIG','500 g','1–2 d')]
rows_A317_step4 = [
    ('HATU',  hatu2_mg,'HATU', 'SIG','5 g','1–2 d'),
    ('DIPEA', DIPEA2_mg,'DIPEA','SIG','100 mL','1–2 d'),
]
rows_A317_pic = [
    ('Pyrrole-2-carboxylic acid',   pyC_mg,   'pyrrole_COOH',  'SIG','1 g','1–2 d'),
    ('4-Picolyl chloride·HCl',      piclCl_mg,'picolyl_Cl_HCl','CB', '1 g','1–5 d'),
]
all_rows_A317 = rows_A317_step1+rows_A317_step2+rows_A317_step3+rows_A317_step4+rows_A317_pic

mat_A317 = sum(mc(r[1],r[2]) for r in all_rows_A317)
pur_A317 = col(A1_out) + 10 + col(A3_out) + col(pic_out)*0.6 + col(100)
lab_A317_cd = 2.5   # Buchwald 0.85 + alpha-Br 0.55 + Hantzsch 0.45 + amide 0.65 + parallel acid (during Buchwald overnight) 0.0 extra
lab_A317 = lab_A317_cd * LABOUR_RATE
tot_A317 = mat_A317 + pur_A317 + lab_A317

print("A317 Route A — 100 mg target")
print(f"  Yields: {y1*100:.0f}%/Buchwald → {y2*100:.0f}%/α-Br → {y3*100:.0f}%/Hantzsch → {y4*100:.0f}%/amide  =  {y1*y2*y3*y4*100:.1f}% overall")
print(f"  SM scale: {sc:.3f} mmol  A1={A1_out:.0f}mg  A2={A2_out:.0f}mg  A3={A3_out:.0f}mg  pic={pic_out:.0f}mg")
print()
print(f"  {'Reagent':<36} {'mg':>8} {'EUR/g':>7} {'EUR':>8}  Src   Lead")
for name,mass,key,sup,pk,lead in all_rows_A317:
    print(f"  {name:<36} {mass:>8.1f} {PRICE[key]:>7.0f} {mc(mass,key):>8.2f}  {sup:<5} {lead}")
sol_A317 = 0.06+0.10+0.06+0.06+0.06  # toluene CHCl3 EtOH DMF DMF
print(f"  {'Solvents (toluene/CHCl₃/EtOH/DMF)':36} {'—':>8} {'':>7} {sol_A317:>8.2f}  SIG")
print(f"  {'Reagent/solvent subtotal':36} {'':>8} {'':>7} {mat_A317+sol_A317:>8.2f}")
print(f"  {'Purification (4 columns)':36} {'':>8} {'':>7} {pur_A317:>8.2f}  EST")
print(f"  {'Labour {:.1f} cd × €{}/cd'.format(lab_A317_cd, LABOUR_RATE):<36} {'':>8} {'':>7} {lab_A317:>8.2f}")
print(f"  {'TOTAL':36} {'':>8} {'':>7} {tot_A317:>8.2f}")
print(f"  Range: €{tot_A317*0.82:.0f} – €{tot_A317*1.35:.0f}")
print()
print("  Critical-path lead time: (S)-2-acetylpyrrolidine, 2–3 weeks (order Day 0)")
print("  Buchwald elucidate on receipt; all other reagents in stock or 2–5 d")
