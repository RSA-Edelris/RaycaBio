
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import matplotlib.cm as cm

# ── Colormap (sequential teal, 0–1 scale) ────────────────────────────────────
cmap_seq = mcolors.LinearSegmentedColormap.from_list(
    'hte_teal',
    ['#f5fbfc','#c7e9f0','#7ecfe0','#3ba8c8','#1a6f96','#0a3a57'], N=256)
norm = mcolors.Normalize(vmin=0, vmax=1)

ROW_LABELS = list('ABCDEFGH')
COL_LABELS  = [str(i) for i in range(1, 13)]

# Geometry — wider spacing so text fits comfortably
XSTEP = 1.25
YSTEP = 1.25
WELL_R = 0.44

xs = np.arange(1, n_cols + 1) * XSTEP
ys = np.arange(n_rows, 0, -1)  * YSTEP    # row A at top

fig, ax = plt.subplots(figsize=(24, 15), facecolor='#ffffff')
ax.set_facecolor('#ffffff')

# ── Plate body ────────────────────────────────────────────────────────────────
x0, y0 = xs[0] - XSTEP*0.75, ys[-1] - YSTEP*0.65
pw, ph  = xs[-1] - xs[0] + XSTEP*1.5, ys[0] - ys[-1] + YSTEP*1.3
ax.add_patch(patches.FancyBboxPatch(
    (x0, y0), pw, ph,
    boxstyle='round,pad=0.15', lw=1.8,
    edgecolor='#6b7280', facecolor='#f1f5f9', zorder=0))

# ── Wells ─────────────────────────────────────────────────────────────────────
for ri in range(n_rows):
    for ci in range(n_cols):
        xc = xs[ci]
        yc = ys[ri]
        v  = plate_norm[ri, ci]
        wid = plate_well[ri, ci]       # "001" … "096"

        color    = cmap_seq(norm(v))
        txt_col  = '#ffffff' if v > 0.48 else '#1e3a4a'
        id_col   = '#ffffff' if v > 0.48 else '#64748b'

        # Circle
        ax.add_patch(patches.Circle(
            (xc, yc), WELL_R,
            facecolor=color, edgecolor='#94a3b8', lw=0.7, zorder=2))

        # Gold ring on best well
        if v == 1.0:
            ax.add_patch(patches.Circle(
                (xc, yc), WELL_R + 0.06,
                facecolor='none', edgecolor='#d97706', lw=2.5, zorder=3))

        # Well ID — small, upper half
        ax.text(xc, yc + 0.14, wid,
                ha='center', va='center',
                fontsize=6.2, color=id_col,
                fontfamily='monospace', zorder=4)

        # Normalised value — bold, lower half
        val_str = f'{v:.2f}' if v > 0 else '0'
        ax.text(xc, yc - 0.14, val_str,
                ha='center', va='center',
                fontsize=7.2, color=txt_col,
                fontweight='bold', zorder=4)

# ── Row labels (A–H) ─────────────────────────────────────────────────────────
for ri, rl in enumerate(ROW_LABELS):
    ax.text(xs[0] - XSTEP*0.62, ys[ri], rl,
            ha='right', va='center', fontsize=12,
            fontweight='bold', color='#374151')

# ── Column labels (1–12) ─────────────────────────────────────────────────────
for ci, cl in enumerate(COL_LABELS):
    ax.text(xs[ci], ys[0] + YSTEP*0.62, cl,
            ha='center', va='bottom', fontsize=11,
            fontweight='bold', color='#374151')

ax.set_xlim(xs[0] - XSTEP, xs[-1] + XSTEP*0.8)
ax.set_ylim(ys[-1] - YSTEP*0.8, ys[0] + YSTEP*0.9)
ax.set_aspect('equal')
ax.axis('off')

# ── Title ─────────────────────────────────────────────────────────────────────
ax.set_title(
    '96-Well Plate — Normalised DP Yield  (each well ÷ plate maximum)\n'
    'Well ID (top)   ·   Normalised yield 0–1 (bottom)',
    fontsize=13, fontweight='bold', color='#111827', pad=10)

# ── Colourbar ─────────────────────────────────────────────────────────────────
sm = cm.ScalarMappable(cmap=cmap_seq, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation='vertical',
                    fraction=0.016, pad=0.01, aspect=30)
cbar.set_label('Normalised yield  (0 = no product, 1 = plate max)',
               fontsize=9, color='#374151')
cbar.ax.tick_params(labelsize=8, colors='#374151')
cbar.outline.set_edgecolor('#d1d5db')

# ── Best-well caption ────────────────────────────────────────────────────────
best = df.loc[df['norm_yield'].idxmax()]
fig.text(0.5, 0.005,
         f"★  Best well: {best['ID'].split('-')[1]}  |  {best['Condition']}  "
         f"|  IS-ratio = {best['norm_yield']:.3f}  (normalised = 1.00)",
         ha='center', va='bottom', fontsize=9.5,
         color='#d97706', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fffbeb',
                   edgecolor='#d97706', lw=0.8))

out = '/home/ubuntu/rayca-sessions/a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/hte_plate_labelled.png'
fig.savefig(out, dpi=160, bbox_inches='tight', facecolor='#ffffff')
plt.close(fig)
print(f"Saved → {out}")
