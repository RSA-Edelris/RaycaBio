
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import matplotlib.cm as cm

# ── Sequential colormap: white → deep teal ────────────────────────────────────
cmap_seq = mcolors.LinearSegmentedColormap.from_list(
    'hte_teal',
    ['#f5fbfc', '#c7e9f0', '#7ecfe0', '#3ba8c8', '#1a6f96', '#0a3a57'], N=256)

vmax = plate.max()
norm = mcolors.Normalize(vmin=0, vmax=vmax)

ROW_LABELS = list('ABCDEFGH')
COL_LABELS  = [str(i) for i in range(1, 13)]
n_rows, n_cols = 8, 12
well_r = 0.38
xs = np.arange(1, n_cols + 1, dtype=float)
ys = np.arange(n_rows, 0, -1, dtype=float)   # A at top

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 15), facecolor='#ffffff')
gs  = gridspec.GridSpec(2, 3, figure=fig,
                        height_ratios=[1.6, 1],
                        hspace=0.48, wspace=0.38,
                        left=0.05, right=0.97,
                        top=0.93, bottom=0.07)

# ════════════════════════════════════════════════════════════════════
# PANEL 1 — 96-well plate
# ════════════════════════════════════════════════════════════════════
ax_p = fig.add_subplot(gs[0, :])

# Plate body
ax_p.add_patch(patches.FancyBboxPatch(
    (0.2, 0.2), n_cols + 0.6, n_rows + 0.6,
    boxstyle='round,pad=0.1', lw=1.5,
    edgecolor='#6b7280', facecolor='#f8f9fa', zorder=0))

for ri in range(n_rows):
    for ci in range(n_cols):
        val   = plate[ri, ci]
        color = cmap_seq(norm(val))
        ax_p.add_patch(patches.Circle(
            (xs[ci], ys[ri]), well_r,
            facecolor=color, edgecolor='#9ca3af', lw=0.6, zorder=2))
        if val == vmax:          # gold ring on best well
            ax_p.add_patch(patches.Circle(
                (xs[ci], ys[ri]), well_r + 0.07,
                facecolor='none', edgecolor='#d97706', lw=2.5, zorder=3))
            ax_p.text(xs[ci], ys[ri] - well_r - 0.18, '★',
                      ha='center', va='top', fontsize=7,
                      color='#d97706', zorder=4)

# Row / col labels
for ri, rl in enumerate(ROW_LABELS):
    ax_p.text(0.42, ys[ri], rl, ha='right', va='center',
              fontsize=11, fontweight='bold', color='#374151')
for ci, cl in enumerate(COL_LABELS):
    ax_p.text(xs[ci], n_rows + 0.88, cl, ha='center', va='bottom',
              fontsize=9, fontweight='bold', color='#374151')

ax_p.set_xlim(0.05, n_cols + 1.05)
ax_p.set_ylim(-0.05, n_rows + 1.3)
ax_p.set_aspect('equal')
ax_p.axis('off')
ax_p.set_title('96-Well Plate — IS-Normalised DP Yield  (DP area ÷ IS area)',
               fontsize=13, fontweight='bold', color='#111827', pad=8)

sm = cm.ScalarMappable(cmap=cmap_seq, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax_p, orientation='vertical',
                    fraction=0.018, pad=0.01, aspect=28)
cbar.set_label('DP / IS  (area ratio)', fontsize=9, color='#374151')
cbar.ax.tick_params(labelsize=8, colors='#374151')
cbar.outline.set_edgecolor('#d1d5db')

# ════════════════════════════════════════════════════════════════════
# PANELS 2–4 — condition heatmaps
# ════════════════════════════════════════════════════════════════════
hm_config = [
    ('Ligand × Solvent',    pv_solv,  ['DMF', 'Dioxane']),
    ('Ligand × Base',       pv_base,  ['K₂CO₃', 'K₃PO₄']),
    ('Ligand × Cu Source',  pv_cu,    ['Cu(OTf)₂', 'CuI']),
]

for idx, (title, pvt, row_lbls) in enumerate(hm_config):
    ax = fig.add_subplot(gs[1, idx])
    data_arr = pvt.reindex(pvt.index.tolist()).values   # 2 × 12

    im = ax.imshow(data_arr, aspect='auto',
                   cmap=cmap_seq, vmin=0, vmax=vmax,
                   interpolation='nearest')

    # Cell annotations
    for ri2 in range(data_arr.shape[0]):
        for ci2 in range(data_arr.shape[1]):
            v = data_arr[ri2, ci2]
            tc = 'white' if norm(v) > 0.52 else '#374151'
            ax.text(ci2, ri2, f'{v:.2f}' if v > 0.005 else '0',
                    ha='center', va='center', fontsize=6.5,
                    color=tc, fontweight='bold')

    ax.set_xticks(range(len(lig_order)))
    ax.set_xticklabels(lig_order, rotation=42, ha='right',
                       fontsize=7.5, color='#374151')
    ax.set_yticks(range(len(pvt.index)))
    ax.set_yticklabels(row_lbls, fontsize=9, color='#374151')
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_edgecolor('#d1d5db'); sp.set_linewidth(0.8)
    ax.set_title(title, fontsize=10, fontweight='bold',
                 color='#111827', pad=5)

    cb2 = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cb2.ax.tick_params(labelsize=7, colors='#374151')
    cb2.outline.set_edgecolor('#d1d5db')

# ── Best-condition annotation ─────────────────────────────────────────────────
best = df.loc[df['norm_yield'].idxmax()]
fig.text(0.5, 0.005,
         f"★  Best: {best['Condition']}   (well {best['ID'].split('-')[1]})"
         f"   norm. yield = {best['norm_yield']:.3f}",
         ha='center', va='bottom', fontsize=9.5,
         color='#d97706', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fffbeb',
                   edgecolor='#d97706', lw=0.8))

out = '/home/ubuntu/rayca-sessions/a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/hte_heatmap.png'
fig.savefig(out, dpi=160, bbox_inches='tight', facecolor='#ffffff')
plt.close(fig)
print(f"Saved → {out}")
