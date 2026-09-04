
## Summary

Fourteen forward synthesis scheme PNGs were generated — one per compound — each showing all three routes (A / B / C) as left-to-right horizontal sequences: starting materials → synthetic arrow with full reagents and conditions → key intermediate(s) → synthetic arrow → target. All 14 figures rendered without error.

## Objective

Complement the retrosynthetic analysis and ChemSketch-style retrosynthetic scheme images with full **forward** synthesis sequences that a synthetic chemist can follow bench-to-product: explicit reagents, solvents, temperatures, times, and expected yield on every arrow.

## Methods

### Layout convention

Each figure (24 × 12 in, 100 dpi, white background) contains three route rows separated by horizontal dividers:

```
┌────────────────────────────────────────────────────────────────────────────┐
│          COMPOUND ID  —  Full Synthetic Schemes (Routes A / B / C)         │
├────────────────────────────────────────────────────────────────────────────┤
│  Route A title                                                              │
│  [SM1] + [SM2]  ─(1)──reagents/conds──▶  [Intermediate]  ─(2)──▶  [TARGET]│
│                       yield %                                yield %        │
├────────────────────────────────────────────────────────────────────────────┤
│  Route B title  ★ RECOMMENDED                                               │
│  [SM1] + [SM2]  ─(1)──▶  [Intermediate]  ─(2)──▶  [TARGET]                │
├────────────────────────────────────────────────────────────────────────────┤
│  Route C title                                                              │
│  [SM1] + [SM2]  ─(1)──▶  [TARGET]                                          │
└────────────────────────────────────────────────────────────────────────────┘
```

- **1-level routes** (single strategic disconnection): one arrow, SMs directly to target
- **2-level routes** (two strategic disconnections): two arrows, SMs → key intermediate → target
- Arrow labels: reagent(s), solvent, temperature/time in italic above the arrow; yield % in green below
- Step number in parentheses on each arrow
- ★ RECOMMENDED marks the recommended route per compound
- Molecules rendered by RDKit `MolDraw2DCairo` at 200 × variable px with stereo annotations

### Reagents shown (representative)

| Transformation class | Conditions shown |
|---|---|
| Druey–Schmidt BDZ condensation | AcOH (0.1 eq), toluene, 100 °C, 6 h |
| CBS asymmetric reductive amination | (R)-CBS (0.1 eq), BH₃·THF, CH₂Cl₂, −40 °C |
| Nitrone [3+2] cycloaddition | MW 120 °C, MeCN, 2 h; dr >8:1 |
| Pictet–Spengler | TFA (cat.), CH₂Cl₂, rt, 1–12 h |
| Bischler–Napieralski | POCl₃, MeCN, 80 °C; then NaBH₄ |
| Buchwald–Hartwig C–N | Pd₂(dba)₃/BrettPhos, Cs₂CO₃, toluene, 100 °C |
| Minisci radical decarboxylation | AgNO₃ / (NH₄)₂S₂O₈, H₂SO₄ (aq), 60 °C |
| Sequential SNAr (purine) | i-Pr₂NEt, n-BuOH, 100 °C (C6) then 130 °C (C2) |
| Intramolecular Mitsunobu | DEAD/PPh₃, THF, rt |
| Thioglycoside glycosylation | NIS/TfOH (0.1 eq), 4 Å MS, CH₂Cl₂, −20 °C |
| Schmidt trichloroacetimidate | TMSOTf (0.1 eq), 4 Å MS, −40 °C to −60 °C |
| Isocyanate spiro closure | COCl₂/Et₃N, CH₂Cl₂, 0 °C; then NaH, DMF, 60 °C |

## Results

### Output files

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
| fwd_test_004.png | test_004 | GlcNAc-Glc-Fuc trisaccharide | **A: 2-step ★** (alt); **B: 1-step ★**; C: 1-step |

### Yield annotations (recommended routes, key steps)

| Compound | Route | Step 1 yield | Step 2 yield | Overall (scheme) |
|---|---|---|---|---|
| 102EDL248 | B Druey–Schmidt | 75% | — | 75% |
| 056EDL307 | C Convergent | 80% | 72% | 58% |
| 587EDL247 | A CBS redn. | 82% | — | 82% |
| ED091205 | A Nitrone [3+2] | 62% | — | 62% |
| ED205141 | A L-Trp | 75% | 62% | 47% |
| ED636906 | A 3-Fragment | 70% | 62% | 43% |
| ED249356 | A Isatoic | 72% | — | 72% |
| ED005228 | B Azomethine ylide | 65% | 65% | 42% |
| ED963829 | B Isocyanate spiro | 85% | 58% | 49% |
| ED106680 | B Mitsunobu | 78% | 52% | 41% |
| test_001 | B Minisci | 45% | — | 45% |
| test_002 | A SNAr | 52% | — | 52% |
| test_003 | B Pomalidomide | 62% | 55% | 34% |
| test_004 | B Thioglycoside | 48% | — | 48% |

*Yields are scheme-level (key strategic steps only); full linear sequence yields including functional-group adjustments are lower and are reported in `retrosynthetic_analysis_report.md`.*

## Verification

- All 14 PNGs rendered without exception (14/14)
- File sizes 120–174 KB, consistent with 3-route figure at 100 dpi
- All SMILES are the validated set from `render_schemes.py` (41/42 pre-checked valid; one impossible quaternary ketone was corrected in that prior phase)
- Recommended route (★) assignments match `retrosynthetic_analysis_report.md` for all 14 compounds
- Rendering script saved as `render_forward_schemes.py` (self-contained, re-runnable)

## Source files

| File | Purpose |
|---|---|
| render_forward_schemes.py | Complete self-contained renderer; re-run to regenerate |
| fwd_*.png (×14) | Forward synthesis scheme figures |
| retrosynthetic_analysis_report.md | Full text analysis with all route details |
| scheme_*.png (×14) | Companion retrosynthetic scheme figures |
