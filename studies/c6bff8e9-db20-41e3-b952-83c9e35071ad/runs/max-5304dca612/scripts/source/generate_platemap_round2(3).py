"""
generate_platemap_round2.py — self-contained plate map generator for HTE Round 2
Run: python generate_platemap_round2.py
Output: HTE_platemap_round2_4x2x12.png (same directory)

Fixes audit Finding (MAJOR): all variables now defined in this file.
007_plt_subplots.py + 006_plate_2_design_*.py merged here; original files
retained as historical artefacts but superseded.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import pathlib

# ── 12 Pd catalysts (columns 1-12) ────────────────────────────────────────────
CATALYSTS = [
    ("BrettPhos Pd G3",     "BPG3",   "#D62828", "1470372-59-8", "R1"),
    ("tBuBrettPhos Pd G3",  "tBBG3",  "#F77F00", "1536473-72-9", "R1"),
    ("RuPhos Pd G3",        "RuPG3",  "#FCBF49", "1445085-77-7", "R1"),
    ("tBuXPhos Pd G3",      "tBXG3",  "#2A9D8F", "1447963-75-8", "R1"),
    ("EPhos Pd G3",         "EPG3",   "#264653", "2940916-90-3", "R1"),
    ("SPhos Pd G3",         "SPG3",   "#9B5DE5", "1445085-82-4", "R1"),
    ("MorDalPhos Pd G3",    "MorG3",  "#00B4D8", "2222690-89-1", "NEW"),
    ("APhos Pd G3",         "APG3",   "#F15BB5", "1820817-64-8", "NEW"),
    ("GPhos Pd G3",         "GPG3",   "#06D6A0", "2489525-82-6", "NEW"),
    ("cataCXium-A Pd G3",   "CatG3",  "#FFB703", "1651823-59-4", "NEW"),
    ("dppf-Pd-G3",          "dppf",   "#8338EC", "1445086-28-1", "NEW"),
    ("PEPPSI [NHC-Pd]",     "PEPSI",  "#E76F51", "1158652-41-5", "NHC"),
]

# ── 4 Bases × 2 Solvents → 8 rows ────────────────────────────────────────────
BASES    = ["K₂CO₃", "Cs₂CO₃", "K₃PO₄", "DIPEA"]
SOLVENTS = ["Dioxane", "t-AmylOH"]
ROWS     = list("ABCDEFGH")
# Row A: Dioxane/K₂CO₃, B: Dioxane/Cs₂CO₃, C: Dioxane/K₃PO₄, D: Dioxane/DIPEA
# Row E: t-AmylOH/K₂CO₃, F: t-AmylOH/Cs₂CO₃, G: t-AmylOH/K₃PO₄, H: t-AmylOH/DIPEA

BASE_COLORS  = ["#FDE8C8", "#D6EAF8", "#D5F5E3", "#FCE4EC"]
SOLVENT_BG   = ["#FFF4E6", "#EBF9F1"]

# ── Build 8×12 grid ───────────────────────────────────────────────────────────
grid_color = [[None]*12 for _ in range(8)]
grid_label = [[None]*12 for _ in range(8)]

for ri in range(8):
    sol_idx  = ri // 4
    base_idx = ri  % 4
    for ci in range(12):
        grid_color[ri][ci] = CATALYSTS[ci][2]
        grid_label[ri][ci] = (CATALYSTS[ci][1], BASES[base_idx], SOLVENTS[sol_idx])

total = sum(1 for r in range(8) for c in range(12) if grid_color[r][c])
if len(CATALYSTS) != 12 or len(BASES) != 4 or len(SOLVENTS) != 2:
    raise ValueError(f"Design parameter error: {len(CATALYSTS)} catalysts, {len(BASES)} bases, {len(SOLVENTS)} solvents — expected 12×4×2")
if total != 96:
    raise ValueError(f"Well count error: {total} ≠ 96")

# ── Render ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(22, 10))
ax.set_aspect('equal')
ax.set_xlim(-2.2, 14.5)
ax.set_ylim(-1.8, 10.2)
ax.axis('off')

for sol_idx in range(2):
    y_top = 7.0 - sol_idx*4 + 0.5
    y_bot = 7.0 - sol_idx*4 - 3.5
    ax.add_patch(FancyBboxPatch((-0.5, y_bot), 12.0, 4.0,
                 boxstyle="round,pad=0.15", lw=1.5,
                 edgecolor='#BBBBBB', facecolor=SOLVENT_BG[sol_idx], zorder=0))
    ax.text(-0.9, (y_top+y_bot)/2, SOLVENTS[sol_idx], rotation=90,
            ha='center', va='center', fontsize=10, fontweight='bold', color='#444')

for ri in range(8):
    base_idx = ri % 4
    ax.add_patch(FancyBboxPatch((-0.45, 7.0-ri-0.42), 11.9, 0.84,
                 boxstyle="round,pad=0.0", lw=0,
                 facecolor=BASE_COLORS[base_idx], alpha=0.35, zorder=0))

for ci, (name, short, color, cas, tag) in enumerate(CATALYSTS):
    ax.add_patch(FancyBboxPatch((ci-0.42, 7.62), 0.84, 1.45,
                 boxstyle="round,pad=0.05", lw=1.2,
                 edgecolor=color, facecolor='white', zorder=1))
    badge_col = {"R1":"#457B9D", "NEW":"#2A9D8F", "NHC":"#E63946"}[tag]
    ax.add_patch(FancyBboxPatch((ci-0.38, 8.82), 0.76, 0.22,
                 boxstyle="round,pad=0.02", lw=0, facecolor=badge_col, zorder=2))
    ax.text(ci, 8.93, tag, ha='center', va='center',
            fontsize=5.5, color='white', fontweight='bold', zorder=3)
    ax.text(ci, 8.55, short, ha='center', va='center',
            fontsize=7, color=color, fontweight='bold', zorder=3)
    ax.text(ci, 7.55, str(ci+1), ha='center', va='center',
            fontsize=7.5, color='#666', zorder=3)

for ri in range(8):
    base_idx = ri % 4
    y = 7.0 - ri
    ax.text(-1.55, y, ROWS[ri], ha='center', va='center',
            fontsize=11, fontweight='bold', color='#333')
    ax.text(-0.85, y, BASES[base_idx], ha='center', va='center',
            fontsize=7.5, color='#333',
            bbox=dict(boxstyle="round,pad=0.15", fc=BASE_COLORS[base_idx],
                      ec='#BBBBBB', lw=0.6))

R = 0.39
DARK_BG = {"#D62828", "#264653", "#8338EC", "#9B5DE5", "#00B4D8"}
for ri in range(8):
    for ci in range(12):
        x, y  = float(ci), 7.0 - float(ri)
        color = CATALYSTS[ci][2]
        short = CATALYSTS[ci][1]
        tag   = CATALYSTS[ci][4]
        tc    = 'white' if color in DARK_BG else '#1a1a1a'
        ax.add_patch(Circle((x,y), R, color=color, zorder=2, linewidth=0))
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

ax.text(5.5, 9.85,
        "HTE Plate — Buchwald-Hartwig C–N Coupling  |  Round 2  |  96-well  |  4×2×12 full factorial",
        ha='center', va='center', fontsize=13.5, fontweight='bold', color='#1a1a2e')
ax.text(5.5, 9.50,
        "ArBr: 5-bromoisoindolinone-glutarimide  +  Amine: N-Boc piperazine  |  "
        "5 mol% Pd  |  1.5 eq amine  |  0.1 M  |  80 °C  |  18 h",
        ha='center', va='center', fontsize=8, color='#666', style='italic')

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
for bi, (base, bc) in enumerate(zip(BASES, BASE_COLORS)):
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
    rows_label = "Rows A-D" if si == 0 else "Rows E-H"
    ax.text(lx+0.45, ly, f"{sol}  ({rows_label})", va='center', fontsize=7.5, color='#222')

plt.tight_layout()
out = pathlib.Path(__file__).parent / "HTE_platemap_round2_4x2x12.png"
plt.savefig(out, dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {out}")
print(f"Wells: {total} unique = 4 bases × 2 solvents × 12 catalysts ✓")
