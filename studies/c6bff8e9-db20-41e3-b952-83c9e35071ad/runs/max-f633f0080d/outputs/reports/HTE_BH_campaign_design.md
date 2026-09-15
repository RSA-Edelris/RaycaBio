
## Reaction

| Role | SMILES | Identity |
|---|---|---|
| Aryl bromide | `Brc1ccc2C(=O)N(Cc2c1)C3CCC(=O)NC3=O` | 5-bromo-2-(2,6-dioxopiperidin-3-yl)isoindolin-1-one (lenalidomide/pomalidomide congener) |
| Amine nucleophile | `CC(C)(C)OC(=O)N1CCNCC1` | N-Boc piperazine (secondary NH nucleophile) |
| Reaction type | — | Pd-catalysed Buchwald-Hartwig C–N cross-coupling |

**Critical structural note:** The aryl bromide contains a free glutarimide NH (pKa ≈ 11–13 in DMSO). Under strong base (NaOtBu), this NH is deprotonated and can compete as a nucleophile or give wrong-regioisomer N-arylation. All hits from NaOtBu wells must be confirmed by MS for correct molecular weight before advancing.

---

## 1. Response Definition

- **Response:** Relative conversion of aryl bromide to monoarylated product (%), measured by reverse-phase UPLC-MS with UV detection at 254 nm, reported as peak-area ratio of product to internal standard (fixed concentration of inert arene added post-reaction).
- **Precision floor:** ±3–5% absolute conversion (σ ≈ 2%) on 40 µL HTE scale.
- **Hit threshold:** ≥ 20% conversion (10× the noise floor). Differences below 5% are within assay noise and are not interpreted.

---

## 2. Reagent Inventory (HTE_Edelris.sdf)

| Category | Count | Used in this campaign |
|---|---|---|
| Pd catalysts (G3 precatalysts + Pd(OAc)₂ + Pd₂dba₃) | 20 | 8 selected |
| Bases | 15 | 3 selected |
| Solvents | 9 | 3 selected |
| Photocatalysts (Ir, Ru, organic) | 14 | Not used (thermal BH) |
| Ligands (bipyridyl, phenanthroline) | 11 | Not used (serve Ni/photoredox manifold) |
| Nickel catalysts | 4 | Not used |
| Copper catalyst | 1 | Not used |

---

## 3. Factor Selection

### Varied factors

| Factor | Type | Levels | Justification |
|---|---|---|---|
| Pd-G3 precatalyst | Categorical, 8 | BrettPhos, RuPhos, XPhos, tBuXPhos, SPhos, DavePhos, EPhos, tBuBrettPhos | Ligand dictates reductive elimination rate and mono- vs. bis-arylation selectivity. Bulky biarylphosphines dominate the N-Boc piperazine BH literature. All 8 available as air-stable G3 precatalysts in the kit. |
| Base | Categorical, 3 | Cs₂CO₃, K₃PO₄, NaOtBu | Cs₂CO₃ and K₃PO₄ are mild and will not deprotonate the glutarimide NH; NaOtBu is a forcing condition. DBU and DIPEA excluded (weaker, less precedented for solid-substrate BH on electron-poor ArBr). |
| Solvent | Categorical, 3 | Dioxane, DMA, Toluene | Dioxane: textbook BH. DMA: polar aprotic, best for solubility of the polar isoindolinone-glutarimide substrate. Toluene: non-polar, maximises catalyst stability. |

### Held constant

| Factor | Value | Reason |
|---|---|---|
| Temperature | 80 °C | Standard BH plateau for ArBr; below 60 °C too slow; above 100 °C risks Boc deprotection. Optimize in Round 2. |
| Pd loading | 5 mol% | Standard HTE loading. Optimize in Round 2. |
| Amine : ArBr ratio | 1.5 : 1 | Slight excess of the cheaper partner. |
| [ArBr] | 0.1 M | Practical for 40 µL wells (~4 nmol substrate). |
| Reaction time | 18 h | Overnight; eliminates kinetic variability between wells. |
| Photocatalysts / Ni salts / bipyridines | 0 | Reserved for a separate Ni/photoredox exploratory plate if Pd fails entirely. |

---

## 4. Design

**Type:** Full 8 × 3 × 3 factorial = 72 unique conditions.

**Rationale:** With zero prior conversion data for this substrate/amine pair, no basis exists for assuming which factors dominate. A full factorial resolves all main effects and all two-way and three-way interactions without aliasing. 72 runs fit on one plate alongside 18 replicate wells and 6 controls.

| Category | Wells |
|---|---|
| Unique conditions | 72 |
| Replicate wells (BrettPhos G3 × all 9 base/solvent combinations, each ×2) | 18 |
| Control wells | 6 |
| **Total** | **96** |

---

## 5. Plate Map

![HTE Round 1 plate map — 96-well, Buchwald-Hartwig, 8 Pd-G3 catalysts × 3 bases × 3 solvents](HTE_platemap_round1.png)

**Layout key:**
- Rows A–H: BrettPhos, RuPhos, XPhos, tBuXPhos, SPhos, DavePhos, EPhos, tBuBrettPhos Pd G3
- Columns 1–3: Dioxane (col 1 = Cs₂CO₃, col 2 = K₃PO₄, col 3 = NaOtBu)
- Columns 4–6: DMA (col 4 = Cs₂CO₃, col 5 = K₃PO₄, col 6 = NaOtBu)
- Columns 7–9: Toluene (col 7 = Cs₂CO₃, col 8 = K₃PO₄, col 9 = NaOtBu)
- Columns 10–12, rows A–F: Replicate wells (REP1–REP9, each in duplicate; light blue dashed border)
- Columns 10–12, rows G–H: Control wells (grey gradient = negative controls; green = positive controls)

### Controls

| Well | Contents | Purpose |
|---|---|---|
| G10 | ArBr + amine + K₃PO₄ + dioxane, no catalyst | Confirms no uncatalysed reaction |
| G11 | ArBr + amine + BrettPhos G3 + dioxane, no base | Confirms base is required |
| G12 | ArBr + BrettPhos G3 + K₃PO₄ + dioxane, no amine | Monitors Pd-mediated ArBr decomposition / homocoupling |
| H10 | ArBr + amine + dioxane only (blank) | Background / ArBr thermal stability |
| H11 | Full reference: BrettPhos G3 + Cs₂CO₃ + dioxane | Positive control, plate QC anchor |
| H12 | Duplicate of H11 | Intra-plate reproducibility |

### Randomisation
Row assignment (catalyst) within each 3-column solvent block is randomised before dispensing Pd stocks. Solvent and base column order is also randomised. Randomisation seed recorded in the ELN before plate preparation.

---

## 6. Statistical Model (fixed before data collection)

Fit a three-way ANOVA on arcsine-transformed conversion:

```
conv_asin ~ Catalyst + Base + Solvent
          + Catalyst:Base + Catalyst:Solvent + Base:Solvent
          + Catalyst:Base:Solvent + ε
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
| Pure error (18 replicate wells = 9 duplicate pairs) | 9 | Yes |

The 18 replicate wells supply a pure error estimate (9 df) for F-testing the 3-way interaction term. Without these replicates, the 3-way interaction would have to serve as the error term, making all tests conservative.

**Cannot be estimated:** absolute yield (requires fully quantitative internal standard). This design measures relative conversion only.

---

## 7. Campaign Rounds and Decision Gates

### Round 1 — this plate (target: 1 week)
**Gate:** ≥ 1 well reaches ≥ 20% conversion AND positive controls (H11/H12) are concordant.
- Pass → advance top 3 catalyst/base/solvent combinations to Round 2.
- Fail with passing controls → consider Ni/photoredox plate or elevated temperature (100 °C).
- Fail with failing controls → suspect substrate quality or dispensing error; repeat before changing chemistry.

### Round 2 — optimisation (~24–30 wells, shared plate)
Fix top 2 catalyst/base/solvent hits. Screen three continuous factors:
- Temperature: 60, 80, 100 °C
- Amine loading: 1.0, 1.5, 2.0 eq
- Catalyst loading: 2.5, 5, 10 mol%

**Design:** Box-Behnken over 3 continuous factors (15 runs per combination).
**Gate:** conversion > 80% → characterise product on mg scale.

### Round 3 (conditional)
If Round 2 plateau is 50–80%, deploy a Gaussian process Bayesian optimiser (e.g., BoTorch with expected improvement) to fine-tune within the established ranges. BO reaches the optimum in 10–15 queries vs. 27 for a full 3³ grid at this stage.

---

## 8. Bayesian Sequential vs. Full Factorial

| Criterion | Round 1 Full Factorial | Bayesian Sequential |
|---|---|---|
| Prior knowledge | None | None (requires 5–10 seed experiments) |
| Calendar time | 1 plate, ~1 week | 5–10 sequential rounds, 5–10 weeks |
| Information per run | All 72 combinations simultaneously | Converges to one optimum, misses the map |
| Best for | Categorical surveys with no prior data | Continuous fine-tuning after a hit is found |

**Conclusion:** The hybrid strategy (full factorial Round 1 → BO in Rounds 2–3 for continuous factors) reaches the optimum faster than either approach alone.

---

## 9. Missing Reagents — Purchase Recommendations

### High priority (before running the plate)

| Reagent | CAS | Role | Gap |
|---|---|---|---|
| 2-MeTHF (2-methyltetrahydrofuran) | 96-47-9 | Solvent | Frequently outperforms dioxane for BH with polar, NH-containing substrates. Absent from kit. Strong literature precedent for lenalidomide-type compounds. |
| KOAc (potassium acetate) | 127-08-2 | Mild base | Ultra-mild (pKa ≈ 9); prevents deprotonation of glutarimide NH entirely. Absent from kit. |
| CsOAc (cesium acetate) | 3396-11-0 | Mild base | Same rationale as KOAc; Cs⁺ improves base solubility in dioxane/DMA. Absent from kit. |

### Medium priority (Round 2)

| Reagent | CAS | Role | Notes |
|---|---|---|---|
| Free BrettPhos ligand | 1070663-78-3 | Pd ligand | Allows variation of Pd:L ratio (G3 precatalysts fix 1:1). |
| Free RuPhos ligand | 787618-22-8 | Pd ligand | Same rationale. |
| Pd[P(t-Bu)₃]₂ | 53199-31-8 | Pd(0) precatalyst | Highly active for electron-poor ArBr; complements G3 series. |
| t-BuOH | 75-65-0 | Co-solvent | Added at 10–20 vol% to DMA or dioxane; improves turnover with hindered secondary amines. |

---

## Files Produced

| File | Description |
|---|---|
| `HTE_platemap_round1.png` | Colour-coded 96-well plate map for Round 1 |
| `HTE_BH_campaign_design.md` | This document |
