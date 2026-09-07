---
title: "Audit — Phase: Create final_calculation.sdf, final_calculation_2d.sdf, final_pose.pdb"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
audit_type: "human-authored post-hoc"
---

# Audit — Create final_calculation.sdf, final_calculation_2d.sdf, final_pose.pdb

## What Was Built

Three deliverable files consolidating all campaign results:

| File | Description |
|------|-------------|
| `final_calculation.sdf` | 22 compounds, best 3D docked pose + 17 SD tags |
| `final_calculation_2d.sdf` | 22 compounds, 2D depiction of correct enantiomer + 17 SD tags |
| `final_pose.pdb` | CRBN receptor (chain B) + LVY crystal ligand + 22 docked poses (chains C–X) |

## Key Technical Issue Resolved

**gnina SDF `$$$$` contamination**: gnina embeds an extra `$$$$` record terminator inside the properties block of each SDF record. When RDKit loads and re-writes via `SDWriter`, this creates a split entry per molecule — SDMolSupplier read 44 records (22 valid + 22 corrupt) instead of 22.

Fix: `mol.ClearProp(pname)` called for all existing properties immediately after loading, before any new properties are set. This strips the embedded terminator and produces a clean 22-record output.

## Verification

Checks run programmatically (2026-09-07) via `build_final_outputs.py` + verification code:

### final_calculation.sdf (3D)

| Check | Expected | Observed | Pass |
|-------|----------|----------|------|
| Records loaded by SDMolSupplier | 22 | 22 | ✓ |
| None (corrupt) records | 0 | 0 | ✓ |
| File size | >70 KB | 78,229 bytes | ✓ |
| 3D coordinates present (max\|z\| > 0.01 Å) | all 22 | all 22 | ✓ |
| Stereo in SMILES\_stereo (@ or /) | all 22 | all 22 | ✓ |
| Required SD tags present | all 17 tags on all 22 | all 17 tags on all 22 | ✓ |
| `Docking_Affinity_kcal_mol` range | −11 to −6 kcal/mol | −10.23 to −6.60 | ✓ |
| `MMGBSA_dG_kcal_mol` range | physically plausible | −37.56 to +9.35 | ✓ |

### final_calculation_2d.sdf (2D enantiomers)

| Check | Expected | Observed | Pass |
|-------|----------|----------|------|
| Records loaded | 22 | 22 | ✓ |
| None records | 0 | 0 | ✓ |
| All z coordinates = 0.000 | yes | yes (max\_z = 0.0000 for all) | ✓ |
| Same SD tags as 3D file | yes | yes | ✓ |

### final_pose.pdb

| Check | Expected | Observed | Pass |
|-------|----------|----------|------|
| ATOM records (receptor chain B) | 6,188 | 6,188 | ✓ |
| LVY crystal HETATM records | 32 | 32 | ✓ |
| Docked LIG HETATM records | >600 | 698 | ✓ |
| Chains used | B + C–X (23 total) | B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X | ✓ |
| TER records | 23 | 23 | ✓ |
| REMARK lines (one per ligand) | 22 | 22 | ✓ |
| File size | >500 KB | 562,949 bytes | ✓ |

## Source Script

`build_final_outputs.py` — in session workspace, ~160 lines, pure Python/RDKit.

## GitHub

Committed to RSA-Edelris/RaycaBio at commit `431054f3ae514e540d3060fcbbacbe3e7a2425ee`.
