
## What was done

The 96-well plate heatmap was redrawn with three changes requested:

1. **Well IDs from conditions.csv** (001–096) shown in the upper half of each circle.
2. **Plate-max normalisation**: every IS-normalised yield was divided by the plate maximum (IS-ratio = 1.689, well 068), giving a 0–1 scale where 1.00 = the best well on this plate.
3. **Normalised value printed** in the lower half of each circle (bold).

## Output

![96-well plate with well IDs and normalised yields](hte_plate_labelled.png)

## Key numbers

| Well | Condition | Norm. yield (0–1) |
|------|-----------|-------------------|
| 068 (F8) ★ | DMCyDA\_K2CO3\_Cu(OTf)2\_Dioxane | **1.00** |
| 071 (F11) | DMCyDA\_K2CO3\_CuI\_DMF | 0.90 |
| 066 (F6) | DMCyDA\_K3PO4\_Cu(OTf)2\_Dioxane | 0.77 |
| 067 (F7) | DMCyDA\_K2CO3\_CuI\_Dioxane | 0.60 |
| 065 (F5) | DMCyDA\_K3PO4\_CuI\_Dioxane | 0.43 |
| 069 (F9) | DMCyDA\_K3PO4\_CuI\_DMF | 0.30 |
| 072 (F12) | DMCyDA\_K2CO3\_Cu(OTf)2\_DMF | 0.29 |

All other wells score ≤ 0.17; the vast majority are 0.
