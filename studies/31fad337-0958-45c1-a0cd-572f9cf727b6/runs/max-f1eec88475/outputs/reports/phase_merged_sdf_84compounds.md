---
title: "Merged Results SDF — 84 CDK2-CyclinE1 Compounds (Docking + MM-GBSA)"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
phase_goal: "Produce a single SDF file containing all 84 docked poses annotated with docking scores and MM-GBSA binding free energies"
status: "complete"
date: "2026-09-06"
model: "claude-sonnet-4-6"
---

# Merged Results SDF — 84 CDK2-CyclinE1 Compounds (Docking + MM-GBSA)

## Summary

A single annotated SDF file was produced combining the best docked pose for each of the 84 CDK2-CyclinE1 compounds with their docking scores (gnina CNN-rescored Vina) and MM-GBSA binding free energies (Uni-GBSA, single-point). All 84 compounds are present; records are ordered by MM-GBSA rank (most favourable first).

- **Output file:** `cdk2_campaign/CDK2_CyclinE1_84compounds_docking_mmgbsa.sdf`
- **File size:** 374.8 KB
- **Compounds:** 84 / 84 (100%)
- **Best compound:** CTX-1020732 (MM-GBSA rank 1, ΔG = −83.188 kcal/mol, CNN pKi = 8.931)

---

## Objective

Consolidate the docked pose geometry, gnina docking scores, and Uni-GBSA MM-GBSA energy decomposition for all 84 campaign compounds into a single, machine-readable SDF that can be loaded directly into molecular visualisation or cheminformatics tools.

---

## Methods

### Source data

| Source file | Content |
|:---|:---|
| `cdk2_campaign/poses_all/{name}_best_pose.sdf` | Best docked pose (heavy atoms, gnina output) for each of the 84 compounds |
| `cdk2_campaign/docking_results.json` | Docking scores for 84 compounds (Vina affinity, CNN pKi, CNN pose score) |
| `cdk2_campaign/CTX-1020667_docking_result.json` | Re-docked values for CTX-1020667 (patched over the original batch entry — see note) |
| `cdk2_campaign/mmgbsa_results.json` | MM-GBSA ΔG and energy decomposition for all 84 compounds, sorted ascending by ΔG |

**Note on CTX-1020667:** The original batch docking run produced a null per-pose CNN score for this compound. It was re-docked independently on 2026-09-06 using gnina with the correct `proteinFile` field. The re-docked values (Vina −8.21 kcal/mol, CNN pKi 7.271, pose score 0.4097) were used in the merged SDF; the original batch entry (Vina −9.39, CNN 6.760) was discarded.

### SDF construction

Script: `cdk2_campaign/build_results_sdf.py` (RDKit 2024.x)

1. Both source tables were loaded into keyed dicts (`name` → record for docking; `ligandName` → record for MM-GBSA).
2. CTX-1020667's docking row was patched with values from `CTX-1020667_docking_result.json`.
3. Docking rank was computed by sorting all 84 compounds by CNN pKi descending (patched values used).
4. MM-GBSA rank was taken from the position in the pre-sorted `mmgbsa_results.json` list (rank 1 = most negative ΔG).
5. Records were written in MM-GBSA rank order; each SD molecule was read from `poses_all/{name}_best_pose.sdf` and annotated with the properties listed below.

### SD properties written per record

| Property name | Units | Source |
|:---|:---|:---|
| `Docking_Rank` | — | Rank by CNN pKi descending |
| `Vina_Affinity_kcal_mol` | kcal/mol | gnina Vina score |
| `CNN_pKi` | log units | gnina CNN-predicted pKi |
| `CNN_Pose_Score` | 0–1 | gnina CNN pose confidence |
| `Num_Docked_Poses` | — | Number of gnina poses generated |
| `MMGBSA_Rank` | — | Rank by MM-GBSA ΔG (1 = most favourable) |
| `MMGBSA_dG_kcal_mol` | kcal/mol | Total MM-GBSA binding free energy |
| `MMGBSA_VdW_kcal_mol` | kcal/mol | Van der Waals component |
| `MMGBSA_Elec_kcal_mol` | kcal/mol | Electrostatic component |
| `MMGBSA_PolarSolv_kcal_mol` | kcal/mol | Polar (GB) solvation component |
| `MMGBSA_NonPolarSolv_kcal_mol` | kcal/mol | Non-polar (SA) solvation component |
| `MMGBSA_Status` | — | "S" = success for all 84 |

Original SDF properties from the gnina output (SMILES, pIC50, batch metadata, minimizedAffinity, CNNscore, CNNaffinity) are also retained in the records.

---

## Results

### Key statistics

| Metric | Value |
|:---|---:|
| Compounds in SDF | 84 |
| MM-GBSA rank 1 | CTX-1020732 (ΔG = −83.188 kcal/mol) |
| MM-GBSA rank 84 | CTX-1020739 (ΔG = −24.691 kcal/mol) |
| Docking rank 1 (CNN pKi) | CTX-1020732 (CNN pKi = 8.931) |
| Co-crystal reference CTX-1017233 | MM-GBSA rank 51 (ΔG = −49.925 kcal/mol), docking rank 45 |
| CTX-1020667 (re-docked) | MM-GBSA rank 70 (ΔG = −41.491 kcal/mol), docking rank 36 |

### Top 10 by MM-GBSA rank

| MM-GBSA Rank | Compound | ΔG (kcal/mol) | CNN pKi | Docking Rank |
|:---:|:---|---:|---:|:---:|
| 1 | CTX-1020732 | −83.188 | 8.931 | 1 |
| 2 | CTX-1020811 | −80.272 | 8.586 | 3 |
| 3 | CTX-1020521 | −80.075 | 8.233 | 6 |
| 4 | CTX-1020903 | −79.956 | 8.586 | 2 |
| 5 | CTX-1020743 | −78.495 | 8.575 | 4 |
| 6 | CTX-1020748 | −77.689 | 7.614 | 20 |
| 7 | CTX-1020555 | −76.526 | 7.700 | 17 |
| 8 | CTX-1019757 | −75.475 | 8.416 | 7 |
| 9 | CTX-1020759 | −75.200 | 7.598 | 22 |
| 10 | CTX-1020800 | −74.601 | 7.680 | 16 |

---

## Output Artifacts

| File | Description |
|:---|:---|
| `cdk2_campaign/CDK2_CyclinE1_84compounds_docking_mmgbsa.sdf` | Merged SDF, 84 compounds, MM-GBSA rank order, all docking + MM-GBSA properties |
| `cdk2_campaign/build_results_sdf.py` | Build script (RDKit) |

---

## Verification

The following claims were checked against the output SDF and source files after generation:

| Claim | Source | Verified value | Result |
|:---|:---|:---|:---:|
| SDF contains 84 records | SDMolSupplier read on output SDF | 84 non-null molecules | CONFIRMED |
| CTX-1020732: MM-GBSA rank 1, ΔG = −83.188 kcal/mol | output SDF SD properties | MMGBSA_Rank=1, MMGBSA_dG_kcal_mol=−83.188 | CONFIRMED |
| CTX-1020732: CNN pKi = 8.931, docking rank 1 | output SDF SD properties | CNN_pKi=8.931, Docking_Rank=1 | CONFIRMED |
| CTX-1020667: MM-GBSA rank 70, ΔG = −41.491 kcal/mol | output SDF SD properties | MMGBSA_Rank=70, MMGBSA_dG_kcal_mol=−41.491 | CONFIRMED |
| CTX-1020667: uses re-docked Vina −8.21, CNN pKi 7.271, docking rank 36 | output SDF SD properties | Vina_Affinity_kcal_mol=−8.210, CNN_pKi=7.271, Docking_Rank=36 | CONFIRMED |
| Records ordered by MM-GBSA rank (rank 1 first) | position of CTX-1020732 in SDF | first record | CONFIRMED |
| All 84 MMGBSA_Status values = "S" | sdmolsupplier enumeration | 84 × "S" | CONFIRMED |
