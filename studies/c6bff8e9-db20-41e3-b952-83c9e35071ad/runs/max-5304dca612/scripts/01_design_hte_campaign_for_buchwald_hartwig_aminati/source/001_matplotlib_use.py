
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

CATALYSTS = [
    "BrettPhos\nPd G3",
    "RuPhos\nPd G3",
    "XPhos\nPd G3",
    "tBuXPhos\nPd G3",
    "SPhos\nPd G3",
    "DavePhos\nPd G3",
    "EPhos\nPd G3",
    "tBuBrettPhos\nPd G3",
]
BASES    = ["Cs₂CO₃", "K₃PO₄", "NaOtBu"]
SOLVENTS = ["Dioxane", "DMA", "Toluene"]
ROWS = list("ABCDEFGH")
COLS = list(range(1, 13))

CATALYST_COLORS = [
    "#D62828",  # BrettPhos       - deep red
    "#F77F00",  # RuPhos          - orange
    "#FCBF49",  # XPhos           - amber
    "#2A9D8F",  # tBuXPhos        - teal
    "#264653",  # SPhos           - dark slate
    "#9B5DE5",  # DavePhos        - purple
    "#F15BB5",  # EPhos           - pink
    "#00B4D8",  # tBuBrettPhos    - cyan
]

REPLICATE_COLOR = "#A8DADC"
CONTROL_COLORS  = ["#CCCCCC","#AAAAAA","#888888","#555555","#66BB6A","#2E7D32"]

CONTROLS = [
    "No cat.\nAr-Br+amine\n+K₃PO₄/Diox",
    "No base\nBPG3+Ar-Br\n+amine/Diox",
    "No amine\nBPG3+K₃PO₄\n/Diox",
    "Blank\nAr-Br only\n/Diox",
    "Pos.ctrl ①\nBPG3+Cs₂CO₃\n/Diox",
    "Pos.ctrl ②\nBPG3+Cs₂CO₃\n/Diox dup",
]

REP_CONDITIONS = [
    ("BPG3", "Cs₂CO₃", "Dioxane"),
    ("BPG3", "K₃PO₄",  "Dioxane"),
    ("BPG3", "NaOtBu", "Dioxane"),
    ("BPG3", "Cs₂CO₃", "DMA"),
    ("BPG3", "K₃PO₄",  "DMA"),
    ("BPG3", "NaOtBu", "DMA"),
    ("BPG3", "Cs₂CO₃", "Toluene"),
    ("BPG3", "K₃PO₄",  "Toluene"),
    ("BPG3", "NaOtBu", "Toluene"),
]

# Build well grid: wells[row_idx][col_idx]
grid_color = [[None]*12 for _ in range(8)]
grid_label = [[""]*12 for _ in range(8)]
grid_type  = [[None]*12 for _ in range(8)]

# Unique conditions (cols 0-8 = col 1-9)
for ri in range(8):
    for ci in range(9):
        sol_idx  = ci // 3
        base_idx = ci  % 3
        grid_color[ri][ci] = CATALYST_COLORS[ri]
        grid_label[ri][ci] = f"{CATALYSTS[ri].split(chr(10))[0]}\n{BASES[base_idx]}"
        grid_type[ri][ci]  = "unique"

# Replicates (cols 9-11 = col 10-12, rows 0-5 = A-F)
for rep_idx in range(9):
    col_offset = rep_idx // 3
    in_col     = rep_idx  % 3
    ci = 9 + col_offset      # column index 9, 10, 11
    row_a = in_col           # row A, B, C
    row_b = in_col + 3       # row D, E, F
    rc = REP_CONDITIONS[rep_idx]
    short_lbl = f"REP{rep_idx+1}\n{rc[0]}\n{rc[1]}/{rc[2]}"
    for ri in [row_a, row_b]:
        grid_color[ri][ci] = REPLICATE_COLOR
        grid_label[ri][ci] = short_lbl
        grid_type[ri][ci]  = "replicate"

# Controls (cols 9-11, rows 6-7 = G-H)
ctrl_positions = [(6,9),(6,10),(6,11),(7,9),(7,10),(7,11)]
for ctrl_i, (ri, ci) in enumerate(ctrl_positions):
    grid_color[ri][ci] = CONTROL_COLORS[ctrl_i]
    grid_label[ri][ci] = CONTROLS[ctrl_i]
    grid_type[ri][ci]  = "control"

# Verify counts
total = sum(1 for r in range(8) for c in range(12) if grid_type[r][c] is not None)
print(f"Wells assigned: {total}")
unique = sum(1 for r in range(8) for c in range(12) if grid_type[r][c]=='unique')
reps   = sum(1 for r in range(8) for c in range(12) if grid_type[r][c]=='replicate')
ctrl   = sum(1 for r in range(8) for c in range(12) if grid_type[r][c]=='control')
print(f"  Unique: {unique}, Replicates: {reps}, Controls: {ctrl}")
assert total == 96
print("Grid OK")
