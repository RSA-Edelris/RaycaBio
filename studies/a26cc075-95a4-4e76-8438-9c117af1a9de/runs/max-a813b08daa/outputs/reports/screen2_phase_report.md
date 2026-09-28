
## Purpose

Design a rational follow-up 96-well HTE plate based on the findings from screen 1. Screen 1 established DMCyDA as the only active ligand (r = +0.83 with yield, 13× above next-best Oxine). Screen 2 fixes DMCyDA and fully optimizes the remaining variables.

## Deliverables

- **`conditions_screen2.csv`** — 96-well conditions file ready for liquid-handler dispensing
- **`screen2_plate_design.png`** — annotated plate layout with color-coded Cu sources and loading labels

## Plate design

**Fixed throughout:** DMCyDA ligand

**Experimental design:** 6 Cu sources × 2 loadings × 4 bases × 4 solvents = 96 wells

![Proposed Screen 2 plate layout — DMCyDA optimization](screen2_plate_design.png)

### Row assignment (Base × Solvent)

| Row | Base | Solvent | Role |
|-----|------|---------|------|
| A | K₂CO₃ | Dioxane | ★ Screen 1 best — internal control |
| B | K₂CO₃ | DMF | Screen 1 control |
| C | Cs₂CO₃ | Dioxane | NEW base |
| D | Cs₂CO₃ | DMF | NEW base |
| E | K₃PO₄ | Dioxane | Screen 1 control |
| F | K₃PO₄ | DMF | ⚠ F9 anomaly re-run |
| G | K₂CO₃ | DMSO | NEW solvent |
| H | K₂CO₃ | MeCN | NEW solvent |

### Column assignment (Cu source × Loading)

| Cols | Cu source | Loadings | Status |
|------|-----------|----------|--------|
| 1–2 | CuI | 5, 10 mol% | Known |
| 3–4 | Cu(OTf)₂ | 5, 10 mol% | Known — best screen 1 hit |
| 5–6 | CuBr | 5, 10 mol% | NEW |
| 7–8 | CuCl | 5, 10 mol% | NEW |
| 9–10 | Cu(OAc)₂ | 5, 10 mol% | NEW Cu(II) |
| 11–12 | Cu₂O | 5, 10 mol% | NEW air-stable Cu(I) |

## Scientific questions addressed

1. **Cs₂CO₃ vs K₂CO₃** — rows C/D vs A/B
2. **Cu(I) vs Cu(II) family** — cols 1–8 vs 9–12
3. **Loading optimum** — every odd/even column pair
4. **DMSO and MeCN viability** — rows G/H vs A
5. **F9 anomaly** — row F provides full Cu source sweep under K₃PO₄/DMF

## Proposed screen 3 (contingent on screen 2)

Fix screen 2 winner. Vary temperature (4 levels: 60–120 °C) × DMCyDA loading (4 levels: 5–30 mol%) = 16 conditions × 6 replicates = 96 wells.
