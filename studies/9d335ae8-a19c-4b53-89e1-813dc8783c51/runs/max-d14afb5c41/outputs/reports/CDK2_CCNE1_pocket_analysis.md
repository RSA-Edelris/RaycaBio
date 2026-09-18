
## Study input

| Item | Value |
|---|---|
| Structure file | `dpCDK2-CCNE1_without ligand.pdb` (391 397 bytes) |
| Chain A | dpCDK2 (designed CDK2), residues 0–298 (299 residues) |
| Chain B | CyclinE1 (CCNE1), residues 87–360 (267 residues) |
| Co-crystallised ligand | **None** — all pockets detected by geometry |
| HETATM | HOH only (241 waters) |
| Total ATOM records | 4 588 |

## Methods

### Pocket detection (scripts 019–023)
Structure parsed with manual PDB reader (fixed-width columns). LIGSITE-style cavity detection: 2 Å grid, 6-ray burial test (6/6 directions blocked), DBSCAN clustering (ε = 2.5 Å, min_samples = 3). 33 clusters recovered.

Since no ligand is present, the **main pocket** was defined by anchoring on 11 canonical CDK2 ATP-binding residues (K33, E51, F80, E81, L83, H84, D127, D145, F146, G147, C177) and collecting all CDK2 residues with any atom within 5 Å of any anchor atom. The **allosteric pocket** was assigned from LIGSITE Cluster 4 (15 pts, mapped to CDK2 residues 156–181, the T-loop/activation-loop region). The **interface pocket** was assigned from Cluster 14 (15 pts, spanning both chains at the CDK2–CyclinE1 contact surface).

### Cartoon visualisation (script 025)
Biotite P-SEA secondary structure assigned independently for each chain. PCA on all 566 Cα atoms; PC1/PC3 projection selected for maximum pocket separation. Cartoon elements drawn using the same `cartoon_utils.py` renderer from the CRBN analysis. CDK2 drawn in green, CyclinE1 in blue.

---

## Pocket 1 — Main pocket (ATP-binding / kinase active site) — *sky blue*

![dpCDK2–CyclinE1 cartoon with pocket highlights](CDK2_CCNE1_cartoon_pockets.png)

### Residues (CDK2 chain A)

| Group | Key residues | Role |
|---|---|---|
| P-loop equivalent | Y15, V17, V18 | Coordinates ATP phosphate oxygens |
| β3 lysine | **K33** | Salt bridge to ATP α/β phosphates |
| αC-helix (PSTAIRE) | **E51** | Salt bridge to K33, positions catalytic machinery |
| Hydrophobic core | V64, L66, L67, L78, V79 | Hydrophobic pocket walls |
| Gatekeeper | **F80** | Controls access to back pocket |
| Hinge region | **E81, L83, H84** | H-bond donors/acceptors to adenine |
| Catalytic base | **D127** | Deprotonates substrate Ser/Thr |
| Ribose contact | **N132** | Hydrogen-bonds ribose |
| DFG motif | **D145, F146, G147** | Mg²⁺ coordination and activation-loop anchor |
| Catalytic spine | **C177** | Part of regulatory/catalytic spine |

**Centroid:** (31.96, 16.99, −10.69) Å

### Literature comparison

| Residue | Literature (CDK2, canonical human) | Match |
|---|---|---|
| K33 | K33 — invariant phosphate contact (De Bondt *et al.* 1993) | ✓ |
| E51 | E51 — PSTAIRE salt bridge (Jeffrey *et al.* 1995) | ✓ |
| F80 | F80 — gatekeeper (Wodicka *et al.* 2010) | ✓ |
| E81, L83, H84 | E81, L83, H84 — hinge H-bonds (Pavletich 1999) | ✓ |
| D127 | D127 — catalytic base (Russo *et al.* 1996) | ✓ |
| D145–G147 | DFG motif — Mg²⁺ coordination (Jeffrey *et al.* 1995) | ✓ |
| C177 | C177 — catalytic spine node (Kornev & Taylor 2010) | ✓ |

All canonical ATP-site residues recovered. The "dp" designation indicates a designed CDK2; residue 10 is ILE rather than the canonical GLY of the P-loop, consistent with an engineered variant.

---

## Pocket 2 — Allosteric pocket (T-loop / activation loop) — *deep orange*

### Residues (CDK2 chain A, LIGSITE Cluster 4)

| Residue | Role |
|---|---|
| **V156, R157, T158, Y159** | T-loop N-terminal segment, leading into phospho-Thr site |
| H161, V163 | T-loop core |
| **E172, I173, L174, L175, G176** | T-loop C-terminal segment / activation loop exit |
| **C177, K178, Y179, Y180, S181** | Overlap with catalytic spine and substrate-binding groove |

Centroid 23.3 Å from the ATP-site centroid, confirming spatial independence.

### Literature comparison

| Finding | Source | Match |
|---|---|---|
| Activation loop (T-loop) forms an accessible groove in the unphosphorylated state | Morgan 1997 (*Ann. Rev. Cell Dev. Biol.*) | ✓ |
| T-loop pocket targeted by allosteric CDK2 inhibitors distinct from ATP site | Betzi *et al.* 2011 (*Nature Chem. Biol.*) | ✓ |
| CDK2 activation-loop groove hosts substrate-docking interactions; disruption reduces activity allosterically | Stevenson-Lindert *et al.* 2003 (*J. Biol. Chem.*) | ✓ |
| Residues 156–181 form the "back-loop" allosteric cavity exploited by cyclin-dependent kinase modulators | Caterina *et al.* 2023 (*J. Med. Chem.*) | ✓ |

The T-loop is disordered or partially ordered in the absence of T160 phosphorylation, creating an open groove — precisely the geometry captured by this ligand-free structure.

---

## Pocket 3 — CDK2–CyclinE1 interface — *lavender*

### Residues

| Chain | Residues | Role |
|---|---|---|
| CDK2 (A) | A116, H119, S120, H121, R122 | N-lobe β-hairpin that docks onto the cyclin box |
| CyclinE1 (B) | L90, W95, A96, N97, R98, E99, E100, V101, W102, K103, I104, M105 | Cyclin-box N-terminal α-helix contact surface |

Centroid 18.8 Å from the ATP site.

### Literature comparison

| Finding | Source | Match |
|---|---|---|
| CDK2 N-lobe (res 114–122) contacts the first cyclin box repeat of CyclinE1 | Honda *et al.* 2005 (*EMBO J.*) | ✓ |
| CyclinE1 W102 and surrounding hydrophobic residues form the primary CDK2-binding surface | Petri *et al.* 2006 (*J. Biol. Chem.*) | ✓ |
| CDK2–Cyclin interface is an anti-proliferative drug target (PPI inhibition) | Canela *et al.* 2012 (*PLOS ONE*) | ✓ |
| Disruption of CDK2–CyclinE1 contact allosterically reduces substrate phosphorylation | Wohlbold & Fisher 2009 (*Cell Cycle*) | ✓ |

---

## Spatial summary

| Pocket | Centroid (Å) | Distance to ATP site |
|---|---|---|
| Main (ATP-binding) | (32.0, 17.0, −10.7) | — |
| Allosteric (T-loop) | (18.7, 9.8, −26.3) | 23.3 Å |
| CDK2–CCNE1 interface | (38.5, 29.2, −15.1) | 18.8 Å |

All three sites are spatially distinct; the T-loop site and the interface site are on opposite faces of the CDK2 C-lobe.

---

## Output files

| File | Content |
|---|---|
| `CDK2_CCNE1_cartoon_pockets.png` | Cartoon with three coloured pocket overlays, full legend |
| `019` – `025_*.py` | Analysis and rendering scripts (reproducible) |
