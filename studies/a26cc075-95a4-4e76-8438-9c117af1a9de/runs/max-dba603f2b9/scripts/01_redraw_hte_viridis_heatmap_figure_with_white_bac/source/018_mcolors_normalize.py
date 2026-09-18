
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np

cmap_v = plt.cm.viridis
norm_c = mcolors.Normalize(vmin=0, vmax=1)

n_rows, n_cols = 8, 12
well_r = 0.40
xs = np.arange(1, n_cols+1, dtype=float)
ys = np.arange(n_rows, 0, -1, dtype=float)

# ── Figure (white background) ─────────────────────────────────────────────────
fig = plt.figure(figsize=(22, 18), facecolor='white')
gs  = gridspec.GridSpec(3, 4, figure=fig,
                        height_ratios=[2.0, 1.0, 1.0],
                        hspace=0.55, wspace=0.38,
                        left=0.10, right=0.97,
                        top=0.94, bottom=0.06)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL 1 — 96-well plate
# ══════════════════════════════════════════════════════════════════════════════
ax_p = fig.add_subplot(gs[0, :])
ax_p.set_facecolor('white')

ax_p.add_patch(mpatches.FancyBboxPatch(
    (0.15, 0.12), n_cols+0.7, n_rows+0.85,
    boxstyle='round,pad=0.12', lw=1.5,
    edgecolor='#9ca3af', facecolor='#f1f5f9', zorder=0))

for ri in range(n_rows):
    for ci in range(n_cols):
        v   = plate[ri, ci]
        col = cmap_v(norm_c(v))
        ax_p.add_patch(mpatches.Circle(
            (xs[ci], ys[ri]), well_r,
            facecolor=col, edgecolor='#d1d5db', lw=0.5, zorder=2))
        if v == 1.0:
            ax_p.add_patch(mpatches.Circle(
                (xs[ci], ys[ri]), well_r+0.08,
                facecolor='none', edgecolor='#b45309', lw=2.5, zorder=3))
        lum = 0.2126*col[0]+0.7152*col[1]+0.0722*col[2]
        tc  = '#111111' if lum > 0.45 else '#ffffff'
        ax_p.text(xs[ci], ys[ri], f'{v:.2f}',
                  ha='center', va='center', fontsize=5.8,
                  color=tc, fontweight='bold', zorder=4)

for ri, (rl, rs) in enumerate(zip(ROWS, ROW_SUBS)):
    ax_p.text(0.40, ys[ri]+0.12, rl,
              ha='right', va='center', fontsize=11,
              fontweight='bold', color='#111827')
    ax_p.text(0.38, ys[ri]-0.18, rs,
              ha='right', va='top', fontsize=5.5, color='#6b7280')

for ci, lig in enumerate(LIGANDS):
    ax_p.text(xs[ci], n_rows+0.92, lig,
              ha='center', va='bottom', fontsize=7.2,
              fontweight='bold', color='#111827',
              rotation=30, rotation_mode='anchor')

ax_p.set_xlim(-0.2, n_cols+0.9)
ax_p.set_ylim(-0.1, n_rows+1.5)
ax_p.set_aspect('equal')
ax_p.axis('off')
ax_p.set_title('96-Well Plate — IS-Normalised DP Yield  (normalised to maximum)',
               fontsize=12, fontweight='bold', color='#111827', pad=6)

sm = cm.ScalarMappable(cmap=cmap_v, norm=norm_c)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax_p, orientation='vertical',
                    fraction=0.015, pad=0.005, aspect=30)
cbar.set_label('Relative yield (0 = none, 1 = best)', fontsize=8, color='#374151')
cbar.ax.tick_params(labelsize=7.5, colors='#374151')
cbar.outline.set_edgecolor('#9ca3af')

# ══════════════════════════════════════════════════════════════════════════════
# PANELS 2–4 — condition heatmaps
# ══════════════════════════════════════════════════════════════════════════════
hm_cfg = [
    ('Ligand × Solvent',   pv_solv, ['DMF','Dioxane']),
    ('Ligand × Base',      pv_base, ['K₂CO₃','K₃PO₄']),
    ('Ligand × Cu Source', pv_cu,   ['Cu(OTf)₂','CuI']),
]
for idx, (title, pvt, row_lbls) in enumerate(hm_cfg):
    ax = fig.add_subplot(gs[1, idx])
    ax.set_facecolor('white')
    data_arr = pvt.values
    im = ax.imshow(data_arr, aspect='auto', cmap=cmap_v,
                   vmin=0, vmax=1, interpolation='nearest')
    for ri2 in range(data_arr.shape[0]):
        for ci2 in range(data_arr.shape[1]):
            v   = data_arr[ri2, ci2]
            c2  = cmap_v(norm_c(v))
            lm  = 0.2126*c2[0]+0.7152*c2[1]+0.0722*c2[2]
            tc2 = '#111111' if lm > 0.45 else '#ffffff'
            ax.text(ci2, ri2, f'{v:.2f}' if v > 0.005 else '0',
                    ha='center', va='center', fontsize=5.5,
                    color=tc2, fontweight='bold')
    ax.set_xticks(range(len(LIGANDS)))
    ax.set_xticklabels(LIGANDS, rotation=42, ha='right',
                       fontsize=6.5, color='#111827')
    ax.set_yticks(range(len(pvt.index)))
    ax.set_yticklabels(row_lbls, fontsize=9, color='#111827')
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_edgecolor('#9ca3af'); sp.set_linewidth(0.7)
    ax.set_title(title, fontsize=9.5, fontweight='bold',
                 color='#111827', pad=4)
    cb2 = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
    cb2.ax.tick_params(labelsize=6.5, colors='#374151')
    cb2.outline.set_edgecolor('#9ca3af')

# ══════════════════════════════════════════════════════════════════════════════
# PANEL 5 — correlation bar chart
# ══════════════════════════════════════════════════════════════════════════════
ax_c = fig.add_subplot(gs[1, 3])
ax_c.set_facecolor('white')

corr_labels = ['Ligand\n(mean score)','Cu(OTf)₂\nvs CuI',
               'K₂CO₃\nvs K₃PO₄','Dioxane\nvs DMF']
corr_vals = [
    np.corrcoef(enc['lig_score'],  enc['norm'])[0,1],
    np.corrcoef(enc['is_CuOTf2'],  enc['norm'])[0,1],
    np.corrcoef(enc['is_K2CO3'],   enc['norm'])[0,1],
    np.corrcoef(enc['is_Dioxane'], enc['norm'])[0,1],
]
colors_bar = ['#16a34a' if v>0 else '#dc2626' for v in corr_vals]
bars = ax_c.barh(corr_labels, corr_vals, color=colors_bar,
                  edgecolor='#9ca3af', lw=0.7, height=0.55)
ax_c.axvline(0, color='#6b7280', lw=0.8, ls='--')
for bar, v in zip(bars, corr_vals):
    ax_c.text(v+(0.01 if v>=0 else -0.01),
              bar.get_y()+bar.get_height()/2,
              f'{v:+.3f}', va='center',
              ha='left' if v>=0 else 'right',
              fontsize=8, color='#111827', fontweight='bold')
ax_c.set_xlim(-1.05, 1.05)
ax_c.set_xlabel('Pearson r  (vs. normalised yield)', fontsize=8, color='#374151')
ax_c.set_title('Variable Correlations', fontsize=9.5,
               fontweight='bold', color='#111827', pad=4)
ax_c.tick_params(colors='#374151', labelsize=8)
for sp in ax_c.spines.values():
    sp.set_edgecolor('#9ca3af')
ax_c.grid(axis='x', color='#e5e7eb', lw=0.5, ls=':')

# ══════════════════════════════════════════════════════════════════════════════
# PANEL 6 — per-ligand bar chart
# ══════════════════════════════════════════════════════════════════════════════
ax_l = fig.add_subplot(gs[2, :])
ax_l.set_facecolor('white')
x_pos = np.arange(len(LIGANDS))
bar_w = 0.38
ax_l.bar(x_pos-bar_w/2, lig_df['mean'], bar_w,
         label='Mean norm. yield', color='#3b82f6',
         edgecolor='#9ca3af', lw=0.6)
ax_l.bar(x_pos+bar_w/2, lig_df['max'],  bar_w,
         label='Max norm. yield',  color='#f59e0b',
         edgecolor='#9ca3af', lw=0.6)
ax_l.set_xticks(x_pos)
ax_l.set_xticklabels(LIGANDS, rotation=35, ha='right',
                      fontsize=8, color='#111827')
ax_l.set_ylabel('Normalised yield', fontsize=9, color='#374151')
ax_l.set_title('Per-Ligand Performance  (mean and max across all 8 sub-conditions)',
               fontsize=10, fontweight='bold', color='#111827', pad=5)
ax_l.tick_params(colors='#374151', labelsize=8)
ax_l.legend(fontsize=8, facecolor='white', edgecolor='#9ca3af',
            labelcolor='#111827', framealpha=1.0)
for sp in ax_l.spines.values():
    sp.set_edgecolor('#9ca3af')
ax_l.grid(axis='y', color='#e5e7eb', lw=0.5, ls=':')
ax_l.set_xlim(-0.6, len(LIGANDS)-0.4)

# ── Footer ────────────────────────────────────────────────────────────────────
best = df.loc[df['norm'].idxmax()]
fig.text(0.5, 0.008,
         f"★  Best: {best['Condition']}  (well {best['Well']})  "
         f"  DP/IS = {best['ratio']:.3f}  →  norm. yield = 1.000",
         ha='center', fontsize=9, color='#92400e', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fffbeb',
                   edgecolor='#d97706', lw=0.9))

base = '/home/ubuntu/rayca-sessions/a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/hte_viridis_white'
fig.savefig(base+'.png', dpi=150, bbox_inches='tight', facecolor='white')
fig.savefig(base+'.jpg', dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig)
print("Saved PNG →", base+'.png')
print("Saved JPG →", base+'.jpg')
