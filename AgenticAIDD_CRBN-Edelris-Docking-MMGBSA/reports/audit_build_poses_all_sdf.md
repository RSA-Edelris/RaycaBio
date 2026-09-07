---
title: "Audit — Build poses_all.sdf (top 5 poses, all 54 compounds)"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-affd8a7bf7"
audit_type: "human-authored post-hoc"
phase: "Build poses_all.sdf with all 5 docking poses for all 32+22 compounds"
date: "2026-09-07"
---

# Audit — Build poses_all.sdf

## What Was Built

`poses_all.sdf`: a single SDF file containing the top 5 gnina docking poses for all 54 compounds in the CRBN docking campaign (22 CRBN_ID_enantio_2 stereoisomers + 32 EDEL-CRBN compounds), 270 records total.

## Key Technical Note: Raw-Text SDF Construction

The file was assembled by parsing SDF records as raw text (splitting on `$$$$`) and injecting new SD tag lines, **without** loading molecules through RDKit's SDMolSupplier/SDWriter. This was required because:

- gnina embeds an extra `$$$$` terminator inside property blocks of its SDF output
- When RDKit re-writes such records via SDWriter, each record is split into two (valid + corrupt), doubling the record count
- Raw-text injection preserves original 3D coordinates and mol block geometry exactly

## Verification

Checks run programmatically (2026-09-07) via `build_poses_all.py` + inline verification code:

### Record count

| Check | Expected | Observed | Pass |
|-------|----------|----------|------|
| Total records (270 = 22×5 + 32×5) | 270 | 270 | ✓ |
| $$$$ separators in output file | 270 | 270 | ✓ |
| 22-compound set records | 110 | 110 | ✓ |
| 32-compound set records | 160 | 160 | ✓ |

### Compound coverage

| Check | Expected | Observed | Pass |
|-------|----------|----------|------|
| Distinct compound names | 54 | 54 | ✓ |
| Records with `Compound_Name` tag | 270 | 270 | ✓ |
| Records with `Pose_Rank` tag | 270 | 270 | ✓ |
| Compounds with unexpected pose ranks | 0 | 0 | ✓ |
| All compounds have exactly ranks 1–5 | all 54 | all 54 | ✓ |
| Any `_poses` suffix in `Compound_Name` | 0 | 0 | ✓ |

### 22-compound set SD tags (sample: Compound_10_ent1, rank 1)

| Tag | Value |
|-----|-------|
| `Molecule Name` | Compound 10 |
| `EC50 (µM) (Excel)` | 14.3 |
| `Compound_Name` | Compound_10_ent1 |
| `Pose_Rank` | 1 |
| `Docking_Affinity_kcal_mol` | -9.47 |
| `CNN_Affinity` | 6.68 |
| `CNN_Pose_Score` | 0.5844 |

### 32-compound set SD tags (sample: EDEL-CRBN-0001_ent, rank 1)

| Tag | Value |
|-----|-------|
| `ID` | EDEL-CRBN-0001_ent |
| `Stereoisomer` | enantiomer |
| `minimizedAffinity` | -8.26589 |
| `CNNscore` | 0.9102458358 |
| `CNNaffinity` | 6.7187666893 |
| `Compound_Name` | EDEL-CRBN-0001_ent |
| `Pose_Rank` | 1 |

### File

| Check | Expected | Observed | Pass |
|-------|----------|----------|------|
| File exists at session root | yes | yes | ✓ |
| File size | >700 KB | 756,429 bytes | ✓ |

## Source Script

`build_poses_all.py` — session workspace, raw-text SDF assembly, no RDKit mol re-write.

## GitHub

Committed to `RSA-Edelris/RaycaBio` at commit `8a081f5`:
- `AgenticAIDD_CRBN-Edelris-Docking-MMGBSA/results/poses_all.sdf`
- `AgenticAIDD_CRBN-Edelris-Docking-MMGBSA/scripts/build_poses_all.py`
