
## Objective

Retrieve public KinomeScan (competition binding panel) data for BX912 and its structural analogues from ChEMBL and cross-reference against the 43-kinase docking panel.

---

## Data Sources Searched

| Source | ChEMBL Document | Outcome |
|:---|:---|:---|
| GSK PKIS — Nanosyn kinase panel | CHEMBL1961873 | 0 hits for any of 105 analogs |
| GSK PKIS — UNC Frye lab | CHEMBL2007661 | 0 hits |
| SGC KinomeScan assays | CHEMBL4507330 | 0 hits |
| ChEMBL full activity pull (all assay types) | All documents | 10 activities for BX912 (CHEMBL3916849) |

**Conclusion:** No public KinomeScan (468-kinase competition binding) panel data exists in ChEMBL for BX912, EL2003A, EL2003A-A2U1, EL2003A-A4U1, EL5001A, or EL5003A, or for any of their 105 structural analogues (Tc ≥ 0.40). These are novel proprietary compounds absent from the PKIS, PKIS2, and SGC KinomeScan public datasets.

---

## BX912 Experimental Kinase Data in ChEMBL

BX912 is deposited in ChEMBL as CHEMBL3916849 (no preferred name; identified by exact SMILES match, Tc = 1.000). It has 10 total activities in ChEMBL, of which 7 are kinase-relevant:

| Target | Measurement | Value | Units | pIC50/pKd | Assay |
|:---|:---|:---:|:---:|:---:|:---|
| Aurora kinase A | Kd | 13.79 | nM | **7.86** | CHEMBL3885761 (SPR kinetics) |
| Aurora kinase A | kon | 3,181,000 | M⁻¹s⁻¹ | — | CHEMBL3885761 |
| Aurora kinase A | k_off | 0.04098 | s⁻¹ | — | CHEMBL3885761 (kd/kon = 12.9 nM) |
| MARK4 | IC50 | 338 | nM | **6.47** | CHEMBL5046588 |
| MARK3 | IC50 | 3,333 | nM | **5.48** | CHEMBL5046587 |
| TBK1 | IC50 | 2,327 | nM | **5.63** | CHEMBL5046589 |
| TBK1 | % inhibition | 90 | % | — | CHEMBL5046631 (single-point confirmation) |

Non-kinase activities: HDAC6 % inhibition at two concentrations (41% and 5%), HepG2 cytotoxicity IC50 = 3,300 nM.

---

## Cross-Reference: Experimental vs. Docking vs. Inference

| Kinase | Experimental pIC50 | Docking pIC50 (KD2) | Inferred pIC50 | Agreement |
|:---|:---:|:---:|:---:|:---|
| AurA | **7.86** (Kd) | 7.40 | 7.86 | Docking −0.46; inference exact ✓ |
| MARK4 | **6.47** (IC50) | not in panel | 6.40 | Inference −0.07 ✓ |
| MARK3 | **5.48** (IC50) | not in panel | 5.96 | Inference +0.48 (overestimate) |
| TBK1 | **5.63** (IC50) | not in panel | 6.99 | Inference +1.36 (overestimate) |

Key finding: The docking panel does not cover MARK3/4 or TBK1. These are experimentally confirmed off-targets of BX912 at low-moderate affinity (pIC50 5.5–6.5), validated here for the first time against the project compounds.

---

## Experimental AurA Binding Kinetics

From assay CHEMBL3885761 (SPR):

| Parameter | Value |
|:---|:---|
| Kd | 13.79 nM |
| kon | 3.18 × 10⁶ M⁻¹s⁻¹ |
| k_off | 0.04098 s⁻¹ |
| Kd (from rate constants) | k_off / kon = 12.9 nM |

The Kd computed from kinetic constants (12.9 nM) is consistent with the directly reported Kd (13.79 nM), confirming measurement quality. This corresponds to pKd = 7.86, which the similarity inference recovered exactly (driven by BX912 itself at Tc = 1.0).

---

## Recommendations for Experimental KinomeScan

No public panel data is available for these compounds. To generate KinomeScan data:

1. **DiscoverX KinomeScan 468-kinase panel** — competition binding, 1 µM screen; ~2–3 weeks turnaround. Would identify all kinases with >35% displacement of control compound. Confirmatory Kd follow-up for hits at >65% displacement.
2. **Nanosyn/Reaction Biology 96- or 384-kinase panel** — enzymatic IC50 format; complementary to competition binding for activation-loop-open kinases (e.g., CDK4 which is inactive in KinomeScan).
3. **Minimum viable screen:** Given the inference data, prioritise AurA (confirmed), MARK4 (confirmed), JAK3/BTK/BMX/IKKε (inferred, EL-series), STK17A (inferred, EL5001A/EL5003A). A targeted biochemical 10-kinase panel covering these would provide experimental grounding for the inference results at substantially lower cost than a full KinomeScan.

---

## Limitations

1. Only BX912 (CHEMBL3916849) has any experimental kinase data; the EL-series compounds have none.
2. The 4 experimental data points cover AurA, MARK3/4, and TBK1 — a very limited slice of kinome space.
3. PKIS/PKIS2 and SGC KinomeScan compounds are not close analogs of our series; no inference from those panel datasets is possible.
4. DiscoverX/Eurofins KinomeScan raw data for BX912 may exist in the literature (GSK PKIS screening was performed on commercial compound collections) but was not located in ChEMBL, BindingDB, or the documents searched.

---

## Output Artifacts

| File | Description |
|:---|:---|
| `chembl_activities_raw.parquet` | 1,294 raw activities for 105 analogs |
| `similarity_inference_matrix.csv` | Cross-compound inferred pIC50 table |
| `bx912_docking_vs_inference_vs_exp.png` | Three-way comparison bar chart |

---

## Verification

| Claim | Method | Result |
|:---|:---|:---|
| BX912 = CHEMBL3916849 | ChEMBL similarity search SMILES exact match | Tc = 1.000 ✓ |
| AurA Kd = 13.79 nM | ChEMBL activity record CHEMBL3885761 | 13.79 nM ✓ |
| kon/koff consistent | k_off / kon = 0.04098 / 3.181×10⁶ = 12.9 nM | Consistent with Kd ✓ |
| MARK4 IC50 = 338 nM | ChEMBL activity record CHEMBL5046588 | 338 nM ✓ |
| PKIS 0 hits | `document_chembl_id=CHEMBL1961873, molecule_chembl_id__in=<105 IDs>` | 0 ✓ |
| SGC KinomeScan 0 hits | `document_chembl_id=CHEMBL4507330` | 0 ✓ |
