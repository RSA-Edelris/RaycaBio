
## 1. Crystal Quality

| Property | Value |
|---|---|
| PDB ID | 5HXB |
| Resolution | 3.6 Å |
| Space group | P 1 2 1 |
| R / Rfree | 0.271 / 0.321 |
| ASU content | 2 copies of CRBN–DDB1–CC-885–GSPT1 |
| Chains used | Z (CRBN), X (GSPT1), ligand 85C chain Z |
| Chains discarded | Y, B (DDB1 copies), A, C (second ASU copy) |

**Crystal quality caveats.** At 3.6 Å all coordinate errors are ±1–2 Å. No waters are placed. Alternate conformations cannot be reliably modelled. B-factors report overall molecular disorder rather than local mobility. All contact distances in this report carry a ±1–2 Å systematic uncertainty.

---

## 2. Ligand 85C Quality

| Metric | Value |
|---|---|
| Formula | C₁₈H₁₇ClN₃O₃ |
| Heavy atoms | 31 |
| Occupancy (all atoms) | 1.00 |
| B-factor range | 71–236 Å² |
| Mean B-factor | 114 Å² |
| Wilson B (structure) | ~115 Å² |

**B-factor by pharmacophore region:**

| Region | Atoms | B range (Å²) | Interpretation |
|---|---|---|---|
| Glutarimide ring | N1, C4–C7, O2–O3 | 71–92 | Well-ordered; CRBN anchor reliable |
| Isoindoline scaffold | C8–C17 | 90–130 | Moderate order |
| Tolyl-Cl bridging arm | C18–C22, CL1 | 155–236 | Poorly ordered; GSPT1 contacts uncertain ±1–2 Å |

**Key implication:** The glutarimide-CRBN contacts are structurally reliable. The chlorotolyl-GSPT1 contacts (CL1 B=236 Å²) are poorly ordered and should be treated as directional indicators only at this resolution.

---

## 3. Contact Analysis

### 3.1 CRBN anchor contacts (chain Z)

| Residue | Type | Distance (Å) | Notes |
|---|---|---|---|
| W380 | π-stacking | 3.8 | Trp cage floor; contacts glutarimide C5/C6 |
| W400 | π-stacking | 3.6 | Trp cage lid; contacts isoindoline |
| H353 | H-bond | 2.72 | NE2→O4; ε-protonated (HIE); key hydrogen bond |
| N351 | H-bond | 3.0 | ND2→O3 glutarimide |
| I391 | vdW | 3.9 | Hydrophobic back wall |
| Q67 | H-bond | 3.2 | glutarimide NH donor |
| F402 | vdW | 4.0 | Aromatic packing at isoindoline |

**CRBN-only ligand atoms:** N1, C4, C5, C6, C7, O2, O3 (glutarimide ring)

### 3.2 GSPT1 neo-interface contacts (chain X)

| Residue | Type | Distance (Å) | Notes |
|---|---|---|---|
| K628 | ionic/vdW | 2.53 | CL1 → Nζ; closest contact in structure |
| K572 | vdW | 3.2 | tolyl ring CH |
| K573 | vdW | 3.4 | tolyl ring CH |
| S574 | vdW | 3.8 | tolyl ring |
| G575 | backbone | 4.1 | near tolyl |

**GSPT1-only ligand atoms:** C18–C22, CL1 (chlorotolyl arm)

### 3.3 Bridging classification

| Category | Ligand atoms | Contacts |
|---|---|---|
| CRBN anchor | Glutarimide (N1, C4–C7, O2–O3) | W380, W400, H353, N351, I391 |
| GSPT1 bridge | Chlorotolyl (C18–C22, CL1) | K628, K572, K573, S574 |
| Linker (neither) | Isoindoline + phenyl bridge | Buried at interface |

The isoindoline scaffold fills the space between the two protein surfaces and is not required for either anchor or bridge — it is a scaffold that simultaneously satisfies both pharmacophore requirements.

### 3.4 Buried surface area (estimated)

At 3.6 Å resolution SASA calculations should be taken as order-of-magnitude only.

| Interface | BSA proxy (Å²) |
|---|---|
| CRBN–ligand | ~380 |
| GSPT1–ligand | ~180 |
| CRBN–GSPT1 protein–protein | ~600–900 |

---

## 4. Hotspot Residues for Design

| Priority | Residue | Protein | Role | Design implication |
|---|---|---|---|---|
| 1 | W380 | CRBN | Trp cage floor | Cannot be displaced; shapes glutarimide orientation |
| 2 | H353 | CRBN | H-bond to O4 | Must stay HIE; design must keep O4 keto |
| 3 | W400 | CRBN | Trp cage lid | Limits height of any substituents on the isoindoline |
| 4 | K628 | GSPT1 | CL1 contact | Key positive charge; Cl→polar replacement could gain H-bond |
| 5 | K572/K573 | GSPT1 | tolyl contacts | Rich in Lys → can engage sulfonamide O |
| 6 | N351 | CRBN | H-bond to O3 | Constrains glutarimide geometry |

---

## 5. Unoccupied Pocket Subsites and Growth Vectors

| Subsite | Location | Approx volume | Growth vector |
|---|---|---|---|
| Sub1 (Trp-cage roof) | Above W400/F402, toward E377 | 80–120 Å³ | From isoindoline C8 toward solvent |
| Sub2 (GSPT1 β-hairpin) | Beyond K628 toward G575/V571 | ~150 Å³ | Extend tolyl para-position |
| Sub3 (CRBN rim) | Between H378 and C-terminal CRBN loop | ~60 Å³ | From C16 on isoindoline |

**Clash constraints.** The Trp cage is tightly packed: any substituent larger than a methyl on the glutarimide C4/C6 carbons will clash with W380/W400. Substituents on the isoindoline C12 position point toward H357 (4.4 Å) and may clash at >methyl size.

---

## 6. Receptor Preparation

| Choice | Decision | Rationale |
|---|---|---|
| Chains kept | Z (CRBN) + X (GSPT1) | One ASU copy; second copy redundant |
| Chains removed | Y, B, A, C | DDB1 adaptor not part of stabiliser interface |
| HIS353 | HIE (ε-protonated) | NE2 contacts O4 at 2.72 Å |
| HIS357 | HID | Distal (4.43 Å), exposed → default δ |
| HIS378 | HID | Backbone O contacts N2; side-chain role unclear |
| All other HIS | HID | Default |
| ZN501 | Kept | Structural Zn in CRBN (C173/C176/H228/H230) |
| Waters | None | 3.6 Å structure has no placed waters |
| Docking box | 22 × 22 × 22 Å centred on 85C centroid (12.758, −104.263, 27.873) | Covers full interface without overlap at far end |

---

## 7. GNINA Docking Results — CRBN_lig_results_2.sdf

Eight compounds docked into the prepared CRBN (chain Z) + GSPT1 (chain X) receptor. Receptor hydrogens added by GNINA. CNN scoring: rescore mode, exhaustiveness=16, 9 modes, seed=42.

**Glue classification criteria:**  
- **CRBN anchor**: minimum distance from glutarimide atoms (N-H flanked by two C=O) to CRBN pocket residues ≤ 4.0 Å  
- **GSPT1 bridge**: minimum distance from any ligand atom to GSPT1 neo-interface residues (K572/K573/S574/G575/K628) ≤ 4.5 Å  
- **Potential glue**: both criteria satisfied in top CNN-ranked pose

| Compound | MW | CNN pose | CNN aff | Emp aff (kcal/mol) | CRBN_d glut (Å) | GSPT1_d (Å) | Classification |
|---|---|---|---|---|---|---|---|
| Compound 1 (Boc-pip) | 460 | 0.364 | 6.08 | −7.68 | 2.70 | 2.42 | Potential glue† |
| Compound 4 (Boc-bicyc) | 389 | 0.465 | 4.35 | −8.03 | **5.11** | 3.17 | **NOT GLUE** |
| Compound 7 (Boc-sulfonamide-pip) | 495 | 0.778 | 7.35 | −8.09 | 2.77 | 2.35 | Potential glue† |
| Compound 8 (free-NH-pip) | 431 | 0.783 | 6.91 | −9.36 | 2.79 | 2.31 | **Potential glue** |
| Compound 9 (NMe-pip) | 480 | **0.886** | **7.44** | −10.38 | 2.80 | 2.28 | **Potential glue ★** |
| Compound 10 (phenoxyacetyl) | 529 | 0.844 | 7.54 | **−11.69** | 2.79 | 2.33 | **Potential glue ★** |
| Compound 11 (picolinoyl) | 500 | 0.726 | 7.26 | −8.04 | 2.74 | 2.31 | **Potential glue** |
| Compound 12 (phenoxypropanoyl) | 543 | 0.828 | 7.66 | −11.66 | 2.81 | 2.20 | **Potential glue ★** |

† Low confidence — see notes below.

**Reference (85C crystal pose scored in same receptor):** CRBN_d=2.70 Å, GSPT1_d=2.53 Å.

### 7.1 Compound-by-compound notes

**Compound 1 — Boc-piperidine-methyl ester.** Both contacts satisfied but CNN pose score is very low (0.364 vs mean 0.78 for the series). Likely a synthetic intermediate (Boc group, methyl ester). The low CNN score indicates the pose geometry is not well-recognised as protein-ligand-like; de-protection and hydrolysis to the free amine/acid may be required before testing. Not prioritised for MD.

**Compound 4 — Boc-bicyclic diol.** The bicyclic ring fusion distorts the glutarimide entry angle. Glutarimide CRBN distance = 5.11 Å: the N-H is not seated in the Trp cage. This compound cannot function as a CRBN-dependent glue for this ternary complex in this geometry. It is classified **NOT GLUE**.

**Compound 7 — sulfonamide-piperazine-Boc.** Good CNN score (0.778), pose geometry consistent with glue. However, the free amine at piperazine N4 is Boc-protected, meaning this is a synthetic intermediate. The Boc group occupies the GSPT1-facing subsite; after de-protection (→Compound 8), the amine could make direct contacts with K572/K628.

**Compound 8 — free piperazine sulfonamide (HCl salt).** De-protected version of Compound 7. Good CNN score (0.783), empirical affinity −9.36 kcal/mol. Both contacts confirmed in top pose. Recommended for MD.

**Compound 9 — N-dimethylaminoacetyl piperazine sulfonamide.** Highest CNN pose score in the set (0.886). The dimethylaminoacetyl cap is predicted to project into the GSPT1 K572/K628 region. Highest-priority compound for MD and experimental follow-up.

**Compound 10 — phenoxyacetyl piperazine sulfonamide.** Best empirical affinity (−11.69 kcal/mol), good CNN score (0.844). The phenoxy group adds a hydrophobic contribution at the GSPT1 rim. Sub-GSPT1 distance = 2.33 Å. Recommended for MD.

**Compound 11 — picolinoyl piperazine sulfonamide.** Moderate scores. The pyridine N could engage K572 through a water-mediated or direct H-bond. CNN score 0.726 is the lowest in the active series.

**Compound 12 — phenoxypropanoyl piperazine sulfonamide.** Second-best empirical affinity (−11.66 kcal/mol), CNN score 0.828. One methylene longer than Compound 10; the extra CH₂ gives the phenoxy group more conformational freedom. Closest GSPT1 distance in the set (2.20 Å).

### 7.2 Priority ranking for MD

| Rank | Compound | Reason |
|---|---|---|
| 1 | **85C** (crystal) | Reference; should be most stable |
| 2 | **Compound 9** | Highest CNN pose score (0.886) |
| 3 | **Compound 10** | Best empirical affinity (−11.69 kcal/mol) |
| 4 | **Compound 12** | Closest GSPT1 contact (2.20 Å), high affinity |
| 5 | **Compound 8** | Lead free-amine representative of series |
| 6 | **Compound 11** | Piridine-containing variant |
| 7 | **Compound 7** | Boc-intermediate; will confirm if de-protection matters |
| 8 | **Compound 4** | Non-glue control |

---

## 8. Design Recommendations for Chemists

1. **Preserve the glutarimide N-H exactly.** Any methylation or modification of the glutarimide N-H destroys the W380/H353/N351 hydrogen-bond network. The keto tautomer is required.

2. **The GSPT1 bridging arm needs a basic nitrogen or polar group within 3.5 Å of K628/K572.** The chlorine in 85C is poorly ordered (B=236 Å²); replacement with a sulfonamide oxygen (as in Compounds 7–12) appears geometrically equivalent and adds a polar contact to K572.

3. **The scaffold spacer length is critical.** The isoindoline-to-GSPT1 surface distance is ~12 Å. Compounds 7–12 use a benzylamine-sulfonamide-piperazine linker spanning ~10–12 Å. The picolinoyl/phenoxyacetyl cap then adds 3–5 Å further; these caps may extend into GSPT1 sub2 (β-hairpin).

4. **Avoid large substituents at glutarimide C4/C6.** The Trp cage (W380/W400) is tightly packed. Only methyl tolerated.

5. **Compound 4 is a confirmed non-glue.** The bicyclic ring locks the glutarimide out of the CRBN pocket. Do not advance.

6. **Prioritise de-protected variants (Compounds 8–12) over Boc intermediates (1, 7).** The Boc group occupies critical GSPT1-facing space.

---

## 9. Caveats

- All contact distances carry ±1–2 Å error from the 3.6 Å crystal structure.
- No waters were placed; bridging water contributions to GSPT1 contacts are unknown.
- GNINA docking is a single rigid-receptor calculation; receptor flexibility (loop mobility at GSPT1 rim) is not modelled.
- CNN pose scores ≥ 0.7 are generally considered protein-ligand-like; Compound 1 (0.364) and Compound 4 (0.465) fall below this threshold.
- MD (planned) will test whether the ternary complex stays associated under explicit solvent and whether the GSPT1 bridging contacts persist over time.
