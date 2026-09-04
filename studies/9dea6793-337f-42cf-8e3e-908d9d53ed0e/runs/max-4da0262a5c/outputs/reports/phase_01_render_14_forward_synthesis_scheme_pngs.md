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

This phase set out to render 14 forward synthesis scheme PNGs. It completed 4 method steps, 17 output files.

## Objective

Render 14 forward synthesis scheme PNGs

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

**Table R.** Key resources used in this phase. Versions are as reported by the running environment; identifiers follow the FORCE11 software citation principles.

| Resource | Type | Version | Identifier | Source |
| :--- | :--- | :--- | :--- | :--- |
| RDKit | software | 2023.9.6 | doi:10.5281/zenodo.591637 | https://www.rdkit.org |

### Procedure

#### 1. Molecular structure extraction and characterisation from V3000 SDF file

Structures of fourteen drug-like compounds were parsed from a V3000 MDL SDF file using RDKit SDMolSupplier. Canonical SMILES, molecular formula, molecular weight, ring count, aromatic ring count, stereocenter count, and hydrogen bond donor/acceptor counts were computed for each molecule.

**Rationale.** Rapid extraction and standardised descriptor computation enables scaffold classification and establishes the baseline structural properties required for retrosynthetic planning.

| Field | Value |
| :--- | :--- |
| Inputs | PoC Retrosynthetic analysis_Targets.sdf |
| Libraries | rdkit |
| Status | running |

Parameters:

```yaml
removeHs: False
sanitize: True
```

#### 2. Retrosynthetic analysis with multi-route generation and scoring

For each of the fourteen compounds, three genuinely independent retrosynthetic routes were derived. Each route was characterised by a one-sentence strategic disconnection statement, expanded into full forward synthesis with reagents, conditions, and expected yield per step with stated basis (literature precedent or extrapolation). Starting materials were sourced to supplier tier and catalogue numb

**Rationale.** Comprehensive retrosynthetic analysis with multiple independent routes and explicit yield bases allows a synthetic chemist to evaluate feasibility, cost, risk, and timing trade-offs before laboratory commitment. Extrapolation flags highlight experimental uncertainty.

| Field | Value |
| :--- | :--- |
| Status | running |

#### 3. Structural visualisation and scaffold classification

All fourteen extracted structures were rendered as 2D annotated PNG images with stereochemical annotation enabled. Structures were organised in a multi-molecule grid and individually as annotated chemistry drawings to support manual scaffold identification and route design.

**Rationale.** Visual inspection of 2D structures with explicit stereochemistry annotation allows chemist-led identification of key disconnection points and retrosynthetic strategy.

| Field | Value |
| :--- | :--- |
| Inputs | PoC Retrosynthetic analysis_Targets.sdf |
| Outputs | all_targets_grid.png |
| Libraries | rdkit |
| Status | running |

Parameters:

```yaml
addStereoAnnotation: True
molsPerRow: 4
```

#### 4. Completeness and internal consistency audit

The retrosynthetic analysis phase was audited for coverage (all 14 compounds included; coverage matrix completed), structural correctness (SMILES and formula verified by RDKit; stereochemical notation handled correctly), yield estimate calibration (basis stated for all steps; extrapolation flags issued where no direct precedent exists), and traceability of scoring metrics to stated assumptions.

**Rationale.** Audit ensures that the deliverables are complete, that claims are traceable to stated assumptions, and that no compound or critical decision was silently omitted or unjustified.

| Field | Value |
| :--- | :--- |
| Status | running |

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

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

- 4 tool call(s) ran in this phase, 0 of which reported a failure.
- 17 file(s) were produced and registered, 17 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

1. Landrum G, et al. RDKit: Open-source cheminformatics. doi:10.5281/zenodo.591637
   *The Zenodo DOI resolves to the latest release. Cite the DOI of the exact version used where possible.*
