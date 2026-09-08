
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import numpy as np

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# Pivot: kinases as rows, compounds as columns, sorted by mean pIC50
tbl = pivot.T.copy()
compound_order = ['BX912', 'EL2003A', 'EL2003A-A2U1', 'EL2003A-A4U1', 'EL5001A', 'EL5003A']
tbl = tbl[compound_order]
tbl['Mean'] = tbl.mean(axis=1)
tbl = tbl.sort_values('Mean', ascending=False)

wb = openpyxl.Workbook()
ws_xl = wb.active
ws_xl.title = "Kinome Selectivity"

# ── colour helpers ────────────────────────────────────────────────────────────
def score_fill(val):
    """Green → yellow → red scale between 6.3 and 7.5."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return PatternFill(fill_type=None)
    lo, hi = 6.3, 7.5
    t = max(0.0, min(1.0, (val - lo) / (hi - lo)))
    # low  = #d73027 (red), mid = #ffffbf (yellow), high = #1a9850 (green)
    if t < 0.5:
        s = t * 2
        r = int(215 + (255 - 215) * (1 - s))
        g = int(48  + (255 - 48)  * s)
        b = int(39  + (191 - 39)  * s)
    else:
        s = (t - 0.5) * 2
        r = int(255 + (26  - 255) * s)
        g = int(255 + (152 - 255) * s)
        b = int(191 + (80  - 191) * s)
    return PatternFill("solid", fgColor=f"{r:02X}{g:02X}{b:02X}")

header_fill  = PatternFill("solid", fgColor="1F3864")
mean_fill    = PatternFill("solid", fgColor="2E4057")
header_font  = Font(bold=True, color="FFFFFF", name="Calibri", size=10)
body_font    = Font(name="Calibri", size=10)
bold_font    = Font(bold=True, name="Calibri", size=10)
center       = Alignment(horizontal="center", vertical="center")
thin         = Side(style="thin", color="CCCCCC")
thin_border  = Border(left=thin, right=thin, top=thin, bottom=thin)

# ── header row ────────────────────────────────────────────────────────────────
headers = ["Kinase"] + compound_order + ["Mean pIC50"]
for col_i, h in enumerate(headers, start=1):
    cell = ws_xl.cell(row=1, column=col_i, value=h)
    cell.fill   = header_fill
    cell.font   = header_font
    cell.alignment = center
    cell.border = thin_border

# ── data rows ─────────────────────────────────────────────────────────────────
for row_i, (kinase, row) in enumerate(tbl.iterrows(), start=2):
    # Kinase name
    c = ws_xl.cell(row=row_i, column=1, value=kinase)
    c.font = bold_font; c.alignment = center; c.border = thin_border

    for col_i, col_name in enumerate(compound_order, start=2):
        val = row[col_name]
        display = round(float(val), 2) if not np.isnan(val) else None
        c = ws_xl.cell(row=row_i, column=col_i, value=display)
        c.fill      = score_fill(display)
        c.font      = body_font
        c.alignment = center
        c.border    = thin_border
        c.number_format = "0.00"

    # Mean column
    mean_val = round(float(row['Mean']), 2)
    c = ws_xl.cell(row=row_i, column=len(compound_order)+2, value=mean_val)
    c.fill   = mean_fill
    c.font   = Font(bold=True, color="FFFFFF", name="Calibri", size=10)
    c.alignment = center
    c.border    = thin_border
    c.number_format = "0.00"

# ── column widths ─────────────────────────────────────────────────────────────
ws_xl.column_dimensions['A'].width = 16
for col_i in range(2, len(headers) + 1):
    ws_xl.column_dimensions[get_column_letter(col_i)].width = 14

ws_xl.row_dimensions[1].height = 22
ws_xl.freeze_panes = "B2"

# ── second sheet: raw pivot (compounds as rows, kinases as columns) ───────────
ws2 = wb.create_sheet("Raw pivot (compounds × kinases)")
raw = pivot[sorted(pivot.columns)]
ws2.cell(row=1, column=1, value="Compound").font = header_font
ws2.cell(row=1, column=1).fill = header_fill
ws2.cell(row=1, column=1).alignment = center
for col_i, k in enumerate(raw.columns, start=2):
    c = ws2.cell(row=1, column=col_i, value=k)
    c.fill = header_fill; c.font = header_font; c.alignment = center
for row_i, (cmpd, row) in enumerate(raw.iterrows(), start=2):
    ws2.cell(row=row_i, column=1, value=cmpd).font = bold_font
    for col_i, val in enumerate(row, start=2):
        display = round(float(val), 2) if not np.isnan(val) else None
        c = ws2.cell(row=row_i, column=col_i, value=display)
        c.fill = score_fill(display); c.font = body_font
        c.alignment = center; c.number_format = "0.00"
ws2.column_dimensions['A'].width = 18
for col_i in range(2, len(raw.columns)+2):
    ws2.column_dimensions[get_column_letter(col_i)].width = 10
ws2.freeze_panes = "B2"

out = f"{WS}/kinome_selectivity_matrix.xlsx"
wb.save(out)
import os
print(f"Saved: {out}  ({os.path.getsize(out):,} bytes)")
