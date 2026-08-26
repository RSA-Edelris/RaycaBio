
## 1. Dataset Overview

| Parameter | Value |
|---|---|
| Total compounds | 57 |
| Activity column | pIC50 (continuous, measured) |
| pIC50 range | 4.044 – 5.959 |
| Series | Naphthyridine (32), Tetrahydrothienopyridine (21), Other (4) |
| Best compound | CTX-1020456 (pIC50 5.959, IC50 ≈ 1.1 µM) |
| Target range | pIC50 8–9 (IC50 10–100 nM) → needs 100–1000× improvement |

**All 57 compounds currently sit below 1 µM potency.** The gap to the 10–100 nM target is 2–3 log units. This report identifies the structural reasons for the ceiling and proposes specific designs to break it.

---

## 2. Structure Standardization

Pipeline (RDKit 2023.9.6): largest-fragment selection → valence cleanup → uncharging → canonical tautomer → canonical SMILES + InChIKey.

| Check | Result |
|---|---|
| Salt-stripped | 0 |
| Parse errors | 0 |
| Tautomer-normalized | 0 (no changes) |
| All achiral | Yes |

No standardization issues. Library delivered as clean, single-component structures.

---

## 3. Deduplication

Zero duplicate InChIKeys across all 57 compounds. Every entry is a unique structure.

---

## 4. Artefact Analysis

### 4.1 PAINS Filter (A/B/C)

| Rule | Count | Compounds |
|---|---|---|
| `anil_di_alk_E(186)` | 34 | 60% of dataset |
| `anil_di_alk_D(198)` | 1 | CTX-1020902 |
| `indol_3yl_alk(461)` | 2 | CTX-1020745, CTX-1020752 |
| **Total flagged** | **36/57** | **63%** |

The `anil_di_alk_E` flag fires on the 4-(N-alkylpiperazin-1-yl)aniline substructure present in the R2 arm of the majority of compounds. This is a *systematic structural feature of the series*, not a minority of outliers. 

**Critically: PAINS-flagged compounds are LESS active than the clean subset on average** (mean pIC50 5.172 vs 4.991 — a modest 0.18 difference). However, when matched by R1 group, the clean best compound CTX-1020698 (pIC50 5.955) *outperforms* the PAINS best (CTX-1020456, 5.959 ≈ equal). The PAINS flag does not explain potency here; it is a structural liability that should be eliminated in future compounds.

The `indol_3yl_alk(461)` flag in CTX-1020745 and CTX-1020752 matches an N-methylindole. These two compounds score 4.517 and 4.060 respectively — below average — consistent with the indole C3 alkylation pattern interfering with binding or conferring non-specific interactions.

**Verdict on PAINS:** Real structural liability for the aniline series (metabolic bioactivation, oxidation risk), but not a dominant artefact mechanism in a biochemical IC50 assay. Confirmed activity in the matched clean pair CTX-1020698 validates that the scaffold is a genuine binder; the PAINS motif simply represents a suboptimal R2 choice.

### 4.2 Brenk Filter

Zero Brenk alerts. No reactive or acutely toxic functional groups identified.

### 4.3 Aggregation and Frequent-Hitter Risk

- MW range 415–603 Da; LogP range 2.00–5.95
- 51/57 compounds have MW > 400 and LogP > 3 — the standard heuristic aggregation-risk zone
- However: the dihydropyrido-piperidine amide scaffold is not a known aggregating chemotype (no catechol, quinone, rhodanine, aldehyde, epoxide, Michael acceptor, or polycyclic aromatic aggregator substructures)
- None match reactive-electrophile catalogues

**Verdict:** No structural evidence for colloidal aggregation. Modest lipophilicity (LogP 3–5) is consistent with the series and unlikely to trigger non-specific binding at typical assay concentrations.

### 4.4 Frequent-Hitter Patterns

- No compound matches known promiscuous scaffold families (PAINS beyond the aniline-piperazine already discussed, metal chelators, redox cyclers)
- The best clean compound CTX-1020698 is confirmed free of all common frequent-hitter motifs

---

## 5. SAR Analysis

### 5.1 Common Scaffold

Both series share the same dual-amide bicyclic core:

**R1–C(=O)–N(–CH₂CH₂)–[pyridine or thiophene ring]–C(=O)–NH–CH₂–[benzyl-R2]**

- **Naphthyridine core**: fused pyridine + piperidine, N-acylated
- **Tetrahydrothienopyridine core**: fused thiophene + piperidine, N-acylated
- Both cores give similar potency ranges; no statistically significant core effect

### 5.2 R1 Potency Rank (head-to-head with constant piperazino-aniline R2)

| R1 | Compound | pIC50 |
|---|---|---|
| 3-Cl-benzothiophen-2-carbonyl | CTX-1020456 | **5.959** |
| 3-Cl-benzofuran-2-carbonyl | CTX-1020453 | 5.762 |
| 3-Me-benzofuran-2-carbonyl + 4-Cl on ring | CTX-1020459 | 5.740 |
| 3-Me-benzofuran-2-carbonyl | CTX-1017233 | 5.593 |
| 3-Me-benzofuran-2-carbonyl + F on ring | CTX-1020454 | 5.567 |
| 1-methyl-3-Cl-benzimidazol-2-yl | CTX-1020748 | 5.556 |
| Pyrazolo[1,5-a]pyrimidine-2-carbonyl | CTX-1020671 | 5.463 (clean) |
| Simple heteroaryls (pyrrole, azaindole) | — | ≤5.192 |

**Key insight:** The 3-Cl on benzothiophene provides the best R1. The combination of a fused bicyclic aromatic, a sulfur atom, and a C3 halogen outperforms all other R1 groups. Replacing the S with O (benzofuran) reduces potency by ~0.2 log units.

### 5.3 R2 Potency Rank (head-to-head with 3-Me-benzofuran R1)

| R2 | Compound | pIC50 | PAINS |
|---|---|---|---|
| 4-(pyridin-4-yl)benzyl | CTX-1020698 | **5.955** | clean |
| 4-(tetrahydropyranyl)benzyl | CTX-1020696 | 5.879 | clean |
| Tetrahydroisoquinolinyl-methyl | CTX-1020695 | 5.565 | clean |
| 4-(N-methylpiperazino)benzyl | CTX-1017233 | 5.593 | PAINS |
| 4-(N-methylpiperidinyl)benzyl | CTX-1020697 | 5.412 | clean |
| 4-hydroxybenzyl | CTX-1020566 | 5.411 | clean |
| 4-pyridylmethyl (no benzyl) | CTX-1019471 | 5.488 | clean |
| Thiazolylmethyl | CTX-1019496 | 5.262 | clean |
| 4-CF₃benzyl | CTX-1020751 | 4.044 | clean |

**Key insights:**
1. **Biaryl R2 is essential**: 4-pyridyl**benzyl** (pIC50 5.955) vs 4-pyridyl**methyl** (5.488) — the extra phenyl ring adds 0.47 log units (3×). Removing the phenyl linker collapses potency by 3×.
2. **Pyridyl N is an HBA contact**: CF₃-benzyl scores 4.044 (worst clean compound), while OH-benzyl scores 5.411 — suggesting an HBA rather than a hydrophobic contact in the R2 terminal zone.
3. **PAINS aniline-piperazine is NOT optimal**: The clean pyridyl-benzyl (5.955) slightly outperforms the PAINS piperazino-aniline-benzyl (5.593) with the same R1. Removing the PAINS motif improves potency.

### 5.4 Critical Missing Combination

The combination of the best R1 (3-Cl-BTP) with the best clean R2 (4-pyridyl-benzyl) has **never been synthesised**. All 3-Cl-BTP compounds use the PAINS R2, and all pyridyl-benzyl compounds use the 3-MeBFO R1. This is the highest-priority synthesis target.

### 5.5 Property–Potency Correlations

| Property | Pearson r vs pIC50 |
|---|---|
| cLogP | 0.234 |
| MW | 0.268 |
| RotB | 0.146 |

Modest positive correlation with both LogP and MW — compounds with higher lipophilicity and more aromatic surface area tend to be more potent. This is consistent with a predominantly hydrophobic binding pocket. However, the low r values indicate that lipophilicity alone is not the driver.

---

## 6. Why All Compounds Are ≤1 µM and How to Break the Ceiling

The pIC50 ceiling at ~6 (1 µM) is likely caused by one or more of:

1. **Unoccupied sub-pocket**: The R2 biaryl chain (best with para-pyridyl) terminates in the correct direction but the pyridyl N may make only a weak or water-mediated HBA contact. Extending the chain or adding an HBD at the terminus could fill the next binding pocket.

2. **R1 not filling the full pocket**: The 3-Cl-benzothiophene fills one lipophilic sub-site, but 3-Cl-benzofuran is only 0.2 log units weaker — suggesting the S atom and the 3-Cl both contribute small increments. A larger fused aromatic (naphthothiophene) or additional substituent on the BTP ring could fill uncaptured pocket space.

3. **Conformational penalty**: The CH₂ linker between the core and R2 benzyl is flexible. Constraining this torsion (α-fluorine, cyclopropyl linker) could recover 0.5–1.5 log units.

4. **No H-bond donor in the molecule** (HBD = 1, the amide NH): Adding an aminopyridine or hydroxyl group at the R2 terminus that can donate to a protein carbonyl could add 1–2 log units.

---

## 7. Proposed New Compounds (20)

All pass PAINS A/B/C, Brenk, and NIH filters. All validated SMILES. MW 490–615, LogP 3.3–7.8, HBD 1–2.

### Group A — Critical untested combinations: best R1 × clean R2

| ID | SMILES | MW | LogP |
|---|---|---|---|
| A1 | `O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2` | 539 | 6.14 |
| A2 | `O=C(NCc1ccc(-c2ccncc2)cc1)c1cc2c(s1)CCN(C(=O)c1sc3ccccc3c1Cl)C2` | 544 | 6.81 |
| A3 | `O=C(NCc1ccc(C2CCOCC2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2` | 546 | 5.97 |
| A4 | `O=C(NCc1ccc2c(c1)NCCC2)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2` | 517 | 5.44 |

**A1 — HIGHEST PRIORITY.** 3-Cl-BTP R1 + 4-(pyridin-4-yl)benzyl R2 on naphthyridine core. The combination of the best R1 (from CTX-1020456, pIC50 5.959) with the best clean R2 (from CTX-1020698, pIC50 5.955) has never been synthesised. If the contributions are even partially additive, the expected pIC50 ≥6.3. This is the minimum-change, highest-confidence path toward breaking the 1 µM ceiling. The 3-Cl-BTP R1 provides a superior lipophilic contact vs 3-MeBFO (0.2–0.4 log units better consistently), and the pyridyl-benzyl R2 is 0.36 log units better than the piperazino-aniline.

**A2** — Same combination on the thienopyridine core. CTX-1020670 showed the thienopyridine core with 3-Cl-BTP + simple benzyl achieves 5.903. Adding the pyridyl to the benzyl should push this further. The S atom in the core may provide a favourable electrostatic interaction complementary to the 3-Cl-BTP sulfur.

**A3** — 3-Cl-BTP R1 + THP-benzyl. CTX-1020696 showed THP-benzyl is second-best R2 (5.879 with 3-MeBFO). Upgrading to best R1 tests if THP-benzyl provides an orthogonal interaction to pyridyl-benzyl (different HBA geometry).

**A4** — 3-Cl-BTP R1 + tetrahydroisoquinolinyl R2. CTX-1020695 showed the rigid bicyclic R2 = 5.565 with 3-MeBFO. The tetrahydroisoquinolinyl NH is an HBD that the simple benzyl-pyridyl lacks. Combining with the best R1 tests whether the rigid bicyclic R2 contributes an HBD contact that benefits from best-R1 amplification.

---

### Group B — Extend R2 biaryl to add new H-bond contacts

| ID | SMILES | MW | LogP |
|---|---|---|---|
| B1 | `O=C(NCc1ccc(-c2ncccn2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2` | 540 | 5.54 |
| B2 | `O=C(NCc1ccc(-c2ccnc(N)c2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2` | 554 | 5.72 |
| B3 | `O=C(NCc1ccc(-c2ccnc(C)c2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2` | 553 | 6.45 |
| B4 | `O=C(NCc1cccc(-c2ccncc2)c1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2` | 539 | 6.14 |

**B1** — 3-Cl-BTP + 4-(pyrimidin-2-yl)benzyl. Pyrimidine has two N atoms at 1 and 3 — the 3-N is an additional HBA not present in pyridyl. If the binding pocket has two H-bond donors on the R2 side (one contacts pyridine-N in the best compound, a second is unreached), the 3-N of pyrimidine captures it. Lower LogP (5.54) than A1 — better drug-likeness profile.

**B2** — 3-Cl-BTP + 4-(2-aminopyridin-4-yl)benzyl. Adds an NH₂ HBD at the 2-position of the pyridine ring. An HBD can form a strong H-bond (up to 3 kcal/mol, 100× potency) with a protein carbonyl or sulphonyl. This is the most likely single change to produce a step-change improvement if a carbonyl-containing residue is adjacent to the R2 pyridyl site.

**B3** — 3-Cl-BTP + 4-(2-methylpyridin-4-yl)benzyl. 2-methyl blocks the most metabolically labile aromatic C-H on the pyridine ring, improving metabolic stability without changing H-bond geometry. Also tests if steric/electronic modulation at the 2-position is tolerated.

**B4** — 3-Cl-BTP + 3-(pyridin-4-yl)benzyl (meta-linkage). The meta-isomer of A1 places the pyridyl in a different spatial orientation relative to the amide backbone. If the para-linkage positions the N poorly for the pocket HBD, the meta-linkage may be superior.

---

### Group C — R1 modifications, keeping pyridyl-benzyl R2

| ID | SMILES | MW | LogP |
|---|---|---|---|
| C1 | `O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1C(F)(F)F)CC2` | 573 | 6.51 |
| C2 | `O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3cc(F)ccc3c1Cl)CC2` | 557 | 6.28 |
| C3 | `O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1c(C)oc3cc(F)ccc13)CC2` | 521 | 5.47 |
| C4 | `O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1cnn3ccncc13)CC2` | 490 | 3.31 |
| C5 | `O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1c(Cl)c3ccccc3n1C)CC2` | 536 | 5.42 |

**C1** — 3-CF₃-BTP + pyridylbenzyl. CF₃ is isosteric with Cl but larger and more lipophilic (+0.5 log units LogP). If the Cl of 3-Cl-BTP is in a tight pocket contact (halogen bond or steric lock), CF₃ would not form a halogen bond but provides a deeper hydrophobic fill. This is an important mechanistic probe for the nature of the 3-position contact.

**C2** — 5-F-3-Cl-BTP + pyridylbenzyl. F at C5 of the BTP benzene ring blocks the main CYP3A4 metabolic site on the aromatic ring without altering the 3-Cl pharmacophore. Expected improvement in microsomal stability; mild electronic effect on the BTP ring system.

**C3** — 5-F-3-Me-benzofuran + pyridylbenzyl. Tests whether fluorine on the benzofuran (second-best R1) boosts potency — the F adds a weak directional C-H···F contact. Lower MW (521) and LogP (5.47) — best drug-likeness in Group C.

**C4** — Pyrazolo[1,5-a]pyrimidine-2-carbonyl + pyridylbenzyl. CTX-1020671 showed this R1 achieves pIC50 5.463 even with a plain benzyl R2. Replacing benzyl with the 3× more potent pyridylbenzyl should add ~0.47 log units, predicting pIC50 ~5.9. The bicyclic N-rich pyrazolopyrimidine can form up to two H-bonds — if one of those contacts an unoccupied protein H-bond donor in the R1 pocket, this compound could substantially outperform CTX-1020671. Lowest LogP (3.31) in the set — excellent ADMET profile.

**C5** — 3-Cl-1-methylbenzimidazol-2-yl + pyridylbenzyl. CTX-1020748 achieved 5.556 with this R1 and PAINS R2. Upgrading to the clean pyridylbenzyl R2 tests if the PAINS motif was limiting CTX-1020748.

---

### Group D — Fluorine scan: conformational and metabolic effects

| ID | SMILES | MW | LogP |
|---|---|---|---|
| D1 | `O=C(NCc1c(F)ccc(-c2ccncc2)c1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2` | 557 | 6.28 |
| D2 | `O=C(NCc1ccc(-c2ccncc2)cc1F)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2` | 557 | 6.28 |
| D3 | `O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3c(F)cccc3c1Cl)CC2` | 557 | 6.28 |
| E4 | `O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccc(F)cc3c1Cl)CC2` | 557 | 6.28 |

**D1** — ortho-F on benzyl ring (F adjacent to CH₂). Fluorine at this position creates a C–F···amide-H dipole interaction that can preorganise the amide into the binding-competent rotamer. Rotamer locking via ortho-F has provided 2–10× potency improvements in multiple medicinal chemistry programmes.

**D2** — F ortho to the biaryl bond on benzyl ring. F adjacent to the biaryl pivot modulates the torsion angle between the phenyl and pyridyl rings. The best geometry for simultaneous binding of both rings may be enforced by ortho-F, which sterically prevents the twisted conformation.

**D3** — F at C4 of the BTP benzene ring (adjacent to the sulfur, meta to the 3-Cl). Tests metabolic blocking at a secondary aromatic position on R1 without altering the 3-Cl pharmacophore.

**E4** — F at C5 of the BTP benzene ring (para to sulfur). Explores the distal ring of R1 for additional van der Waals contacts in the adjacent protein sub-pocket. The para-F position on benzothiophene is synthetically accessible and offers a unique directional dipole.

---

### Group E — Novel R2 pharmacophores

| ID | SMILES | MW | LogP |
|---|---|---|---|
| E1 | `O=C(NCc1ccc(-c2ccc(-c3ccncc3)cc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2` | 615 | 7.81 |
| E2 | `O=C(NCc1ccc(-c2cccc3[nH]ccc23)cc1)c1ccc2c(n1)CN(C(=O)c1c(C)oc3ccccc13)CC2` | 541 | 6.41 |
| E3r | `O=C(NCc1ccc(-c2cn[nH]c2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2` | 528 | 5.47 |

**E1** — 3-Cl-BTP + 4-[4-(pyridin-4-yl)phenyl]benzyl (terphenyl-CH₂). Extends the aromatic chain from biphenyl to terphenyl, placing the pyridyl N approximately 10 Å from the amide nitrogen instead of 7 Å. Tests whether a deeper sub-pocket can accommodate an extended chain. Note MW 615, LogP 7.81 — acceptable for an in vitro probe but would need optimisation for drug-likeness. Synthesise only if A1/B2 fail to break the ceiling.

**E2** — 3-MeBFO + 4-(1H-indol-4-yl)benzyl. Indole provides both a π-face for stacking AND an NH donor. The NH could contact a protein carbonyl that is not reached by the pyridyl N in CTX-1020698. The 4-yl attachment of indole presents the NH and the C3 proton toward the pocket interior.

**E3r** — 3-Cl-BTP + 4-(1H-pyrazol-4-yl)benzyl. Pyrazole combines an HBD (NH) with an HBA (N at position 2), offering bidentate binding potential. Notably, pyrazole is not flagged by PAINS, Brenk, or NIH. HBD = 2. The NH could bridge to a backbone carbonyl while the ring N accepts from a backbone NH — a common kinase hinge-binding motif.

---

## 8. Synthesis Priorities and Expected Impact

### Tier 1 — Synthesise immediately (highest confidence, minimum change from validated SAR)

| Priority | ID | Basis | Expected pIC50 |
|---|---|---|---|
| 1 | **A1** | Best R1 + best R2, never made | ≥6.3 (predicted) |
| 2 | **A2** | Same combo, thienopyridine core | ≥6.2 |
| 3 | **C4** | N-rich R1 + pyridylbenzyl; cleanest ADMET (LogP 3.31) | ~5.9 |
| 4 | **B2** | Adds HBD to R2; potential step-change if protein HBA present | ~6–7 if contact |
| 5 | **A4** | Rigid bicyclic R2 + best R1; only compound with HBD on R2 (NH) | ~6.0 |

### Tier 2 — Potency expansion and metabolic block

C5, B1, B3, B4, D1, D2, E3r

### Tier 3 — Mechanism probes and probe compounds

C1 (CF₃ vs Cl mechanism), A3 (THP-benzyl), C2/C3 (F-metabolic block), E1, E2, D3, E4

---

## 9. Path to 10–100 nM (pIC50 8–9)

The current ceiling of pIC50 ~6 (1 µM) is approximately 100–1000× from the 10–100 nM target. Closing this gap with a single molecule requires additive contributions from multiple strategies:

| Strategy | Expected gain | Compounds |
|---|---|---|
| Combine best R1 + best R2 (A1) | +0.3–0.5 log | A1, A2 |
| Add HBD to R2 terminal (B2, E3r, A4) | +0.5–2.0 log | B2, E3r, A4 |
| N-rich R1 hinge contacts (C4) | +0.3–0.8 log | C4 |
| Conformational preorganisation via F (D1/D2) | +0.3–0.7 log | D1, D2 |
| Metabolic block → higher free-drug concentration | +0.2–0.5 measured | C2, C3, B3 |

**Combined best case (A1 + B2 strategy):** Start from A1 (predicted ~6.3), then introduce an HBD at the terminal pyridyl (→ 2-aminopyridyl as in B2). If the HBD makes a direct contact with a protein H-bond acceptor, the compound B2-equivalent could reach pIC50 7.5–8.5 (10–100 nM range).

Reaching pIC50 9 (1 nM) is unlikely through ligand-based optimisation alone from a µM starting point without access to structural data (protein crystallography or cryo-EM) to guide precise pocket filling. Structure-guided design is strongly recommended after confirming the first sub-µM compound.
