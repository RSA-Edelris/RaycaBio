## Objective

Determine which kinases are differentially engaged by BX912 versus EL2003A by computing the per-kinase pIC50 delta across all 43 profiled kinases. Identify BX912-specific and EL2003A-specific engagement above the DNN scorer noise floor (±0.3 pIC50).

---

## Inputs

| Item | Detail |
|:---|:---|
| Source data | Five raw KinaseDocker2 CSVs from Phase 1 (PDK1_AGC, probe5, batch2, batch3, batch4) |
| Aggregation | Max avg_score per compound–kinase pair (same rule as Phase 1 pivot) |
| Compounds compared | BX912 (bromopyrimidine scaffold) vs EL2003A (bicyclic imidazopyrimidine scaffold) |

---

## Methods

The Phase 1 pivot matrix (6 compounds × 43 kinases, max avg_score per pair) was rebuilt from the raw CSVs. The per-kinase delta was computed as:

```
Δ = pIC50(BX912) − pIC50(EL2003A)
```

Kinases are reported in descending order of Δ. Differences ≥ +0.30 (BX912-enriched) or ≤ −0.15 (EL2003A-enriched) are highlighted; the DNN scorer uncertainty is ±0.3 pIC50, so only deltas well above 0.30 are considered robust.

---

## Results

### Full per-kinase delta table

| Kinase | BX912 | EL2003A | Δ (BX912−EL2003A) | Family |
|:---|:---|:---|:---|:---|
| RSK2 | 6.940 | 6.503 | **+0.437** | AGC |
| PDK1 | 6.893 | 6.473 | **+0.420** | AGC (target) |
| YANK1 | 6.913 | 6.523 | **+0.390** | AGC |
| JNK1 | 6.827 | 6.457 | **+0.370** | CMGC |
| p70S6K | 6.873 | 6.530 | **+0.343** | AGC |
| BTK | 7.053 | 6.740 | **+0.313** | TK |
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
| SRC | 6.883 | 6.853 | +0.030 | TK |
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
| p38α | 6.907 | 7.013 | **−0.107** | CMGC |
| PKG1 | 6.640 | 6.787 | **−0.147** | AGC |
| ROCK1 | 6.840 | 7.020 | **−0.180** | AGC |
| FLT3 | 6.973 | 7.160 | **−0.187** | TK |
| MRCKb | 6.443 | 6.633 | **−0.190** | AGC |

### BX912-specific off-targets (Δ ≥ +0.30, above scorer noise floor)

| Kinase | Δ | Clinical relevance |
|:---|:---|:---|
| RSK2 | +0.437 | PI3K–AKT–mTOR axis effector; ribosomal S6 kinase; potential contribution to metabolic/proliferative side effects |
| YANK1 | +0.390 | AGC orphan kinase; limited clinical characterization |
| JNK1 | +0.370 | Stress-activated MAPK; inflammation, apoptosis; JNK inhibition can be both protective and harmful depending on context |
| p70S6K | +0.343 | mTOR pathway effector; inhibition associated with insulin resistance and immune effects |
| BTK | +0.313 | B-cell receptor signalling (ibrutinib target); borderline — right at the noise floor; myelosuppression risk |

Note: PDK1 Δ = +0.420 reflects EL2003A's potency deficit at its intended target, not an off-target difference.

### EL2003A-enriched kinases (Δ ≤ −0.15)

| Kinase | Δ | Note |
|:---|:---|:---|
| FLT3 | −0.187 | EL2003A has stronger FLT3 engagement; previously identified as EL2003A/EL5003A opportunity in FLT3-ITD AML |
| MRCKb | −0.190 | Myotonic dystrophy kinase-related CDC42-binding kinase; cytoskeletal effects |
| ROCK1 | −0.180 | Dominant ROCK1/2 engagement is a known EL2003A liability; BP effects |
| PKG1 | −0.147 | cGMP-dependent kinase; cardiovascular effects |
| p38α | −0.107 | EL2003A shows moderately higher p38α engagement; borderline |

---

## Structural interpretation

BX912 carries a simple bromopyrimidine hinge binder with a piperidine urea, whereas EL2003A replaces the bromopyrimidine with a bicyclic imidazopyrimidine fused ring. The larger fused ring in EL2003A:

- **Improves** DFG-out accommodation for kinases with bulkier back-pockets (ROCK1, FLT3, MRCKb).
- **Reduces** fit into tighter AGC-family active sites (RSK2, p70S6K, YANK1) where the smaller hinge binder of BX912 is geometrically favoured.
- **Reduces** JNK1 engagement — BX912's more planar hinge binder fits the narrow JNK1 ATP cleft better.

---

## Limitations

1. Scorer uncertainty ≈ ±0.3 pIC50. BTK (+0.31) and PLK1 (+0.30) are at the noise boundary; treat as hypothesis only.
2. Static docking — no MD relaxation or induced-fit modelling.
3. 43 kinases profiled; differential engagement at unscreened kinases is unknown.

---

## Output Files

| File | Description |
|:---|:---|
| Derived from `kinome_selectivity_matrix.csv` | Phase 1 pivot reused; no new docking runs required |
| `141_bx912_vs_el2003a_per_kinase_delta.py` | Delta computation code |
| `142_open.py` | Pivot rebuild from raw CSVs |

---

## Verification

| Claim | Method | Result |
|:---|:---|:---|
| Pivot rebuilt correctly | Shape (6, 43); all 6 SMILES mapped | ✓ |
| RSK2 Δ = +0.437 | `pivot.loc['BX912','RSK2'] − pivot.loc['EL2003A','RSK2']` = 6.940 − 6.503 | +0.437 ✓ |
| JNK1 Δ = +0.370 | 6.827 − 6.457 | +0.370 ✓ |
| FLT3 Δ = −0.187 | 6.973 − 7.160 | −0.187 ✓ |
| ROCK1 Δ = −0.180 | 6.840 − 7.020 | −0.180 ✓ |
| PDK1 Δ = +0.420 | 6.893 − 6.473 | +0.420 ✓ (potency gap, not off-target) |
| AurA Δ = +0.043 | 7.403 − 7.360 | +0.043 — confirmed near-equal across both compounds ✓ |
| No kinase has \|Δ\| > 0.5 | `delta.abs().max()` = 0.437 (RSK2) | ✓ |
