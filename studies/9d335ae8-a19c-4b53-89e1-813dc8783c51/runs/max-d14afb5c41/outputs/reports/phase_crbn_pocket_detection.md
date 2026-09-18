
## Phase objective

Parse `CRBN.pdb`, characterise the co-crystallised ligand and ion, identify the main (IMiD-binding) pocket residues from direct ligand contacts, and lay the grid for cavity-based allosteric pocket detection.

---

## Script 001 — Ligand and ion identification (`001_check_what_lvy_print_all_hetatm_lvy.py`)

**What was done.** All HETATM records were printed to identify the non-protein content of the structure.

**Key findings.**

| Item | Serial | Atoms | Notes |
|---|---|---|---|
| LVY ligand | 1429 | 19 heavy atoms (C, N, O) | Co-crystallised CRBN modulator in TBD pocket |
| Zn²⁺ ion | 1428 | 1 | Structural zinc at LON/CULT domain junction |
| HOH | 2001+ | solvent | Not further analysed |

LVY centroid: (84.80, 154.94, 13.24) Å. Zn²⁺ position: (75.76, 152.11, 31.43) Å.

---

## Script 002 — PDB parsing (`002_parse_pdb_manually_extract_all_atom_hetatm_records.py`)

**What was done.** All ATOM and HETATM records were parsed into dictionaries containing record type, atom name, residue name, chain, residue number, and XYZ coordinates.

**Key findings.**

| Record class | Count |
|---|---|
| ATOM (protein) | 2 977 |
| HETATM LVY | 19 |
| HETATM ZN | 1 |
| HETATM HOH | ~20 |
| Chain | B only |
| Residue range | 47–427 |

A `scipy.spatial.cKDTree` was built over all protein heavy atoms for fast neighbour queries in subsequent steps.

---

## Script 003 — Main pocket residues (`003_main_pocket_residues_within_4_5_any_lvy_atom.py`)

**What was done.** For each protein heavy atom, its distance to every LVY atom was computed. Any protein residue with at least one atom within 4.5 Å of any LVY atom was retained as a main-pocket residue. The ZN coordination shell was collected separately at 3.0 Å and 5.0 Å cutoffs.

**Main pocket residues (≤4.5 Å from LVY):**

| Residue | Atoms within cutoff | Role |
|---|---|---|
| VAL 352 | 1 | hydrophobic wall |
| ASN 353 | 5 | H-bond to LVY |
| PRO 354 | 2 | β-hairpin turn |
| HIS 355 | 2 | H-bond donor (roof) |
| HIS 359 | 2 | H-bond donor |
| GLU 379 | 1 | polar rim |
| HIS 380 | 6 | key H-bond donor (= H378, Fischer 2014) |
| SER 381 | 5 | backbone H-bond |
| **TRP 382** | 12 | tri-Trp cage floor |
| **TRP 388** | 10 | tri-Trp cage floor |
| **TRP 402** | 8 | tri-Trp cage floor |
| PHE 404 | 2 | hydrophobic cap |

**Zn²⁺ direct coordination (≤3.0 Å):** CYS 325, CYS 328, CYS 393, CYS 396 — tetrahedral Cys₄ motif.

**Zn²⁺ extended shell (≤5.0 Å):** CYS 325, GLN 327, CYS 328, THR 331, CYS 393, ILE 395, CYS 396, GLY 397, ASN 398.

---

## Script 004 — Grid setup for LIGSITE cavity search (`004_grid_based_cavity_detection_fpocket_lite_approach.py`)

**What was done.** A 1.5 Å spacing 3-D grid covering the protein bounding box + 5 Å padding was constructed. Each grid point was filtered by:
- nearest protein atom distance > 1.4 Å (not inside protein)
- ≥ 8 protein atoms within 5.5 Å (enclosed / buried)

This produced 16 455 candidate probe points, which were then passed to the DBSCAN and LIGSITE-ray steps described in scripts 005–009.

**Grid dimensions:** 50 × 52 × 42 = 109 200 total points; 16 455 passed the initial burial filter.

---

## Outcome of this phase

The four scripts established:
1. Structure content (LVY in TBD, Zn²⁺ at LON/CULT junction)
2. Complete main-pocket residue list from ligand contacts
3. Zinc coordination shell residues
4. A candidate probe-point cloud for allosteric pocket detection

All downstream pocket characterisation (allosteric site, visualisation, literature comparison) built directly on these results. The full integrated findings are in `CRBN_pocket_analysis.md`.
