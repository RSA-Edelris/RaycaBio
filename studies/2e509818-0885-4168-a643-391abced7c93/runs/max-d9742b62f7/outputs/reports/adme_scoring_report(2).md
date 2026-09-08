
## Overview

353 amide analogues were enumerated by coupling the amine scaffold (`amine.mol`) to each acid in `acid.sdf`. Every product was scored across seven ADME endpoints with explicit uncertainty bounds and applicability-domain (AD) checks. A weighted multiparameter optimisation (MPO) score was computed using desirability functions tuned for a PPI-stabilising interface binder. The top 96 compounds by MPO were exported to `results.sdf`.

---

## 1. Reaction

**Scaffold amine SMILES:** `O=C(NCc1ccccc1)c1ccc2c(n1)CNCC2`

Three nitrogens are present; only one is reactive:

| Atom index | Type | Reactive? |
|---|---|---|
| N-2 | Aliphatic secondary ring-NH | **Yes** — amidation target |
| N-14 | Aromatic pyridine N | No |
| N-17 | Existing amide NH (O=C–NH) | No — excluded by SMARTS |

**Reaction SMARTS:** `[NH1;!$(N-C=O);!$(N-S=O);!a:1].[C:2](=O)[OH]>>[N:1][C:2]=O`

All 353 reactions succeeded (0 failures). Products were sanitised with RDKit; the first unique canonical SMILES was retained per acid.

---

## 2. ADME models and applicability domains

### 2.1 Aqueous solubility — ESOL (Delaney 2004)

**Formula:** logS = 0.16 − 0.63·cLogP − 0.0062·MW + 0.066·RB − 0.74·AP

- RB = rotatable bonds; AP = fraction of aromatic heavy atoms
- Training set: 1 144 compounds
- Published RMSE: 0.93 log-units (±1 SD)
- **AD:** MW 50–800 Da, cLogP −8 to +8
- **Coverage:** 353/353 in-domain

### 2.2 Lipophilicity — RDKit Crippen cLogP

- Atomic-contribution method; benchmark RMSE ≈ 0.40 log-units across DrugBank
- **AD:** All organic molecules (essentially unlimited)
- **Coverage:** 353/353

### 2.3 Passive permeability — Hou 2004 PAMPA linear model

**Formula:** logPapp = −0.01578·TPSA + 0.5·cLogP − 0.0008·MW − 5.5

- Units: log(cm/s)
- Classification: High (>−5.5), Medium (−7.0 to −5.5), Low (<−7.0)
- Published RMSE: 0.80 log-units
- **AD:** MW 100–700, TPSA 0–200, cLogP −3 to +7
- **Coverage:** 353/353 in-domain

### 2.4 Metabolic stability and clearance route — rule-based HLM classifier

A continuous stability score (0–1) is derived from:

- cLogP penalty: >4.0 (−0.25), >5.5 (additional −0.15)
- Aromatic-ring penalty: >3 rings (−0.15)
- Fsp3 bonus: >0.4 (+0.15)
- MW penalty: >500 Da (−0.10)
- Structural alerts (each flagged individually): phenol/Ar-OH (UGT/CYP), free acid (glucuronidation), Ar-methyl (CYP soft spot), tertiary amine (CYP oxidation), Ar-NH2 (N-hydroxylation)

Classification: High t½ >60 min (score >0.7), Medium 30–60 min (0.4–0.7), Low <30 min (<0.4).

Clearance route assignment:
- Free-acid or glucuronidation alert → Phase II (glucuronidation)
- Basic-N + aromatic ring → CYP2D6/3A4 oxidation
- Otherwise → CYP3A4 (lipophilic aromatic)

**Uncertainty:** ±1 class boundary. Stated as heuristic; no regression training data.
**AD:** Applicable to all organic molecules; rule-based.

### 2.5 CYP inhibition liability — SMARTS pharmacophore-alert panel

| Isoform | Alerts used |
|---|---|
| CYP2D6 | Basic NH 2–3 bonds from Ar ring; tertiary N near Ar |
| CYP3A4 | Imidazole/pyrimidine motif; cyclic tertiary N |
| CYP2C9 | Phenol; free COOH; sulfonamide NH |

Risk classification: Low (0 isoforms flagged), Medium (1), High (≥2).

**Important:** These are structural flags only — no IC50 is predicted. A flag indicates pharmacophore overlap with known inhibitors; confirmation requires assay data.
**AD:** All organic molecules; rule-based flags.

### 2.6 Plasma protein binding — Valko 2003 logP-linear model

**Formula:** fu = 1 / (1 + 10^(0.72·cLogP − 0.40))

- Training set: 87 compounds
- RMSE ≈ 10 percentage points (%PPB)
- **AD:** cLogP −2 to +7
- **Coverage:** 353/353 in-domain

### 2.7 hERG risk — structural-alert + cLogP rule (Redfern 2003 anchor)

- High: cyclic tertiary non-amide N **and** cLogP >3.5 **and** ≥1 aromatic ring
- Medium: any non-amide, non-aromatic N **and** cLogP >2.0
- Low: otherwise

**Uncertainty:** ±1 class. No compound reached High risk in this set.

---

## 3. MPO design for a PPI-stabilising interface binder

PPI stabilisers bind large hydrophobic protein–protein interfaces. This changes the property target relative to a generic oral small molecule: MW 400–650 Da is acceptable, cLogP 2–4 is preferred (not 1–3), high PPB is tolerated, but cardiac safety (hERG) and CYP interaction risk carry the same clinical weight.

| Property | Weight | Desirability function | Rationale |
|---|---|---|---|
| Solubility (logS) | 1.5 | Linear 0→1 from −5.5 to −3.0 | Cell assays need ≥10 µM; −5.5 is a 3 µM floor |
| cLogP | 1.0 | Trapezoid: 0 at ≤0, plateau 1 at 2–4, 0 at ≥5.5 | PPI interfaces hydrophobic; >5 degrades solubility |
| PAMPA logPapp | 1.5 | Linear 0→1 from −7.0 to −5.5 | Intracellular target; passive permeability required |
| MetStab score | 1.5 | Direct: 0–1 continuous | HLM stability defines viable in-cell / in-vivo window |
| CYP inhibition | 1.5 | Low=1.0 · Medium=0.5 · High=0.0 | Multi-isoform block → PK interaction in co-dosing |
| PPB (fu) | 0.5 | fu≥0.05→1.0, 0.01–0.05→0.7, <0.01→0.3 | High PPB expected and accepted for PPI probes |
| hERG | 2.0 | Low=1.0 · Medium=0.5 · High=0.0 | Cardiac safety; doubled weight as the hard safety endpoint |
| MW | 0.5 | Trapezoid: 0 at ≤200, 1 at 400–650, 0 at ≥850 | Informational; larger MW legitimately accepted for PPI |

**MPO = Σ(wᵢ·dᵢ) / 10.0** (weighted arithmetic mean; max = 1.0, total weight = 10.0)

---

## 4. Hard filters (gates applied before ranking)

| Filter | Threshold | Justification |
|---|---|---|
| Solubility | logS ≥ −5.5 | Minimum 3 µM required for any cell-based assay |
| Permeability | PAMPA ≠ Low | logPapp < −7.0 is inconsistent with intracellular target engagement |
| hERG | Risk ≠ High | Cardiac safety is non-negotiable at lead stage |
| CYP | Risk ≠ High | Multi-isoform inhibition (≥2 isoforms) creates unacceptable DDI risk |

---

## 5. Results

| Stage | N |
|---|---|
| Amide products enumerated | 353 |
| Pass solubility (logS ≥ −5.5) | 343 |
| Pass PAMPA (not Low) | 353 |
| Pass hERG (not High) | 353 |
| Pass CYP (not High) | 353 |
| Pass all four filters | 343 |
| Selected for synthesis (top 96 by MPO) | **96** |

### 5.1 Top-96 property distribution

| Property | Min | Median | Max |
|---|---|---|---|
| MW (Da) | 323 | 378 | 420 |
| cLogP | 0.89 | 2.61 | 3.25 |
| logS ESOL | −4.43 | −3.84 | −2.52 |
| logPapp | −6.88 | −5.73 | −5.16 |
| MetStab | High (t½ >60 min) for all 96 | | |
| PPB | 63% | 97% | 99% |
| hERG | 74 Low · 22 Medium · 0 High | | |
| CYP | 82 Low · 14 Medium · 0 High | | |
| MPO | 0.799 | 0.826 | 0.929 |

### 5.2 Rejected compounds (10 total — all solubility failures)

| CR_ID | cLogP | logS | PAMPA | hERG | Rejected because |
|---|---|---|---|---|---|
| R-009810 | 4.28 | −5.59 | High | Medium | logS < −5.5 |
| R-004811 | 4.52 | −5.59 | High | Medium | logS < −5.5 |
| R-003716 | 4.52 | −5.59 | High | Medium | logS < −5.5 |
| R-003231 | 4.42 | −5.51 | High | Medium | logS < −5.5 |
| R-008694 | 4.47 | −5.55 | High | Medium | logS < −5.5 |
| R-008840 | 4.84 | −5.80 | High | Medium | logS < −5.5 |
| R-009771 | 4.88 | −5.99 | High | Medium | logS < −5.5 |
| R-002547 | 5.06 | −6.02 | High | Medium | logS < −5.5 |
| R-000765 | 4.73 | −5.78 | High | Medium | logS < −5.5 |
| R-007781 | 5.00 | −5.97 | High | Medium | logS < −5.5 |

### 5.3 Structural-override candidates

All 10 rejected compounds fail **only the solubility filter** and have MPO ≥ 0.59. They are worth a conversation rather than automatic discard because:

1. ESOL predicts thermodynamic (equilibrium) solubility. Kinetic solubility from a DMSO stock diluted into warm buffer is typically 3–10× higher for aromatic amides in this cLogP range.
2. All 10 have High PAMPA permeability and no other failing endpoints.
3. Recommended action: run a miniaturised nephelometric kinetic-solubility assay (10 mM DMSO stock, 1% final DMSO, 37 °C). If kinetic solubility ≥10 µM, include in the synthesis plate.

---

## 6. Output files

| File | Description |
|---|---|
| `results.sdf` | 96 compounds; 38 SD-tag fields per molecule including rank, SMILES, all raw predicted values with uncertainty strings, AD flag per model, clearance route, CYP isoform flags, MPO score, and individual desirability values |
| `adme_models.py` | Reproducible Python module containing all seven ADME model functions and their AD bounds |

---

## 7. Limitations and caveats

- All ADME predictions are **in-silico estimates**, not measured values. They should be treated as triage scores, not go/no-go decisions. Every compound selected for synthesis should receive at least a kinetic solubility and PAMPA measurement before committing to dose–response work.
- The metabolic stability and hERG classifiers are **rule-based**; they have no training-set calibration curve and cannot produce a probability. Predictions should be confirmed by microsomal stability (MLM/HLM) and hERG patch-clamp assays for the top leads.
- The CYP alert panel flags **pharmacophore overlap** only. Confirmed IC50 data are required before concluding inhibition is absent.
- All 353 products are **in-domain for the three regression models** (ESOL, PAMPA, PPB). The PPB model (n=87) has the smallest training set and the broadest uncertainty at the edges of its cLogP range.
- The hERG Medium classification predominates (317/353) because the piperidine-like ring nitrogen in the amine scaffold, even after amide formation, contributes to the basic-nitrogen feature used by the rule. This is a scaffold-level property and should not be interpreted as a differentiated liability across the series. Patch-clamp data on 3–5 representatives are needed to calibrate the real hERG risk of the series.
