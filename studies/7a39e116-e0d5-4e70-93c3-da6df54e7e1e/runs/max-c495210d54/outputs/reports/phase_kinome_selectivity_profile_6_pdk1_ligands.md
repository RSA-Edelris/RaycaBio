## Overview

**Date:** 2026-09-07 | **Tool:** KinaseDocker2 (AutoDock Vina-GPU + DNN pIC50, PLEC fingerprint) | **Kinases profiled:** 43

Six PDK1-directed ligands (BX912, EL2003A, EL2003A-A2U1, EL2003A-A4U1, EL5001A, EL5003A) were docked against 43 kinases covering the AGC family in full and a targeted clinical panel across CMGC, TK, TKL, CAMK, STE, CK1, and Other groups. The goal was to identify clinically relevant off-targets, determine which are common to the whole series versus compound-specific, and rank the six compounds by selectivity.

---

## Inputs

| Item | Detail |
|:---|:---|
| Compound SMILES | `ligand_smiles.json` — 6 compounds |
| Docking tool | KinaseDocker2 via platform dispatch |
| Structural database | KLIFS (via KinaseDocker2) — representative X-ray structures |

---

## Methods

KinaseDocker2 accepts `kinase_families` (all KLIFS structures in a family) or `accessions` (UniProt IDs). The AGC family was profiled in one call (1397 s, ~25 structures). Full-family calls for other groups exceeded the 1800 s MCP timeout, so the remainder of the panel was profiled using `accessions`-based batches capped at 7 UniProt IDs per call (~980–1143 s each).

**Docking runs**

| Run | Family / accessions | Structures | Time (s) |
|:---|:---|:---|:---|
| PDK1_AGC | AGC family | ~25 | 1397 |
| PDK1_probe5 | CDK2, GSK3B, EGFR, ABL1, AURKA | 14 | 1143 |
| PDK1_batch2 | CDK1, CDK4, CDK6, ERK1, ERK2, p38α, JNK1 | 11 | 981 |
| PDK1_batch3 | KDR, FGFR1, MET, SRC, BTK, JAK2, FLT3 | 19 | 1044 |
| PDK1_batch4 | CHEK1, CHEK2, PLK1, MEK1, BRAF, CK1d | 11 | 598 |

`avg_score` (mean DNN pIC50 of top-3 Vina poses) was used throughout. Where a kinase had multiple KLIFS structures, the maximum `avg_score` per compound–kinase pair was used. **pIC50 interpretation:** ≥7.0 = strong (≤100 nM); 6.5–7.0 = moderate; scorer uncertainty ≈ ±0.3.

---

## Results

### PDK1 engagement

| Compound | PDK1 pIC50 |
|:---|:---|
| EL5003A | 6.93 |
| EL2003A-A4U1 | 6.91 |
| BX912 | 6.89 |
| EL5001A | 6.87 |
| EL2003A-A2U1 | 6.86 |
| EL2003A | **6.47** (weakest — requires potency rescue) |

### Universal off-target: AurA only

AurA (Aurora A kinase, O14965) is the only kinase with predicted pIC50 ≥ 6.90 in all six compounds:

| Compound | AurA pIC50 |
|:---|:---|
| BX912 | 7.40 |
| EL2003A-A2U1 | 7.40 |
| EL2003A-A4U1 | 7.40 |
| EL2003A | 7.36 |
| EL5003A | 7.13 |
| EL5001A | 6.98 |
| **Mean** | **7.28 (+0.46 above PDK1 mean)** |

AurA engagement is scaffold-level (hinge pharmacophore) and cannot be removed by peripheral substitution.

### Top 10 off-targets by mean pIC50

| Kinase | Mean pIC50 | Δ vs PDK1 | CV | Family |
|:---|:---|:---|:---|:---|
| AurA | 7.28 | +0.46 | 0.025 | Other |
| FLT3 | 7.04 | +0.22 | 0.021 | TK |
| JAK2 | 7.04 | +0.21 | 0.014 | TK |
| FGFR1 | 7.03 | +0.20 | 0.028 | TK |
| MET | 6.96 | +0.13 | 0.016 | TK |
| CDK4 | 6.95 | +0.13 | 0.029 | CMGC |
| BRAF | 6.95 | +0.12 | 0.034 | TKL |
| EGFR | 6.95 | +0.12 | 0.008 | TK |
| ROCK2 | 6.94 | +0.12 | 0.031 | AGC |
| p38α | 6.93 | +0.11 | 0.014 | CMGC |

### Compound-specific off-targets (max ≥ 7.05, std ≥ 0.12; AurA excluded — classified as universal)

| Kinase | Max pIC50 | Top compound | Structural driver |
|:---|:---|:---|:---|
| FGFR1 | 7.32 | EL2003A-A4U1 | CF₃ hydrophobic back-pocket |
| BRAF | 7.28 | EL2003A-A4U1 | CF₃ hydrophobic back-pocket |
| CDK4 | 7.23 | EL2003A-A4U1 | CF₃ expansion |
| ROCK2 | 7.23 | EL2003A-A2U1 | ortho-methyl tolyl |
| FLT3 | 7.21 | EL5003A | cyclopentyl ring geometry |
| PKACa | 7.08 | EL5001A | linear ethylene linker |
| BTK | 7.06 | EL2003A-A2U1 | ortho-methyl tolyl |
| ABL1 | 7.05 | EL2003A-A2U1 | ortho-methyl tolyl |

### Selectivity ranking (best to worst)

1. **EL5001A** — PKACa and JAK2 co-top at +0.21/+0.20; narrowest off-target profile
2. **EL5003A** — best PDK1 (6.93); FLT3 the main concern (+0.28)
3. **BX912** — clean except AurA (+0.51)
4. **EL2003A-A2U1** — ROCK2/BRAF/BTK driven by ortho-methyl tolyl
5. **EL2003A-A4U1** — worst selectivity; CF₃ drives FGFR1, BRAF, CDK4 above PDK1
6. **EL2003A** — weakest PDK1 (6.47); AurA gap +0.89; not a selective PDK1 tool compound

### Clinical significance

| Off-target | Clinical risk | Addressable by SAR? |
|:---|:---|:---|
| AurA | Mitotic arrest, neutropenia, mucositis | No — scaffold-level |
| FLT3 | Myelosuppression; opportunity in FLT3-ITD AML | Partially |
| JAK2 | Anaemia, thrombocytopenia, immune effects | No — scaffold-level |
| FGFR1 | Hyperphosphataemia, retinal toxicity | Yes — remove CF₃ |
| BRAF | Paradoxical MAPK activation, secondary SCC | Yes — remove CF₃ |
| CDK4 | Neutropenia, G1 arrest | Yes — remove CF₃ |
| EGFR | Dermatological effects | No — scaffold-level |
| ROCK1/2 | Blood-pressure reduction | Partially |
| PKACa | cAMP pathway disruption | Yes — modify linker |

---

## Recommendations

1. **AurA biochemical counter-screen mandatory** for the whole series (predicted IC50 ~50 nM is pharmacologically active).
2. **EL2003A needs potency rescue** before further profiling — PDK1 pIC50 6.47, ROCK1/2 dominant.
3. **Remove CF₃ from EL2003A-A4U1** — simultaneously worsens FGFR1, BRAF, CDK4; BRAF paradoxical activation is the most serious clinical concern.
4. **Advance EL5001A and EL5003A** as primary candidates pending AurA wet-lab confirmation.
5. **Evaluate FLT3 dual engagement** (EL2003A, EL5003A) in FLT3-ITD AML cell lines — potential therapeutic opportunity.

---

## Limitations

1. DNN scorer uncertainty ≈ ±0.3 pIC50 — differences < 0.2 should not be over-interpreted.
2. 43 of ~500 kinases covered — full kinome not scanned; STE, full CMGC, full TK not included.
3. Static docking only — no MD relaxation; conformation-dependent selectivity not fully explored.
4. No cellular PK correction — values are biochemical IC50 predictions.

---

## Output Files

| File | Description |
|:---|:---|
| `kd2_out/PDK1_AGC/docking_results/PDK1_AGC_vina_results.csv` | AGC family raw results |
| `kd2_out/PDK1_probe5/docking_results/PDK1_probe5_vina_results.csv` | CDK2, GSK3B, EGFR, ABL1, AurA |
| `kd2_out/PDK1_batch2/docking_results/PDK1_batch2_vina_results.csv` | CMGC core |
| `kd2_out/PDK1_batch3/docking_results/PDK1_batch3_vina_results.csv` | TK panel |
| `kd2_out/PDK1_batch4/docking_results/PDK1_batch4_vina_results.csv` | CHEK1/2, PLK1, MEK1, BRAF, CK1d |
| `kinome_selectivity_matrix.csv` | 6×43 aggregated pIC50 matrix |
| `kinome_heatmap.png` | Full heatmap — 43 kinases × 6 compounds |
| `kinome_per_compound.png` | Per-compound top-8 off-targets vs. PDK1 |

## Figures

![Full kinome heatmap — 43 kinases × 6 compounds, RdYlGn, PDK1 first](kinome_heatmap.png)

![Per-compound top-8 off-targets versus PDK1 (white dashed line)](kinome_per_compound.png)

## Verification

| Claim | Verification method | Result |
|:---|:---|:---|
| 475 total rows across 5 CSVs | `len(pd.concat([...]))` | 475 ✓ |
| 43 unique kinases | `df_all['Kinase'].nunique()` | 43 ✓ |
| All 6 SMILES map to compound names | `df_all[compound.isna()]` empty | ✓ |
| EL2003A PDK1 = 6.47 | `pivot['PDK1']['EL2003A']` | 6.473 ✓ |
| AurA universal (all ≥ 6.90) | `(pivot['AurA'] >= 6.90).all()` | True ✓ |
| AurA only universal off-target | Checked all 43 columns | AurA only ✓ |
| EL2003A-A4U1 FGFR1 = 7.32 | `pivot.loc['EL2003A-A4U1','FGFR1']` | 7.323 ✓ |
| Matrix CSV exists (4,216 bytes) | `os.path.getsize(...)` | 4,216 ✓ |
| Heatmap exists (256 KB) | `os.path.getsize(...)` | 262,432 bytes ✓ |
| Per-compound figure (176 KB) | `os.path.getsize(...)` | 181,066 bytes ✓ |
| Independent audit | `reports/audit_kinome_selectivity_profile.md` | 0 critical, 0 major, 3 minor ✓ |
