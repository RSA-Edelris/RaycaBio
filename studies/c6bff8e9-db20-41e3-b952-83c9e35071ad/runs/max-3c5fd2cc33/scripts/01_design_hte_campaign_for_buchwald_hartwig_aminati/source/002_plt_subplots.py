
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.patheffects as pe
import numpy as np

fig, ax = plt.subplots(figsize=(20, 11))
ax.set_aspect('equal')
ax.set_xlim(-1.5, 14.5)
ax.set_ylim(-1.5, 10.0)
ax.axis('off')

# ── Background solvent blocks ──────────────────────────────────────────────────
solvent_bg = [
    (0,  3,  "#FFF8F0", "Dioxane"),
    (3,  6,  "#F0F8FF", "DMA"),
    (6,  9,  "#F5FFF0", "Toluene"),
    (9,  12, "#FAFAFA", "Replicates & Controls"),
]
for c_start, c_end, bg, label in solvent_bg:
    rect = FancyBboxPatch((c_start - 0.45, -0.55), c_end - c_start - 0.1, 8.6,
                           boxstyle="round,pad=0.1", linewidth=1.5,
                           edgecolor='#CCCCCC', facecolor=bg, zorder=0)
    ax.add_patch(rect)
    ax.text(c_start + (c_end - c_start)/2 - 0.45, 8.35, label,
            ha='center', va='bottom', fontsize=11, fontweight='bold', color='#555555')

# ── Column headers (bases) ─────────────────────────────────────────────────────
base_labels = BASES * 3 + ["col10","col11","col12"]
for ci in range(12):
    if ci < 9:
        base_lbl = BASES[ci % 3]
        ax.text(ci, 8.0, base_lbl, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='#333')
    else:
        ax.text(ci, 8.0, f"col {ci+1}", ha='center', va='center',
                fontsize=8, color='#888')
    ax.text(ci, -0.95, str(ci+1), ha='center', va='center',
            fontsize=9, color='#666')

# ── Row labels ─────────────────────────────────────────────────────────────────
for ri, row in enumerate(ROWS):
    y = 7.0 - ri
    ax.text(-0.9, y, row, ha='center', va='center', fontsize=11,
            fontweight='bold', color='#333')

# ── Wells ─────────────────────────────────────────────────────────────────────
R = 0.40  # circle radius
for ri in range(8):
    for ci in range(12):
        y = 7.0 - ri
        x = ci
        color = grid_color[ri][ci]
        wtype = grid_type[ri][ci]
        lbl   = grid_label[ri][ci]

        if color is None:
            color = '#EEEEEE'

        # Draw well circle
        circle = Circle((x, y), R, color=color, zorder=2, linewidth=1.2,
                         edgecolor='white')
        ax.add_patch(circle)

        # Add thin border
        border_color = '#FFFFFF' if wtype == 'unique' else '#AAAAAA'
        border_lw = 0.8 if wtype == 'unique' else 1.5
        if wtype == 'control':
            border_color = '#333333'
            border_lw = 1.8
        elif wtype == 'replicate':
            # dashed border for replicates
            border_color = '#2980B9'
            border_lw = 1.8
        circ2 = Circle((x, y), R, fill=False, linewidth=border_lw,
                        edgecolor=border_color, zorder=3, linestyle='--' if wtype=='replicate' else '-')
        ax.add_patch(circ2)

        # Text inside well
        lines = lbl.strip().split('\n')
        # For unique wells: show catalyst abbreviation + base
        if wtype == 'unique' and lines:
            # short label
            cat_short = lines[0][:5] if lines else ""
            base_short = lines[1] if len(lines)>1 else ""
            # determine text color contrast
            tc = 'white' if color not in ["#FCBF49","#A8DADC","#CCCCCC","#AAAAAA"] else '#333'
            ax.text(x, y+0.08, cat_short, ha='center', va='center',
                    fontsize=5.2, color=tc, fontweight='bold', zorder=4)
        elif wtype == 'replicate':
            ax.text(x, y, lines[0], ha='center', va='center',
                    fontsize=6.5, color='#1A5276', fontweight='bold', zorder=4)
        elif wtype == 'control':
            tc = 'white' if color in ["#555555","#264653","#2E7D32","#888888"] else '#222'
            short = {"No cat.":"NoCat","No base":"NoBase","No amine":"NoAm","Blank":"BLNK",
                     "Pos.ctrl ①":"POS①","Pos.ctrl ②":"POS②"}
            key = lines[0]
            disp = short.get(key, key[:5])
            ax.text(x, y, disp, ha='center', va='center',
                    fontsize=6, color=tc, fontweight='bold', zorder=4)

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(5.5, 9.5,
        "HTE Plate — Buchwald-Hartwig C–N Coupling  |  Round 1  |  96-well",
        ha='center', va='center', fontsize=14, fontweight='bold', color='#1a1a2e')
ax.text(5.5, 9.1,
        "ArBr: 5-bromoisoindolinone-glutarimide  +  Amine: N-Boc piperazine  |  5 mol% Pd-G3  |  1.5 eq amine  |  0.1 M  |  80 °C  |  18 h",
        ha='center', va='center', fontsize=8.5, color='#444', style='italic')

# ── Legend ────────────────────────────────────────────────────────────────────
legend_x = 12.7
legend_y_start = 7.6
ax.text(legend_x + 0.3, legend_y_start + 0.3, "Catalyst", fontsize=9,
        fontweight='bold', color='#222')

cat_short_names = [
    "BrettPhos Pd G3",
    "RuPhos Pd G3",
    "XPhos Pd G3",
    "tBuXPhos Pd G3",
    "SPhos Pd G3",
    "DavePhos Pd G3",
    "EPhos Pd G3",
    "tBuBrettPhos Pd G3",
]
for i, (name, color) in enumerate(zip(cat_short_names, CATALYST_COLORS)):
    y_leg = legend_y_start - 0.5 - i * 0.52
    circ_leg = Circle((legend_x, y_leg), 0.2, color=color, zorder=5)
    ax.add_patch(circ_leg)
    ax.text(legend_x + 0.35, y_leg, name, va='center', fontsize=7.5, color='#222')

# Replicate legend entry
y_rep = legend_y_start - 0.5 - 8 * 0.52 - 0.3
circ_rep = Circle((legend_x, y_rep), 0.2, color=REPLICATE_COLOR,
                  linewidth=1.5, edgecolor='#2980B9', linestyle='--', zorder=5)
ax.add_patch(circ_rep)
circ_rep2 = Circle((legend_x, y_rep), 0.2, fill=False, linewidth=1.5,
                   edgecolor='#2980B9', linestyle='--', zorder=6)
ax.add_patch(circ_rep2)
ax.text(legend_x + 0.35, y_rep, "Replicate (BPG3, all cond.×2)", va='center', fontsize=7.5, color='#222')

ctrl_short = ["Neg. ctrl: no catalyst","Neg. ctrl: no base",
              "Neg. ctrl: no amine","Neg. ctrl: blank",
              "Pos. ctrl ① reference","Pos. ctrl ② duplicate"]
for i, (name, color) in enumerate(zip(ctrl_short, CONTROL_COLORS)):
    y_c = y_rep - 0.5 - i * 0.52
    circ_c = Circle((legend_x, y_c), 0.2, color=color, linewidth=1.5,
                    edgecolor='#333', zorder=5)
    ax.add_patch(circ_c)
    tc = 'white' if color in ["#555555","#2E7D32","#888888"] else '#222'
    ax.text(legend_x + 0.35, y_c, name, va='center', fontsize=7.5, color='#222')

# Column base-label bar
for ci in range(9):
    base_idx = ci % 3
    base_colors_bar = ["#FDE8C8","#D6EAF8","#D5F5E3"]
    rect = FancyBboxPatch((ci - 0.4, 7.55), 0.8, 0.3,
                           boxstyle="round,pad=0.05",
                           facecolor=base_colors_bar[base_idx], edgecolor='#CCC', lw=0.5, zorder=1)
    ax.add_patch(rect)

plt.tight_layout()
plt.savefig('/home/ubuntu/rayca-sessions/c6bff8e9-db20-41e3-b952-83c9e35071ad-9b531d029532/HTE_platemap_round1.png',
            dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("Plate map saved.")
