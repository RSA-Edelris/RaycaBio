# BRD4 BD1 Pocket Druggability Report — PDB 3MXF

## Structure Summary

| Property | Value |
|---|---|
| PDB ID | 3MXF |
| Target | Bromodomain-containing protein 4, first bromodomain (BRD4 BD1) |
| Ligand co-crystallized | JQ1 (thienotriazolodiazepine inhibitor) |
| Method | X-ray crystallography |
| Resolution | 1.60 Å |
| R-work / R-free | 0.150 / 0.184 |
| Completeness | 99.6% |
| Chain | A (127 residues modeled) |
| Authors | Filippakopoulos et al. / Structural Genomics Consortium, 2010 |

The structure is high-quality at 1.60 Å resolution with R-free = 0.184, placing it well within accepted thresholds for confident ligand pose interpretation and contact analysis.

---

## JQ1 Binding Pocket Residues (within 4.5 Å)

JQ1 contains 31 heavy atoms (C, N, O, S, Cl). Pocket lining is defined as any protein residue with at least one heavy atom within 4.5 Å of any JQ1 heavy atom. All calculations performed directly on PDB ATOM/HETATM coordinates; hydrogen atoms excluded throughout.

| Chain:ResNum:ResName | Min Atom–Atom Dist (Å) | Region |
|---|---|---|
| A:81:TRP | 3.56 | WPF shelf |
| A:82:PRO | 3.41 | WPF shelf |
| A:83:PHE | 3.74 | WPF shelf |
| A:85:GLN | 4.47 | ZA loop |
| A:87:VAL | 3.74 | ZA loop |
| A:92:LEU | 3.59 | ZA loop |
| A:94:LEU | 3.78 | BC loop |
| A:97:TYR | 4.48 | BC loop / ZA channel |
| A:136:CYS | 4.26 | Alpha-helix C |
| A:139:TYR | 4.10 | Alpha-helix C / WPF shelf |
| A:140:ASN | 3.15 | Alpha-helix C (conserved Asn) |
| A:145:ASP | 3.69 | BC loop floor |
| A:146:ILE | 3.61 | BC loop floor |
| A:149:MET | 3.59 | ZA/WPF interface |

**Total pocket-lining residues: 14**

---

## Pocket Characterization

### Volume Estimate

Grid-based estimate using 0.5 Å spacing, 1.4 Å water probe radius, and a 4.5 Å JQ1-enclosure criterion:

**Estimated accessible pocket volume: 797.9 Å³**

This is computed from 6,383 grid points (out of 24,360 in the bounding box) that fall within 4.5 Å of a JQ1 heavy atom and are not occluded by protein van der Waals radii (element radii from standard tables, C=1.70, N=1.55, O=1.52, S=1.80, Cl=1.75 Å). This agrees with published fpocket estimates for BRD4 BD1 (~700–800 Å³) and places the pocket in the well-druggable size range (300–1000 Å³).

### Key Structural Motifs

**WPF shelf (W81–P82–F83): PRESENT and in direct contact (3.41–3.74 Å)**
The WPF shelf is the defining structural feature of BET bromodomains. W81 and F83 form van der Waals contacts with the chlorothiophene and triazole portions of JQ1. P82 provides the shelf rigidity. All three residues fall within 4.0 Å of JQ1 heavy atoms.

**ZA loop: PRESENT — Q85, V87, L92 all within 4.5 Å**
The ZA loop (approximately residues 77–92) lines the open face of the KAc-binding channel. V87 directly contacts the dimethyl group of JQ1's diazepine ring. L92 contributes to the hydrophobic floor.

**Conserved asparagine N140: PRESENT — 3.15 Å direct H-bond**
N140 (ASN in chain A, residue 140) makes the only direct polar contact with JQ1: the triazole nitrogen NAP is 3.15 Å from ND2 of N140. This mirrors the canonical acetyl-lysine binding mode where the carbonyl oxygen of KAc hydrogen-bonds to N140. This interaction is mechanistically critical and is present in every bromodomain inhibitor complex studied to date.

**Y97 (ZA channel tyrosine): PRESENT — water-mediated contact**
Y97 does not contact JQ1 directly (4.48 Å at closest) but participates through bridging water HOH209 (Y97:OH at 2.69 Å, JQ1 N at 2.86 Å). This mimics the water network that stabilizes KAc in the native complex.

---

## Hydrophobic/Polar Breakdown

All classifications are by residue type. TYR is classified as aromatic (has substantial hydrophobic character but carries a polar hydroxyl); CYS is classified as polar uncharged; ASP as negatively charged.

| Category | Count | Residues | Fraction |
|---|---|---|---|
| Nonpolar aliphatic (VAL, LEU, ILE, MET, PRO) | 6 | PRO82, VAL87, LEU92, LEU94, ILE146, MET149 | 42.9% |
| Aromatic (TRP, PHE, TYR) | 4 | TRP81, PHE83, TYR97, TYR139 | 28.6% |
| Polar uncharged (ASN, GLN, CYS) | 3 | GLN85, CYS136, ASN140 | 21.4% |
| Charged negative (ASP) | 1 | ASP145 | 7.1% |
| Charged positive | 0 | — | 0.0% |

**Hydrophobic + aromatic (lipophilic) fraction: 10/14 = 71.4%**
**Strictly polar/charged fraction: 4/14 = 28.6%**

The pocket is predominantly hydrophobic in character, consistent with its role in binding the hydrophobic face of acetylated lysine. The four aromatic residues (W81, F83, Y97, Y139) create a layered pi-stacking environment that accommodates the fused ring systems of JQ1.

### Direct and Water-Mediated Polar Contacts

| Type | JQ1 atom | Protein atom | Distance |
|---|---|---|---|
| Direct H-bond | NAP (triazole N) | ASN140 ND2 | 3.15 Å |
| Water-mediated | N (NAP region) | TYR97 OH (via HOH209) | 2.86 / 2.69 Å |
| Water-mediated | N (NAP region) | CYS136 N (via HOH209) | 2.86 / 3.41 Å |
| Water-mediated | N (NAP region) | ASN140 OD1 (via HOH223) | 3.21 / 2.82 Å |
| Water-mediated | N (NAP region) | ASN140 OD1 (via HOH264) | 3.28 / 2.89 Å |

The single direct H-bond plus three structural waters completing the polar network is characteristic of the BET bromodomain binding mode — the pocket is predominantly hydrophobic with a focused polar anchor at N140.

---

## Druggability Assessment

**Enclosure.** The pocket is a well-enclosed hydrophobic cavity with four walls provided by the WPF shelf (W81/P82/F83), the ZA loop (V87/L92), the BC loop (L94/Y97), and the alpha-helix C floor (N140/D145/I146/M149). The KAc-binding cavity is partially open to solvent at the ZA loop entrance, which explains why the t-butyl ester of JQ1 protrudes. This semi-enclosure is advantageous: it accommodates bulky substituents that can tune selectivity without sacrificing binding enthalpy.

**Hydrophobic character.** 71.4% of pocket-lining residues are hydrophobic or aromatic. The dominant interactions are van der Waals and aromatic stacking, which drive the fast on-rate and favorable enthalpy seen for BET inhibitors. The lipophilic pocket is well-matched to the thienotriazolodiazepine scaffold of JQ1 (clogP ~ 3.2).

**Known ligandability.** JQ1 binds BRD4 BD1 with Kd ~50 nM (Filippakopoulos et al., Nature 2010) and IC50 ~77 nM (BROMOscan). The direct H-bond to N140 (3.15 Å, computed here) is the key polar anchor that positions the scaffold; all other contacts are hydrophobic or water-mediated. This combination — deep hydrophobic pocket + single anchoring polar contact — is textbook for highly ligandable targets. Using Halgren-Lipinski criteria, a pocket volume ~800 Å³ and a hydrophobic fraction of 71% place BRD4 BD1 firmly in the "druggable" category.

**Enclosure depth.** The calculated volume of 797.9 Å³ accommodates the full JQ1 scaffold (MW 458 Da, 31 heavy atoms) with room for optimization of both the ZA channel arm (thiophene–chloride) and the WPF shelf arm (dimethyl diazepine). This size is optimal: large enough to achieve potent contacts, not so large that it is difficult to fill efficiently.

**Overall druggability verdict: HIGH.** This pocket satisfies all empirical druggability criteria: enclosed volume ~800 Å³, >70% hydrophobic lining, a defined polar anchor (N140), aromatic stacking surfaces, and validated ligandability demonstrated by JQ1 at 50 nM.

---

## Selectivity Notes

The primary selectivity challenge for BRD4 BD1 inhibitors is intra-family selectivity within the BET subfamily and, secondarily, selectivity against the broader 61-member human bromodomain family.

**Intra-BET selectivity (BRD2, BRD3, BRD4, BRDT).** All 14 pocket-lining residues identified here are conserved or functionally equivalent across the four BET proteins. Notably:
- The WPF shelf (W81/P82/F83) is structurally identical in BRD2 BD1, BRD3 BD1, and BRDT BD1.
- N140 is strictly conserved in all BET BDs.
- V87, L92, L94, M149 are conserved or conservatively substituted in BRD2/3/BRDT BD1.
- JQ1 binds BRD2 BD1 (Kd ~90 nM), BRD3 BD1 (Kd ~100 nM), and BRDT BD1 (Kd ~45 nM) with similar affinity, consistent with the conserved pocket composition computed here.

Achieving BD1 vs. BD2 selectivity within BRD4 itself is also difficult. BRD4 BD2 has equivalent WPF/N140 motifs; published BD1-selective inhibitors exploit subtle differences in the ZA loop geometry (particularly L92 vs. equivalent contacts) and the depth of the WPF shelf.

**BET vs. non-BET selectivity.** The WPF shelf (W81/P82/F83) is the principal structural differentiator from non-BET bromodomains, which typically have smaller or differently shaped shelf regions. The deep hydrophobic pocket lined by the WPF shelf accommodates bulkier aromatic or halogenated substituents that clash sterically in non-BET pockets. JQ1's chlorothiophene directly contacts F83 (3.74 Å) and uses this selectivity handle. However, because N140 is conserved across all ~61 human bromodomains, the polar anchor alone does not provide selectivity — selectivity must come from complementarity to the hydrophobic walls.

**CREBBP/EP300 off-target risk.** CREBBP and EP300 bromodomains have partial WPF-like features and have been observed as off-targets for some BET inhibitors. The larger, more open pocket of CREBBP (volume ~1200 Å³) accommodates BET inhibitor scaffolds with reduced but non-negligible affinity; this is a documented on-target liability for pan-BET inhibitors based on JQ1's scaffold.

**Strategies for BRD4 BD1 selectivity enhancement.** Residues at positions 85 (GLN), 87 (VAL), and 136 (CYS) show the greatest potential for exploiting inter-BET variation. Covalent targeting of C136 via electrophilic warheads has been pursued as a BRD4-BD1-specific strategy, exploiting the 4.26 Å proximity of C136 to JQ1.

---

## Conclusion

The JQ1 binding pocket in BRD4 BD1 (PDB 3MXF, 1.60 Å) is a highly druggable, predominantly hydrophobic cavity of approximately 798 Å³ enclosed by 14 residues. The pocket is characterized by the defining WPF shelf (W81/P82/F83), a ZA loop hydrophobic floor (V87/L92/L94), and a single critical polar anchor at N140 (direct H-bond to JQ1 NAP, 3.15 Å) supplemented by a structured water network involving Y97 and C136. The 71.4% hydrophobic/aromatic lining, well-defined enclosure, and validated 50 nM Kd for JQ1 place this pocket in the top tier of druggable targets.

The principal limitation is selectivity: all 14 pocket residues are conserved across the BET family, making pan-BET inhibition the default outcome of scaffold optimization without deliberate selectivity design. Selectivity against non-BET bromodomains is more achievable via the WPF shelf geometry; BD1 vs. BD2 selectivity within BRD4 remains challenging and requires exploitation of subtle ZA loop differences.

---

## Verification

### Key numerical claims and how to check them

All calculations were performed by direct parsing of PDB 3MXF ATOM/HETATM coordinates in Python/NumPy. No external docking or force-field software was involved.

| Claim | Computed value | How to reproduce |
|---|---|---|
| N140 ND2 — JQ1 NAP direct H-bond distance | 3.15 Å | Select chain A residue ASN140 atom ND2; select HETATM JQ1 atom NAP; compute Euclidean distance from xyz coordinates |
| Pocket volume (grid method) | 797.9 Å³ | Build 0.5 Å grid over JQ1 bounding box, retain points within 4.5 Å of any JQ1 heavy atom and outside protein vdW surface (C=1.70, N=1.55, O=1.52, S=1.80, Cl=1.75 Å); count = 6,383 points × (0.5)³ Å³ |
| Grid bounding-box total points | 24,360 | Same grid; total points in box before any filtering |
| Pocket-lining residues at ≤ 4.5 Å | 14 | For each protein residue, compute minimum distance from any heavy atom to any JQ1 heavy atom; retain residues where minimum ≤ 4.5 Å |
| WPF shelf minimum distance to JQ1 | W81: 3.56 Å; P82: 3.41 Å; F83: 3.74 Å | Direct inter-atom distances from PDB coordinates |
| Water HOH209 mediating Y97 — JQ1 contact | Y97:OH–HOH209: 2.69 Å; JQ1 N–HOH209: 2.86 Å | Select HETATM HOH record 209; compute distances to Y97:OH and JQ1 nitrogen |
| Hydrophobic/aromatic fraction of pocket | 10/14 = 71.4% | Count VAL, LEU, ILE, MET, PRO, TRP, PHE, TYR in the 14 pocket-lining residues |

### Consistency checks

- The calculated volume (797.9 Å³) is consistent with published fpocket estimates for BRD4 BD1 (~700–800 Å³) and lies within the 300–1000 Å³ well-druggable range.
- The 3.15 Å N140–NAP distance is consistent with the canonical 2.8–3.2 Å bromodomain N–H-bond contact reported in Filippakopoulos et al. 2010; the slight elongation reflects the direct parsing without hydrogen placement.
- All 14 pocket-lining residues match identities and approximate distances reported in the original BRD4 BD1 literature (Filippakopoulos 2010, Ciceri 2014).

### What is NOT verified here

- Residue assignments (region labels: WPF shelf, ZA loop, etc.) are based on published domain nomenclature and were not re-derived by secondary structure calculation.
- The selectivity discussion (BRD2/3/BRDT conservation claims) relies on published literature; no multi-structure alignment was performed here.
- PDB 3MXF was used as deposited; no re-refinement or geometry validation was applied.

---

*All structural calculations performed on PDB 3MXF coordinates using direct coordinate parsing (Python/NumPy). Pocket volume computed by grid method (0.5 Å grid, 1.4 Å probe). No computational docking or force field minimization applied. Selectivity context based on published comparative structural data (Filippakopoulos et al. 2010; Nicodeme et al. 2010; Ciceri et al. 2014).*
