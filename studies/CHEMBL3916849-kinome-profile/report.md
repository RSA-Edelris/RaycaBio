
## Compound

**CHEMBL3916849** is an experimental 2-aminopyrimidyl *N*-aryl urea with a 4-bromopyrimidine core and an imidazolylethylamine sidechain.

| Property | Value |
|---|---|
| SMILES | `O=C(Nc1cccc(Nc2ncc(Br)c(NCCc3cnc[nH]3)n2)c1)N1CCCC1` |
| MW (freebase) | 471.36 |
| ALogP | 3.99 |
| HBD / HBA | 4 / 6 |
| PSA | 110.86 Å² |
| Solubility (measured) | 173 µM |
| Peff (Caco-2, measured) | 1.39 × 10⁻⁷ cm/s |
| Max phase | Pre-clinical (no indication assigned) |

The pharmacophore — anilinopyrimidine hinge-binder + distal urea + imidazolylethylamine DFG-region group — is consistent with a type-I or type-I½ protein kinase inhibitor scaffold.

---

## Primary Target

**Aurora kinase A (AURKA, CHEMBL4722, UniProt O14965)** is the confirmed primary target.

| Measurement | Value | Assay |
|---|---|---|
| Kd | **13.79 nM** | SPR (CHEMBL3885761) |
| kₒₙ | 3.18 × 10⁶ M⁻¹s⁻¹ | SPR |
| kₒff | 0.041 s⁻¹ | SPR |
| Residence time (1/kₒff) | ~24 s | derived |

The kinetics suggest rapid binding, moderate residence — consistent with a reversible ATP-competitive inhibitor.

---

## Confirmed Secondaries (ChEMBL experimental data)

| Target | ChEMBL ID | Measurement | Window vs AURKA Kd |
|---|---|---|---|
| MARK4 | CHEMBL5754 | IC50 = **338 nM** | 24× |
| TBK1 | CHEMBL5408 | IC50 = **2327 nM** | 169× |
| MARK3 | CHEMBL5600 | IC50 = **3333 nM** | 241× |
| HDAC6 | CHEMBL1865 | 41% inhibition (single conc.) | non-quantified |
| HepG2 cytotox | — | IC50 = 3300 nM | 241× |

HDAC6 inhibition was assay-variable (41% vs 5% in two separate formats) — treat as potential but unconfirmed.

---

## DeepPurpose CNN-CNN Kinome Scan

**Method.** 80 ChEMBL kinase-drug binding pairs (pChEMBL-labelled Ki/Kd, human, single-protein, assay type B), stratified by pChEMBL bin (5–6, 6–7, 7–8, 8–9, ≥9; 16 pairs each). CNN drug encoder + CNN protein encoder. 15 epochs, Adam LR 0.001, batch 32. Protein sequences truncated to 300 AA. 40 clinically curated kinases scored as prediction pairs.

| Model stat | Value |
|---|---|
| Training pairs | 56 (70%) |
| Unique training proteins | 12 |
| Unique training compounds | 76 |
| Test MSE | 2.265 |
| Test RMSE | **1.505 pChEMBL** |
| Prediction range across 40 kinases | 7.779 – 7.834 pChEMBL (**Δ = 0.055**) |
| Training set mean pChEMBL | 7.532 |

**Interpretation.** A discriminatory model should produce ≥ 1–2 pChEMBL units of spread across a diverse kinome panel (corresponding to ≥10–100-fold selectivity differences). The observed Δ = 0.055 (< 1.14-fold) indicates the model has **collapsed to the training mean** and provides no discriminatory signal. This is a mean-regression failure, not a genuine flat selectivity profile.

---

## Applicability Domain Assessment

### Chemical space
| Metric | Value | AD threshold | Verdict |
|---|---|---|---|
| Max Tanimoto (Morgan r=2, 2048-bit) to any training compound | 0.211 | ≥ 0.40 | **OUTSIDE** |
| Training compounds with Tc ≥ 0.40 | 0 | — | — |
| Training compounds with Tc ≥ 0.30 | 0 | — | — |

CHEMBL3916849 is a novel scaffold with no close analogues in the training set. The nearest training compound (Tc = 0.211) shares the urea partial substructure but differs in the kinase-binding hinge motif.

### Protein space
| Metric | Value | AD threshold | Verdict |
|---|---|---|---|
| Unique training protein sequences | 12 | — | — |
| Prediction kinases with k5-mer overlap ≥ 0.40 | 1 (EGFR) | — | 1/40 inside |
| Mean max overlap across 40 kinases | 0.026 | — | 39/40 OUTSIDE |

Only EGFR (P00533) matches a training protein sequence (CHEMBL203). Its predicted value is 7.810 pChEMBL (~15.5 nM).

### Combined verdict

| Condition | EGFR | All other 39 kinases |
|---|---|---|
| Protein in training | ✓ | ✗ |
| Compound in chemical AD | ✗ | ✗ |
| **Combined AD** | **OUTSIDE** | **OUTSIDE** |

**Zero of 40 predictions satisfy both conditions simultaneously. No DeepPurpose prediction for CHEMBL3916849 can be trusted as a quantitative estimate.** All 40 values reflect extrapolation from a mean-regressed, low-data model.

The RMSE of 1.505 pChEMBL (≈30-fold) on the test set represents the best-case uncertainty even *within* the training domain. Outside it, uncertainty is larger.

---

## Off-Targets Most Likely to Matter Clinically

Ranked by: (1) confidence of engagement at therapeutic exposure, (2) clinical consequence if engaged, (3) status of evidence.

### 1. AURKB (Aurora kinase B, Q96GD4) — **Critical gap, highest priority**
- **Evidence**: No direct measurement. Not in ChEMBL for this compound.
- **Basis for concern**: AURKB shares ~70% kinase-domain sequence identity with AURKA. No selective AURKA inhibitor scaffold avoids AURKB without intentional design. Alisertib (the clinical AURKA inhibitor) required extensive engineering to achieve AURKA/AURKB selectivity, and even then shows some AURKB activity.
- **Clinical consequence**: AURKB inhibition causes polyploidy and chromosome missegregation via loss of error-correction at the kinetochore. It produces a distinct safety and efficacy signature vs. AURKA alone — polyploid tumour cells can emerge and evade death, and haematological/GI toxicity pattern differs.
- **This is the single most important off-target to measure before further compound progression.**

### 2. MARK4 (MAP/microtubule affinity-regulating kinase 4, Q96L34) — **Confirmed, moderate concern**
- **Evidence**: IC50 = 338 nM (measured, ChEMBL5754). 24× selectivity window over AURKA Kd.
- **Clinical consequence**: MARK4 phosphorylates tau at S262/S356, promoting tau detachment from microtubules. At pharmacologically relevant free concentrations — especially in CNS-penetrant contexts — MARK4 engagement could perturb tau biology (Alzheimer's-relevant pathway). MARK4 also feeds into mTOR and Hippo signalling.
- **A 24× biochemical window is not sufficient to declare MARK4 safe without cellular engagement data.** The measured Peff suggests the compound does cross membranes.

### 3. TBK1 (TANK-binding kinase 1, Q9UHD2) — **Confirmed, lower immediate concern**
- **Evidence**: IC50 = 2327 nM biochemical (ChEMBL5046589); separately, 90% inhibition observed in a single-concentration assay (ChEMBL5046631) — this discrepancy requires attention.
- **Clinical consequence**: TBK1 is the central signalling kinase downstream of STING and TRIF, driving type I IFN production and NF-κB activation. Inhibition suppresses innate antiviral and antitumour immune responses. In the oncology context, TBK1 inhibition could impair immune surveillance; in immunocompromised patients already receiving cytotoxic therapy this is a compounding risk.
- **The 90% inhibition datapoint at unspecified concentration suggests potency may be underestimated by the IC50 assay. Resolve this discrepancy before dismissing TBK1.**

### 4. CDK1/CDK2 — **Unconfirmed, mechanistic concern**
- **Evidence**: No direct measurement for this compound. DeepPurpose predictions (CDK1: 7.825, CDK2: 7.789 pChEMBL) are OOD artifacts.
- **Basis for concern**: The anilinopyrimidine scaffold overlaps with CDK inhibitor chemotype space. CDK1 and AURKA co-regulate mitotic entry; co-inhibition would generate a combinatorial mitotic blockade that confounds phenotypic interpretation of AURKA-selective biology and could exacerbate toxicity.
- **Priority: medium — measure on any kinase panel.**

### 5. EGFR (P00533) — **Unconfirmed, structural argument only**
- **Evidence**: No measurement. Model prediction: 7.810 pChEMBL (only kinase with protein-in-training-domain support, but compound chemically OOD).
- **Basis for concern**: Anilinopyrimidines bind the EGFR hinge. The 3-position bromine and imidazolylethyl sidechain do not match canonical EGFR inhibitor pharmacophores, but the partial scaffold overlap merits a single datapoint.
- **Priority: low — include at 1 µM in kinase panel, do not pursue unless positive.**

---

## Three Assays to Settle the Rest

### Assay 1 — DiscoverX KINOMEscan S(35) or Eurofins SelectScreen (468 kinases, 1 µM single-point)

**What it answers**: Every kinase in the human kinome at a single screening concentration. Expresses as % inhibition vs. DMSO. Identifies all secondaries ≥ 25% inhibition for follow-up Kd determination.

**Why**: Directly replaces the failed DeepPurpose prediction. At 1 µM (~72× AURKA Kd), AURKA should show ≥ 97% inhibition (positive control). AURKB, CDK1/2, EGFR/FGFR, PLK1, and any unanticipated targets will be detected simultaneously. This is the standard post-hit kinase derisking experiment for any kinase inhibitor program.

**Readout**: % inhibition at 1 µM; Kd follow-up for any hit ≥ 35%.

---

### Assay 2 — AURKB, CDK1, CDK2, PLK1 quantitative Kd (SPR or radiometric 10-point Kᵢ)

**What it answers**: Quantitative affinity for the four kinases most likely to cause mechanistic off-target effects that would confound or harm a clinical candidate.

- **AURKB**: Is there genuine selectivity or co-inhibition? What is the AURKA/AURKB window?
- **CDK1/CDK2**: Does the compound contribute a CDK component to observed anti-proliferative activity?
- **PLK1**: Polo-like kinase 1 inhibition causes monopolar spindles — a distinct from AURKA phenotype that could confound mechanistic studies.

**Why not rely on KINOMEscan alone**: Single-concentration screening will detect a ≥10 nM hit at 1 µM, but quantitative Kd or Ki is needed for structure–activity guidance and therapeutic index calculation. SPR gives kₒₙ/kₒff as a bonus.

**Readout**: Kd (SPR, direct binding) or Kᵢ (radiometric ³³P-ATP, 10-point). Run in parallel with AURKA as reference control.

---

### Assay 3 — NanoBRET cellular target engagement for MARK4 and TBK1 (HEK293 or HeLa, 2-h pre-incubation)

**What it answers**: Whether the biochemical selectivity windows for MARK4 (24×) and TBK1 (169×) hold in intact cells, accounting for intracellular compound concentration, protein binding, and competing endogenous ATP.

**Why cellular TE is needed**:
- Biochemical IC50s are measured at low, artificial ATP concentrations. Cellular [ATP] is 1–5 mM, which right-shifts apparent IC50 for ATP-competitive inhibitors.
- Permeability is measured (Peff = 1.39 × 10⁻⁷ cm/s) but intracellular accumulation is not.
- For MARK4: the 24× window is narrow enough that modest permeability differences could close it inside cells.
- For TBK1: the 90% inhibition datapoint (CHEMBL5046631) is unexplained and could indicate the biochemical IC50 is an artefact of assay conditions. NanoBRET will resolve this in a cellular context.

**Format**: NanoBRET kinase engagement assay (Promega), MARK4-NanoLuc and TBK1-NanoLuc constructs in HEK293T. Tracer displacement 8-point dose-response, 0.3 nM – 10 µM. Report BRET50 and compare to AURKA NanoBRET EC₅₀ as reference.

---

## Summary Table

| Off-target | Evidence | Clinical risk | AD status (model) | Action |
|---|---|---|---|---|
| AURKB | None | High — polyploidy, hematotox | OOD | **Assay 2** (immediate) |
| MARK4 | IC50 338 nM | Moderate — tau, mTOR | OOD | **Assay 3** (cellular TE) |
| TBK1 | IC50 2327 nM, 90% inhib discrepancy | Moderate — innate immunity | OOD | **Assay 3** (cellular TE) |
| CDK1/2 | None | Moderate — mechanistic confound | OOD | **Assay 1** (KINOMEscan) |
| EGFR | None | Low | Protein only (compound OOD) | **Assay 1** (KINOMEscan) |
| MARK3 | IC50 3333 nM | Low | OOD | Monitor |
| HDAC6 | 41% inhib (one assay) | Low (separate mechanism) | OOD | Confirm if program continues |

---

## Caveats

1. **DeepPurpose predictions are uninformative for this compound.** The model collapsed to the training mean (prediction Δ = 0.055 pChEMBL across 40 kinases). All 40 scores reflect the training set average, not compound-specific binding. A useful kinome-wide DTI model would require: (a) training on a larger, kinase-focused dataset (e.g., full ChEMBL kinase binding data, ~420k pairs); (b) a compound in the training chemical space (Tc ≥ 0.4 to at least one training compound); or (c) a pre-trained foundation model (e.g., MolTrans or Binding DB-trained MPNN) that is not retrained from scratch on 80 pairs.

2. **AURKA Kd vs. MARK4 IC50 comparison is imprecise.** Kd (equilibrium) and IC50 (functional, ATP-competitive) are not directly comparable. The apparent IC50 for an ATP-competitive inhibitor scales with [ATP]/Kₘ. At cellular [ATP] ~2 mM (Kₘ ~20–100 µM for most kinases), biochemical IC50 may underestimate cellular potency shift by 10–100×. True cellular selectivity window for MARK4 is unknown.

3. **HDAC6 signal.** HDAC6 is not a kinase. 41% inhibition in one assay, 5% in another suggests either assay interference or weak, conditional binding. This requires a clean concentration-response in a validated HDAC6 fluorescence assay before interpretation.
