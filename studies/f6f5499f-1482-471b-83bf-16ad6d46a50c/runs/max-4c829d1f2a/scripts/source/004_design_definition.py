
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ── DESIGN DEFINITION ──────────────────────────────────────────────────────────
PHOTOCATALYSTS = {
    'A': dict(
        name='Ir[dF(CF₃)ppy]₂(dtbbpy)·PF₆',
        short='Ir-CF₃',
        e_star='+1.32 V',
        color='#2374AB',      # deep blue
        source='kit #31'
    ),
    'B': dict(
        name='4CzIPN',
        short='4CzIPN',
        e_star='+1.52 V',
        color='#2D9E2D',      # green
        source='kit #38'
    ),
    'C': dict(
        name='Mes-Acr⁺·BF₄',
        short='Acr⁺',
        e_star='+2.00 V',
        color='#C0392B',      # red
        source='kit #32'
    ),
    'D': dict(
        name='Ir[dF(4-tBupy)]₂(dtbbpy)',
        short='Ir-dF',
        e_star='+1.10 V',
        color='#7B2D8B',      # purple
        source='kit #12'
    ),
}

NI_LIGANDS = {
    (1,2): dict(name='dtbbpy',          short='dtbbpy', hatch='',   color_bg='#E8F4FD', source='kit #27'),
    (3,4): dict(name="4,4'-dMe-bpy",    short='dMe-bpy',hatch='//', color_bg='#E8F9EE', source='kit #1'),
    (5,6): dict(name='1,10-phen',       short='phen',   hatch='xx', color_bg='#FFF8E8', source='kit #46'),
}

BASES = {
    1: ('Cs₂CO₃', 'Cs', 'kit #52'),
    2: ('K₃PO₄',  'K₃P', 'kit #53'),
    3: ('Cs₂CO₃', 'Cs', 'kit #52'),
    4: ('K₃PO₄',  'K₃P', 'kit #53'),
    5: ('Cs₂CO₃', 'Cs', 'kit #52'),
    6: ('K₃PO₄',  'K₃P', 'kit #53'),
}

ROWS = ['A','B','C','D']
COLS = [1,2,3,4,5,6]

# ── FIGURE LAYOUT ──────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 10), facecolor='#F0F0F0')
ax = fig.add_axes([0.06, 0.13, 0.60, 0.78])
ax.set_facecolor('#D0D0D0')

well_r = 0.38          # well radius as fraction of cell
cell_w, cell_h = 1.0, 1.0

ax.set_xlim(0, 6.8)
ax.set_ylim(-0.3, 4.6)
ax.set_aspect('equal')
ax.axis('off')

# Plate border
plate_rect = FancyBboxPatch((0.15, -0.1), 6.3, 4.4,
    boxstyle="round,pad=0.15", linewidth=2.5, edgecolor='#555', facecolor='#E8E8E8', zorder=0)
ax.add_patch(plate_rect)

# Column headers
for ci, col in enumerate(COLS):
    # ligand group background
    if col in (1,2): bg, lig_short = '#D0E8FB', 'dtbbpy'
    elif col in (3,4): bg, lig_short = '#D0F0DA', "dMe-bpy"
    else: bg, lig_short = '#FFF0C8', 'phen'
    
    rect = plt.Rectangle((0.2 + ci*1.0, 4.0), 0.85, 0.45, 
                           facecolor=bg, edgecolor='#999', linewidth=1, zorder=1)
    ax.add_patch(rect)
    ax.text(0.625 + ci*1.0, 4.225, f'Col {col}', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#333')

# Ligand group labels above columns
for (c1,c2), lig in NI_LIGANDS.items():
    mid = 0.2 + (c1-1)*1.0 + 0.85*1.0
    ax.text(mid, 4.52, lig['name'], ha='center', va='center',
            fontsize=9, color='#222', style='italic',
            bbox=dict(facecolor=lig['color_bg'], edgecolor='#999', boxstyle='round,pad=0.2', linewidth=1))

# Row headers
for ri, row in enumerate(ROWS):
    pc = PHOTOCATALYSTS[row]
    y = 3.5 - ri * 1.0
    rect = plt.Rectangle((0.17, y-0.4), 0.30, 0.80,
                           facecolor=pc['color'], edgecolor='white', linewidth=1.5, zorder=1, alpha=0.9)
    ax.add_patch(rect)
    ax.text(0.32, y, row, ha='center', va='center', fontsize=14, fontweight='bold', color='white', zorder=2)

# Draw wells
for ri, row in enumerate(ROWS):
    pc = PHOTOCATALYSTS[row]
    for ci, col in enumerate(COLS):
        cx = 0.625 + ci * 1.0
        cy = 3.5 - ri * 1.0
        base_short = BASES[col][1]
        
        # Ligand hatch background
        if col in (1,2): hatch, lig_bg = '', '#EEF6FF'
        elif col in (3,4): hatch, lig_bg = '//', '#EEF9EE'
        else: hatch, lig_bg = 'xx', '#FFFAEE'
        
        # Outer circle (well border)
        circle_bg = plt.Circle((cx, cy), well_r + 0.05, color='white', linewidth=2, zorder=2)
        ax.add_patch(circle_bg)
        
        # Main well circle colored by PC
        well = plt.Circle((cx, cy), well_r, color=pc['color'], alpha=0.82, zorder=3)
        ax.add_patch(well)
        
        # Hatch overlay for ligand
        if hatch:
            well_hatch = plt.Circle((cx, cy), well_r, 
                                     facecolor='none', hatch=hatch,
                                     edgecolor='white', linewidth=0, alpha=0.4, zorder=4)
            ax.add_patch(well_hatch)
        
        # Well ID top
        ax.text(cx, cy + 0.17, f'{row}{col}', ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white', zorder=5)
        # PC short bottom
        ax.text(cx, cy - 0.03, pc['short'], ha='center', va='center',
                fontsize=6.5, color='white', zorder=5, alpha=0.95)
        # Base very bottom  
        ax.text(cx, cy - 0.21, base_short, ha='center', va='center',
                fontsize=7, color='#FFE', fontweight='bold', zorder=5)

ax.set_title('HTE Plate — Round 1  |  Ni/Photoredox Decarboxylative Arylation  |  470 nm  |  24 wells',
             fontsize=12, fontweight='bold', pad=10, color='#222')

# ── LEGEND (right panel) ───────────────────────────────────────────────────────
ax_leg = fig.add_axes([0.69, 0.05, 0.30, 0.90])
ax_leg.axis('off')

y = 0.98
ax_leg.text(0.0, y, 'LEGEND', fontsize=12, fontweight='bold', va='top', transform=ax_leg.transAxes)

y -= 0.06
ax_leg.text(0.0, y, '■ Photocatalyst (row)', fontsize=10, fontweight='bold', va='top',
            transform=ax_leg.transAxes, color='#333')
for row, pc in PHOTOCATALYSTS.items():
    y -= 0.055
    ax_leg.add_patch(plt.Rectangle((0.0, y-0.012), 0.05, 0.035,
                                    transform=ax_leg.transAxes,
                                    facecolor=pc['color'], edgecolor='white', linewidth=1))
    ax_leg.text(0.07, y, f"Row {row}: {pc['name']}\n         E* = {pc['e_star']}  ({pc['source']})",
                fontsize=8.2, va='center', transform=ax_leg.transAxes, color='#222')
    y -= 0.03

y -= 0.03
ax_leg.text(0.0, y, '▨ Ni-Ligand (column pair)', fontsize=10, fontweight='bold', va='top',
            transform=ax_leg.transAxes, color='#333')
lig_items = [
    ('Cols 1-2', 'dtbbpy', 'kit #27', '#2374AB', ''),
    ("Cols 3-4", "4,4'-dMe-bpy", 'kit #1',  '#2D9E2D', '///'),
    ('Cols 5-6', '1,10-phen',   'kit #46', '#C0392B', 'xxx'),
]
for cols_label, lname, src, lc, hatch in lig_items:
    y -= 0.055
    patch = plt.Rectangle((0.0, y-0.012), 0.05, 0.035, transform=ax_leg.transAxes,
                            facecolor='#DDD', edgecolor='#666', linewidth=1, hatch=hatch)
    ax_leg.add_patch(patch)
    ax_leg.text(0.07, y, f"{cols_label}: {lname}  ({src})",
                fontsize=8.5, va='center', transform=ax_leg.transAxes, color='#222')

y -= 0.05
ax_leg.text(0.0, y, '● Base (column, text in well)', fontsize=10, fontweight='bold', va='top',
            transform=ax_leg.transAxes, color='#333')
base_items = [
    ('Cols 1,3,5 — Cs₂CO₃ (Cs)', 'kit #52'),
    ('Cols 2,4,6 — K₃PO₄  (K₃P)', 'kit #53'),
]
for blabel, src in base_items:
    y -= 0.05
    ax_leg.text(0.04, y, f"• {blabel}  {src}",
                fontsize=8.5, va='center', transform=ax_leg.transAxes, color='#222')

y -= 0.07
ax_leg.text(0.0, y, 'FIXED CONDITIONS', fontsize=10, fontweight='bold', va='top',
            transform=ax_leg.transAxes, color='#333')
fixed = [
    'Ni source: NiBr₂·dme, 10 mol% (kit #21)',
    'Electrophile: N-Cbz-4-BrPip, 1.0 equiv',
    'Carboxylic acid: N-Boc-spiro-AA, 1.5 equiv',
    'Base stoich: 2.0 equiv',
    'Solvent: DMA, 0.1 M (kit #66)',
    'Light: 470 nm (fixed)',
    'Temperature: rt',
    'Time: 16 h, inert atmosphere',
    'Analysis: UPLC relative conversion',
]
for f in fixed:
    y -= 0.044
    ax_leg.text(0.02, y, f'• {f}', fontsize=7.8, va='center', transform=ax_leg.transAxes, color='#444')

y -= 0.06
ax_leg.text(0.0, y, 'DESIGN', fontsize=10, fontweight='bold', va='top',
            transform=ax_leg.transAxes, color='#333')
design_notes = [
    'Full factorial: 4 PC × 3 Lig × 2 Base = 24',
    'No replicates (Round 1 screen)',
    'Randomise dispensing order (see Table)',
    'Model: main effects + 2-way interactions',
    '3-way PC×Lig×Base (6 df) → error term',
]
for d in design_notes:
    y -= 0.044
    ax_leg.text(0.02, y, f'• {d}', fontsize=7.8, va='center', transform=ax_leg.transAxes, color='#444')

# Bottom note
fig.text(0.5, 0.01,
         'Reagent source: HTE_Edelris.sdf  |  Reaction: BrC1CCN(CC1)C(=O)OCc2ccccc2  +  CC(C)(C)OC(=O)N1CC2(CC2)CC1C(=O)O',
         ha='center', fontsize=7.5, color='#666')

plt.savefig('plate_map_round1.png', dpi=160, bbox_inches='tight', facecolor='#F0F0F0')
plt.close()
print("Plate map saved: plate_map_round1.png")
