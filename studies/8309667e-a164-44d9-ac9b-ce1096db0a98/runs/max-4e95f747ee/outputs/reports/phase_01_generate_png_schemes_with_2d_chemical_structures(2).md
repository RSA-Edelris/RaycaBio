---
title: "Phase 1: Generate PNG schemes with 2D chemical structures for all 9 routes"
study_id: "8309667e-a164-44d9-ac9b-ce1096db0a98"
run_id: "max-e5095bffca"
phase_index: 1
phase_id: "1"
phase_goal: "Generate PNG schemes with 2D chemical structures for all 9 routes"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Generate PNG schemes with 2D chemical structures for all 9 routes

## Summary

This phase set out to generate PNG schemes with 2D chemical structures for all 9 routes. It completed 13 output files.

## Objective

Generate PNG schemes with 2D chemical structures for all 9 routes

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

This phase used no external software or databases that the record identifies by name.

### Software

| Library | Role |
| :--- | :--- |
| RDKit | 2D coordinate generation (`AllChem.Compute2DCoords`) and structure rendering (`Draw.MolToImage`) |
| matplotlib 3.x (Agg) | Figure layout, arrow annotation, text labels |
| Pillow (PIL) | Intermediate image handling and background-colour substitution |

### Procedure

All nine synthetic-scheme PNG diagrams for MCUF651, A317, and 7977 were regenerated with 2D molecular-structure drawings in the compound boxes, replacing the text labels used in the previous text-label schemes.

1. **SMILES dictionary** — SMILES strings were compiled for every starting material, intermediate, and final product across all nine routes. Targets were taken from the SDF file parsed in the retrosynthetic-analysis phase. Intermediates were derived by forward-synthetic reasoning from each route's step sequence. All SMILES are validated at runtime via `Chem.MolFromSmiles`; any failure falls back to a blank white box without crashing.

2. **Structure rendering** — Each compound was rendered to a NumPy image array via `Draw.MolToImage(mol, size)`, scaled to the compound-slot dimensions of the matplotlib canvas.

3. **Single-row layout** (`make_struct_scheme`): canvas width = n_steps × 5.2 in + 1.0 in padding. One- or two-compound slots supported; two-compound slots show structures side-by-side with a "+" symbol. Box background colours: green (SM, step 0), blue (intermediate), yellow (product). Reagents above arrows, conditions/yield below, price labels in italic, red warning text for scale-up flags and extrapolations.

4. **Two-row layout** (`make_struct_scheme_2row_v2`): used for the 6-step MCUF651 Route C. Steps 1–3 in upper row (y = 0.79), steps 4–6 in lower row (y = 0.25), connected by a vertical-then-horizontal arrow. Row separation was widened from an initial draft (Δy = 0.48 → 0.54) to prevent the row-1 warning text from overlapping row-2 reagent labels.

5. All files saved at 150 dpi with `bbox_inches='tight'`. Source script: `make_struct_schemes.py`.

## Results

**Final diagrams:**

| File | Target | Route | Steps | Canvas (in) |
| :--- | :--- | :--- | :---: | :--- |
| mcuf651_A_struct.png | MCUF651 | A — amide coupling → N-alkylation | 2 | 11.4 × 7.0 |
| mcuf651_B_struct.png | MCUF651 | B — N-alkylation → CDI amide → Buchwald C–N | 3 | 16.6 × 7.0 |
| mcuf651_C_struct.png | MCUF651 | C — asymmetric hydrogenation, 2-row | 6 | 16.6 × 11.0 |
| a317_A_struct.png | A317 | A — Buchwald N-arylation → α-Br → Hantzsch → amide | 4 | 21.8 × 7.0 |
| a317_B_struct.png | A317 | B — α-Br → Hantzsch → amide → SNAr (Pd-free) | 4 | 21.8 × 7.0 |
| a317_C_struct.png | A317 | C — aminobromothiazole amide → Suzuki (⚠ extrapolative) | 2 | 11.4 × 7.0 |
| 7977_A_struct.png | 7977 | A — SNAr → reduction → CDI → Suzuki → N-alkylation | 5 | 27.0 × 7.0 |
| 7977_B_struct.png | 7977 | B — SNAr → Suzuki → reduction → CDI → N-alkylation ★ | 5 | 27.0 × 7.0 |
| 7977_C_struct.png | 7977 | C — mono-Suzuki + 7-azaindole + Cu-Ullmann (⚠ extrapolative) | 4 | 21.8 × 7.0 |

No RDKit rendering failures (white-box fallbacks) were observed in any output file. All SMILES in the SML dictionary parse successfully.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| make_struct_schemes.py | PY | 32.8 KB | 01_generate_png_schemes_with_2d_chemical_structures/source | 877436dfc7a6... |
| 7977_A_struct.png | PNG | 175.0 KB | 01_generate_png_schemes_with_2d_chemical_structures/figures | b7a4ad37ea7f... |
| 7977_B_struct.png | PNG | 176.7 KB | 01_generate_png_schemes_with_2d_chemical_structures/figures | d2979a004a37... |
| 7977_C_struct.png | PNG | 158.3 KB | 01_generate_png_schemes_with_2d_chemical_structures/figures | 5de50d417f88... |
| a317_A_struct.png | PNG | 147.3 KB | 01_generate_png_schemes_with_2d_chemical_structures/figures | f23a79857611... |
| a317_B_struct.png | PNG | 137.7 KB | 01_generate_png_schemes_with_2d_chemical_structures/figures | 944a821dc944... |
| a317_C_struct.png | PNG | 95.3 KB | 01_generate_png_schemes_with_2d_chemical_structures/figures | 3fa6280826e8... |
| mcuf651_A_struct.png | PNG | 74.7 KB | 01_generate_png_schemes_with_2d_chemical_structures/figures | 477c007298ab... |
| mcuf651_B_struct.png | PNG | 109.5 KB | 01_generate_png_schemes_with_2d_chemical_structures/figures | ae9babc77a94... |
| mcuf651_C_struct.png | PNG | 197.9 KB | 01_generate_png_schemes_with_2d_chemical_structures/figures | 519de12a5358... |
| 014_exec.py | PY | 121 B | 01_generate_png_schemes_with_2d_chemical_structures/source | aa60bf0b4f03... |
| mcuf651_C_struct.png | PNG | 196.1 KB | 01_generate_png_schemes_with_2d_chemical_structures/figures | 10ea84e3917d... |
| 015_matplotlib_use.py | PY | 8.3 KB | 01_generate_png_schemes_with_2d_chemical_structures/source | 29894ee0a047... |

## Verification

- No tool call is on record for this phase.
- 13 file(s) were produced and registered, 13 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
