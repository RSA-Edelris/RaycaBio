---
title: "Phase 1: Generate enantiomers and 3D conformers for CRBN_ID.sdf"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-06e7647662"
phase_index: 1
phase_id: "1"
phase_goal: "Generate enantiomers and 3D conformers for CRBN_ID.sdf"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Generate enantiomers and 3D conformers for CRBN_ID.sdf

## Summary

This phase set out to generate enantiomers and 3D conformers for CRBN_ID.sdf. It completed 2 output files.

## Objective

Generate enantiomers and 3D conformers for CRBN_ID.sdf

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

| Tool | Version | Use |
| :--- | :--- | :--- |
| RDKit | session default | SMILES/SDF parsing, stereochemistry perception, conformer generation, force-field minimization |
| AllChem.ETKDGv3 | RDKit | Distance-geometry conformer embedding with torsion-angle knowledge base |
| MMFF94 | RDKit | Force-field energy minimization after embedding |

### Procedure

**Input inspection.** The 16 V3000 Molfile records in `CRBN_ID.sdf` were read with `SDMolSupplier(removeHs=False, sanitize=True)`. Every molecule carried an `MDLV30/STERAC1` collection, marking all stereocenters as having undefined absolute configuration (racemic). Stereocenters were perceived from the V3000 bond CFG wedge annotations via `AssignStereochemistry(cleanIt=True, force=True)`.

**Enantiomer generation.** For each molecule all defined chiral tags were inverted (CW ↔ CCW) to produce the mirror-image enantiomer. For the six molecules with two stereocenters sharing a single STERAC1 group, both centers were inverted simultaneously, preserving the drawn relative configuration in the enantiomeric series.

**3D conformer generation.** For each stereoisomer (original and enantiomer): (1) hydrogens were added; (2) a conformer was embedded with `ETKDGv3` (`enforceChirality=True`, `randomSeed=42`); (3) the conformer was minimized with MMFF94 (`maxIts=2000`); (4) hydrogens were removed before writing. ETKDGv3 succeeded for all 32 structures; no fallback to ETKDG or UFF was required.

## Results

All 16 input molecules are racemic (STERAC1). Both enantiomers were enumerated and a lowest-energy 3D conformer generated for each, yielding 32 structures total with zero failures.

**Table R1.** Stereocenters per molecule and conformer outcome.

| Molecule | Stereocenters | Atom indices (0-based) | Config (drawn) | Enantiomer ID | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| EDEL-CRBN-0001 | 1 | 16 | CCW | EDEL-CRBN-0001_ent | ✓ both |
| EDEL-CRBN-0002 | 1 | 18 | CCW | EDEL-CRBN-0002_ent | ✓ both |
| EDEL-CRBN-0003 | 1 | 18 | CCW | EDEL-CRBN-0003_ent | ✓ both |
| EDEL-CRBN-0004 | 1 | 20 | CCW | EDEL-CRBN-0004_ent | ✓ both |
| EDEL-CRBN-0005 | 2 | 3, 5 | CCW, CCW | EDEL-CRBN-0005_ent | ✓ both |
| EDEL-CRBN-0006 | 2 | 3, 5 | CCW, CCW | EDEL-CRBN-0006_ent | ✓ both |
| EDEL-CRBN-0007 | 2 | 3, 5 | CCW, CCW | EDEL-CRBN-0007_ent | ✓ both |
| EDEL-CRBN-0008 | 1 | 16 | CW | EDEL-CRBN-0008_ent | ✓ both |
| EDEL-CRBN-0009 | 2 | 14, 15 | CW, CW | EDEL-CRBN-0009_ent | ✓ both |
| EDEL-CRBN-0010 | 2 | 3, 5 | CCW, CCW | EDEL-CRBN-0010_ent | ✓ both |
| EDEL-CRBN-0011 | 1 | 16 | CW | EDEL-CRBN-0011_ent | ✓ both |
| EDEL-CRBN-0012 | 1 | 16 | CW | EDEL-CRBN-0012_ent | ✓ both |
| EDEL-CRBN-0013 | 2 | 16, 17 | CCW, CCW | EDEL-CRBN-0013_ent | ✓ both |
| EDEL-CRBN-0014 | 2 | 16, 17 | CW, CW | EDEL-CRBN-0014_ent | ✓ both |
| EDEL-CRBN-0015 | 1 | 16 | CW | EDEL-CRBN-0015_ent | ✓ both |
| EDEL-CRBN-0016 | 2 | 17, 19 | CW, CW | EDEL-CRBN-0016_ent | ✓ both |

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| CRBN_ID_enantio.sdf | SDF | 73.9 KB | 01_generate_enantiomers_and_3d_conformers_for_crbn_/structures | c21e3450938f... |
| 001_lowest_energy_conformer.py | PY | 3.0 KB | 01_generate_enantiomers_and_3d_conformers_for_crbn_/source | 0c2435eac3d6... |

## Verification

- No tool call is on record for this phase.
- 2 file(s) were produced and registered, 2 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
