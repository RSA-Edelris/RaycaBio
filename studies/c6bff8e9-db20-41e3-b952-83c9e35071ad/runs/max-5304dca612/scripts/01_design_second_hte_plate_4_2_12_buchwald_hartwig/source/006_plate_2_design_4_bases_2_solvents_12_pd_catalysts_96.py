
# ── Plate 2 design: 4 bases × 2 solvents × 12 Pd catalysts = 96 wells ──────
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import pathlib

# ── 12 Pd catalysts (columns 1-12) ────────────────────────────────────────────
# 8 phosphine G3 (5 carried from Round 1, 3 new P-based) + 1 NHC (non-phos) +
# 1 bidentate bisphosphine + 1 adamantyl phosphine + 1 aminophos
CATALYSTS = [
    ("BrettPhos Pd G3",     "BPG3",   "#D62828", "1470372-59-8", "R1"),  # col 1
    ("tBuBrettPhos Pd G3",  "tBBG3",  "#F77F00", "1536473-72-9", "R1"),  # col 2
    ("RuPhos Pd G3",        "RuPG3",  "#FCBF49", "1445085-77-7", "R1"),  # col 3
    ("tBuXPhos Pd G3",      "tBXG3",  "#2A9D8F", "1447963-75-8", "R1"),  # col 4
    ("EPhos Pd G3",         "EPG3",   "#264653", "2940916-90-3", "R1"),  # col 5
    ("SPhos Pd G3",         "SPG3",   "#9B5DE5", "1445085-82-4", "R1"),  # col 6
    ("MorDalPhos Pd G3",    "MorG3",  "#00B4D8", "2222690-89-1", "NEW"), # col 7
    ("APhos Pd G3",         "APG3",   "#F15BB5", "1820817-64-8", "NEW"), # col 8
    ("GPhos Pd G3",         "GPG3",   "#06D6A0", "2489525-82-6", "NEW"), # col 9
    ("cataCXium-A Pd G3",   "CatG3",  "#FFB703", "1651823-59-4", "NEW"), # col10
    ("dppf-Pd-G3",          "dppf",   "#8338EC", "1445086-28-1", "NEW"), # col11
    ("PEPPSI [NHC-Pd]",     "PEPSI",  "#E76F51", "1158652-41-5", "NHC"), # col12 ← non-phos
]
# Non-phosphine marker: col 12 (PEPPSI) is an NHC-Pd; col 11 (dppf) is bidentate bisphosphine

# ── 4 Bases × 2 Solvents → 8 rows ────────────────────────────────────────────
BASES    = ["K₂CO₃",  "Cs₂CO₃", "K₃PO₄", "DIPEA"]
SOLVENTS = ["Dioxane", "t-AmylOH"]
ROWS     = list("ABCDEFGH")
# Row A: Dioxane/K₂CO₃, B: Dioxane/Cs₂CO₃, C: Dioxane/K₃PO₄, D: Dioxane/DIPEA
# Row E: t-AmylOH/K₂CO₃, F: t-AmylOH/Cs₂CO₃, G: t-AmylOH/K₃PO₄, H: t-AmylOH/DIPEA

BASE_COLORS = ["#FDE8C8","#D6EAF8","#D5F5E3","#FCE4EC"]  # per base level

# ── Build 8×12 grid ───────────────────────────────────────────────────────────
grid_color = [[None]*12 for _ in range(8)]
grid_label = [[""]*12   for _ in range(8)]

for ri in range(8):
    sol_idx  = ri // 4   # 0=Dioxane rows A-D, 1=t-AmylOH rows E-H
    base_idx = ri  % 4
    for ci in range(12):
        grid_color[ri][ci] = CATALYSTS[ci][2]
        grid_label[ri][ci] = (CATALYSTS[ci][1],
                              BASES[base_idx],
                              SOLVENTS[sol_idx])

total = sum(1 for r in range(8) for c in range(12) if grid_color[r][c])
assert total == 96
print(f"Total wells: {total}")
print(f"Breakdown: 12 catalysts × 4 bases × 2 solvents = {12*4*2}")
print(f"Controls: 0 (full factorial, references Round 1 controls)")
print("\n12 catalysts:")
for i,(name,short,col,cas,tag) in enumerate(CATALYSTS):
    ligand_type = "NHC (non-phosphine)" if tag=="NHC" else ("bidentate bisphosphine" if name.startswith("dppf") else "phosphine G3")
    print(f"  {i+1:2d}. [{tag}] {name} ({cas}) — {ligand_type}")
