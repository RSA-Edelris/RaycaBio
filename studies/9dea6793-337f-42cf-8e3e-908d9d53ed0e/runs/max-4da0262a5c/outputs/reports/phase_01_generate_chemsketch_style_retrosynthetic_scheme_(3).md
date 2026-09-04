
## Summary

Fourteen retrosynthetic scheme PNG images were generated — one per drug-like target compound — each showing all three independent routes side by side in a ChemSketch-convention layout. Each figure places the target structure at the top centre, then three columns (Routes A, B, C) below, with double retrosynthetic arrows (⟹) connecting each retrosynthetic level, reaction labels in red italics on the arrows, molecule structures rendered by RDKit with stereo annotations, and supplier-tier source lines at the base of each column. The recommended route in each column is marked ★. All 14 figures rendered without error.

## Objective

Produce visual retrosynthetic scheme diagrams for all 14 target compounds that a synthetic chemist can read at a glance, equivalent to the output of ChemDraw/ChemSketch retrosynthetic drawing tools: target at top, starting materials at bottom, retrosynthetic arrows between levels, reaction and condition labels, and starting material sourcing.

## Methods

### Software

- RDKit (2024) via `rdMolDraw2D.MolDraw2DCairo` for 2D structure rendering with stereo annotations
- matplotlib (Agg backend) for figure composition
- Pillow for image format conversion

### Procedure

1. All 14 target SMILES were read fresh from the V3000 MDL SDF file using `Chem.SDMolSupplier(removeHs=False, sanitize=True)`.
2. Retrosynthetic scheme data were defined in `render_schemes.py` as a Python dictionary keyed by compound ID. Each entry contains three route records with title, recommended flag, level-1 intermediate SMILES, arrow label, optional level-2 starting material SMILES, optional second arrow label, and supplier tier/catalogue strings.
3. A validity pre-check (006_nc1ccccc1c.py) tested all 42 intermediate SMILES before rendering: 41/42 passed; the one failure (`O=C1(C)CCN(C(=O)OC(C)(C)C)CC1`, an impossible quaternary ketone carbon) was replaced before rendering.
4. Each figure was composed using `matplotlib.figure` with `add_axes` for molecule images at fixed fractional positions. Retrosynthetic arrows were drawn using `ax.annotate` with a double-line effect (two offset arrows). Column dividers were drawn as `plt.Line2D` artists.
5. Figures were saved at 100 dpi, 21 × 16 inches (≈ 2100 × 1600 px), white background.
6. The full rendering script is saved as `render_schemes.py` (17,675 bytes).

## Results

### Output figures

| File | Compound | Scaffold | Routes shown |
|---|---|---|---|
| scheme_102EDL248.png | 102EDL248 | 1,5-Benzodiazepinone | A: Mannich; **B: Druey–Schmidt ★**; C: Enamine |
| scheme_056EDL307.png | 056EDL307 | Dihydroquinazolinone | A: Isatoic anhydride; B: 3-comp.; **C: Amino-acid ★** |
| scheme_587EDL247.png | 587EDL247 | 2-Aminoindanone | **A: CBS redn. ★**; B: α-Bromination; C: Strecker |
| scheme_ED091205.png | ED091205 | Spiro-isoindolinone | **A: Nitrone [3+2] ★**; B: Radical; C: Schmidt |
| scheme_ED205141.png | ED205141 | Pyrroloindoline | **A: L-Trp chiral pool ★**; B: Pictet–Spengler; C: Pd C–H |
| scheme_ED636906.png | ED636906 | THIQ-1-one biaryl | **A: Convergent 3-frag. ★**; B: Bischler–Napieralski; C: Suzuki |
| scheme_ED249356.png | ED249356 | Benzimidazolone | **A: Isatoic anhydride ★**; B: Anthranilamide; C: Buchwald |
| scheme_ED005228.png | ED005228 | Dihydroisoindolone | A: Nitrone [3+2]; **B: Azomethine ylide ★**; C: Staudinger |
| scheme_ED963829.png | ED963829 | Spiro-azetidinone | A: Staudinger [2+2]; **B: Isocyanate spiro ★**; C: RCM |
| scheme_ED106680.png | ED106680 | Galanthamine-type | A: Oxidative coupling; **B: Mannich/CBS/Mitsunobu ★**; C: RCM |
| scheme_test_001.png | test_001 | Isoquinoline-piperidine | A: Organolithium/Barton–McCombie; **B: Minisci radical ★**; C: Rh(I) iminium |
| scheme_test_002.png | test_002 | Purine kinase ligand | **A: Sequential SNAr ★**; B: 2-F-6-Cl-purine; C: Buchwald |
| scheme_test_003.png | test_003 | PROTAC-type bifunctional | A: De novo 3-fragment; **B: Pomalidomide + THIQ ★**; C: Late Suzuki |
| scheme_test_004.png | test_004 | GlcNAc-Glc-Fuc trisaccharide | A: Schmidt imidate linear; **B: Thioglycoside block ★**; C: One-pot orthogonal |

### Figure layout convention

```
┌─────────────────────────────────────────────────────────────────┐
│           COMPOUND ID — Retrosynthetic Analysis (Routes A/B/C)  │
├─────────────────────────────────────────────────────────────────┤
│         TARGET STRUCTURE (large, stereo annotations)            │
├────────────────┬────────────────┬───────────────────────────────┤
│  Route A       │  Route B ★     │  Route C                      │
│    ⟹           │    ⟹           │    ⟹                          │
│  [int 1]       │  [int 1]       │  [int 1]                      │
│    ⟹ (opt)     │    ⟹ (opt)     │    ⟹ (opt)                    │
│  [SM1]+[SM2]   │  [SM1]+[SM2]   │  [SM1]+[SM2]                  │
│  Tier | Cat    │  Tier | Cat    │  Tier | Cat                   │
└────────────────┴────────────────┴───────────────────────────────┘
```

Arrow labels (red italic): reaction name, key reagent, temperature, selectivity note.  
★ = recommended route. Molecules rendered at 200 × 165 px (level 1) or 200 × 155 px (level 2).

## Verification

- All 14 figures rendered without RDKit parse errors (blank grey tiles would appear for invalid SMILES; none were observed).
- SMILES validity was pre-checked: 41/42 valid; the one failure was identified and replaced before rendering.
- Output file sizes are consistent: 130–202 KB per PNG, appropriate for 21×16 in at 100 dpi with molecular content.
- Recommended route markers (★) verified consistent with the text analysis recommendations for all 14 compounds.
- The rendering script `render_schemes.py` is saved in the workspace and can be re-run to regenerate all figures.
- Full audit: `scheme_generation_audit.md`.

## Limitations

1. Intermediates shown may omit protecting groups for visual clarity; full PG schemes are in `retrosynthetic_analysis_report.md`.
2. Schemes show at most 2 retrosynthetic levels; longer routes are collapsed to show only the strategic disconnections.
3. No atom-mapping; no electron-pushing mechanism arrows.

## Source files

| File | Purpose |
|---|---|
| render_schemes.py | Complete self-contained rendering script |
| 006_nc1ccccc1c.py | SMILES validation pre-check |
| 007_part_1_helpers_scheme_data.py | Development cell (superseded) |
| 008_exec.py | Execution wrapper |
