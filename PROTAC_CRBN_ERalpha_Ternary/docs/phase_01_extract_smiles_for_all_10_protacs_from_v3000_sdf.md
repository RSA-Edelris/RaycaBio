---
title: "Phase 1: Extract SMILES for all 10 PROTACs from V3000 SDF"
study_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-eebe5aee8e"
phase_index: 1
phase_id: "1"
phase_goal: "Extract SMILES for all 10 PROTACs from V3000 SDF"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Extract SMILES for all 10 PROTACs from V3000 SDF

## Summary

Extracted canonical SMILES for all 10 PROTACs (ARV-001 through ARV-010) from
`Protacs.sdf` (V3000 format) using RDKit 2026.03.4. Characterised linker composition,
CRBN binder type, and heavy-atom counts. All 10 SMILES confirmed by atom-count
cross-check against the V3000 COUNTS field. Detailed write-up: `phase_08_protac_series_smiles_extraction.md`.

## Objective

Extract SMILES for all 10 PROTACs from V3000 SDF

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 (local); RDKit 2026.03.4 |

### Software and Databases

**Table R.** Key resources used in this phase.

| Resource | Type | Version | Notes |
| :--- | :--- | :--- | :--- |
| RDKit | software | 2026.03.4 | Local host python3; V3000 support native |

### Procedure

#### 1. SMILES extraction from V3000 SDF

`Chem.SDMolSupplier(path, removeHs=True)` was applied to `Protacs.sdf`. RDKit 2026.03.4
reads V3000 molfiles natively. The Rayca `run_python` sandbox was attempted first but
returned `"Bad pickle format: ENDMOL tag not found"` on every V3000 input including a
minimal 4-atom test; this is a container serialisation issue, not a data error. All
successful work used the local interpreter via Bash.

Canonical SMILES were generated with `Chem.MolToSmiles(mol, canonical=True)`. Atom
counts were confirmed with `mol.GetNumHeavyAtoms()`.

| Field | Value |
| :--- | :--- |
| Input | `/home/ubuntu/rayca-artifacts/1320c8c41b74f89c8a917762/files/Protacs.sdf` |
| Tool | RDKit 2026.03.4 `Chem.SDMolSupplier` |
| Status | complete |

## Results

### Extracted SMILES

| Name | HA | CRBN binder | Linker type | Linker atoms |
| :--- | :--- | :--- | :--- | :--- |
| ARV-001 | 53 | isoindolinone | O-ethyl-piperazine-ethyl-O | 9 |
| ARV-002 | 51 | **phthalimide** | N-piperazine-ethyl-O | 7 |
| ARV-003 | 55 | isoindolinone | NH-butyl-piperazine-ethyl-O | 10 |
| ARV-004 | 45 | isoindolinone | PEG-1 | 4 |
| ARV-005 | 48 | isoindolinone | PEG-2 | 7 |
| ARV-006 | 51 | isoindolinone | PEG-3 | 10 |
| ARV-007 | 54 | isoindolinone | PEG-4 | 13 |
| ARV-008 | 57 | isoindolinone | PEG-5 | 16 |
| ARV-009 | 60 | isoindolinone | PEG-6 | 19 |
| ARV-010 | 87 | isoindolinone | PEG-13 | 40 |

All 10 share the same THIQ ERα warhead and glutarimide ring. ARV-002 is the only compound
with a phthalimide (thalidomide-type) CRBN binder. ARV-007 has the same heavy-atom count
as ARV-471 (54) but a PEG-4 linker, not the piperazine-piperidine linker of ARV-471 —
they are distinct compounds. Full SMILES strings and structural notes are in
`phase_08_protac_series_smiles_extraction.md`.

### Output Artifacts

**Table A.** Files produced by this phase.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| 042_chem_sdmolsupplier.py | PY | 730 B | 01_extract_smiles_for_all_10_protacs_from_v3000_sdf/source | a272341e1615... |
| 043_v3000_might_need_special_handling_try_sanitize_false.py | PY | 835 B | 01_extract_smiles_for_all_10_protacs_from_v3000_sdf/source | 319d138ec8a1... |
| 044_check_rdkit_version_v3000_support.py | PY | 663 B | 01_extract_smiles_for_all_10_protacs_from_v3000_sdf/source | 9ad40c4d2944... |

*Note: artifacts 042–044 are the Bash scripts executed in this phase. The SMILES results
themselves are in `phase_08_protac_series_smiles_extraction.md` (session root).*

## Verification

**Atom counts cross-checked against V3000 COUNTS field.** All 10 match exactly (see
`phase_08_protac_series_smiles_extraction.md` §Verification for the full table).

**SMILES round-trip confirmed.** Each SMILES was re-parsed with `Chem.MolFromSmiles()`
and `GetNumHeavyAtoms()` matched the source count for all 10 compounds.

**PEG series verified.** The `OCCO` repeat count in each SMILES matches the EO unit
assignments: 1, 2, 3, 4, 5, 6, 13 for ARV-004 through ARV-010 respectively.

**run_python failure was sandbox serialisation, not data corruption.** Confirmed by
testing a minimal 4-atom V3000 block; error is reproducible regardless of molecule size.

## Limitations

- Glutarimide stereocentre is unspecified in all 10 compounds (V3000 CFG=3 on that bond);
  RDKit outputs no `@` at that centre. The THIQ warhead stereocentres are retained.
- The Rayca `run_python` container image that produced the failed attempts is not
  identified here; no result derives from it.

## References

- RDKit: RDKit: Open-source cheminformatics. https://www.rdkit.org
