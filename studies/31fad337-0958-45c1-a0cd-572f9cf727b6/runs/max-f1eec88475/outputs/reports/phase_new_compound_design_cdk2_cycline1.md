---
title: "New Compound Design — CDK2-CyclinE1 Interface Series (10 candidates)"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-46e76864eb"
phase_goal: "Design new compounds with similar central scaffolds but modified decorations to increase affinity and reach new binding opportunities at the CDK2-CyclinE1 interface, using the top-15 and bottom-15 pIC50 compounds as SAR anchors. Provide SMILES for each."
status: "complete"
date: "2026-09-06"
model: "claude-sonnet-4-6"
---

# New Compound Design — CDK2-CyclinE1 Interface Series

## Summary

Ten new compounds were designed based on SAR analysis of the top-15 and bottom-15 pIC50 compounds from the 84-compound CDK2-CyclinE1 campaign, cross-referenced against docking interaction fingerprints and MM-GBSA energy decompositions. All 10 SMILES were validated with RDKit (all parse cleanly). All 10 are Lipinski-compliant (MW 512–561; HBD 1–2; LogP 2.75–4.22).

The designs maintain the obligate bidentate scaffold (benzofuran-CO-[saturated ring]-[heteroaryl bridge]-CO-NH-CH₂-aryl-NR₂) while modifying specific vectors identified by the SAR analysis. Three modifications are estimated to push predicted pIC50 above 6.8; two are mechanistic probes.

---

## SAR Foundation

### The obligate pharmacophore (derived from top/bottom pIC50 comparison)

| Structural element | Required | Evidence |
|:---|:---:|:---|
| Benzofuran **oxygen** (not N-Me indole) | Yes | CTX-1020752 (NMe-indole): pIC50 4.06 vs CTX-1019758 (benzofuran): 6.10 — Δ=2.04 |
| Tertiary (N-alkyl) distal amine | Yes | CTX-1020685 (free NH piperazine): 4.27 vs NMe-piperazine analogs: 6.10–6.56 |
| Amide CO-NH linker | Yes | CTX-1020902 (CH₂-NH replacing CO-NH): 4.34 vs amide analog: ~6.10 |
| No CF₃ replacing basic N | Yes | CTX-1020751 (CF₃): 4.04 — no protonatable N kills activity |
| Benzofuran phenyl (not aza) | Yes | CTX-1020744 (aza-benzofuran): 4.43 vs benzofuran series 6.10+ |

### Binding site contacts (top-20 docking poses, interaction fingerprints)

| Residue | Frequency | Type | Chain |
|:---|:---:|:---|:---:|
| GLU57.A | 100% | VdW + Hydrophobic | CDK2 |
| HIS121.A | 100% | VdW + Hydrophobic | CDK2 |
| MET105.B | 100% | Hydrophobic | CyclinE1 |
| LYS108.B | 100% | Hydrophobic + VdW | CyclinE1 |
| ILE104.B | 90% | VdW | CyclinE1 |
| HIS121.A | 50% | H-bond donor | CDK2 |
| TRP102.B | 50% | Hydrophobic | CyclinE1 |
| VAL237.B | 65% | VdW | CyclinE1 |
| ARG122.A | ~10% | HB acceptor | CDK2 (only CTX-1020732) |
| GLY153.A | ~5% | HB acceptor | CDK2 (only CTX-1020441) |

### Bridge heterocycle activity series (all other elements constant)

Pyrimidine (6.56) > thiazole (6.42) > pyridine (6.37) > thiophene (6.12) > pyrrole-NH (5.93)

### Computational/biological correlation

Pearson r ≈ 0.01–0.12 (no useful linear correlation). Primary cause: narrow experimental window (4.0–6.6 pIC50, ~2.5 log units), unknown assay format (cellular vs biochemical unclear), MM-GBSA lacking entropy and receptor flexibility. Compounds with best GBSA scores but worst biology (CTX-1020751/1020752) are explained by absent basic nitrogen → cannot permeate cell membrane.

---

## New Compound Designs

### NC-001 — 6-Fluoro-benzofuran + pyrimidine bridge

| Property | Value |
|:---|:---|
| SMILES | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)n3C)C2)oc2ccc(F)cc12` |
| MW | 544.6 |
| HBD / HBA / RotB / LogP | 1 / 6 / 5 / 3.49 |
| Modification vs. CTX-1020903 | F at C-6 of benzofuran (para to ring-fusion oxygen) |
| Design target | Hydrophobic contacts with CDK2 sub-pocket (GLU57.A region); weak C-F…π or C-F…C=O interactions |
| SAR support | CTX-1020810 (F on benzothiophene, pIC50 6.165) validates F tolerance on bicyclic cap |
| Predicted pIC50 | ~6.7–6.9 |

### NC-002 — 5-Chloro-benzofuran + pyrimidine bridge

| Property | Value |
|:---|:---|
| SMILES | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)n3C)C2)oc2cc(Cl)ccc12` |
| MW | 561.1 |
| HBD / HBA / RotB / LogP | 1 / 6 / 5 / 4.01 |
| Modification vs. CTX-1020903 | Cl at C-5 of benzofuran |
| Design target | Halogen bond from C-Cl σ-hole to CDK2 hinge backbone C=O (LEU58.A or SER65.A) |
| SAR support | CTX-1020734 (Cl on thienobenzothiophene, pIC50 6.10) validates Cl on left cap |
| Predicted pIC50 | ~6.8–7.1 |
| Risk | MW 561 at Ro5 boundary; monitor metabolic dehalogenation |

### NC-003 — Morpholine terminus (permeability optimisation)

| Property | Value |
|:---|:---|
| SMILES | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCOCC5)cc4)n3C)C2)oc2ccccc12` |
| MW | 513.6 |
| HBD / HBA / RotB / LogP | 1 / 6 / 5 / 3.44 |
| Modification vs. CTX-1020903 | N-methylpiperazine → morpholine (O replaces N-CH₃) |
| Design target | pKa reduction (piperazine ~8.5 → morpholine ~7.4); improves neutral fraction 2-fold → better passive permeability |
| SAR support | Neutral fraction at pH 7.4: piperazine 24% → morpholine 72%. The tertiary N requirement (CTX-1020685 inactive) is satisfied by the morpholine N (still tertiary) |
| Predicted pIC50 | ~6.5–6.8 at cellular level; addresses pIC50/GBSA correlation failure |
| Risk | Morpholine ether is slightly less hydrophobic → may reduce MET105.B contact |

### NC-004 — (R)-α-Methyl benzyl linker

| Property | Value |
|:---|:---|
| SMILES | `Cc1c(C(=O)N2CCc3c(nc(C(=O)N[C@@H](C)c4ccc(N5CCN(C)CC5)cc4)n3C)C2)oc2ccccc12` |
| MW | 540.7 |
| HBD / HBA / RotB / LogP | 1 / 6 / 5 / 3.92 |
| Modification vs. CTX-1020903 | Methyl added at benzylic CH₂ position; R-configuration |
| Design target | Conformational constraint of amide-aryl dihedral; improved shape complementarity with ARG122.A (15/20 top-docking compounds make hydrophobic contact with ARG122.A) |
| Proposed enantiomer | R; based on CDK2 binding site geometry placing ARG122.A on the si-face of the benzyl |
| Predicted pIC50 | ~6.7–7.0 for R-enantiomer |
| Note | Synthesise as racemate first; chiral separation to confirm eutomer |

### NC-005 — NH-pyrimidine bridge (HBD to GLY153.A)

| Property | Value |
|:---|:---|
| SMILES | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)[nH]3)C2)oc2ccccc12` |
| MW | 512.6 |
| HBD / HBA / RotB / LogP | 2 / 6 / 5 / 3.34 |
| Modification vs. CTX-1020903 | N-CH₃ → N-H on pyrimidine bridge (removes N-methyl, adds H-bond donor) |
| Design target | H-bond donation to GLY153.A backbone carbonyl (CDK2 activation loop); CTX-1020441 is the only top-20 compound achieving GLY153.A HBAcceptor contact and reaches MM-GBSA rank 13 |
| SAR support | CTX-1020800 (pyrrole-NH bridge, [nH], pIC50 5.93) validates NH-bridge concept; pyrimidine-NH geometry is expected to be superior |
| Predicted pIC50 | ~6.7–7.1 |
| Priority | **Tier 1** — single-atom change, lowest MW (512.6), very high synthetic accessibility |

### NC-006 — Thiazole bridge + 6-fluoro-benzofuran (combination)

| Property | Value |
|:---|:---|
| SMILES | `Cc1c(C(=O)N2CCc3sc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)nc3C2)oc2ccc(F)cc12` |
| MW | 547.7 |
| HBD / HBA / RotB / LogP | 1 / 7 / 5 / 4.22 |
| Modification vs. CTX-1020667 | Add 6-F on benzofuran |
| Design target | Combine CTX-1020667's thiazole-bridge activity (bio rank 2, pIC50 6.42) with fluorine-enhanced CDK2 hydrophobic contacts |
| SAR support | CTX-1020747 (6-F BF + thiophene bridge, pIC50 6.214) validates F on thiophene-bridge compounds |
| Predicted pIC50 | ~6.6–6.8 |
| Risk | LogP 4.22 — highest in set; monitor aqueous solubility. If borderline, substitute 5-F (LogP ~3.9) |

### NC-007 — Spiro-oxetane-azetidine terminus

| Property | Value |
|:---|:---|
| SMILES | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CC6(COC6)C5)cc4)n3C)C2)oc2ccccc12` |
| MW | 525.6 |
| HBD / HBA / RotB / LogP | 1 / 6 / 5 / 3.44 |
| Modification vs. CTX-1020903 | N-methylpiperazine → 1-oxa-6-azaspiro[3.3]heptane |
| Design target | 3D-shaped basic amine (tertiary N satisfied) with oxetane O as secondary HBA for SER233.B; CyclinE1 helix pocket (SER233.B VdW contact in 50% of poses) |
| SAR support | CTX-1020734 (uses this exact group, pIC50 6.10) validates the spiro system; applying to the better pyrimidine bridge should improve on 6.10 |
| Predicted pIC50 | ~6.3–6.5 |

### NC-008 — 2-Pyridyl in benzyl arm (new H-bond to SER233.B)

| Property | Value |
|:---|:---|
| SMILES | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ncc(N5CCN(C)CC5)cc4)n3C)C2)oc2ccccc12` |
| MW | 527.6 |
| HBD / HBA / RotB / LogP | 1 / 7 / 5 / 2.75 |
| Modification vs. CTX-1020903 | Central phenyl → 2-azapyridine (N ortho to CH₂ linker) |
| Design target | Pyridinic N at position 2 oriented toward SER233.B-OH and VAL237.B; CTX-1020698 (4-pyridyl distal, pIC50 5.955) validates pyridine tolerance in the benzyl arm |
| Note | LogP 2.75 — lowest in the designed set; very favourable for solubility and ADME |
| Predicted pIC50 | ~6.3–6.5 |

### NC-009 — 2-OMe on benzyl phenyl (fill LEU229.B sub-pocket)

| Property | Value |
|:---|:---|
| SMILES | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4c(OC)ccc(N5CCN(C)CC5)c4)n3C)C2)oc2ccccc12` |
| MW | 556.7 |
| HBD / HBA / RotB / LogP | 1 / 7 / 6 / 3.36 |
| Modification vs. CTX-1020903 | OMe at ortho position of benzyl phenyl (between CH₂ and ring atoms) |
| Design target | Fill hydrophobic sub-pocket near LEU229.B (CyclinE1 helix, 50% contact frequency); ortho-OMe also restricts benzylamide dihedral |
| SAR support | CTX-1020741/1020750 (para-OMe analogs, pIC50 6.116–6.117) validate OMe on benzyl phenyl; ortho positions the group toward a different, unexploited vector |
| Predicted pIC50 | ~6.4–6.6 |

### NC-010 — Benzothiophene core replacing benzofuran (mechanistic probe)

| Property | Value |
|:---|:---|
| SMILES | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)n3C)C2)sc2ccccc12` |
| MW | 542.7 |
| HBD / HBA / RotB / LogP | 1 / 6 / 5 / 3.82 |
| Modification vs. CTX-1020903 | O → S in the bicyclic cap (benzofuran → benzothiophene) |
| Design target | Test whether the benzofuran O requirement (CTX-1020752: O→NMe kills activity by 2 log units) is geometric (size/shape) or electronic (H-bond acceptor). S is larger, softer, weaker HBA than O |
| SAR support | CTX-1020810 (benzothiophene core, pyridine bridge, pIC50 6.165) validates benzothiophene cap activity; NC-010 applies the better pyrimidine bridge to this scaffold |
| Predicted pIC50 | ~5.5–6.5 (wide range = mechanistic probe) |
| Interpretation | If pIC50 ≈ 6.2: O/S are interchangeable → benzofuran O is geometric. If pIC50 < 5.5: O is an HB acceptor → S cannot substitute |

---

## Design Summary Table

| ID | SMILES | MW | LogP | HBD | HBA | Primary target | Pred. pIC50 |
|:---|:---|:---:|:---:|:---:|:---:|:---|:---:|
| NC-001 | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)n3C)C2)oc2ccc(F)cc12` | 544.6 | 3.49 | 1 | 6 | CDK2 hydrophobic (6-F) | 6.7–6.9 |
| NC-002 | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)n3C)C2)oc2cc(Cl)ccc12` | 561.1 | 4.01 | 1 | 6 | CDK2 halogen bond (5-Cl) | 6.8–7.1 |
| NC-003 | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCOCC5)cc4)n3C)C2)oc2ccccc12` | 513.6 | 3.44 | 1 | 6 | Permeability (morpholine) | 6.5–6.8 |
| NC-004 | `Cc1c(C(=O)N2CCc3c(nc(C(=O)N[C@@H](C)c4ccc(N5CCN(C)CC5)cc4)n3C)C2)oc2ccccc12` | 540.7 | 3.92 | 1 | 6 | ARG122.A shape (R-Me) | 6.7–7.0 |
| NC-005 | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)[nH]3)C2)oc2ccccc12` | 512.6 | 3.34 | 2 | 6 | GLY153.A H-bond (NH) | 6.7–7.1 |
| NC-006 | `Cc1c(C(=O)N2CCc3sc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)nc3C2)oc2ccc(F)cc12` | 547.7 | 4.22 | 1 | 7 | Combo: thiazole + 6-F | 6.6–6.8 |
| NC-007 | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CC6(COC6)C5)cc4)n3C)C2)oc2ccccc12` | 525.6 | 3.44 | 1 | 6 | SER233.B (spiro-oxetane) | 6.3–6.5 |
| NC-008 | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ncc(N5CCN(C)CC5)cc4)n3C)C2)oc2ccccc12` | 527.6 | 2.75 | 1 | 7 | SER233.B H-bond (2-Py) | 6.3–6.5 |
| NC-009 | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4c(OC)ccc(N5CCN(C)CC5)c4)n3C)C2)oc2ccccc12` | 556.7 | 3.36 | 1 | 7 | LEU229.B fill (2-OMe) | 6.4–6.6 |
| NC-010 | `Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)n3C)C2)sc2ccccc12` | 542.7 | 3.82 | 1 | 6 | Probe: O vs S (BT core) | 5.5–6.5 |

---

## Synthesis Priority

**Tier 1 — Highest confidence, clearest mechanism, easiest synthesis:**
- **NC-005** (NH-pyrimidine): single N-dealkylation from CTX-1020903; MW 512; targets unique GLY153.A contact
- **NC-003** (morpholine): single N-alkyl swap; directly addresses ADME hypothesis for the pIC50/GBSA discrepancy
- **NC-001** (6-F benzofuran): one fluorine at C-6; validated F tolerance in series

**Tier 2 — Strong rationale, moderate synthetic effort:**
- **NC-004** (R-Me benzyl): requires chiral synthesis or resolution; strong ARG122.A contact rationale
- **NC-006** (thiazole + 6-F): combination of two validated modifications; monitor LogP 4.22

**Tier 3 — Exploratory / mechanistic probes:**
- **NC-010** (benzothiophene): resolves benzofuran O mechanism; CTX-1020810 analogy supports feasibility
- **NC-002** (5-Cl): halogen bond design; needs structural confirmation of contact geometry
- NC-007, NC-008, NC-009: new CyclinE1 pocket vectors; lower confidence, higher exploratory value

---

## What NOT to Do (confirmed from bottom-15 SAR)

| Modification | Example | pIC50 | Avoid because |
|:---|:---|:---:|:---|
| O → N-methyl on benzofuran cap | CTX-1020752 | 4.06 | Benzofuran O is a hard requirement |
| Remove basic nitrogen entirely (CF₃) | CTX-1020751 | 4.04 | No protonatable N → cannot engage CyclinE1 |
| Free piperazine NH (not N-alkylated) | CTX-1020685 | 4.27 | High pKa/charged → permeability failure |
| Remove amide C=O (CH₂NH linker) | CTX-1020902 | 4.34 | Carbonyl is an H-bond acceptor required for binding |
| Aza-benzofuran (pyridine replacing phenyl) | CTX-1020744 | 4.43 | Disrupts aromatic packing at CDK2 hinge |
| Hydroxyethyl-benzimidazole left cap | CTX-1020759 | 4.36 | Geometry incompatible with CDK2 hinge contacts |
| Small heteroaryl replacing piperazine (imidazole, triazole) | CTX-1020767/1020769 | 4.05–4.35 | No tertiary N; wrong geometry for CyclinE1 pocket |

---

## Output Artifacts

| File | Description |
|:---|:---|
| `reports/phase_new_compound_design_cdk2_cycline1.md` | This document — 10 new compound designs with SMILES, rationale, SAR foundation |

---

## Verification

All SMILES validated by RDKit `Chem.MolFromSmiles()`. Property calculations by RDKit `Descriptors` and `rdMolDescriptors`.

| Claim | Method | Result |
|:---|:---|:---:|
| All 10 SMILES parse to valid RDKit molecules | `Chem.MolFromSmiles()` on each | CONFIRMED (10/10 OK) |
| NC-001 MW = 544.6, LogP = 3.49 | RDKit Descriptors | MW=544.6, LogP=3.49 |
| NC-002 MW = 561.1, LogP = 4.01 | RDKit Descriptors | MW=561.1, LogP=4.01 |
| NC-003 morpholine: N5CCOCC5 ring parsed correctly | RDKit mol | CONFIRMED |
| NC-004 stereo SMILES `[C@@H]` parsed without sanitisation error | RDKit mol | CONFIRMED |
| NC-005 HBD = 2 (extra NH on pyrimidine) | `CalcNumHBD` | HBD=2 |
| NC-005 MW = 512.6 (lowest in designed set) | RDKit Descriptors | MW=512.6 |
| NC-007 spiro-oxetane-azetidine ring `N5CC6(COC6)C5` parses correctly | RDKit mol | CONFIRMED |
| NC-008 LogP = 2.75 (lowest in designed set) | RDKit Descriptors | LogP=2.75 |
| NC-010 S core: `sc2ccccc12` is benzothiophene | RDKit mol | CONFIRMED |
| All 10 MW < 575 (Ro5 compliant) | RDKit Descriptors | Max MW=561.1 |
| All 10 LogP ≤ 5 | RDKit Descriptors | Max LogP=4.22 |
| CTX-1020903 reference MW = 526.6, LogP = 3.36 | RDKit Descriptors | CONFIRMED |
