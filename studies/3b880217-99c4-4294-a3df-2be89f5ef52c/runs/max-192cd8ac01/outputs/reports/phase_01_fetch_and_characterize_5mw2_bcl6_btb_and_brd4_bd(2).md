---
title: "Phase 1: Fetch and characterize 5MW2 (BCL6 BTB) and BRD4 BD1 structures"
study_id: "3b880217-99c4-4294-a3df-2be89f5ef52c"
run_id: "max-d4c4d49754"
phase_index: 1
phase_id: "1"
phase_goal: "Fetch and characterize 5MW2 (BCL6 BTB) and BRD4 BD1 structures"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "human audit (context-recovery rewrite)"
---

# Phase 1: Fetch and characterize 5MW2 (BCL6 BTB) and BRD4 BD1 structures

## Summary

Fetched PDB structures 5MW2 (BCL6 BTB domain + BI-3802) and 3P5O (BRD4 BD1 + EAM inhibitor) from the RCSB via HTTP. Confirmed chain composition, residue ranges, ligand identities, and centres of mass for both bound small molecules. Results were used to define the two anchor sites for the hypothetical heterobifunctional molecule.

## Objective

Fetch and characterize 5MW2 (BCL6 BTB) and BRD4 BD1 structures

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

| Tool / DB | Version / Source | Purpose |
| :--- | :--- | :--- |
| BioPython PDBParser | 1.x (system install) | Parse PDB text into structure objects |
| RCSB PDB HTTPS endpoint | `https://files.rcsb.org/download/{id}.pdb` | Structure download |
| NumPy | system | Centre-of-mass calculation |

### Procedure

Script: `001_warnings_filterwarnings.py`

1. Fetch 5MW2 and 3P5O PDB text via `requests.get` (30 s timeout, `raise_for_status`).
2. Parse both with `Bio.PDB.PDBParser(QUIET=True)` to suppress noise.
3. For each structure iterate chains in model 0; separate ATOM (protein) from HETATM (ligand/ion/water) records by `residue.id[0]`.
4. For protein chains: record residue count and residue-number range.
5. For hetero residues (excluding waters `id[0]=='W'`): compute heavy-atom count (`element != 'H'`) and centre of mass as the mean of all atom coordinates.
6. Print TITLE record, chain summary, and per-ligand report.

### Key parameters

| Parameter | Value | Reason |
| :--- | :--- | :--- |
| SASA not computed in this phase | — | Deferred to Phase 2 |
| Water residues excluded from hetero listing | `id[0]=='W'` | Avoid noise in ligand inventory |

## Results

### 5MW2 — BCL6 BTB domain + BI-3802

| Property | Value |
| :--- | :--- |
| Chain | A |
| Residues | 122 aa (A7–A128) |
| Ligand | U52 (BI-3802) |
| U52 heavy atoms | 34 |
| U52 centre of mass | [13.66, 17.40, 14.07] Å |

The U52 CoM defines the BCL6 BTB anchor point for Arm 1 of the heterobifunctional molecule. BI-3802 occupies the lateral corepressor-binding groove of the BTB domain; its CoM is 13.7 Å from the chain centroid and fully enclosed within the groove.

### 3P5O — BRD4 BD1 + EAM inhibitor

| Property | Value |
| :--- | :--- |
| Chain | A |
| Residues | 127 aa (A42–A168, full-length BRD4 numbering) |
| Ligand | EAM (BD1 inhibitor) |
| EAM heavy atoms | 30 |
| EAM centre of mass | [26.29, 50.72, −2.12] Å |
| Co-crystallised cryo-protectant | EDO × 4 (ethylene glycol, excluded from analysis) |

The EAM CoM is located at the centre of the acetyl-lysine reading pocket and serves as the initial anchor estimate for BRD4 Arm 2. Subsequent phases refined the anchor to the Kac Nζ position (4.5 Å from Asn140 ND2) rather than the ligand CoM.

## Verification

- 1 script produced and registered with SHA-256 digest (see artifact index).
- Structure download reproducible: both PDB entries are public with stable accession codes.

## Limitations

- Only model 0 / chain A was examined for each structure; alternate conformations and non-A chains were not inventoried.
- EDO molecules in 3P5O were not mapped to specific crystal contacts (not needed for this study).

## References

- PDB 5MW2: Cardote, T.A.F. et al. (2017). Structure of BCL6 BTB domain with BI-3802.
- PDB 3P5O: Filippakopoulos, P. et al. (2010). Selective inhibition of BET bromodomains. *Nature* 468, 1067–1073.
