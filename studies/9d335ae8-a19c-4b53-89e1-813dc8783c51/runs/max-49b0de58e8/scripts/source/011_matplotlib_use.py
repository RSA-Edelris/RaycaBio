
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# ── Gather Cα positions with labels for all pocket residues ──────────────────
def get_ca(protein, resids):
    out = {}
    for a in protein:
        if a['name'] == 'CA' and a['resseq'] in resids:
            out[a['resseq']] = (a['resname'], a['x'], a['y'], a['z'])
    return out

main_res  = {351,352,353,354,355,356,357,358,359,379,380,381,382,388,402,404}
allo_res  = {384,385,386,387,405,406,407,408,409,410,411,412,413,414,415}
zinc_res  = {325,328,368,369,370,371,393,394,395,396}

ca_main_d = get_ca(protein, main_res)
ca_allo_d = get_ca(protein, allo_res)
ca_zinc_d = get_ca(protein, zinc_res)

# Build Cα backbone trace
ca_sorted = sorted([a for a in protein if a['name']=='CA'], key=lambda a: a['resseq'])
trace = np.array([[a['x'],a['y'],a['z']] for a in ca_sorted])

# LVY and ZN
lvy_xyz = np.array([[a['x'],a['y'],a['z']] for a in lvy])
zn_xyz  = np.array([[a['x'],a['y'],a['z']] for a in zn_atm])

# ── Create annotated figure (XZ projection – most informative view) ──────────
fig, axes = plt.subplots(1, 3, figsize=(20, 8), facecolor='#0d1117',
                          gridspec_kw={'width_ratios':[1.4,1.4,0.8]})
fig.suptitle('CRBN Pocket Analysis — Residue-level Annotation',
             fontsize=15, color='white', fontweight='bold', y=0.98)

COLS = {'main':'#4FC3F7','allo':'#FF8A65','zinc':'#A5D6A7','other':'#37474F'}

for ax_i, (ax, proj, title) in enumerate(zip(
        axes[:2],
        [(0,1),(0,2)],
        ['XY projection','XZ projection'])):
    ax.set_facecolor('#0d1117')
    i, j = proj
    lbl = ['X','Y','Z']

    # backbone
    ax.plot(trace[:,i], trace[:,j], '-', color='#263238', lw=0.7, zorder=1, alpha=0.8)

    # other Cα (tiny)
    other = np.array([[a['x'],a['y'],a['z']] for a in protein
                       if a['name']=='CA'
                       and a['resseq'] not in main_res|allo_res|zinc_res])
    if len(other):
        ax.scatter(other[:,i], other[:,j], s=8, c=COLS['other'], alpha=0.3, zorder=2, linewidths=0)

    # LVY
    ax.scatter(lvy_xyz[:,i], lvy_xyz[:,j], s=50, c='#FFD54F',
               marker='*', zorder=6, linewidths=0, label='LVY ligand')
    # ZN
    ax.scatter(zn_xyz[:,i], zn_xyz[:,j], s=200, c='#A5D6A7',
               marker='D', zorder=7, edgecolors='white', linewidths=1.2, label='Zn²⁺')

    # Plot pocket residues with labels
    for pocket_d, col, offset_mult in [
            (ca_zinc_d, COLS['zinc'], 1.0),
            (ca_main_d, COLS['main'], 1.0),
            (ca_allo_d, COLS['allo'], 1.0)]:
        xs = [v[1+i] for v in pocket_d.values()]   # v = (resname, x, y, z)
        ys = [v[1+j] for v in pocket_d.values()]
        ax.scatter(xs, ys, s=80, c=col, alpha=1.0, zorder=5, linewidths=0)

        # Label every residue
        for rseq, (rname, x, y, z) in pocket_d.items():
            coord = [x, y, z]
            px, py = coord[i], coord[j]
            ax.annotate(f'{rname[:3]}{rseq}',
                        xy=(px, py), xytext=(px+1.2*offset_mult, py+1.2*offset_mult),
                        fontsize=5.5, color=col, alpha=0.92,
                        arrowprops=dict(arrowstyle='-', color=col, lw=0.4, alpha=0.5),
                        zorder=8)

    # Dashed ellipse halos
    from matplotlib.patches import Ellipse
    for pocket_d, col in [(ca_main_d,COLS['main']),(ca_allo_d,COLS['allo']),(ca_zinc_d,COLS['zinc'])]:
        xs = np.array([v[1+i] for v in pocket_d.values()])
        ys = np.array([v[1+j] for v in pocket_d.values()])
        if len(xs) < 2: continue
        cx,cy = xs.mean(), ys.mean()
        wx = max(xs.max()-xs.min(), 4)+6
        wy = max(ys.max()-ys.min(), 4)+6
        el = Ellipse((cx,cy), wx, wy, fill=False, edgecolor=col,
                     linestyle='--', lw=1.2, alpha=0.5, zorder=3)
        ax.add_patch(el)

    ax.set_title(title, color='#CFD8DC', fontsize=11, pad=5)
    ax.set_xlabel(lbl[i]+' (Å)', color='#78909C', fontsize=9)
    ax.set_ylabel(lbl[j]+' (Å)', color='#78909C', fontsize=9)
    ax.tick_params(colors='#546E7A', labelsize=7)
    for sp in ax.spines.values(): sp.set_edgecolor('#1c2833')

# ── Third panel: residue table ────────────────────────────────────────────────
ax3 = axes[2]; ax3.axis('off'); ax3.set_facecolor('#0d1117')

def aa1(three):
    d={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E',
       'GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F',
       'PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
    return d.get(three,'?')

sections = [
    ('Main pocket (TBD/IMiD-binding)', COLS['main'], ca_main_d),
    ('Allosteric pocket (back-hairpin + C-term)', COLS['allo'], ca_allo_d),
    ('Zinc coordination shell', COLS['zinc'], ca_zinc_d),
]
y = 0.97
for title_txt, col, pocket_d in sections:
    ax3.text(0.0, y, title_txt, transform=ax3.transAxes,
             color=col, fontsize=8.5, fontweight='bold')
    y -= 0.035
    # Format as a compact table
    rows = sorted(pocket_d.items())
    line_parts = [f"{aa1(rname)}{rseq}" for rseq,(rname,_,_,_) in rows]
    # wrap at 4 per line
    for k in range(0, len(line_parts), 5):
        ax3.text(0.02, y, '  '.join(line_parts[k:k+5]),
                 transform=ax3.transAxes, color='#CFD8DC', fontsize=7.5, family='monospace')
        y -= 0.032
    y -= 0.025

# Literature comparison note
ax3.text(0.0, y, 'Literature (Fischer 2014, Chamberlain 2014)', 
         transform=ax3.transAxes, color='#FFD54F', fontsize=8, fontweight='bold')
y -= 0.035
lit_notes = [
    'Main: W380,W400,W404 tri-Trp cage',
    '      H378, Y355 H-bond donors',
    '      N351/Q99 neosubstrate contacts',
    'Allosteric: back β-hairpin pocket',
    '      (Matyskiela 2018, Heim 2019)',
    '      C-term groove T403-K415',
    'Zinc: C323/C326/C391/C394 (tetra)',
    '      (Hartmann 2019 – LON domain)',
]
for note in lit_notes:
    ax3.text(0.02, y, note, transform=ax3.transAxes,
             color='#90A4AE', fontsize=7.2, family='monospace')
    y -= 0.032

plt.tight_layout(rect=[0,0,1,0.96])
out2 = '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8/CRBN_pockets_annotated.png'
plt.savefig(out2, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {out2}")
