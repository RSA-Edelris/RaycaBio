
## Plate overview

![HTE Round 2 plate map — 96-well, 4 bases × 2 solvents × 12 Pd catalysts](HTE_platemap_round2_4x2x12.png)

| Parameter | Value |
|---|---|
| Design | Full 4 × 2 × 12 factorial |
| Total wells | 96 (fully saturated) |
| Unique conditions | 96 |
| Controls | 0 dedicated (reference Round 1 plate — see note below) |
| Response | % relative conversion ArBr → monoarylated product, UPLC-UV 254 nm |
| Fixed conditions | 5 mol% Pd, 1.5 eq amine, 0.1 M [ArBr], 80 °C, 18 h |

> **Controls note.** A 4 × 2 × 12 full factorial uses all 96 wells. No room remains for dedicated control wells. This is acceptable only because Round 1 established the assay on the same substrate lot with qualified negative controls (no-cat, no-base, blank) and a positive reference (BrettPhos G3 / Cs₂CO₃ / dioxane). Round 2 must be run with the **same internal standard, same quench protocol, and same UPLC method** as Round 1. If any of these change, insert a 6-well control strip by dropping one catalyst column and running 11 catalysts instead of 12.

---

## Layout

| Axis | Factor | Levels |
|---|---|---|
| Columns 1–12 | Pd catalyst | 12 (see table below) |
| Rows A–D | Base (in dioxane) | K₂CO₃ · Cs₂CO₃ · K₃PO₄ · DIPEA |
| Rows E–H | Base (in t-AmylOH) | K₂CO₃ · Cs₂CO₃ · K₃PO₄ · DIPEA |

Row-block backgrounds: warm yellow = dioxane (A–D), cool green = t-AmylOH (E–H).  
Row colour bands: peach = K₂CO₃, blue = Cs₂CO₃, green = K₃PO₄, pink = DIPEA.  
Column borders: gold ring = NHC catalyst; dashed white = bidentate bisphosphine.

---

## 12 Pd catalysts — selection rationale

| Col | Short | Full name | CAS | Tag | Ligand class | Rationale |
|---|---|---|---|---|---|---|
| 1 | BPG3 | BrettPhos Pd G3 | 1470372-59-8 | R1 | Bulky biaryl monophosphine | Top literature catalyst for ArBr + secondary amine C–N coupling; large cone angle suppresses bis-arylation |
| 2 | tBBG3 | tBuBrettPhos Pd G3 | 1536473-72-9 | R1 | Bulky biaryl monophosphine | tBu version of BrettPhos; more electron-rich, accelerates reductive elimination for hindered amines; complements col 1 |
| 3 | RuPG3 | RuPhos Pd G3 | 1445085-77-7 | R1 | Biaryl dialkylphosphine | Excellent breadth across ArBr partners; well-characterised with piperazine nucleophiles in the literature |
| 4 | tBXG3 | tBuXPhos Pd G3 | 1447963-75-8 | R1 | Bulky biaryl monophosphine | Favoured when reductive elimination is rate-limiting; large steric profile accelerates C–N bond formation |
| 5 | EPG3 | EPhos Pd G3 | 2940916-90-3 | R1 | Biaryl dialkylphosphine with ether | Handles challenging coupling partners; newer-generation ligand with increased electron density |
| 6 | SPG3 | SPhos Pd G3 | 1445085-82-4 | R1 | Biaryl dialkylphosphine | Classical BH reference; broad precedent on electron-poor ArBr; benchmark for comparison |
| 7 | MorG3 | MorDalPhos Pd G3 | 2222690-89-1 | NEW | Morpholine-biaryl phosphine | Ligand designed explicitly for C–N coupling with **secondary** amines including piperazines; morpholine oxygen modulates electronics at Pd; not tested in Round 1 |
| 8 | APG3 | APhos Pd G3 | 1820817-64-8 | NEW | Aminobiaryl phosphine | Dimethylaminophenyl donor increases electron density at Pd; reported excellent yields for N-arylation of cyclic secondary amines |
| 9 | GPG3 | GPhos Pd G3 | 2489525-82-6 | NEW | Biaryl phosphine, gem-dialkyl | Rigid gem-dialkyl-substituted backbone fixes the bite geometry; may outperform flexible analogues on this electron-poor ArBr |
| 10 | CatG3 | cataCXium-A Pd G3 | 1651823-59-4 | NEW | Di(adamantyl)butylphosphine | Aliphatic (non-biaryl) bulky phosphine; different steric profile from all biaryl entries; active catalyst for challenging ArBr coupling |
| 11 | dppf | dppf-Pd-G3 | 1445086-28-1 | NEW | **Bidentate bisphosphine** | Only bidentate entry; larger bite angle (96°) stabilises Pd(0)/Pd(II) cycle differently; known activity for BH; direct comparison with mono-dentate G3 series |
| 12 | PEPSI | **PEPPSI [NHC-Pd]** | 1158652-41-5 | **NHC** | **N-heterocyclic carbene** | **Only non-phosphine ligand in the campaign.** NHC ligands are stronger σ-donors than phosphines, making Pd more electron-rich and accelerating oxidative addition. The 3-chloropyridine leaving group gives a well-defined active Pd(0) species. NHC-Pd can outperform phosphine catalysts on electron-poor ArBr with challenging nucleophiles where phosphine dissociation is problematic. |

### Why PEPPSI as the non-phosphine entry

NHC ligands are non-labile (unlike phosphines, which can dissociate under turnover), making the catalyst more robust at elevated temperatures. For the lenalidomide-type ArBr substrate — which is electron-poor due to flanking imide carbonyls — oxidative addition to Pd(0) is fast regardless of ligand donor strength, but reductive elimination of the C–N bond is the bottleneck. The strong σ-donor NHC pushes electron density onto Pd, directly accelerating this step. No NHC-based entry was in Round 1, so PEPPSI provides an orthogonal chemotype that could succeed where phosphine G3 catalysts fail, or reveal a selectivity pattern distinct from the phosphine series.

---

## 4 Bases — selection rationale

| Base | pKa (water) | Type | Round 1 | Rationale |
|---|---|---|---|---|
| **K₂CO₃** | 10.3 | Inorganic, mild | No | Mildest inorganic base in the kit. Will not deprotonate the glutarimide NH (pKa ≈ 11–13). Added because Round 1 included Cs₂CO₃ and K₃PO₄ but not K₂CO₃; relevant if Cs₂CO₃ gave side products via the Cs⁺ activating effect. Heterogeneous in dioxane — suspension often beneficial. |
| **Cs₂CO₃** | ~10.3 | Inorganic, mild | Yes | Round 1 reference base. The Cs⁺ cation enhances anion activation and base solubility in organic solvents. Retained as the intra-plate calibration anchor against Round 1. |
| **K₃PO₄** | 12.4 | Inorganic, mild | Yes | Second Round 1 reference base. Slightly stronger than Cs₂CO₃; frequently the best base for BH with electron-poor aryl bromides. Retained as second intra-plate anchor. |
| **DIPEA** | 11.4 (MeCN) | Organic, non-nucleophilic | No | Hünig's base; homogeneous in all solvents (unlike the three inorganic bases). Key question: can a fully soluble base outperform a heterogeneous suspension? Particularly relevant in t-AmylOH where K₃PO₄ and K₂CO₃ are poorly soluble. DIPEA cannot deprotonate the glutarimide NH under thermal conditions. |

**What changed vs Round 1:** NaOtBu is dropped. It caused the greatest risk of glutarimide NH deprotonation and N-arylation side products. K₂CO₃ and DIPEA are new entries that extend coverage in the mild-base region without adding deprotonation risk.

---

## 2 Solvents — selection rationale

| Solvent | BP (°C) | Type | Round 1 | Rationale |
|---|---|---|---|---|
| **1,4-Dioxane** | 101 | Cyclic ether, aprotic | Yes | Benchmark solvent from Round 1; provides direct comparison of all 12 catalysts and 4 bases against the established reference. |
| **t-AmylOH** | 102 | Tertiary alcohol, protic | No | In kit (CAS 75-65-0). Protic but has no β-H for elimination. Used in BH protocols where substrate solubility in aprotic solvents is poor; the polar-protic environment can accelerate the proton-transfer step during amine coordination. The isoindolinone-glutarimide substrate is polar and may be better solvated here than in dioxane. Not tested in Round 1. |

**Why not include DMA or toluene from Round 1?** Both were already explored. The purpose of Round 2 is to expand the chemical space, not repeat it. t-AmylOH introduces a new solvent class (protic) and is available in the kit without additional purchase.

> If 2-MeTHF has been purchased following the Round 1 recommendation, **replace t-AmylOH with 2-MeTHF** — it has stronger literature precedent for BH with N-H-containing substrates and is the higher-priority solvent to evaluate.

---

## What the design can and cannot estimate

**Can estimate (full factorial, saturated):**
- All catalyst main effects (11 df across 12 levels)
- Base main effect (3 df)
- Solvent main effect (1 df)
- All two-way interactions: Cat × Base (33 df), Cat × Solvent (11 df), Base × Solvent (3 df)
- Three-way interaction: Cat × Base × Solvent (33 df)

**Cannot estimate without replicates:**
- Pure error term (no replicate wells)
- Statistical significance of three-way interaction requires Round 1 pure-error σ² as the reference

**Consequence:** Use Round 1 replicate-based σ² (from REP1–REP9 pairs) as the error estimate for Round 2 ANOVA. This is valid only if the assay precision has not changed between plates. Run at least two wells in common between the two plates (e.g., BrettPhos G3 / Cs₂CO₃ / dioxane, which appears at B1 in Round 2) to verify assay drift.

---

## Analysis plan

1. **Cross-plate calibration:** Compare wells B1 (BPG3/Cs₂CO₃/dioxane, Round 2) against H11/H12 (positive controls, Round 1). Difference > 15% absolute triggers assay-drift investigation before proceeding.
2. **Hit calling:** Conversion ≥ 20% (same threshold as Round 1).
3. **New-entry performance:** Compare MorDalPhos (col 7), APhos (col 8), GPhos (col 9), cataCXium-A (col 10) against the Round 1 champion in the same base/solvent row.
4. **NHC benchmark:** PEPPSI (col 12) vs. best phosphine in each row — if PEPPSI wins in ≥ 3 rows, include NHC catalysts in Round 3.
5. **Solvent comparison:** Dioxane rows A–D vs. t-AmylOH rows E–H — paired by catalyst and base.
6. **Base comparison within solvent:** For each catalyst × solvent pair, rank K₂CO₃ vs. Cs₂CO₃ vs. K₃PO₄ vs. DIPEA.

---

## Files

| File | Description |
|---|---|
| `HTE_platemap_round2_4x2x12.png` | Colour-coded 96-well plate map, Round 2 |
| `HTE_BH_round2_4x2x12.md` | This document |
| `HTE_BH_campaign_design.md` | Round 1 full campaign rationale |
| `HTE_BH_results_summary.md` | Round 1 summary with verification section |
| `generate_platemap.py` | Self-contained script for Round 1 plate map |
