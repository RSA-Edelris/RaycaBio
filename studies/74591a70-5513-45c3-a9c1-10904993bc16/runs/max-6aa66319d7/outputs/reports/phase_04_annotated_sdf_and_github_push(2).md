---
title: "Phase 4: Create annotated SDF and push session to GitHub"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-5c6f9d06e5"
phase_index: 4
phase_goal: "Build annotated SDF with docking + MM-GBSA properties and push all session outputs to RSA-Edelris/RaycaBio"
status: "complete"
model: "claude-sonnet-4-6"
generator: "human post-hoc"
---

# Phase 4: Create annotated SDF and push session to GitHub

## Summary

An annotated multi-compound SDF file was built from the 32 best-pose SDF files,
enriched with gnina docking scores and MM-GBSA binding energies as SD properties.
All key session outputs were pushed to the GitHub repository
RSA-Edelris/RaycaBio under the folder
`AgenticAIDD_CRBN-Edelris-Docking-MMGBSA/`.

---

## Procedure

### Step 1 — Annotated SDF construction

For each of the 32 compounds (ordered by MM-GBSA rank), the best-pose SDF from
`best_poses/{name}_pose1.sdf` was read, stripped of its terminal `$$$$`, and
annotated with the following SD properties:

| Property tag | Source | Units |
|---|---|---|
| `Compound_ID` | compound name | — |
| `Vina_dG_kcal_mol` | `docking_scores_all32.json` → `affinity` | kcal/mol |
| `CNN_pKd` | `docking_scores_all32.json` → `cnn_affinity` | pKd units |
| `GBSA_dG_kcal_mol` | `mmgbsa_results.json` → `DELTA TOTAL` | kcal/mol |
| `GBSA_dG_std` | `mmgbsa_results.json` → `DELTA TOTAL_std` | kcal/mol |
| `GBSA_VDWAALS` | `mmgbsa_results.json` → `VDWAALS` | kcal/mol |
| `GBSA_EEL` | `mmgbsa_results.json` → `EEL` | kcal/mol |
| `GBSA_EGB` | `mmgbsa_results.json` → `EGB` | kcal/mol |
| `GBSA_ESURF` | `mmgbsa_results.json` → `ESURF` | kcal/mol |
| `GBSA_rank` | position in MM-GBSA-sorted list | integer |

Output: `CRBN_32_ligands_docking_GBSA.sdf` (119.6 KB, 32 compounds, V2000 format).
All 32 compounds present; no missing pose files.

### Step 2 — GitHub push

The Rayca `push_to_github` MCP tool timed out. Push was performed via direct git
clone + commit + push using the project token:

```
Repository : RSA-Edelris/RaycaBio (public, branch: main)
Folder     : AgenticAIDD_CRBN-Edelris-Docking-MMGBSA/
Commit SHA : 15febb9
```

Files pushed:

| Path in repo | Description |
|---|---|
| `results/CRBN_32_ligands_docking_GBSA.sdf` | 32-compound annotated SDF |
| `results/combined_results.json` | Ranked docking + MM-GBSA table |
| `results/mmgbsa_results.json` | Raw MM-GBSA components |
| `results/docking_scores_all32.json` | Raw gnina docking scores |
| `report.md` | Full study report |
| `scripts/pipeline.py` | Topology preparation script |
| `scripts/run_mmpbsa.py` | MMPBSA.py execution script |
| `scripts/collate_results.py` | Collation script |
| `reports/` | 4 phase and audit documents |

---

## Output artifacts

| File | Size | Description |
|---|---|---|
| `CRBN_32_ligands_docking_GBSA.sdf` | 119.6 KB | 32-compound annotated SDF (primary deliverable) |
| `source/101_open.py` | 1.8 KB | Script that built the SDF from `combined_results.json` + `best_poses/` |

**`CRBN_32_ligands_docking_GBSA.sdf`** — the primary deliverable.  
Contains 3D coordinates from gnina best pose + 10 SD property fields per compound.
Sorted by MM-GBSA GBSA_rank (rank 1 = EDEL-CRBN-0009_ent, GBSA ΔG = −44.75 kcal/mol).
Suitable for direct import into molecular visualisation tools (PyMOL, Maestro, LigandScout).

**`source/101_open.py`** — the SDF builder script.  
Reads `mmgbsa/combined_results.json` (ranked list), iterates in GBSA order, appends
`best_poses/{name}_pose1.sdf` mol block for each compound, attaches 10 SD property
tags (Compound_ID, Vina_dG_kcal_mol, CNN_pKd, GBSA_dG_kcal_mol, GBSA_dG_std,
GBSA_VDWAALS, GBSA_EEL, GBSA_EGB, GBSA_ESURF, GBSA_rank), and writes the merged file.

---

## Verification

| Check | Result |
|---|---|
| SDF compound count (`$$$$` occurrences) | 32 / 32 |
| All 10 SD property tags present in all 32 records | 320 / 320 occurrences |
| GBSA_rank runs 1–32 without gaps | PASS |
| First record is rank 1 (EDEL-CRBN-0009_ent, ΔG = −44.75 kcal/mol) | PASS |
| Last record is rank 32 (EDEL-CRBN-0010, ΔG = −21.33 kcal/mol) | PASS |
| All GBSA_dG values negative | PASS (−44.75 to −21.33 kcal/mol) |
| Vina_dG range plausible for CRBN pocket | PASS (−10.21 to −5.20 kcal/mol) |
| CNN_pKd range plausible | PASS (4.51 to 7.59) |
| SHA-256 | `51b07a71be7076dd91fddbadfcb527f59181c81b415fc35d550642cafedb56ab` |
| GitHub commit present | 15febb9 on RSA-Edelris/RaycaBio main |
| No missing pose files | PASS — `101_open.py` reported 32/32, missing=[] |
