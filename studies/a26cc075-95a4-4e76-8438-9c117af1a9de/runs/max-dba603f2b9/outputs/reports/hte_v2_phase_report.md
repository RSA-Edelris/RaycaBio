
## What was done

Re-analysed the 96-well copper-catalysed HTE screen using `conditions_2.csv` (explicit well positions) and `results.csv` (HPLC-UV areas). The new conditions file maps each reaction to a named well (A1–H12) with ligands in columns and base/Cu/solvent sub-conditions in rows — a cleaner layout than the previous row-major numbering.

**Normalisation applied (two steps):**
1. IS-normalisation: `ratio = Area(DP) / Area(IS)` — removes injection variability
2. Max-normalisation: `norm = ratio / max(ratio)` — scales the plate to 0–1 relative yield

## Figure produced

![96-well plate heatmap (viridis), condition heatmaps, and correlation chart](hte_viridis_v2.png)

Four panels:
- **Top:** 96-well plate with viridis colormap; per-well normalised value annotated in each circle; gold ring on the best well (D9)
- **Middle left × 3:** Ligand × Solvent, Ligand × Base, Ligand × Cu Source condition heatmaps (mean normalised yield)
- **Middle right:** Pearson correlation bar chart — each binary condition variable vs. normalised yield
- **Bottom:** Per-ligand mean and max normalised yield bar chart

## Key results

### Best conditions

| Rank | Well | Condition | Norm. yield |
|------|------|-----------|-------------|
| 1 | D9 | DMCyDA / K₂CO₃ / Cu(OTf)₂ / Dioxane | **1.000** |
| 2 | G9 | DMCyDA / K₂CO₃ / CuI / DMF | 0.905 |
| 3 | B9 | DMCyDA / K₃PO₄ / Cu(OTf)₂ / Dioxane | 0.774 |
| 4 | C9 | DMCyDA / K₂CO₃ / CuI / Dioxane | 0.605 |
| 5 | A9 | DMCyDA / K₃PO₄ / CuI / Dioxane | 0.430 |

All top 7 positions are DMCyDA. Best non-DMCyDA condition: Oxine/K₂CO₃/CuI/DMF (G1) at 0.175.

### Correlation analysis

| Variable | Pearson r | Variance explained |
|----------|-----------|-------------------|
| Ligand (mean score) | +0.827 | ~68% |
| K₂CO₃ vs K₃PO₄ | +0.074 | <1% |
| Cu(OTf)₂ vs CuI | −0.070 | <1% |
| Dioxane vs DMF | +0.048 | <1% |

Ligand identity is the gating variable. Base, Cu source and solvent show negligible global correlation; their effect is almost entirely contained within the DMCyDA column.

### Within DMCyDA

| Well | Base | Cu | Solvent | Norm. yield |
|------|------|----|---------|-------------|
| D9 | K₂CO₃ | Cu(OTf)₂ | Dioxane | 1.000 |
| G9 | K₂CO₃ | CuI | DMF | 0.905 |
| B9 | K₃PO₄ | Cu(OTf)₂ | Dioxane | 0.774 |
| C9 | K₂CO₃ | CuI | Dioxane | 0.605 |
| A9 | K₃PO₄ | CuI | Dioxane | 0.430 |
| E9 | K₃PO₄ | CuI | DMF | 0.297 |
| H9 | K₂CO₃ | Cu(OTf)₂ | DMF | 0.285 |
| F9 | K₃PO₄ | Cu(OTf)₂ | DMF | **0.000** ⚠ |

F9 is anomalous — the only zero in the DMCyDA column. Likely a pipetting or injection error; recommend re-injection.

## Interpretation

1. **Ligand dominates (r = +0.83).** DMCyDA uniquely enables the reaction; all other ligands are at least 13× lower in mean yield. No base/Cu/solvent combination rescues inactive ligands.
2. **Base: K₂CO₃ preferred** within DMCyDA (mean 0.70 vs 0.37 for K₃PO₄).
3. **Solvent: Dioxane generally better**, but DMF is viable with CuI (G9 = 0.905).
4. **Cu source: no consistent winner.** CuI has a higher global mean; Cu(OTf)₂ gives the single best hit. Both are viable.
5. **F9 anomaly** (DMCyDA/K₃PO₄/Cu(OTf)₂/DMF = 0) should be re-run before drawing conclusions about that specific combination.

## Recommendation

**Primary:** DMCyDA / K₂CO₃ / Cu(OTf)₂ / Dioxane (D9)

**Next steps:**
- Re-inject F9 to clarify the zero
- DMCyDA loading/stoichiometry optimisation under K₂CO₃/Dioxane
- Brief Oxine follow-up (CuI/DMF) as a secondary scaffold
