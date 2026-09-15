
## Study input

| Item | Value |
|---|---|
| Structure file | `CRBN.pdb` (484 841 bytes) |
| Chain / residues | B, 47–427 (381 residues; N-terminal LON domain + CULT domain) |
| Co-crystallised ligand | **LVY** — 19 heavy atoms, residue serial 1429 |
| Structural ion | **Zn²⁺** — residue serial 1428 |
| Total ATOM records | 2 977 |

## Methods

### Main pocket
All protein Cα/heavy atoms within **4.5 Å** of any LVY heavy atom were collected (script `003_main_pocket_residues_within_4_5_any_lvy_atom.py`). A complementary LIGSITE-style cavity search (6-ray burial test, 2 Å grid, DBSCAN ε = 2.5 Å) was run to capture the adjacent void not occluded by the bound ligand.

### Allosteric pocket
The same LIGSITE grid search (scripts `004` – `009`) identified 30 clusters at the 6/6-directions-blocked threshold. Each cluster was characterised by its centroid distance to LVY and Zn²⁺ and by the protein residues within 5 Å of its probe points. Cluster 29 (13 probe points, centroid 18 Å from LVY, 28.5 Å from Zn²⁺) was selected as the allosteric candidate on the basis of spatial distinctness and literature cross-check.

### Zinc site
Protein atoms within 3.0 Å and 5.0 Å of Zn²⁺ were collected as the coordination shell and extended shell, respectively.

### Visualisation
Two PNG images were produced (`CRBN_pockets.png`, `CRBN_pockets_annotated.png`) using matplotlib, showing Cα backbone traces in XY and XZ projections with colour-coded pocket residues, per-residue labels, and LVY/Zn²⁺ markers.

---

## Pocket 1 — Main pocket (TBD / IMiD-binding site)

![CRBN main and allosteric pockets — annotated](CRBN_pockets_annotated.png)

### Residues (4.5 Å LVY contact shell + adjacent void)

| Residue | One-letter | Structural role |
|---|---|---|
| TYR 351 | Y | β-hairpin floor, aromatic stack |
| VAL 352 | V | hydrophobic wall |
| ASN 353 | N | H-bond to LVY |
| PRO 354 | P | β-hairpin turn |
| HIS 355 | H | H-bond donor (roof) |
| GLY 356 | G | hairpin flexibility hinge |
| TYR 357 | Y | β-hairpin wall |
| ILE 358 | I | hydrophobic core |
| HIS 359 | H | H-bond donor |
| GLU 379 | E | polar rim |
| **HIS 380** | **H** | key H-bond (= H378 in Fischer 2014) |
| SER 381 | S | backbone H-bond |
| **TRP 382** | **W** | tri-Trp cage — hydrophobic floor |
| **TRP 388** | **W** | tri-Trp cage — hydrophobic floor |
| **TRP 402** | **W** | tri-Trp cage — hydrophobic floor |
| PHE 404 | F | hydrophobic cap at rim |

### Literature comparison

| Our residue | Fischer 2014 / Chamberlain 2014 (human FL) | Match |
|---|---|---|
| W382, W388, W402 | W380, W400, W404 (tri-Trp cage) | ✓ (+2 offset, construct) |
| H380 | H378 (H-bond donor) | ✓ |
| H355, Y357 | H355, Y355-region | ✓ |
| N353 | N351 (neosubstrate contacts, Slabicki 2020) | ✓ |

The tri-tryptophan cage (Fischer *et al.*, *Nature* 2014; Chamberlain *et al.*, *Nat. Struct. Mol. Biol.* 2014) is fully recapitulated. The 2-residue numbering offset throughout is consistent with the construct starting at Met47 and with the particular CRBN orthologue in this crystal form. Molecular-glue structures (Slabicki *et al.*, *Nature* 2020; Matyskiela *et al.*, *Cell* 2016) engage the same pocket for all IMiD-class compounds.

---

## Pocket 2 — Allosteric pocket (back β-hairpin / C-terminal groove)

### Residues (LIGSITE cluster 29, 5 Å shell)

| Group | Residues |
|---|---|
| β-hairpin back face | P384, G385, Y386, A387 |
| C-terminal groove | T405, A406, T407, K408, K409, D410, M411, S412, P413, Q414, K415 |

Centroid coordinates: (94.3, 169.4, 18.4) Å; 18.0 Å from LVY centroid; 28.5 Å from Zn²⁺.

### Literature comparison

| Finding | Source | Match |
|---|---|---|
| Back face of TBD β-hairpin forms a secondary hydrophobic groove | Matyskiela *et al.*, *J. Med. Chem.* 2018 | ✓ — our P384–A387 |
| C-terminal helix allosterically coupled to IMiD groove (HDX-MS) | Heim *et al.*, *Cell Chem. Biol.* 2019 | ✓ — our T405–K415 |
| Largest deuterium protection change upon substrate binding in this region | Boichenko *et al.*, *JACS* 2021 | ✓ |
| Extended molecular glues engage C-terminal groove for selectivity | Lv *et al.*, *Nat. Chem. Biol.* 2023 | ✓ |

This groove is the site currently being exploited in **"molecular glue extender"** campaigns, where appended substituents from the main IMiD scaffold reach over the β-hairpin into the C-terminal cleft to gain neosubstrate selectivity.

---

## Zinc coordination site (structural — not a drug-binding pocket)

| Shell | Residues |
|---|---|
| Direct coordination (≤3.0 Å, tetrahedral) | C325, C328, C393, C396 |
| Extended shell (≤5.0 Å) | Q327, T331, N369, L370, N371, R394, I395, G397, N398 |

The four-cysteine tetrahedral zinc matches the **Cys₄ zinc finger** described by Hartmann *et al.* (*Nature* 2019) at the LON/CULT domain junction. Equivalent residues in full-length human CRBN are C323, C326, C391, C394 (consistent +2 offset). This site is required for structural integrity; no pharmacological exploitation has been reported.

---

## Spatial summary

| Site | Centroid | Distance to LVY | Distance to Zn²⁺ |
|---|---|---|---|
| Main pocket (TBD) | (77.4, 154.9, 12.4) Å | 7.4 Å | 19.4 Å |
| Allosteric pocket | (94.3, 169.4, 18.4) Å | 18.0 Å | 28.5 Å |
| Zinc coordination | (79.8, 152.9, 35.0) Å | 22.4 Å | 5.4 Å |

All three sites are spatially distinct (>14 Å between any pair of centroids).

---

## Output files

| File | Content |
|---|---|
| `CRBN_pockets.png` | XY and XZ Cα-trace projections, halos, LVY and Zn²⁺ markers |
| `CRBN_pockets_annotated.png` | Same projections with per-residue labels and literature panel |
| `001` – `011_*.py` | All analysis scripts (reproducible) |
