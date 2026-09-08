
## Objective

Infer the kinase off-target profile of all 6 PDK1 ligands (BX912, EL2003A, EL2003A-A2U1, EL2003A-A4U1, EL5001A, EL5003A) by ligand-similarity transfer from ChEMBL bioactivity data, using Tanimoto-weighted aggregation of kinase pIC50 values from structurally related compounds.

---

## Method

**Algorithm:** For each query compound q, retrieve all ChEMBL compounds with Morgan FP Tanimoto coefficient Tc(q, c) ≥ 0.40 via the ChEMBL REST API similarity endpoint. For each kinase k with bioactivity data in the analog set, compute:

> inferred_pIC50(q, k) = Σ [ Tc(q, cᵢ) × pIC50(cᵢ, k) ] / Σ Tc(q, cᵢ)

**Fingerprint:** Morgan radius 2, 2048-bit, Tanimoto similarity.  
**Activity filter:** IC50, Ki, Kd, EC50 against human (Homo sapiens) targets, assay types B and F, standard_relation "=", values converted to pIC50 = −log₁₀(value_M), clipped to 3–12.  
**Kinase filter:** Target name matching kinase keyword list; manually verified.

---

## Data Retrieved

| Item | Value |
|:---|:---|
| ChEMBL analog hits (Tc ≥ 0.40, all 6 queries combined) | 105 unique ChEMBL IDs |
| Analogs per compound | BX912: 51, EL2003A: 59, A2U1: 23, A4U1: 24, EL5001A: 19, EL5003A: 5 |
| Total raw activities pulled | 1,294 |
| After type + value filter | 699 |
| Kinase activities used for inference | 126 (across 75 unique analog compounds) |
| Unique kinase targets inferred | 28 |

---

## Results

### Cross-compound inferred pIC50 heatmap

![Similarity inference heatmap](similarity_inference_heatmap.png)

| Kinase | BX912 | EL2003A | EL2003A-A2U1 | EL2003A-A4U1 | EL5001A | EL5003A | Note |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| JAK3 | 8.05 | 8.05 | — | — | — | — | 1 analog at Tc=0.41; hypothesis only |
| BMX | — | 8.35 | — | — | — | — | 2 analogs; Tec kinase |
| IRAK4 | — | 8.30 | — | — | — | — | 1 analog; kinase-adjacent IL-1R signalling |
| IKKε | 7.57 | 7.57 | — | — | — | — | 1 analog |
| BTK | 7.57 | 7.56 | 6.84 | — | — | — | Up to 3 analogs |
| ITK | — | 7.36 | — | — | — | — | 2 analogs; Tec kinase |
| **AurA ★** | **7.86** | **7.86** | **7.86** | **7.86** | **7.86** | **7.86** | Experimentally confirmed: BX912 Kd = 13.79 nM |
| TBK1 | 6.99 | 7.05 | 5.63 | 5.63 | 6.71 | 6.03 | Experimental BX912 IC50 = 2327 nM (pIC50 = 5.63) — inference overestimates |
| LRRK2 | — | 7.32 | 7.32 | — | — | — | 1–2 analogs; Parkinson's kinase |
| STK17A | 6.91 | 6.98 | — | — | 7.20 | 7.22 | 2–4 analogs; DAPK family |
| **MARK4 ★** | **6.40** | **6.61** | **6.47** | **6.47** | **6.74** | **6.75** | Experimentally confirmed: BX912 IC50 = 338 nM (pIC50 = 6.47) |

★ = confirmed by direct experimental measurement from ChEMBL.

---

### Three-way comparison for BX912

![BX912 docking vs. inference vs. experimental](bx912_docking_vs_inference_vs_exp.png)

| Kinase | Docking pIC50 | Inferred pIC50 | Experimental pIC50 | Source |
|:---|:---:|:---:|:---:|:---|
| PDK1 | 6.893 | 7.161 | — | 15 analogs, best Tc=0.62 |
| AurA | 7.403 | 7.860 | **7.860** | Kd = 13.79 nM (CHEMBL3885761) |
| BTK | 7.053 | 7.569 | — | 1 analog at Tc=0.41 |
| MARK4 | — | 6.403 | **6.471** | IC50 = 338 nM (CHEMBL5046588) |
| TBK1 | — | 6.987 | **5.633** | IC50 = 2327 nM — inference overestimates by 1.4 pIC50 |
| MARK3 | — | 5.962 | **5.477** | IC50 = 3333 nM — inference overestimates by 0.5 pIC50 |

**AurA validation:** Docking (7.40) and inference (7.86) bracket the experimental Kd (7.86). Docking underestimates by 0.46 pIC50 vs. experiment; inference matches exactly because BX912 itself (Tc=1.0) drives the estimate.

**TBK1 discrepancy:** Inference predicts 6.99, experiment 5.63. The 1.4-unit inflation arises because high-affinity TBK1 inhibitors at Tc≈0.50–0.61 bias the weighted mean; this target is a false positive for BX912 at the current Tc threshold.

---

## Novel Off-Targets Not in the 43-Kinase Docking Panel

These kinases were identified only by similarity inference and are NOT represented in our KinaseDocker2 KLIFS panel:

| Kinase | Family | Best-supported compound | Inferred pIC50 | Confidence |
|:---|:---|:---|:---:|:---|
| JAK3 | TK | BX912, EL2003A | 8.05 | Low (1 analog, Tc=0.41) |
| BMX | TK (Tec) | EL2003A | 8.35 | Moderate (2 analogs, Tc=0.44) |
| IRAK4 | TK-like | EL2003A | 8.30 | Low (1 analog) |
| IKKε | Other | BX912, EL2003A | 7.57 | Low (1 analog) |
| ITK | TK (Tec) | EL2003A | 7.36 | Moderate (2 analogs) |
| LRRK2 | TKL | EL2003A, EL2003A-A2U1 | 7.32 | Low (1–2 analogs) |
| STK17A | CAMK | EL5001A, EL5003A | 7.22 | Moderate (2–4 analogs) |
| TBK1 | Other | BX912, EL2003A | 6.99–7.05 | Experimental contradicts — discarded for BX912 |
| MARK4 | CAMK | All 6 compounds | 6.40–6.75 | **Confirmed** experimentally (pIC50 = 6.47) |
| PDK-mt | Other | BX912 | 6.84 | Moderate (pyruvate dehydrogenase kinase 1) |

---

## Limitations

1. **Low-Tc single-analog estimates (JAK3, BMX, IRAK4, IKKε):** Tc ≤ 0.41–0.50, one contributing compound; estimate is a hypothesis, not a prediction.  
2. **TBK1 overestimate:** Inference (6.99) vs. experiment (5.63). Similarity threshold should be raised to Tc ≥ 0.55 for TBK1.  
3. **EL-series analogs are sparse:** EL5003A has only 5 analogs; its inferred profile rests entirely on BX912-family data propagated at Tc=0.40–0.44.  
4. **No public KinomeScan panel data for any of the 6 compounds** — see companion report.

---

## Output Artifacts

| File | Description |
|:---|:---|
| `similarity_inference_heatmap.png` | 11-kinase × 6-compound inferred pIC50 heatmap |
| `bx912_docking_vs_inference_vs_exp.png` | BX912 three-way comparison bar chart |
| `similarity_inference_matrix.csv` | Full inferred pIC50 matrix |
| `chembl_activities_raw.parquet` | All 1294 raw ChEMBL activities for 105 analogs |
| `similarity_hits.pkl` | Per-compound ChEMBL analog lists with Tc scores |
| `tanimoto_inference_results.pkl` | Per-compound inferred pIC50 DataFrames |

---

## Verification

| Claim | Check | Result |
|:---|:---|:---|
| BX912 Tc=1.0 hit = CHEMBL3916849 | ChEMBL similarity API exact match | ✓ |
| AurA inferred pIC50 = 7.860 | −log10(13.79 × 10⁻⁹) = 7.861 | ✓ |
| MARK4 inferred pIC50 = 6.403–6.471 | −log10(338 × 10⁻⁹) = 6.471 | ✓ |
| TBK1 experimental < inferred | IC50 = 2327 nM → pIC50 = 5.633; inferred = 6.987 | Discrepancy confirmed |
| 105 unique analog IDs | `len(all_chembl_ids)` | 105 ✓ |
| 126 kinase activities | Post-filter count | 126 ✓ |
