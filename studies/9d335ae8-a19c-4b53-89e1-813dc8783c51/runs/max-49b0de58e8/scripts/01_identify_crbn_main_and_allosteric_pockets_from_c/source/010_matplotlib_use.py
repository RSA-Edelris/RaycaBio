
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# ── Define pocket residue sets ────────────────────────────────────────────────
main_res = {351,352,353,354,355,356,357,358,359,379,380,381,382,388,402,404}
allo_res = {384,385,386,387,405,406,407,408,409,410,411,412,413,414,415}
zinc_res = {325,328,368,369,370,371,393,394,395,396}
lvy_resname = 'LVY'

# Collect Cα coordinates for protein, coloured by pocket membership
ca_main, ca_allo, ca_zinc, ca_other = [], [], [], []
for a in protein:
    if a['name'] != 'CA':
        continue
    rn = a['resseq']
    xyz = [a['x'], a['y'], a['z']]
    if rn in main_res:   ca_main.append(xyz)
    elif rn in allo_res: ca_allo.append(xyz)
    elif rn in zinc_res: ca_zinc.append(xyz)
    else:                ca_other.append(xyz)

ca_main  = np.array(ca_main)
ca_allo  = np.array(ca_allo)
ca_zinc  = np.array(ca_zinc)
ca_other = np.array(ca_other)

# LVY heavy atom positions
lvy_xyz = np.array([[a['x'],a['y'],a['z']] for a in lvy])
zn_xyz  = np.array([[a['x'],a['y'],a['z']] for a in zn_atm])

print(f"Cα counts — main:{len(ca_main)}  allo:{len(ca_allo)}  zinc:{len(ca_zinc)}  other:{len(ca_other)}")

# ── Build the Cα backbone trace (sorted by residue number) ───────────────────
ca_all_sorted = sorted([a for a in protein if a['name']=='CA'], key=lambda a: a['resseq'])
trace = np.array([[a['x'],a['y'],a['z']] for a in ca_all_sorted])

# ── Project onto XY and XZ planes for two informative views ──────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 8), facecolor='#1a1a2e')
fig.suptitle('CRBN – Main Pocket (IMiD/TBD) & Allosteric Pocket',
             fontsize=16, color='white', fontweight='bold', y=0.97)

colors = {'main':'#4FC3F7', 'allo':'#FF8A65', 'zinc':'#A5D6A7', 'other':'#455A64'}

for ax_idx, (ax, dim, proj) in enumerate(zip(axes,
        ['XY plane','XZ plane'], [(0,1),(0,2)])):
    ax.set_facecolor('#0d1117')
    i, j = proj

    # backbone trace
    ax.plot(trace[:,i], trace[:,j], '-', color='#37474F', lw=0.6, zorder=1, alpha=0.7)

    # other Cα
    ax.scatter(ca_other[:,i], ca_other[:,j], s=10, c=colors['other'],
               alpha=0.35, zorder=2, linewidths=0)

    # pocket Cα – larger markers
    ax.scatter(ca_zinc[:,i], ca_zinc[:,j], s=70, c=colors['zinc'],
               alpha=0.9, zorder=3, linewidths=0)
    ax.scatter(ca_main[:,i], ca_main[:,j], s=90, c=colors['main'],
               alpha=1.0, zorder=5, linewidths=0)
    ax.scatter(ca_allo[:,i], ca_allo[:,j], s=90, c=colors['allo'],
               alpha=1.0, zorder=5, linewidths=0)

    # LVY ligand
    ax.scatter(lvy_xyz[:,i], lvy_xyz[:,j], s=60, c='#FFD54F',
               marker='*', zorder=6, linewidths=0)

    # ZN ion
    ax.scatter(zn_xyz[:,i], zn_xyz[:,j], s=180, c='#A5D6A7',
               marker='D', zorder=6, edgecolors='white', linewidths=0.8)

    # highlight halos around pocket centroids
    for cen, col in [
        (ca_main.mean(axis=0),  colors['main']),
        (ca_allo.mean(axis=0),  colors['allo']),
        (ca_zinc.mean(axis=0),  colors['zinc']),
    ]:
        circ = plt.Circle((cen[i], cen[j]), 7, color=col, fill=False,
                          lw=1.5, linestyle='--', alpha=0.6, zorder=4)
        ax.add_patch(circ)

    ax.set_title(proj_label := dim, color='#CFD8DC', fontsize=11, pad=6)
    ax.set_xlabel(['X','Y','Z'][i]+' (Å)', color='#78909C', fontsize=9)
    ax.set_ylabel(['X','Y','Z'][j]+' (Å)', color='#78909C', fontsize=9)
    ax.tick_params(colors='#546E7A', labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor('#263238')

# legend
handles = [
    mpatches.Patch(color=colors['main'],  label='Main pocket / TBD\n(W382,W388,W402,H355,H359,H380,…)'),
    mpatches.Patch(color=colors['allo'],  label='Allosteric pocket\n(P384-A387 back-hairpin, T405-K415)'),
    mpatches.Patch(color=colors['zinc'],  label='Zinc coordination site\n(C325,C328,C393,C396 shell)'),
    mpatches.Patch(color='#455A64',       label='Other residues'),
    plt.Line2D([0],[0], marker='*', color='w', markerfacecolor='#FFD54F',
               markersize=12, label='LVY ligand', linestyle='None'),
    plt.Line2D([0],[0], marker='D', color='w', markerfacecolor='#A5D6A7',
               markersize=9, markeredgecolor='white', label='Zn²⁺ ion', linestyle='None'),
]
fig.legend(handles=handles, loc='lower center', ncol=3, framealpha=0.15,
           facecolor='#1a1a2e', edgecolor='#37474F',
           labelcolor='white', fontsize=8.5, bbox_to_anchor=(0.5, -0.01))

plt.tight_layout(rect=[0, 0.13, 1, 0.95])
out_path = '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8/CRBN_pockets.png'
plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {out_path}")
