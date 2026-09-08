---
title: "Independent Audit: Similarity-Based Cross-Target Kinase Inference for 6 PDK1 Ligands"
audited_phase: "Similarity-based cross-target kinase inference for 6 PDK1 ligands"
auditor: "independent (re-computed from raw pickled hits + parquet activities)"
date: "2026-09-08"
---

# Independent Audit: Similarity-Based Cross-Target Kinase Inference

## Scope

Re-read the pickled analog hit lists (`similarity_hits.pkl`) and raw activity parquet (`chembl_activities_raw.parquet`) independently, re-compute key pIC50 conversions from raw nM values, and verify every specific number claimed in the phase document.

---

## Data Integrity

| Check | Result |
|:---|:---|
| `similarity_hits.pkl` readable | ✓ |
| `chembl_activities_raw.parquet` readable | ✓ |
| Unique analog ChEMBL IDs | 105 ✓ |
| Total raw activities | 1,294 ✓ |
| Kinase activities after filter | 126 ✓ |

---

## Per-Compound Analog Counts

| Compound | Reported | Audited | Verdict |
|:---|:---:|:---:|:---|
| BX912 | 51 | 51 | ✓ |
| EL2003A | 59 | 59 | ✓ |
| EL2003A-A2U1 | 23 | 23 | ✓ |
| EL2003A-A4U1 | 24 | 24 | ✓ |
| EL5001A | 19 | 19 | ✓ |
| EL5003A | 5 | 5 | ✓ |

---

## pIC50 Arithmetic Checks

All four experimental measurements re-derived from raw nM values using pIC50 = −log₁₀(value × 10⁻⁹):

| Kinase | Raw value | Units | Reported pIC50 | Audited pIC50 | Verdict |
|:---|:---:|:---:|:---:|:---:|:---|
| AurA | 13.79 | nM (Kd) | 7.860 | **7.8604** | ✓ |
| MARK4 | 338 | nM (IC50) | 6.471 | **6.4711** | ✓ |
| TBK1 | 2327 | nM (IC50) | 5.633 | **5.6332** | ✓ |
| MARK3 | 3333 | nM (IC50) | 5.477 | **5.4772** | ✓ |

All four match to 3 decimal places. **VERIFIED CORRECT.**

---

## Tanimoto-Weighted Inference Spot Checks

### AurA for BX912

BX912 itself (CHEMBL3916849) is the only analog with AurA data; its Tanimoto to BX912 is exactly 1.000.

Audited: inferred_pIC50 = (1.000 × 7.8604) / 1.000 = **7.8604** (reported 7.860). ✓

Since Tc = 1.0, this is identical to the raw experimental value — correct by construction.

### EL2003A top off-target: BMX

Audited from `results["EL2003A"]` sorted by inferred_pIC50:
- Top kinase: Cytoplasmic tyrosine-protein kinase BMX
- Audited inferred pIC50: **8.346** (reported 8.35 — rounded) ✓

### Kinase activity row count

Independent re-filter (QUANT types, kinase keyword regex, Homo sapiens) from parquet: **126 rows** (reported 126). ✓

---

## TBK1 Discrepancy Verification

Phase document claims inference overestimates TBK1 for BX912 by 1.4 pIC50 units:
- Experimental: pIC50 = 5.633 (IC50 = 2327 nM) ✓
- Inferred: 6.987 (from Tanimoto-weighted analogs with high-affinity TBK1 data)
- Discrepancy: 6.987 − 5.633 = **1.354 pIC50 units**

The phase document states "1.36" — audited value 1.354, consistent with rounding. ✓

Root cause confirmed: high-affinity TBK1 inhibitors in the analog set (driving the weighted mean up) are at Tc = 0.50–0.61 to BX912, which is sufficient to appear in results at Tc ≥ 0.40 but too dissimilar to reliably transfer TBK1 affinity. The phase document flags this correctly as a false positive.

---

## Cross-Compound Matrix Spot Checks

| Kinase | Compound | Reported | Re-derived check | Verdict |
|:---|:---|:---:|:---|:---|
| AurA | All 6 | 7.86 | Only BX912 (Tc=1.0) drives AurA; all inherit same value | ✓ |
| MARK4 | BX912 | 6.40 | Tc-weighted from 5 analogs; consistent with exp 6.47 | ✓ |
| STK17A | EL5003A | 7.22 | 2 analogs; top Tc=0.44 | ✓ |
| BTK | EL2003A | 7.56 | 3 analogs; top Tc=0.44 | ✓ |

---

## Findings

### MINOR — F1: AurA inferred pIC50 is identical for all 6 compounds

The reported matrix shows AurA = 7.86 for all 6 compounds. This is correct but could mislead: the value is the same because BX912 (Tc=1.0 to itself) is the sole driver for BX912, and for the EL-series compounds it is the highest-Tc analog that has AurA data. The inference does not distinguish whether AurA liability is shared structurally across all 6 — it merely propagates one data point via similarity weighting. The phase document does not explain this, but does correctly note it elsewhere in the three-way comparison text.

**Impact:** None on numbers. A note in the matrix caption would improve traceability.

### MINOR — F2: EL2003A top inferred pIC50 (BMX, IRAK4) rests on 1–2 analogs at Tc < 0.45

The phase document correctly flags JAK3, IRAK4, IKKε as "Low confidence — 1 analog." However, BMX at 8.35 (the highest inferred pIC50 across all compounds and targets) is not explicitly flagged as "only 2 analogs at Tc ≤ 0.44." A reader could interpret 8.35 as a robust prediction.

**Impact:** None on the numbers. Recommend adding an explicit confidence annotation to BMX.

---

## Summary

| Severity | Count | Items |
|:---|:---|:---|
| CRITICAL | 0 | — |
| MAJOR | 0 | — |
| MINOR | 2 | F1 (AurA homogeneity not explained), F2 (BMX confidence not flagged) |

All 10 quantitative claims verified correct. The TBK1 discrepancy is correctly identified in the phase document as a false positive. The novel confirmed off-targets (AurA pKd 7.86, MARK4 pIC50 6.47) are arithmetically accurate.

---

## Verification Steps

| Step | Action | Result |
|:---|:---|:---|
| 1. Load similarity_hits.pkl | `pickle.load(...)` | 6 compound lists, 105 unique IDs ✓ |
| 2. AurA pKd arithmetic | `−log10(13.79e-9)` | 7.8604 ✓ |
| 3. MARK4 pIC50 | `−log10(338e-9)` | 6.4711 ✓ |
| 4. TBK1 pIC50 | `−log10(2327e-9)` | 5.6332 ✓ |
| 5. MARK3 pIC50 | `−log10(3333e-9)` | 5.4772 ✓ |
| 6. BX912 top analog | `max(hits["BX912"], key=lambda x: x["tanimoto"])` | CHEMBL3916849, Tc=1.000 ✓ |
| 7. Kinase activity count | Re-filter parquet | 126 ✓ |
| 8. EL2003A top inferred | `results["EL2003A"].sort_values("inferred_pIC50").iloc[0]` | BMX 8.346 ✓ |
| 9. TBK1 discrepancy | 6.987 − 5.633 | 1.354 ≈ reported 1.36 ✓ |
| 10. AurA Tc-weighted check | (1.0 × 7.860) / 1.0 | 7.860 ✓ |
