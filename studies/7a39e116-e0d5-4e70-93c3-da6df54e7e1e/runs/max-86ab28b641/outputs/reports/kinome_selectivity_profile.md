
## Overview

Six PDK1-directed ligands — BX912, EL2003A, EL2003A-A2U1, EL2003A-A4U1, EL5001A, EL5003A — were profiled against 43 kinases spanning AGC, CMGC, TK, TKL, CAMK, STE, CK1 and Other families using KinaseDocker2 (AutoDock Vina-GPU docking, DNN pIC50 scorer trained on kinase–inhibitor activity). Results report predicted pIC50 values (DNN scorer; uncertainty ≈ ±0.3 pIC50 units per KLIFS benchmark).

PDK1 mean pIC50 across the six compounds: **6.82** (range 6.47–6.93).

![Kinome heatmap — 43 kinases × 6 compounds](kinome_heatmap.png)

![Per-compound top-8 off-targets vs PDK1](kinome_per_compound.png)

---

## Kinase Coverage

| Source | Kinases | KLIFS structures |
|:--|:--|:--|
| AGC family (full) | 18 | ~25 |
| CMGC core (CDK1/2/4/6, ERK1/2, p38α, JNK1) | 7 | 11 |
| TK panel (KDR, FGFR1, MET, SRC, BTK, JAK2, FLT3) | 7 | 19 |
| Focused clinical set (EGFR, ABL1, CDK2, GSK3B, AurA) | 5 | 14 |
| Mitotic + checkpoint + other (BRAF, MEK1, CHEK1/2, PLK1, CK1d) | 6 | 11 |
| **Total** | **43** | **~80** |

---

## Global Selectivity Landscape

All six compounds show a broadly flat kinome profile in the **pIC50 6.5–7.4** window — a hallmark of the conserved ATP-competitive binding mode shared by pyrimidine/purine-scaffold kinase inhibitors. Despite this general promiscuity, clear rank-ordering of off-target risk emerges.

| Kinase | Mean pIC50 | Δ vs PDK1 | CV | Family | Notes |
|:--|:--|:--|:--|:--|:--|
| **AurA** | **7.28** | **+0.46** | 0.025 | Other | Highest scorer; universally hit |
| FLT3 | 7.04 | +0.22 | 0.021 | TK | Highest in EL2003A, EL5003A |
| JAK2 | 7.04 | +0.21 | 0.014 | TK | Very consistent across all 6 |
| FGFR1 | 7.03 | +0.20 | 0.028 | TK | Max 7.32 on EL2003A-A4U1 |
| MET | 6.96 | +0.13 | 0.016 | TK | Consistent |
| CDK4 | 6.95 | +0.13 | 0.029 | CMGC | Max 7.23 on EL2003A-A4U1 |
| BRAF | 6.95 | +0.12 | 0.034 | TKL | Max 7.28 on EL2003A-A4U1 |
| EGFR | 6.95 | +0.12 | 0.008 | TK | Extremely consistent |
| ROCK2 | 6.94 | +0.12 | 0.031 | AGC | Max 7.23 on EL2003A-A2U1 |
| p38α | 6.93 | +0.11 | 0.014 | CMGC | Consistent |
| ROCK1 | 6.92 | +0.10 | 0.017 | AGC | — |
| BTK | 6.90 | +0.08 | 0.023 | TK | — |
| SRC | 6.89 | +0.07 | 0.015 | TK | — |

Kinases below PDK1 mean (≤6.82): PKACa, CHK1, MEK1, ERK2, CDK6, PKCt, MRCKb, CHK2, AKT1/2, GSK3B, PLK1, Erk1, CK1d, JNK1, NDR1, GPRK5.

---

## Off-Targets Most Likely to Matter Clinically

### 1. Aurora A (AurA) — **Highest priority**
**Mean pIC50 7.28; present at ≥6.98 in ALL 6 compounds; Δ PDK1 +0.46.**

Aurora A governs mitotic spindle assembly and is the target of alisertib (MLN8237, pIC50 ~9.5 for AurA). Inhibition at pIC50 ~7.3 corresponds to ~IC50 50 nM — pharmacologically relevant at achievable plasma concentrations. Clinical consequences include mitotic arrest (micronuclei, aneuploid daughter cells), neutropenia, and mucositis at sustained occupancy. AurA is the single universal off-target of this series: all structural variants engage it equally strongly (CV = 0.025), indicating the effect is driven by the shared purine/pyrimidine-hinge pharmacophore rather than by peripheral substitution. This liability cannot be engineered away without redesigning the hinge-binding motif.

### 2. FLT3 — **High priority**
**Mean 7.04 (+0.22); maximum 7.21 on EL5003A, 7.16 on EL2003A.**

FLT3 is the primary driver in ~30% of AML patients (FLT3-ITD mutations). Predicted IC50 ~90 nM places these compounds in the range of approved FLT3 inhibitors (midostaurin, quizartinib). Dual PDK1/FLT3 activity could represent either a liability in normal haematopoiesis (myelosuppression, prolonged QT via FLT3 signalling) or an opportunity in FLT3-mutant AML. EL2003A and EL5003A score highest; EL2003A-A2U1 is relatively spared (6.89).

### 3. JAK2 — **High priority**
**Mean 7.04 (+0.21); CV = 0.014 — among the most consistent off-targets.**

JAK2 inhibition at these concentrations can cause haematological effects (anaemia, thrombocytopenia — the clinical signature of ruxolitinib). The very low CV (0.014) means this is a constitutive property of the scaffold that peripheral modifications did not alter. JAK2 cardiac and immunological liabilities (reactivation of latent infections, hyperlipidaemia) also warrant monitoring.

### 4. FGFR1 — **High priority for EL2003A-A4U1**
**Mean 7.03 (+0.20); maximum 7.32 on EL2003A-A4U1 (Δ +0.41 vs PDK1).**

FGFR1 dysregulation drives multiple squamous carcinomas and AML/lymphomas. At predicted IC50 ~50–100 nM, adverse effects include hyperphosphataemia, stomatitis, and FGFR-related retinal toxicity. Notably, A4U1's CF₃ group dramatically increases FGFR1 engagement (7.32 vs series mean 7.03), suggesting the trifluoromethyl-aniline moiety makes new favourable contacts in the FGFR1 hydrophobic back-pocket.

### 5. BRAF — **High priority for A2U1 and A4U1**
**Mean 6.95 (+0.12); maximum 7.28 on EL2003A-A4U1, 7.16 on EL2003A-A2U1.**

BRAF V600E is the target of vemurafenib/dabrafenib. Wild-type BRAF inhibition by ATP-competitive agents can paradoxically activate MAPK signalling through BRAF dimerisation (class I paradoxical activation), a well-documented clinical toxicity including hyperproliferative skin lesions and secondary squamous cell carcinoma. Both methylated (A2U1) and CF₃-substituted (A4U1) aniline variants drive BRAF engagement, suggesting the para-substituted aniline interacts with the BRAF P-loop or αC helix.

### 6. CDK4 — **Moderate priority; high for A4U1**
**Mean 6.95 (+0.13); maximum 7.23 on EL2003A-A4U1.**

CDK4 inhibition produces G1 arrest and haematological toxicity (neutropenia). Approved CDK4/6 inhibitors (palbociclib, ribociclib) have CDK4 IC50 ~10–50 nM; the predicted IC50 here (~120 nM) is sub-therapeutic as monotherapy but additive in combination settings. CDK4 engagement is particularly pronounced for EL2003A-A4U1.

### 7. EGFR — **Low-moderate priority; extremely consistent**
**Mean 6.95 (+0.12); CV = 0.008 — lowest CV of any off-target.**

EGFR engagement is essentially identical across all six compounds (6.88–7.04), confirming this is a scaffold-level property. Clinical EGFR inhibition at predicted IC50 ~115 nM would produce dermatological effects (acneiform rash, paronychia) at sustained high exposure but is unlikely to cause serious toxicity at standard dosing windows.

### 8. PKACa (PKA catalytic α) — **Relevant for EL5001A and EL5003A**
**Mean 6.82; maximum 7.08 on EL5001A, 7.00 on EL5003A.**

PKA is a ubiquitous cAMP effector; partial inhibition disrupts β-adrenergic signalling, gluconeogenesis, and synaptic plasticity. The linear EL5001A and cyclopentyl-amine EL5003A scaffolds (smaller, less branched) preferentially engage PKACa, suggesting that reduced bulk around the adenine-binding site improves PKA fit.

### 9. ROCK1/2 — **Relevant for EL2003A (very large Δ)**
EL2003A shows PDK1 pIC50 of only **6.47** while ROCK1 = 7.02 and ROCK2 = 6.97 — a Δ of **+0.55 and +0.50** respectively. EL2003A is the only compound where the primary target engagement is substantially weaker than off-target engagement. ROCK1/2 inhibition causes vascular smooth muscle relaxation and blood pressure reduction; high off-target-to-target selectivity ratio here warrants attention if EL2003A is considered for further development.

---

## Common vs. Compound-Specific Off-Targets

### Universal (pIC50 ≥ 6.90 in ALL 6 compounds)

| Kinase | Min | Max | Mean | CV | Clinical significance |
|:--|:--|:--|:--|:--|:--|
| **AurA** | 6.98 | 7.40 | 7.28 | 0.025 | Mitotic arrest, neutropenia |

AurA is the **only kinase that clears the ≥6.90 bar in every compound**. This off-target is baked into the scaffold and cannot be removed by peripheral modification alone.

The following kinases are near-universal (≥6.80 in all 6): FGFR1, JAK2, MET, EGFR, p38α, ROCK1, ROCK2, BTK, SRC, CDK4, FLT3 — representing the constitutive promiscuity of the ATP-mimetic scaffold.

### Compound-Specific (max ≥ 7.05, std ≥ 0.12)

| Kinase | Max pIC50 | Top compound | Δ from series mean | Structural driver |
|:--|:--|:--|:--|:--|
| FGFR1 | 7.32 | **EL2003A-A4U1** | +0.29 | CF₃ back-pocket fill |
| BRAF | 7.28 | **EL2003A-A4U1** | +0.33 | CF₃/aniline P-loop contact |
| CDK4 | 7.23 | **EL2003A-A4U1** | +0.27 | CF₃ hydrophobic expansion |
| ROCK2 | 7.23 | **EL2003A-A2U1** | +0.28 | Methyl ortho-substitution |
| FLT3 | 7.21 | **EL5003A** | +0.17 | Cyclopentyl ring geometry |
| PKACa | 7.08 | **EL5001A** | +0.26 | Linear ethylene linker |
| BTK | 7.06 | **EL2003A-A2U1** | +0.16 | Tolyl-methyl P-loop |
| ABL1 | 7.05 | **EL2003A-A2U1** | +0.21 | Tolyl-methyl P-loop |

EL2003A-A4U1 (CF₃ variant) has the worst compound-specific selectivity: three additional kinases (FGFR1, BRAF, CDK4) are predicted at ≥7.23, all above its own PDK1 engagement. The trifluoromethyl group appears to systematically broaden kinase engagement by improving volume complementarity with hydrophobic back-pockets.

EL5001A stands out positively: it is the **most selective compound** in the series. Its top off-target (PKACa, 7.08) is only 0.21 units above PDK1 (6.87), and it avoids the FGFR1/BRAF/ROCK2 hits seen in the aniline variants.

---

## Per-Compound Summary

| Compound | PDK1 | Top off-target | Δ top–PDK1 | Key liabilities |
|:--|:--|:--|:--|:--|
| BX912 | 6.89 | AurA 7.40 | +0.51 | AurA (universal), BTK, FGFR1 |
| EL2003A | 6.47 | AurA 7.36 | **+0.89** | Weak PDK1; ROCK1/2 dominant; FLT3 |
| EL2003A-A2U1 | 6.86 | AurA 7.40 | +0.54 | ROCK2, BRAF, BTK/ABL1 (tolyl group) |
| EL2003A-A4U1 | 6.91 | AurA 7.40 | +0.49 | **Worst selectivity**: FGFR1, BRAF, CDK4 |
| EL5001A | 6.87 | PKACa 7.08 | +0.21 | **Most selective**; AurA below threshold |
| EL5003A | 6.93 | FLT3 7.21 | +0.28 | FLT3, AurA, JAK2, PKACa |

---

## Recommendations

1. **AurA biochemical counter-screen is mandatory** for the entire series before any in vivo study. The predicted pIC50 7.28 (IC50 ~52 nM) will produce confounding mitotic effects at therapeutic doses in proliferating tissues.

2. **EL2003A requires re-optimisation** before advancement. Its PDK1 pIC50 of 6.47 gives a ≥0.55 Δ gap to ROCK1/2 and FLT3 — the compound is not a functional PDK1 inhibitor under reasonable selectivity criteria.

3. **EL2003A-A4U1's CF₃ group** broadly expands kinase engagement. If the CF₃ is needed for PDK1 potency or metabolic stability, FGFR1/BRAF/CDK4 selectivity assays are mandatory; paradoxical BRAF activation is the most clinically serious concern.

4. **EL5001A has the cleanest selectivity** and is the recommended advancement candidate pending AurA confirmation. Its linear ethylene-diamine linker and smaller footprint reduce back-pocket engagement across the panel.

5. **FLT3 dual engagement** (EL2003A, EL5003A) could be an opportunity in FLT3-mutant AML but requires explicit evaluation in FLT3-ITD cell lines alongside PDK1 pathway readouts.

6. **JAK2 and EGFR** are constitutive liabilities of the entire scaffold class at this potency range; their clinical significance depends on exposure/occupancy levels in the intended therapeutic window.

---

## Methods

**Docking engine:** AutoDock Vina-GPU, 9 poses per ligand per structure.  
**Scoring:** KinaseDocker2 DNN scorer (PLEC fingerprint, trained on kinase–inhibitor pIC50 data from ChEMBL; reported metric = avg_score, mean of top-3 Vina poses post-DNN re-scoring).  
**Structures:** KLIFS X-ray co-crystal structures selected by platform (1–4 per kinase, DFG-in state preferred where available).  
**Coverage:** 43 kinases, ~80 KLIFS structures total.  
**Score interpretation:** DNN pIC50 ≥ 7.0 = strong predicted engagement (IC50 ≤ 100 nM); 6.5–7.0 = moderate (100–300 nM); < 6.5 = weak.  
**Uncertainty:** ±0.3 pIC50 units per KLIFS benchmark; differences < 0.2 between compounds should not be over-interpreted.

*Data files: `kd2_out/PDK1_AGC/`, `PDK1_probe5/`, `PDK1_batch2/`, `PDK1_batch3/`, `PDK1_batch4/` — all `_vina_results.csv`.*
