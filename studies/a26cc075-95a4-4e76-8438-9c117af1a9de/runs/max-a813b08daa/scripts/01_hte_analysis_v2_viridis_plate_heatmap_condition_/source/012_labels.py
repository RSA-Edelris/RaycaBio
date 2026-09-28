
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np

# ── Labels ─────────────────────────────────────────────────────────────────────
ROWS     = list('ABCDEFGH')
ROW_SUBS = ['K₃PO₄/CuI/Diox','K₃PO₄/Cu(OTf)₂/Diox',
            'K₂CO₃/CuI/Diox','K₂CO₃/Cu(OTf)₂/Diox',
            'K₃PO₄/CuI/DMF','K₃PO₄/Cu(OTf)₂/DMF',
            'K₂CO₃/CuI/DMF','K₂CO₃/Cu(OTf)₂/DMF']
LIGANDS  = ['Oxine','Chxn-Py-Al','THMD','BTMO','DPEO','DMPO',
            "4,4'-(tBu)bpy",'TMEDA','DMCyDA','1,10-phen',
            "4,4'-(Me)bpy","4,4'-(OMe)bpy"]

cmap_v = plt.cm.viridis
norm   = mcolors.Normalize(vmin=0, vmax=1)

n_rows, n_cols = 8, 12
xs = np.arange(1, n_cols+1, dtype=float)
ys = np.arange(n_rows, 0, -1, dtype=float)   # A at top
well_r = 0.39

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE — 3 panels: plate | condition heatmaps (×3) | correlation bar chart
# ══════════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(22, 18), facecolor='#0d0d0d')
gs  = gridspec.GridSpec(3, 4, figure=fig,
                        height_ratios=[2.0, 1.0, 1.0],
                        hspace=0.55, wspace=0.38,
                        left=0.10, right=0.97,
                        top=0.94, bottom=0.06)

# ── PANEL 1: 96-well plate ─────────────────────────────────────────────────
ax_p = fig.add_subplot(gs[0, :])
ax_p.set_facecolor('#1a1a2e')

# Plate body
ax_p.add_patch(mpatches.FancyBboxPatch(
    (0.15, 0.15), n_cols+0.7, n_rows+0.8,
    boxstyle='round,pad=0.12', lw=1.5,
    edgecolor='#4a4a6a', facecolor='#16213e', zorder=0))

for ri in range(n_rows):
    for ci in range(n_cols):
        v   = plate[ri, ci]
        col = cmap_v(norm(v))

        # Well circle
        ax_p.add_patch(mpatches.Circle(
            (xs[ci], ys[ri]), well_r,
            facecolor=col, edgecolor='#3a3a5c', lw=0.5, zorder=2))

        # Gold ring on best well
        if v == 1.0:
            ax_p.add_patch(mpatches.Circle(
                (xs[ci], ys[ri]), well_r+0.08,
                facecolor='none', edgecolor='#fbbf24', lw=2.5, zorder=3))

        # Value text — white for dark bg, dark for bright bg
        lum = 0.2126*col[0] + 0.7152*col[1] + 0.0722*col[2]
        tc  = '#111111' if lum > 0.45 else '#ffffff'
        ax_p.text(xs[ci], ys[ri], f'{v:.2f}',
                  ha='center', va='center', fontsize=5.8,
                  color=tc, fontweight='bold', zorder=4)

# Row labels (letter + sub-condition)
for ri, (rl, rs) in enumerate(zip(ROWS, ROW_SUBS)):
    ax_p.text(0.42, ys[ri], rl,
              ha='right', va='center', fontsize=10,
              fontweight='bold', color='#e2e8f0')
    ax_p.text(0.38, ys[ri]-0.30, rs,
              ha='right', va='top', fontsize=5.5, color='#94a3b8')

# Column labels (ligand names)
for ci, lig in enumerate(LIGANDS):
    ax_p.text(xs[ci], n_rows+0.92, lig,
              ha='center', va='bottom', fontsize=7.2,
              fontweight='bold', color='#e2e8f0',
              rotation=30, rotation_mode='anchor')

ax_p.set_xlim(-0.2, n_cols+0.9)
ax_p.set_ylim(-0.1, n_rows+1.5)
ax_p.set_aspect('equal')
ax_p.axis('off')
ax_p.set_title('96-Well Plate — IS-Normalised DP Yield  (normalised to maximum)',
               fontsize=12, fontweight='bold', color='#f1f5f9', pad=6)

sm = cm.ScalarMappable(cmap=cmap_v, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax_p, orientation='vertical',
                    fraction=0.015, pad=0.005, aspect=30)
cbar.set_label('Relative yield (0 = none, 1 = best)', fontsize=8, color='#94a3b8')
cbar.ax.tick_params(labelsize=7.5, colors='#94a3b8')
cbar.outline.set_edgecolor('#4a4a6a')
cbar.ax.yaxis.set_tick_params(color='#4a4a6a')

# ── PANELS 2–4: condition heatmaps ────────────────────────────────────────────
def pivot_cond(row_var, col_var='Ligand', col_order=LIGANDS):
    pv = df.pivot_table(index=row_var, columns=col_var,
                        values='norm', aggfunc='mean')
    return pv.reindex(columns=col_order, fill_value=0)

hm_cfg = [
    ('Ligand × Solvent',    pivot_cond('Solvent'),    ['DMF','Dioxane']),
    ('Ligand × Base',       pivot_cond('Base'),       ['K₂CO₃','K₃PO₄']),
    ('Ligand × Cu Source',  pivot_cond('Cu'),         ['Cu(OTf)₂','CuI']),
]

for idx, (title, pvt, row_lbls_disp) in enumerate(hm_cfg):
    ax = fig.add_subplot(gs[1, idx])
    ax.set_facecolor('#1a1a2e')
    data_arr = pvt.values

    im = ax.imshow(data_arr, aspect='auto',
                   cmap=cmap_v, vmin=0, vmax=1,
                   interpolation='nearest')

    for ri2 in range(data_arr.shape[0]):
        for ci2 in range(data_arr.shape[1]):
            v  = data_arr[ri2, ci2]
            c2 = cmap_v(norm(v))
            lm = 0.2126*c2[0]+0.7152*c2[1]+0.0722*c2[2]
            tc = '#111111' if lm > 0.45 else '#ffffff'
            ax.text(ci2, ri2, f'{v:.2f}',
                    ha='center', va='center', fontsize=5.5,
                    color=tc, fontweight='bold')

    ax.set_xticks(range(len(LIGANDS)))
    ax.set_xticklabels(LIGANDS, rotation=42, ha='right',
                       fontsize=6.5, color='#e2e8f0')
    ax.set_yticks(range(len(pvt.index)))
    ax.set_yticklabels(row_lbls_disp, fontsize=8, color='#e2e8f0')
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_edgecolor('#4a4a6a'); sp.set_linewidth(0.7)
    ax.set_title(title, fontsize=9.5, fontweight='bold',
                 color='#f1f5f9', pad=4)
    cb2 = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
    cb2.ax.tick_params(labelsize=6.5, colors='#94a3b8')
    cb2.outline.set_edgecolor('#4a4a6a')

# ── PANEL 5: correlation / effect size ────────────────────────────────────────
ax_c = fig.add_subplot(gs[1, 3])
ax_c.set_facecolor('#1a1a2e')

# Binary encode each variable; correlate with norm_yield
enc = df.copy()
enc['is_Dioxane']     = (enc['Solvent'] == 'Dioxane').astype(float)
enc['is_K2CO3']       = (enc['Base']    == 'K2CO3').astype(float)
enc['is_CuOTf2']      = (enc['Cu']      == 'Cu(OTf)2').astype(float)

# Per-ligand mean (treat each ligand as a numeric score = mean norm across its 8 wells)
lig_means = enc.groupby('Ligand')['norm'].mean()
enc['lig_score'] = enc['Ligand'].map(lig_means)

corr_vars = {
    'Dioxane\nvs DMF':         'is_Dioxane',
    'K₂CO₃\nvs K₃PO₄':        'is_K2CO3',
    'Cu(OTf)₂\nvs CuI':       'is_CuOTf2',
    'Ligand\n(mean score)':    'lig_score',
}

corr_vals, corr_labels = [], []
for lbl, col in corr_vars.items():
    r = np.corrcoef(enc[col], enc['norm'])[0, 1]
    corr_vals.append(r)
    corr_labels.append(lbl)

colors_bar = ['#22c55e' if v > 0 else '#ef4444' for v in corr_vals]
bars = ax_c.barh(corr_labels, corr_vals, color=colors_bar,
                  edgecolor='#4a4a6a', lw=0.7, height=0.55)
ax_c.axvline(0, color='#94a3b8', lw=0.8, ls='--')
for bar, v in zip(bars, corr_vals):
    ax_c.text(v + (0.01 if v >= 0 else -0.01),
              bar.get_y() + bar.get_height()/2,
              f'{v:+.3f}', va='center',
              ha='left' if v >= 0 else 'right',
              fontsize=8, color='#f1f5f9', fontweight='bold')
ax_c.set_xlim(-1.05, 1.05)
ax_c.set_xlabel('Pearson r  (vs. normalised yield)', fontsize=8, color='#94a3b8')
ax_c.set_title('Variable Correlations', fontsize=9.5,
               fontweight='bold', color='#f1f5f9', pad=4)
ax_c.tick_params(colors='#e2e8f0', labelsize=8)
ax_c.set_facecolor('#1a1a2e')
for sp in ax_c.spines.values():
    sp.set_edgecolor('#4a4a6a')
ax_c.xaxis.label.set_color('#94a3b8')
ax_c.grid(axis='x', color='#2d2d4e', lw=0.5, ls=':')

# ── PANEL 6: per-ligand bar chart ─────────────────────────────────────────────
ax_l = fig.add_subplot(gs[2, :])
ax_l.set_facecolor('#1a1a2e')

lig_df = df.groupby('Ligand')['norm'].agg(['mean','max']).reindex(LIGANDS)
x_pos  = np.arange(len(LIGANDS))
bar_w  = 0.38

b1 = ax_l.bar(x_pos - bar_w/2, lig_df['mean'], bar_w,
               label='Mean norm. yield', color='#3b82f6',
               edgecolor='#4a4a6a', lw=0.6)
b2 = ax_l.bar(x_pos + bar_w/2, lig_df['max'],  bar_w,
               label='Max norm. yield',  color='#fbbf24',
               edgecolor='#4a4a6a', lw=0.6)

ax_l.set_xticks(x_pos)
ax_l.set_xticklabels(LIGANDS, rotation=35, ha='right',
                      fontsize=8, color='#e2e8f0')
ax_l.set_ylabel('Normalised yield', fontsize=9, color='#94a3b8')
ax_l.set_title('Per-Ligand Performance  (mean and max across all 8 sub-conditions)',
               fontsize=10, fontweight='bold', color='#f1f5f9', pad=5)
ax_l.tick_params(colors='#e2e8f0', labelsize=8)
ax_l.legend(fontsize=8, facecolor='#16213e', edgecolor='#4a4a6a',
            labelcolor='#e2e8f0', framealpha=0.8)
ax_l.set_facecolor('#1a1a2e')
for sp in ax_l.spines.values():
    sp.set_edgecolor('#4a4a6a')
ax_l.yaxis.label.set_color('#94a3b8')
ax_l.grid(axis='y', color='#2d2d4e', lw=0.5, ls=':')
ax_l.set_xlim(-0.6, len(LIGANDS)-0.4)

# ── Footer ────────────────────────────────────────────────────────────────────
best = df.loc[df['norm'].idxmax()]
fig.text(0.5, 0.012,
         f"★  Best: {best['Condition']}  (well {best['Well']})  "
         f"  DP/IS = {best['ratio']:.3f}  →  norm. yield = 1.000",
         ha='center', fontsize=9, color='#fbbf24', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1c1410',
                   edgecolor='#fbbf24', lw=0.9))

out = '/home/ubuntu/rayca-sessions/a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/hte_viridis_v2.png'
fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='#0d0d0d')
plt.close(fig)
print("Saved →", out)
