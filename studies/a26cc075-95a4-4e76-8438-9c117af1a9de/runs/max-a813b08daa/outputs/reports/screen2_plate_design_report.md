
## Rationale

Screen 1 established that **DMCyDA is the sole active ligand** (r = +0.83 with yield; 13× better mean than next-best Oxine). The three remaining variables — base, Cu source, solvent — showed weak global correlations (r < 0.08) but clear within-DMCyDA effects. Screen 2 fixes DMCyDA and fully optimizes the other three variables, adding catalyst loading as a fourth axis.

## Plate design

**Fixed:** DMCyDA ligand (all 96 wells)

**Plate layout:** `conditions_screen2.csv`

![Screen 2 proposed plate layout](screen2_plate_design.png)

### Rows A–H: Base × Solvent (8 combos)

| Row | Base | Solvent | Notes |
|-----|------|---------|-------|
| A | K₂CO₃ | Dioxane | ★ Best from screen 1 — internal control |
| B | K₂CO₃ | DMF | Screen 1 control |
| C | Cs₂CO₃ | Dioxane | **NEW** — stronger, more soluble carbonate |
| D | Cs₂CO₃ | DMF | **NEW** |
| E | K₃PO₄ | Dioxane | Screen 1 control |
| F | K₃PO₄ | DMF | ⚠ Re-run of F9 anomaly zone |
| G | K₂CO₃ | DMSO | **NEW** — excellent Cu solvation |
| H | K₂CO₃ | MeCN | **NEW** — polar aprotic contrast |

### Columns 1–12: Cu source × Loading (6 sources × 2 loadings)

| Cols | Cu source | Loadings | Status |
|------|-----------|----------|--------|
| 1–2 | CuI | 5, 10 mol% | ★ Known (screen 1) |
| 3–4 | Cu(OTf)₂ | 5, 10 mol% | ★ Known — best single hit |
| 5–6 | CuBr | 5, 10 mol% | **NEW** Cu(I) halide |
| 7–8 | CuCl | 5, 10 mol% | **NEW** Cu(I) halide |
| 9–10 | Cu(OAc)₂ | 5, 10 mol% | **NEW** Cu(II) source |
| 11–12 | Cu₂O | 5, 10 mol% | **NEW** air-stable Cu(I) oxide |

Dashed gold rings on wells A1–A4 mark direct repeats of screen 1's best conditions.

## Scientific questions answered

1. **Is Cs₂CO₃ better than K₂CO₃?** Rows C/D vs A/B — Cs₂CO₃ is more soluble and often superior in Cu-catalysed C–heteroatom couplings
2. **Best Cu source family (Cu(I) halide vs Cu(II))?** Cols 1–8 vs 9–12 across all base/solvent combinations
3. **Optimal loading: 5 vs 10 mol%?** Every odd/even column pair answers this directly
4. **Are DMSO and MeCN viable solvents?** Rows G/H vs A/B (same base K₂CO₃)
5. **F9 anomaly confirmed or artefact?** Row F re-runs the K₃PO₄/DMF combination across all 6 Cu sources

## Deliverable from screen 2

- Identity of the optimal Cu source and whether Cu(I) or Cu(II) is mechanistically preferred
- Optimal catalyst loading (5 vs 10 mol%)
- Whether Cs₂CO₃ offers a meaningful gain over K₂CO₃
- Solvent space expanded: DMSO/MeCN validated or ruled out
- Clarification of the F9 zero

## Suggested screen 3 (if needed)

Once screen 2 identifies the optimal Cu/base/solvent, screen 3 should vary **temperature** (e.g. 60, 80, 100, 120 °C) and **DMCyDA loading** (5, 10, 20 mol%) — a 4 × 4 factorial with replication = 96 wells at fixed best conditions.
