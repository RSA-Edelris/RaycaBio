---
title: "Phase 1: Phase 1 — Protein preparation (4CI2)"
study_id: "e26cbe99-cda1-479d-beb9-9d03c9c7cc03"
run_id: "max-7e8c57ab26"
phase_index: 1
phase_id: "1"
phase_goal: "Phase 1 — Protein preparation (4CI2)"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Phase 1 — Protein preparation (4CI2)

## Summary

This phase set out to phase 1 — Protein preparation (4CI2). It completed 19 output files.

## Objective

Phase 1 — Protein preparation (4CI2)

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
| PB-20260903-4CI2_raw.pdb | PDB | 1.8 MB | 01_phase_1_protein_preparation_4ci2/inputs | c2902e096995... |
| 005_download_pdb_4ci2_inspect.py | PY | 1.3 KB | 01_phase_1_protein_preparation_4ci2/source | 3586b38d1b53... |
| 006_extract_lvy_lenalidomide_coordinates_pocket_centre.py | PY | 1.3 KB | 01_phase_1_protein_preparation_4ci2/source | 40b5dc0aeb55... |
| 007_confirm_all_missing_residues_his_tag_linker_there.py | PY | 1013 B | 01_phase_1_protein_preparation_4ci2/source | 83c8afb2fdea... |
| 008_re_parse_remark_465_directly_raw_pdb_lines.py | PY | 1.4 KB | 01_phase_1_protein_preparation_4ci2/inputs | a2ee0a77648f... |
| 009_full_missing_residue_list_chain_b.py | PY | 390 B | 01_phase_1_protein_preparation_4ci2/source | 355707be62e1... |
| 010_phase_1_launch_pdbfixer.py | PY | 1.1 KB | 01_phase_1_protein_preparation_4ci2/source | 6fa03be03dc2... |
| PB-20260903-4CI2_receptor.pdb | PDB | 1.9 MB | 01_phase_1_protein_preparation_4ci2/structures | 3631479233d0... |
| 011_phase_1_pdbfixer_process.py | PY | 2.0 KB | 01_phase_1_protein_preparation_4ci2/source | af54284430f9... |
| PB-20260903-4CI2_receptor_noH.pdb | PDB | 950.4 KB | 01_phase_1_protein_preparation_4ci2/structures | 79dde47e3da6... |
| 012_1_strip_h_receptor_fpocket.py | PY | 1.3 KB | 01_phase_1_protein_preparation_4ci2/source | 90d994b8f7ce... |
| 013_fpocket.py | PY | 1.0 KB | 01_phase_1_protein_preparation_4ci2/source | f90e6433de4e... |
| 014_pocket_characterisation_crystal_structure_pocket.py | PY | 3.0 KB | 01_phase_1_protein_preparation_4ci2/source | 99bbbcc5cc24... |
| protonation-state-results-2.json | JSON | 721 B | 01_phase_1_protein_preparation_4ci2/results | 690f3e56a4cf... |
| protonation-state-results-3.json | JSON | 751 B | 01_phase_1_protein_preparation_4ci2/results | 8daaaef9b18d... |
| protonation-state-results-4.json | JSON | 751 B | 01_phase_1_protein_preparation_4ci2/results | 4e5b545bcb6f... |
| protonation-state-results-5.json | JSON | 667 B | 01_phase_1_protein_preparation_4ci2/results | d7a54b495e8d... |
| protonation-state-results.json | JSON | 715 B | 01_phase_1_protein_preparation_4ci2/results | 4faf406c9adb... |
| 015_protonate_each_ligand_ph_7_4_via_dimorphite_dl.py | PY | 1.1 KB | 01_phase_1_protein_preparation_4ci2/source | 9f08f258fecd... |

## Verification

- No tool call is on record for this phase.
- 19 file(s) were produced and registered, 19 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/pdbfixer:latest`
- Container Image: `registry.rayca.org/rayca-tools/fpocket:latest`
- Container Image: `registry.rayca.org/rayca-tools/protonation-state:latest`

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
