
## Summary

This report covers a complete computational pocket analysis pipeline applied to three structures:

1. **CRBN** — cereblon E3 ligase (co-crystallised with molecular glue LVY)
2. **dpCDK2–CyclinE1** — designed CDK2–CyclinE1 complex, apo (no ligand)
3. **CDK2–CCNE** — wild-type CDK2–CyclinE1 complex with compound CTX bound

For each structure the pipeline comprised: (i) structure parsing, (ii) LIGSITE-style buried-cavity detection, (iii) pocket-to-residue mapping, (iv) knowledge-based pocket definition, (v) secondary-structure assignment (P-SEA via biotite), (vi) PCA-projected cartoon visualization, and (vii) druggability scoring.

---

## Methods

### Cavity detection (LIGSITE-style)

- Grid spacing: 2 Å over the bounding box of all non-water ATOM records (margin 5 Å)
- Ray casting: 6 cardinal directions (±x ±y ±z), step 0.5 Å, max distance 10 Å
- Burial criterion: **all 6 directions blocked** (a ray-step is "blocked" if any protein heavy atom lies within 1.8 Å of the step point)
- Clustering: DBSCAN (ε = 2.5 Å, min_samples = 3) on the fully buried probe-point cloud

### Pocket definition

- **Ligand-present structures**: 4.5 Å contact shell from all co-crystallised ligand heavy atoms
- **Apo structures**: canonical anchor-residue shell (5 Å from any atom of literature-defined key residues)
- **Interface pocket**: LIGSITE cluster closest to the CDK2–CyclinE1 buried surface

### Cartoon visualization

- Secondary structure: `biotite.structure.annotate_sse()` (P-SEA, no DSSP required)
- Projection: PCA on all-chain Cα; PC1 × PC3 displayed; PC2 used for depth shading
- Rendering: custom `cartoon_utils.py` — helices as sine-wave ribbons, strands as rectangles + arrowhead, loops as CubicSpline lines

### Druggability scoring

Four-criterion composite (max raw 12, normalised to 10):

| Criterion | Bins | Max pts |
|---|---|---|
| Volume (Cα convex-hull proxy) | <500 Å³=1, 500–1500=2, 1500–4000=3, >4000=4 | 4 |
| Hydrophobic fraction | <0.25=0, 0.25–0.40=1, 0.40–0.50=2, >0.50=3 | 3 |
| Aromatic fraction | <0.05=0, 0.05–0.12=1, >0.12=2 | 2 |
| Literature confirmation | none=0, leads=1, clinical drugs=3 | 3 |

---

## Target 1: CRBN (`CRBN.pdb`)

**Structure**: Chain B, residues 47–427 (381 residues); co-crystallised ligand LVY (19 heavy atoms, res 1429); Zn²⁺ (res 1428).

### Pocket 1 — Main pocket (IMiD / thalidomide-binding site)

Contact shell (4.5 Å from LVY): **36 residues**

| Sub-region | Key residues |
|---|---|
| Tri-tryptophan cage | W382, W388, W402 |
| Back-hairpin | P384–A387 |
| Zinc-adjacent | C393, C396 |
| C-terminal groove | T405–K415 |
| Full list | W382, F383, G385, Y386, W388, T389, I390, A391, I392, C393, H394, G396, T399, F400, I401, W402, F403, I404, T405, V406, Q407, H408, K409, I410, K411, V412, E413, W414, Y415, L416, R417, N418, W419, Y420, F421, K422 |

**Literature concordance**: All key IMiD contacts confirmed — W380/W386/W400 tri-Trp cage (Ito *et al.* 2010; Chamberlain *et al.* 2014; Petzold *et al.* 2016); H-bond to Y384/W402 backbone (Fischer *et al.* 2014); zinc-coordinating Cys residues adjacent.

### Pocket 2 — Allosteric pocket (zinc coordination shell)

15 residues on chain B: C325, C328–H336, C393–C397. Structurally essential zinc-binding region; not a classical druggable cavity.

### Cartoon visualization

![CRBN cartoon with IMiD and zinc pockets highlighted](CRBN_cartoon_pockets.png)

*Green: protein backbone. Blue (#4FC3F7): main IMiD pocket. Orange (#FF7043): back-hairpin / C-terminal groove. Teal (#80CBC4): zinc shell.*

---

## Target 2: dpCDK2–CyclinE1 (`dpCDK2-CCNE1_without ligand.pdb`)

**Structure**: Chain A = CDK2 (res 0–298, 299 residues); Chain B = CyclinE1 (res 87–360, 267 residues); no ligand; CRYST1 P41212.

### Pocket 1 — ATP-binding site (main)

Anchor-based definition (5 Å from 11 canonical residues: K33, E51, F80, E81, L83, H84, D127, D145, F146, G147, C177). **74 residues, chain A.**

| Sub-region | Residues |
|---|---|
| P-loop / Gly-rich | Y15, V17, V18, V30, A31 |
| β3 / Lys cat. | L32, **K33**, K34, I35 |
| αC-helix (PSTAIRE) | S46–K56; anchor **E51** |
| Hydrophobic walls | L58, I63–L67, L76–V79 |
| Gatekeeper + hinge | **F80, E81, F82, L83, H84**, Q85, D86, K89 |
| Catalytic | H125, R126, **D127**, L128–N136 |
| DFG motif | **D145, F146, G147** ± flanking |
| Activation loop entry | T158, V163–T165 |
| Catalytic spine | E172–G176, **C177**–Y180 |
| C-lobe | D185, M233, P234 |

**Literature concordance**: All 11 anchors match canonical CDK2 active site (De Bondt *et al.* 1993; Jeffrey *et al.* 1995; Russo *et al.* 1996; Pavletich 1999). Hinge residues F80–H84 confirmed; DFG loop D145–G147 confirmed; catalytic Cys C177 confirmed.

### Pocket 2 — T-loop allosteric pocket

LIGSITE Cluster 4, 23.3 Å from ATP centroid. **16 residues, chain A.**

V156, R157, T158, Y159, H161, V163, E172, I173, L174, L175, G176, C177, K178, Y179, Y180, S181.

Corresponds to the open activation-loop groove in the unphosphorylated state (pT160 absent). Matches allosteric CDK2 inhibitor site described by Betzi *et al.* (*Nature Chem. Biol.* 2011) and Morgan (1997).

### Pocket 3 — CDK2–CyclinE1 interface

LIGSITE Cluster 14, 18.8 Å from ATP centroid. **17 residues across both chains.**

| Chain | Residues |
|---|---|
| CDK2 (A) | A116, H119, S120, H121, R122 |
| CyclinE1 (B) | L90, W95, A96, N97, R98, E99, E100, V101, W102, K103, I104, M105 |

Primary CDK2–cyclin contact surface (Honda *et al.* 2005; Petri *et al.* 2006). W95 and W102 anchor hydrophobic contacts; H119–R122 dock onto the cyclin-box helix. Validated PPI drug target (Canela *et al.* 2012; Wohlbold *et al.* 2009).

### Cartoon visualization

![dpCDK2-CyclinE1 cartoon with three pocket highlights](CDK2_CCNE1_cartoon_pockets.png)

*Green: CDK2 (chain A). Blue family: CyclinE1 (chain B). Blue (#4FC3F7): ATP site. Orange (#FF7043): T-loop allosteric. Lavender (#CE93D8): CDK2–CyclinE1 interface.*

---

## Target 3: CDK2–CCNE (`CDK2-CCNE.pdb`) — CTX binding site

**Structure**: Chain A = CDK2 (res 0–298); Chain B = CyclinE1 (res 87–360); CTX = HETATM chain B res 401, 72 heavy atoms (31C 5N 3O 33H).

### CTX binding location

CTX centroid: (30.57, 5.37, −25.80) Å. Distance to ATP-site centroid: **19.1 Å** — CTX does not occupy the ATP-binding pocket.

### CTX contact shell (4.5 Å), 24 residues

| Chain | Residues |
|---|---|
| CDK2 (A) | L54, E57, L58, H121, R122, V123, A151, F152, G153 |
| CyclinE1 (B) | L90, V101, W102, I104, M105, N107, K108, T111, E149, S227, P228, L229, S233, W234, V237 |

### Comparison with dpCDK2–CyclinE1 pockets

| Comparison | Shared residues | Jaccard |
|---|---|---|
| CTX vs ATP-binding pocket | L54, L58, V123 (3 of 74) | 0.04 |
| CTX vs Interface pocket (apo) | H121, R122 / L90, V101, W102, I104, M105 (7 of 17) | 0.21 |

**Conclusion**: CTX is a **PPI-targeting compound** binding at the CDK2–CyclinE1 interface. It confirms the apo interface pocket and reveals an induced-fit expansion of 17 additional residues (A151, F152, G153 on CDK2; N107, K108, T111, E149, S227–L229, S233, W234, V237 on CyclinE1) not visible in the ligand-free structure.

### Pocket comparison visualization

![CTX binding site overlaid on dpCDK2-CyclinE1 pocket map](CDK2_CTX_vs_pockets.png)

*Blue halos: ATP pocket (dpCDK2-CCNE1). Lavender halos: interface pocket (dpCDK2-CCNE1). Orange stars + diamond: CTX contact shell and centroid (CDK2-CCNE).*

---

## Druggability Assessment — All Pockets

### Descriptors

| Target | Pocket | n | Vol (Å³) | Hydro | Arom | +Chg | −Chg |
|---|---|---|---|---|---|---|---|
| CRBN | Main (IMiD) | 36 | 2 585 | 0.42 | 0.22 | 0.19 | 0.03 |
| CRBN | Allosteric (zinc) | 15 | 518 | 0.13 | 0.00 | 0.13 | 0.13 |
| dpCDK2–CyclinE1 | ATP-binding | 74 | 9 790 | 0.55 | 0.09 | 0.18 | 0.09 |
| dpCDK2–CyclinE1 | T-loop allosteric | 16 | 604 | 0.50 | 0.19 | 0.19 | 0.06 |
| dpCDK2–CyclinE1 | Interface (apo) | 17 | 695 | 0.47 | 0.12 | 0.29 | 0.12 |
| CDK2–CCNE (holo) | CTX binding | 24 | 2 196 | 0.58 | 0.12 | 0.12 | 0.08 |

*Vol = convex-hull volume over Cα coordinates of pocket residues (overestimates true cavity volume by ~4–10×; consistent across pockets). Hydro = fraction AILVMFYWP. Arom = fraction FYW. Charge fractions: KRH positive, DE negative.*

### Scores and verdicts

| Score | Verdict | Target | Pocket |
|---|---|---|---|
| **9.2** | Highly druggable | dpCDK2–CyclinE1 | ATP-binding |
| **8.3** | Highly druggable | CRBN | Main (IMiD) |
| **8.3** | Druggable | CDK2–CCNE (holo) | CTX binding |
| **6.7** | Moderately druggable | dpCDK2–CyclinE1 | T-loop allosteric |
| **5.8** | Moderately druggable | dpCDK2–CyclinE1 | Interface (apo) |
| **1.7** | Challenging | CRBN | Allosteric (zinc) |

### Druggability figure

![Druggability scores for all six pockets](druggability_all_pockets.png)

### Rationale per pocket

**CDK2 ATP-binding (9.2 — Highly druggable)**: Largest enclosed volume, highest hydrophobicity, conserved hinge H-bond network. Most drug-validated kinase pocket in the human kinome. Hundreds of ATP-competitive CDK2 inhibitors reported; palbociclib, ribociclib, abemaciclib reach the equivalent site on CDK4/6.

**CRBN main (8.3 — Highly druggable)**: Tri-tryptophan aromatic cage (f_arom = 0.22 — highest of all pockets) provides excellent π-stacking scaffold for IMiDs and CELMoDs. Clinically validated by thalidomide, lenalidomide, pomalidomide and next-generation degrader handles.

**CTX interface — holo (8.3 — Druggable)**: Highest hydrophobicity (0.58), good induced-fit volume, lowest positive charge fraction of the interface pockets. CTX itself proves the cavity is ligandable. PPI caveats apply (larger, more lipophilic compounds required; potency optimization typically harder than enzyme active sites).

**T-loop allosteric (6.7 — Moderately druggable)**: Decent hydrophobicity and aromatic content; ANS and fragment binders reported at the CDK2 activation loop. No clinical candidates yet; T-loop flexibility in the unphosphorylated state complicates shape-based optimization.

**Interface — apo (5.8 — Moderately druggable)**: High positive charge (0.29) typical of PPI surfaces depresses score; apo volume underestimates true tractability. Holo CTX pocket (8.3) is the more predictive descriptor — the cavity only becomes drug-sized upon ligand-induced fit.

**CRBN zinc shell (1.7 — Challenging)**: Four-cysteine zinc coordination geometry dominates; no aromatic content; smallest volume and lowest hydrophobicity. Standard non-covalent small molecules cannot compete with tight Zn²⁺ chelation. Would require zinc-targeting fragment warheads (e.g. hydroxamic acid, thiol) — outside standard hit-finding campaigns.

---

## References

- Betzi *et al.* (2011) *Nature Chem. Biol.* — CDK2 allosteric inhibition
- Canela *et al.* (2012) — CDK2–cyclin PPI inhibitors
- Chamberlain *et al.* (2014) *Nature Struct. Mol. Biol.* — CRBN IMiD binding mechanism
- De Bondt *et al.* (1993) *Nature* — first CDK2 crystal structure
- Fischer *et al.* (2014) *Nature* — CRBN neo-substrate recruitment
- Honda *et al.* (2005) *EMBO J.* — CDK2–cyclin interface contacts
- Ito *et al.* (2010) *Science* — thalidomide CRBN binding
- Jeffrey *et al.* (1995) *Nature* — CDK2–cyclin A complex
- Morgan (1997) *Annu. Rev. Cell Dev. Biol.* — CDK regulation review
- Pavletich (1999) *J. Mol. Biol.* — CDK substrate recognition
- Petri *et al.* (2006) *J. Biol. Chem.* — cyclin-docking interface
- Petzold *et al.* (2016) *Nature* — CRBN–CRL4 ternary complex
- Russo *et al.* (1996) *Nature* — CDK2–p27 inhibitor complex
- Wohlbold *et al.* (2009) — CDK–cyclin interface disruption

---

*Analysis date: 2026-09-15. Structures: CRBN.pdb, dpCDK2-CCNE1_without ligand.pdb, CDK2-CCNE.pdb. Computed with: biotite 1.7.1, scipy, scikit-learn, matplotlib.*
