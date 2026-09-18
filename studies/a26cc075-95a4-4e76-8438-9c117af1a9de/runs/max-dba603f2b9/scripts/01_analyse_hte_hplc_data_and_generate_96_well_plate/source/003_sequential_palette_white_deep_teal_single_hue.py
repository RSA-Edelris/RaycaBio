
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np
import seaborn as sns

# ── Sequential palette: white → deep teal (single hue, magnitude) ─────────────
# Validated sequential: lightness 97 → 25, single hue ~195° (teal)
cmap_seq = mcolors.LinearSegmentedColormap.from_list(
    'hte_teal',
    ['#f5fbfc', '#c7e9f0', '#7ecfe0', '#3ba8c8', '#1a6f96', '#0a3a57'],
    N=256)

vmax = plate.max()

# ── Figure layout ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 15), facecolor='#ffffff')
fig.patch.set_facecolor('#ffffff')

gs = gridspec.GridSpec(
    2, 3,
    figure=fig,
    height_ratios=[1.6, 1],
    hspace=0.45,
    wspace=0.35,
    left=0.06, right=0.96,
    top=0.93, bottom=0.06
)

# ════════════════════════════════════════════════════════════════════════════
# PANEL 1 — 96-well plate heatmap
# ════════════════════════════════════════════════════════════════════════════
ax_plate = fig.add_subplot(gs[0, :])   # spans all 3 columns

ROW_LABELS = list('ABCDEFGH')
COL_LABELS = [str(i) for i in range(1, 13)]
n_rows, n_cols = 8, 12

# Well geometry
well_r   = 0.38        # circle radius in data units
x_pad, y_pad = 0.6, 0.6

xs = np.arange(1, n_cols + 1, dtype=float)
ys = np.arange(n_rows, 0, -1, dtype=float)   # row A at top

# Plate body
rect = patches.FancyBboxPatch(
    (0.2, 0.2), n_cols + 0.6, n_rows + 0.6,
    boxstyle='round,pad=0.1', linewidth=1.5,
    edgecolor='#6b7280', facecolor='#f8f9fa', zorder=0)
ax_plate.add_patch(rect)

norm = mcolors.Normalize(vmin=0, vmax=vmax)

for ri in range(n_rows):
    for ci in range(n_cols):
        y_val = ys[ri]
        x_val = xs[ci]
        val   = plate[ri, ci]
        color = cmap_seq(norm(val))

        circ = patches.Circle(
            (x_val, y_val), well_r,
            facecolor=color, edgecolor='#9ca3af', linewidth=0.6, zorder=2)
        ax_plate.add_patch(circ)

        # Mark best well with gold ring
        if val == vmax:
            ring = patches.Circle(
                (x_val, y_val), well_r + 0.06,
                facecolor='none', edgecolor='#d97706', linewidth=2.2, zorder=3)
            ax_plate.add_patch(ring)
            ax_plate.text(x_val, y_val - well_r - 0.15, '★',
                          ha='center', va='top', fontsize=7,
                          color='#d97706', zorder=4)

# Row labels (A–H) left side
for ri, rl in enumerate(ROW_LABELS):
    ax_plate.text(0.45, ys[ri], rl,
                  ha='right', va='center', fontsize=10,
                  fontweight='bold', color='#374151')

# Column labels (1–12) top
for ci, cl in enumerate(COL_LABELS):
    ax_plate.text(xs[ci], n_rows + 0.85, cl,
                  ha='center', va='bottom', fontsize=9,
                  fontweight='bold', color='#374151')

ax_plate.set_xlim(0.1, n_cols + 1.0)
ax_plate.set_ylim(0.0, n_rows + 1.2)
ax_plate.set_aspect('equal')
ax_plate.axis('off')
ax_plate.set_title('96-Well Plate — IS-Normalised DP Yield  (DP area / IS area)',
                   fontsize=13, fontweight='bold', color='#111827', pad=8)

# Colorbar
sm = cm.ScalarMappable(cmap=cmap_seq, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax_plate, orientation='vertical',
                    fraction=0.018, pad=0.01, aspect=28)
cbar.set_label('DP / IS  (area ratio)', fontsize=9, color='#374151')
cbar.ax.tick_params(labelsize=8, colors='#374151')
cbar.outline.set_edgecolor('#d1d5db')

# ════════════════════════════════════════════════════════════════════════════
# PANELS 2–4 — condition heatmaps
# ════════════════════════════════════════════════════════════════════════════
cbar_kw = dict(cmap=cmap_seq, vmin=0, vmax=vmax)

hm_titles = ['Ligand × Solvent', 'Ligand × Base', 'Ligand × Cu Source']
hm_data   = [pv_solv, pv_base, pv_cu]
row_labels_list = [
    ['DMF', 'Dioxane'],
    ['K₂CO₃', 'K₃PO₄'],
    ['Cu(OTf)₂', 'CuI'],
]

for idx, (title, pvt, rlabels) in enumerate(zip(hm_titles, hm_data, row_labels_list)):
    ax = fig.add_subplot(gs[1, idx])

    # Re-index rows for display label order
    data_arr = pvt.reindex(pvt.index.tolist()).values

    im = ax.imshow(data_arr, aspect='auto',
                   cmap=cmap_seq, vmin=0, vmax=vmax,
                   interpolation='nearest')

    # Annotate cells with value
    for ri2 in range(data_arr.shape[0]):
        for ci2 in range(data_arr.shape[1]):
            v = data_arr[ri2, ci2]
            txt_col = 'white' if norm(v) > 0.55 else '#374151'
            ax.text(ci2, ri2, f'{v:.2f}' if v > 0.01 else '0',
                    ha='center', va='center', fontsize=6.5,
                    color=txt_col, fontweight='bold')

    ax.set_xticks(range(len(lig_order)))
    ax.set_xticklabels(lig_order, rotation=40, ha='right', fontsize=7.5,
                       color='#374151')
    ax.set_yticks(range(len(pvt.index)))
    ax.set_yticklabels(rlabels, fontsize=8.5, color='#374151')
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_edgecolor('#d1d5db')
        spine.set_linewidth(0.8)

    ax.set_title(title, fontsize=10, fontweight='bold',
                 color='#111827', pad=5)

    cb2 = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cb2.ax.tick_params(labelsize=7, colors='#374151')
    cb2.outline.set_edgecolor('#d1d5db')

# ── Figure-level annotation ────────────────────────────────────────────────
best_row = df.loc[df['norm_yield'].idxmax()]
note = (f"★ Best condition:  {best_row['Condition']}  "
        f"(well {best_row['ID'].split('-')[1]})  "
        f"— norm. yield = {best_row['norm_yield']:.3f}")
fig.text(0.5, 0.002, note, ha='center', va='bottom',
         fontsize=9, color='#d97706', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fffbeb',
                   edgecolor='#d97706', linewidth=0.8))

out_path = '/home/ubuntu/rayca-sessions/a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/hte_heatmap.png'
fig.savefig(out_path, dpi=160, bbox_inches='tight', facecolor='#ffffff')
plt.close(fig)
print(f"Saved → {out_path}")
