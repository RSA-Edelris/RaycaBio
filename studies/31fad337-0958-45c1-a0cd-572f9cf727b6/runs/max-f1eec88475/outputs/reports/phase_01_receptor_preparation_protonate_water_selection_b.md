---
title: "Phase 1: Receptor preparation: protonate, water selection, box definition"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-5c3f1ad2aa"
phase_index: 1
phase_id: "1"
phase_goal: "Receptor preparation: protonate, water selection, box definition"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Receptor preparation: protonate, water selection, box definition

## Summary

This phase set out to receptor preparation: protonate, water selection, box definition. It completed 10 output files.

## Objective

Receptor preparation: protonate, water selection, box definition

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

No method records were captured for this phase, so the procedure cannot be stated. This is a gap in the record, not a phase that did no work.
## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| 001_step_0_verify_dimorphite_dl_import.py | PY | 2.6 KB | 01_receptor_preparation_protonate_water_selection_b/source | 9bf08090dd7e... |
| box_params.json | JSON | 175 B | 01_receptor_preparation_protonate_water_selection_b/work | ae541a1f3660... |
| ctx_ligand.pdb | PDB | 5.7 KB | 01_receptor_preparation_protonate_water_selection_b/structures | 201f9b8dcc6c... |
| ctx_reference_ligand.sdf | SDF | 6.0 KB | 01_receptor_preparation_protonate_water_selection_b/inputs | 897fd5923c27... |
| receptor_prepared.pdb | PDB | 733.0 KB | 01_receptor_preparation_protonate_water_selection_b/structures | b822441a2880... |
| receptor_raw.pdb | PDB | 363.8 KB | 01_receptor_preparation_protonate_water_selection_b/inputs | da4fc83c4635... |
| 002_step_3_build_clean_receptor_pdb_protein_kept_waters.py | PY | 3.0 KB | 01_receptor_preparation_protonate_water_selection_b/source | 2fb32a76f872... |
| 003_path.py | PY | 2.8 KB | 01_receptor_preparation_protonate_water_selection_b/source | 2961da20dab4... |
| receptor_prepared.pdb | PDB | 733.0 KB | 01_receptor_preparation_protonate_water_selection_b/structures | 1668089e6741... |
| 004_pdbfixer_add_missing_atoms_protonate_ph_7_4.py | PY | 1.3 KB | 01_receptor_preparation_protonate_water_selection_b/source | 61621ebfc5fb... |

## Verification

- No tool call is on record for this phase.
- 10 file(s) were produced and registered, 10 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
