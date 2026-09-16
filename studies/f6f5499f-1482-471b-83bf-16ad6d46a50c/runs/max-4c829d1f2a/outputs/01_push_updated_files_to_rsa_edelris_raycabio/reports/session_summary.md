# Session Summary — HTE Campaign Design
**Date:** 2026-09-16  
**Session ID:** f6f5499f-1482-471b-83bf-16ad6d46a50c  
**Run ID:** max-6c649ef204  
**Repository:** RSA-Edelris/RaycaBio (commit `da27bb1`, 48 files)

---

## Overview

Two independent 24-well HTE Round 1 screening plates were designed for photocatalytic C–C bond-forming reactions, both run at fixed 470 nm irradiation. The work covered reagent inventory, factor selection and justification, full factorial design, statistical model pre-registration, plate map generation, and multi-phase audit with documented corrections.

---

## Campaign 1 — Ni/Ir Dual Photoredox Decarboxylative Cross-Coupling

### Reaction

| Item | Detail |
|------|--------|
| Electrophile | N-Cbz-4-bromopiperidine — `BrC1CCN(CC1)C(=O)OCc2ccccc2` |
| Radical precursor (acid) | N-Boc-1-azaspiro[5.2]octane-4-carboxylic acid — `CC(C)(C)OC(=O)N1CC2(CC2)CC1C(=O)O` |
| Mechanism | Ni(I/II/III) + PC* (oxidative quench) decarboxylative radical C(sp³)–C(sp³) coupling |
| Reagent kit | `HTE_Edelris.sdf` — 72 molecules |
| Light | 470 nm (fixed) |

### Reagent Inventory (72 entries, 0 failures)

| Class | Count | Kit indices |
|-------|-------|-------------|
| Photocatalyst — Ir | 4 | 12, 31, 35, 58 |
| Photocatalyst — Ru | 3 | 13, 15, 33 |
| Photocatalyst — Organic | 5 | 5, 6, 32, 38, 60 |
| Ni catalyst | 4 | 10, 21, 34, 55 |
| Pd catalyst (not used) | 20 | 0, 2, 3, 7–9, 14, 16–19, 30, 36, 39–40, 47, 56, 59, 61, 63 |
| Bidentate N-ligand for Ni | 8 | 1, 4, 11, 22, 26, 27, 46, 57 |
| Chiral N-ligand | 1 | 62 |
| Base (inorganic/organic) | 12 | 23, 29, 37, 41, 42, 43, 48, 50, 51, 52, 53, 71 |
| Solvent | 9 | 24, 25, 64, 65, 66, 67, 68, 69, 70 |
| Cu catalyst | 1 | 49 |
| HAT/amine additive | 1 | 28 |
| P-ligand | 2 | 20, 45 |

**Missing reagents:** MeCN absent from kit (most common solvent for this reaction class). All other essential components present. No purchase is required to run the plate; MeCN is recommended for Round 2.

### Factors and Design

| Factor | Levels | Justification |
|--------|--------|---------------|
| **Photocatalyst** (rows A–D) | 4 | E*(PC*/PC⁺) must exceed Ep(carboxylate) ≈ +0.9–1.1 V vs SCE; PC is the dominant variable |
| **Ni bidentate N-ligand** (column pairs) | 3 | Controls Ni oxidation-state cycling and C–C reductive elimination |
| **Inorganic base** (odd/even) | 2 | Cs₂CO₃ vs K₃PO₄; affects carboxylate deprotonation and Ni catalyst resting state |

**Photocatalysts selected (E* vs SCE for oxidative quenching):**

| Row | Photocatalyst | E*(PC*/PC⁺) | Role |
|-----|--------------|-------------|------|
| A | Ir[dF(CF₃)ppy]₂(dtbbpy)·PF₆ (kit #31) | +1.32 V | MacMillan reference |
| B | 4CzIPN (kit #38) | +1.52 V | Organic PC; cost-effective |
| C | Mes-Acr⁺·BF₄ (kit #32) | +2.00 V | Highly oxidising; over-oxidation risk |
| D | Ir[dF(4-tBupy)]₂(dtbbpy) (kit #12) | ~+1.10 V | Borderline E*; diagnostic reference |

**Ni ligands:** dtbbpy (kit #27) · 4,4′-dMe-bpy (kit #1) · 1,10-phen (kit #46)  
**Bases:** Cs₂CO₃ (kit #52) · K₃PO₄ (kit #53)

**Design:** Full 4 × 3 × 2 = 24-well factorial. All main effects and 2-way interactions estimable; 3-way PC×Lig×Base (6 df) used as error surrogate.

**Fixed conditions:** NiBr₂·dme 10 mol% (kit #21) · DMA 0.1 M (kit #66) · electrophile 1.0 equiv · acid 1.5 equiv · base 2.0 equiv · PC 1 mol% · 470 nm · rt · 16 h · N₂

### Pre-registered Statistical Model

```
Y_ijk = µ + α_i(PC) + β_j(Lig) + γ_k(Base) + (αβ)_ij + (αγ)_ik + (βγ)_jk + ε_ijk
```

| Source | df |
|--------|----|
| PC | 3 |
| Ligand | 2 |
| Base | 1 |
| PC × Ligand | 6 |
| PC × Base | 3 |
| Ligand × Base | 2 |
| **PC × Lig × Base (error)** | **6** |
| **Total** | **23** |

Response: relative conversion (%) by UPLC. Arcsin√(p/100) transform if data cluster near 0 or 100%.

### Round Structure

| Round | Plate | Variables | Decision rule |
|-------|-------|-----------|---------------|
| 1 (this) | 24 wells | PC × Lig × Base | ≥1 well ≥30%: fix PC+Lig, go Round 2 |
| 2 (if hit) | 24 wells | Concentration, base stoich, temperature, time (CCD + centre + axial) | ≥60%: scale up |
| 3 (if needed) | 24 wells | Acid equiv, quinuclidine HAT | ≥60%: scale up |

**Bayesian BO vs. full factorial:** BO offers no advantage in Round 1 (search space = plate capacity). BO valuable from Round 2 onward with continuous variables.

### Response Definition

| Item | Decision |
|------|----------|
| Response | Relative conversion (%): product / (product + SM) × 100 |
| Measurement | UPLC, internal standard (1,3,5-trimethoxybenzene, 1 equiv) |
| Precision | ±3–5% absolute |
| Hit threshold | ≥30% = Round 2 candidate; ≥60% = direct scale-up |

### Plate Map

**File:** `plate_map_round1.png` | Dispensing seed: 42

- Rows → Photocatalyst (A = deep blue, B = green, C = red, D = purple)
- Column pairs 1–2 / 3–4 / 5–6 → Ni ligand (no hatch / diagonal / cross hatch)
- Well text "Cs" / "K₃P" → Base

### Reagents to Purchase

| Reagent | Priority | Reason |
|---------|----------|--------|
| Acetonitrile (MeCN) | High | Most used solvent for Ni/photoredox; absent from kit |
| [Ir(dF(CF₃)ppy)₂(bpy)]PF₆ | Medium | Decouples PC ancillary ligand from Ni ligand |
| 4,4′-di-CF₃-2,2′-bipyridine | Medium | Completes electron-poor Ni-ligand series |
| Phenylsilane (PhSiH₃) | Medium | HAT catalyst; entirely absent from kit |
| HFIP or TFE | Low | Fluorinated alcohol cosolvent |

---

## Campaign 2 — Photocatalytic NHP-ester Minisci Radical C–H Alkylation

### Reaction

| Item | Detail |
|------|--------|
| Heteroarene (acceptor) | 8-bromoquinoline — `Brc1cncc2ccccc12` |
| NHP ester (radical precursor) | N-Boc-piperidine-4-yl NHP ester — `CC(C)(C)OC(=O)N1CCC(CC1)C(=O)OC2C(=O)c3ccccc3C2=O` |
| Product | `CC(C)(C)OC(=O)N1CCC(CC1)c2ncc(Br)c3ccccc23` — C2-alkylated quinoline |
| Mechanism | PC* (reductive quench) → R• + CO₂ + phthalimide⁻; R• adds to protonated quinolinium at C2; re-oxidation by PC⁺ restores aromaticity. **No Ni required.** |
| Reagent kit | `HTE_Edelris_2.sdf` — 74 molecules |
| Light | 470 nm (fixed) |

### Reagent Inventory (74 entries, 0 failures)

| Class | Count | Kit indices |
|-------|-------|-------------|
| Photocatalyst — Ir | 4 | 12, 31, 35, 58 |
| Photocatalyst — Ru | 3 | 13, 15, 33 |
| Photocatalyst — Organic | 5 | 5, 6, 32, 38, 60 |
| Ni catalyst | 4 | 10, 21, 34, 55 |
| Pd catalyst (not relevant) | 20 | 0, 2, 3, 7–9, 14, 16–19, 30, 36, 39–40, 47, 56, 59, 61, 63 |
| Bidentate N-ligand | 8 | 1, 4, 11, 22, 26, 27, 46, 57 |
| Monodentate N-ligand | 2 | 44 (2,6-lutidine), 54 (pyridine) |
| Chiral N-ligand | 1 | 62 |
| Base (inorganic/organic) | 12 | 23, 29, 37, 41, 42, 43, 48, 50, 51, 52, 53, 71 |
| Solvent | 11 | 24, 25, 64, 65, 66, 67, 68, 69, 70, 72, 73 |
| Cu catalyst | 1 | 49 |
| HAT/amine additive | 1 | 28 |
| P-ligand | 2 | 20, 45 |

**vs. HTE_Edelris.sdf (kit 1):** MeCN (idx 72) and Water (idx 73) added. DCE replaces DCM. Dioxane confirmed (kit 1 erroneously labelled it DME).

**Critical gap — MUST PURCHASE:** No Brønsted acid anywhere in 74 entries. Confirmed by SMARTS search `[CX3](=O)[OX2H1]` (0 hits). TFA is required for quinolinium protonation; without it radical addition rate and C2 regioselectivity drop >10× (literature precedent).

> **Note:** An earlier search using Python substring `'C(=O)O'` gave a false 0 result by coincidence (TFA canonicalises in RDKit as `O=C(O)C(F)(F)F`, which does not contain the literal substring). The SMARTS-based re-run (`012_acid_smarts_recheck.py`) is the authoritative check. Conclusion (TFA absent) is unchanged.

### Factors and Design

| Factor | Levels | Justification |
|--------|--------|---------------|
| **Photocatalyst** (rows A–D) | 4 | E*(PC*/PC⁺) must be more negative than Ep(NHP ester) ≈ −1.0 to −1.2 V vs SCE; PC is the highest-impact variable |
| **Solvent** (column pairs) | 3 | Controls radical solvation, NHP-ester solubility, quinolinium pKₐ |
| **Acid additive** (odd/even) | 2 | Protonation of quinoline N activates ring toward radical addition; TFA vs. no acid |

**Photocatalysts selected (E*(PC*/PC⁺) for oxidative quenching; must be more negative than Ep(NHP ester)):**

| Row | Photocatalyst | E*(PC*/PC⁺) | Role |
|-----|--------------|-------------|------|
| A | fac-Ir(ppy)₃ (kit #58) | −1.51 V | Strongest reductant; reference for NHP Minisci |
| B | 4CzIPN (kit #38) | −1.04 V | Organic PC; most used in published NHP-Minisci |
| C | Ir(ppy)₂(dtbbpy)·PF₆ (kit #35) | −0.96 V | Moderate Ir; borderline comparison |
| D | Ir[dF(CF₃)ppy]₂(dtbbpy)·PF₆ (kit #31) | −0.89 V | Below threshold; diagnostic role |

**Solvents:** MeCN (kit #72) · DMSO (kit #24) · Dioxane (kit #70)  
**Acid:** TFA 1.0 equiv (odd columns) vs. no acid (even columns)

**Design:** Full 4 × 3 × 2 = 24-well factorial. All main effects and 2-way interactions estimable; 3-way PC×Solv×Acid (6 df) used as error surrogate.

**Fixed conditions:** Quinoline 1.0 equiv · NHP ester 1.5 equiv · PC 2 mol% · 0.1 M · 470 nm · rt · 16 h · N₂. No Ni catalyst.

### Pre-registered Statistical Model

```
Y_ijk = µ + α_i(PC) + β_j(Solv) + γ_k(Acid) + (αβ)_ij + (αγ)_ik + (βγ)_jk + ε_ijk
```

| Source | df |
|--------|----|
| PC | 3 |
| Solvent | 2 |
| Acid | 1 |
| PC × Solvent | 6 |
| PC × Acid | 3 |
| Solvent × Acid | 2 |
| **PC × Solv × Acid (error)** | **6** |
| **Total** | **23** |

### Round Structure

| Round | Plate | Variables | Decision rule |
|-------|-------|-----------|---------------|
| 1 (this) | 24 wells | PC × Solvent × Acid | ≥1 well ≥30%: fix PC+Solvent, go Round 2 |
| 2 (if hit) | 24 wells | Acid stoich (0.5–3 equiv), NHP equiv (1.0–2.5), PC loading (1–5 mol%) — RSM/CCD | ≥60%: scale up |
| 3 (if needed) | 24 wells | Temperature (rt, 40, 60°C), time (8, 16, 24 h) | ≥60%: scale up |

### Response Definition

| Item | Decision |
|------|----------|
| Response | Relative conversion (%): product / (product + SM) × 100 |
| Measurement | UPLC, internal standard (1,3,5-trimethoxybenzene, 1 equiv) |
| Precision | ±3–5% absolute |
| Hit threshold | ≥30% = Round 2 candidate; ≥60% = direct scale-up |

### Plate Map

**File:** `plate_map_minisci_round1.png` | Dispensing seed: 7

- Rows → Photocatalyst (A = emerald #1A7A4A, B = teal #1B7E8C, C = blue #1F4E8C, D = purple #6B2FA0)
- Column pairs 1–2 / 3–4 / 5–6 → Solvent (no hatch = MeCN / diagonal = DMSO / cross = Dioxane)
- Well text gold "TFA" (odd cols) / blue "−H⁺" (even cols) → Acid

### Reagents to Purchase

| Reagent | Priority | Reason |
|---------|----------|--------|
| **TFA (trifluoroacetic acid, ≥99%)** | **Essential** | Only Brønsted acid needed; absent from all 74 kit entries |
| Acetic acid / p-TsOH | High | Alternative acids for Round 2 acid-strength sweep |
| K₂HPO₄ / NaH₂PO₄ buffer | Medium | Aqueous-acid Minisci conditions; Water present (kit #73) but no buffer |
| [Ir(dFppy)₂(bpy)]PF₆ | Medium | Intermediate E* between rows C and D |
| Thiophenol (PhSH) | Low | HAT catalyst; entirely absent from kit |

---

## Audit Summary

### Minisci Campaign Audit (independent subagent, 2026-09-16)

Three MAJOR findings were identified and corrected before the GitHub push:

| # | Finding | Status |
|---|---------|--------|
| M1 | Inventory table summed to 72, not 74 — 2 monodentate N-ligand entries (2,6-lutidine idx 44; pyridine idx 54) omitted | **Fixed** — row added to table |
| M2 | E* comparison used wrong inequality direction in phase_02 verification (">" instead of "more negative than") | **Fixed** — sign convention corrected throughout |
| M3 | Original acid search used Python substring `'C(=O)O'` which silently fails for TFA (RDKit canonical: `O=C(O)C(F)(F)F`) | **Fixed** — SMARTS recheck `012_acid_smarts_recheck.py` run; 0 hits confirmed; phase_01 documentation updated |

The TFA-is-absent conclusion was correct regardless of the search method defect (TFA was genuinely absent).

### Push Phase Audit (independent subagent, 2026-09-16)

Six MAJOR findings; no CRITICAL findings:

| # | Finding |
|---|---------|
| M1 | No phase document records the push procedure — push not reproducible from phase report |
| M2 | 48 files committed vs. ~27 workspace files — 14-file surplus unexplained |
| M3 | `phase_01_minisci_reagent_inventory.md` committed 4× with different sizes; canonical version not identified |
| M4 | `phase_01_parse_hte_edelris_sdf…md` committed under a phase-02 directory on GitHub |
| M5 | `008_classify_all_74_reagents…py` (broken acid check) committed without inline defect annotation |
| M6 | Workspace listing used as evidence had CSV in wrong subdirectory |

Scientific content is intact; push succeeded. M3 (multiple versions of the same document) is the most actionable item for repo cleanliness.

---

## Files Produced

| File | Description |
|------|-------------|
| `plate_map_round1.png` | Campaign 1 plate map (4×6, 160 dpi) |
| `plate_map_minisci_round1.png` | Campaign 2 plate map (4×6, 160 dpi) |
| `source/001–006_*.py` | Campaign 1 scripts: parse, classify, design, dispensing table |
| `source/007–012_*.py` | Campaign 2 scripts: parse, classify, design, SMARTS recheck |
| `results/003_extract_all_molecules_their_properties.csv` | 72-row reagent table (Campaign 1) |
| `phase_01_reagent_inventory.md` | Campaign 1 Phase 1 report |
| `hte_campaign_round1.md` | Campaign 1 full report |
| `phase_01_minisci_reagent_inventory.md` | Campaign 2 Phase 1 report (corrected) |
| `phase_02_minisci_campaign_design.md` | Campaign 2 Phase 2 report (corrected) |
| `audit_minisci_phase01_phase02.md` | Independent audit of Campaign 2 phases 1–2 |
| `audit_push_phase_github.md` | Independent audit of GitHub push phase |
| `session_summary.md` | This file |

---

## GitHub

- **Repository:** RSA-Edelris/RaycaBio
- **Branch:** main
- **Commit:** `da27bb16986df591bf9ee27227f2998f198e71d9`
- **Path:** `studies/f6f5499f-1482-471b-83bf-16ad6d46a50c/runs/max-6c649ef204/`
- **Files committed:** 48
