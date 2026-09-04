
# Corrected totals using realistic purification cost
# Silica chromatography materials: ~€20-25/column (silica + solvents + disposables)
# Labour for columns already included in chemist-day estimates

pur_A_corr    = 25    # MCUF651: 1 column step 1 + extraction step 2
pur_A317_corr = 85    # A317: 4 columns (step1 Buchwald, step3 Hantzsch, step4 amide, parallel acid)
pur_7977_corr = 90    # 7977: columns at steps 1,2,4,5 + crystallisation step3

# Recalculate totals
mat_A_corr = (100.3*45 + 157.0*90 + 324.7*40 + 250.8*5 + 83.7*25 + 123.6*1 + 0.14) / 1000
tot_A_corr    = mat_A_corr + pur_A_corr    + lab_A
tot_A317_corr = mat_A317   + pur_A317_corr + lab_A317 + 0.34   # solvents
tot_7977_corr = mat_7977   + pur_7977_corr + lab_7977 + 0.45
grand_corr    = tot_A_corr + tot_A317_corr + tot_7977_corr

print("CORRECTED TOTALS (purification: €20-25/column, silica+solvents+disposables)")
print(f"  MCUF651 Route A:  mat {mat_A_corr:>6.1f} + pur {pur_A_corr:>5.0f} + lab {lab_A:>7.0f} = {tot_A_corr:>8.0f} EUR")
print(f"  A317    Route A:  mat {mat_A317:>6.1f} + pur {pur_A317_corr:>5.0f} + lab {lab_A317:>7.0f} = {tot_A317_corr:>8.0f} EUR")
print(f"  7977    Route B:  mat {mat_7977:>6.1f} + pur {pur_7977_corr:>5.0f} + lab {lab_7977:>7.0f} = {tot_7977_corr:>8.0f} EUR")
print(f"  Grand total:                                            {grand_corr:>8.0f} EUR")
print(f"  Range:  €{grand_corr*0.80:.0f} – €{grand_corr*1.35:.0f}")
print()
# labour breakdown
total_cd = lab_A_cd + lab_A317_cd + lab_7977_cd
print(f"  Total chemist-days: {total_cd:.1f} cd  →  labour €{total_cd*LABOUR_RATE:.0f}")
print(f"  Materials + purification: €{grand_corr - total_cd*LABOUR_RATE:.0f}")
print()
print("  Labour as % of total:", f"{total_cd*LABOUR_RATE/grand_corr*100:.0f}%")
