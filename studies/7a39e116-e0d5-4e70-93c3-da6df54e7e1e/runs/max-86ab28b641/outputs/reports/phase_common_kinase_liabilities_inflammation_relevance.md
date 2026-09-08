
## Objective

Identify kinases with predicted or confirmed engagement across all six PDK1 ligands (BX912, EL2003A, EL2003A-A2U1, EL2003A-A4U1, EL5001A, EL5003A) by cross-referencing the 43-kinase docking panel with Tanimoto-weighted similarity inference. Assess whether any common kinases have established roles in inflammatory signalling.

---

## Methods

Two independent data sources were interrogated:

1. **KinaseDocker2 docking panel** (43 kinases, DNN pIC50, all 6 compounds): kinases were counted as "present for all 6" if no NaN appeared in any of the six compound rows. Kinases with mean pIC50 ≥ 6.9 across all 6 were considered to show meaningful consistent engagement (threshold = noise floor + 0.6 units of headroom).

2. **Tanimoto-weighted ChEMBL inference** (105 analogs, Tc ≥ 0.40): kinases inferred for all 6 compounds were those where every compound had at least one structurally similar analog with measured activity at that kinase.

Pivot rebuilt from raw CSVs: `df.groupby(['compound','Kinase'])['avg_score'].max().unstack('Kinase')`, shape (6, 43).

---

## Results

### Docking panel — kinases with mean pIC50 ≥ 6.9 across all 6 compounds

42 of 43 kinases have values for all 6 compounds (CDK6 missing for EL5001A only). Of these, 11 meet mean pIC50 ≥ 6.9:

| Kinase | Mean pIC50 | Min | Max | Present in all 6 |
|:---|:---:|:---:|:---:|:---:|
| AurA | 7.279 | 6.980 | 7.403 | ✓ |
| FLT3 | 7.042 | 6.870 | 7.213 | ✓ |
| JAK2 | 7.036 | 6.880 | 7.160 | ✓ |
| FGFR1 | 7.026 | 6.793 | 7.323 | ✓ |
| MET | 6.958 | 6.847 | 7.140 | ✓ |
| CDK4 | 6.951 | 6.683 | 7.230 | ✓ |
| BRAF | 6.948 | 6.690 | 7.277 | ✓ |
| EGFR | 6.947 | 6.880 | 7.040 | ✓ |
| ROCK2 | 6.943 | 6.567 | 7.227 | ✓ |
| p38α | 6.929 | 6.750 | 7.013 | ✓ |
| ROCK1 | 6.921 | 6.750 | 7.020 | ✓ |

### Similarity inference — kinases with inferred pIC50 for all 6 compounds

| Kinase | Mean pIC50 | Min | Max | Experimentally confirmed |
|:---|:---:|:---:|:---:|:---|
| Aurora kinase A | 7.860 | 7.860 | 7.860 | ★ BX912 Kd = 13.79 nM |
| MARK4 | 6.570 | 6.400 | 6.750 | ★ BX912 IC50 = 338 nM |
| TBK1 | 6.340 | 5.630 | 7.050 | Partial — BX912 exp = 5.63; inference overestimates |
| MARK3 | 5.840 | 5.480 | 5.960 | ★ BX912 IC50 = 3333 nM |

---

## Inflammation Involvement

Three of the eleven consistently-docked kinases are canonical inflammatory kinases:

### p38α (MAPK14) — major pro-inflammatory MAPK
- Activated by TNF-α, IL-1β, TLR ligands, and cellular stress
- Drives transcription and stabilisation of TNF-α, IL-1β, IL-6, IL-8, and COX-2 mRNA
- Central to RA, IBD, COPD, and sepsis pathology
- Docking pIC50 range 6.75–7.01 across all 6 compounds; minimum above noise floor
- Many clinical-stage p38α inhibitors have been developed (limited therapeutic success due to toxicity/rebound, but target validated)

### JAK2 — cytokine receptor signalling kinase
- Transmits signals from IL-6, IL-12, IL-23, IFN-γ, EPO, and TPO via STAT3/STAT5
- Elevated JAK2/STAT3 activity is a hallmark of chronic inflammatory and autoimmune disease (RA, myelofibrosis, SLE)
- Baricitinib (JAK1/2) approved for RA and COVID-19 pneumonia; ruxolitinib (JAK1/2) for myelofibrosis and GVHD
- Docking pIC50 range 6.88–7.16 across all 6 compounds — one of the strongest consistent off-target signals in the panel

### ROCK1 / ROCK2 — Rho-associated kinases
- Regulate actin cytoskeleton, inflammatory cell migration, and endothelial permeability
- ROCK2 specifically controls Th17 differentiation (IL-17, IL-21 production), relevant to RA, SLE, and MS
- ROCK inhibition (fasudil) reduces leukocyte recruitment and attenuates NF-κB signalling in multiple preclinical inflammatory models
- Docking pIC50 6.57–7.23 (ROCK2) and 6.75–7.02 (ROCK1) across all 6 compounds

### TBK1 (inference only) — innate immunity / interferon axis
- Activated by cGAS-STING, TLR3/4, and RIG-I; phosphorylates IRF3/IRF7 to drive IFN-α/β production
- Central to type I interferon-mediated inflammation (lupus, SLE, viral immune response)
- **Caveat:** experimental BX912 IC50 = 2327 nM (pIC50 = 5.63); inference overestimates by 1.4 pIC50 units due to high-affinity TBK1 inhibitors in the analog set at Tc = 0.50–0.61. The true TBK1 liability of this scaffold is weak (pIC50 ≤ 5.7), not moderate.

### Non-inflammatory common kinases (for completeness)
AurA, MARK3, MARK4: mitotic/cytoskeletal roles; MARK4 has emerging metabolic-inflammatory associations but is not a canonical inflammatory kinase. FLT3 influences dendritic cell development but is primarily a haematopoietic receptor. FGFR1, MET, EGFR, CDK4, BRAF: growth/proliferation axes with minimal direct inflammatory roles.

---

## Clinical Interpretation

The scaffold carries a three-kinase inflammatory polypharmacology pattern at pIC50 6.9–7.1: **p38α + JAK2 + ROCK1/2** are all consistently engaged across all 6 compounds above the DNN scorer noise floor. This has two possible framings:

**Liability:** Simultaneous modulation of three inflammatory pathways by a PDK1 inhibitor creates unpredictable immunomodulation. JAK2 inhibition in particular affects haematopoiesis (anaemia, thrombocytopenia). Off-target p38α and ROCK inhibition at these levels could contribute to on-study immune-related adverse events.

**Opportunity:** PDK1 + p38α co-inhibition is mechanistically interesting in cancers where both PDK1 (PI3K-AKT pathway) and p38α (stress response survival) drive tumour cell survival. PDK1 + JAK2 co-inhibition could be relevant in AML (where FLT3/JAK2 and PDK1 are co-activated) or in RA where both pathways are active. This deserves evaluation rather than reflexive optimisation away.

---

## Limitations

1. DNN scorer uncertainty ±0.3 pIC50; differences < 0.2 within the common-kinase set are not distinguishable.
2. Inference values for TBK1 are overestimates; experimental BX912 data shows only pIC50 = 5.63.
3. ROCK1/2 pIC50 for EL5001A (6.57) approaches the noise floor; the ROCK liability is clearest for EL2003A-A2U1/A4U1 (pIC50 ≥ 6.92).
4. No experimental data for EL-series compounds at any of the 11 common kinases; all EL-series conclusions rest on DNN prediction.

---

## Output Artifacts

| File | Description |
|:---|:---|
| `similarity_inference_heatmap.png` | Cross-compound inferred pIC50 heatmap (includes AurA, MARK4, TBK1) |
| `kinome_selectivity_matrix.xlsx` | Full 43-kinase × 6-compound docking pIC50 matrix |
| `similarity_inference_matrix.csv` | Tanimoto-weighted inferred pIC50 table |

---

## Verification

| Claim | Method | Result |
|:---|:---|:---|
| 42/43 docking kinases present for all 6 | `pivot.notna().all(axis=0).sum()` | 42 ✓ |
| AurA mean = 7.279 | `pivot["AurA"].mean()` | 7.279 ✓ |
| p38α min = 6.750 | `pivot["p38a"].min()` | 6.750 ✓ |
| JAK2 range 6.88–7.16 | `pivot["JAK2-b"].min(), .max()` | 6.880 / 7.160 ✓ |
| 4 inference kinases common to all 6 | `inf_mat.notna().all(axis=1).sum()` | 4 ✓ |
| AurA inference = 7.86 uniform | Single data point at Tc=1.0 drives all 6 | ✓ |
| TBK1 exp < inference for BX912 | BX912 IC50=2327 nM → 5.63 vs. inferred 6.99 | Discrepancy confirmed ✓ |
