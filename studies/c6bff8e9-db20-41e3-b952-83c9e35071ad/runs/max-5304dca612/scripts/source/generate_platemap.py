"""
generate_platemap.py — self-contained plate map generator for HTE Round 1
Run: python generate_platemap.py
Output: HTE_platemap_round1.png (same directory)

Fixes audit findings:
  - Finding 2: CONTROLS[3] (H10) corrected to "ArBr+amine/Diox" (was "Ar-Br only")
  - Finding 3: all definitions consolidated here; no cross-script namespace dependency
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import pathlib

# ── Design parameters ──────────────────────────────────────────────────────────
CATALYSTS = [
    "BrettPhos\nPd G3", "RuPhos\nPd G3", "XPhos\nPd G3", "tBuXPhos\nPd G3",
    "SPhos\nPd G3",     "DavePhos\nPd G3","EPhos\nPd G3", "tBuBrettPhos\nPd G3",
]
BASES    = ["Cs₂CO₃", "K₃PO₄", "NaOtBu"]
SOLVENTS = ["Dioxane", "DMA", "Toluene"]
ROWS     = list("ABCDEFGH")

CATALYST_COLORS = [
    "#D62828","#F77F00","#FCBF49","#2A9D8F",
    "#264653","#9B5DE5","#F15BB5","#00B4D8",
]
REPLICATE_COLOR = "#A8DADC"
CONTROL_COLORS  = ["#CCCCCC","#AAAAAA","#888888","#555555","#66BB6A","#2E7D32"]

# Well contents for control positions G10-G12, H10-H12
# H10 = "ArBr + amine + dioxane only" (no catalyst, no base) — blank stability control
CONTROLS = [
    "No cat.\nAr-Br+amine\n+K₃PO₄/Diox",   # G10
    "No base\nBPG3+Ar-Br\n+amine/Diox",      # G11
    "No amine\nBPG3+K₃PO₄\n/Diox",           # G12
    "Blank\nAr-Br+amine\n/Diox",             # H10  (ArBr + amine, no cat, no base)
    "Pos.ctrl ①\nBPG3+Cs₂CO₃\n/Diox",        # H11
    "Pos.ctrl ②\nBPG3+Cs₂CO₃\n/Diox dup",    # H12
]

REP_CONDITIONS = [
    ("BPG3","Cs₂CO₃","Dioxane"),("BPG3","K₃PO₄","Dioxane"),("BPG3","NaOtBu","Dioxane"),
    ("BPG3","Cs₂CO₃","DMA"),    ("BPG3","K₃PO₄","DMA"),    ("BPG3","NaOtBu","DMA"),
    ("BPG3","Cs₂CO₃","Toluene"),("BPG3","K₃PO₄","Toluene"),("BPG3","NaOtBu","Toluene"),
]

# ── Build well grid (8 rows × 12 cols) ────────────────────────────────────────
grid_color = [[None]*12 for _ in range(8)]
grid_label = [[""]*12   for _ in range(8)]
grid_type  = [[None]*12 for _ in range(8)]

# Unique conditions: plate cols 1-9 (ci 0-8)
# ci // 3 → solvent index (0=Dioxane,1=DMA,2=Toluene)
# ci  % 3 → base index   (0=Cs₂CO₃,1=K₃PO₄,2=NaOtBu)
for ri in range(8):
    for ci in range(9):
        grid_color[ri][ci] = CATALYST_COLORS[ri]
        grid_label[ri][ci] = f"{CATALYSTS[ri].split(chr(10))[0]}\n{BASES[ci % 3]}"
        grid_type[ri][ci]  = "unique"

# Replicates: plate cols 10-12 (ci 9-11), rows A-F (ri 0-5)
# rep_idx 0-8: ci = 9 + rep_idx//3; row_a = rep_idx%3; row_b = row_a+3
for rep_idx in range(9):
    ci    = 9 + rep_idx // 3
    row_a = rep_idx % 3
    row_b = row_a + 3
    rc    = REP_CONDITIONS[rep_idx]
    for ri in [row_a, row_b]:
        grid_color[ri][ci] = REPLICATE_COLOR
        grid_label[ri][ci] = f"REP{rep_idx+1}\n{rc[0]}\n{rc[1]}/{rc[2]}"
        grid_type[ri][ci]  = "replicate"

# Controls: plate cols 10-12 (ci 9-11), rows G-H (ri 6-7)
for ctrl_i, (ri, ci) in enumerate([(6,9),(6,10),(6,11),(7,9),(7,10),(7,11)]):
    grid_color[ri][ci] = CONTROL_COLORS[ctrl_i]
    grid_label[ri][ci] = CONTROLS[ctrl_i]
    grid_type[ri][ci]  = "control"

# Verify
unique = sum(1 for r in range(8) for c in range(12) if grid_type[r][c]=='unique')
reps   = sum(1 for r in range(8) for c in range(12) if grid_type[r][c]=='replicate')
ctrl   = sum(1 for r in range(8) for c in range(12) if grid_type[r][c]=='control')
assert unique + reps + ctrl == 96, f"Well count error: {unique}+{reps}+{ctrl}≠96"

# ── Render ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(20, 11))
ax.set_aspect('equal')
ax.set_xlim(-1.5, 14.5)
ax.set_ylim(-1.5, 10.0)
ax.axis('off')

for c_start, c_end, bg, label in [
    (0,3,"#FFF8F0","Dioxane"),(3,6,"#F0F8FF","DMA"),
    (6,9,"#F5FFF0","Toluene"),(9,12,"#FAFAFA","Replicates & Controls"),
]:
    ax.add_patch(FancyBboxPatch((c_start-0.45,-0.55),c_end-c_start-0.1,8.6,
                 boxstyle="round,pad=0.1",lw=1.5,edgecolor='#CCC',facecolor=bg,zorder=0))
    ax.text(c_start+(c_end-c_start)/2-0.45,8.35,label,
            ha='center',va='bottom',fontsize=11,fontweight='bold',color='#555')

base_bar_colors = ["#FDE8C8","#D6EAF8","#D5F5E3"]
for ci in range(12):
    if ci < 9:
        ax.add_patch(FancyBboxPatch((ci-0.4,7.55),0.8,0.3,
                     boxstyle="round,pad=0.05",facecolor=base_bar_colors[ci%3],
                     edgecolor='#CCC',lw=0.5,zorder=1))
        ax.text(ci,8.0,BASES[ci%3],ha='center',va='center',
                fontsize=8.5,fontweight='bold',color='#333')
    else:
        ax.text(ci,8.0,f"col {ci+1}",ha='center',va='center',fontsize=8,color='#888')
    ax.text(ci,-0.95,str(ci+1),ha='center',va='center',fontsize=9,color='#666')

for ri,row in enumerate(ROWS):
    ax.text(-0.9,7.0-ri,row,ha='center',va='center',
            fontsize=11,fontweight='bold',color='#333')

R = 0.40
dark_bg = {"#264653","#555555","#2E7D32","#888888","#D62828",
           "#F15BB5","#2A9D8F","#9B5DE5","#00B4D8"}
ctrl_short = {"No cat.":"NoCat","No base":"NoBase","No amine":"NoAm",
              "Blank":"BLNK","Pos.ctrl ①":"POS①","Pos.ctrl ②":"POS②"}
for ri in range(8):
    for ci in range(12):
        x,y   = float(ci), 7.0-float(ri)
        color = grid_color[ri][ci] or '#EEE'
        wtype = grid_type[ri][ci]
        lbl   = grid_label[ri][ci]
        ax.add_patch(Circle((x,y),R,color=color,zorder=2,linewidth=0))
        ec = {'unique':'#FFFFFF','replicate':'#2980B9','control':'#333333'}.get(wtype,'#CCC')
        ax.add_patch(Circle((x,y),R,fill=False,lw=1.5,
                     edgecolor=ec,linestyle='--' if wtype=='replicate' else '-',zorder=3))
        tc = 'white' if color in dark_bg else '#222'
        lines = lbl.strip().split('\n')
        if wtype == 'unique':
            ax.text(x,y,lines[0],ha='center',va='center',
                    fontsize=5.5,color=tc,fontweight='bold',zorder=4)
        elif wtype == 'replicate':
            ax.text(x,y,lines[0],ha='center',va='center',
                    fontsize=6.5,color='#1A5276',fontweight='bold',zorder=4)
        elif wtype == 'control':
            ax.text(x,y,ctrl_short.get(lines[0],lines[0][:5]),
                    ha='center',va='center',fontsize=6,color=tc,fontweight='bold',zorder=4)

ax.text(5.5,9.5,"HTE Plate — Buchwald-Hartwig C–N Coupling  |  Round 1  |  96-well",
        ha='center',va='center',fontsize=14,fontweight='bold',color='#1a1a2e')
ax.text(5.5,9.1,
        "ArBr: 5-bromoisoindolinone-glutarimide  +  Amine: N-Boc piperazine  |  "
        "5 mol% Pd-G3  |  1.5 eq amine  |  0.1 M  |  80 °C  |  18 h",
        ha='center',va='center',fontsize=8.5,color='#444',style='italic')

lx,ly = 12.7, 7.6
ax.text(lx+0.3,ly+0.3,"Catalyst",fontsize=9,fontweight='bold',color='#222')
cat_names = ["BrettPhos Pd G3","RuPhos Pd G3","XPhos Pd G3","tBuXPhos Pd G3",
             "SPhos Pd G3","DavePhos Pd G3","EPhos Pd G3","tBuBrettPhos Pd G3"]
for i,(name,col) in enumerate(zip(cat_names,CATALYST_COLORS)):
    yy = ly - 0.5 - i*0.52
    ax.add_patch(Circle((lx,yy),0.2,color=col,zorder=5))
    ax.text(lx+0.35,yy,name,va='center',fontsize=7.5,color='#222')
y_rep = ly - 0.5 - 8*0.52 - 0.3
ax.add_patch(Circle((lx,y_rep),0.2,color=REPLICATE_COLOR,zorder=5))
ax.add_patch(Circle((lx,y_rep),0.2,fill=False,lw=1.5,edgecolor='#2980B9',linestyle='--',zorder=6))
ax.text(lx+0.35,y_rep,"Replicate (BPG3, all 9 cond.×2)",va='center',fontsize=7.5)
ctrl_leg = ["Neg. ctrl: no catalyst","Neg. ctrl: no base","Neg. ctrl: no amine",
            "Blank: ArBr+amine/Diox","Pos. ctrl ① reference","Pos. ctrl ② duplicate"]
for i,(name,col) in enumerate(zip(ctrl_leg,CONTROL_COLORS)):
    yy = y_rep - 0.5 - i*0.52
    ax.add_patch(Circle((lx,yy),0.2,color=col,zorder=5))
    ax.add_patch(Circle((lx,yy),0.2,fill=False,lw=1.2,edgecolor='#333',zorder=6))
    ax.text(lx+0.35,yy,name,va='center',fontsize=7.5,color='#222')

plt.tight_layout()
out = pathlib.Path(__file__).parent / "HTE_platemap_round1.png"
plt.savefig(out, dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {out}")
print(f"Wells: {unique} unique + {reps} replicates + {ctrl} controls = 96 ✓")
