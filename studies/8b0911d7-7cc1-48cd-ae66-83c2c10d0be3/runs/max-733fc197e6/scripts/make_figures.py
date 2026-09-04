#!/usr/bin/env python3
"""
Generate publication-quality figures for the docking report.
Requires: matplotlib, rdkit, numpy
Produces:
  - figures/pocket_residues.png  : pocket residue contact bar chart
  - figures/score_comparison.png : docking score bar chart for all 4 ligands
  - figures/enantiomer_delta.png : delta affinity between enantiomers
  - figures/<id>_interaction.png : per-ligand interaction heatmap
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

WORKDIR = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc'
FIG_DIR = os.path.join(WORKDIR, 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# ── Score data (updated from docking results) ──
# Format: {id, label, kd_exp, score_best, all_scores}
LIGAND_DATA = [
    {'id': 'EDS00760714-1', 'label': 'Cpd32 (R)', 'kd': '1–5 µM', 'stereo': 'R',
     'score': -7.0, 'scores': [-7.0, -6.9, -6.8, -6.8, -6.7]},
    {'id': 'EDS00760714-2', 'label': 'Cpd32 (S)', 'kd': 'n.d.',   'stereo': 'S',
     'score': -6.7, 'scores': [-6.7, -6.6, -6.6, -6.6, -6.5]},
    {'id': 'EDS00760778-1', 'label': 'Cpd16 (R)', 'kd': '<1 µM',  'stereo': 'R',
     'score': None, 'scores': []},   # filled when results arrive
    {'id': 'EDS00760778-2', 'label': 'Cpd16 (S)', 'kd': 'n.d.',   'stereo': 'S',
     'score': None, 'scores': []},
]

# Overwrite with any result JSON files present
for lig in LIGAND_DATA:
    rj = os.path.join(WORKDIR, 'ligands', f"{lig['id']}_results.json")
    if os.path.exists(rj):
        with open(rj) as f:
            d = json.load(f)
        lig['score'] = d.get('best_affinity_kcal_mol', lig['score'])
        lig['scores'] = d.get('affinities_kcal_mol', lig['scores'])
        print(f"Loaded {lig['id']}: {lig['score']} kcal/mol")

# ── Palette ──
COLOR_R = '#2E86AB'   # R enantiomers - blue
COLOR_S = '#E84855'   # S enantiomers - red
COLORS  = [COLOR_R if d['stereo']=='R' else COLOR_S for d in LIGAND_DATA]

# ── Figure 1: Docking score bar chart ──
valid = [d for d in LIGAND_DATA if d['score'] is not None]
labels  = [d['label'] for d in valid]
scores  = [d['score'] for d in valid]
colors  = [COLOR_R if d['stereo']=='R' else COLOR_S for d in valid]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(labels, scores, color=colors, edgecolor='black', linewidth=0.8, width=0.55)
ax.set_ylabel('Vina ΔGᵇᵉⁿᵈ (kcal/mol)', fontsize=12)
ax.set_title('AutoDock-Vina Docking Scores\nPTPN2/TCPTP Allosteric Site (9C56)', fontsize=13, fontweight='bold')
ax.axhline(0, color='black', lw=0.5)
ax.set_ylim(min(scores)*1.15 if scores else -8, 0.5)
for bar, score in zip(bars, scores):
    ax.text(bar.get_x()+bar.get_width()/2, score - 0.1, f'{score:.1f}', ha='center', va='top', fontsize=10, fontweight='bold', color='white')
patch_r = mpatches.Patch(color=COLOR_R, label='R enantiomer')
patch_s = mpatches.Patch(color=COLOR_S, label='S enantiomer')
ax.legend(handles=[patch_r, patch_s], loc='lower right', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'score_comparison.png'), dpi=150)
plt.close(fig)
print('Saved score_comparison.png')

# ── Figure 2: All 5 poses per ligand (scatter) ──
valid_all = [d for d in LIGAND_DATA if d['scores']]
if valid_all:
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, lig in enumerate(valid_all):
        x = [i + 0.1*j for j in range(len(lig['scores']))]
        c = COLOR_R if lig['stereo']=='R' else COLOR_S
        ax.scatter(x, lig['scores'], color=c, s=80, zorder=3, edgecolors='black', lw=0.5)
        ax.plot([i, i+0.1*(len(lig['scores'])-1)], [lig['scores'][0], lig['scores'][-1]],
                color=c, alpha=0.4, lw=1)
    ax.set_xticks(range(len(valid_all)))
    ax.set_xticklabels([d['label'] for d in valid_all], fontsize=11)
    ax.set_ylabel('Vina score (kcal/mol)', fontsize=11)
    ax.set_title('Top 5 Docking Poses per Compound', fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, 'poses_scatter.png'), dpi=150)
    plt.close(fig)
    print('Saved poses_scatter.png')

# ── Figure 3: Enantiomer comparison ──
pairs = [
    ('EDS00760714', 'Compound 32'),
    ('EDS00760778', 'Compound 16'),
]
pair_data = []
for root_id, name in pairs:
    r_lig = next((d for d in LIGAND_DATA if d['id']==f'{root_id}-1'), None)
    s_lig = next((d for d in LIGAND_DATA if d['id']==f'{root_id}-2'), None)
    if r_lig and s_lig and r_lig['score'] and s_lig['score']:
        delta = r_lig['score'] - s_lig['score']
        pair_data.append({'name': name, 'R': r_lig['score'], 'S': s_lig['score'], 'delta': delta})

if pair_data:
    fig, ax = plt.subplots(figsize=(6, 5))
    x = np.arange(len(pair_data))
    w = 0.35
    r_bars = ax.bar(x - w/2, [p['R'] for p in pair_data], w, label='R enantiomer', color=COLOR_R, edgecolor='k', lw=0.8)
    s_bars = ax.bar(x + w/2, [p['S'] for p in pair_data], w, label='S enantiomer', color=COLOR_S, edgecolor='k', lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([p['name'] for p in pair_data], fontsize=12)
    ax.set_ylabel('Vina ΔG (kcal/mol)', fontsize=11)
    ax.set_title('Enantiomer Docking Score Comparison', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    for pd_ in pair_data:
        print(f"  {pd_['name']}: R={pd_['R']}, S={pd_['S']}, ΔΔG={pd_['delta']:.1f} kcal/mol (R vs S)")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, 'enantiomer_comparison.png'), dpi=150)
    plt.close(fig)
    print('Saved enantiomer_comparison.png')

# ── Figure 4: Pocket residue interaction map ──
POCKET_RESIDUES = ['SER188','PRO189','ALA190','LEU193','ASN194',
                   'PHE197','LYS198','GLU201','GLU274','GLY275',
                   'LYS277','CYS278','ILE279','LYS280']
RESIDUE_TYPE = {
    'SER188': 'polar', 'PRO189': 'hydrophobic', 'ALA190': 'hydrophobic',
    'LEU193': 'hydrophobic', 'ASN194': 'polar', 'PHE197': 'hydrophobic',
    'LYS198': 'charged+', 'GLU201': 'charged-', 'GLU274': 'charged-',
    'GLY275': 'polar', 'LYS277': 'charged+', 'CYS278': 'polar',
    'ILE279': 'hydrophobic', 'LYS280': 'charged+'
}
TYPE_COLOR = {'polar':'#8ecae6','hydrophobic':'#f4a261','charged+':'#2a9d8f','charged-':'#e76f51'}

fig, ax = plt.subplots(figsize=(10, 4))
res_x = np.arange(len(POCKET_RESIDUES))
res_colors = [TYPE_COLOR[RESIDUE_TYPE[r]] for r in POCKET_RESIDUES]
ax.bar(res_x, [1]*len(POCKET_RESIDUES), color=res_colors, edgecolor='black', lw=0.5, width=0.8)
ax.set_xticks(res_x)
ax.set_xticklabels(POCKET_RESIDUES, rotation=45, ha='right', fontsize=9)
ax.set_yticks([])
ax.set_title('Allosteric Binding Site Residues (PTPN2, within 5Å of FRJ)', fontsize=11, fontweight='bold')
handles = [mpatches.Patch(color=v, label=k) for k,v in TYPE_COLOR.items()]
ax.legend(handles=handles, loc='upper right', fontsize=9)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'pocket_residues.png'), dpi=150)
plt.close(fig)
print('Saved pocket_residues.png')
print('\nALL FIGURES DONE')
