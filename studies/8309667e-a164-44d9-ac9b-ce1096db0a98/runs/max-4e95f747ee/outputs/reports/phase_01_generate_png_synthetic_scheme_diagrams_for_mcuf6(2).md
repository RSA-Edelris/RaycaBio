---
title: "Phase 1: Generate PNG synthetic scheme diagrams for MCUF651, A317, 7977"
study_id: "8309667e-a164-44d9-ac9b-ce1096db0a98"
run_id: "max-e6e2fcafb5"
phase_index: 1
phase_id: "1"
phase_goal: "Generate PNG synthetic scheme diagrams for MCUF651, A317, 7977"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Generate PNG synthetic scheme diagrams for MCUF651, A317, 7977

## Summary

This phase set out to generate PNG synthetic scheme diagrams for MCUF651, A317, 7977. It completed 26 output files.

## Objective

Generate PNG synthetic scheme diagrams for MCUF651, A317, 7977

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

### Procedure

Linear synthetic scheme PNG diagrams were generated for all three routes per target (MCUF651, A317, 7977) using **matplotlib** (Agg backend, 150 dpi). Each diagram uses a custom box-and-arrow layout with the following conventions:

- **Canvas sizing**: fixed 5.2 inches per step plus 1.0 inch padding, so text size is constant regardless of step count.
- **Compound boxes**: green = starting materials (first step), blue = intermediates, yellow/cream = final product. Rounded rectangles with a blue border.
- **Arrow annotation**: reagent names and prices above each arrow; solvent, temperature, time, and expected yield below. Warnings (scale-up flags, extrapolations, autoclave requirements) in red below conditions.
- **Two-row layout** for the 6-step MCUF651 Route C: steps 1–3 in the upper row, steps 4–6 in the lower row, connected by a vertical-then-horizontal arrow at the right-hand edge (file: mcuf651_C_v3.png).

An initial set of diagrams used a fixed total canvas width (route_A/B/C.png files); these became illegible at ≥ 4 steps and were superseded by the fixed-step-width v2/v3 files. The superseded files are retained in the artifact index.

## Results

**Final diagrams (use these):**

| File | Target | Route | Steps |
| :--- | :--- | :--- | :--- |
| mcuf651_A_v2.png | MCUF651 | A — Amide coupling → N-alkylation | 2 |
| mcuf651_B_v2.png | MCUF651 | B — N-alkylation → CDI amide → Buchwald C–N | 3 |
| mcuf651_C_v3.png | MCUF651 | C — Asymmetric hydrogenation (de novo stereocentre), 2-row | 6 |
| a317_A_v2.png | A317 | A — Buchwald N-arylation → α-Br → Hantzsch → amide | 4 |
| a317_B_v2.png | A317 | B — α-Br → Hantzsch → amide → SNAr (Pd-free) | 4 |
| a317_C_v2.png | A317 | C — Aminobromothiazole amide → Suzuki (⚠ extrapolative) | 2 + parallel |
| 7977_A_v2.png | 7977 | A — SNAr → reduction → CDI → Suzuki → N-alkylation | 5 |
| 7977_B_v2.png | 7977 | B — SNAr → Suzuki → reduction → CDI → N-alkylation ★ | 5 |
| 7977_C_v2.png | 7977 | C — Dibromopyrimidine Suzuki + 7-azaindole + Cu-Ullmann (⚠ extrapolative) | 4 |

**Superseded drafts** (fixed total canvas, illegible at ≥ 4 steps): mcuf651_route_A/B/C.png, a317_route_A/B/C.png, 7977_route_A/B/C.png, mcuf651_C_v2.png.

All reagent prices are Sigma-Aldrich / Combi-Blocks list at 1 g scale. Full reagent price table and route scoring are in the retrosynthetic analysis text report (phase_01_retrosynthetic_analysis_mcuf651_a317_7977.md).

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| mcuf651_route_A.png | PNG | 59.5 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | d95d616e4ffb... |
| mcuf651_route_B.png | PNG | 75.6 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 64ee71359b2e... |
| mcuf651_route_C.png | PNG | 101.7 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 5b68e7661c43... |
| 007_matplotlib_use.py | PY | 7.8 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/source | 9ac9afd8d05e... |
| a317_route_A.png | PNG | 110.6 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 4dc7eeda2e1a... |
| a317_route_B.png | PNG | 105.6 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 845297a0ab48... |
| a317_route_C.png | PNG | 86.5 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 1d018843615e... |
| 008_matplotlib_use.py | PY | 6.9 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/source | 389e4aabce6f... |
| 7977_route_A.png | PNG | 81.5 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 46d94018c62e... |
| 7977_route_B.png | PNG | 83.8 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 66aa040c18fe... |
| 7977_route_C.png | PNG | 98.6 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | c1d27a9aa088... |
| 009_matplotlib_use.py | PY | 7.5 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/source | a016aad65ccc... |
| mcuf651_A_v2.png | PNG | 56.4 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | c20655c71e65... |
| mcuf651_B_v2.png | PNG | 81.6 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 4a635be277ab... |
| mcuf651_C_v2.png | PNG | 113.1 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | f6b2b04a4b36... |
| 010_matplotlib_use.py | PY | 6.7 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/source | cbc7563b9375... |
| a317_A_v2.png | PNG | 107.8 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 0309168882dc... |
| a317_B_v2.png | PNG | 103.8 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | f6871d2d9db3... |
| a317_C_v2.png | PNG | 80.6 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 3290d9b341f8... |
| 011_matplotlib_use.py | PY | 6.7 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/source | c5478dd8d77d... |
| 7977_A_v2.png | PNG | 103.4 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 4f07f88048c9... |
| 7977_B_v2.png | PNG | 105.5 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | c00bb77fcf04... |
| 7977_C_v2.png | PNG | 101.3 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 3ebe65c4c813... |
| 012_matplotlib_use.py | PY | 7.2 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/source | 9a6ba8e78116... |
| mcuf651_C_v3.png | PNG | 117.6 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/figures | 14e8cfb65346... |
| 013_matplotlib_use.py | PY | 6.8 KB | 01_generate_png_synthetic_scheme_diagrams_for_mcuf6/source | 9b3679731531... |

## Verification

- No tool call is on record for this phase.
- 26 file(s) were produced and registered, 26 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
