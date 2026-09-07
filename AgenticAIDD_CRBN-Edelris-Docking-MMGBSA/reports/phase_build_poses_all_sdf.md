---
title: "Phase: Build poses_all.sdf with all 5 docking poses for all 32+22 compounds"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-affd8a7bf7"
phase_id: "1"
phase_goal: "Build poses_all.sdf containing top 5 docking poses for all 54 compounds (22 CRBN_ID_enantio_2 stereoisomers + 32 EDEL-CRBN compounds)"
date: "2026-09-07"
---

# Phase: Build poses_all.sdf

## Goal

Produce a single consolidated SDF file (`poses_all.sdf`) containing the top 5 gnina docking poses for every compound in the CRBN docking campaign:

- 22 CRBN_ID_enantio_2 stereoisomers (from `best_poses2/*.sdf`, 10 poses per file — top 5 taken)
- 32 EDEL-CRBN compounds (from `poses/*.sdf.gz`, 5 poses per file — all used)

Total: **270 records**.

## Source Files

| Source | Format | Compounds | Poses per compound |
|--------|--------|-----------|-------------------|
| `best_poses2/*.sdf` | Plain SDF, 10 poses each | 22 (Compound_N_entX) | 5 (top 5 of 10) |
| `poses/*.sdf.gz` | Gzipped SDF, 5 poses each | 32 (EDEL-CRBN-XXXX[_ent]) | 5 (all) |

## SD Tags in Output

### 22-compound set (CRBN_ID_enantio_2)

All original biological SD tags preserved from source SDF:
`Molecule Name`, `EC50 (µM) (Excel)`, `Error (µM)`, `HTRC CRBN-DDB1 EC50 (µM)`, `EC50 fitting (µM)`, `Modèle Fitting`, `Parent_Compound`, `MMFF94s_energy_kcalmol`

Per-pose gnina scores added from `docking2_results.json`:
`Compound_Name`, `Pose_Rank` (1–5), `Docking_Affinity_kcal_mol`, `CNN_Affinity`, `CNN_Pose_Score`

### 32-compound set (EDEL-CRBN)

All original gnina SD tags preserved:
`ID`, `Stereoisomer`, `MW`, `HBD`, `HBA`, `RotBonds`, `cLogP`, `minimizedAffinity`, `CNNscore`, `CNNaffinity`, `CNN_VS`, `CNNaffinity_variance`

Added: `Compound_Name`, `Pose_Rank` (1–5)

## Implementation

**Script:** `build_poses_all.py`

SDF records are parsed and written as **raw text** (splitting on `$$$$` delimiters, injecting new SD tag lines after the existing property block). No RDKit mol loading or re-writing is performed. This preserves the original 3D mol block geometry exactly and avoids the gnina `$$$$` contamination bug (where gnina embeds an extra `$$$$` terminator inside property blocks, causing RDKit SDWriter to split each record into two).

Compound names for the 32-compound set are derived from the `.sdf.gz` filename by stripping the `_poses.sdf.gz` suffix (longest suffix matched first to prevent partial stripping to the shorter `.sdf.gz` alone).

## Output

| File | Size | Records | $$$$ separators |
|------|------|---------|----------------|
| `poses_all.sdf` | 739 KB (756,429 bytes) | 270 | 270 ✓ |

## Bugs Fixed During Build

Two SDF formatting bugs were found and fixed after observing molfile parsing errors in downstream viewers:

**Bug 1 — gnina `$$$$` contamination in `best_poses2/` source files:**  
gnina writes a `$$$$` inside the property block between biological tags and its own score tags, then a real `$$$$` at the end of each record. The original `split_sdf` function treated both as record terminators, producing alternating good (mol block + bio tags) and bad (gnina scores, no mol block) fragments. Downstream viewers saw some records with no mol block.  
Fix: after splitting on `$$$$`, any fragment that contains no `M  END` is a contamination artifact and is merged back into the preceding record with `"\n\n"` as separator.

**Bug 2 — missing blank line before `$$$$` record terminator:**  
SDF spec requires a blank line between the last property value and `$$$$`. Without it, RDKit reads `$$$$` and the next record's header as a multi-line continuation of the last property value — silently consuming one record per compound (269 loaded instead of 270). The `Pose_Rank` for affected records contained `5\n$$$$\nEDEL-CRBN-0016` as a 3-line value.  
Fix: terminate each injected tag block with `"\n$$$$\n"` instead of `"$$$$\n"`.

## Verification

Checks run programmatically (2026-09-07) after final script execution:

| Check | Expected | Observed | Pass |
|-------|----------|----------|------|
| Total records in `poses_all.sdf` | 270 (22×5 + 32×5) | 270 | ✓ |
| `$$$$` separators in output file | 270 | 270 | ✓ |
| RDKit SDMolSupplier valid records | 270 | 270 | ✓ |
| RDKit None (corrupt) records | 0 | 0 | ✓ |
| Distinct `Compound_Name` values | 54 | 54 | ✓ |
| Records missing `Compound_Name` or `Pose_Rank` | 0 | 0 | ✓ |
| All compounds have exactly ranks 1–5 | all 54 | all 54 | ✓ |
| Any `Compound_Name` with trailing `_poses` | 0 | 0 | ✓ |
| File size | >900 KB | 907,947 bytes | ✓ |

## GitHub

Committed to `RSA-Edelris/RaycaBio` at commit `8a081f5`:
- `AgenticAIDD_CRBN-Edelris-Docking-MMGBSA/results/poses_all.sdf`
- `AgenticAIDD_CRBN-Edelris-Docking-MMGBSA/scripts/build_poses_all.py`
