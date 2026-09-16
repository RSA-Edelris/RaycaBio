
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.patches as mpatches
import pathlib

fig, ax = plt.subplots(figsize=(22, 10))
ax.set_aspect('equal')
ax.set_xlim(-2.2, 14.5)
ax.set_ylim(-1.8, 10.2)
ax.axis('off')

SOLVENT_BG = ["#FFF4E6", "#EBF9F1"]   # dioxane=warm, t-AmylOH=cool-green
BASE_ROW_ALPHA = ["#FDE8C8","#D6EAF8","#D5F5E3","#FCE4EC"]  # K2CO3/Cs2CO3/K3PO4/DIPEA

# ── Solvent row-block backgrounds (rows 0-3 and 4-7) ────────────────────────
for sol_idx in range(2):
    y_top = 7.0 - sol_idx*4 + 0.5
    y_bot = 7.0 - sol_idx*4 - 3.5
    ax.add_patch(FancyBboxPatch((-0.5, y_bot), 12.0, 4.0,
                 boxstyle="round,pad=0.15", lw=1.5,
                 edgecolor='#BBBBBB', facecolor=SOLVENT_BG[sol_idx], zorder=0))
    ax.text(-0.9, (y_top + y_bot)/2,
            SOLVENTS[sol_idx], rotation=90,
            ha='center', va='center', fontsize=10, fontweight='bold',
            color='#444')

# ── Base row colour bands ────────────────────────────────────────────────────
for ri in range(8):
    base_idx = ri % 4
    ax.add_patch(FancyBboxPatch((-0.45, 7.0 - ri - 0.42), 11.9, 0.84,
                 boxstyle="round,pad=0.0", lw=0,
                 facecolor=BASE_ROW_ALPHA[base_idx], alpha=0.35, zorder=0))

# ── Column headers (catalyst names) ─────────────────────────────────────────
for ci, (name, short, color, cas, tag) in enumerate(CATALYSTS):
    # Background chip
    chip_color = color + "33"  # transparent
    ax.add_patch(FancyBboxPatch((ci-0.42, 7.62), 0.84, 1.45,
                 boxstyle="round,pad=0.05", lw=1.2,
                 edgecolor=color, facecolor='white', zorder=1))
    # Tag badge
    badge_col = {"R1":"#457B9D","NEW":"#2A9D8F","NHC":"#E63946"}[tag]
    ax.add_patch(FancyBboxPatch((ci-0.38, 8.82), 0.76, 0.22,
                 boxstyle="round,pad=0.02", lw=0, facecolor=badge_col, zorder=2))
    ax.text(ci, 8.93, tag, ha='center', va='center',
            fontsize=5.5, color='white', fontweight='bold', zorder=3)
    # Short label
    ax.text(ci, 8.55, short, ha='center', va='center',
            fontsize=7, color=color, fontweight='bold', zorder=3)
    # Col number
    ax.text(ci, 7.55, str(ci+1), ha='center', va='center',
            fontsize=7.5, color='#666', zorder=3)

# ── Row labels (base + solvent) ──────────────────────────────────────────────
for ri in range(8):
    base_idx = ri % 4
    sol_idx  = ri // 4
    y = 7.0 - ri
    row_ltr = ROWS[ri]
    ax.text(-1.55, y, row_ltr, ha='center', va='center',
            fontsize=11, fontweight='bold', color='#333')
    ax.text(-0.85, y, BASES[base_idx], ha='center', va='center',
            fontsize=7.5, color='#333',
            bbox=dict(boxstyle="round,pad=0.15", fc=BASE_ROW_ALPHA[base_idx],
                      ec='#BBBBBB', lw=0.6))

# ── Wells ────────────────────────────────────────────────────────────────────
R = 0.39
DARK_BG = {"#D62828","#264653","#8338EC","#9B5DE5"}
for ri in range(8):
    for ci in range(12):
        x, y   = float(ci), 7.0 - float(ri)
        color  = CATALYSTS[ci][2]
        short  = CATALYSTS[ci][1]
        tag    = CATALYSTS[ci][4]
        tc     = 'white' if color in DARK_BG else '#1a1a1a'
        # Well circle
        ax.add_patch(Circle((x,y), R, color=color, zorder=2, linewidth=0))
        # NHC: gold ring; dppf: double ring; others: white
        if tag == 'NHC':
            ax.add_patch(Circle((x,y), R, fill=False, lw=2.2,
                         edgecolor='#FFD700', zorder=3))
        elif CATALYSTS[ci][0].startswith('dppf'):
            ax.add_patch(Circle((x,y), R, fill=False, lw=1.8,
                         edgecolor='white', linestyle='--', zorder=3))
        else:
            ax.add_patch(Circle((x,y), R, fill=False, lw=0.8,
                         edgecolor='white', zorder=3))
        ax.text(x, y, short, ha='center', va='center',
                fontsize=5.5, color=tc, fontweight='bold', zorder=4)

# ── Titles ──────────────────────────────────────────────────────────────────
ax.text(5.5, 9.85,
        "HTE Plate — Buchwald-Hartwig C–N Coupling  |  Round 2  |  96-well  |  4×2×12 full factorial",
        ha='center', va='center', fontsize=13.5, fontweight='bold', color='#1a1a2e')
ax.text(5.5, 9.50,
        "ArBr: 5-bromoisoindolinone-glutarimide  +  Amine: N-Boc piperazine  |  "
        "5 mol% Pd  |  1.5 eq amine  |  0.1 M  |  80 °C  |  18 h  |  No dedicated controls (reference Round 1 plate)",
        ha='center', va='center', fontsize=8, color='#666', style='italic')

# ── Legend ──────────────────────────────────────────────────────────────────
lx, ly = 12.9, 9.1
ax.text(lx, ly, "Tag", fontsize=8.5, fontweight='bold', color='#222')
for tag, col, desc in [
    ("R1",  "#457B9D", "Carried from Round 1"),
    ("NEW", "#2A9D8F", "New phosphine G3"),
    ("NHC", "#E63946", "NHC (non-phosphine)  ★"),
]:
    ly -= 0.52
    ax.add_patch(FancyBboxPatch((lx-0.1, ly-0.18), 0.38, 0.36,
                 boxstyle="round,pad=0.02", facecolor=col, lw=0, zorder=5))
    ax.text(lx+0.05, ly, tag, ha='center', va='center',
            fontsize=6.5, color='white', fontweight='bold', zorder=6)
    ax.text(lx+0.45, ly, desc, va='center', fontsize=7.5, color='#222')

ly -= 0.7
ax.text(lx, ly, "Border", fontsize=8.5, fontweight='bold', color='#222')
ly -= 0.52
ax.add_patch(Circle((lx+0.15, ly), 0.18, color='#E76F51', zorder=5))
ax.add_patch(Circle((lx+0.15, ly), 0.18, fill=False, lw=2, edgecolor='#FFD700', zorder=6))
ax.text(lx+0.45, ly, "Gold ring = NHC catalyst", va='center', fontsize=7.5)
ly -= 0.52
ax.add_patch(Circle((lx+0.15, ly), 0.18, color='#8338EC', zorder=5))
ax.add_patch(Circle((lx+0.15, ly), 0.18, fill=False, lw=1.5,
             edgecolor='white', linestyle='--', zorder=6))
ax.text(lx+0.45, ly, "Dashed = bidentate (dppf)", va='center', fontsize=7.5)

ly -= 0.7
ax.text(lx, ly, "Row key", fontsize=8.5, fontweight='bold', color='#222')
for bi, (base, bc) in enumerate(zip(BASES, BASE_ROW_ALPHA)):
    ly -= 0.50
    ax.add_patch(FancyBboxPatch((lx-0.1, ly-0.17), 0.38, 0.34,
                 boxstyle="round,pad=0.02", facecolor=bc, edgecolor='#BBBBBB', lw=0.6))
    ax.text(lx+0.45, ly, base, va='center', fontsize=7.5, color='#222')

ly -= 0.7
ax.text(lx, ly, "Solvent blocks", fontsize=8.5, fontweight='bold', color='#222')
for si, (sol, sc) in enumerate(zip(SOLVENTS, SOLVENT_BG)):
    ly -= 0.50
    ax.add_patch(FancyBboxPatch((lx-0.1, ly-0.17), 0.38, 0.34,
                 boxstyle="round,pad=0.02", facecolor=sc, edgecolor='#BBBBBB', lw=0.8))
    rows_label = "Rows A-D" if si==0 else "Rows E-H"
    ax.text(lx+0.45, ly, f"{sol}  ({rows_label})", va='center', fontsize=7.5, color='#222')

plt.tight_layout()
outpath = '/home/ubuntu/rayca-sessions/c6bff8e9-db20-41e3-b952-83c9e35071ad-9b531d029532/HTE_platemap_round2_4x2x12.png'
plt.savefig(outpath, dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved:", outpath)
