
## Phase Identity

**Phase:** Export merged SDF files and push to GitHub  
**Input:** 30 docked poses in `all_poses/`, 6 MM-GBSA JSON files, `gnina_docked.sdf.gz`  
**Output:** `docking_PDK1.sdf` (30 records), `MD_PDK1.sdf` (6 records), GitHub push  
**Status:** Completed successfully  
**Date:** 2026-09-07

---

## What Was Done

### Step 1 — Rebuild pose and GBSA tables
- Re-parsed `gnina_docked.sdf.gz` with longest-first ligand name matching to correctly assign all 30 poses
- Loaded all 6 `gbsa_{LIG}.json` files; merged MM-GBSA ΔG (TOTAL) and energy components per pose
- Selected best pose per ligand by lowest MM-GBSA ΔG (EM-refined selection):
  - EL2003A-A2U1: pose 2, ΔG = −61.665 kcal/mol
  - EL2003A: pose 2, ΔG = −61.835 kcal/mol
  - EL2003A-A4U1: pose 1, ΔG = −64.741 kcal/mol
  - BX912: pose 2, ΔG = −60.328 kcal/mol
  - EL5001A: pose 1, ΔG = −54.420 kcal/mol
  - EL5003A: pose 3, ΔG = −57.187 kcal/mol

### Step 2 — Build `docking_PDK1.sdf`
- Merged all 30 docked poses sorted by ligand order then rank
- Each record annotated with 11 SDF properties: `Molecule_Name`, `Pose_Rank`, `pIC50_PDK1`, `GNINA_Affinity_kcal_mol`, `CNN_Score`, `CNN_Affinity`, `MMGBSA_dG_kcal_mol`, `MMGBSA_VdW`, `MMGBSA_Elec`, `MMGBSA_PolarSolv`, `MMGBSA_NonPolarSolv`
- Verified: 30 `$$$$` terminators; file size 100,603 bytes

### Step 3 — Build `MD_PDK1.sdf`
- Note: the GBSA dispatch used `mode="em"` (GROMACS energy minimisation), not full MD. The GBSA container did not return refined coordinate files; `MD_PDK1.sdf` therefore contains the original GNINA docked pose for each best-GBSA-ranked compound, annotated with the EM-derived energy scores. These are the poses that were submitted to and scored by the EM/GBSA pipeline.
- 6 records (one per ligand), same property annotations as `docking_PDK1.sdf`
- Verified: 6 `$$$$` terminators; file size 20,121 bytes

### Step 4 — GitHub push
- Checked `RSA-Edelris/RaycaBio` exists and is writable (confirmed, default branch: `main`)
- Pushed all workspace files via `push_to_github`
- Commit: `ee6dd4aad03ac19f1d79454c55b16471f7b2528a`
- URL: https://github.com/RSA-Edelris/RaycaBio/tree/main/studies/7a39e116-e0d5-4e70-93c3-da6df54e7e1e/runs/max-96504792c8
- Files committed: 465

---

## Files Produced

| File | Type | Size | Records | Description |
|:-----|:----:|-----:|:-------:|:-----------|
| `docking_PDK1.sdf` | molecules | 100,603 B | 30 | All docked poses with GNINA + MM-GBSA annotations |
| `MD_PDK1.sdf` | molecules | 20,121 B | 6 | Best EM-selected pose per ligand with full score annotations |

---

## Audit Notes

- GBSA container (`mode="em"`) does not return refined coordinates; `MD_PDK1.sdf` uses original GNINA coordinates for the GBSA-best pose — this is documented as a known limitation
- All 30 pose records verified by `$$$$` count before push
- No credential exposure; push accepted without warnings
