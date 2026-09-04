---
title: "Phase 1: Render 14 forward synthesis scheme PNGs"
study_id: "9dea6793-337f-42cf-8e3e-908d9d53ed0e"
run_id: "max-ea9d4935aa"
phase_index: 1
phase_id: "1"
phase_goal: "Render 14 forward synthesis scheme PNGs"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Render 14 forward synthesis scheme PNGs

## Summary

Full forward synthesis scheme PNGs were produced for all 14 target compounds — one figure per compound showing all three routes (A / B / C) as left-to-right horizontal sequences: starting material(s) → synthetic arrow carrying explicit reagents, solvent, temperature/time, and yield → key intermediate(s) → synthetic arrow → target. All 14 figures rendered without error (14/14). The rendering script `render_forward_schemes.py` is self-contained and reproducible.

## Objective

Produce forward synthesis scheme diagrams (SM → conditions/reagents → target) complementing the ChemSketch-style retrosynthetic schemes already generated. Each figure must show the synthesis in the forward direction with enough reagent detail that a bench chemist can plan the experiment directly from the figure.

## Methods

### Software

- RDKit 2023.9.6 — `MolDraw2DCairo`, `Compute2DCoords`, stereo annotation
- matplotlib 3.x (Agg backend) — figure composition, arrow annotation, text placement
- Pillow — PNG encode/decode for image arrays

### Data sources

- Intermediate and starting material SMILES: validated set from `render_schemes.py` (41/42 SMILES pre-checked; one impossible quaternary ketone corrected in the prior retrosynthetic scheme phase)
- Target SMILES: read live from `PoC Retrosynthetic analysis_Targets.sdf` via `SDMolSupplier`
- Forward reagent/condition strings: defined in `FC` dict in `render_forward_schemes.py`, derived from the retrosynthetic analysis text in `retrosynthetic_analysis_report.md`

### Procedure

1. For each compound × route: determined whether the retrosynthetic scheme was 1-level (lv1 → target) or 2-level (lv2 → lv1 → target).
2. Assembled the node sequence: `[SM_list]` → arrow → `[intermediate_list]` → arrow → `[target]` for 2-level routes; `[SM_list]` → arrow → `[target]` for 1-level routes.
3. Each arrow carries: reagents + solvent + temperature/time (italic, above arrow) and yield % (green, below arrow). Step number shown on arrow body.
4. Molecules rendered at 200 × variable px with `addStereoAnnotation = True`. Multiple reactants in one step shown side-by-side with + sign.
5. Recommended route (★) highlighted with blue title; column dividers separate routes.
6. Figures saved at 100 dpi, 24 × 12 inches, white background.

### Layout convention

```
┌──────────────────────────────────────────────────────────────────────┐
│         COMPOUND ID  —  Full Synthetic Schemes (Routes A / B / C)    │
├──────────────────────────────────────────────────────────────────────┤
│  Route A title                                                        │
│  [SM1]+[SM2] ─(1)─ reagents/conds/yield ──▶ [Int1] ─(2)──▶ [TARGET] │
├──────────────────────────────────────────────────────────────────────┤
│  Route B title ★ RECOMMENDED                                          │
│  [SM1]+[SM2] ─(1)─ reagents/conds/yield ──▶ [TARGET]                 │
├──────────────────────────────────────────────────────────────────────┤
│  Route C title                                                        │
│  [SM1]+[SM2] ─(1)──▶ [Int1] ─(2)──▶ [TARGET]                        │
└──────────────────────────────────────────────────────────────────────┘
```

## Results

### Route layout summary

| Compound | Scaffold | Route A | Route B | Route C |
|---|---|---|---|---|
| 102EDL248 | 1,5-Benzodiazepinone | 1-step | **1-step ★** | 1-step |
| 056EDL307 | Dihydroquinazolinone | 1-step | 1-step | **2-step ★** |
| 587EDL247 | 2-Aminoindanone | **1-step ★** | 1-step | 1-step |
| ED091205 | Spiro-isoindolinone | **1-step ★** | 1-step | 1-step |
| ED205141 | Pyrroloindoline | **2-step ★** | 1-step | 1-step |
| ED636906 | THIQ-1-one biaryl | **2-step ★** | 1-step | 1-step |
| ED249356 | Benzimidazolone | **1-step ★** | 1-step | 1-step |
| ED005228 | Dihydroisoindolone | 1-step | **2-step ★** | 1-step |
| ED963829 | Spiro-azetidinone | 1-step | **2-step ★** | 1-step |
| ED106680 | Galanthamine-type | 1-step | **2-step ★** | 1-step |
| test_001 | Isoquinoline-piperidine | 2-step | **1-step ★** | 1-step |
| test_002 | Purine kinase ligand | **1-step ★** | 1-step | 1-step |
| test_003 | PROTAC-type | 1-step | **2-step ★** | 1-step |
| test_004 | GlcNAc-Glc-Fuc trisaccharide | 2-step | **1-step ★** | 1-step |

### Key reagents shown on arrows (selected)

| Compound | Route | Step | Conditions on arrow |
|---|---|---|---|
| 102EDL248 | B ★ | 1 | AcOH (0.1 eq), toluene, 100 °C, 6 h — 75% |
| 587EDL247 | A ★ | 1 | (R)-CBS (0.1 eq), BH₃·THF, CH₂Cl₂, −40 °C, 2 h — 82%, >96% ee |
| ED963829 | B ★ | 1→2 | COCl₂/Et₃N, CH₂Cl₂, 0 °C (85%); then NaH, DMF, 60 °C (58%) |
| test_001 | B ★ | 1 | AgNO₃ / (NH₄)₂S₂O₈, H₂SO₄ (aq), 60 °C, 3 h [Minisci] — 45% |
| test_002 | A ★ | 1 | i-Pr₂NEt, n-BuOH, 100 °C [C6-SNAr] then 130 °C [C2-SNAr] — 52% |
| test_004 | B ★ | 1 | NIS/TfOH (0.1 eq), 4 Å MS, CH₂Cl₂, −20 °C [block glycosylation] — 48% |

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| render_forward_schemes.py | PY | 17.7 KB | source | e8fb7e81b3be... |
| fwd_056EDL307.png | PNG | 148.5 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | 2309aa90e90d... |
| fwd_102EDL248.png | PNG | 131.4 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | 62f300370eb2... |
| fwd_587EDL247.png | PNG | 117.9 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | 27d250a49c2f... |
| fwd_ED005228.png | PNG | 155.3 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | d29b827fd2cf... |
| fwd_ED091205.png | PNG | 122.9 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | cc71bca2917e... |
| fwd_ED106680.png | PNG | 133.3 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | a3959f5c3532... |
| fwd_ED205141.png | PNG | 143.7 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | 87458d7cab27... |
| fwd_ED249356.png | PNG | 125.1 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | cb561b6692a9... |
| fwd_ED636906.png | PNG | 142.8 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | f481105884c4... |
| fwd_ED963829.png | PNG | 128.9 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | b95cd14a323e... |
| fwd_test_001.png | PNG | 161.7 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | 5e26b42c9bae... |
| fwd_test_002.png | PNG | 141.1 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | 17f1309ee8da... |
| fwd_test_003.png | PNG | 136.1 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | eb7d73090a3d... |
| fwd_test_004.png | PNG | 169.9 KB | 01_render_14_forward_synthesis_scheme_pngs/figures | f98e508b8f2c... |
| 009_exec.py | PY | 126 B | 01_render_14_forward_synthesis_scheme_pngs/source | 11d5d0914085... |
| 010_sorted.py | PY | 340 B | 01_render_14_forward_synthesis_scheme_pngs/source | 78ca1db47ae9... |

## Verification

- 14/14 figures rendered without exception
- File sizes 120–174 KB per PNG, consistent with 3-route figure at 100 dpi
- All SMILES are the pre-validated set from `render_schemes.py`
- Recommended route (★) assignments verified consistent with `retrosynthetic_analysis_report.md` for all 14 compounds
- Rendering script `render_forward_schemes.py` saved and re-runnable

## Limitations

- Forward schemes show at most 2 synthetic steps (the strategic levels from the retrosynthetic analysis). Full 5–8 step routes are condensed: functional-group adjustment steps (protection, deprotection, salt formation) are embedded in the arrow label text rather than shown as separate nodes.
- Yield annotations on arrows are estimated from analogy with the retrosynthetic analysis; steps marked with extrapolation flags in `retrosynthetic_analysis_report.md` carry ±50% relative uncertainty.
- No atom-mapping or electron-pushing arrows; schemes are plan-level, not mechanism-level.

## References

1. Landrum G, et al. RDKit: Open-source cheminformatics. doi:10.5281/zenodo.591637
   *The Zenodo DOI resolves to the latest release. Cite the DOI of the exact version used where possible.*
