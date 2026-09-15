
import sys, os
sys.path.insert(0, '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8')
from cartoon_utils import draw_helix, draw_strand, draw_loop

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.spatial import cKDTree

# Redefine helpers (dropped across call boundary)
def ca_table_fn(s, sse):
    import biotite.structure as struc
    ca = s[s.atom_name == 'CA']
    return [(int(ca.res_id[i]), ca.coord[i], sse[i]) for i in range(len(ca))]

def proj_fn(ca_list, pc_data):
    return [(r, pc_data[i, 0], pc_data[i, 2], pc_data[i, 1]) for i, (r,_,_) in enumerate(ca_list)]

def make_segs_fn(proj_list, sse_list):
    segs = []
    cur_type, cur_pts, cur_depths = sse_list[0], [], []
    for i, (r, px, py, pd) in enumerate(proj_list):
        t = sse_list[i]
        if t == cur_type:
            cur_pts.append((px, py)); cur_depths.append(pd)
        else:
            segs.append((cur_type, cur_pts, np.mean(cur_depths)))
            cur_type = t; cur_pts = [(px, py)]; cur_depths = [pd]
    segs.append((cur_type, cur_pts, np.mean(cur_depths)))
    return segs

# Rebuild projections from persisted data
proj_a = proj_fn(ca_a, pcs_a)
proj_b = proj_fn(ca_b, pcs_b)
sse_a_list = [c[2] for c in ca_a]
sse_b_list = [c[2] for c in ca_b]
segs_a = make_segs_fn(proj_a, sse_a_list)
segs_b = make_segs_fn(proj_b, sse_b_list)

# Project pocket residue Cα and CTX centroid into PCA space
def resid_proj(ca_list, pc_data, resid_set):
    return [(pc_data[i,0], pc_data[i,2]) for i,(r,_,_) in enumerate(ca_list) if r in resid_set]

# Previously identified pockets in dpCDK2-CCNE1
atp_resids   = atp_main          # chain A
iface_cdk2_r = {116,119,120,121,122}
iface_ccne1_r= {90,95,96,97,98,99,100,101,102,103,104,105}

# CTX contact residues (current structure)
ctx_cdk2_r  = {54,57,58,121,122,123,151,152,153}
ctx_ccne1_r = {90,101,102,104,105,107,108,111,149,227,228,229,233,234,237}

atp_pts      = resid_proj(ca_a, pcs_a, atp_resids)
iface_a_pts  = resid_proj(ca_a, pcs_a, iface_cdk2_r)
iface_b_pts  = resid_proj(ca_b, pcs_b, iface_ccne1_r)
ctx_a_pts    = resid_proj(ca_a, pcs_a, ctx_cdk2_r)
ctx_b_pts    = resid_proj(ca_b, pcs_b, ctx_ccne1_r)

# Project CTX centroid
ctx_cen_3d = np.array([30.57, 5.37, -25.80])
ctx_cen_pc = (ctx_cen_3d - mean) @ Vt.T
ctx_pc1, ctx_pc3 = ctx_cen_pc[0], ctx_cen_pc[2]

# ---- Draw ----
BG = '#1a1a2e'
COL_CDK2   = '#2ecc71'
COL_CCNE1  = '#6488ea'
COL_ATP    = '#4FC3F7'
COL_IFACE  = '#CE93D8'
COL_CTX    = '#FF7043'

def depth_shade(val, arr):
    lo, hi = np.percentile(arr, 5), np.percentile(arr, 95)
    return np.clip((val - lo) / (hi - lo + 1e-9), 0, 1) * 0.6 - 0.3

all_depths_a = [p[3] for p in proj_a]
all_depths_b = [p[3] for p in proj_b]

fig, ax = plt.subplots(figsize=(11, 8), facecolor=BG)
ax.set_facecolor(BG)

# Draw backbones
for seg_type, pts, mean_d in sorted(segs_a, key=lambda s: s[2]):
    if len(pts) < 2: continue
    xs, ys = zip(*pts)
    ds = depth_shade(mean_d, all_depths_a)
    if seg_type == 'a':   draw_helix(ax, list(xs), list(ys), color=COL_CDK2,  depth_shade=ds)
    elif seg_type == 'b': draw_strand(ax,list(xs), list(ys), color=COL_CDK2,  depth_shade=ds)
    else:                 draw_loop(ax,  list(xs), list(ys), color=COL_CDK2,  depth_shade=ds)

for seg_type, pts, mean_d in sorted(segs_b, key=lambda s: s[2]):
    if len(pts) < 2: continue
    xs, ys = zip(*pts)
    ds = depth_shade(mean_d, all_depths_b)
    if seg_type == 'a':   draw_helix(ax, list(xs), list(ys), color=COL_CCNE1, depth_shade=ds)
    elif seg_type == 'b': draw_strand(ax,list(xs), list(ys), color=COL_CCNE1, depth_shade=ds)
    else:                 draw_loop(ax,  list(xs), list(ys), color=COL_CCNE1, depth_shade=ds)

# Pocket halos — ATP (from dpCDK2-CCNE1)
if atp_pts:
    xs,ys = zip(*atp_pts)
    ax.scatter(xs, ys, s=200, c=COL_ATP,   alpha=0.35, zorder=5, edgecolors='none')
    ax.scatter(xs, ys, s=60,  c=COL_ATP,   alpha=0.85, zorder=6, edgecolors='none', marker='o')

# Pocket halos — interface (from dpCDK2-CCNE1)
for pts, col in [(iface_a_pts, COL_IFACE), (iface_b_pts, COL_IFACE)]:
    if pts:
        xs,ys = zip(*pts)
        ax.scatter(xs, ys, s=200, c=col, alpha=0.35, zorder=5, edgecolors='none')
        ax.scatter(xs, ys, s=60,  c=col, alpha=0.85, zorder=6, edgecolors='none', marker='o')

# CTX contact shell (current structure) — stars
for pts in [ctx_a_pts, ctx_b_pts]:
    if pts:
        xs,ys = zip(*pts)
        ax.scatter(xs, ys, s=260, c=COL_CTX, alpha=0.50, zorder=7, edgecolors='none')
        ax.scatter(xs, ys, s=90,  c=COL_CTX, alpha=1.00, zorder=8, marker='*', edgecolors='none')

# CTX centroid marker
ax.scatter([ctx_pc1],[ctx_pc3], s=350, c=COL_CTX, marker='D', zorder=9,
           edgecolors='white', linewidths=1.2, label='CTX centroid')

# Legend
legend_elems = [
    mpatches.Patch(color=COL_CDK2,  label='CDK2 (chain A)'),
    mpatches.Patch(color=COL_CCNE1, label='CyclinE1 (chain B)'),
    mpatches.Patch(color=COL_ATP,   label='ATP pocket (dpCDK2-CCNE1)', alpha=0.7),
    mpatches.Patch(color=COL_IFACE, label='Interface pocket (dpCDK2-CCNE1)', alpha=0.7),
    mpatches.Patch(color=COL_CTX,   label='CTX contact shell (CDK2-CCNE.pdb)'),
]
ax.legend(handles=legend_elems, loc='upper right', framealpha=0.25,
          labelcolor='white', fontsize=9, facecolor='#111122', edgecolor='#444466')

ax.set_title('CDK2–CyclinE1: CTX binding site vs previously identified pockets',
             color='white', fontsize=13, pad=10)
ax.tick_params(colors='#888899'); ax.set_xlabel('PC1', color='#888899'); ax.set_ylabel('PC3', color='#888899')
for sp in ax.spines.values(): sp.set_color('#333355')

out = '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8/CDK2_CTX_vs_pockets.png'
plt.tight_layout()
plt.savefig(out, dpi=150, facecolor=BG)
plt.close()
print("Saved:", out, os.path.getsize(out), "bytes")
