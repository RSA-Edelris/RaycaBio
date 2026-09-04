
## Summary

Full forward synthesis scheme PNGs were produced for all 14 target compounds — one figure per compound showing all three routes (A / B / C) as left-to-right horizontal sequences: starting material(s) → synthetic arrow with explicit reagents/solvent/temperature/time/yield → key intermediate(s) → synthetic arrow → target. All 14 figures rendered without error (14/14). The rendering script `render_forward_schemes.py` is self-contained and reproducible.

## Objective

Produce forward synthesis scheme diagrams complementing the ChemSketch-style retrosynthetic schemes. Each figure shows the synthesis in the forward direction with enough reagent detail for a bench chemist to plan experiments directly from the figure.

## Methods

### Software

- RDKit 2023.9.6 — `MolDraw2DCairo`, `Compute2DCoords`, stereo annotation
- matplotlib (Agg backend) — figure composition, arrow annotation, text placement
- Pillow — PNG encode/decode

### Procedure

1. For each compound × route: determined 1-level (lv1 → target) or 2-level (lv2 → lv1 → target) layout from the validated retrosynthetic SMILES in `render_schemes.py`.
2. Assembled node sequence: `[SM_list]` → arrow → `[intermediate_list]` → arrow → `[target]` for 2-level; `[SM_list]` → arrow → `[target]` for 1-level.
3. Each arrow carries reagents + solvent + temperature/time (italic, above) and yield % (green, below). Step number on arrow body.
4. Molecules rendered at 200 × variable px, `addStereoAnnotation = True`. Multiple reactants shown side-by-side with + sign.
5. ★ RECOMMENDED route highlighted with blue title; horizontal dividers separate routes.
6. Figures saved: 24 × 12 in, 100 dpi, white background.

### Layout convention

```
┌──────────────────────────────────────────────────────────────────────┐
│         COMPOUND ID  —  Full Synthetic Schemes (Routes A / B / C)    │
├──────────────────────────────────────────────────────────────────────┤
│  Route A title                                                        │
│  [SM1]+[SM2] ─(1)─ reagents · conds · yield% ──▶ [Int] ─(2)──▶ [TGT]│
├──────────────────────────────────────────────────────────────────────┤
│  Route B title  ★ RECOMMENDED                                         │
│  [SM1]+[SM2] ─(1)─ reagents · conds · yield% ──▶ [TARGET]            │
├──────────────────────────────────────────────────────────────────────┤
│  Route C title                                                        │
│  [SM1]+[SM2] ─(1)──▶ [Int] ─(2)──▶ [TARGET]                          │
└──────────────────────────────────────────────────────────────────────┘
```

## Results

### Output figures

| File | Compound | Scaffold | Route layout |
|---|---|---|---|
| fwd_102EDL248.png | 102EDL248 | 1,5-Benzodiazepinone | A: 1-step; **B: 1-step ★**; C: 1-step |
| fwd_056EDL307.png | 056EDL307 | Dihydroquinazolinone | A: 1-step; B: 1-step; **C: 2-step ★** |
| fwd_587EDL247.png | 587EDL247 | 2-Aminoindanone | **A: 1-step ★**; B: 1-step; C: 1-step |
| fwd_ED091205.png | ED091205 | Spiro-isoindolinone | **A: 1-step ★**; B: 1-step; C: 1-step |
| fwd_ED205141.png | ED205141 | Pyrroloindoline | **A: 2-step ★**; B: 1-step; C: 1-step |
| fwd_ED636906.png | ED636906 | THIQ-1-one biaryl | **A: 2-step ★**; B: 1-step; C: 1-step |
| fwd_ED249356.png | ED249356 | Benzimidazolone | **A: 1-step ★**; B: 1-step; C: 1-step |
| fwd_ED005228.png | ED005228 | Dihydroisoindolone | A: 1-step; **B: 2-step ★**; C: 1-step |
| fwd_ED963829.png | ED963829 | Spiro-azetidinone | A: 1-step; **B: 2-step ★**; C: 1-step |
| fwd_ED106680.png | ED106680 | Galanthamine-type | A: 1-step; **B: 2-step ★**; C: 1-step |
| fwd_test_001.png | test_001 | Isoquinoline-piperidine | A: 2-step; **B: 1-step ★**; C: 1-step |
| fwd_test_002.png | test_002 | Purine kinase ligand | **A: 1-step ★**; B: 1-step; C: 1-step |
| fwd_test_003.png | test_003 | PROTAC-type bifunctional | A: 1-step; **B: 2-step ★**; C: 1-step |
| fwd_test_004.png | test_004 | GlcNAc-Glc-Fuc trisaccharide | A: 2-step; **B: 1-step ★**; C: 1-step |

### Key reagents shown on arrows

| Compound | Route | Conditions on arrow | Yield |
|---|---|---|---|
| 102EDL248 | B ★ | AcOH (0.1 eq), toluene, 100 °C, 6 h [Druey–Schmidt] | 75% |
| 587EDL247 | A ★ | (R)-CBS (0.1 eq), BH₃·THF, CH₂Cl₂, −40 °C, 2 h | 82%, >96% ee |
| ED091205 | A ★ | NaIO₄, MeOH/H₂O; MW 120 °C, MeCN, dr >8:1 | 62% |
| ED963829 | B ★ step 1 | COCl₂ (1.0 eq), Et₃N, CH₂Cl₂, 0 °C, 1 h [isocyanate] | 85% |
| ED963829 | B ★ step 2 | THF, rt [carbamate]; then NaH, DMF, 60 °C [spiro] | 58% |
| test_001 | B ★ | AgNO₃ / (NH₄)₂S₂O₈, H₂SO₄ (aq), 60 °C, 3 h [Minisci] | 45% |
| test_002 | A ★ | i-Pr₂NEt, n-BuOH, 100 °C [C6-SNAr] then 130 °C [C2-SNAr] | 52% |
| test_004 | B ★ | NIS/TfOH (0.1 eq), 4 Å MS, CH₂Cl₂, −20 °C [block glycosylation] | 48% |

## Verification

- 14/14 figures rendered without exception; `exec()` returned no errors
- File sizes 120–174 KB per PNG, consistent with 3-route forward scheme at 100 dpi
- All SMILES are the pre-validated set from `render_schemes.py` (41/42 valid; one corrected in prior phase)
- ★ route assignments verified consistent with `retrosynthetic_analysis_report.md` for all 14 compounds
- Rendering script `render_forward_schemes.py` (18,123 bytes) saved and re-runnable

## Limitations

1. At most 2 synthetic steps shown per route (strategic levels from retrosynthetic analysis). FG-adjustment steps (protection/deprotection, salt formation) are embedded in arrow text rather than shown as separate nodes.
2. Yield estimates carry ±50% relative uncertainty at steps flagged as extrapolations in `retrosynthetic_analysis_report.md`.
3. No atom-mapping or electron-pushing arrows; plan-level representation only.

## Source files

| File | Purpose |
|---|---|
| render_forward_schemes.py | Complete self-contained renderer; re-run to regenerate all 14 PNGs |
| fwd_*.png (×14) | Forward synthesis scheme figures |
| retrosynthetic_analysis_report.md | Full route text with reagents, yields, extrapolation flags |
| scheme_*.png (×14) | Companion retrosynthetic scheme figures |
