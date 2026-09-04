
## 1. Dataset Overview

| Parameter | Value |
|---|---|
| Total compounds in ASMS.sdf | 23,712 |
| Active (Hit P841 = Active) | 15 |
| Inactive | 23,697 |
| Activity metric | AS ratio (affinity-selected compound signal, protein-present vs. protein-absent) |
| Active AS ratio range | 0.0012 – 0.172 |
| Compound MW range (actives) | 353 – 550 Da |
| Retention time range (actives) | 1.00 – 1.32 min |

---

## 2. Structure Standardization

All 23,712 structures were processed through the following pipeline (RDKit 2023.9.6):

1. **Largest-fragment selection** — removes counter-ions and solvent molecules  
2. **Valence cleanup** — `rdMolStandardize.Cleanup()`  
3. **Neutralisation** — `Uncharger.uncharge()` removes formal charges where possible  
4. **Canonical tautomer** — `TautomerEnumerator.Canonicalize()` enforces one tautomeric form per structure  
5. **Canonical SMILES** — `Chem.MolToSmiles(mol, canonical=True)`  
6. **InChIKey** — used as identity key for deduplication  

**Outcome:** Zero salt-stripping events and zero parsing errors. The library was already delivered as salt-free, charge-neutral structures; no separate counter-ions were present in any entry.

All 15 actives were confirmed achiral by the SDF stereo-configuration annotation and by absence of stereocenters in the canonical SMILES. No tautomer-normalization changes altered scaffold connectivity.

---

## 3. Deduplication

| Check | Count |
|---|---|
| Duplicates within actives (same InChIKey) | 0 |
| Duplicates within inactives (same InChIKey) | 0 |
| Cross-class duplicates (active InChIKey also in inactives) | 0 |

No duplicate or conflicting data. Every compound has a unique identity across both classes.

---

## 4. Artefact Analysis

### 4.1 PAINS Filters (RDKit PAINS_A/B/C)

Three actives match the `anil_di_alk_E(186)` PAINS pattern — a dialkyl-substituted aniline:

| Compound | Rank | AS ratio | PAINS rule | Structural basis |
|---|---|---|---|---|
| EDS00480994 | 24 | 0.0891 | anil_di_alk_E(186) | 4-(N-methylpiperazino)aniline in R2 arm |
| EDS00490594 | 157 | 0.0301 | anil_di_alk_E(186) | Same motif, naphthyl R1 instead of benzofuran |
| EDS00481762 | 195 | 0.0181 | anil_di_alk_E(186) | Same motif, benzothiophenyl R1 |

**Interpretation:** The `anil_di_alk_E` flag marks dialkylaminophenyl groups as potential redox-active or assay-interfering moieties. In *biochemical* assays this pattern can quench fluorescent readouts. In ASMS the mechanism of artefact would differ: an oxidation product of the aniline could become covalently attached to protein cysteines, giving a false retention signal. However, all three share the *same* piperazine-aniline R2 group and differ only in R1; if the flag drove activity they would be indistinguishable from each other in rank, which is not the case (ranks 24, 157, 195 with 3–5× span in AS ratio). The scaffold is otherwise legitimate. **Verdict:** retain with caution, confirm with orthogonal SPR or ITC, and note that these three compounds are essentially one SAR point (R2 is constant).

### 4.2 Brenk Reactive-Group Filter

| Compound | Rank | AS ratio | Brenk rule | Basis |
|---|---|---|---|---|
| EDS00459274 | 314 | 0.0074 | halogenated_ring_1 | Difluoro + chloro on benzyl R2 |

**Interpretation:** The `halogenated_ring_1` flag matches aryl polyhalogenation. A 2,4-difluoro-1-chlorobenzyl group is not intrinsically reactive; the concern is metabolic bioactivation at the arene. In ASMS context this is not a primary artefact mechanism. **Verdict:** the compound is a marginal hit (rank 314, AS 0.0074) and the mixed-halide R2 is not reproduced elsewhere; deprioritise and replace with dehalogenated analogue F3 in the proposal set.

### 4.3 Aggregation and Colloidal Aggregator Risk

A heuristic score (0–3) was applied: +1 for MW > 400, +1 for cLogP > 3.0, +1 for ≥3 aromatic rings.

| Score | Interpretation | Active count |
|---|---|---|
| 0–1 | Low risk | 0 |
| 2 | Moderate | 3 |
| 3 | Elevated | 12 |

All 15 actives have MW > 400 and ≥3 aromatic rings; 12 have cLogP > 3. This means *the screening library itself* is biased toward compounds with elevated aggregation risk scores. This is a property of the library design, not a marker selective for actives. **Compound-specific concern:** EDS00495858 (top hit, rank 5, AS 0.172, MW 536, LogP 4.3, 4 aromatic rings) has the highest individual score. Its AS ratio is also substantially higher than all other actives, which could indicate non-specific protein sequestration by aggregates. However, the structural motif — a bicyclic tetrahydropyrido-piperidine core with two amide arms — is not a recognised aggregating scaffold, and the RT (1.13 min) is normal. **Verdict:** test EDS00495858 at multiple concentrations and in the presence of 0.01% Tween-20 to rule out colloidal aggregation before assigning SAR weight to it as the top hit.

### 4.4 ASMS-Specific Mass-Spectrometry Artefact Checks

**AS ratio distribution:** Inactive compounds have no recorded AS ratio (blank in SDF), consistent with the ASMS data-reduction workflow: only library members that pass the initial compound-detection step in both the protein-present and protein-absent runs are scored. There is therefore no population overlap to examine; artefact discrimination rests on structural and physico-chemical analysis.

**Dimer artefact check:** In-source dimerisation can produce a compound with MW ≈ 2× a monomeric member of the library; that dimer could then be scored as an "active" if it elutes at the expected RT and the mass matches a library entry. For 8 of the 15 actives, 1–7 compounds in the dataset have MW within 2 Da of half the active's MW. However, this hit rate is expected by chance across a 23,712-member library spanning MW 250–600 Da (normal distribution of masses). Structural inspection of the putative "half-mass" compounds shows no obvious dimerisation relationship. **Verdict:** no compound is flagged as a probable dimer artefact.

**Retention time:** All 15 actives elute in a narrow window of 1.00–1.32 min. Early elution (< 0.8 min) would indicate a hydrophilic, poorly retained compound that might co-elute with non-specific binders or show variable ionisation; no active falls in this zone. Late elution would indicate unusual lipophilicity and potential non-specific binding. The RT distribution is consistent with the drug-like properties of the series.

**Ionisation bias:** The amide-rich bicyclic scaffold is predominantly neutral at physiological pH (EDS00444974 as example: no basic nitrogen, no carboxylic acid). Four actives carry a piperazine or morpholine nitrogen (pKa ~7–9) that could shift ionisation efficiency between the protein-present and protein-absent runs; however, all four use ESI-positive mode compatibly and their AS ratios do not cluster anomalously. The aniline group in the three PAINS hits is weakly basic (pKa ~5) and unlikely to cause differential ion suppression.

**Frequent-hitter / promiscuous scaffold screening:** None of the 15 actives match common promiscuous aggregator scaffolds (rhodanine, catechol, quinone, Michael acceptors, aldehydes, acyl halides). One has a primary aniline (EDS00492986/EDS00492874 secondary amine — not primary), and no compound matches any reactive electrophilic motif (epoxide, isocyanate, alpha-halo-ketone). The scaffold family — bicyclic saturated-ring amides — does not appear in known frequent-hitter databases.

---

## 5. Consensus Scaffold and SAR Summary

**Maximum Common Substructure** across all 15 actives (RDKit rdFMCS, 15-atom, 16-bond):

```
O=C(N)–c1ccc2c(n1)–CH₂–N(–C=O)–CH₂–CH₂–2
```

This encodes a **5,6,7,8-tetrahydropyrido[3,4-d]piperidine** bicyclic core bearing two amide exit vectors:
- **R1 position**: acyl group on the saturated-ring nitrogen
- **R2 position**: amide-linked amine from the aromatic pyridine C5

All 15 actives share this core. The scaffold is not a known frequent hitter and is not represented in PAINS or Brenk catalogs.

| R1 group | R2 group | Rank | AS ratio |
|---|---|---|---|
| 4-(OCH₂CF₃)pyridine-2-carbonyl | 2-(pyrrol-1-yl)benzylamine | 5 | **0.172** |
| 2-methylbenzofuran-3-carbonyl | 4-(N-Me-piperazino)benzyl | 24 | 0.089 |
| 2-Cl-3-pyridyl-carbonyl | 4,4-difluorocyclohexylamine | 249 | 0.033 |
| 3-methoxynaphthalen-2-carbonyl | 4-(N-Me-piperazino)benzyl | 157 | 0.030 |
| 1,3-dimethylpyrazole-5-carbonyl | 3-(morpholino)pyridyl-methyl | 294 | 0.021 |
| Isobutyryl | 5-methylpyrimidinyl-methyl | 387 | 0.016 |
| Dimethylpyrazolyl | 2,4-difluoro-1-Cl-benzyl (Brenk) | 314 | 0.007 |
| 4-CF₃pyridyl, 2-MeO-naphthalyl, benzothienyl | piperazino-aniline (PAINS×3) | 195–468 | 0.001–0.012 |

**Key SAR observations:**

1. **R1 dominates potency.** The fluorinated-aliphatic-ether pyridyl (trifluoroethoxy-pyridine-2-carbonyl) in the top hit gives a 2–10× AS-ratio improvement over all other R1 groups, including the closely related methylbenzofuran and pyridyl-halide entries.
2. **R2 modulates potency secondarily.** The 2-(pyrrol-1-yl)benzyl group is unique to the top hit; the 4-(N-methylpiperazino)benzyl appears across three compounds with consistent mid-range AS ratios regardless of R1 variation.
3. **Simple R2 works.** EDS00444974 (methylpyrimidyl-methyl R2 + isobutyryl R1) is active at rank 387 with zero flags, demonstrating that elaborate R2 substituents are not required for binding.
4. **Aliphatic cyclic R2 is tolerated.** EDS00469766 uses a 4,4-difluorocyclohexylamine (not a benzylamine) as R2; its rank-249 activity demonstrates the R2 amide NH is not constrained to aryl-methyl.
5. **PAINS compounds (ranks 24, 157, 195) cluster.** Their activity span (2.5× in AS ratio) with *identical* R2 groups reflects R1 influence only, supporting R1 as the primary pharmacophoric determinant.

---

## 6. Proposed New Compounds

The following 20 compounds all pass PAINS_A/B/C, Brenk, and NIH filters, and have MW 369–557 Da, cLogP 1.5–4.4, and HBD = 1. They were designed on the validated bicyclic scaffold with rationale grounded in the SAR above.

### Group A — R1 fluorine bioisosteres, best R2 retained

| ID | SMILES | MW | LogP |
|---|---|---|---|
| A1 | `O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2` | 455 | 4.14 |
| A2 | `O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1cnc(OC(F)(F)F)cc1)CC2` | 521 | 4.29 |
| A3 | `O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(C(F)(F)F)nc1)CC2` | 506 | 4.41 |

**A1** — Best R2 (2-pyrrolyl-benzyl) + 4-fluorophenyl R1. Reduces MW by 80 Da versus the top hit by removing the pyridine N and the trifluoroethyl chain; tests whether the pyridine ring nitrogen in R1 makes an H-bond contact or whether aryl-F alone is sufficient for the lipophilic pocket. Lower MW also improves ligand efficiency.

**A2** — Best R2 + OCF₃-pyridine R1. The trifluoromethoxy group is a direct metabolic bioisostere of the trifluoroethoxy group in EDS00495858: same acceptor character, one fewer carbon, better resistance to ether oxidation. Prioritised metabolic stability improvement.

**A3** — Best R2 + 4-CF₃-pyridine-2-carbonyl R1. Tests direct aryl-CF₃ (lipophilic, non-HBA) versus ether-CF₃ (HBA component). If activity is maintained, the CF₃ itself rather than the ether oxygen explains the R1 contribution.

---

### Group B — Clean analogues of PAINS-flagged EDS00480994 series

| ID | SMILES | MW | LogP |
|---|---|---|---|
| B1 | `Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccncc4)nc3C2)oc2ccccc12` | 426 | 3.66 |
| B2 | `Cc1c(C(=O)N2CCc3ccc(C(=O)NCC4CCOCC4)nc3C2)oc2ccccc12` | 434 | 3.49 |
| B3 | `Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(F)cc4)nc3C2)oc2ccccc12` | 443 | 4.40 |

**B1** — EDS00480994 aniline PAINS removed by substituting 4-pyridylmethyl for the piperazino-aniline-benzyl. Keeps the methylbenzofuran R1 that defines the EDS00480994 scaffold. Cleanest possible like-for-like replacement; tests whether the piperazine was binding or the aniline alone drove the PAINS flag.

**B2** — Replaces aniline-piperazine with a tetrahydropyranyl-methyl R2 (aliphatic, no amine). If activity is lost relative to B1, confirms the basic nitrogen contributes binding; if retained, the aniline context was the only issue.

**B3** — Simplest control: 4-fluorobenzyl R2 (no basic nitrogen at all). Benchmark for the contribution of the piperazine-aniline versus a plain aryl-methyl.

---

### Group C — Best R1 with unexplored clean R2 motifs

| ID | SMILES | MW | LogP |
|---|---|---|---|
| C1 | `O=C(NCc1ccc(N2CCOCC2)nc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` | 557 | 2.78 |
| C2 | `O=C(NCc1cccc(F)c1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` | 488 | 3.69 |
| C3 | `O=C(NCc1cnc(C)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` | 485 | 3.25 |
| C4 | `O=C(NCc1ccc(-n2ccnc2)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` | 537 | 3.73 |

**C1** — Best R1 + morpholino-pyridinyl-methyl R2. Morpholine on a pyridine ring (not aniline context, no PAINS) provides HBA oxygen and partial basic nitrogen; lower pKa (~5) versus piperazine. Rationale: determine whether the basic nitrogen identified in the inactive piperazine-aniline PAINS series can be retained in a clean form.

**C2** — Best R1 + 3-fluorobenzyl R2. Minimal probe: only adds a single fluorine to the benzyl of EDS00490706 (rank 468, no flags, AS 0.0012). If the top-hit R1 is solely responsible for high AS ratio, this should jump from rank ~468 to near-top. Confirms R1 primacy.

**C3** — Best R1 + 5-methylpyridyl-methyl R2. Heteroaromatic bioisostere of the methylpyrimidine R2 from EDS00444974 (cleanest active). Tests whether the second ring nitrogen in pyrimidine is a productive HBA contact or whether a mono-aza ring suffices.

**C4** — Best R1 + 4-(imidazol-1-yl)benzyl R2. N-linked imidazole adds an HBA imidazole nitrogen without creating an aniline motif. Tests whether N-heterocycle on benzyl provides a binding contact analogous to the pyrrolyl group in the top hit.

---

### Group D — 4,4-Difluorocyclohexyl R2 with upgraded R1

| ID | SMILES | MW | LogP |
|---|---|---|---|
| D1 | `O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` | 498 | 3.92 |
| D2 | `O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2` | 417 | 3.73 |

**D1** — Combines the two strongest individual structural signals: best R1 (trifluoroethoxypyridyl, from rank-5 hit) and the aliphatic 4,4-difluorocyclohexylamine R2 (from rank-249 EDS00469766). EDS00469766 had a suboptimal R1 (2-Cl-pyridyl, also halogenated). This direct combination tests whether the R1–R2 contributions are additive. No flags. **Priority compound.**

**D2** — Same aliphatic R2 + minimised 4-fluorophenyl R1. MW 417, the lowest in the series, HBD = 1, RotB = 3 (most conformationally constrained new compound proposed). Tests minimal pharmacophore with excellent ligand efficiency potential.

---

### Group E — Low-MW / simplified scaffolds

| ID | SMILES | MW | LogP |
|---|---|---|---|
| E1 | `Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(F)cc2)CC3)cn1` | 405 | 2.45 |
| E2 | `Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(OCC(F)(F)F)nc2)CC3)cn1` | 486 | 2.64 |
| E3 | `Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)C4(F)CC4)CC3)cn1` | 369 | 1.50 |

**E1** — EDS00444974 (cleanest active, all-clean, rank 387, AS 0.016) with R1 upgraded from isobutyryl to 4-fluorophenyl. Tests if the isobutyryl R1 was suboptimal; fluorophenyl is more rigid and has an H-bond donor from the ring edge. Lowest MW in group A–C analogy.

**E2** — EDS00444974 R2 (methylpyrimidine-methyl) + best R1 (trifluoroethoxypyridyl). This is the most direct upgrade of the cleanest active with the best-characterised R1. High-priority synthesis target: if EDS00444974's low rank (387) was purely an R1 limitation, this compound should be a strong binder. LogP 2.64 — best drug-likeness in the entire proposed set.

**E3** — EDS00444974 R2 + 1-fluorocyclopropane-carbonyl R1 (MW 369, lowest in the entire set). A rigidifying probe: cyclopropyl is a common metabolic stability enhancer and conformational lock. If activity is maintained despite the tiny R1, it suggests the R1 pocket tolerates small, rigid groups. Excellent ligand efficiency target.

---

### Group F — Novel R2 combinations and derisked analogues

| ID | SMILES | MW | LogP |
|---|---|---|---|
| F1 | `O=C(NCC1(c2ccccc2)CCOCC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` | 555 | 4.09 |
| F2 | `O=C(NCc1ccsc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` | 476 | 3.61 |
| F3 | `O=C(NCc1cc(F)ccc1F)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` | 506 | 3.82 |
| F4 | `O=C(NCc1ccc(S(C)(=O)=O)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` | 549 | 2.95 |
| F5 | `O=C(NCc1cccc(N2CCOCC2)n1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` | 557 | 2.78 |

**F1** — Best R1 + spirocyclic benzyl-THF R2 from EDS00470458 (the spiro compound, rank 613, AS 0.0015). The weak activity of EDS00470458 may reflect its poor R1 (methoxythiophene). Upgrading to best R1 tests whether the spiro R2 contributes positively, or whether that compound is simply a near-insoluble weak binder irrespective of R1.

**F2** — Best R1 + thienylmethyl R2 from EDS00474254 (rank 677, AS 0.0037). Simple thiophene-methyl is clean, compact, introduces an aromatic sulfur as weak HBA/contact. Another "upgrade the R1 to rescue a weak hit" experiment.

**F3** — Clean analogue of EDS00459274 (Brenk:halogenated_ring_1). Removes the aryl chlorine (metabolic liability), retains both fluorines (2,4-position), and adds best R1. Derisked version of rank-314 hit; the chlorine removal reduces MW by 35 Da.

**F4** — Best R1 + methylsulfonyl-benzyl R2 from EDS00474362 (rank 794, AS 0.0026). The sulfonyl group is an HBA without basicity; this R2 pattern should provide excellent solubility. Tests whether the extremely weak AS ratio for EDS00474362 was an R1 limitation.

**F5** — Best R1 + 3-(morpholino)pyridinyl-methyl R2 from EDS00459346 (rank 294, AS 0.021). EDS00459346 had a dimethylpyrazole R1 that ranks at 294; replacing it with the best R1 (≈10× stronger in the top hit) should substantially improve activity. This is a targeted R1 swap on a mid-ranked, clean hit.

---

## 7. Synthesis and Testing Priorities

**Tier 1 — Highest confidence / most informative (synthesise first):**

| Priority | ID | Rationale |
|---|---|---|
| 1 | **E2** | Direct upgrade of cleanest active (EDS00444974) with best R1; zero flags, excellent drug-likeness (LogP 2.64) |
| 2 | **D1** | Combination of the two strongest individual structural elements from different actives |
| 3 | **B1** | Derisked PAINS-free analogue of second-best hit (AS 0.089); immediate synthesis from EDS00480994 |
| 4 | **F5** | R1 upgrade of mid-ranked clean hit; tests R1 primacy hypothesis |
| 5 | **C2** | Minimal probe of R1 primacy with simplest R2 |

**Tier 2 — Mechanistic probes and SAR expansion:**

A2, A3, C1, C3, C4, D2, E1, E3, F2

**Tier 3 — Lower priority / rescue experiments:**

A1, B2, B3, F1, F3, F4

---

## 8. Recommendations for Follow-Up Assays

1. **Re-screen EDS00495858 at 3 concentrations** (0.1×, 1×, 10× standard assay concentration) with and without 0.01% Tween-20. Aggregation-driven hits show blunted concentration-response curves in detergent.
2. **Confirm the three PAINS hits (EDS00480994, EDS00490594, EDS00481762) by SPR or ITC** before routing to chemistry; if they show dose-dependent, saturable binding, the aniline flag is a false positive for this target.
3. **Run EDS00469766 at lower concentration** — its 4,4-difluorocyclohexyl R2 motif is rare and clean; confirming this hit would validate the aliphatic R2 vector and support D1/D2.
4. **EDS00444974** (the cleanest active, all-clear, simplest structure) should be used as an anchor for SPR Kd determination — it has no flags and is the best compound for establishing a biophysical binding benchmark.
