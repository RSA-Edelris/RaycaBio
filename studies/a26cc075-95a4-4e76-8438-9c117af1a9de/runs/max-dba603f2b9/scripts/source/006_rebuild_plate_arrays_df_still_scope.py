
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np

# ── Rebuild plate arrays from df (still in scope) ────────────────────────────
n_rows, n_cols = 8, 12
plate_raw  = np.zeros((n_rows, n_cols))
plate_well = np.full((n_rows, n_cols), '', dtype=object)   # e.g. "001"

for _, r in df.iterrows():
    ri = int(r['row_idx'])
    ci = int(r['col_idx']) - 1
    plate_raw[ri, ci]  = r['norm_yield']
    plate_well[ri, ci] = r['ID'].split('-')[1]             # "001" … "096"

# Normalise to plate maximum (0 → 1)
plate_max  = plate_raw.max()
plate_norm = plate_raw / plate_max

print(f"Plate max IS-ratio: {plate_max:.4f}  (well {df.loc[df['norm_yield'].idxmax(),'ID']})")
print(f"Normalised range:   {plate_norm.min():.3f} – {plate_norm.max():.3f}")
print("First row wells:", plate_well[0])
