
# Correlate physicochemical properties with pIC50 in clean (non-PAINS) subset
clean = df2[df2['pains_flag']==''].copy()
pains = df2[df2['pains_flag']!=''].copy()

print(f"Clean compounds: {len(clean)}, mean pIC50={clean['pIC50_num'].mean():.3f}")
print(f"PAINS compounds: {len(pains)}, mean pIC50={pains['pIC50_num'].mean():.3f}")

print("\n--- Clean compounds ranked ---")
for _, r in clean.sort_values('pIC50_num', ascending=False).iterrows():
    print(f"{r['pIC50_num']:.3f}  {r['Serie'][:8]:<8}  {r['Molecule Name']:<14}  MW={r['MW']:.0f} LogP={r['LogP']:.2f}")
    print(f"  R1 context: {r['can_smiles'][:100]}")
    print()

# R1/R2 pattern extraction for clean compounds
print("\n=== Correlation: LogP vs pIC50 (all) ===")
import numpy as np
corr = np.corrcoef(df2['LogP'].dropna(), df2['pIC50_num'].dropna())[0,1]
print(f"LogP-pIC50 correlation: {corr:.3f}")
corr_mw = np.corrcoef(df2['MW'].dropna(), df2['pIC50_num'].dropna())[0,1]
print(f"MW-pIC50 correlation:   {corr_mw:.3f}")
corr_rotb = np.corrcoef(df2['RotB'].dropna(), df2['pIC50_num'].dropna())[0,1]
print(f"RotB-pIC50 correlation: {corr_rotb:.3f}")
