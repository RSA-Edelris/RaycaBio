# HTE Campaign — Buchwald-Hartwig C–N Coupling: Design Results

**Date:** 2026-09-15  
**Status:** Design complete — plate ready for execution

---

## Reaction

| Role | SMILES | Identity |
|---|---|---|
| Aryl bromide | `Brc1ccc2C(=O)N(Cc2c1)C3CCC(=O)NC3=O` | 5-bromo-2-(2,6-dioxopiperidin-3-yl)isoindolin-1-one |
| Amine | `CC(C)(C)OC(=O)N1CCNCC1` | N-Boc piperazine |
| Product | C–N bond at Ar-5 position | 5-(4-Boc-piperazin-1-yl)-2-(2,6-dioxopiperidin-3-yl)isoindolin-1-one |

> **Structural alert:** The aryl bromide carries a free glutarimide NH (pKa ≈ 11–13 in DMSO). Strong bases (NaOtBu) will deprotonate it and can promote wrong-regioisomer N-arylation. Confirm product mass on all NaOtBu hits before advancing.

---

## Reagent Inventory (HTE_Edelris.sdf — 74 entries)

| Category | Count in kit | Used in Round 1 |
|---|---|---|
| Pd catalysts | 20 | 8 |
| Bases | 15 | 3 |
| Solvents | 9 | 3 |
| Photocatalysts (Ir, Ru, organic) | 14 | 0 |
| Ligands (bipyridyl, phenanthroline) | 11 | 0 |
| Nickel catalysts | 4 | 0 |
| Copper catalyst | 1 | 0 |

Photocatalysts, Ni catalysts, and N,N-bipyridyl/phenanthroline ligands serve Ni-photoredox dual-catalysis manifolds, not classical thermal Pd-BH. They are reserved for a separate exploratory plate if Pd fails entirely.

---

## Design

### Type
**Full 8 × 3 × 3 factorial** = 72 unique conditions.  
Rationale: zero prior conversion data for this substrate/amine pair. Full factorial resolves all main effects and interactions without aliasing; fits on one plate with room for controls and replicates.

### Factors varied

| Factor | Type | Levels |
|---|---|---|
| **Pd-G3 precatalyst** | Categorical | BrettPhos Pd G3, RuPhos Pd G3, XPhos Pd G3, tBuXPhos Pd G3, SPhos Pd G3, DavePhos Pd G3, EPhos Pd G3, tBuBrettPhos Pd G3 |
| **Base** | Categorical | Cs₂CO₃, K₃PO₄, NaOtBu |
| **Solvent** | Categorical | 1,4-Dioxane, DMA, Toluene |

### Factors held constant

| Factor | Value | Reason |
|---|---|---|
| Temperature | 80 °C | Standard BH for ArBr; Boc-safe; optimise in Round 2 |
| Pd loading | 5 mol% | Standard HTE; optimise in Round 2 |
| Amine : ArBr | 1.5 : 1 | Slight excess of the cheaper partner |
| [ArBr] | 0.1 M | Practical for 40 µL wells (~4 nmol) |
| Reaction time | 18 h | Overnight; eliminates kinetic between-well variability |

---

## Plate Map — Round 1

![HTE plate map Round 1](HTE_platemap_round1.png)

### Layout

| Columns | Solvent | Col 1/4/7 | Col 2/5/8 | Col 3/6/9 |
|---|---|---|---|---|
| 1–3 | 1,4-Dioxane | Cs₂CO₃ | K₃PO₄ | NaOtBu |
| 4–6 | DMA | Cs₂CO₃ | K₃PO₄ | NaOtBu |
| 7–9 | Toluene | Cs₂CO₃ | K₃PO₄ | NaOtBu |
| 10–12, rows A–F | Replicates | — | — | — |
| 10–12, rows G–H | Controls | — | — | — |

**Rows A–H (within cols 1–9):**

| Row | Catalyst |
|---|---|
| A | BrettPhos Pd G3 |
| B | RuPhos Pd G3 |
| C | XPhos Pd G3 |
| D | tBuXPhos Pd G3 |
| E | SPhos Pd G3 |
| F | DavePhos Pd G3 |
| G | EPhos Pd G3 |
| H | tBuBrettPhos Pd G3 |

### Well counts

| Type | Wells |
|---|---|
| Unique conditions | 72 |
| Replicates (BrettPhos G3 × all 9 base/solvent combinations, each ×2) | 18 |
| Controls | 6 |
| **Total** | **96** |

### Controls

| Well | Contents | Purpose |
|---|---|---|
| G10 | ArBr + amine + K₃PO₄ + dioxane, **no catalyst** | Confirms no uncatalysed reaction |
| G11 | ArBr + amine + BrettPhos G3 + dioxane, **no base** | Confirms base is required |
| G12 | ArBr + BrettPhos G3 + K₃PO₄ + dioxane, **no amine** | Monitors ArBr decomposition / homocoupling |
| H10 | ArBr + amine + dioxane only — **blank** | Background / ArBr thermal stability |
| H11 | BrettPhos G3 + Cs₂CO₃ + dioxane — **positive ctrl #1** | Plate QC anchor |
| H12 | BrettPhos G3 + Cs₂CO₃ + dioxane — **positive ctrl #2** | Intra-plate reproducibility |

### Randomisation
Row (catalyst) assignment within each 3-column solvent block is randomised before dispensing Pd stocks. Solvent and base column order is also randomised. Randomisation seed must be recorded in the ELN before plate preparation.

---

## Response and Measurement

| Parameter | Value |
|---|---|
| Response | % relative conversion of ArBr → monoarylated product |
| Method | Reverse-phase UPLC-MS, UV 254 nm, peak-area ratio vs. internal standard |
| Precision | ±3–5% absolute conversion (σ ≈ 2%) at 40 µL scale |
| Hit threshold | ≥ 20% conversion (10× precision floor) |
| Detection limit | ~5% conversion (below this, results are not interpreted) |

---

## Statistical Model

Fit a three-way ANOVA on arcsine-transformed conversion (stabilises variance near 0% and 100%):

```
conv_asin ~ Catalyst + Base + Solvent
          + Catalyst:Base + Catalyst:Solvent + Base:Solvent
          + Catalyst:Base:Solvent
          + ε
```

| Source | df | Estimable |
|---|---|---|
| Catalyst | 7 | Yes |
| Base | 2 | Yes |
| Solvent | 2 | Yes |
| Catalyst × Base | 14 | Yes |
| Catalyst × Solvent | 14 | Yes |
| Base × Solvent | 4 | Yes |
| Catalyst × Base × Solvent | 28 | Yes |
| Pure error (18 replicate wells → 9 duplicate pairs) | 9 | Yes |

The 18 replicate wells provide a pure error estimate (9 df) for F-testing the 3-way interaction term. Without them, the 3-way term would serve as the error, making all tests conservative.

**Cannot be estimated:** absolute yield (requires a quantitative internal standard). This design measures relative conversion only.

---

## Campaign Rounds

### Round 1 — this plate (~1 week)

**Decision gate:** ≥1 well reaches ≥20% conversion AND positive controls H11/H12 are concordant.

| Outcome | Next action |
|---|---|
| ≥1 hit, controls pass | Advance top 3 conditions to Round 2 |
| 0 hits, controls pass | Explore Ni/photoredox plate or increase temperature to 100 °C |
| 0 hits, controls fail | Suspect substrate quality or dispensing error; repeat before changing chemistry |

### Round 2 — optimisation (~15–30 wells, shared plate)

Fix top 2 catalyst/base/solvent hits. Vary three continuous factors:

| Factor | Levels |
|---|---|
| Temperature | 60, 80, 100 °C |
| Amine loading | 1.0, 1.5, 2.0 eq |
| Catalyst loading | 2.5, 5, 10 mol% |

Design: **Box-Behnken** (15 runs per catalyst combination).  
Gate: conversion >80% → characterise product on mg scale.

### Round 3 (conditional)

If Round 2 plateau is 50–80%, deploy Gaussian-process Bayesian optimisation (BoTorch, expected-improvement acquisition) to fine-tune within the established ranges. Expected: optimum reached in 10–15 BO queries vs. 27 for a full 3³ grid.

---

## Bayesian Sequential vs. Full Factorial

| Criterion | Full Factorial (Round 1) | Bayesian Sequential |
|---|---|---|
| Prior knowledge required | None | None (needs 5–10 seed experiments) |
| Calendar time | 1 plate, ~1 week | 5–10 sequential rounds, 5–10 weeks |
| Information per run | All 72 combinations simultaneously | Converges to one optimum, misses the map |
| Best for | Categorical survey, no prior data | Continuous fine-tuning after a hit is found |

**Recommendation:** Full factorial in Round 1, Bayesian BO for continuous factors in Rounds 2–3.

---

## Missing Reagents — Purchase List

### High priority (before running the plate)

| Reagent | CAS | Role | Gap |
|---|---|---|---|
| 2-MeTHF (2-methyltetrahydrofuran) | 96-47-9 | Solvent | Frequently outperforms dioxane for BH with polar NH-containing substrates. Absent from kit. |
| KOAc (potassium acetate) | 127-08-2 | Mild base | Ultra-mild (pKa ≈ 9); prevents glutarimide NH deprotonation. Absent from kit. |
| CsOAc (cesium acetate) | 3396-11-0 | Mild base | Same rationale as KOAc; Cs⁺ improves solubility in dioxane/DMA. Absent from kit. |

### Medium priority (Round 2)

| Reagent | CAS | Role | Notes |
|---|---|---|---|
| Free BrettPhos ligand | 1070663-78-3 | Pd ligand | Allows variation of Pd:L ratio beyond 1:1 fixed in G3 precatalysts |
| Free RuPhos ligand | 787618-22-8 | Pd ligand | Same rationale |
| Pd[P(t-Bu)₃]₂ | 53199-31-8 | Pd(0) precatalyst | Highly active for electron-poor ArBr; complements G3 series |
| t-BuOH | 75-65-0 | Co-solvent | 10–20 vol% in DMA/dioxane improves turnover with hindered secondary amines |

---

## Files

| File | Description |
|---|---|
| `HTE_platemap_round1.png` | Colour-coded 96-well plate map |
| `HTE_BH_campaign_design.md` | Full campaign rationale (registered report) |
| `HTE_BH_results_summary.md` | This document |
| `001_matplotlib_use.py` | Plate map source code (grid construction) |
| `002_plt_subplots.py` | Plate map source code (rendering) |
| `HTE_Edelris.sdf` | Reagent kit (74 entries; input) |
