
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np

# ── Color coding by Cu source (adjusted for white background) ─────────────────
CU_COLORS = {
    'CuI':       '#2563eb',   # strong blue
    'Cu(OTf)2':  '#d97706',   # amber/gold
    'CuBr':      '#60a5fa',   # light blue
    'CuCl':      '#93c5fd',   # lighter blue
    'Cu(OAc)2':  '#ea580c',   # orange
    'Cu2O':      '#7c3aed',   # violet
}

ROWS_DESIGN = [
    ('A', 'K2CO3',  'Dioxane'),
    ('B', 'K2CO3',  'DMF'),
    ('C', 'Cs2CO3', 'Dioxane'),
    ('D', 'Cs2CO3', 'DMF'),
    ('E', 'K3PO4',  'Dioxane'),
    ('F', 'K3PO4',  'DMF'),
    ('G', 'K2CO3',  'DMSO'),
    ('H', 'K2CO3',  'MeCN'),
]
COLS_DESIGN = [
    (1,'CuI',5),(2,'CuI',10),(3,'Cu(OTf)2',5),(4,'Cu(OTf)2',10),
    (5,'CuBr',5),(6,'CuBr',10),(7,'CuCl',5),(8,'CuCl',10),
    (9,'Cu(OAc)2',5),(10,'Cu(OAc)2',10),(11,'Cu2O',5),(12,'Cu2O',10),
]

ROW_DESC = [
    'K₂CO₃ / Dioxane  ★ best from screen 1',
    'K₂CO₃ / DMF',
    'Cs₂CO₃ / Dioxane  ◆ new base',
    'Cs₂CO₃ / DMF  ◆ new base',
    'K₃PO₄ / Dioxane  (control)',
    'K₃PO₄ / DMF  (⚠ F9 anomaly re-run)',
    'K₂CO₃ / DMSO  ◆ new solvent',
    'K₂CO₃ / MeCN  ◆ new solvent',
]
COL_DESC = ['CuI\n5%','CuI\n10%','Cu(OTf)₂\n5%','Cu(OTf)₂\n10%',
            'CuBr\n5%','CuBr\n10%','CuCl\n5%','CuCl\n10%',
            'Cu(OAc)₂\n5%','Cu(OAc)₂\n10%','Cu₂O\n5%','Cu₂O\n10%']

n_rows, n_cols = 8, 12
well_r = 0.40
xs = np.arange(1, n_cols+1, dtype=float)
ys = np.arange(n_rows, 0, -1, dtype=float)

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(22, 13), facecolor='white')
gs  = gridspec.GridSpec(1, 1, left=0.26, right=0.97, top=0.91, bottom=0.10)
ax  = fig.add_subplot(gs[0, 0])
ax.set_facecolor('#f8f9fa')

# Plate body
ax.add_patch(mpatches.FancyBboxPatch(
    (0.15, 0.12), n_cols+0.7, n_rows+0.85,
    boxstyle='round,pad=0.12', lw=1.5,
    edgecolor='#9ca3af', facecolor='#f1f5f9', zorder=0))

for ri, (row_lbl, base, solvent) in enumerate(ROWS_DESIGN):
    for ci, (col_num, cu, loading) in enumerate(COLS_DESIGN):
        color = CU_COLORS[cu]
        alpha = 1.0 if loading == 5 else 0.60

        ax.add_patch(mpatches.Circle(
            (xs[ci], ys[ri]), well_r,
            facecolor=color, alpha=alpha,
            edgecolor='#d1d5db', lw=0.6, zorder=2))

        # Gold dashed ring on screen-1 control wells
        if base == 'K2CO3' and solvent == 'Dioxane' and cu in ('CuI','Cu(OTf)2'):
            ax.add_patch(mpatches.Circle(
                (xs[ci], ys[ri]), well_r+0.07,
                facecolor='none', edgecolor='#b45309',
                lw=2.0, zorder=4, linestyle='--'))

        # Loading label
        ax.text(xs[ci], ys[ri], f'{loading}%',
                ha='center', va='center', fontsize=6.5,
                color='white', fontweight='bold', zorder=3)

# Row labels
ROW_LABELS = list('ABCDEFGH')
for ri, (rl, desc) in enumerate(zip(ROW_LABELS, ROW_DESC)):
    ax.text(0.40, ys[ri]+0.12, rl,
            ha='right', va='center', fontsize=11,
            fontweight='bold', color='#111827')
    ax.text(0.38, ys[ri]-0.18, desc,
            ha='right', va='top', fontsize=7, color='#6b7280')

# Col labels
for ci, cdesc in enumerate(COL_DESC):
    ax.text(xs[ci], n_rows+0.92, cdesc,
            ha='center', va='bottom', fontsize=7,
            fontweight='bold', color='#111827', linespacing=1.3)

ax.set_xlim(-0.1, n_cols+0.9)
ax.set_ylim(-0.15, n_rows+1.7)
ax.set_aspect('equal')
ax.axis('off')

fig.suptitle('Proposed Screen 2 — DMCyDA Optimization Plate  '
             '(96 wells: 6 Cu sources × 2 loadings × 4 bases × 4 solvents)',
             fontsize=12, fontweight='bold', color='#111827', y=0.97)

# Legend
legend_patches = []
for cu, col in CU_COLORS.items():
    tag = '  ★ known' if cu in ('CuI','Cu(OTf)2') else '  ◆ new'
    legend_patches.append(mpatches.Patch(facecolor=col, edgecolor='#9ca3af',
                                          label=f'{cu}{tag}'))
legend_patches.append(mpatches.Patch(facecolor='none', edgecolor='#b45309',
                                      linestyle='--',
                                      label='Dashed ring = screen 1 control wells'))
ax.legend(handles=legend_patches, loc='lower center',
          bbox_to_anchor=(0.5, -0.06), ncol=4,
          fontsize=8, facecolor='white', edgecolor='#9ca3af',
          labelcolor='#111827', framealpha=1.0)

# Rationale panel
rationale = [
    'SCREEN 2 RATIONALE',
    '',
    'FIXED: DMCyDA (sole active ligand)',
    '',
    'NEW vs screen 1:',
    '  Bases:   + Cs₂CO₃ (rows C, D)',
    '           K₃PO₄ retained as control',
    '  Solvents: + DMSO (row G)',
    '             + MeCN (row H)',
    '  Cu:  + CuBr, CuCl (Cu(I) halides)',
    '       + Cu(OAc)₂  (Cu(II))',
    '       + Cu₂O  (air-stable Cu(I))',
    '  Loading: 5 mol%  vs  10 mol%',
    '',
    'QUESTIONS ANSWERED:',
    '  1. Cs₂CO₃ > K₂CO₃?',
    '  2. Best Cu source family',
    '     (Cu(I) vs Cu(II))?',
    '  3. Optimal loading?',
    '  4. DMSO / MeCN viable?',
    '  5. F9 anomaly confirmed',
    '     (row F re-run)',
    '',
    'CONTROLS:',
    '  Dashed-ring wells = direct',
    '  repeats of screen 1',
    '  best conditions',
]
fig.text(0.01, 0.92, '\n'.join(rationale),
         va='top', ha='left', fontsize=7.8,
         color='#374151', family='monospace',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#f9fafb',
                   edgecolor='#9ca3af', lw=0.8))

base_path = '/home/ubuntu/rayca-sessions/a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/screen2_plate_white'

fig.savefig(base_path + '.png', dpi=150, bbox_inches='tight', facecolor='white')
fig.savefig(base_path + '.jpg', dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig)
print("Saved PNG →", base_path + '.png')
print("Saved JPG →", base_path + '.jpg')
