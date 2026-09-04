---
title: "Phase 1: Generate ChemSketch-style retrosynthetic scheme images for all 14 compounds"
study_id: "9dea6793-337f-42cf-8e3e-908d9d53ed0e"
run_id: "max-2c6d36f425"
phase_index: 1
phase_id: "1"
phase_goal: "Generate ChemSketch-style retrosynthetic scheme images for all 14 compounds"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Generate ChemSketch-style retrosynthetic scheme images for all 14 compounds

## Summary

This phase set out to generate ChemSketch-style retrosynthetic scheme images for all 14 compounds. It completed 4 method steps, 18 output files.

## Objective

Generate ChemSketch-style retrosynthetic scheme images for all 14 compounds

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
| 006_nc1ccccc1c.py | PY | 2.1 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/source | 4196d50cc10d... |
| 007_part_1_helpers_scheme_data.py | PY | 6.2 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/source | d671fb2f5b63... |
| render_schemes.py | PY | 17.3 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/source | 54bb5c9150ba... |
| scheme_056EDL307.png | PNG | 170.2 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | c14b0049da68... |
| scheme_102EDL248.png | PNG | 127.9 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | c895049a87e5... |
| scheme_587EDL247.png | PNG | 127.5 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | ef846e6f7764... |
| scheme_ED005228.png | PNG | 153.6 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | 7c36e6bd513f... |
| scheme_ED091205.png | PNG | 138.3 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | 9793647353b8... |
| scheme_ED106680.png | PNG | 156.8 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | 6b6a18f6a922... |
| scheme_ED205141.png | PNG | 149.2 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | 2447411657b0... |
| scheme_ED249356.png | PNG | 145.2 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | 9047db2452ec... |
| scheme_ED636906.png | PNG | 172.8 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | 7a20138a63a0... |
| scheme_ED963829.png | PNG | 152.6 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | e3516b0233a7... |
| scheme_test_001.png | PNG | 197.1 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | 2440259e9050... |
| scheme_test_002.png | PNG | 174.9 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | e9ba0450786e... |
| scheme_test_003.png | PNG | 171.9 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | b049ca00d836... |
| scheme_test_004.png | PNG | 188.9 KB | 01_generate_chemsketch_style_retrosynthetic_scheme_/figures | 50a5d9ba05bb... |
| 008_exec.py | PY | 118 B | 01_generate_chemsketch_style_retrosynthetic_scheme_/source | 678ad04bcf81... |

## Verification

- 4 tool call(s) ran in this phase, 0 of which reported a failure.
- 18 file(s) were produced and registered, 18 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No limitations were detected automatically. This is not a statement that none exist.

## References

1. Landrum G, et al. RDKit: Open-source cheminformatics. doi:10.5281/zenodo.591637
   *The Zenodo DOI resolves to the latest release. Cite the DOI of the exact version used where possible.*
