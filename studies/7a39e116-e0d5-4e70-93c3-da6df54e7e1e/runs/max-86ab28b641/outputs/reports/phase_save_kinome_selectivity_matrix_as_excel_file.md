## Objective

Export the 43-kinase × 6-compound pIC50 pivot table to a formatted, heat-coloured Excel workbook for sharing and offline analysis.

---

## Inputs

| Item | Detail |
|:---|:---|
| Source | Five raw KinaseDocker2 CSVs (PDK1_AGC, probe5, batch2, batch3, batch4) |
| Compounds | BX912, EL2003A, EL2003A-A2U1, EL2003A-A4U1, EL5001A, EL5003A |
| Kinases | 43 (AGC full family + targeted clinical panel) |
| Aggregation | Max avg_score per compound–kinase pair |

---

## Methods

Pivot rebuilt from raw CSVs via `pandas.groupby(['compound','Kinase'])['avg_score'].max().unstack('Kinase')`. Workbook written with `openpyxl`.

**Sheet 1 — Kinome Selectivity:** rows = 43 kinases sorted by mean pIC50 descending; columns = 6 compounds + Mean pIC50. RdYlGn cell fill (red = 6.3, green = 7.5). Row 1 and column A frozen.

**Sheet 2 — Raw (compounds × kinases):** original orientation, kinases alphabetical, same colour scale.

---

## Results

| Property | Value |
|:---|:---|
| Output file | `kinome_selectivity_matrix.xlsx` |
| File size | 11,066 bytes |
| Sheet 1 | 43 kinase rows × 8 columns (6 compounds + Mean) |
| Sheet 2 | 6 compound rows × 43 kinase columns |
| Score range | 6.29 – 7.40 pIC50 |
| Missing cells | 1 (EL5001A / CDK6 — no KLIFS structure in that batch) |

---

## Limitations

1. DNN scorer uncertainty ≈ ±0.3; differences < 0.2 should not be over-interpreted.
2. Colour scale clipped at 6.3–7.5; values outside this range show boundary colour.
3. One missing cell: EL5001A / CDK6.

---

## Output Artifacts

| File | Description |
|:---|:---|
| `kinome_selectivity_matrix.xlsx` | Heat-coloured two-sheet workbook |
| `145_open.py` | Pivot rebuild from raw CSVs |
| `146_copy.py` | Excel generation script |

---

## Verification

| Check | Method | Result |
|:---|:---|:---|
| File on disk | `os.path.getsize(kinome_selectivity_matrix.xlsx)` | 11,066 bytes ✓ |
| Pivot shape | `pivot.shape` | (6, 43) ✓ |
| AurA top row (highest mean) | `pivot.T.mean(axis=1).idxmax()` | AurA (7.28) ✓ |
| EL5001A/CDK6 blank | `pivot.loc['EL5001A','CDK6']` is NaN | blank cell ✓ |
| Spot check: AurA/BX912 | raw max = 7.403 → workbook 7.40 | ✓ |
| Spot check: PDK1/EL2003A | raw max = 6.473 → workbook 6.47 | ✓ |
| Independent audit | `reports/audit_save_kinome_selectivity_matrix_as_excel_file.md` | 0 critical, 0 major, 0 minor ✓ |
