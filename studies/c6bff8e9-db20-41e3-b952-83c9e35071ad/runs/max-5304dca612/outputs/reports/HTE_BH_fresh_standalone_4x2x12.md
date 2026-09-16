
## Overview

This plate is designed entirely from chemical first principles. It makes no reference to data from any prior HTE plate. Every factor-level choice is justified by literature precedent or chemical logic alone.

| Parameter | Value |
|---|---|
| Reaction | Buchwald-Hartwig C–N cross-coupling |
| Aryl bromide | `Brc1ccc2C(=O)N(Cc2c1)C3CCC(=O)NC3=O` — 5-bromo-2-(2,6-dioxopiperidin-3-yl)isoindolin-1-one |
| Amine | `CC(C)(C)OC(=O)N1CCNCC1` — N-Boc piperazine (secondary NH) |
| Design | Full 4 × 2 × 12 factorial |
| Total wells | 96 (fully saturated) |
| Fixed conditions | 5 mol% Pd, 1.5 eq amine, 0.1 M [ArBr], 80 °C, 18 h |
| Controls | 0 dedicated wells — add 6-well strip if no prior assay qualification exists |

> **Structural alert — glutarimide NH.** The aryl bromide carries a free glutarimide NH (pKa ≈ 11–13 in DMSO). Bases with pKaH > 13 risk deprotonating it and causing N-arylation side products. All bases in this plate are selected below that threshold.

---

## Plate map

![Fresh standalone HTE plate — 96-well, 4 bases × 2 solvents × 12 Pd catalysts](HTE_platemap_fresh_4x2x12.png)

---

## Layout

| Axis | Factor | Levels |
|---|---|---|
| Columns 1–12 | Pd catalyst | 12 (see table below) |
| Rows A–D | Base in **Dioxane** | K₃PO₄ · Cs₂CO₃ · DBU · DIPEA |
| Rows E–H | Base in **DMF** | K₃PO₄ · Cs₂CO₃ · DBU · DIPEA |

---

## 12 Pd catalysts — rationale

| Col | Short | Full name | CAS | Ligand class | Rationale |
|---|---|---|---|---|---|
| 1 | BPG3 | BrettPhos Pd G3 | 1470372-59-8 | Biaryl mono-phosphine | Benchmark: best-documented catalyst for ArBr + secondary amine BH; large %Vbur suppresses bis-arylation |
| 2 | tBBG3 | tBuBrettPhos Pd G3 | 1536473-72-9 | Biaryl mono-phosphine | Most electron-rich BrettPhos analogue; larger bulk accelerates C–N reductive elimination |
| 3 | RuPG3 | RuPhos Pd G3 | 1445085-77-7 | Biaryl mono-phosphine | Broad-scope reference; well-characterized on piperazine nucleophiles |
| 4 | XPG3 | XPhos Pd G3 | 1445085-55-1 | Biaryl mono-phosphine | Large cone angle; excellent for electron-poor ArBr substrates |
| 5 | MorG3 | MorDalPhos Pd G3 | 2222690-89-1 | Biaryl mono-phosphine | Ligand architected specifically for C–N coupling with **secondary amines**; morpholine-O modulates Pd electronics |
| 6 | PCy3 | PCy3 Pd G3 | 1445086-12-3 | **Trialkyl mono-phosphine** | Only purely aliphatic monodentate entry; no biaryl framework; different steric topology entirely; pure σ-donor |
| 7 | XantG3 | XantPhos Pd G3 | 1445085-97-1 | **Bidentate bisphosphine** | Wide natural bite angle (≈108°); well-established in BH; chelate prevents phosphine dissociation; geometry distinct from all monodentates |
| 8 | dppf | dppf Pd G3 | 1445086-28-1 | **Bidentate bisphosphine** | Ferrocenyl backbone; natural bite angle ≈96°; flexible conformational space around Pd; different from XantPhos |
| 9 | BINAP | rac-BINAP Pd G3 | 2151915-22-7 | **Bidentate bisphosphine** | Atropisomeric axial chirality; bite angle ≈92°; rarely included in BH screens but active; covers an underexplored bidentate topology |
| 10 | CatA | cataCXium-A Pd G3 | 1651823-59-4 | **Aliphatic bulky mono-P** | 1-adamantyl groups; non-biaryl; complementary steric profile to biaryl series; documented activity on challenging ArBr |
| 11 | GPG3 | GPhos Pd G3 | 2489525-82-6 | Biaryl mono-phosphine | Rigid gem-dialkyl-substituted backbone; unique bite geometry among biaryl mono-phosphines |
| 12 | **PEPSI** | **PEPPSI [NHC-Pd]** | 1158652-41-5 | **NHC — non-phosphine ★** | The only non-phosphine catalyst in the campaign. NHC is a stronger σ-donor than any phosphine and non-labile under turnover. The 3-chloropyridine labilising ligand generates a well-defined Pd(0) active species. For this electron-poor ArBr, C–N reductive elimination is rate-limiting; NHC directly accelerates it. Provides an orthogonal chemotype that could outperform the entire phosphine series. |

### Ligand-class coverage

| Class | Cols | Count |
|---|---|---|
| Biaryl mono-phosphine | 1–5, 11 | 6 |
| Trialkyl / aliphatic mono-phosphine | 6, 10 | 2 |
| Bidentate bisphosphine | 7–9 | 3 |
| NHC (non-phosphine) | 12 | **1** |

---

## 4 Bases — rationale

| Base | pKa (aq) | Type | Rationale |
|---|---|---|---|
| **K₃PO₄** | 12.4 | Inorganic, mild | Classical BH base; heterogeneous suspension in organic solvents (often beneficial for selectivity); below glutarimide NH deprotonation threshold; broad precedent |
| **Cs₂CO₃** | ~10 | Inorganic, mild | Cs⁺ activates anion and improves solubility vs K⁺ salts; very mild; one of the most widely used BH bases in the literature |
| **DBU** | ~13 (aq), ~24 (MeCN) | Organic, strong | Homogeneous in all solvents; commonly paired with NHC-Pd catalysts; provides a fundamentally different base environment (non-ionic, no counter-cation effects); borderline for glutarimide NH — verify product MW on all DBU hits |
| **DIPEA** | 11.4 | Organic, mild | Non-nucleophilic; homogeneous; mildest in this set; particularly valuable in DMF where inorganic bases may be poorly soluble |

**Dropped vs a generic screen:** NaOtBu and LiHMDS — both in the kit but unacceptable here because pKa > 13 guarantees glutarimide NH deprotonation and will generate N-arylation side products.

---

## 2 Solvents — rationale

| Solvent | ε | Type | Rationale |
|---|---|---|---|
| **1,4-Dioxane** | 2.2 | Cyclic ether, aprotic | Standard reference solvent for Pd-catalysed BH; low polarity allows clean substrate/product partitioning; the default against which all BH protocols are benchmarked |
| **DMF** | 37 | Amide, polar aprotic | Very high polarity for maximal solvation of the polar isoindolinone-glutarimide substrate; commonly the superior solvent for challenging BH substrates with limited solubility in dioxane; not a duplication of any prior plate in this campaign |

The two solvents span the widest achievable polarity contrast within the aprotic class (ε ≈ 2 vs ε ≈ 37). This design avoids protic solvents (risk of Pd(0) oxidation) and halogenated solvents (DCE can be oxidising to Pd).

---

## What the design can estimate

| Effect | df | Estimable |
|---|---|---|
| Catalyst main effect | 11 | Yes |
| Base main effect | 3 | Yes |
| Solvent main effect | 1 | Yes |
| Catalyst × Base | 33 | Yes |
| Catalyst × Solvent | 11 | Yes |
| Base × Solvent | 3 | Yes |
| Catalyst × Base × Solvent | 33 | Yes |
| **Pure error** | **0** | **No — no replicate wells** |

No replicates fit on a fully saturated 96-well plate. Use a σ² estimate from an independent assay qualification run (3–6 duplicate wells) before applying ANOVA F-tests.

---

## Controls

A fully saturated 4×2×12 = 96 plate leaves no dedicated control wells. Two approaches:

**Option A (preferred):** Add a separate 6-well control strip in the same assay run:
- No catalyst / K₃PO₄ / dioxane (confirms no uncatalysed reaction)
- No base / BrettPhos G3 / dioxane (confirms base is required)
- No amine / BrettPhos G3 / K₃PO₄ / dioxane (monitors ArBr side reactions)
- Blank: ArBr + amine / dioxane only (thermal stability)
- Positive ctrl × 2: BrettPhos G3 / Cs₂CO₃ / dioxane (duplicate)

**Option B:** Drop one catalyst column (run 11 catalysts, 88 wells) and use cols 12 rows G-H + col 11 rows G-H for 6 control wells.

---

## Analysis plan

1. **Hit calling:** conversion ≥ 20% (UPLC-UV 254 nm, ±3–5% absolute precision)
2. **NHC vs phosphine:** PEPPSI (col 12) vs. best phosphine across all base × solvent combinations
3. **Denticity comparison:** bidentate block (cols 7–9) vs. monodentate block (cols 1–6, 10–11)
4. **Solvent effect:** compare each catalyst × base row across dioxane vs DMF
5. **Base sensitivity:** for each catalyst × solvent, rank K₃PO₄ vs Cs₂CO₃ vs DBU vs DIPEA
6. **DBU alert:** all DBU hits (rows C/G) must be confirmed by MS for correct product MW before advancing — DBU may produce glutarimide N-arylation side product

---

## Files

| File | Description |
|---|---|
| `HTE_platemap_fresh_4x2x12.png` | Colour-coded 96-well plate map |
| `generate_platemap_fresh.py` | Self-contained, standalone plate map generator |
| `HTE_BH_fresh_standalone_4x2x12.md` | This document |
