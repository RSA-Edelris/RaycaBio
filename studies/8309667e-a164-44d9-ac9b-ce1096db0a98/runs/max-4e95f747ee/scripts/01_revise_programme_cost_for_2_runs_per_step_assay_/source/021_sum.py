
def ac(mmol, mw_key, eq, price_key):
    return mmol * eq * MW[mw_key] / 1000 * PRICE[price_key]

ASSAY_MMOL = 0.1

# ── MCUF651 Route A: 2 steps ─────────────────────────────────────────────────
assay_mcuf651 = {
    'Step 1 assay': (
        ac(ASSAY_MMOL,'nipecotic_acid',1.0,'nipecotic_acid') +
        ac(ASSAY_MMOL,'amino_F2_BT',1.0,'amino_F2_BT') +
        ASSAY_MMOL * 380.23/1000 * 1.1 * 40 +   # HATU
        ASSAY_MMOL * 103.16/1000 * 2.5 * 5       # DIPEA
    ),
    'Step 2 assay': (
        ASSAY_MMOL * 144.04/1000 * 1.3 * 25      # DMAE-Cl·HCl
    ),
}
n_steps_mcuf = 2
assay_mat_mcuf  = sum(assay_mcuf651.values())
assay_lab_mcuf  = n_steps_mcuf * ASSAY_LCD * LABOUR_RATE
assay_tot_mcuf  = assay_mat_mcuf + assay_lab_mcuf

# ── A317 Route A: 4 main steps + 1 parallel picolylpyrrole acid = 5 assay runs
assay_a317 = {
    'Step 1 Buchwald assay': (
        ac(ASSAY_MMOL,'S_acetylpyrrolidine',1.0,'S_acetylpyrrolidine') +
        ac(ASSAY_MMOL,'bromopyridine',1.1,'bromopyridine') +
        ac(ASSAY_MMOL,'Pd2dba3',0.02,'Pd2dba3') +
        ac(ASSAY_MMOL,'BINAP_rac',0.04,'BINAP_rac') +
        ASSAY_MMOL * 325.82/1000 * 2.0 * 15     # Cs2CO3
    ),
    'Step 2 alpha-Br assay': (
        ASSAY_MMOL * 177.99/1000 * 1.05 * 5     # NBS
    ),
    'Step 3 Hantzsch assay': (
        ASSAY_MMOL * 76.12/1000 * 1.2 * 1       # thiourea
    ),
    'Step 4 amide assay': (
        ASSAY_MMOL * 380.23/1000 * 1.1 * 40 +   # HATU
        ASSAY_MMOL * 103.16/1000 * 2.5 * 5      # DIPEA
    ),
    'Parallel acid assay': (
        ac(ASSAY_MMOL,'pyrrole_COOH',1.0,'pyrrole_COOH') +
        ac(ASSAY_MMOL,'picolyl_Cl_HCl',1.0,'picolyl_Cl_HCl')
    ),
}
n_steps_a317 = 5
assay_mat_a317 = sum(assay_a317.values())
assay_lab_a317 = n_steps_a317 * ASSAY_LCD * LABOUR_RATE
assay_tot_a317 = assay_mat_a317 + assay_lab_a317

# ── 7977 Route B★: 5 steps ───────────────────────────────────────────────────
assay_7977 = {
    'Step 1 SNAr assay': (
        ac(ASSAY_MMOL,'amino_Br_Me_pym',1.0,'amino_Br_Me_pym') +
        ac(ASSAY_MMOL,'Br_NO2_pyr',1.05,'Br_NO2_pyr')
    ),
    'Step 2 Suzuki assay': (
        ac(ASSAY_MMOL,'ClF_Ph_BA',1.1,'ClF_Ph_BA') +
        ASSAY_MMOL * 1155.6/1000 * 0.05 * 150   # PdPPh3_4 (MW ~1156, use PdPPh3_4 price)
    ),
    'Step 3 Fe-red assay': (
        ASSAY_MMOL * 55.85/1000 * 3.0 * 2       # Fe powder (MW 55.85, ~€2/100g)
    ),
    'Step 4 CDI assay': (
        ASSAY_MMOL * 162.15/1000 * 1.2 * 20     # CDI
    ),
    'Step 5 N-alkylation assay': (
        ASSAY_MMOL * 93.51/1000 * 1.2 * 5       # chloroacetamide
    ),
}
n_steps_7977 = 5
assay_mat_7977 = sum(assay_7977.values())
assay_lab_7977 = n_steps_7977 * ASSAY_LCD * LABOUR_RATE
assay_tot_7977 = assay_mat_7977 + assay_lab_7977

# ── Revised totals ─────────────────────────────────────────────────────────────
orig = {'MCUF651':(60,1082,1143,1.25), 'A317':(187,2165,2352,2.5), '7977':(150,2165,2315,2.5)}
additions = {
    'MCUF651': (assay_mat_mcuf, assay_lab_mcuf, assay_tot_mcuf, n_steps_mcuf*ASSAY_LCD),
    'A317':    (assay_mat_a317, assay_lab_a317, assay_tot_a317, n_steps_a317*ASSAY_LCD),
    '7977':    (assay_mat_7977, assay_lab_7977, assay_tot_7977, n_steps_7977*ASSAY_LCD),
}

print("ASSAY-RUN ADDITIONS  (0.1 mmol scouting run before each preparative step)")
print(f"  Assay labour = {ASSAY_LCD} cd/step × €{LABOUR_RATE}/cd = €{ASSAY_LCD*LABOUR_RATE:.0f}/step\n")

for cpd, steps in [('MCUF651',assay_mcuf651),('A317',assay_a317),('7977',assay_7977)]:
    print(f"  {cpd}:")
    for k,v in steps.items():
        print(f"    {k:<35} €{v:.2f} reagents")
    print()

print("─"*72)
print(f"  {'Compound':12} {'Orig mat':>9} {'Orig lab':>9} {'Orig tot':>9} | {'Assay add':>10} {'New total':>10} {'New cd':>7}")
grand_orig = 0; grand_new = 0; grand_cd_new = 0
for cpd in ('MCUF651','A317','7977'):
    om,ol,ot,ocd = orig[cpd]
    am,al,at,acd = additions[cpd]
    nt = ot+at
    ncd = ocd+acd
    grand_orig += ot; grand_new += nt; grand_cd_new += ncd
    print(f"  {cpd:12} {om:>9} {ol:>9} {ot:>9} | {at:>10.0f} {nt:>10.0f} {ncd:>7.2f}")

print(f"  {'ALL THREE':12} {'':>9} {'':>9} {grand_orig:>9} | {grand_new-grand_orig:>10.0f} {grand_new:>10.0f} {grand_cd_new:>7.2f}")
print()
print(f"  Grand total: €{grand_new:.0f}  |  Range: €{round(grand_new*0.80,-1):.0f} – €{round(grand_new*1.35,-1):.0f}")
print(f"  Total chemist-days: {grand_cd_new:.2f} cd  ≈ {grand_cd_new/5:.1f} working weeks")
