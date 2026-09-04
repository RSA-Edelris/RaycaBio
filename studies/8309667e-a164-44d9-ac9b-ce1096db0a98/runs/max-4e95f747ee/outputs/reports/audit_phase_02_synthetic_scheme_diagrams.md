
## Audit checklist

### Files expected vs produced

9 final-quality PNG files were expected (3 routes × 3 targets). All 9 were produced.

| Expected file | Present | Notes |
| :--- | :--- | :--- |
| mcuf651_A_v2.png | ✓ | 2-step, 11.4 × 6.0 in |
| mcuf651_B_v2.png | ✓ | 3-step, 16.6 × 6.0 in |
| mcuf651_C_v3.png | ✓ | 6-step 2-row layout, 16.6 × 9.5 in |
| a317_A_v2.png | ✓ | 4-step, 21.8 × 6.0 in |
| a317_B_v2.png | ✓ | 4-step, 21.8 × 6.0 in |
| a317_C_v2.png | ✓ | 2-step + parallel note, 11.4 × 6.0 in |
| 7977_A_v2.png | ✓ | 5-step, 27.0 × 6.0 in |
| 7977_B_v2.png | ✓ | 5-step, 27.0 × 6.0 in |
| 7977_C_v2.png | ✓ | 4-step, 21.8 × 6.0 in |

### Superseded drafts

9 earlier draft files (mcuf651_route_A/B/C.png, a317_route_A/B/C.png, 7977_route_A/B/C.png) used a fixed total canvas and became illegible at ≥4 steps. These are retained in the artifact index but superseded by the v2/v3 files. mcuf651_C_v2.png (single-row 6-step) is also superseded by mcuf651_C_v3.png (2-row).

### Content checks

**Reagents above arrow**: confirmed present on all 9 files — verified by visual inspection during display.

**Prices below compound boxes**: confirmed for all starting materials.

**Warnings in red**: confirmed for:
- mcuf651_B_v2.png — "SM may exceed €150/g" on 2-Cl-5,6-F₂-benzothiazole
- mcuf651_C_v3.png — "autoclave required" on asymmetric hydrogenation step
- a317_A_v2.png — "use immediately" on α-bromoketone step
- a317_B_v2.png — "use immediately" and "monitor ee — epimerisation risk"
- a317_C_v2.png — "EXTRAPOLATION — boronate prep needs validation"
- 7977_C_v2.png — "EXTRAPOLATION" on triphosgene step and Cu-Ullmann step

**Recommended routes marked**: 7977_B_v2.png title includes "★ RECOMMENDED".

### Known limitations carried forward

1. Parallel steps (picolyl-pyrrole acid for A317; mono-Suzuki fragment for 7977 C) are described in subtitle text only; the diagram format does not render branching.
2. 5-step 7977 routes A/B display at 2× compression on a 2000 px screen; they print correctly at 150 dpi on A3/tabloid. A 2-row version can be generated on request.
3. Intermediate boxes show labels only ([A1], [B2], etc.); full structures are in the retrosynthetic analysis text report.

### Recovery audit

No tool failures occurred during this phase. All 13 `run_python` calls completed with return code 0. The only iteration was an intentional layout upgrade (v1 → v2 fixed-step-width; v2 → v3 two-row for 6-step route).
