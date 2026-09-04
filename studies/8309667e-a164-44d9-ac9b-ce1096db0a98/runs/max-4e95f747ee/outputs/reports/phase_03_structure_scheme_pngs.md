## Summary

This phase regenerated all nine synthetic-scheme PNG diagrams for MCUF651, A317, and 7977, replacing the text-label compound boxes from Phase 1 with 2D molecular-structure drawings rendered by RDKit. Three routes per target were produced. The six-step MCUF651 Route C retains the two-row layout introduced in Phase 1.

## Objective

Replace text labels in compound boxes with actual 2D chemical structures, as requested by the user. All other scheme elements (reagents above arrows, conditions/yields below, price labels, coloured boxes, warning text) were preserved from the v2/v3 text schemes.

## Methods

### Software

| Library | Role |
| :--- | :--- |
| RDKit (installed in session) | 2D coordinate generation (`AllChem.Compute2DCoords`) and structure-image rendering (`Draw.MolToImage`) |
| matplotlib 3.x (Agg backend) | Figure layout, arrow annotation, text labels |
| Pillow (PIL) | Intermediate image handling; background-colour substitution |

### Procedure

1. **SMILES dictionary** — SMILES strings were compiled for every starting material, intermediate, and final product across all nine routes. Targets were taken directly from the SDF file parsed in Phase 1. Intermediates were derived manually by forward-synthetic reasoning from each route's established step sequence. All SMILES were passed to `Chem.MolFromSmiles` at runtime; any invalid entry falls back to a blank box, preventing script failure.

2. **Structure rendering** — Each compound was rendered to a NumPy image array via `Draw.MolToImage(mol, size)`. Image dimensions were scaled to the compound-slot size on the matplotlib canvas so that molecules fill the box without distortion.

3. **Layout engine — single-row** (`make_struct_scheme`): identical slot-width arithmetic to the Phase 1 `make_scheme` function (5.2 in/step + 1.0 in padding). Compound slots hold one or two structures; two-compound slots place images side-by-side with a "+" symbol. Box background colours retained: green (SM), blue (intermediate), yellow (product). Reagents above arrows, conditions/yield below, price label in italic below each box, red warning text below conditions.

4. **Layout engine — two-row** (`make_struct_scheme_2row_v2`): used for the six-step MCUF651 Route C. Steps 1–3 in upper row (y = 0.79), steps 4–6 in lower row (y = 0.25). A vertical-then-horizontal connecting arrow links the rows. Row separation was widened from the initial draft (y_top 0.75 → 0.79, y_bot 0.27 → 0.25) to prevent the row-1 warning text from overlapping the row-2 reagent labels; the warning y-offset was also reduced from −0.30 to −0.22 relative to the row centre.

5. **Output** — All nine files saved at 150 dpi with `bbox_inches='tight'`.

### Script

`make_struct_schemes.py` — written to the session directory and executed via `run_python`. The source is also recorded as `014_exec.py` and `015_matplotlib_use.py` in the artifact index.

## Results

### Output files

| File | Target | Route | Steps | Canvas (in) |
| :--- | :--- | :--- | :---: | :--- |
| mcuf651_A_struct.png | MCUF651 | A — amide coupling → N-alkylation | 2 | 11.4 × 7.0 |
| mcuf651_B_struct.png | MCUF651 | B — N-alkylation → CDI amide → Buchwald C–N | 3 | 16.6 × 7.0 |
| mcuf651_C_struct.png | MCUF651 | C — asymmetric hydrogenation (de novo stereocentre), 2-row | 6 | 16.6 × 11.0 |
| a317_A_struct.png | A317 | A — Buchwald N-arylation → α-Br → Hantzsch → amide | 4 | 21.8 × 7.0 |
| a317_B_struct.png | A317 | B — α-Br → Hantzsch → amide → SNAr (Pd-free) | 4 | 21.8 × 7.0 |
| a317_C_struct.png | A317 | C — aminobromothiazole amide → Suzuki (⚠ extrapolative) | 2 | 11.4 × 7.0 |
| 7977_A_struct.png | 7977 | A — SNAr → nitro reduction → CDI → Suzuki → N-alkylation | 5 | 27.0 × 7.0 |
| 7977_B_struct.png | 7977 | B — SNAr → Suzuki → nitro reduction → CDI → N-alkylation ★ | 5 | 27.0 × 7.0 |
| 7977_C_struct.png | 7977 | C — mono-Suzuki + 7-azaindole + Cu-Ullmann (⚠ extrapolative) | 4 | 21.8 × 7.0 |

### Visual quality

- All 2D structures rendered without RDKit errors; no fallback blank boxes were triggered.
- Single-compound boxes (e.g. Route C intermediates [C1]–[C5]) show clearly legible structures at the rendered scale.
- Two-compound boxes are more compact but the key substructures (piperidine ring, fluorothiazole, nitropyridine) remain identifiable.
- The "⚠ autoclave required" warning in MCUF651 Route C is positioned cleanly in the inter-row space after the layout fix.
- Red "⚠ EXTRAPOLATION" text in 7977 Route C and A317 Route C appears correctly below the relevant conditions lines.

## Limitations

- Intermediate SMILES were derived by manual retrosynthetic reasoning; they have not been validated against a structural database. Connectivity is consistent with the stated chemistry, but exact stereochemistry of transient intermediates (e.g. alpha-bromoketones) is not encoded.
- Five-step routes (7977 A, B) produce wide canvases (27 × 7 in); molecule images in two-compound slots at this width are approximately 160 × 110 px, which is readable at full resolution but may appear small when rendered at screen width.
- Inorganic reagents (Fe, K₂CO₃, Cs₂CO₃, CDI) are listed as text above/below arrows and are not drawn as structures; only organic compounds with defined SMILES are shown in boxes.

## References

No external databases were queried in this phase. SMILES for the three targets were carried over from Phase 1 (SDF parsing). Intermediate SMILES were constructed from first principles using the reaction sequences established in Phase 1.
