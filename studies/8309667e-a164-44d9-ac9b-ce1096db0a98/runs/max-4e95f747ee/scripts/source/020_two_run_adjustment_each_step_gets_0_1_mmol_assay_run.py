
# Two-run adjustment: each step gets a 0.1 mmol assay run before the prep run
# Assay labour: 0.35 cd/step (setup 1h, reaction, TLC/LC-MS, simple workup = ~3h)
# Assay reagent cost: proportional to 0.1 mmol / prep mmol at that step
# Precious metals and building blocks are included even at assay scale

ASSAY_MMOL = 0.1
ASSAY_LCD  = 0.35   # chemist-days per assay step
LABOUR_RATE = 866   # EUR/cd

PRICE = {
    'K2CO3':1,'HATU':40,'DIPEA':5,'NBS':5,'thiourea':1,
    'CDI':20,'Fe_powder':2,'chloroacetamide':5,'Cs2CO3':15,
    'nipecotic_acid':45,'amino_F2_BT':90,'DMAE_Cl_HCl':25,
    'S_acetylpyrrolidine':130,'bromopyridine':15,'Pd2dba3':250,
    'BINAP_rac':500,'pyrrole_COOH':35,'picolyl_Cl_HCl':30,
    'amino_Br_Me_pym':75,'Br_NO2_pyr':40,'ClF_Ph_BA':50,'PdPPh3_4':150,
}
MW = {
    'nipecotic_acid':129.16,'amino_F2_BT':202.19,'DMAE_Cl_HCl':144.04,
    'S_acetylpyrrolidine':113.16,'bromopyridine':157.99,
    'amino_Br_Me_pym':188.04,'Br_NO2_pyr':203.01,
    'ClF_Ph_BA':174.97,'PdPPh3_4_dimer':1155.6,'Pd2dba3':915.67,
    'BINAP_rac':622.67,'Cs2CO3':325.82,'NBS':177.99,'thiourea':76.12,
    'HATU':380.23,'CDI':162.15,'chloroacetamide':93.51,
    'pyrrole_COOH':111.10,'picolyl_Cl_HCl':164.04,
}

def ac(mmol, mw_key, eq, price_key):
    return mmol * eq * MW[mw_key] / 1000 * PRICE[price_key]

# ── MCUF651 Route A: 2 steps ─────────────────────────────────────────────────
# Prep scale inputs: step1 = 0.776 mmol, step2 = 0.447 mmol [A1]
assay_mcuf651 = {
    'Step 1 assay (0.1 mmol)': (
        ac(ASSAY_MMOL,'nipecotic_acid',1.0,'nipecotic_acid') +
        ac(ASSAY_MMOL,'amino_F2_BT',1.0,'amino_F2_BT') +
        ac(ASSAY_MMOL,'HATU',1.1,'HATU') +
        ac(ASSAY_MMOL,'DIPEA',2.5,'DIPEA')
    ),
    'Step 2 assay (0.1 mmol)': (
        ac(ASSAY_MMOL,'DMAE_Cl_HCl',1.3,'DMAE_Cl_HCl')
    ),
}
n_steps_mcuf = 2
assay_mat_mcuf  = sum(assay_mcuf651.values())
assay_lab_mcuf  = n_steps_mcuf * ASSAY_LCD * LABOUR_RATE
assay_tot_mcuf  = assay_mat_mcuf + assay_lab_mcuf

# Originals
orig_mat_mcuf = 60; orig_lab_mcuf = 1082; orig_tot_mcuf = 1143
new_tot_mcuf  = orig_tot_mcuf + assay_tot_mcuf
new_cd_mcuf   = 1.25 + n_steps_mcuf * ASSAY_LCD

# ── A317 Route A: 4 steps + 1 parallel = 5 assay runs ───────────────────────
assay_a317 = {
    'Step 1 Buchwald assay': (
        ac(ASSAY_MMOL,'S_acetylpyrrolidine',1.0,'S_acetylpyrrolidine') +
        ac(ASSAY_MMOL,'bromopyridine',1.1,'bromopyridine') +
        ac(ASSAY_MMOL,'Pd2dba3',0.02,'Pd2dba3') +
        ac(ASSAY_MMOL,'BINAP_rac',0.04,'BINAP_rac') +
        ac(ASSAY_MMOL,'Cs2CO3',2.0,'Cs2CO3')
    ),
    'Step 2 alpha-Br assay': ac(ASSAY_MMOL,'NBS',1.05,'NBS'),
    'Step 3 Hantzsch assay': ac(ASSAY_MMOL,'thiourea',1.2,'thiourea'),
    'Step 4 amide assay': (
        ac(ASSAY_MMOL,'HATU',1.1,'HATU') +
        ac(ASSAY_MMOL,'DIPEA',2.5,'DIPEA') +
        0.1/0.388*98/1000*202.21*0   # picolylpyrrole acid already made, ~negligible marginal
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

orig_mat_a317 = 187; orig_lab_a317 = 2165; orig_tot_a317 = 2352
new_tot_a317  = orig_tot_a317 + assay_tot_a317
new_cd_a317   = 2.5 + n_steps_a317 * ASSAY_LCD

# ── 7977 Route B: 5 steps ─────────────────────────────────────────────────────
assay_7977 = {
    'Step 1 SNAr assay': (
        ac(ASSAY_MMOL,'amino_Br_Me_pym',1.0,'amino_Br_Me_pym') +
        ac(ASSAY_MMOL,'Br_NO2_pyr',1.05,'Br_NO2_pyr')
    ),
    'Step 2 Suzuki assay': (
        ac(ASSAY_MMOL,'ClF_Ph_BA',1.1,'ClF_Ph_BA') +
        ac(ASSAY_MMOL,'PdPPh3_4_dimer',0.05,'PdPPh3_4')
    ),
    'Step 3 Fe reduction assay': ac(ASSAY_MMOL,'Fe_powder',3.0,'Fe_powder')*0.056,
    'Step 4 CDI assay': ac(ASSAY_MMOL,'CDI',1.2,'CDI'),
    'Step 5 N-alkylation assay': ac(ASSAY_MMOL,'chloroacetamide',1.2,'chloroacetamide'),
}
n_steps_7977 = 5
assay_mat_7977 = sum(assay_7977.values())
assay_lab_7977 = n_steps_7977 * ASSAY_LCD * LABOUR_RATE
assay_tot_7977 = assay_mat_7977 + assay_lab_7977

orig_mat_7977 = 150; orig_lab_7977 = 2165; orig_tot_7977 = 2315
new_tot_7977  = orig_tot_7977 + assay_tot_7977
new_cd_7977   = 2.5 + n_steps_7977 * ASSAY_LCD

grand_new = new_tot_mcuf + new_tot_a317 + new_tot_7977
grand_orig = orig_tot_mcuf + orig_tot_a317 + orig_tot_7977

print("ASSAY-RUN ADDITIONS (0.1 mmol assay before each preparative step)")
print(f"  Assay labour rate: {ASSAY_LCD} cd/step × €{LABOUR_RATE}/cd = €{ASSAY_LCD*LABOUR_RATE:.0f}/step")
print()
for cpd, steps in [('MCUF651',assay_mcuf651),('A317',assay_a317),('7977',assay_7977)]:
    print(f"  {cpd} assay steps:")
    for k,v in steps.items():
        print(f"    {k:<35} €{v:.2f} reagents")

print()
print("═"*65)
print(f"  {'':12} {'Orig €':>9} {'Assay add.':>11} {'New total €':>12} {'New cd':>7}")
print(f"  {'MCUF651':12} {orig_tot_mcuf:>9} {assay_tot_mcuf:>11.0f} {new_tot_mcuf:>12.0f} {new_cd_mcuf:>7.2f}")
print(f"  {'A317':12} {orig_tot_a317:>9} {assay_tot_a317:>11.0f} {new_tot_a317:>12.0f} {new_cd_a317:>7.2f}")
print(f"  {'7977':12} {orig_tot_7977:>9} {assay_tot_7977:>11.0f} {new_tot_7977:>12.0f} {new_cd_7977:>7.2f}")
print(f"  {'ALL THREE':12} {grand_orig:>9} {assay_tot_mcuf+assay_tot_a317+assay_tot_7977:>11.0f} {grand_new:>12.0f} {new_cd_mcuf+new_cd_a317+new_cd_7977:>7.2f}")
print()
print(f"  Grand total: €{grand_new:.0f}   Range: €{grand_new*0.80:.0f} – €{grand_new*1.35:.0f}")
print(f"  Total chemist-days: {new_cd_mcuf+new_cd_a317+new_cd_7977:.2f} cd  ({(new_cd_mcuf+new_cd_a317+new_cd_7977)/5:.1f} working weeks)")
print()
print(f"  Assay reagent cost is trivial (MCUF651 €{assay_mat_mcuf:.1f}, A317 €{assay_mat_a317:.1f}, 7977 €{assay_mat_7977:.1f})")
print(f"  Labour for assay runs dominates the addition: €{(assay_lab_mcuf+assay_lab_a317+assay_lab_7977):.0f} of €{assay_tot_mcuf+assay_tot_a317+assay_tot_7977:.0f} total addition")
