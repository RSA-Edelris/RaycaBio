---
title: "Phase 1: Compare BX912 vs EL2003A kinase specificity"
study_id: "7a39e116-e0d5-4e70-93c3-da6df54e7e1e"
run_id: "max-7307d91685"
phase_index: 1
phase_id: "1"
phase_goal: "Compare BX912 vs EL2003A kinase specificity"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Compare BX912 vs EL2003A Kinase Specificity

## Objective

Determine which kinases are differentially engaged by BX912 versus EL2003A by computing the per-kinase pIC50 delta across all 43 profiled kinases. Identify BX912-specific and EL2003A-specific engagement above the DNN scorer noise floor (±0.3 pIC50).

---

## Inputs

| Item | Detail |
|:---|:---|
| Source data | Five raw KinaseDocker2 CSVs from Phase 1 kinome profiling (PDK1_AGC, probe5, batch2, batch3, batch4) |
| Compounds compared | BX912 (bromopyrimidine scaffold) vs EL2003A (bicyclic imidazopyrimidine scaffold) |
| Aggregation | Max avg_score per compound–kinase pair, consistent with Phase 1 pivot |

---

## Methods

The Phase 1 pivot matrix (6 compounds × 43 kinases) was rebuilt from the raw CSVs. The per-kinase differential was computed as:

```
Δ = pIC50(BX912) − pIC50(EL2003A)
```

Kinases were ranked by Δ descending. Cutoffs: Δ ≥ +0.30 = BX912-enriched (above noise floor); Δ ≤ −0.15 = EL2003A-enriched (approaching noise floor).

---

## Results

### Full per-kinase delta (BX912 − EL2003A, all 43 kinases)

| Kinase | BX912 | EL2003A | Δ | Family |
|:---|:---|:---|:---|:---|
| RSK2 | 6.940 | 6.503 | **+0.437** | AGC |
| PDK1 | 6.893 | 6.473 | **+0.420** | AGC (target — potency gap, not off-target) |
| YANK1 | 6.913 | 6.523 | **+0.390** | AGC |
| JNK1 | 6.827 | 6.457 | **+0.370** | CMGC |
| p70S6K | 6.873 | 6.530 | **+0.343** | AGC |
| BTK | 7.053 | 6.740 | **+0.313** | TK (borderline — at noise floor) |
| PLK1 | 6.733 | 6.437 | +0.297 | Other |
| FGFR1 | 7.043 | 6.793 | +0.250 | TK |
| CDK2 | 6.937 | 6.690 | +0.247 | CMGC |
| BRAF | 6.993 | 6.750 | +0.243 | TKL |
| Erk2 | 6.843 | 6.613 | +0.230 | CMGC |
| GPRK5 | 6.697 | 6.477 | +0.220 | AGC |
| GSK3B | 6.733 | 6.543 | +0.190 | CMGC |
| PKCt | 6.933 | 6.767 | +0.167 | AGC |
| PKCh | 6.587 | 6.453 | +0.133 | AGC |
| BARK1 | 6.473 | 6.353 | +0.120 | AGC |
| JAK2 | 6.980 | 6.880 | +0.100 | TK |
| PKCi | 6.613 | 6.517 | +0.097 | AGC |
| CHK1 | 6.740 | 6.643 | +0.097 | CAMK |
| CDC2 | 6.810 | 6.717 | +0.093 | CMGC |
| PKN1 | 6.807 | 6.717 | +0.090 | AGC |
| ABL1 | 6.827 | 6.737 | +0.090 | TK |
| PKACa | 6.660 | 6.587 | +0.073 | AGC |
| Erk1 | 6.460 | 6.400 | +0.060 | CMGC |
| KDR | 6.957 | 6.900 | +0.057 | TK |
| CDK4 | 7.010 | 6.967 | +0.043 | CMGC |
| AurA | 7.403 | 7.360 | +0.043 | Other |
| SRC | 6.883 | 6.853 | +0.030 | AGC |
| ROCK2 | 6.993 | 6.970 | +0.023 | AGC |
| MET | 6.907 | 6.890 | +0.017 | TK |
| MAP2K1 | 6.800 | 6.797 | +0.003 | STE |
| AKT2 | 6.557 | 6.560 | −0.003 | AGC |
| CDK6 | 6.847 | 6.853 | −0.007 | CMGC |
| EGFR | 6.880 | 6.893 | −0.013 | TK |
| CHK2 | 6.793 | 6.840 | −0.047 | CAMK |
| NDR1 | 6.537 | 6.593 | −0.057 | AGC |
| CK1d | 6.287 | 6.353 | −0.067 | CK1 |
| AKT1 | 6.560 | 6.653 | −0.093 | AGC |
| p38α | 6.907 | 7.013 | −0.107 | CMGC |
| PKG1 | 6.640 | 6.787 | −0.147 | AGC |
| ROCK1 | 6.840 | 7.020 | −0.180 | AGC |
| FLT3 | 6.973 | 7.160 | −0.187 | TK |
| MRCKb | 6.443 | 6.633 | −0.190 | AGC |

### BX912-specific off-targets (Δ ≥ +0.30, above scorer noise floor)

| Kinase | Δ | Clinical relevance |
|:---|:---|:---|
| RSK2 | +0.437 | PI3K–AKT–mTOR effector; metabolic/proliferative side effects |
| YANK1 | +0.390 | AGC orphan kinase; limited clinical characterisation |
| JNK1 | +0.370 | Stress MAPK; inflammation and apoptosis |
| p70S6K | +0.343 | mTOR pathway; insulin resistance, immune effects |
| BTK | +0.313 | B-cell signalling (ibrutinib target); at noise floor — hypothesis only |

### EL2003A-enriched kinases (Δ ≤ −0.15)

| Kinase | Δ | Note |
|:---|:---|:---|
| FLT3 | −0.187 | Potential FLT3-ITD AML opportunity; identified in Phase 1 kinome profile |
| MRCKb | −0.190 | Cytoskeletal; ROCK-adjacent effects |
| ROCK1 | −0.180 | EL2003A dominant ROCK liability (Phase 1) |
| PKG1 | −0.147 | Cardiovascular cGMP pathway |
| p38α | −0.107 | Stress kinase; borderline |

### AurA — shared by both

AurA Δ = +0.043 (BX912 7.403, EL2003A 7.360). The universal scaffold liability identified in Phase 1 is confirmed near-equal for both compounds; it is not addressable by the structural changes distinguishing BX912 from EL2003A.

---

## Structural interpretation

BX912 (bromopyrimidine hinge binder + piperidine urea) fits AGC kinases with tighter active sites better than EL2003A's larger bicyclic imidazopyrimidine core, explaining the BX912-enrichment across RSK2, p70S6K, and YANK1. EL2003A's expanded core favours DFG-out-accessible kinases (ROCK1, FLT3, MRCKb).

---

## Limitations

1. DNN scorer uncertainty ≈ ±0.3 pIC50; BTK (+0.31) and differences < 0.20 should not be over-interpreted.
2. No new docking runs performed — analysis derived entirely from Phase 1 pivot.
3. 43/~500 kinases covered.

---

## Output Artifacts

| File | Description |
|:---|:---|
| `141_bx912_vs_el2003a_per_kinase_delta.py` | Delta computation script |
| `142_open.py` | Pivot rebuild from raw CSVs |

---

## Verification

| Claim | Method | Result |
|:---|:---|:---|
| Pivot (6, 43) rebuilt correctly | `df_all.groupby(['compound','Kinase'])['avg_score'].max().unstack('Kinase').shape` | (6, 43) ✓ |
| RSK2 Δ = +0.437 | 6.940 − 6.503 | +0.437 ✓ |
| JNK1 Δ = +0.370 | 6.827 − 6.457 | +0.370 ✓ |
| p70S6K Δ = +0.343 | 6.873 − 6.530 | +0.343 ✓ |
| FLT3 Δ = −0.187 | 6.973 − 7.160 | −0.187 ✓ |
| ROCK1 Δ = −0.180 | 6.840 − 7.020 | −0.180 ✓ |
| AurA near-equal | 7.403 − 7.360 = +0.043 | ✓ |
| Max \|Δ\| | `delta.abs().max()` = 0.437 (RSK2) | ✓ |
| Independent audit | `reports/audit_compare_bx912_vs_el2003a_kinase_specificity.md` | 0 critical, 0 major, 2 minor ✓ |
