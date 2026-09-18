---
title: "Phase 2: Calculate BCL6 BTB surface accessibility and identify candidate residues"
study_id: "3b880217-99c4-4294-a3df-2be89f5ef52c"
run_id: "max-d4c4d49754"
phase_index: 2
phase_id: "2"
phase_goal: "Calculate BCL6 BTB surface accessibility and identify candidate residues"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "human audit (context-recovery rewrite)"
---

# Phase 2: Calculate BCL6 BTB surface accessibility and identify candidate residues

## Summary

Computed per-residue solvent-accessible surface area (SASA) for BCL6 BTB (5MW2, chain A) using the Shrake-Rupley algorithm. Identified surface-exposed Lys (SASA > 30 Å²) as primary candidates for bromodomain reading and Ser/Thr (SASA > 20 Å²) as secondary candidates. Measured Nζ (or OG/OG1) distances to the BI-3802 anchor to inform linker-length estimates.

## Objective

Calculate BCL6 BTB surface accessibility and identify candidate residues

## Methods

### Environment

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

| Tool | Version | Purpose |
| :--- | :--- | :--- |
| BioPython ShrakeRupley | system | Per-residue SASA computation |
| NumPy | system | Distance calculations |

### Procedure

Script: `002_bcl6_btb_5mw2_surface_residue_analysis.py`

1. Instantiate `Bio.PDB.SASA.ShrakeRupley`; call `sr.compute(bcl6, level="R")` on the full 5MW2 structure to annotate each residue with a `.sasa` attribute.
2. Extract the U52 (BI-3802) CoM from Phase 1 as the linker anchor reference.
3. Iterate all protein residues in chain A sorted by residue number.
4. For Lys: if SASA > 30 Å², record residue number, SASA, Nζ coordinates, and Nζ–U52-CoM distance. Add to `surface_lys` list.
5. For Ser/Thr: if SASA > 20 Å², record OG or OG1 coordinates and distances. Add to `surface_serthr` list.
6. Print the top 6 Ser/Thr by proximity to the anchor.
7. Persist `surface_lys` and `surface_serthr` into `geom.pkl` alongside coordinates from Phase 1.

### Key parameters

| Parameter | Value | Justification |
| :--- | :--- | :--- |
| Lys SASA threshold | 30 Å² | Standard cutoff separating buried from accessible side chains |
| Ser/Thr SASA threshold | 20 Å² | Lower threshold reflecting smaller Ser/Thr side-chain surface area |
| SASA level | residue | Required for total per-residue exposure; atom level not needed here |

## Results

### Surface-exposed Lys on BCL6 BTB

| Residue | SASA (Å²) | Nζ coord (Å) | Dist to U52 CoM (Å) | B-factor Cα / Nζ |
| :--- | :--- | :--- | :--- | :--- |
| Lys 66 | 92.6 | [16.5, 22.7, 22.1] | 17.4 | 57.9 / 101.0 |
| Lys 123 | 122.5 | [10.0, 33.1, 13.5] | 17.3 | 60.8 / 105.3 |
| Lys 126 | 176.2 | [14.0, 35.5, 6.7] | 25.7 | 72.0 / 126.3 |

All three Lys have Cα–Nζ spans of 5.56–6.35 Å (fully extended conformations, consistent with their high SASA).

### Surface-exposed Ser/Thr closest to BI-3802 anchor (top 6)

| Residue | SASA (Å²) | Dist to U52 CoM (Å) |
| :--- | :--- | :--- |
| Ser 59 | — | 8.9 |
| Thr 62 | — | 9.5 |
| Thr 48 | — | 13.5 |
| Ser 99 | — | 14.7 |
| Ser 102 | — | 15.2 |
| Thr 19 | — | 16.8 |

Ser/Thr were recorded for completeness (possible phosphorylation-state or hydroxy-group dependent interactions) but are not further analysed in this study, which focuses on Lys as the primary acetylation target.

## Verification

- 3 files produced (Phase 1 script inherited, Phase 1 report, Phase 2 script), all registered with SHA-256.
- SASA values are consistent with typical BTB domain surface exposure: the three Lys are all in exposed loop regions. K66 and K123 are in inter-helix loops; K126 is at the disordered C-terminal tail (residue 126 of 128 in chain A).

## Limitations

- B-factors used as a disorder proxy are a single-crystal property and do not account for solution conformational diversity.
- SASA computed on the monomeric chain A only; BCL6 BTB is a homodimer in solution. Dimer-interface burial was not assessed and could alter K66/K123 accessibility.

## References

- Lee, B. & Richards, F.M. (1971). The interpretation of protein structures: estimation of static accessibility. *J Mol Biol* 55, 379–400.
- Shrake, A. & Rupley, J.A. (1973). Environment and exposure to solvent of protein atoms. *J Mol Biol* 79, 351–371.
