---
title: "Independent Audit: Save Kinome Selectivity Matrix as Excel File"
audited_phase: "Save kinome selectivity matrix as Excel file"
auditor: "independent"
date: "2026-09-08"
---

# Independent Audit: Kinome Selectivity Matrix Excel Export

## Scope

Verify that `kinome_selectivity_matrix.xlsx` correctly encodes the 43-kinase × 6-compound pIC50 values from the raw docking CSVs, that the file is readable, and that the spot-check values match recomputed figures.

---

## File Integrity

| Check | Result |
|:---|:---|
| File present at declared path | `kinome_selectivity_matrix.xlsx` — 11,066 bytes ✓ |
| Readable by openpyxl | ✓ |
| Two sheets present | "Kinome Selectivity" and "Raw (compounds × kinases)" ✓ |
| Sheet 1 dimensions | 44 rows × 8 columns (43 kinases + header; 6 compounds + Mean) ✓ |
| Sheet 2 dimensions | 7 rows × 44 columns ✓ |

---

## Spot-Check Values

Five cells independently recomputed from raw CSVs and cross-checked against the workbook:

| Kinase | Compound | Raw CSV max avg_score | Workbook value | Verdict |
|:---|:---|:---|:---|:---|
| AurA | BX912 | 7.403 | 7.40 | ✓ |
| PDK1 | EL2003A | 6.473 | 6.47 | ✓ |
| FGFR1 | EL2003A-A4U1 | 7.323 | 7.32 | ✓ |
| PKACa | EL5001A | 7.077 | 7.08 | ✓ |
| FLT3 | EL5003A | 7.213 | 7.21 | ✓ |

All five match (values rounded to 2 d.p. as declared). **VERIFIED CORRECT.**

---

## Sort Order

Sheet 1 claims kinases are sorted by mean pIC50 descending. Independently verified: AurA (mean 7.28) is row 2 (first data row), CK1d (mean 6.55) is last. Verified against `pivot.T[compound_order].mean(axis=1).sort_values(ascending=False)`. **VERIFIED CORRECT.**

---

## Missing Cell

EL5001A / CDK6: `pivot.loc['EL5001A','CDK6']` is NaN (CDK6 not in EL5001A batch). Sheet 1 cell is blank. **VERIFIED CORRECT.**

---

## Findings

No issues found.

| Severity | Count |
|:---|:---|
| CRITICAL | 0 |
| MAJOR | 0 |
| MINOR | 0 |

---

## Verification

| Step | Action | Result |
|:---|:---|:---|
| 1. File size | `os.path.getsize(...)` | 11,066 bytes ✓ |
| 2. Sheet names | `wb.sheetnames` | ["Kinome Selectivity", "Raw (compounds × kinases)"] ✓ |
| 3. AurA / BX912 cell | Sheet 1, row where Kinase="AurA", col BX912 | 7.40 ✓ |
| 4. PDK1 / EL2003A cell | Sheet 1, row Kinase="PDK1", col EL2003A | 6.47 ✓ |
| 5. FGFR1 / EL2003A-A4U1 | Sheet 1 | 7.32 ✓ |
| 6. AurA first data row | `ws_xl.cell(2,1).value` = "AurA" | ✓ |
| 7. EL5001A/CDK6 blank | Cell value is None | ✓ |
| 8. Raw sheet row count | 6 data rows + 1 header | ✓ |
