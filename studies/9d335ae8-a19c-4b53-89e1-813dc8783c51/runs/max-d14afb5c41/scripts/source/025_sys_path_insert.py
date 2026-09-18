
import sys
sys.path.insert(0, '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8')
from cartoon_utils import draw_helix, draw_strand, draw_loop

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse
import numpy as np

# ── Projection helpers ────────────────────────────────────────────────────────
def proj2d(xyz):
    c = np.atleast_2d(xyz) - mu_
    return c @ V1, c @ V3
def depth_of(xyz):
    return (np.atleast_2d(xyz) - mu_) @ V2

# ── Segment builder ───────────────────────────────────────────────────────────
def make_segments(res_ids, sse, pxs, pys, depths):
    segs, i, n = [], 0, len(sse)
    while i < n:
        t = sse[i]; j = i
        while j < n and sse[j] == t: j += 1
        idx = list(range(i, j))
        segs.append(dict(type=t, idx=idx, px=pxs[idx], py=pys[idx],
                         depth=depths[idx].mean()))
        i = j
    return segs

def chain_segments(ca_atoms, sse_arr):
    coords_c = ca_atoms.coord
    pxs = (coords_c - mu_) @ V1
    pys = (coords_c - mu_) @ V3
    dps = (coords_c - mu_) @ V2
    return make_segments(ca_atoms.res_id, sse_arr, pxs, pys, dps), ca_atoms.res_id

segs_cdk2,  rids_cdk2  = chain_segments(ca_cdk2,  sse_cdk2)
segs_ccne1, rids_ccne1 = chain_segments(ca_ccne1, sse_ccne1)

# Cα lookup by (chain, resseq)
def ca_px_py(chain_atoms_list, resset):
    out = []
    for a in chain_atoms_list:
        if a['name']=='CA' and a['resseq'] in resset:
            px,py = proj2d(np.array([[a['x'],a['y'],a['z']]]))
            out.append((float(px), float(py)))
    return out

main_pts  = ca_px_py(cdk2,  MAIN_FINAL)
allo_pts  = ca_px_py(cdk2,  ALLO_FINAL)
iface_cdk2_pts  = ca_px_py(cdk2,  IFACE_FINAL)
iface_ccne1_pts = ca_px_py(ccne1, IFACE_CCNE1)

# Colours
COL_MAIN  = '#4FC3F7'   # sky blue
COL_ALLO  = '#FF7043'   # deep orange
COL_IFACE = '#CE93D8'   # lavender
BG = '#0d1117'
HELIX_A, STRAND_A, LOOP_A = '#2ecc71','#27ae60','#1a9950'
HELIX_B, STRAND_B, LOOP_B = '#5DADE2','#2E86C1','#1A5276'  # blue family for CyclinE1

# ── Figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 12), facecolor=BG)
ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')

# Draw CyclinE1 (blue) then CDK2 (green) — depth sorted across both
all_segs = (
    [(s, HELIX_B, STRAND_B, LOOP_B) for s in segs_ccne1] +
    [(s, HELIX_A, STRAND_A, LOOP_A) for s in segs_cdk2]
)
for seg, hc, sc, lc in sorted(all_segs, key=lambda x: -x[0]['depth']):
    x, y = seg['px'], seg['py']
    ds = float(np.clip(seg['depth']/35, -1, 1))
    zo = 3 + seg['depth']/120
    if seg['type']=='a' and len(x)>=3:
        draw_helix(ax, x, y, width=1.4, color=hc, zorder=zo, depth_shade=ds)
    elif seg['type']=='b' and len(x)>=2:
        draw_strand(ax, x, y, width=1.0, color=sc, zorder=zo, depth_shade=ds)
    else:
        draw_loop(ax, x, y, lw=1.2, color=lc, zorder=zo, depth_shade=ds)

# ── Pocket glows + Cα dots ─────────────────────────────────────────────────────
for pts, col, zo in [
        (iface_cdk2_pts+iface_ccne1_pts, COL_IFACE, 8),
        (allo_pts,  COL_ALLO,  9),
        (main_pts,  COL_MAIN, 10)]:
    if not pts: continue
    xs,ys = zip(*pts)
    ax.scatter(xs, ys, s=420, c=col, alpha=0.15, zorder=zo-0.5, linewidths=0)
    ax.scatter(xs, ys, s=200, c=col, alpha=0.30, zorder=zo-0.3, linewidths=0)
    ax.scatter(xs, ys, s=90,  c=col, alpha=1.0,  zorder=zo,
               edgecolors='white', linewidths=0.5)

# ── Labels ────────────────────────────────────────────────────────────────────
def pocket_cen(pts): return np.mean(pts,axis=0)
for label, pts, col, dxy in [
        ('ATP-binding pocket\n(K33, E51, F80-H84,\nD127, DFG145-147, C177)',
         main_pts, COL_MAIN, (-17, -6)),
        ('Allosteric pocket\n(T-loop / activation loop\nV156–S181)',
         allo_pts, COL_ALLO, (8, -8)),
        ('CDK2–CyclinE1\ninterface',
         iface_cdk2_pts+iface_ccne1_pts, COL_IFACE, (-16, 8))]:
    if not pts: continue
    cx,cy = pocket_cen(pts)
    ax.annotate(label, xy=(cx,cy), xytext=(cx+dxy[0], cy+dxy[1]),
                fontsize=8.5, color=col, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.35', facecolor='#0d1117',
                          edgecolor=col, linewidth=1.0, alpha=0.88),
                arrowprops=dict(arrowstyle='->', color=col, lw=1.2), zorder=20)

# ── Chain labels ──────────────────────────────────────────────────────────────
for ca_arr, lbl, col in [(ca_cdk2,'CDK2 (chain A)',HELIX_A),
                          (ca_ccne1,'CyclinE1 (chain B)',HELIX_B)]:
    pxs = (ca_arr.coord - mu_) @ V1
    pys = (ca_arr.coord - mu_) @ V3
    ax.text(float(pxs.max())+1.5, float(pys[np.argmax(pxs)]),
            lbl, color=col, fontsize=9, fontweight='bold', zorder=22)

# ── Legend ────────────────────────────────────────────────────────────────────
handles = [
    mpatches.Patch(color=HELIX_A,  label='CDK2 α-helix'),
    mpatches.Patch(color=STRAND_A, label='CDK2 β-strand'),
    mpatches.Patch(color=LOOP_A,   label='CDK2 loop'),
    mpatches.Patch(color=HELIX_B,  label='CyclinE1 α-helix'),
    mpatches.Patch(color=STRAND_B, label='CyclinE1 β-strand'),
    mpatches.Patch(color=LOOP_B,   label='CyclinE1 loop'),
    plt.Line2D([0],[0],marker='o',color='w',markerfacecolor=COL_MAIN, markersize=10,
               label='Main pocket (ATP-binding)',linestyle='None'),
    plt.Line2D([0],[0],marker='o',color='w',markerfacecolor=COL_ALLO, markersize=10,
               label='Allosteric pocket (T-loop)',linestyle='None'),
    plt.Line2D([0],[0],marker='o',color='w',markerfacecolor=COL_IFACE,markersize=10,
               label='CDK2–CyclinE1 interface',linestyle='None'),
]
ax.legend(handles=handles, loc='lower right', fontsize=8.5, framealpha=0.2,
          facecolor='#0d1117', edgecolor='#37474F', labelcolor='white', ncol=3)

ax.set_title('dpCDK2–CyclinE1 — Cartoon with Pocket Highlights',
             color='white', fontsize=14, fontweight='bold', pad=12)

plt.tight_layout()
out = '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8/CDK2_CCNE1_cartoon_pockets.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print(f"Saved: {out}")
