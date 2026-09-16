
# Self-contained corrected plate map — fixes both audit findings:
#   Finding 2: CONTROLS[3] corrected from "Ar-Br only" to "ArBr+amine/Diox"
#   Finding 3: all definitions in one file, no cross-script dependency

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import numpy as np

# ── Design parameters ─────────────────────────────────────────────────────────
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

# CONTROLS[3] corrected: "ArBr + amine\n/Diox" matches both markdown documents
CONTROLS = [
    "No cat.\nAr-Br+amine\n+K₃PO₄/Diox",   # G10
    "No base\nBPG3+Ar-Br\n+amine/Diox",      # G11
    "No amine\nBPG3+K₃PO₄\n/Diox",           # G12
    "Blank\nAr-Br+amine\n/Diox",             # H10  ← FIXED (was "Ar-Br only")
    "Pos.ctrl ①\nBPG3+Cs₂CO₃\n/Diox",        # H11
    "Pos.ctrl ②\nBPG3+Cs₂CO₃\n/Diox dup",    # H12
]

REP_CONDITIONS = [
    ("BPG3","Cs₂CO₃","Dioxane"),("BPG3","K₃PO₄","Dioxane"),("BPG3","NaOtBu","Dioxane"),
    ("BPG3","Cs₂CO₃","DMA"),    ("BPG3","K₃PO₄","DMA"),    ("BPG3","NaOtBu","DMA"),
    ("BPG3","Cs₂CO₃","Toluene"),("BPG3","K₃PO₄","Toluene"),("BPG3","NaOtBu","Toluene"),
]

# ── Build well grid ────────────────────────────────────────────────────────────
grid_color = [[None]*12 for _ in range(8)]
grid_label = [[""]*12   for _ in range(8)]
grid_type  = [[None]*12 for _ in range(8)]

# Unique conditions (cols 0-8 → plate cols 1-9)
for ri in range(8):
    for ci in range(9):
        grid_color[ri][ci] = CATALYST_COLORS[ri]
        grid_label[ri][ci] = f"{CATALYSTS[ri].split(chr(10))[0]}\n{BASES[ci % 3]}"
        grid_type[ri][ci]  = "unique"

# Replicates (cols 9-11 → plate cols 10-12, rows 0-5 → A-F)
for rep_idx in range(9):
    ci    = 9 + rep_idx // 3
    row_a = rep_idx % 3
    row_b = row_a + 3
    rc    = REP_CONDITIONS[rep_idx]
    for ri in [row_a, row_b]:
        grid_color[ri][ci] = REPLICATE_COLOR
        grid_label[ri][ci] = f"REP{rep_idx+1}\n{rc[0]}\n{rc[1]}/{rc[2]}"
        grid_type[ri][ci]  = "replicate"

# Controls (cols 9-11 → plate cols 10-12, rows 6-7 → G-H)
ctrl_positions = [(6,9),(6,10),(6,11),(7,9),(7,10),(7,11)]
for ctrl_i, (ri, ci) in enumerate(ctrl_positions):
    grid_color[ri][ci] = CONTROL_COLORS[ctrl_i]
    grid_label[ri][ci] = CONTROLS[ctrl_i]
    grid_type[ri][ci]  = "control"

# ── Verify counts ─────────────────────────────────────────────────────────────
unique = sum(1 for r in range(8) for c in range(12) if grid_type[r][c]=='unique')
reps   = sum(1 for r in range(8) for c in range(12) if grid_type[r][c]=='replicate')
ctrl   = sum(1 for r in range(8) for c in range(12) if grid_type[r][c]=='control')
total  = unique + reps + ctrl
assert total == 96, f"Expected 96, got {total}"
print(f"Wells: {unique} unique + {reps} replicates + {ctrl} controls = {total} ✓")
print(f"H10 label now: {repr(CONTROLS[3])}")
