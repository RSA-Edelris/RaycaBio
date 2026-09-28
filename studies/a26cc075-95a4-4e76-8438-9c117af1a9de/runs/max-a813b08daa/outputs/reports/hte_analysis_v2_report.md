
## Overview

A 96-well copper-catalysed reaction screen (12 ligands × 2 bases × 2 Cu sources × 2 solvents) was re-analysed with explicit well positions from `conditions_2.csv`. The plate layout encodes **ligands in columns (1–12)** and **base/Cu/solvent sub-conditions in rows (A–H)**.

**Two-step normalisation:**
1. DP/IS area ratio (removes injection variability)
2. Divide by the maximum ratio across all 96 wells (0–1 relative scale; 1.0 = best condition)

## Figure

![96-well viridis heatmap, condition breakdowns, and correlation analysis](hte_viridis_v2.png)

*Top: 96-well plate in viridis colormap with per-well normalised values. Middle: Ligand × Solvent / Base / Cu heatmaps + variable correlation bar chart. Bottom: per-ligand mean and max.*

## Best conditions

| Rank | Well | Ligand | Base | Cu | Solvent | DP/IS | Norm. yield |
|------|------|--------|------|----|---------|-------|-------------|
| 1 | **D9** | **DMCyDA** | K₂CO₃ | Cu(OTf)₂ | Dioxane | 1.689 | **1.000** |
| 2 | G9 | DMCyDA | K₂CO₃ | CuI | DMF | 1.528 | 0.905 |
| 3 | B9 | DMCyDA | K₃PO₄ | Cu(OTf)₂ | Dioxane | 1.306 | 0.774 |
| 4 | C9 | DMCyDA | K₂CO₃ | CuI | Dioxane | 1.021 | 0.605 |
| 5 | A9 | DMCyDA | K₃PO₄ | CuI | Dioxane | 0.727 | 0.430 |

All top 7 hits are DMCyDA. The next-best non-DMCyDA condition is Oxine/K₂CO₃/CuI/DMF (G1, norm = 0.175), roughly 6× lower.

## Correlation analysis

| Variable | Encoding | Pearson r |
|----------|----------|-----------|
| **Ligand** | mean yield per ligand | **+0.827** |
| K₂CO₃ vs K₃PO₄ | binary | +0.074 |
| CuI vs Cu(OTf)₂ | binary | −0.070 |
| Dioxane vs DMF | binary | +0.048 |

**Ligand identity explains ≈ 68% of variance** (r² = 0.68). The three remaining variables (base, Cu source, solvent) each contribute < 1% of variance globally, because their signal is almost entirely confined to the DMCyDA column.

## Condition-level means

| Variable | Level | Mean norm. | Max norm. |
|----------|-------|-----------|----------|
| **Solvent** | Dioxane | 0.069 | 1.000 |
| | DMF | 0.052 | 0.905 |
| **Base** | K₂CO₃ | 0.073 | 1.000 |
| | K₃PO₄ | 0.047 | 0.774 |
| **Cu source** | CuI | 0.072 | 0.905 |
| | Cu(OTf)₂ | 0.048 | 1.000 |

## Correlations and interpretations

### 1. Ligand is the decisive variable
r = +0.83 confirms that which ligand is chosen almost entirely determines whether product forms. DMCyDA (mean norm = 0.537) outperforms the next-best ligand (Oxine, mean = 0.042) by **13×**. The other 10 ligands are essentially inactive. This suggests DMCyDA uniquely enables the Cu catalytic cycle, likely through its bidentate N,N-chelation mode.

### 2. Base: mild preference for K₂CO₃ (r = +0.074)
Globally weak, but within DMCyDA: K₂CO₃ gives a mean of 0.699 vs K₃PO₄ 0.375 (1.9× advantage). K₂CO₃ likely provides a more compatible basicity for the reaction mechanism.

### 3. Solvent: mild preference for Dioxane (r = +0.048)
Within DMCyDA: Dioxane mean = 0.702, DMF mean = 0.372. Dioxane is preferred, particularly when paired with Cu(OTf)₂ (best = 1.000 in Dioxane; 0.285 in DMF). DMF gives good results with CuI (0.905 in G9).

### 4. Cu source: no consistent preference (r = −0.070)
Cu(OTf)₂ has the highest individual hit but a lower overall mean than CuI (0.048 vs 0.072), because CuI performs more consistently across both solvents. One well stands out as anomalous: **F9 (DMCyDA/K₃PO₄/Cu(OTf)₂/DMF) = 0.000** — the only complete failure in the DMCyDA column, suggesting a possible injection error or an incompatibility specific to K₃PO₄ + Cu(OTf)₂ + DMF together.

### 5. No synergistic interaction between inactive ligands
None of the 11 other ligands showed conditional activity — no condition rescued them. This rules out a simple "wrong base" or "wrong solvent" explanation for their inactivity; the limitation is intrinsic to the ligand scaffold.

## Recommendation

**Primary:** DMCyDA / K₂CO₃ / Cu(OTf)₂ / Dioxane (well D9)

**Backup:** DMCyDA / K₂CO₃ / CuI / DMF (well G9, norm = 0.905) if Dioxane is inconvenient at scale.

**Follow-up priorities:**
1. Investigate the F9 zero-yield anomaly (repeated injection recommended)
2. DMCyDA concentration/loading screen under K₂CO₃/Dioxane with both Cu sources
3. Oxine with CuI in DMF as a distant second scaffold worth a brief optimisation pass (top non-DMCyDA hits G1, E1)
