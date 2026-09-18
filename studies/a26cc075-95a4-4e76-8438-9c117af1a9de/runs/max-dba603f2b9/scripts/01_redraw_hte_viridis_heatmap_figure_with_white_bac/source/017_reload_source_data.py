
import pandas as pd
import numpy as np

# Reload source data
cond = pd.read_csv('/home/ubuntu/rayca-artifacts/26995afd35296f81e92b889c/files/conditions_2.csv')
cond.columns = ['ID', 'Condition', 'Well']
res  = pd.read_csv('/home/ubuntu/rayca-artifacts/ab6ab3d3a46e0d2cc39a9030/files/results.csv')
df   = res.merge(cond, left_on='ID', right_on='ID')

df['ratio'] = (df['Area Abs DP'] / df['Area Abs IS']).fillna(0)
max_ratio    = df['ratio'].max()
df['norm']   = df['ratio'] / max_ratio

def parse_cond(c):
    parts = c.split('_')
    for i, p in enumerate(parts):
        if p in ('K3PO4','K2CO3'):
            bi = i; break
    return '_'.join(parts[:bi]), parts[bi], parts[bi+1], parts[bi+2]

df[['Ligand','Base','Cu','Solvent']] = df['Condition'].apply(lambda x: pd.Series(parse_cond(x)))
df['plate_row'] = df['Well'].str[0]
df['plate_col'] = df['Well'].str[1:].astype(int)

ROWS    = list('ABCDEFGH')
LIGANDS = ['Oxine','Chxn-Py-Al','THMD','BTMO','DPEO','DMPO',
           "4,4'-(tBu)bpy",'TMEDA','DMCyDA','1,10-phen',
           "4,4'-(Me)bpy","4,4'-(OMe)bpy"]
ROW_SUBS = ['K₃PO₄/CuI/Diox','K₃PO₄/Cu(OTf)₂/Diox',
            'K₂CO₃/CuI/Diox','K₂CO₃/Cu(OTf)₂/Diox',
            'K₃PO₄/CuI/DMF','K₃PO₄/Cu(OTf)₂/DMF',
            'K₂CO₃/CuI/DMF','K₂CO₃/Cu(OTf)₂/DMF']

plate = np.zeros((8,12))
for _, r in df.iterrows():
    ri = ROWS.index(r['plate_row'])
    ci = int(r['plate_col']) - 1
    plate[ri, ci] = r['norm']

def pivot_cond(row_var):
    pv = df.pivot_table(index=row_var, columns='Ligand',
                        values='norm', aggfunc='mean')
    return pv.reindex(columns=LIGANDS, fill_value=0)

pv_solv = pivot_cond('Solvent')
pv_base = pivot_cond('Base')
pv_cu   = pivot_cond('Cu')

enc = df.copy()
enc['is_Dioxane'] = (enc['Solvent']=='Dioxane').astype(float)
enc['is_K2CO3']   = (enc['Base']   =='K2CO3').astype(float)
enc['is_CuOTf2']  = (enc['Cu']     =='Cu(OTf)2').astype(float)
lig_means = enc.groupby('Ligand')['norm'].mean()
enc['lig_score'] = enc['Ligand'].map(lig_means)

lig_df = df.groupby('Ligand')['norm'].agg(['mean','max']).reindex(LIGANDS)

print("Data rebuilt. plate.max()=", plate.max())
