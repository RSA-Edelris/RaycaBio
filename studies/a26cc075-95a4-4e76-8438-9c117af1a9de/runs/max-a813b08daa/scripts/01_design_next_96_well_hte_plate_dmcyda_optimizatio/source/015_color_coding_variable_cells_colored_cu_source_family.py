
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import numpy as np

# ── Color coding by variable ───────────────────────────────────────────────────
# Cells colored by Cu source family; loading shown as text; base/solvent on axes

CU_COLORS = {
    'CuI':       '#3b82f6',   # blue   — Cu(I) halide (known)
    'Cu(OTf)2':  '#f59e0b',   # amber  — Cu(II) triflate (known)
    'CuBr':      '#60a5fa',   # light blue — Cu(I) halide (new)
    'CuCl':      '#93c5fd',   # lighter blue — Cu(I) halide (new)
    'Cu(OAc)2':  '#f97316',   # orange — Cu(II) (new)
    'Cu2O':      '#a78bfa',   # violet — Cu(I) oxide (new)
}

ROW_LABELS = ['A','B','C','D','E','F','G','H']
ROW_DESC   = [
    'K₂CO₃ / Dioxane  ★ best from screen 1',
    'K₂CO₃ / DMF',
    'Cs₂CO₃ / Dioxane  ◆ new base',
    'Cs₂CO₃ / DMF  ◆ new base',
    'K₃PO₄ / Dioxane  (control)',
    'K₃PO₄ / DMF  (⚠ F9 anomaly re-run zone)',
    'K₂CO₃ / DMSO  ◆ new solvent',
    'K₂CO₃ / MeCN  ◆ new solvent',
]
COL_LABELS = [str(i) for i in range(1, 13)]
COL_DESC   = ['CuI\n5%','CuI\n10%',
               'Cu(OTf)₂\n5%','Cu(OTf)₂\n10%',
               'CuBr\n5%','CuBr\n10%',
               'CuCl\n5%','CuCl\n10%',
               'Cu(OAc)₂\n5%','Cu(OAc)₂\n10%',
               'Cu₂O\n5%','Cu₂O\n10%']

n_rows, n_cols = 8, 12
well_r = 0.40
xs = np.arange(1, n_cols+1, dtype=float)
ys = np.arange(n_rows, 0, -1, dtype=float)

fig = plt.figure(figsize=(22, 13), facecolor='#0d0d0d')
gs  = gridspec.GridSpec(1, 1, left=0.26, right=0.97, top=0.91, bottom=0.10)
ax  = fig.add_subplot(gs[0, 0])
ax.set_facecolor('#1a1a2e')

# Plate body
ax.add_patch(mpatches.FancyBboxPatch(
    (0.15, 0.12), n_cols+0.7, n_rows+0.85,
    boxstyle='round,pad=0.12', lw=1.5,
    edgecolor='#4a4a6a', facecolor='#16213e', zorder=0))

CU_ORDER = ['CuI','Cu(OTf)2','CuBr','CuCl','Cu(OAc)2','Cu2O']

for ri, (row_lbl, base, solvent) in enumerate(ROWS_DESIGN):
    for ci, (col_num, cu, loading) in enumerate(COLS_DESIGN):
        color = CU_COLORS[cu]
        # dim the 10 mol% wells slightly so 5% is brighter
        alpha = 1.0 if loading == 5 else 0.65

        ax.add_patch(mpatches.Circle(
            (xs[ci], ys[ri]), well_r,
            facecolor=color, alpha=alpha,
            edgecolor='#3a3a5c', lw=0.5, zorder=2))

        # Loading label inside well
        tc = 'white'
        ax.text(xs[ci], ys[ri], f'{loading}%',
                ha='center', va='center', fontsize=6.5,
                color=tc, fontweight='bold', zorder=3)

        # Mark the 4 control wells matching screen 1 best hits
        is_control = (base=='K2CO3' and solvent=='Dioxane' and cu in ('CuI','Cu(OTf)2'))
        if is_control:
            ax.add_patch(mpatches.Circle(
                (xs[ci], ys[ri]), well_r+0.07,
                facecolor='none', edgecolor='#fbbf24',
                lw=1.8, zorder=4, linestyle='--'))

# Row labels
for ri, (rl, desc) in enumerate(zip(ROW_LABELS, ROW_DESC)):
    ax.text(0.40, ys[ri]+0.12, rl,
            ha='right', va='center', fontsize=11,
            fontweight='bold', color='#f1f5f9')
    ax.text(0.38, ys[ri]-0.18, desc,
            ha='right', va='top', fontsize=7, color='#94a3b8')

# Col labels (Cu source + loading)
for ci, (cdesc, clbl) in enumerate(zip(COL_DESC, COL_LABELS)):
    ax.text(xs[ci], n_rows+0.92, cdesc,
            ha='center', va='bottom', fontsize=7,
            fontweight='bold', color='#e2e8f0',
            linespacing=1.3)

ax.set_xlim(-0.1, n_cols+0.9)
ax.set_ylim(-0.15, n_rows+1.7)
ax.set_aspect('equal')
ax.axis('off')

fig.suptitle('Proposed Screen 2 — DMCyDA Optimization Plate  '
             '(96 wells: 6 Cu sources × 2 loadings × 4 bases × 4 solvents)',
             fontsize=12, fontweight='bold', color='#f1f5f9', y=0.97)

# ── Legend ────────────────────────────────────────────────────────────────────
legend_patches = []
for cu, col in CU_COLORS.items():
    tag = '  ★ known' if cu in ('CuI','Cu(OTf)2') else '  ◆ new'
    legend_patches.append(mpatches.Patch(facecolor=col, edgecolor='#4a4a6a',
                                          label=f'{cu}{tag}'))
legend_patches.append(mpatches.Patch(facecolor='none', edgecolor='#fbbf24',
                                      linestyle='--', label='Dashed ring = screen 1 control wells'))
ax.legend(handles=legend_patches, loc='lower center',
          bbox_to_anchor=(0.5, -0.06), ncol=4,
          fontsize=8, facecolor='#16213e',
          edgecolor='#4a4a6a', labelcolor='#e2e8f0', framealpha=0.9)

# ── Rationale panel (left margin text) ───────────────────────────────────────
rationale = [
    'SCREEN 2 RATIONALE',
    '',
    'FIXED: DMCyDA (sole active ligand)',
    '',
    'NEW vs screen 1:',
    '  Bases:  + Cs₂CO₃ (rows C,D)',
    '          K₃PO₄ retained as control',
    '  Solvents: + DMSO (row G)',
    '             + MeCN (row H)',
    '  Cu:  + CuBr, CuCl (Cu(I) halides)',
    '       + Cu(OAc)₂ (Cu(II))',
    '       + Cu₂O (air-stable Cu(I))',
    '  Loading: 5 mol% vs 10 mol%',
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
         color='#cbd5e1', family='monospace',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#16213e',
                   edgecolor='#4a4a6a', lw=0.8))

out2 = '/home/ubuntu/rayca-sessions/a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/screen2_plate_design.png'
fig.savefig(out2, dpi=150, bbox_inches='tight', facecolor='#0d0d0d')
plt.close(fig)
print("Saved →", out2)
