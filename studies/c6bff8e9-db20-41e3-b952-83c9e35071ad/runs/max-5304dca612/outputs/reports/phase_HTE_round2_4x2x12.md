
## What this phase produced

A complete HTE plate design for a second Buchwald-Hartwig C–N coupling campaign on the same substrate pair (5-bromoisoindolinone-glutarimide + N-Boc piperazine), using a 4 × 2 × 12 full factorial that saturates all 96 wells.

| Artefact | Path | Description |
|---|---|---|
| `HTE_platemap_round2_4x2x12.png` | figures/ | Colour-coded 96-well plate map |
| `HTE_BH_round2_4x2x12.md` | reports/ | Full rationale, factor tables, analysis plan |
| `006_plate_2_design_...py` | source/ | Grid construction script |
| `007_plt_subplots.py` | source/ | Rendering script |

---

## Design

| Axis | Factor | N levels | Levels |
|---|---|---|---|
| Columns 1–12 | Pd catalyst | 12 | BPG3, tBBG3, RuPG3, tBXG3, EPG3, SPG3, MorG3, APG3, GPG3, CatG3, dppf, **PEPPSI(NHC)** |
| Rows A–D | Base in dioxane | 4 | K₂CO₃, Cs₂CO₃, K₃PO₄, DIPEA |
| Rows E–H | Base in t-AmylOH | 4 | K₂CO₃, Cs₂CO₃, K₃PO₄, DIPEA |

Full factorial: 4 × 2 × 12 = **96 unique conditions**, 0 dedicated controls (reference Round 1).

---

## Key decisions and rationale

### Non-phosphine entry (requirement met)
Column 12: **PEPPSI** ([1,3-bis[2,6-bis(1-ethylpropyl)phenyl]-4,5-dichloro-imidazol-2-ylidene]Pd(II), CAS 1158652-41-5). NHC ligands are stronger σ-donors than phosphines and non-labile under turnover. For this electron-poor ArBr, oxidative addition is fast; C–N reductive elimination is rate-limiting. A stronger donor at Pd accelerates this step. No NHC entry existed in Round 1 — this is a chemotype orthogonal to the entire phosphine series.

Column 11: **dppf-Pd-G3** (CAS 1445086-28-1) — bidentate bisphosphine included as the only chelate entry; distinct bite angle (96°) vs. all monodentate G3 entries.

### New phosphine G3 entries (cols 7–10)
- **MorDalPhos Pd G3** — designed specifically for secondary amine C–N coupling
- **APhos Pd G3** — aminophos scaffold, higher electron density at Pd
- **GPhos Pd G3** — rigid gem-dialkyl backbone, unexplored on this substrate
- **cataCXium-A Pd G3** — non-biaryl aliphatic phosphine; distinct steric profile

### Base changes vs Round 1
- **Added:** K₂CO₃ (mildest inorganic, new) and DIPEA (homogeneous organic, new)
- **Dropped:** NaOtBu — deprotonates the glutarimide NH (pKa ≈ 11–13), causing wrong-regioisomer N-arylation side products
- **Retained:** Cs₂CO₃ and K₃PO₄ as cross-plate calibration anchors

### Solvent changes vs Round 1
- **Retained:** dioxane (benchmark / cross-plate reference)
- **Replaced** DMA and toluene with **t-AmylOH** (in kit, CAS 75-65-0): protic, no β-H elimination, may improve solubility of the polar isoindolinone substrate; untested in Round 1
- **Note:** if 2-MeTHF was purchased following Round 1 recommendations, replace t-AmylOH with 2-MeTHF

### Controls
4 × 2 × 12 = 96 fully saturates the plate. No dedicated control wells. Acceptable because Round 1 qualified the assay. Well B1 (BPG3/Cs₂CO₃/dioxane) appears in both Round 1 and Round 2 and serves as the cross-plate anchor; conversion must agree within ±15% before Round 2 data are interpreted.

---

## Analysis plan

1. Cross-plate calibration: well B1 vs. Round 1 H11/H12 positive controls (±15% tolerance)
2. Hit threshold: ≥20% conversion (same as Round 1)
3. NHC benchmark: PEPPSI (col 12) vs. best phosphine in each row
4. New-entry comparison: cols 7–10 vs. Round 1 champions in matching base/solvent rows
5. Solvent comparison: dioxane rows A–D vs. t-AmylOH rows E–H, paired by catalyst and base
6. ANOVA: same three-way model as Round 1; use Round 1 pure-error σ² (9 df from REP1–REP9) as the error reference

---

## Plate map

![HTE Round 2 plate map — 96-well, 4 bases × 2 solvents × 12 Pd catalysts](HTE_platemap_round2_4x2x12.png)
