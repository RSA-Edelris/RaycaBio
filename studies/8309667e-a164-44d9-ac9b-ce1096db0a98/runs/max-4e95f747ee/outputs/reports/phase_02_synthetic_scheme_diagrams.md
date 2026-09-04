
## Objective

Generate publication-quality linear synthetic scheme diagrams as PNG files for all three routes per target (MCUF651, A317, 7977). Each diagram shows compound boxes connected by arrows, with reagents printed above each arrow, reaction conditions and expected yield below, and commercially available starting material prices in italic below each compound box.

## Methods

All diagrams were generated in Python using **matplotlib** (Agg backend, 150 dpi) with custom box-and-arrow layout logic. Key design decisions:

- **Fixed per-step width** of 5.2 inches per step rather than a fixed total canvas width. This prevents text from becoming illegible as step count increases.
- **Colour coding**: green boxes = starting materials (first step only), blue boxes = intermediates, yellow/cream boxes = final product.
- **Two-row layout** for 6-step routes (MCUF651 Route C) to maintain readability on screen: steps 1–3 in the upper row, steps 4–6 in the lower row, connected by a vertical-then-horizontal arrow at the right-hand edge.
- Reagent names and prices appear above the arrow; solvent, temperature, time, and yield appear below. Warnings (scale-up flags, extrapolations, special equipment) appear in red below conditions.

## Output Files

| Filename | Target | Route | Steps | Canvas (in) |
| :--- | :--- | :--- | :--- | :--- |
| mcuf651_A_v2.png | MCUF651 | A — Amide coupling → N-alkylation | 2 | 11.4 × 6.0 |
| mcuf651_B_v2.png | MCUF651 | B — N-alkylation → CDI → Buchwald C–N | 3 | 16.6 × 6.0 |
| mcuf651_C_v3.png | MCUF651 | C — Asymmetric hydrogenation (de novo) | 6 (2-row) | 16.6 × 9.5 |
| a317_A_v2.png | A317 | A — Buchwald → α-bromination → Hantzsch → amide | 4 | 21.8 × 6.0 |
| a317_B_v2.png | A317 | B — α-bromination → Hantzsch → amide → SNAr (Pd-free) | 4 | 21.8 × 6.0 |
| a317_C_v2.png | A317 | C — Aminobromothiazole amide → Suzuki | 2 + parallel | 11.4 × 6.0 |
| 7977_A_v2.png | 7977 | A — SNAr → reduction → CDI → Suzuki → N-alkylation | 5 | 27.0 × 6.0 |
| 7977_B_v2.png | 7977 | B — SNAr → Suzuki → reduction → CDI → N-alkylation ★ | 5 | 27.0 × 6.0 |
| 7977_C_v2.png | 7977 | C — Dibromopyrimidine Suzuki + 7-azaindole + Cu-Ullmann | 4 | 21.8 × 6.0 |

Earlier draft versions (mcuf651_route_A.png, mcuf651_route_B.png, mcuf651_route_C.png, a317_route_A/B/C.png, 7977_route_A/B/C.png) used a fixed total canvas width and were superseded by the v2/v3 files above, which maintain a constant per-step width for consistent legibility.

## Reagent Prices Shown in Diagrams

All prices are Sigma-Aldrich / Combi-Blocks list at 1 g scale. Values are embedded in each compound box label or price line. Full price table is in the retrosynthetic analysis text report. All starting materials are ≤ €150/g except 2-chloro-5,6-difluorobenzothiazole (MCUF651 Route B, €120–200/g, flagged ⚠ in the diagram).

## Limitations

- Diagrams use compound abbreviations ([A1], [B2], etc.) for intermediates; full IUPAC names and SMILES are in the accompanying retrosynthetic analysis text.
- Parallel steps (picolyl-pyrrole acid synthesis for A317; mono-Suzuki fragment for 7977 Route C) are noted in diagram subtitles but not drawn as separate branching arrows — this is a layout limitation of the linear scheme format.
- A317 Route C boronate synthesis (decarboxylative borylation) is marked ⚠ EXTRAPOLATION in the diagram; this step requires experimental validation before the route is committed.
- 7977 Route C steps 2 and 3 are similarly marked ⚠ EXTRAPOLATION.
