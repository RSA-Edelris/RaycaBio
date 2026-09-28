
## Task

Redraw `hte_viridis_v2.png` with a white background and save as both PNG and JPG for use in documents, slides, and publications.

## Outputs

| File | Format | DPI | Size |
|------|--------|-----|------|
| `hte_viridis_white.png` | PNG (lossless) | 150 | 590 KB |
| `hte_viridis_white.jpg` | JPEG | 150 | 420 KB |

## Figure

![HTE Screen 1 — viridis plate heatmap, white background](hte_viridis_white.png)

## Data pipeline (reproduced from source)

```
conditions_2.csv  →  merge on ID  →  df['ratio'] = Area_DP / Area_IS
results.csv       →                →  df['norm']  = ratio / ratio.max()
```

- 96 reactions: 12 ligands × 8 sub-conditions (2 bases × 2 Cu salts × 2 solvents)
- Normalization: DP/IS area ratio removes injection-volume variability; divide by plate maximum → 0–1 relative yield

## Key findings (unchanged from original)

| Rank | Well | Ligand | Base | Cu | Solvent | norm. yield |
|------|------|--------|------|----|---------|-------------|
| 1 | D9 | DMCyDA | K₂CO₃ | Cu(OTf)₂ | Dioxane | **1.000** |
| 2 | C9 | DMCyDA | K₂CO₃ | CuI | Dioxane | 0.684 |
| 3 | A9 | DMCyDA | K₃PO₄ | CuI | Dioxane | 0.577 |
| 4 | B9 | DMCyDA | K₃PO₄ | Cu(OTf)₂ | Dioxane | 0.823 |
| 5 | G9 | DMCyDA | K₂CO₃ | CuI | DMF | 0.570 |

**Ligand is the dominant variable** (Pearson r = +0.827, r² ≈ 0.68). Base, Cu source, and solvent each explain < 1 % of variance globally. Well F9 (DMCyDA/K₃PO₄/Cu(OTf)₂/DMF) = 0.000, flagged as a likely pipetting/injection anomaly.

## Style changes vs dark version

- Figure and axes backgrounds: white
- Text: #111827 (near-black) throughout
- Grid lines: #e5e7eb (light grey)
- Best-well annotation ring: #b45309 (amber, legible on white)
- Colormap: viridis (unchanged — perceptually uniform, sequential)
- Luminance threshold for per-well text: white overlay if lum < 0.45, dark if ≥ 0.45
