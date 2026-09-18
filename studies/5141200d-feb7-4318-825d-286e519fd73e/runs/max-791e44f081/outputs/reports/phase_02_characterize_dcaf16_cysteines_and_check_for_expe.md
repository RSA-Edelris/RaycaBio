---
title: "Phase 2: Characterize DCAF16 cysteines and check for experimental PDB structure"
study_id: "5141200d-feb7-4318-825d-286e519fd73e"
run_id: "max-48d0e66755"
phase_index: 2
phase_id: "2"
phase_goal: "Characterize DCAF16 cysteines and check for experimental PDB structure"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 2: Characterize DCAF16 cysteines and check for experimental PDB structure

## Summary

This phase set out to characterize DCAF16 cysteines and check for experimental PDB structure. It completed 15 output files.

## Objective

Characterize DCAF16 cysteines and check for experimental PDB structure

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
| 5EU1.pdb | PDB | 363.0 KB | 01_fetch_and_parse_5eu1_brd9_bi_7273_and_alphafold_/structures | 5e68ec174ad9... |
| 001_1_download_5eu1.py | PY | 1.7 KB | 01_fetch_and_parse_5eu1_brd9_bi_7273_and_alphafold_/source | 2d3849017cf2... |
| 002_scan_5eu1_already_memory_pdb_text_intact.py | PY | 932 B | 01_fetch_and_parse_5eu1_brd9_bi_7273_and_alphafold_/source | d3917ac3503c... |
| 003_query_alphafold_api_q9nxf7_get_correct_download_url.py | PY | 573 B | 01_fetch_and_parse_5eu1_brd9_bi_7273_and_alphafold_/source | 25c62575131f... |
| DCAF16_AF.pdb | PDB | 139.6 KB | 01_fetch_and_parse_5eu1_brd9_bi_7273_and_alphafold_/structures | 8c9b8e9dc851... |
| DCAF16_pae.json | JSON | 134.4 KB | 01_fetch_and_parse_5eu1_brd9_bi_7273_and_alphafold_/work | 95e734e00731... |
| 004_urllib_request_urlopen.py | PY | 1.4 KB | 01_fetch_and_parse_5eu1_brd9_bi_7273_and_alphafold_/source | 5c8ba51a62b6... |
| 005_1_parse_5eu1_extract_chain_brd9_protein_atoms_5sw.py | PY | 1.0 KB | 01_fetch_and_parse_5eu1_brd9_bi_7273_and_alphafold_/source | 83a1bd275610... |
| 006_helper_atom_arrays.py | PY | 1.7 KB | 01_fetch_and_parse_5eu1_brd9_bi_7273_and_alphafold_/source | 6ac686c00904... |
| phase_01_fetch_and_parse_5eu1_brd9_bi_7273_and_alphafold_.md | MD | 3.0 KB | reports | 33cd9a319240... |
| 007_1_full_per_residue_plddt_profile_dcaf16.py | PY | 4.0 KB | 02_characterize_dcaf16_cysteines_and_check_for_expe/source | 44bb20d5ffab... |
| 008_1_proper_pdb_rest_search_dcaf16.py | PY | 4.5 KB | 02_characterize_dcaf16_cysteines_and_check_for_expe/source | 826a4ca31cf5... |
| 009_all_dcaf16_heavy_atoms_clash_checking.py | PY | 3.0 KB | 02_characterize_dcaf16_cysteines_and_check_for_expe/source | ae4500cdd602... |
| 010_helper_local_window_clash_check_only_residues_cys.py | PY | 3.7 KB | 02_characterize_dcaf16_cysteines_and_check_for_expe/source | 6a4ec857fe13... |
| 011_cysteine_reactivity_proxies_af_model_disordered.py | PY | 4.1 KB | 02_characterize_dcaf16_cysteines_and_check_for_expe/source | 8c978e74337a... |

## Verification

- No tool call is on record for this phase.
- 15 file(s) were produced and registered, 15 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- No method records were captured, so this phase cannot be reproduced from this report alone.

## References

This phase recorded no external tools or databases.
