
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import matplotlib.cm as cm

# ── Load from source files ────────────────────────────────────────────────────
cond = pd.read_csv(
    '/home/ubuntu/rayca-artifacts/ab6ab3d3a46e0d2cc39a9030/files/conditions.csv',
    header=None, names=['ID','Condition'])
res  = pd.read_csv(
    '/home/ubuntu/rayca-artifacts/ab6ab3d3a46e0d2cc39a9030/files/results.csv')

df = res.merge(cond, on='ID')
df['norm_yield'] = (df['Area Abs DP'] / df['Area Abs IS']).fillna(0)

well_num     = df['ID'].str.extract(r'-(\d+)$').astype(int)[0]
df['row_idx'] = (well_num - 1) // 12
df['col_idx'] = (well_num - 1) % 12 + 1

# ── Plate arrays ──────────────────────────────────────────────────────────────
n_rows, n_cols = 8, 12
plate_raw  = np.zeros((n_rows, n_cols))
plate_well = np.full((n_rows, n_cols), '', dtype=object)

for _, r in df.iterrows():
    ri = int(r['row_idx']); ci = int(r['col_idx']) - 1
    plate_raw[ri, ci]  = r['norm_yield']
    plate_well[ri, ci] = r['ID'].split('-')[1]   # "001" … "096"

plate_max  = plate_raw.max()
plate_norm = plate_raw / plate_max

print(f"max IS-ratio: {plate_max:.4f}  |  normalised range: {plate_norm.min():.3f}–{plate_norm.max():.3f}")
print("row F wells:", plate_well[5])
