
## Objective

Produce a single PDB file of the BRD4 BD1 / VHL:ElonginCB ternary complex model for
visualisation and downstream use (docking, clash screening, E2-accessibility checks).

---

## What was done

### 1. Transform recovery
The Kabsch rotation matrix (Rf) and translation vector (tf) from the prior superposition
phase were re-derived from scratch to confirm reproducibility:
- Needleman–Wunsch alignment of BD1 and BD2 SEQRES sequences (42% identity)
- Kabsch fit on gap-free Cα pairs, iterative 2σ outlier trimming
- Result: **0.53 Å core RMSD over 73 residues** — identical to the prior phase

### 2. Coordinate extraction and transformation

| Output chain | Source | Records extracted | Transform applied |
|-------------|--------|-------------------|-------------------|
| A (BD1) | 3MXF chain A, ATOM | 1,074 atoms | Rf / tf (Kabsch) |
| A (JQ1) | 3MXF chain A, HETATM resname JQ1 | 31 atoms | Rf / tf (Kabsch) |
| B (VHL) | 5T35 chain D, ATOM | 1,215 atoms | None (verbatim) |
| B (MZ1) | 5T35 chain D, HETATM resname 759 | 69 atoms | None (verbatim) |
| C (ElonginC) | 5T35 chain C, ATOM | 689 atoms | None (verbatim) |
| D (ElonginB) | 5T35 chain B, ATOM | 814 atoms | None (verbatim) |

Waters (HOH/WAT), crystallographic additives (DMS, EDO, IOD), and the second
crystallographic copy (5T35 chains E–H) were excluded.

### 3. Output file

**`BRD4BD1_VHL_ternary_model.pdb`** — 3,892 ATOM/HETATM records, 261,087 bytes.
REMARK header records document the provenance and chain assignments.

---

## Sanity checks

| Check | Result | Pass? |
|-------|--------|-------|
| BD1 Cα centroid vs BD2 Cα centroid (5T35) | 2.25 Å | ✓ (expected small offset from fold differences) |
| VHL centroid displacement (chain B vs 5T35 chain D) | 0.00 Å | ✓ (verbatim copy) |
| ElonginC centroid displacement | 0.00 Å | ✓ |
| ElonginB centroid displacement | 0.00 Å | ✓ |
| BD1–VHL centroid distance | 39.4 Å | ✓ (consistent with compact ternary) |
| VHL–ElonginC centroid distance | 28.0 Å | ✓ (consistent with VHL:EC sub-complex) |
| JQ1–MZ1 warhead bridging gap | ~5.6 Å | ✓ (matches linker model input) |

---

## How to use the file

- Load in PyMOL / ChimeraX / UCSF Chimera — chains A–D display immediately
- JQ1 (chain A, resname JQ1) sits in BD1's acetyl-lysine pocket
- MZ1 VHL warhead (chain B, resname 759) anchors the VHL side
- The ~5.6 Å gap between JQ1 and MZ1 represents the linker-bridging space
- For an explicit linker: use RDKit or Corina to generate 3D conformers of a
  PEG3/PEG4 linker (12–18 heavy atoms) constrained to the two exit atoms

---

## Limitations

1. No energy minimisation was performed — side-chain clashes at the BD1–VHL interface
   are possible and should be checked before use in docking.
2. The linker between JQ1 and the VHL warhead is absent; the file models binary anchors only.
3. BD1 and BD2 have different surface residues at the VHL contact face; visual inspection
   of the interface is recommended before interpreting contact maps.
4. MZ1 (chain B) represents the BD2-targeting warhead, not a BD1-specific compound;
   its presence is for VHL binding-mode reference only.
