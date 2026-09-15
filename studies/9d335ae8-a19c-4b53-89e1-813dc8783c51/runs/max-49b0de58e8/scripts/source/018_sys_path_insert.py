
import sys
sys.path.insert(0, '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8')
from cartoon_utils import draw_helix, draw_strand, draw_loop, smooth_spline

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Projection helper (re-define) ─────────────────────────────────────────────
mu_ = coords.mean(axis=0)
def proj(xyz):
    c = np.atleast_2d(xyz) - mu_
    return c @ V1, c @ V3
def depth_of(xyz):
    return (np.atleast_2d(xyz) - mu_) @ V2

# ── Colour palette ─────────────────────────────────────────────────────────────
HELIX_COL = '#2ecc71'   # bright green
STRAND_COL= '#27ae60'   # mid green  
LOOP_COL  = '#1a9950'   # dark green
MAIN_COL  = '#4FC3F7'   # sky blue
ALLO_COL  = '#FF7043'   # deep orange
ZINC_COL  = '#80CBC4'   # teal
LIG_COL   = '#FFD54F'   # amber

BG = '#0d1117'

# ── Rebuild segments (need function here) ─────────────────────────────────────
def make_segments(res_ids, sse, px, py, depth):
    segs = []
    n = len(sse)
    i = 0
    while i < n:
        t = sse[i]; j = i
        while j < n and sse[j] == t: j += 1
        idx = list(range(i, j))
        segs.append(dict(type=t, idx=idx, px=px[idx], py=py[idx],
                         depth=depth[idx].mean()))
        i = j
    return segs

_px, _py = proj(coords)
_px = _px[0] if _px.ndim>1 else _px  # flatten
_py = _py[0] if _py.ndim>1 else _py

# proj returns 1D arrays when coords is 2D
_px, _py = (coords - mu_) @ V1, (coords - mu_) @ V3
_depth    = (coords - mu_) @ V2

segments = make_segments(res_ids, sse, _px, _py, _depth)

# ── Figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 11), facecolor=BG)
ax.set_facecolor(BG)
ax.set_aspect('equal')
ax.axis('off')

# Depth-sort segments (back to front)
for seg in sorted(segments, key=lambda s: -s['depth']):
    ds = np.clip(seg['depth']/30, -1, 1)   # depth shade
    x, y = seg['px'], seg['py']
    if seg['type'] == 'a' and len(x) >= 3:
        draw_helix(ax, x, y, width=1.5, color=HELIX_COL, zorder=3+seg['depth']/100, depth_shade=ds)
    elif seg['type'] == 'b' and len(x) >= 2:
        draw_strand(ax, x, y, width=1.1, color=STRAND_COL, zorder=3+seg['depth']/100, depth_shade=ds)
    else:
        draw_loop(ax, x, y, lw=1.3, color=LOOP_COL, zorder=2+seg['depth']/100, depth_shade=ds)

# ── Pocket residue HALOS + Cα dots ────────────────────────────────────────────
for res_set, col, label, ms, zo in [
        (ZINC_RES,  ZINC_COL, 'Zinc site',              140, 8),
        (ALLO_RES,  ALLO_COL, 'Allosteric pocket',      160, 9),
        (MAIN_RES,  MAIN_COL, 'Main pocket (TBD/IMiD)', 160, 10)]:
    xi = [_px[i] for i,r in enumerate(res_ids) if int(r) in res_set]
    yi = [_py[i] for i,r in enumerate(res_ids) if int(r) in res_set]
    # glow halo
    ax.scatter(xi, yi, s=ms*2.8, c=col, alpha=0.18, zorder=zo-0.5, linewidths=0)
    ax.scatter(xi, yi, s=ms*1.4, c=col, alpha=0.35, zorder=zo-0.3, linewidths=0)
    # solid dot
    ax.scatter(xi, yi, s=ms*0.75, c=col, alpha=1.0, zorder=zo,
               edgecolors='white', linewidths=0.5)

# ── LVY ligand (amber stars) ──────────────────────────────────────────────────
lvy_px2, lvy_py2 = (LVY_XYZ - mu_) @ V1, (LVY_XYZ - mu_) @ V3
ax.scatter(lvy_px2, lvy_py2, s=90, c=LIG_COL, marker='*',
           zorder=12, linewidths=0, alpha=0.95)
lvy_cx, lvy_cy = lvy_px2.mean(), lvy_py2.mean()
ax.scatter([lvy_cx], [lvy_cy], s=420, c=LIG_COL, alpha=0.20, zorder=11, linewidths=0)

# ── Zn²⁺ ion ──────────────────────────────────────────────────────────────────
zn_px2, zn_py2 = (ZN_XYZ - mu_) @ V1, (ZN_XYZ - mu_) @ V3
ax.scatter(zn_px2, zn_py2, s=260, c=ZINC_COL, marker='D',
           zorder=12, edgecolors='white', linewidths=1.2)
ax.scatter(zn_px2, zn_py2, s=600, c=ZINC_COL, alpha=0.20, zorder=11, linewidths=0)

# ── Pocket labels ─────────────────────────────────────────────────────────────
label_offsets = {
    'Main pocket\n(TBD / IMiD-binding)':
        (np.mean([_px[i] for i,r in enumerate(res_ids) if int(r) in MAIN_RES]),
         np.mean([_py[i] for i,r in enumerate(res_ids) if int(r) in MAIN_RES]),
         MAIN_COL, (-12, -9)),
    'Allosteric pocket\n(back-hairpin + C-term)':
        (np.mean([_px[i] for i,r in enumerate(res_ids) if int(r) in ALLO_RES]),
         np.mean([_py[i] for i,r in enumerate(res_ids) if int(r) in ALLO_RES]),
         ALLO_COL, (8, 6)),
    'Zinc coordination\n(C325/C328/C393/C396)':
        (np.mean([_px[i] for i,r in enumerate(res_ids) if int(r) in ZINC_RES]),
         np.mean([_py[i] for i,r in enumerate(res_ids) if int(r) in ZINC_RES]),
         ZINC_COL, (-14, 6)),
}
for txt, (cx, cy, col, (dx, dy)) in label_offsets.items():
    ax.annotate(txt, xy=(cx, cy), xytext=(cx+dx, cy+dy),
                fontsize=9, color=col, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.35', facecolor='#0d1117',
                          edgecolor=col, linewidth=1.0, alpha=0.85),
                arrowprops=dict(arrowstyle='->', color=col, lw=1.2),
                zorder=20)

# ── Legend ────────────────────────────────────────────────────────────────────
handles = [
    mpatches.Patch(color=HELIX_COL, label='α-helix'),
    mpatches.Patch(color=STRAND_COL, label='β-strand'),
    mpatches.Patch(color=LOOP_COL,  label='Loop / coil'),
    plt.Line2D([0],[0], marker='o', color='w', markerfacecolor=MAIN_COL,
               markersize=10, label='Main pocket (TBD)', linestyle='None'),
    plt.Line2D([0],[0], marker='o', color='w', markerfacecolor=ALLO_COL,
               markersize=10, label='Allosteric pocket', linestyle='None'),
    plt.Line2D([0],[0], marker='o', color='w', markerfacecolor=ZINC_COL,
               markersize=9, label='Zinc coordination', linestyle='None'),
    plt.Line2D([0],[0], marker='*', color='w', markerfacecolor=LIG_COL,
               markersize=12, label='LVY ligand', linestyle='None'),
    plt.Line2D([0],[0], marker='D', color='w', markerfacecolor=ZINC_COL,
               markersize=9, markeredgecolor='white',
               label='Zn²⁺ ion', linestyle='None'),
]
legend = ax.legend(handles=handles, loc='lower right', fontsize=9,
                   framealpha=0.2, facecolor='#0d1117', edgecolor='#37474F',
                   labelcolor='white', ncol=2, markerscale=1.0)

ax.set_title('CRBN — Cartoon (green) with Pocket Highlights',
             color='white', fontsize=14, fontweight='bold', pad=12)

plt.tight_layout()
out = '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8/CRBN_cartoon_pockets.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print(f"Saved: {out}")
