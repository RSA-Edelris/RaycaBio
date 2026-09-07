
doc = """## Objective

Build a self-contained interactive HTML viewer so docking poses from the CRBN (4CI2) study can be inspected in any browser without installing software.

## Methods

### Inputs

| File | Role |
|:--|:--|
| `PB-20260903-4CI2_receptor_trimmed_fixed.pdb` | 142-residue CRBN pocket fragment (chain B, ≤20 Å from LVY centroid), orphan-TER-fixed |
| `poses_EDS01357518_ent1.sdf` … `poses_EDS01889984.sdf` | 5-pose gnina output SDF per compound (5 files) |
| `final_results.json` | Vina, CNN pose score, pKi, ΔG for each compound |

### Procedure

1. **Pocket contact residues identified** — NumPy distance search (≤4.5 Å) of all protein atoms against best-scoring ligand (EDS01806218_ent2); 14 residues returned including TRP 104, TRP 110, TRP 123 (tri-Trp basket), ASN 76, HIS 78, TYR 80.

2. **Data embedded** — receptor PDB (183 KB), per-compound pose SDF blocks (5 × 5 poses; ~82 KB total), score JSON, and compound metadata embedded as JavaScript template-literal strings after backtick/`${`-escaping. Poses pre-split by `$$$$` into individual blocks for per-pose style control.

3. **3Dmol.js viewer** — CDN-loaded (`3dmol.csb.pitt.edu`). On compound selection:
   - Receptor loaded as cartoon (#b0b8cc, opacity 0.85).
   - 14 contact residues rendered as CPK sticks; TRP 104/110/123 labelled via `addLabel(text, style, {resi, model, atom:'CA'})` (3-argument API).
   - All 5 poses loaded individually via `addModel(sdf, 'sdf')`; active pose full opacity/radius 0.18, inactive at 15% opacity/radius 0.10.
   - Optional VDW surface (opacity 0.35) via `addSurface`.

4. **Controls** — Pose 1–5 toggle, Cartoon/+Surface protein display, Pocket residues on/off, Reset view, per-compound score cards.

5. **Bug fixes applied before final write**:
   - Replaced `{position: {resi}}` label spec (not valid 3Dmol.js API) with 3-argument `addLabel` form.
   - Removed `sphere:` style blocks (caused empty-object trailing-comma risk; sticks sufficient for drug-like ligands).

### Output

`docking_viewer.html` — 276 KB, fully self-contained, no server required.

## Verification

15 structural checks run against the written file (Python string inspection):

| Check | Result |
|:--|:--|
| 3Dmol CDN script tag present | PASS |
| `RECEPTOR_PDB` template literal embedded (file > 200 KB) | PASS |
| `POSES` object present | PASS |
| `SCORES` object present | PASS |
| `COMPOUNDS` array present | PASS |
| 5 compound IDs present | PASS |
| Pose SDFs embedded as literals (not file references) | PASS |
| `POCKET_RESI` array starts at residue 76 | PASS |
| Tri-Trp basket `[104, 110, 123]` present | PASS |
| `addLabel` uses 3-argument selection form | PASS |
| `selectPose`, `setProteinStyle`, `togglePocket`, `resetView` functions present | PASS (×4) |
| No residual `sphere:` style blocks | PASS |

All 15 checks passed. File size confirmed at 275.6 KB.

## Limitations

- Requires an internet connection to load 3Dmol.js from CDN (no offline fallback).
- Receptor is the 142-residue trimmed fragment used for docking, not the full 4CI2 complex — global fold context is absent.
- Pose scores shown are from gnina (Vina AutoDock-Vina scoring + CNN rescore); ΔG is CNN-derived (−1.364 × pKi), not MM-GBSA.
- Labels for TRP residues are positioned at Cα; if the Cα atom is not present in the trimmed fragment the label falls back to the residue centroid.
"""

finish(doc)
