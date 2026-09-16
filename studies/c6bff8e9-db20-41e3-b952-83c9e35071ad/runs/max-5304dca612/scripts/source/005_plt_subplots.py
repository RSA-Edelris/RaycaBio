
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

fig, ax = plt.subplots(figsize=(20, 11))
ax.set_aspect('equal')
ax.set_xlim(-1.5, 14.5)
ax.set_ylim(-1.5, 10.0)
ax.axis('off')

# Solvent block backgrounds
for c_start, c_end, bg, label in [
    (0, 3, "#FFF8F0", "Dioxane"), (3, 6, "#F0F8FF", "DMA"),
    (6, 9, "#F5FFF0", "Toluene"), (9, 12, "#FAFAFA", "Replicates & Controls"),
]:
    ax.add_patch(FancyBboxPatch((c_start-0.45, -0.55), c_end-c_start-0.1, 8.6,
                 boxstyle="round,pad=0.1", lw=1.5, edgecolor='#CCC', facecolor=bg, zorder=0))
    ax.text(c_start+(c_end-c_start)/2-0.45, 8.35, label,
            ha='center', va='bottom', fontsize=11, fontweight='bold', color='#555')

# Column base-label bars and column numbers
for ci in range(12):
    if ci < 9:
        for bc, ba in zip(["#FDE8C8","#D6EAF8","#D5F5E3"], BASES):
            if ci % 3 == ["#FDE8C8","#D6EAF8","#D5F5E3"].index(bc):
                ax.add_patch(FancyBboxPatch((ci-0.4,7.55),0.8,0.3,
                             boxstyle="round,pad=0.05",facecolor=bc,edgecolor='#CCC',lw=0.5,zorder=1))
        ax.text(ci, 8.0, BASES[ci%3], ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='#333')
    else:
        ax.text(ci, 8.0, f"col {ci+1}", ha='center', va='center', fontsize=8, color='#888')
    ax.text(ci, -0.95, str(ci+1), ha='center', va='center', fontsize=9, color='#666')

# Row labels
for ri, row in enumerate(ROWS):
    ax.text(-0.9, 7.0-ri, row, ha='center', va='center',
            fontsize=11, fontweight='bold', color='#333')

# Wells
R = 0.40
for ri in range(8):
    for ci in range(12):
        x, y   = ci, 7.0 - ri
        color  = grid_color[ri][ci] or '#EEE'
        wtype  = grid_type[ri][ci]
        lbl    = grid_label[ri][ci]
        ax.add_patch(Circle((x,y), R, color=color, zorder=2, linewidth=0))
        ec = {'unique':'#FFFFFF','replicate':'#2980B9','control':'#333333'}.get(wtype,'#CCC')
        ls = '--' if wtype=='replicate' else '-'
        lw = 1.5
        ax.add_patch(Circle((x,y), R, fill=False, linewidth=lw, edgecolor=ec, linestyle=ls, zorder=3))
        lines = lbl.strip().split('\n')
        tc = 'white' if color in ["#264653","#555555","#2E7D32","#888888","#D62828",
                                   "#F15BB5","#2A9D8F","#9B5DE5","#00B4D8"] else '#222'
        if wtype == 'unique':
            ax.text(x, y, lines[0], ha='center', va='center',
                    fontsize=5.5, color=tc, fontweight='bold', zorder=4)
        elif wtype == 'replicate':
            ax.text(x, y, lines[0], ha='center', va='center',
                    fontsize=6.5, color='#1A5276', fontweight='bold', zorder=4)
        elif wtype == 'control':
            short = {"No cat.":"NoCat","No base":"NoBase","No amine":"NoAm",
                     "Blank":"BLNK","Pos.ctrl ①":"POS①","Pos.ctrl ②":"POS②"}
            ax.text(x, y, short.get(lines[0], lines[0][:5]), ha='center', va='center',
                    fontsize=6, color=tc, fontweight='bold', zorder=4)

# Title
ax.text(5.5, 9.5, "HTE Plate — Buchwald-Hartwig C–N Coupling  |  Round 1  |  96-well",
        ha='center', va='center', fontsize=14, fontweight='bold', color='#1a1a2e')
ax.text(5.5, 9.1,
        "ArBr: 5-bromoisoindolinone-glutarimide  +  Amine: N-Boc piperazine  |  "
        "5 mol% Pd-G3  |  1.5 eq amine  |  0.1 M  |  80 °C  |  18 h",
        ha='center', va='center', fontsize=8.5, color='#444', style='italic')

# Legend
lx, ly = 12.7, 7.6
ax.text(lx+0.3, ly+0.3, "Catalyst", fontsize=9, fontweight='bold', color='#222')
cat_names = ["BrettPhos Pd G3","RuPhos Pd G3","XPhos Pd G3","tBuXPhos Pd G3",
             "SPhos Pd G3","DavePhos Pd G3","EPhos Pd G3","tBuBrettPhos Pd G3"]
for i,(name,col) in enumerate(zip(cat_names, CATALYST_COLORS)):
    yy = ly - 0.5 - i*0.52
    ax.add_patch(Circle((lx,yy),0.2,color=col,zorder=5))
    ax.text(lx+0.35, yy, name, va='center', fontsize=7.5, color='#222')

y_rep = ly - 0.5 - 8*0.52 - 0.3
ax.add_patch(Circle((lx,y_rep),0.2,color=REPLICATE_COLOR,zorder=5))
ax.add_patch(Circle((lx,y_rep),0.2,fill=False,linewidth=1.5,edgecolor='#2980B9',linestyle='--',zorder=6))
ax.text(lx+0.35, y_rep, "Replicate (BPG3, all 9 cond.×2)", va='center', fontsize=7.5)

ctrl_leg = ["Neg. ctrl: no catalyst","Neg. ctrl: no base","Neg. ctrl: no amine",
            "Blank: ArBr+amine/Diox","Pos. ctrl ① reference","Pos. ctrl ② duplicate"]
for i,(name,col) in enumerate(zip(ctrl_leg, CONTROL_COLORS)):
    yy = y_rep - 0.5 - i*0.52
    ax.add_patch(Circle((lx,yy),0.2,color=col,linewidth=1.2,zorder=5))
    ax.add_patch(Circle((lx,yy),0.2,fill=False,linewidth=1.2,edgecolor='#333',zorder=6))
    tc = 'white' if col in ["#555555","#2E7D32","#888888"] else '#222'
    ax.text(lx+0.35, yy, name, va='center', fontsize=7.5, color='#222')

plt.tight_layout()
outpath = '/home/ubuntu/rayca-sessions/c6bff8e9-db20-41e3-b952-83c9e35071ad-9b531d029532/HTE_platemap_round1.png'
plt.savefig(outpath, dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("PNG saved:", outpath)
