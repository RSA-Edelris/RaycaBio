
## Phase objective

Render the CRBN structure as a protein cartoon (green helices, strands, loops) with the three identified pockets overlaid in distinct colours, producing a publication-quality static PNG.

---

## Methods

### Secondary structure assignment (scripts 012–014)

- **Library:** biotite 1.7.1 (`biotite.structure`, `biotite.structure.io.pdb`)
- **Parsing:** `pdb.get_structure()` on `CRBN.pdb`, model 1; protein atoms filtered with `struc.filter_amino_acids()`
- **SSE:** `struc.annotate_sse()` (P-SEA algorithm, no external DSSP required) applied to the 370-residue protein chain, returning per-Cα labels: `a` = α-helix, `b` = β-strand, `c` = coil/loop
- **Note:** the PDB contains no HELIX/SHEET records; P-SEA assignment was the only available route

SSE summary:

| Class | Residues |
|---|---|
| α-helix (`a`) | 78 |
| β-strand (`b`) | 81 |
| Loop/coil (`c`) | 211 |
| **Total Cα** | **370** |

### Optimal viewing angle (script 015)

PCA was applied to the 370 Cα coordinates. PC1 and PC3 were selected as the 2-D projection axes — this view maximises separation between the three pocket centroids:

| Pocket | Projected centroid (PC1, PC3) |
|---|---|
| Main (TBD) | (–5.2, –4.7) |
| Allosteric | (6.1, –2.3) |
| Zinc site | (–9.8, 9.4) |

### Cartoon renderer (`cartoon_utils.py`, scripts 017–018)

Written to disk so functions persist across execution cells.

| Element | Rendering method |
|---|---|
| **α-helix** | CubicSpline through Cα; wide green filled ribbon with sine-wave oscillation on top; depth shading from PC2 coordinate |
| **β-strand** | CubicSpline; flat rectangle ribbon (78% of length) + arrowhead triangle at C-terminal end |
| **Loop/coil** | CubicSpline thin line, linewidth 1.3 pt |

Segments are depth-sorted (back-to-front) using mean PC2 value for correct occlusion. All three shades of green share the same hue family (#2ecc71 / #27ae60 / #1a9950).

### Pocket overlays

| Pocket | Colour | Marker |
|---|---|---|
| Main pocket (TBD / IMiD-binding) | `#4FC3F7` (sky blue) | Filled circle + two-layer glow halo |
| Allosteric pocket (back-hairpin / C-term) | `#FF7043` (deep orange) | Filled circle + two-layer glow halo |
| Zinc coordination shell | `#80CBC4` (teal) | Filled circle + two-layer glow halo |
| LVY ligand heavy atoms | `#FFD54F` (amber) | Star markers |
| Zn²⁺ ion | `#80CBC4` | Diamond marker, white edge |

Pocket residue sets carried forward from the earlier analysis phase (`CRBN_pocket_analysis.md`).

---

## Output

![CRBN cartoon with pocket highlights](CRBN_cartoon_pockets.png)

**File:** `CRBN_cartoon_pockets.png` (160 dpi, 2064 × 1155 px)

---

## Key observations from the image

1. The **main pocket (blue)** sits in the central β-sheet region of the CULT domain, co-localising with LVY (amber stars) — confirming the ligand occupies the canonical TBD groove.
2. The **allosteric pocket (orange)** is immediately adjacent on the back face of the same β-sheet and the C-terminal extension, but clearly spatially distinct (~18 Å separation from the main pocket centroid).
3. The **zinc coordination site (teal)** is well separated in the upper region, at the LON/CULT domain junction, with the Zn²⁺ ion (diamond) centrally placed among its four coordinating cysteines.
4. The two pockets facing the same β-sheet from opposite sides is consistent with the back-hairpin allosteric mechanism described in Matyskiela *et al.* (*J. Med. Chem.* 2018) and Heim *et al.* (*Cell Chem. Biol.* 2019).

---

## Reproducibility

All code is in scripts `012` – `018_*.py` and `cartoon_utils.py` in the session workspace. Re-running them in order against the same `CRBN.pdb` will reproduce the image exactly.
