
import pandas as pd
import numpy as np

# ── Load data ─────────────────────────────────────────────────────────────────
cond = pd.read_csv('/home/ubuntu/rayca-artifacts/26995afd35296f81e92b889c/files/conditions_2.csv')
cond.columns = ['ID', 'Condition', 'Well']

res = pd.read_csv('/home/ubuntu/rayca-artifacts/ab6ab3d3a46e0d2cc39a9030/files/results.csv')

df = res.merge(cond, left_on='ID', right_on='ID')

# ── Step 1: IS-normalise ──────────────────────────────────────────────────────
df['ratio'] = (df['Area Abs DP'] / df['Area Abs IS']).fillna(0)

# ── Step 2: normalise to max (0–1 scale) ─────────────────────────────────────
max_ratio = df['ratio'].max()
df['norm'] = df['ratio'] / max_ratio

# ── Parse conditions ──────────────────────────────────────────────────────────
def parse_cond(c):
    parts = c.split('_')
    for i, p in enumerate(parts):
        if p in ('K3PO4', 'K2CO3'):
            bi = i; break
    return '_'.join(parts[:bi]), parts[bi], parts[bi+1], parts[bi+2]

df[['Ligand','Base','Cu','Solvent']] = df['Condition'].apply(lambda x: pd.Series(parse_cond(x)))

# ── Well → row/col indices ────────────────────────────────────────────────────
df['plate_row'] = df['Well'].str[0]           # A-H
df['plate_col'] = df['Well'].str[1:].astype(int)  # 1-12

# ── Build 8×12 plate matrix ───────────────────────────────────────────────────
rows = list('ABCDEFGH')
plate = np.zeros((8, 12))
for _, r in df.iterrows():
    ri = rows.index(r['plate_row'])
    ci = int(r['plate_col']) - 1
    plate[ri, ci] = r['norm']

print("Plate matrix (8×12) built. Max norm =", plate.max())
print("\nTop 10 conditions:")
top10 = df.nlargest(10, 'norm')[['ID','Well','Condition','ratio','norm']].reset_index(drop=True)
print(top10.to_string())
print(f"\nRow labels (A-H sub-conditions):")
for rl in rows:
    sub = df[df['plate_row']==rl]['Condition'].iloc[0]
    sub_parts = sub.split('_')
    print(f"  {rl}: {sub_parts[-3]}_{sub_parts[-2]}_{sub_parts[-1]}")
print(f"\nColumn labels (ligands):")
for ci in range(1,13):
    lig = df[df['plate_col']==ci]['Ligand'].iloc[0]
    print(f"  Col {ci}: {lig}")
