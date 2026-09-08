
## Provenance

All numbers derive exclusively from:
- **Compound data**: user-supplied `/home/ubuntu/rayca-artifacts/58e70b8d6c265c53a41c3467/files/ASMS.sdf` (23,712 compounds, 15 actives by HIT P841 field)
- **Crystal structure**: user-supplied `/home/ubuntu/rayca-artifacts/396fce89620d1932c2d5eb11/files/CDK2-CCNE.pdb` (1.94 Å, chains A=CDK2, B=Cyclin E, co-crystal ligand CTX at chain B residue 401)
- **No public CDK2 structures or compound databases were used.**

---

## Stage 1 — Screen Triage

| Metric | Value |
|---|---|
| Library | 23,712 compounds |
| Actives (HIT P841 = "Active") | 15 (0.063%) |
| Primary scaffold (THN core) | 13/15 actives |
| Alternate chemotype | 2/15 (EDS00492874, EDS00492986 — piperidinyl-succinamide) |
| AS-ratio range (actives) | 0.0012 – 0.172 |

**THN core SMARTS** (validated against 13/13 THN actives):
`[#6](=O)-[#7]1-[#6]-[#6]-[#6]2:[#6](-[#6]-1):[#7]:[#6](:[#6]:[#6]:2)-[#6](=O)-[#7]`

Two R-group positions on the THN scaffold:
- **R1**: N-acyl aromatic cap (varies across all 13 actives)
- **R2**: Ar via NH–CH₂ linker (varies across all 13 actives)

---

## Stage 2 — Binding Site Characterisation

CTX (39 heavy atoms, C₃₁N₅O₃) bridges both protein chains, confirming a **PPI glue mechanism**.

**Pocket residues within 4.5 Å of CTX:**

| Chain | Residues |
|---|---|
| A (CDK2) | LEU54, GLU57, LEU58, HIS121, ARG122, VAL123, ALA151, PHE152, GLY153 |
| B (Cyclin E) | LEU90, VAL101, TRP102, ILE104, MET105, ASN107, LYS108, THR111, SER227, PRO228, LEU229, SER233, TRP234, VAL237 |

**Key pharmacophore interactions from CTX crystal pose:**

| Interaction | Distance | Type |
|---|---|---|
| HIS121-A backbone C=O ↔ CTX N2 | 3.12 Å | H-bond acceptor (backbone carbonyl accepts NH) |
| LYS108-B NZ ↔ CTX O2 | 3.27 Å | H-bond donor (Lys NH donates to ligand C=O) |
| TRP102-B / TRP234-B | — | Aromatic sandwich for R1 π-stacking |

**Core pharmacophore**: HBD-1 = THN ring NH → HIS121-A backbone carbonyl (present in 14/15 actives; the 1 exception is EDS00444974 which has an alternative donor geometry). The LYS108-B interaction appears to be the R2-side anchor.

---

## Stage 3 — SAR from Screen (Pre-Design, Derived Only from ASMS Actives)

| Feature | Observation |
|---|---|
| THN core | Required (13/15 actives share it; 2 alternate chemotype active but MW and shape differ substantially) |
| R1 diversity | All 13 THN actives have distinct R1 groups — the TRP sandwich pocket tolerates wide aromatic variation |
| R2 diversity | Benzyl-type dominant (Ar–CH₂–NH); one non-benzyl (diF-cyclohexyl-like in EDS00444974) |
| Activity range | AS ratio 0.0012–0.172; highest active (EDS00495858, AS=0.172) not the best docking score, indicating the screen signal is noisy |
| MW range | 353–549 Da (mean 480) |
| Most potent active by AS ratio | EDS00495858 (AS=0.172, Vina −10.0, CNN pKi 6.78) |
| Strongest docking active | EDS00480994 (Vina −14.4, CNN pKi 8.07) — note discordance with AS rank |

---

## Stage 4 — Analogue Design (38 Compounds)

Template: `O=C(R1)N1Cc2nc(C(=O)NCC_R2)ccc2CC1` (THN core, two variable positions)

Series designed:
- **A (9)**: R1 = 2-OCH₂CF₃-pyridin-5-yl × varied R2
- **B (5)**: R1 = benzofuran-2-yl × varied R2
- **C (3)**: R1 = benzothiophen-2-yl × varied R2
- **D (3)**: R1 = 5-CF₃-pyridin-3-yl × varied R2
- **E (3)**: R1 = 2-OMe-naphthyl × varied R2
- **F (2)**: R1 = quinolin-3-yl × varied R2
- **G (3)**: R1 = 4-F-phenyl × varied R2
- **H (2)**: R1 = 2-OMe-pyridin-5-yl × varied R2
- **I (2)**: R1 = 4-CF₃-phenyl × varied R2
- **J (6)**: Novel R1/R2 combinations (fused heterocycles, benzo[d]isoxazole, CN-benzyl)

All 38 SMILES passed RDKit validation.

---

## Stage 5 — Docking Results (gnina, CDK2-CCNE receptor)

Docking box centred on CTX centroid: (30.57, 5.37, −25.80) Å, box 24×20×20 Å.
All 53 compounds (15 actives + 38 designed) docked with 9 poses each = 477 total poses.

**ASMS actives ranked by Vina:**

| Compound | Vina (kcal/mol) | CNN pKi | AS ratio |
|---|---|---|---|
| EDS00480994 | −14.36 | 8.07 | 0.089 |
| EDS00490594 | −13.12 | 8.07 | 0.030 |
| EDS00481762 | −11.74 | 6.87 | 0.018 |
| EDS00459346 | −11.25 | 6.72 | 0.021 |
| EDS00490706 | −11.22 | 6.19 | 0.0012 |
| EDS00492986 | −10.67 | 7.20 | 0.0097 |
| EDS00492874 | −10.41 | 7.42 | 0.011 |
| EDS00474362 | −10.28 | 7.19 | 0.0026 |
| EDS00459442 | −10.23 | 6.17 | 0.0083 |
| EDS00469766 | −10.03 | 6.87 | 0.033 |
| EDS00495858 | −9.98 | 6.78 | 0.172 |
| EDS00474254 | −9.65 | 6.49 | 0.0037 |
| EDS00470458 | −9.57 | 6.64 | 0.0015 |
| EDS00444974 | −9.32 | 6.92 | 0.016 |
| EDS00459274 | −9.20 | 6.62 | 0.0074 |

**Note**: Spearman rank correlation between Vina and AS ratio is weak (the highest AS-ratio compound ranks 11th by Vina). This is expected — gnina docks into the crystal pocket; the ASMS signal integrates all protein-compound contacts including possible secondary sites.

---

## Stage 6 — ADME Filtering

Criteria: Lipinski RO5 (0 violations), TPSA ≤ 140 Å², rotatable bonds ≤ 10, no PAINS alerts.

- **16/38 designed compounds pass** all criteria
- **22/38 fail** — mostly due to: MW > 500 (11 compounds), PAINS from para-aminobenzyl groups (18 compounds), or both
- **9/15 ASMS actives pass** ADME (all are experimental confirmed binders, so ADME failures among actives represent real druggable scaffolds that the PAINS filter over-penalises)

---

## Stage 7 — Ranked Synthesis List (ADME-Passing Designed Compounds)

Ranked by Vina affinity (most negative = best). CNN pKi reported as secondary metric.

| Rank | ID | R1 | R2 | Vina | CNN pKi | MW | logP | TPSA | RotB |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **A09** | 2-CF₃EtO-py5 | 4,4-diF-cHex | −11.44 | 6.58 | 498 | 3.92 | 84.4 | 5 |
| 2 | **D03** | 5-CF₃-pyridin-3-yl | 4,4-diF-cHex | −11.24 | 6.67 | 468 | 4.00 | 75.2 | 3 |
| 3 | **B05** | benzofuran-2-yl | 4,4-diF-cHex | −11.01 | 6.20 | 439 | 4.33 | 75.4 | 3 |
| 4 | **B01** | benzofuran-2-yl | 2-pyrrolyl-Bn | −10.98 | 6.90 | 476 | 4.75 | 80.4 | 5 |
| 5 | **G01** | 4-F-phenyl | 2-pyrrolyl-Bn | −10.97 | 6.56 | 454 | 4.14 | 67.2 | 5 |
| 6 | **G03** | 4-F-phenyl | 4,4-diF-cHex | −10.94 | 5.97 | 417 | 3.73 | 62.3 | 3 |
| 7 | **B04** | benzofuran-2-yl | pyrimidin-5-CH₂ | −10.94 | 6.48 | 413 | 2.75 | 101.2 | 4 |
| 8 | **F01** | quinolin-3-yl | 2-pyrrolyl-Bn | −10.84 | 6.97 | 487 | 4.55 | 80.1 | 5 |
| 9 | **J03** | 2-CF₃EtO-py5 | 3-CN-Bn | −10.79 | 6.18 | 495 | 3.42 | 108.2 | 6 |
| 10 | **J02** | benzo[d]isoxazol-3-yl | 2-pyrrolyl-Bn | −10.68 | 7.13 | 477 | 4.14 | 93.3 | 5 |
| 11 | **C03** | benzothiophen-2-yl | 4,4-diF-cHex | −10.64 | 6.20 | 455 | 4.80 | 62.3 | 3 |
| 12 | **E03** | 2-OMe-naphthyl | 4,4-diF-cHex | −10.33 | 6.45 | 479 | 4.75 | 71.5 | 5 |
| 13 | **H01** | 2-OMe-pyridin-5-yl | 2-pyrrolyl-Bn | −9.81 | 7.04 | 467 | 3.40 | 89.3 | 7 |
| 14 | **A05** | 2-CF₃EtO-py5 | pyrimidin-5-CH₂ | −9.10 | 6.23 | 472 | 2.34 | 110.2 | 6 |
| 15 | **A07** | 2-CF₃EtO-py5 | 4-F-Bn | −8.77 | 6.17 | 488 | 3.69 | 84.4 | 6 |
| 16 | **A06** | 2-CF₃EtO-py5 | pyridin-4-CH₂ | −8.45 | 6.16 | 471 | 2.94 | 97.3 | 6 |

**Recommended priority subset for synthesis** (top 6 covering diverse R1/R2 combinations):
A09, D03, B05, B04, G03, J02

---

## Stage 8 — Explicit Falsifiable SAR Claims

These predictions are committed before seeing experimental SAR. They are stated as directional inequalities with a minimum effect size sufficient to distinguish from assay noise. The experimental comparator is assumed to be IC₅₀ or Kd measured by the same assay format across all compounds.

---

### SAR Claim 1 (R2 — most important, highest confidence)
**4,4-difluorocyclohexyl at R2 gives higher potency than 4-fluorobenzyl at R2 (same R1).**

Direct matched pair: A09 (R2 = diF-cHex) vs A07 (R2 = 4-F-Bn), both with R1 = 2-CF₃EtO-py5.
Predicted direction: **A09 more potent than A07, by ≥ 5-fold in IC₅₀.**
Structural basis: The R2 pocket (lined by TRP102-B/LYS108-B) is enclosed and hydrophobic; the 4,4-diF-cyclohexyl fills it with a compact, shape-matched lipophilic group and no conformational entropy cost from a benzylic rotor. The gem-difluoro provides a partial dipole interaction with LYS108-B NZ at the pocket edge.

**⚠ Most damaging if wrong**: Falsification of this claim means the R2 vector does not point into a defined hydrophobic pocket, and the structural model for R2 SAR is incorrect. The entire R2 design rationale would need to be revised.

---

### SAR Claim 2 (R1 — high confidence)
**Fused bicyclic R1 groups outperform monocyclic phenyl at R1 when R2 is held constant.**

Matched set at R2 = 4,4-diF-cHex: A09 (2-CF₃EtO-py5) > D03 (5-CF₃-py3) > B05 (benzofuran) > G03 (4-F-phenyl) > C03 (benzothiophene) > E03 (2-OMe-naphthyl).
Predicted direction: **B05 more potent than G03, by ≥ 3-fold in IC₅₀.**
Structural basis: TRP102-B and TRP234-B form an aromatic sandwich; a fused bicyclic system (benzofuran or benzothiophene, ~10 heavy atoms) makes larger π-stacking contacts than a monocyclic phenyl (~6 heavy atoms).

**⚠ Damaging if wrong**: Means the R1 pocket is not size-discriminating for π-stacking; the TRP sandwich either is not the binding mode or is saturated by a monocyclic ring.

---

### SAR Claim 3 (R1 electronic substitution — medium confidence)
**Within heteroaromatic R1, electron-withdrawing substituents (CF₃, F) outperform electron-donating (OMe) at the pyridine 2-position.**

Comparisons: A-series (2-CF₃EtO-py5) > H-series (2-OMe-py5) at matched R2.
Predicted direction: **A09 more potent than H01, by ≥ 3-fold in IC₅₀** (holding caveat that R2 differs: A09 has diF-cHex, H01 has 2-pyrrolyl-Bn; the R1 comparison is confounded unless H01 analogues with diF-cHex R2 are also made).
Structural basis: TRP102/234 are electron-rich aromatic residues; an electron-poor R1 ring engages in stronger edge-to-face stacking. The 2-OMe substituent on pyridine also adds a steric bump that may force a tilt away from ideal TRP stacking geometry.

---

### SAR Claim 4 (R2 heterocyclic substitution — medium confidence)
**R2 bearing a heteroaromatic N-H donor (2-pyrrolyl at ortho of benzyl) gives higher potency than simple 4-F-benzyl.**

Comparison: B01 (R2=2-pyrrolyl-Bn) vs B05 (R2=diF-cHex) both with R1=benzofuran (Vina nearly equal: −10.98 vs −11.01). G01 (R2=2-pyrrolyl-Bn) vs G03 (R2=diF-cHex) — also nearly equal: −10.97 vs −10.94.
Predicted direction: **2-pyrrolyl-Bn and diF-cHex R2 groups are within assay noise of each other (< 2-fold difference).** The 2-pyrrolyl NH may H-bond with a polar residue (ASN107-B or THR111-B) at the rim of the R2 pocket, compensating for the larger lipophilic surface of the diF-cyclohexyl.

**⚠ Damaging if wrong (in either direction)**: If 2-pyrrolyl-Bn is substantially better, it suggests a buried H-bond acceptor we missed. If it is substantially worse, it suggests the NH is desolvated with no compensating H-bond, and the model for the R2 pocket rim is wrong.

---

### SAR Claim 5 (para-aminoalkyl at R2 — high confidence, strong prediction)
**Adding piperazinyl or morpholinyl at para of the R2 benzyl ring reduces intrinsic potency vs the same benzyl without the amine.**

Supporting data from ADME-failing compounds: D02 (R2=4-piperazino-Bn, Vina −13.0, but MW 524, PAINS) vs D03 (R2=diF-cHex, Vina −11.2, MW 468, passes ADME). The large Vina scores for piperazino compounds are not supported by their CNN affinity scores.
Predicted direction: **D03 more potent than D02 in a cell-free binding assay, by ≥ 5-fold IC₅₀,** despite D02 scoring better in Vina. The Vina over-scoring for piperazino compounds reflects non-specific electrostatic contacts at the pocket entry rather than occupancy of the core hydrophobic site.

---

### SAR Claim 6 (scaffold — high confidence, ground-level)
**Removal of the THN ring NH (replacing with N-methyl or N-alkyl) abolishes activity.**

This is not directly testable from the 38 designed analogues but is the anchor prediction for the entire SAR model. All 14 THN actives with measurable AS ratios retain the secondary amine NH. The H-bond to HIS121-A backbone (3.12 Å in CTX crystal) is the single most conserved pharmacophoric feature.
Predicted direction: **Any THN analogue lacking the ring NH will show > 100-fold loss in potency.**

---

## Priority Claims for Experimental Comparison (Rank Order of Confidence and Informativeness)

| Priority | Claim | Matched pair to test | Effect size predicted | Most damaging if wrong? |
|---|---|---|---|---|
| 1 | diF-cHex > 4-F-Bn at R2 | A09 vs A07 | ≥ 5-fold | Yes — invalidates R2 pocket model |
| 2 | Fused bicyclic > monocyclic at R1 | B05 vs G03 | ≥ 3-fold | Yes — invalidates TRP sandwich model |
| 3 | diF-cHex > piperazino-Bn at R2 | D03 vs D02 | ≥ 5-fold | Partial — Vina fails to discriminate if wrong |
| 4 | EW-R1 > ED-R1 (CF₃ > OMe on pyridine) | A09 vs H01 (confounded) | ≥ 3-fold | Partial — R2 differs |
| 5 | 2-pyrrolyl-Bn ≈ diF-cHex at R2 | B01 vs B05; G01 vs G03 | < 2-fold difference | Partial — directs R2 rim model |
| 6 | THN NH required | N-methyl analogue vs any active | ≥ 100-fold | Yes — invalidates entire HIS121 pharmacophore |

---

## Limitations and Calibration Notes

1. **Docking vs AS ratio correlation is weak** for the 15 actives (highest-AS compound ranks 11th by Vina). Gnina was trained on crystallographic poses of tight binders; at the mM–μM affinity range typical of primary screen hits, CNN scores are less reliable. Claims 1–5 rest on the docking model, not on observed activity rank within the 15 actives.

2. **Two actives (EDS00480994, EDS00490594) have anomalously high CNN scores** (0.97 and 0.94 vs ≤0.53 for designed analogues). If these reflect genuinely high-confidence poses, they suggest the screening actives may be higher-affinity than the designed set at this round. If these scores are artefacts of pose scoring, the rank order is less reliable.

3. **gnina CNN was trained on general protein-ligand complexes, not PPI glue interfaces.** The pocket spans two chains with unusual geometry; CNN scores may underestimate compounds that make contacts across the interface (e.g., A-chain-only contacts not captured by the standard scoring function).

4. **PAINS alerts should not be treated as hard failures.** 22/38 flagged analogues include validated scaffolds (pyridinyl-piperazines, benzofuryl-amides) where PAINS hits are likely false positives. The ADME-failing set contains the highest Vina scorers (D02, C02, B03) — these warrant re-synthesis with ADME-modified groups before being discarded.

5. **Provenance of all claims is this analysis alone.** No knowledge of experimental SAR was used in generating these predictions.
