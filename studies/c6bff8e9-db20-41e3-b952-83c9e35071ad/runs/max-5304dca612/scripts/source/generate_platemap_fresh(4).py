"""
generate_platemap_fresh.py — self-contained plate map generator, fresh standalone design
Run: python generate_platemap_fresh.py
Output: HTE_platemap_fresh_4x2x12.png (same directory)

Design: 4 bases × 2 solvents × 12 Pd catalysts = 96 wells, fully saturated.
Rationale: first-principles selection, no prior HTE data assumed.
Non-phosphine: column 12 = PEPPSI [NHC-Pd], CAS 1158652-41-5.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import pathlib

# ── 12 Pd catalysts (columns 1-12) ────────────────────────────────────────────
# Covers: biaryl monophosphine (5), trialkyl/aliphatic (2), bidentate (3), NHC (1), 2°-amine-specialist (1)
CATALYSTS = [
    ("BrettPhos Pd G3",   "BPG3",   "#D62828", "1470372-59-8", "biaryl"),  # 1
    ("tBuBrettPhos Pd G3","tBBG3",  "#F77F00", "1536473-72-9", "biaryl"),  # 2
    ("RuPhos Pd G3",      "RuPG3",  "#FCBF49", "1445085-77-7", "biaryl"),  # 3
    ("XPhos Pd G3",       "XPG3",   "#2A9D8F", "1445085-55-1", "biaryl"),  # 4
    ("MorDalPhos Pd G3",  "MorG3",  "#264653", "2222690-89-1", "biaryl"),  # 5
    ("PCy3 Pd G3",        "PCy3",   "#9B5DE5", "1445086-12-3", "alkyl"),   # 6
    ("XantPhos Pd G3",    "XantG3", "#F15BB5", "1445085-97-1", "bident"),  # 7
    ("dppf Pd G3",        "dppf",   "#00B4D8", "1445086-28-1", "bident"),  # 8
    ("BINAP Pd G3",       "BINAP",  "#06D6A0", "2151915-22-7", "bident"),  # 9
    ("cataCXium-A Pd G3", "CatA",   "#FFB703", "1651823-59-4", "alkyl"),   # 10
    ("GPhos Pd G3",       "GPG3",   "#8338EC", "2489525-82-6", "biaryl"),  # 11
    ("PEPPSI [NHC-Pd]",   "PEPPSI", "#E76F51", "1158652-41-5", "NHC"),    # 12 ← non-phosphine ★
]

# ── 4 Bases (rows A/E=K₃PO₄, B/F=Cs₂CO₃, C/G=DBU, D/H=DIPEA) ───────────────
BASES    = ["K₃PO₄", "Cs₂CO₃", "DBU", "DIPEA"]
# ── 2 Solvents (rows A-D=Dioxane, rows E-H=DMF) ──────────────────────────────
SOLVENTS = ["Dioxane", "DMF"]
ROWS     = list("ABCDEFGH")

BASE_COLORS = ["#D5F5E3", "#D6EAF8", "#FDEBD0", "#FCE4EC"]
SOLVENT_BG  = ["#FFF4E6", "#EEF2FF"]
TAG_COLORS  = {"biaryl":"#457B9D", "alkyl":"#2A9D8F", "bident":"#E67E22", "NHC":"#E63946"}

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
ax.set_xlim(-2.2, 15.0)
ax.set_ylim(-1.8, 10.5)
ax.axis('off')

for sol_idx in range(2):
    y_top = 7.0 - sol_idx*4 + 0.55
    y_bot = 7.0 - sol_idx*4 - 3.55
    ax.add_patch(FancyBboxPatch((-0.5, y_bot), 12.0, 4.1,
                 boxstyle="round,pad=0.15", lw=1.5,
                 edgecolor='#BBBBBB', facecolor=SOLVENT_BG[sol_idx], zorder=0))
    ax.text(-0.85, (y_top+y_bot)/2, SOLVENTS[sol_idx], rotation=90,
            ha='center', va='center', fontsize=10, fontweight='bold', color='#444')

for ri in range(8):
    base_idx = ri % 4
    ax.add_patch(FancyBboxPatch((-0.45, 7.0-ri-0.43), 11.9, 0.86,
                 boxstyle="round,pad=0.0", lw=0,
                 facecolor=BASE_COLORS[base_idx], alpha=0.40, zorder=0))

for ci, (name, short, color, cas, tag) in enumerate(CATALYSTS):
    ax.add_patch(FancyBboxPatch((ci-0.42, 7.62), 0.84, 1.5,
                 boxstyle="round,pad=0.05", lw=1.2,
                 edgecolor=color, facecolor='white', zorder=1))
    badge_col = TAG_COLORS[tag]
    ax.add_patch(FancyBboxPatch((ci-0.38, 8.88), 0.76, 0.20,
                 boxstyle="round,pad=0.02", lw=0, facecolor=badge_col, zorder=2))
    tag_label = "NHC★" if tag=="NHC" else tag[:5]
    ax.text(ci, 8.98, tag_label, ha='center', va='center',
            fontsize=5.2, color='white', fontweight='bold', zorder=3)
    ax.text(ci, 8.55, short, ha='center', va='center',
            fontsize=6.5, color=color, fontweight='bold', zorder=3)
    ax.text(ci, 7.55, str(ci+1), ha='center', va='center',
            fontsize=7.5, color='#666', zorder=3)

for ri in range(8):
    base_idx = ri % 4
    y = 7.0 - ri
    ax.text(-1.55, y, ROWS[ri], ha='center', va='center',
            fontsize=11, fontweight='bold', color='#333')
    ax.text(-0.85, y, BASES[base_idx], ha='center', va='center',
            fontsize=7.2, color='#333',
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
            ax.add_patch(Circle((x,y), R, fill=False, lw=2.5,
                         edgecolor='#FFD700', zorder=3))
        elif tag == 'bident':
            ax.add_patch(Circle((x,y), R, fill=False, lw=1.8,
                         edgecolor='white', linestyle='--', zorder=3))
        elif tag == 'alkyl':
            ax.add_patch(Circle((x,y), R, fill=False, lw=1.8,
                         edgecolor='white', linestyle=':', zorder=3))
        else:
            ax.add_patch(Circle((x,y), R, fill=False, lw=0.8,
                         edgecolor='white', zorder=3))
        ax.text(x, y, short, ha='center', va='center',
                fontsize=5.5, color=tc, fontweight='bold', zorder=4)

ax.text(5.5, 10.1,
        "HTE Plate — Buchwald-Hartwig C–N Coupling  |  Fresh Standalone Design  |  96-well  |  4×2×12",
        ha='center', va='center', fontsize=13.5, fontweight='bold', color='#1a1a2e')
ax.text(5.5, 9.70,
        "ArBr: 5-bromoisoindolinone-glutarimide  +  Amine: N-Boc piperazine  |  "
        "5 mol% Pd  |  1.5 eq amine  |  0.1 M  |  80 °C  |  18 h  |  6-well control strip recommended",
        ha='center', va='center', fontsize=8, color='#666', style='italic')

lx, ly = 13.1, 9.5
ax.text(lx, ly, "Ligand class", fontsize=8.5, fontweight='bold', color='#222')
for tag_k, desc in [
    ("biaryl","Biaryl mono-phosphine G3"),
    ("alkyl", "Trialkyl / aliphatic mono-P G3"),
    ("bident","Bidentate bisphosphine G3"),
    ("NHC",  "NHC (non-phosphine) ★"),
]:
    ly -= 0.52
    ax.add_patch(FancyBboxPatch((lx-0.1, ly-0.18), 0.76, 0.36,
                 boxstyle="round,pad=0.02", facecolor=TAG_COLORS[tag_k], lw=0, zorder=5))
    ax.text(lx+0.42, ly, tag_k[:5], ha='left', va='center',
            fontsize=6.5, color='white', fontweight='bold', zorder=6)
    ax.text(lx+1.3, ly, desc, va='center', fontsize=7.2, color='#222')

ly -= 0.7
ax.text(lx, ly, "Border", fontsize=8.5, fontweight='bold', color='#222')
for ec, lw, ls, desc in [
    ('#FFD700',2.5,'-', 'Gold ring = NHC (non-phosphine)'),
    ('white',  1.8,'--','Dashed = bidentate bisphosphine'),
    ('white',  1.8,':', 'Dotted = trialkyl / aliphatic-P'),
]:
    ly -= 0.52
    ax.add_patch(Circle((lx+0.18, ly), 0.18, color='#888', zorder=5))
    ax.add_patch(Circle((lx+0.18, ly), 0.18, fill=False, lw=lw, edgecolor=ec, linestyle=ls, zorder=6))
    ax.text(lx+0.5, ly, desc, va='center', fontsize=7.2, color='#222')

ly -= 0.7
ax.text(lx, ly, "Base (row)", fontsize=8.5, fontweight='bold', color='#222')
for base, bc in zip(BASES, BASE_COLORS):
    ly -= 0.50
    ax.add_patch(FancyBboxPatch((lx-0.1, ly-0.17), 0.5, 0.34,
                 boxstyle="round,pad=0.02", facecolor=bc, edgecolor='#BBBBBB', lw=0.6))
    ax.text(lx+0.55, ly, base, va='center', fontsize=7.2, color='#222')

ly -= 0.7
ax.text(lx, ly, "Solvent (block)", fontsize=8.5, fontweight='bold', color='#222')
for sol, sc, rows_lbl in zip(SOLVENTS, SOLVENT_BG, ["Rows A-D","Rows E-H"]):
    ly -= 0.50
    ax.add_patch(FancyBboxPatch((lx-0.1, ly-0.17), 0.5, 0.34,
                 boxstyle="round,pad=0.02", facecolor=sc, edgecolor='#BBBBBB', lw=0.8))
    ax.text(lx+0.55, ly, f"{sol}  ({rows_lbl})", va='center', fontsize=7.2, color='#222')

plt.tight_layout()
out = pathlib.Path(__file__).parent / "HTE_platemap_fresh_4x2x12.png"
plt.savefig(out, dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {out}")
print(f"Wells: {total} = 4 bases × 2 solvents × 12 catalysts ✓")
