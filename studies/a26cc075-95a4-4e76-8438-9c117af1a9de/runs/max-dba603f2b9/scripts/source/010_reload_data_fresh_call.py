
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import matplotlib.cm as cm

# ── Reload data (fresh call) ──────────────────────────────────────────────────
conditions = pd.read_csv(
    '/home/ubuntu/rayca-artifacts/ab6ab3d3a46e0d2cc39a9030/files/conditions.csv',
    header=None, names=['ID','Condition'])
results = pd.read_csv(
    '/home/ubuntu/rayca-artifacts/ab6ab3d3a46e0d2cc39a9030/files/results.csv')
df = results.merge(conditions, on='ID')
df['norm_yield'] = (df['Area Abs DP'] / df['Area Abs IS']).fillna(0)

def parse_condition(cond):
    parts = cond.split('_')
    for i, p in enumerate(parts):
        if p in ('K3PO4','K2CO3'):
            base_idx = i; break
    return '_'.join(parts[:base_idx]), parts[base_idx], parts[base_idx+1], parts[base_idx+2]

df[['Ligand','Base','Cu','Solvent']] = df['Condition'].apply(
    lambda x: pd.Series(parse_condition(x)))

well_num = df['ID'].str.extract(r'-(\d+)$').astype(int)[0]
df['row_idx'] = (well_num - 1) // 12   # 0-7  → A-H
df['col_idx'] = (well_num - 1) % 12    # 0-11 → 1-12

# Build original plate (8 rows × 12 cols)
plate = np.zeros((8, 12))
for _, r in df.iterrows():
    plate[int(r['row_idx']), int(r['col_idx'])] = r['norm_yield']

# ── Transpose: 12 rows (col numbers) × 8 cols (row letters) ──────────────────
plate_T = plate.T     # shape (12, 8)

# ── Black-to-yellow colormap ──────────────────────────────────────────────────
cmap_by = mcolors.LinearSegmentedColormap.from_list(
    'black_yellow',
    ['#000000', '#1c1400', '#3d2b00', '#7a5200', '#c28400', '#f0cc00', '#ffee00'],
    N=256)

vmax = plate_T.max()
norm = mcolors.Normalize(vmin=0, vmax=vmax)

# ── Condition pivots ──────────────────────────────────────────────────────────
lig_order = (df.groupby('Ligand')['norm_yield'].mean()
               .sort_values(ascending=False).index.tolist())

def piv(row_var):
    p = df.pivot_table(index=row_var, columns='Ligand',
                       values='norm_yield', aggfunc='mean')
    return p[lig_order]

pv_solv = piv('Solvent')
pv_base = piv('Base')
pv_cu   = piv('Cu')

# ── Figure ────────────────────────────────────────────────────────────────────
ROW_LABELS = [str(i) for i in range(1, 13)]   # 1–12 on y-axis
COL_LABELS = list('ABCDEFGH')                  # A–H on x-axis
n_rows_T, n_cols_T = 12, 8

well_r = 0.38
xs = np.arange(1, n_cols_T + 1, dtype=float)
ys = np.arange(n_rows_T, 0, -1, dtype=float)  # row-1 at top

fig = plt.figure(figsize=(16, 18), facecolor='#0d0d0d')
gs  = gridspec.GridSpec(2, 3, figure=fig,
                        height_ratios=[2.0, 1.0],
                        hspace=0.40, wspace=0.40,
                        left=0.07, right=0.97,
                        top=0.94, bottom=0.06)

# ── Panel 1: transposed plate ─────────────────────────────────────────────────
ax_p = fig.add_subplot(gs[0, :])
ax_p.set_facecolor('#0d0d0d')

# Plate body
ax_p.add_patch(patches.FancyBboxPatch(
    (0.3, 0.2), n_cols_T + 0.6, n_rows_T + 0.65,
    boxstyle='round,pad=0.1', lw=1.2,
    edgecolor='#444444', facecolor='#1a1a1a', zorder=0))

for ri in range(n_rows_T):
    for ci in range(n_cols_T):
        val   = plate_T[ri, ci]
        color = cmap_by(norm(val))
        ax_p.add_patch(patches.Circle(
            (xs[ci], ys[ri]), well_r,
            facecolor=color, edgecolor='#333333', lw=0.5, zorder=2))
        if val == vmax:
            ax_p.add_patch(patches.Circle(
                (xs[ci], ys[ri]), well_r + 0.08,
                facecolor='none', edgecolor='#ffffff', lw=2.2, zorder=3))
            ax_p.text(xs[ci], ys[ri], '★',
                      ha='center', va='center', fontsize=7,
                      color='#ffffff', zorder=4, fontweight='bold')

# Column labels A–H (top)
for ci, cl in enumerate(COL_LABELS):
    ax_p.text(xs[ci], n_rows_T + 0.80, cl,
              ha='center', va='bottom', fontsize=11,
              fontweight='bold', color='#cccccc')

# Row labels 1–12 (left)
for ri, rl in enumerate(ROW_LABELS):
    ax_p.text(0.47, ys[ri], rl,
              ha='right', va='center', fontsize=9.5,
              fontweight='bold', color='#cccccc')

ax_p.set_xlim(0.1, n_cols_T + 1.0)
ax_p.set_ylim(-0.1, n_rows_T + 1.3)
ax_p.set_aspect('equal')
ax_p.axis('off')
ax_p.set_title('96-Well Plate — IS-Normalised DP Yield  (transposed: rows = columns 1–12, cols = rows A–H)',
               fontsize=11, fontweight='bold', color='#eeeeee', pad=8)

sm = cm.ScalarMappable(cmap=cmap_by, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax_p, orientation='vertical',
                    fraction=0.015, pad=0.01, aspect=30)
cbar.set_label('DP / IS  (area ratio)', fontsize=8, color='#aaaaaa')
cbar.ax.tick_params(labelsize=8, colors='#aaaaaa')
cbar.outline.set_edgecolor('#444444')
cbar.ax.yaxis.set_tick_params(color='#444444')

# ── Panels 2–4: condition heatmaps ───────────────────────────────────────────
hm_config = [
    ('Ligand × Solvent', pv_solv, ['DMF', 'Dioxane']),
    ('Ligand × Base',    pv_base, ['K₂CO₃', 'K₃PO₄']),
    ('Ligand × Cu',      pv_cu,   ['Cu(OTf)₂', 'CuI']),
]

for idx, (title, pvt, rlbls) in enumerate(hm_config):
    ax = fig.add_subplot(gs[1, idx])
    ax.set_facecolor('#0d0d0d')
    data_arr = pvt.reindex(pvt.index.tolist()).values

    im = ax.imshow(data_arr, aspect='auto', cmap=cmap_by,
                   vmin=0, vmax=vmax, interpolation='nearest')

    for ri2 in range(data_arr.shape[0]):
        for ci2 in range(data_arr.shape[1]):
            v = data_arr[ri2, ci2]
            tc = '#000000' if norm(v) > 0.60 else '#888888'
            ax.text(ci2, ri2, f'{v:.2f}' if v > 0.005 else '0',
                    ha='center', va='center', fontsize=6.5,
                    color=tc, fontweight='bold')

    ax.set_xticks(range(len(lig_order)))
    ax.set_xticklabels(lig_order, rotation=42, ha='right',
                       fontsize=7.5, color='#cccccc')
    ax.set_yticks(range(len(pvt.index)))
    ax.set_yticklabels(rlbls, fontsize=9, color='#cccccc')
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_edgecolor('#333333'); sp.set_linewidth(0.8)
    ax.set_title(title, fontsize=10, fontweight='bold', color='#eeeeee', pad=5)

    cb2 = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cb2.ax.tick_params(labelsize=7, colors='#aaaaaa')
    cb2.outline.set_edgecolor('#444444')

# Best condition label
best = df.loc[df['norm_yield'].idxmax()]
fig.text(0.5, 0.008,
         f"★  Best: {best['Condition']}   (well {best['ID'].split('-')[1]})"
         f"   norm. yield = {best['norm_yield']:.3f}",
         ha='center', va='bottom', fontsize=10,
         color='#ffee00', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1400',
                   edgecolor='#ffee00', lw=0.8))

out = '/home/ubuntu/rayca-sessions/a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/hte_heatmap_transposed.png'
fig.savefig(out, dpi=160, bbox_inches='tight', facecolor='#0d0d0d')
plt.close(fig)
print(f"Saved → {out}")
