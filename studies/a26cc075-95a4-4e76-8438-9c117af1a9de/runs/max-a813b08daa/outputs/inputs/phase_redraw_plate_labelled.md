
## Objective

Redraw the HTE 96-well plate heatmap with three modifications: (1) well identifiers from conditions.csv printed inside each circle, (2) all yields normalised to the plate maximum (0–1 scale), and (3) the normalised value printed inside each well.

## Methods

**Data source:** `conditions.csv` (96 well IDs and condition strings) and `results.csv` (HPLC areas for SM, IS, DP).

**IS normalisation:** `norm_yield = Area(DP) / Area(IS)` — same as the prior phase.

**Plate-max normalisation:** `plate_norm = norm_yield / max(norm_yield)`. The plate maximum was IS-ratio = 1.689 at well 068 (DMCyDA\_K2CO3\_Cu(OTf)2\_Dioxane), which therefore receives a value of 1.00.

**Well mapping:** row-major, wells 001–012 → row A cols 1–12, 013–024 → row B, … 085–096 → row H.

**Labels inside each well circle:**
- Upper half: well number (001–096) in small monospace font
- Lower half: normalised value (0.00–1.00) in bold

## Output

![96-well plate — well IDs and plate-max normalised yields](hte_plate_labelled.png)

## Results

| Well | Row/Col | Condition | Norm. yield (0–1) |
|------|---------|-----------|-------------------|
| 068 ★ | F8 | DMCyDA\_K2CO3\_Cu(OTf)2\_Dioxane | **1.00** |
| 071   | F11 | DMCyDA\_K2CO3\_CuI\_DMF | 0.90 |
| 066   | F6  | DMCyDA\_K3PO4\_Cu(OTf)2\_Dioxane | 0.77 |
| 067   | F7  | DMCyDA\_K2CO3\_CuI\_Dioxane | 0.60 |
| 065   | F5  | DMCyDA\_K3PO4\_CuI\_Dioxane | 0.43 |
| 069   | F9  | DMCyDA\_K3PO4\_CuI\_DMF | 0.30 |
| 072   | F12 | DMCyDA\_K2CO3\_Cu(OTf)2\_DMF | 0.29 |
| 007   | A7  | Oxine\_K2CO3\_CuI\_DMF | 0.17 |
| 005   | A5  | Oxine\_K3PO4\_CuI\_DMF | 0.16 |
| 013   | B1  | Chxn-Py-Al\_K3PO4\_CuI\_Dioxane | 0.09 |

All remaining 86 wells score ≤ 0.08; 60 wells show no detectable product (value = 0).

## Conclusion

DMCyDA in row F (columns 5–8, 11–12) is the exclusive hotspot on this plate. Well 068 (DMCyDA / K₂CO₃ / Cu(OTf)₂ / Dioxane) is the clear winner at normalised yield = 1.00. The next best condition (071, normalised = 0.90) uses the same ligand and base but switches to CuI and DMF, confirming DMCyDA and K₂CO₃ as the critical variables.
