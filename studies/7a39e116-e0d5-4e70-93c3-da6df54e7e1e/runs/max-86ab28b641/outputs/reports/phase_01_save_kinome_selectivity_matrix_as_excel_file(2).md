---
title: "Phase 1: Save kinome selectivity matrix as Excel file"
study_id: "7a39e116-e0d5-4e70-93c3-da6df54e7e1e"
run_id: "max-5ddba1ca76"
phase_index: 1
phase_id: "1"
phase_goal: "Save kinome selectivity matrix as Excel file"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Save Kinome Selectivity Matrix as Excel File

## Objective

Export the 43-kinase × 6-compound pIC50 pivot table (built in Phase 1 kinome profiling) to a formatted, heat-coloured Excel workbook for sharing and offline analysis.

---

## Inputs

| Item | Detail |
|:---|:---|
| Source | Five raw KinaseDocker2 CSVs (PDK1_AGC, probe5, batch2, batch3, batch4) |
| Aggregation | Max avg_score per compound–kinase pair (consistent with Phase 1 pivot) |
| Compounds | BX912, EL2003A, EL2003A-A2U1, EL2003A-A4U1, EL5001A, EL5003A |
| Kinases | 43 (AGC full family + targeted clinical panel) |

---

## Methods

The pivot was rebuilt from the raw CSVs using `pandas.groupby(['compound','Kinase'])['avg_score'].max().unstack('Kinase')`. The workbook was written with `openpyxl` and contains two sheets:

**Sheet 1 — Kinome Selectivity (primary view):**
- Rows = 43 kinases, sorted by mean pIC50 descending
- Columns = 6 compounds + Mean pIC50 summary column
- Cell colour: RdYlGn diverging scale (red = 6.3, yellow = midpoint, green = 7.5)
- Header and Mean column styled in dark navy; row 1 and column A frozen

**Sheet 2 — Raw (compounds × kinases):**
- Original orientation: compounds as rows, all 43 kinases as columns, alphabetically sorted
- Same heat-colour scale; header frozen

Score values are rounded to 2 decimal places. Missing cells (EL5001A / CDK6, no KLIFS structure in that batch) are left blank.

---

## Results

| Property | Value |
|:---|:---|
| Output file | `kinome_selectivity_matrix.xlsx` |
| File size | 11,066 bytes |
| Sheet 1 dimensions | 44 rows × 8 columns (43 kinases + header; 6 compounds + Mean) |
| Sheet 2 dimensions | 7 rows × 44 columns (6 compounds + header; 43 kinases) |
| Missing cells | 1 (EL5001A / CDK6) |
| Score range | 6.29 (BX912/CK1d) – 7.40 (BX912, EL2003A-A2U1, EL2003A-A4U1 / AurA) |

---

## Output Artifacts

| File | Format | Description |
|:---|:---|:---|
| `kinome_selectivity_matrix.xlsx` | XLSX | Heat-coloured two-sheet workbook |
| `144_pivot_t_copy.py` | PY | Initial pivot transpose attempt (namespace error) |
| `145_open.py` | PY | Pivot rebuild from raw CSVs |
| `146_copy.py` | PY | Final Excel generation script |

---

## Limitations

1. Scores are DNN pIC50 predictions with ±0.3 uncertainty; differences < 0.2 should not be over-interpreted.
2. One missing cell (EL5001A / CDK6) — CDK6 was not present in the EL5001A docking batch.
3. The colour scale (6.3–7.5) is fixed; cells outside this range are clipped to the boundary colour.

---

## Verification

| Check | Method | Result |
|:---|:---|:---|
| File written to disk | `os.path.getsize(kinome_selectivity_matrix.xlsx)` | 11,066 bytes ✓ |
| Pivot shape | `pivot.shape` | (6, 43) ✓ |
| All 6 compounds present | Column headers in Sheet 1 | BX912, EL2003A, EL2003A-A2U1, EL2003A-A4U1, EL5001A, EL5003A ✓ |
| 43 kinases as rows | Row count Sheet 1 (excl. header) | 43 ✓ |
| AurA top row | Highest mean pIC50 kinase | AurA (mean 7.28) sorted first ✓ |
| Missing cell EL5001A/CDK6 | `pivot.loc['EL5001A','CDK6']` is NaN | Blank cell in workbook ✓ |
