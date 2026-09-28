
# Print the full correlation and effect-size numbers for the report
import numpy as np

enc2 = df.copy()
enc2['is_Dioxane'] = (enc2['Solvent'] == 'Dioxane').astype(float)
enc2['is_K2CO3']   = (enc2['Base']    == 'K2CO3').astype(float)
enc2['is_CuOTf2']  = (enc2['Cu']      == 'Cu(OTf)2').astype(float)

lig_means2 = enc2.groupby('Ligand')['norm'].mean()
enc2['lig_score'] = enc2['Ligand'].map(lig_means2)

print("=== Pearson r vs. normalised yield ===")
for lbl, col in [('Ligand (mean score)', 'lig_score'),
                 ('Dioxane vs DMF',      'is_Dioxane'),
                 ('K2CO3 vs K3PO4',      'is_K2CO3'),
                 ('Cu(OTf)2 vs CuI',     'is_CuOTf2')]:
    r = np.corrcoef(enc2[col], enc2['norm'])[0,1]
    print(f"  {lbl:<24} r = {r:+.4f}")

print("\n=== Mean norm yield by condition level ===")
for var in ['Ligand','Solvent','Base','Cu']:
    print(f"\n  {var}:")
    grp = df.groupby(var)['norm'].agg(['mean','max','count']).sort_values('mean', ascending=False)
    print(grp.to_string())

print("\n=== DMCyDA only: effect of Base × Cu × Solvent ===")
dmc = df[df['Ligand']=='DMCyDA'].sort_values('norm', ascending=False)
print(dmc[['Well','Base','Cu','Solvent','ratio','norm']].to_string(index=False))
