
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import random

# ── DESIGN DEFINITION ──────────────────────────────────────────────────────────
PHOTOCATALYSTS2 = {
    'A': dict(name='fac-Ir(ppy)₃',                     short='Ir(ppy)₃',
              e_star='−1.51 V', color='#1A7A4A', source='kit #58'),
    'B': dict(name='4CzIPN',                             short='4CzIPN',
              e_star='−1.04 V', color='#1B7E8C', source='kit #38'),
    'C': dict(name='Ir(ppy)₂(dtbbpy)·PF₆',             short='Ir-ppy-dt',
              e_star='−0.96 V', color='#1F4E8C', source='kit #35'),
    'D': dict(name='Ir[dF(CF₃)ppy]₂(dtbbpy)·PF₆',     short='Ir-dFCF₃',
              e_star='−0.89 V', color='#6B2FA0', source='kit #31'),
}

SOLVENTS2 = {
    (1,2): dict(name='MeCN',    short='MeCN',   color_bg='#FFFDE7', source='kit #72'),
    (3,4): dict(name='DMSO',    short='DMSO',   color_bg='#FFF3E0', source='kit #24'),
    (5,6): dict(name='Dioxane', short='Diox',   color_bg='#EDE7F6', source='kit #70'),
}

ACIDS2 = {
    1: ('TFA 1 equiv', 'TFA', '⚠ purchased'),
    2: ('No acid',     '−H⁺', 'control'),
    3: ('TFA 1 equiv', 'TFA', '⚠ purchased'),
    4: ('No acid',     '−H⁺', 'control'),
    5: ('TFA 1 equiv', 'TFA', '⚠ purchased'),
    6: ('No acid',     '−H⁺', 'control'),
}

ROWS2 = ['A','B','C','D']
COLS2  = [1,2,3,4,5,6]

# ── FIGURE ─────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 10.5), facecolor='#F2F2F2')
ax  = fig.add_axes([0.04, 0.12, 0.60, 0.80])
ax.set_facecolor('#CCCCCC')
ax.set_xlim(0, 6.9); ax.set_ylim(-0.35, 4.7)
ax.set_aspect('equal'); ax.axis('off')

# Plate border
plate = FancyBboxPatch((0.14, -0.15), 6.42, 4.5,
    boxstyle="round,pad=0.15", linewidth=2.5,
    edgecolor='#444', facecolor='#EAEAEA', zorder=0)
ax.add_patch(plate)

# Solvent group labels (above plate)
for (c1, c2), sv in SOLVENTS2.items():
    mid_x = 0.2 + (c1-1)*1.0 + 0.9
    ax.text(mid_x, 4.55, sv['name'], ha='center', va='center',
            fontsize=9.5, style='italic', color='#222',
            bbox=dict(facecolor=sv['color_bg'], edgecolor='#AAA',
                      boxstyle='round,pad=0.25', linewidth=1))

# Column headers
hatch_map = {(1,2): '', (3,4): '//', (5,6): 'xx'}
for ci, col in enumerate(COLS2):
    if col in (1,2): bg = '#FFFDE7'
    elif col in (3,4): bg = '#FFF3E0'
    else: bg = '#EDE7F6'
    rect = plt.Rectangle((0.185 + ci*1.0, 4.02), 0.87, 0.43,
                           facecolor=bg, edgecolor='#999', linewidth=1, zorder=1)
    ax.add_patch(rect)
    acid_lbl = 'TFA' if col % 2 == 1 else '−H⁺'
    ax.text(0.625 + ci*1.0, 4.235, f'Col {col}',
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#333')

# Row headers (photocatalyst)
for ri, row in enumerate(ROWS2):
    pc = PHOTOCATALYSTS2[row]
    y  = 3.5 - ri*1.0
    rect = plt.Rectangle((0.15, y-0.41), 0.31, 0.82,
                           facecolor=pc['color'], edgecolor='white', linewidth=1.5, zorder=1)
    ax.add_patch(rect)
    ax.text(0.305, y, row, ha='center', va='center',
            fontsize=14, fontweight='bold', color='white', zorder=2)

# Draw wells
for ri, row in enumerate(ROWS2):
    pc = PHOTOCATALYSTS2[row]
    for ci, col in enumerate(COLS2):
        cx = 0.625 + ci*1.0
        cy = 3.5 - ri*1.0
        acid_short = ACIDS2[col][1]
        acid_warn  = col % 2 == 1  # TFA = purchased

        # Solvent background
        if col in (1,2): sv_bg = '#FFFDE7'
        elif col in (3,4): sv_bg = '#FFF3E0'
        else: sv_bg = '#EDE7F6'

        # Well shadow
        shadow = plt.Circle((cx+0.03, cy-0.03), 0.40, color='#888', alpha=0.3, zorder=2)
        ax.add_patch(shadow)
        # White ring
        ring = plt.Circle((cx, cy), 0.41, color='white', linewidth=0, zorder=3)
        ax.add_patch(ring)
        # Main well
        well = plt.Circle((cx, cy), 0.38, color=pc['color'], alpha=0.85, zorder=4)
        ax.add_patch(well)
        # Hatch for solvent
        if col in (3,4):
            hatch_c = plt.Circle((cx, cy), 0.38, facecolor='none',
                                  hatch='///', edgecolor='white', linewidth=0,
                                  alpha=0.35, zorder=5)
            ax.add_patch(hatch_c)
        elif col in (5,6):
            hatch_c = plt.Circle((cx, cy), 0.38, facecolor='none',
                                  hatch='xxx', edgecolor='white', linewidth=0,
                                  alpha=0.35, zorder=5)
            ax.add_patch(hatch_c)

        # Well ID
        ax.text(cx, cy+0.18, f'{row}{col}', ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white', zorder=6)
        # PC short label
        ax.text(cx, cy+0.01, pc['short'], ha='center', va='center',
                fontsize=6, color='white', zorder=6, alpha=0.95)
        # Acid label (bottom, highlighted if TFA)
        acid_col = '#FFD700' if acid_warn else '#CCE5FF'
        ax.text(cx, cy-0.19, acid_short, ha='center', va='center',
                fontsize=8, fontweight='bold', color=acid_col, zorder=6)

ax.set_title('HTE Plate — Round 1  |  Photocatalytic Minisci (NHP-ester)  |  470 nm  |  24 wells',
             fontsize=12, fontweight='bold', pad=10, color='#111')

# ── LEGEND ─────────────────────────────────────────────────────────────────────
ax2 = fig.add_axes([0.67, 0.04, 0.32, 0.92])
ax2.axis('off')

y = 0.98
ax2.text(0.0, y, 'LEGEND', fontsize=13, fontweight='bold', va='top',
         transform=ax2.transAxes)

y -= 0.06
ax2.text(0.0, y, '■ Photocatalyst (row) — E*(PC*/PC⁺)', fontsize=9.5,
         fontweight='bold', va='top', transform=ax2.transAxes, color='#222')
for row, pc in PHOTOCATALYSTS2.items():
    y -= 0.055
    ax2.add_patch(plt.Rectangle((0.0, y-0.013), 0.055, 0.038,
        transform=ax2.transAxes, facecolor=pc['color'], edgecolor='white', linewidth=1))
    ax2.text(0.075, y+0.006, f"Row {row}: {pc['name']}",
             fontsize=8.0, va='center', transform=ax2.transAxes, color='#111')
    ax2.text(0.075, y-0.013, f"         E* = {pc['e_star']}  ({pc['source']})",
             fontsize=7.5, va='center', transform=ax2.transAxes, color='#555')

y -= 0.045
ax2.text(0.0, y, '▨ Solvent (column pair)', fontsize=9.5, fontweight='bold',
         va='top', transform=ax2.transAxes, color='#222')
sv_items = [
    ('Cols 1–2', 'MeCN',    'kit #72', '#FFFDE7', ''),
    ('Cols 3–4', 'DMSO',    'kit #24', '#FFF3E0', '///'),
    ('Cols 5–6', 'Dioxane', 'kit #70', '#EDE7F6', 'xxx'),
]
for cols_lbl, sname, src, sbg, sh in sv_items:
    y -= 0.052
    ax2.add_patch(plt.Rectangle((0.0, y-0.012), 0.055, 0.035,
        transform=ax2.transAxes, facecolor=sbg, edgecolor='#888',
        linewidth=1, hatch=sh))
    ax2.text(0.075, y, f"{cols_lbl}: {sname}  ({src})",
             fontsize=8.5, va='center', transform=ax2.transAxes, color='#111')

y -= 0.045
ax2.text(0.0, y, '● Acid additive (column, text in well)', fontsize=9.5,
         fontweight='bold', va='top', transform=ax2.transAxes, color='#222')
acid_items = [
    ('Cols 1, 3, 5 — TFA  (gold text)',    '⚠ PURCHASED — not in kit'),
    ('Cols 2, 4, 6 — No acid  (blue text)','control condition'),
]
for albl, anote in acid_items:
    y -= 0.050
    ax2.text(0.04, y, f'• {albl}', fontsize=8.2, va='center',
             transform=ax2.transAxes, color='#111')
    y -= 0.030
    ax2.text(0.07, y, anote, fontsize=7.5, va='center',
             transform=ax2.transAxes, color='#888', style='italic')

y -= 0.05
ax2.text(0.0, y, '⚠ MISSING REAGENT — MUST PURCHASE',
         fontsize=9.5, fontweight='bold', va='top',
         transform=ax2.transAxes, color='#C0392B')
y -= 0.045
ax2.text(0.02, y,
         'TFA (trifluoroacetic acid, ≥99%)\n'
         'Use 1.0 equiv vs quinoline.\n'
         'No Brønsted acid found anywhere in kit.',
         fontsize=8.0, va='top', transform=ax2.transAxes, color='#C0392B')

y -= 0.085
ax2.text(0.0, y, 'FIXED CONDITIONS', fontsize=9.5, fontweight='bold',
         va='top', transform=ax2.transAxes, color='#222')
fixed2 = [
    'No Ni catalyst (Minisci = PC-only)',
    'Quinoline: Brc1cncc2ccccc12, 1.0 equiv',
    'NHP ester: 1.5 equiv',
    'PC loading: 2 mol%',
    'Concentration: 0.1 M, 100 µL',
    'Light: 470 nm (fixed)',
    'Temp: rt,  Time: 16 h,  N₂',
    'Analysis: UPLC relative conversion',
]
for f in fixed2:
    y -= 0.042
    ax2.text(0.02, y, f'• {f}', fontsize=7.8, va='center',
             transform=ax2.transAxes, color='#333')

y -= 0.05
ax2.text(0.0, y, 'DESIGN', fontsize=9.5, fontweight='bold',
         va='top', transform=ax2.transAxes, color='#222')
design2 = [
    'Full factorial: 4 PC × 3 Solvent × 2 Acid = 24',
    'All main effects + 2-way interactions estimable',
    '3-way PC×Solv×Acid (6 df) → error term',
    'No replicates (Round 1 screening)',
    'Randomise dispensing order',
]
for d in design2:
    y -= 0.042
    ax2.text(0.02, y, f'• {d}', fontsize=7.8, va='center',
             transform=ax2.transAxes, color='#333')

fig.text(0.5, 0.005,
    'Reagent source: HTE_Edelris_2.sdf  |  '
    'Brc1cncc2ccccc12 + NHP-ester  →  CC(C)(C)OC(=O)N1CCC(CC1)c2ncc(Br)c3ccccc23',
    ha='center', fontsize=7.5, color='#777')

plt.savefig('plate_map_minisci_round1.png', dpi=160, bbox_inches='tight',
            facecolor='#F2F2F2')
plt.close()
print("Saved: plate_map_minisci_round1.png")

# Randomised dispensing table
random.seed(7)
exps2 = []
for ri, row in enumerate(ROWS2):
    pc = PHOTOCATALYSTS2[row]
    for col in COLS2:
        sv = 'MeCN' if col in (1,2) else ('DMSO' if col in (3,4) else 'Dioxane')
        acid_lbl = 'TFA 1 equiv' if col % 2 == 1 else 'No acid'
        exps2.append({'Well': f'{row}{col}', 'PC': pc['name'], 'Solvent': sv,
                      'Acid': acid_lbl})
order = list(range(24)); random.shuffle(order)
print("\nRandomised dispensing order:")
print(f"{'Disp':<5} {'Well':<6} {'Photocatalyst':<42} {'Solvent':<10} Acid")
print("-"*90)
for rank, idx in enumerate(order):
    e = exps2[idx]
    print(f"{rank+1:<5} {e['Well']:<6} {e['PC']:<42} {e['Solvent']:<10} {e['Acid']}")
