---
title: "Phase 1: MM-GBSA binding free energies for 83 CDK2-CyclinE1 compounds"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-7a31d87c13"
phase_index: 1
phase_id: "1"
phase_goal: "MM-GBSA binding free energies for 83 CDK2-CyclinE1 compounds"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: MM-GBSA binding free energies for 83 CDK2-CyclinE1 compounds

## Summary

This phase set out to mM-GBSA binding free energies for 83 CDK2-CyclinE1 compounds. It completed 1 method step, 476 output files.

## Objective

MM-GBSA binding free energies for 83 CDK2-CyclinE1 compounds

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

**Table R.** Key resources used in this phase. Versions are as reported by the running environment; identifiers follow the FORCE11 software citation principles.

| Resource | Type | Version | Identifier | Source |
| :--- | :--- | :--- | :--- | :--- |
| GNINA | software | not recorded | doi:10.1186/s13321-021-00522-2 | https://github.com/gnina/gnina |
| Rayca Modulon | platform | not recorded | this platform | not recorded |

### Procedure

#### 1. Receptor preparation for GROMACS/MM-GBSA

The CDK2-CyclinE1 receptor (`receptor_raw.pdb`, chains A+B) was incompatible with GROMACS pdb2gmx: chain A residue numbering started at 0 and chain B had a 7-residue structural gap (ASN 245 → PRO 253). MDAnalysis was used to renumber both chains from residue 1, producing `receptor_gromacs_ready.pdb` (chain A: 299 residues 1–299, chain B: 267 residues 1–267). All 83 MM-GBSA calculations used this file as the protein input.

| Field | Value |
| :--- | :--- |
| Inputs | receptor_raw.pdb |
| Outputs | receptor_gromacs_ready.pdb |
| Tools | MDAnalysis 2.10.0 |
| Status | complete |

#### 2. Ligand hydrogen addition

Gnina docked-pose SDF files contain only 1 explicit hydrogen per ligand. GAFF2/antechamber requires explicit hydrogens for atom typing and AM1-BCC charge assignment. RDKit `Chem.AddHs(mol, addCoords=True)` was applied to all 83 best-pose SDF files, preserving 3D coordinates. Output: `poses_all_H/{name}_best_pose_H.sdf`.

| Field | Value |
| :--- | :--- |
| Inputs | 83 × `poses_all/{name}_best_pose.sdf` (gnina output) |
| Outputs | 83 × `poses_all_H/{name}_best_pose_H.sdf` |
| Tools | RDKit 2024.x |
| Script | `add_explicit_h.py` |
| Status | complete |

#### 3. MM-GBSA single-point binding free energy calculations

Single-point MM-GBSA binding free energies (ΔG_bind = E_complex − E_receptor − E_ligand) were computed for all 83 H-added best-pose ligands using the Uni-GBSA containerised tool (GROMACS + gmx_MMPBSA, GAFF2, AM1-BCC). Each call: energy minimisation (mode=em), Generalised Born implicit solvent (method=gb), amber99sb-ildn protein force field, GAFF2 ligand force field, AM1-BCC partial charges, 4 CPU threads, A100 GPU (GROMACS mdrun -nb gpu). ~75 s per ligand.

Execution was parallelised across 9 Python daemon threads in a single `run_python` call (total wall time ~870 s for 73 ligands), seeded with 10 ligands computed earlier (batch_00). Four ligands (1 timeout + 3 transient failures under parallel load) were re-run sequentially in a follow-up call (~303 s).

| Field | Value |
| :--- | :--- |
| Inputs | `receptor_gromacs_ready.pdb`, 83 × `poses_all_H/{name}_best_pose_H.sdf` |
| Outputs | `mmgbsa_results.json`, 9 × `gbsa_thread_XX.json`, `gbsa_batch_results_00.json` |
| Tools | Uni-GBSA (GROMACS 2024, gmx_MMPBSA, GAFF2, antechamber/acpype) |
| Container | `registry.rayca.org/rayca-tools/gbsa:latest` |
| Script | `run_mmgbsa_threaded.py` |
| Status | complete |

Parameters (per ligand):

```yaml
task: protein-ligand
mode: em
method: gb
proteinForceField: amber99sb-ildn
ligandForceField: gaff2
ligandCharge: bcc
threads: 4
gpu: true (A100 80 GB)
```

## Results

MM-GBSA single-point binding free energies were calculated for all 83 scoreable CDK2-CyclinE1 ligands in this phase (CTX-1020667 excluded: null per-pose CNN score in the original batch docking run). All 83 calculations completed with status "S" (success); 0 failures.

**Addendum (2026-09-06):** CTX-1020667 was subsequently re-docked independently (same gnina box/parameters) and MM-GBSA was computed for its best pose (ΔG = −41.491 kcal/mol, rank 70/84). The merged 84-compound results are in `cdk2_campaign/mmgbsa_results.json`; individual result: `cdk2_campaign/CTX-1020667_mmgbsa_result.json`.

**Key results:**

| Metric | Value |
| :--- | :--- |
| Compounds scored | 83 / 83 |
| Best compound | CTX-1020732 (ΔG = −83.188 kcal/mol) |
| Worst compound | CTX-1020739 (ΔG = −24.691 kcal/mol) |
| Mean ΔG | −55.199 kcal/mol |
| Median ΔG | −54.234 kcal/mol |
| SD | 15.769 kcal/mol |
| Co-crystal ref CTX-1017233 | Rank 51, ΔG = −49.925 kcal/mol |

**Top 10 compounds by MM-GBSA ΔG:**

| Rank | Compound | ΔG (kcal/mol) | VdW | Electrostatic |
| :---: | :--- | ---: | ---: | ---: |
| 1 | CTX-1020732 | −83.188 | −79.340 | −4.815 |
| 2 | CTX-1020811 | −80.272 | −77.798 | −4.040 |
| 3 | CTX-1020521 | −80.075 | −79.361 | −2.617 |
| 4 | CTX-1020903 | −79.956 | −78.319 | −3.001 |
| 5 | CTX-1020743 | −78.495 | −75.425 | −2.929 |
| 6 | CTX-1020748 | −77.689 | −74.693 | −8.823 |
| 7 | CTX-1020555 | −76.526 | −74.586 | −4.481 |
| 8 | CTX-1019757 | −75.475 | −71.392 | −4.367 |
| 9 | CTX-1020759 | −75.200 | −75.055 | −3.850 |
| 10 | CTX-1020800 | −74.601 | −72.741 | −7.069 |

The dominant energy term across the series is van der Waals burial (mean −54.671 kcal/mol), consistent with the primarily hydrophobic CDK2 ATP-binding pocket pharmacophore. CTX-1020732 is ranked #1 by both gnina CNN-rescored Vina affinity and MM-GBSA. Notable re-rankings: CTX-1020748 (docking rank 20 → MM-GBSA rank 6) and CTX-1020759 (docking rank 22 → MM-GBSA rank 9).

Full results: `cdk2_campaign/mmgbsa_results.json` (84 entries including CTX-1020667 addendum, sorted ascending by ΔG).

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| gbsa_batch_results_00.json | JSON | 3.7 KB | work | 66903d829d68... |
| run_mmgbsa_threaded.py | PY | 4.5 KB | source | 27e1f557dd71... |
| BindingEnergy.csv | CSV | 391 B | tables | f275db31e362... |
| CTX-1017233_best_pose_H.mol | MOL | 6.7 KB | structures | 3751016ed0d4... |
| Energy.csv | CSV | 353 B | tables | 2537c8f6e568... |
| complex.pdb | PDB | 718.1 KB | structures | e463a45b4509... |
| complex.top | TOP | 4.6 MB | work | d43a70d484a2... |
| complex_reres.pdb | PDB | 718.1 KB | structures | fd51edfee75b... |
| CTX-1019471_best_pose_H.mol | MOL | 5.0 KB | structures | ce1637eaec7d... |
| Energy.csv | CSV | 342 B | tables | 27687f73f5e3... |
| complex.pdb | PDB | 716.7 KB | structures | c4780814e983... |
| complex.top | TOP | 4.6 MB | work | 27b039a5d342... |
| complex_reres.pdb | PDB | 716.7 KB | structures | dc393b336a38... |
| CTX-1019473_best_pose_H.mol | MOL | 5.8 KB | structures | da44f5edeed3... |
| Energy.csv | CSV | 344 B | tables | 5e07bfcba16e... |
| complex.pdb | PDB | 717.4 KB | structures | 32fda2453a11... |
| complex.top | TOP | 4.6 MB | work | f3f9b64a6fb2... |
| complex_reres.pdb | PDB | 717.4 KB | structures | 0d5ea1d1e361... |
| CTX-1019480_best_pose_H.mol | MOL | 5.1 KB | structures | 2d6df7896653... |
| Energy.csv | CSV | 343 B | tables | 3b3693164be1... |
| complex.pdb | PDB | 716.8 KB | structures | fe17a0a91cbf... |
| complex.top | TOP | 4.6 MB | work | d6b97b7fb52d... |
| complex_reres.pdb | PDB | 716.8 KB | structures | 403f93ccece0... |
| CTX-1019496_best_pose_H.mol | MOL | 4.7 KB | structures | c5810cec2e6a... |
| Energy.csv | CSV | 340 B | tables | ca0cf33fbc11... |
| complex.pdb | PDB | 716.5 KB | structures | edf9e7c96cef... |
| complex.top | TOP | 4.6 MB | work | a18ce6fba5f6... |
| complex_reres.pdb | PDB | 716.5 KB | structures | 4baff9a012f8... |
| CTX-1019613_best_pose_H.mol | MOL | 6.7 KB | structures | 1406c8bd3b9c... |
| Energy.csv | CSV | 343 B | tables | d8b220bea9ea... |
| complex.pdb | PDB | 718.1 KB | structures | 5ff684ce3b85... |
| complex.top | TOP | 4.6 MB | work | 523f104f9b34... |
| complex_reres.pdb | PDB | 718.1 KB | structures | 57212240f663... |
| CTX-1019630_best_pose_H.mol | MOL | 6.2 KB | structures | 6c732da33b0e... |
| Energy.csv | CSV | 341 B | tables | 42c4bc7bc7ff... |
| complex.pdb | PDB | 717.7 KB | structures | 6ba9981e65ee... |
| complex.top | TOP | 4.6 MB | work | 21568747392e... |
| complex_reres.pdb | PDB | 717.7 KB | structures | 8a89c029a5c2... |
| CTX-1019660_best_pose_H.mol | MOL | 6.3 KB | structures | 4d0bc9b275aa... |
| Energy.csv | CSV | 348 B | tables | ba62e4166589... |
| complex.pdb | PDB | 717.8 KB | structures | d5322c595db6... |
| complex.top | TOP | 4.6 MB | work | 571ec427076f... |
| complex_reres.pdb | PDB | 717.8 KB | structures | 2db4baf43b82... |
| CTX-1019757_best_pose_H.mol | MOL | 6.7 KB | structures | a552d958ded0... |
| Energy.csv | CSV | 342 B | tables | b9be3c354deb... |
| complex.pdb | PDB | 718.2 KB | structures | ada147b50358... |
| complex.top | TOP | 4.6 MB | work | 2ef8b4487dc8... |
| complex_reres.pdb | PDB | 718.2 KB | structures | d36f9965be36... |
| CTX-1019758_best_pose_H.mol | MOL | 6.5 KB | structures | 2e0d516c9e09... |
| Energy.csv | CSV | 347 B | tables | b2eba34c42c2... |
| complex.pdb | PDB | 717.9 KB | structures | 8905b7b609b8... |
| complex.top | TOP | 4.6 MB | work | a25394a77bec... |
| complex_reres.pdb | PDB | 717.9 KB | structures | e59a66e4aa09... |
| gbsa_thread_00.json | JSON | 3.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 2c8e444646bd... |
| gbsa_thread_01.json | JSON | 3.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 119525bd288e... |
| gbsa_thread_02.json | JSON | 2.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 45860887bd71... |
| gbsa_thread_03.json | JSON | 3.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | aa85b7812d53... |
| gbsa_thread_04.json | JSON | 3.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 369e6ac7f197... |
| gbsa_thread_05.json | JSON | 3.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | b13a468d297d... |
| gbsa_thread_06.json | JSON | 2.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | d4e974ac005c... |
| gbsa_thread_07.json | JSON | 3.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | c4fd8e7564ca... |
| gbsa_thread_08.json | JSON | 2.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | b5e939e9ffd6... |
| mmgbsa_results.json | JSON | 30.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | f635b164e408... |
| BindingEnergy.csv | CSV | 391 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 592b43e8d33d... |
| CTX-1019813_best_pose_H.mol | MOL | 6.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 066f8134ce64... |
| Energy.csv | CSV | 335 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 584f6183c33c... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | f13217b767f4... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 61a00e14f8c9... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e72832da583c... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ef996cb27652... |
| CTX-1019904_best_pose_H.mol | MOL | 6.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 9c226a1701d1... |
| Energy.csv | CSV | 344 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 758311d40601... |
| complex.pdb | PDB | 718.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | da0396eab20d... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | d48a2025f97c... |
| complex_reres.pdb | PDB | 718.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 36e09e40ea2b... |
| index.ndx | NDX | 296.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 8f0c449e4c6a... |
| CTX-1020440_best_pose_H.mol | MOL | 6.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e0bea94af45e... |
| Energy.csv | CSV | 349 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | f26c977a3766... |
| complex.pdb | PDB | 717.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ab1b52de0641... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 972ffb8dec37... |
| complex_reres.pdb | PDB | 717.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 505593fbc8a0... |
| CTX-1020441_best_pose_H.mol | MOL | 6.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 6b360db5701b... |
| Energy.csv | CSV | 340 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 072751164cee... |
| complex.pdb | PDB | 718.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 9768bdcfa858... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 06dbec654a53... |
| complex_reres.pdb | PDB | 718.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 81ab8207cf78... |
| CTX-1020453_best_pose_H.mol | MOL | 6.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 83a53b602422... |
| Energy.csv | CSV | 343 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 90c130ba4fb0... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c93c9b93ccf4... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | f23e7af9237f... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 0944b9950415... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ef996cb27652... |
| CTX-1020454_best_pose_H.mol | MOL | 6.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 1b7a9a4910e8... |
| Energy.csv | CSV | 342 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 09d0282bffcd... |
| complex.pdb | PDB | 718.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ca54b6d78478... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 0ef71d68ba6a... |
| complex_reres.pdb | PDB | 718.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 000479051e8a... |
| CTX-1020456_best_pose_H.mol | MOL | 6.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 5e68ed6ddd54... |
| Energy.csv | CSV | 345 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 4ff23335cea9... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | bd12ff910c0c... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 7e4cc659b4a0... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e479e7ef7457... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ef996cb27652... |
| CTX-1020458_best_pose_H.mol | MOL | 6.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 945243b5b04c... |
| Energy.csv | CSV | 347 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 8faefff2d4df... |
| complex.pdb | PDB | 718.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 23e98f98914f... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 51505090ddbb... |
| complex_reres.pdb | PDB | 718.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 34b814e256d7... |
| index.ndx | NDX | 296.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 8f0c449e4c6a... |
| CTX-1020516_best_pose_H.mol | MOL | 4.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 804c3e208e6b... |
| Energy.csv | CSV | 347 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 088b809146fd... |
| complex.pdb | PDB | 716.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 7eb842b09412... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 1cfd262d5898... |
| complex_reres.pdb | PDB | 716.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | d0f84fbeead4... |
| index.ndx | NDX | 296.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 68335c8bd48f... |
| CTX-1020517_best_pose_H.mol | MOL | 6.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 84cfc23c787a... |
| Energy.csv | CSV | 339 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | c72197495b40... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ac3ababca00f... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 9560f71fcb80... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 5f3b7bd847a4... |
| CTX-1020518_best_pose_H.mol | MOL | 5.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c8482a842bdf... |
| Energy.csv | CSV | 348 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 6d65d3eed641... |
| complex.pdb | PDB | 717.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 20eec1828016... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | c3f9d2bb1d3a... |
| complex_reres.pdb | PDB | 717.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 4ae99b16b574... |
| index.ndx | NDX | 296.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 35ddd8afa915... |
| CTX-1020520_best_pose_H.mol | MOL | 7.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 4dd1e2076339... |
| Energy.csv | CSV | 337 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | f7c1c98e1288... |
| complex.pdb | PDB | 718.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | d89198b26469... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 8a22a3366f15... |
| complex_reres.pdb | PDB | 718.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 037f2c1a9d62... |
| index.ndx | NDX | 296.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 64561f5031c3... |
| CTX-1020521_best_pose_H.mol | MOL | 7.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c6891525828d... |
| Energy.csv | CSV | 348 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 7a59e8204ffe... |
| complex.pdb | PDB | 718.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | def78a989897... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 15807d68b41e... |
| complex_reres.pdb | PDB | 718.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | a14ca68102b6... |
| index.ndx | NDX | 296.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 6f6ce51e8477... |
| CTX-1020523_best_pose_H.mol | MOL | 6.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | aec2dc924e8a... |
| Energy.csv | CSV | 342 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | bac629ad6031... |
| complex.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 8305e4f2312c... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 8cff6cdce536... |
| complex_reres.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 9ea0164ff80a... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ce232c22736e... |
| CTX-1020555_best_pose_H.mol | MOL | 6.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 61140b475b31... |
| Energy.csv | CSV | 342 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | f31f9d5e1bcb... |
| complex.pdb | PDB | 717.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 9f07046829ff... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | f5ca1f230355... |
| complex_reres.pdb | PDB | 717.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | eafc7c4fe347... |
| CTX-1020562_best_pose_H.mol | MOL | 6.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 6ac07744d620... |
| Energy.csv | CSV | 344 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | c8c3a6d9cc5d... |
| complex.pdb | PDB | 718.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 69dc5348bb28... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | b832a166253f... |
| complex_reres.pdb | PDB | 718.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | abf6f078a8f8... |
| index.ndx | NDX | 296.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 8f0c449e4c6a... |
| CTX-1020565_best_pose_H.mol | MOL | 6.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ddbde9ead0b3... |
| Energy.csv | CSV | 343 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | aa4eb65eb262... |
| complex.pdb | PDB | 717.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | d858ae06bdd3... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | c429d1bd367e... |
| complex_reres.pdb | PDB | 717.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c27eb88382ba... |
| CTX-1020566_best_pose_H.mol | MOL | 5.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 15ff002d4331... |
| Energy.csv | CSV | 344 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | c6aa565fc959... |
| complex.pdb | PDB | 716.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 14947cb739f1... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 499dac24f35c... |
| complex_reres.pdb | PDB | 716.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | b55ba9cbced2... |
| index.ndx | NDX | 296.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 95a80cd9a699... |
| CTX-1020582_best_pose_H.mol | MOL | 6.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 37baff7e2228... |
| Energy.csv | CSV | 342 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 1f807920c3b0... |
| complex.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 59da3c6e3922... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | cf0066c8110d... |
| complex_reres.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | d7550be465b2... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ce232c22736e... |
| CTX-1020669_best_pose_H.mol | MOL | 6.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 1de1b3eef96e... |
| Energy.csv | CSV | 339 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 598c2310dfab... |
| complex.pdb | PDB | 717.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 07bf3bb8d6bd... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 1b602af01089... |
| complex_reres.pdb | PDB | 717.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 28a2a446ce77... |
| CTX-1020670_best_pose_H.mol | MOL | 4.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | cabdc2a75955... |
| Energy.csv | CSV | 339 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 42a2be0e3550... |
| complex.pdb | PDB | 716.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 6d08e18afb0b... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 33c451b0456f... |
| complex_reres.pdb | PDB | 716.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 887ad42955c5... |
| index.ndx | NDX | 296.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 00b5c277f5d9... |
| CTX-1020671_best_pose_H.mol | MOL | 4.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 207ef519ccca... |
| Energy.csv | CSV | 338 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | be66dca6ab55... |
| complex.pdb | PDB | 716.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 299b351373a1... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 3401295e602e... |
| complex_reres.pdb | PDB | 716.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ecd7bd9859aa... |
| index.ndx | NDX | 296.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 4751fd02695f... |
| CTX-1020685_best_pose_H.mol | MOL | 6.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | de2820b9a47c... |
| Energy.csv | CSV | 327 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 22c7486d634d... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 3820e849860f... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 63891ddf9976... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 5d10458b98ff... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ef996cb27652... |
| CTX-1020696_best_pose_H.mol | MOL | 6.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 9fbd3e883c5c... |
| Energy.csv | CSV | 341 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | eeb51d3e1349... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 918e40bfe705... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | da7c5f727eb0... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 6a495fdaa6f0... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ef996cb27652... |
| CTX-1020697_best_pose_H.mol | MOL | 6.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ba6a3c1d17ef... |
| Energy.csv | CSV | 343 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | c70cf8a96ac4... |
| complex.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 052d98999503... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 5c7eb8249ba6... |
| complex_reres.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 28eff49b3ef7... |
| CTX-1020698_best_pose_H.mol | MOL | 5.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ffbefba9daaf... |
| Energy.csv | CSV | 340 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 4eef1c199a83... |
| complex.pdb | PDB | 717.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 08f21cf741d6... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 6533fe41b5de... |
| complex_reres.pdb | PDB | 717.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 35d5135aa150... |
| index.ndx | NDX | 296.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | fadd40409df6... |
| CTX-1020699_best_pose_H.mol | MOL | 5.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 510b45d62d42... |
| Energy.csv | CSV | 340 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | cad613680c59... |
| complex.pdb | PDB | 717.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | a48d9f28787f... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 784ab93722de... |
| complex_reres.pdb | PDB | 717.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 5ddef2fa549b... |
| index.ndx | NDX | 296.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | f03fb33f63e8... |
| CTX-1020726_best_pose_H.mol | MOL | 5.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | be544a1130f6... |
| Energy.csv | CSV | 339 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 3dc6199221df... |
| complex.pdb | PDB | 716.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 05589206391f... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | b94188cc748f... |
| complex_reres.pdb | PDB | 716.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 060d2b85c7fe... |
| CTX-1020732_best_pose_H.mol | MOL | 6.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | f352ea72219b... |
| Energy.csv | CSV | 335 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | edd9390c5e3e... |
| complex.pdb | PDB | 717.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e544d52019ce... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 7dd5e2e631d0... |
| complex_reres.pdb | PDB | 717.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ff754267165d... |
| CTX-1020733_best_pose_H.mol | MOL | 4.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | b614fcbae220... |
| Energy.csv | CSV | 336 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | f1ecd113de3c... |
| complex.pdb | PDB | 716.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 9af6caf095ab... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 36685178f361... |
| complex_reres.pdb | PDB | 716.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | d9c5ca2add67... |
| index.ndx | NDX | 296.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 4751fd02695f... |
| CTX-1020734_best_pose_H.mol | MOL | 6.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 3eef36ba7eb6... |
| Energy.csv | CSV | 346 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 1a3e8cb7fa9f... |
| complex.pdb | PDB | 717.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 9f4059333245... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 0a31a7a18b3b... |
| complex_reres.pdb | PDB | 717.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e71e63497579... |
| index.ndx | NDX | 296.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | fadd40409df6... |
| CTX-1020735_best_pose_H.mol | MOL | 6.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 02ee17e7fae7... |
| Energy.csv | CSV | 340 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 4d348ab290fc... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | fb37a735fa7a... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | a51f5193fa03... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 2e999f4860d1... |
| CTX-1020739_best_pose_H.mol | MOL | 4.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e5682c7ea0c5... |
| Energy.csv | CSV | 340 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 00217c06c25a... |
| complex.pdb | PDB | 716.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 28977785ab28... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 42311e5c6662... |
| complex_reres.pdb | PDB | 716.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 36fa3a7a5022... |
| index.ndx | NDX | 296.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 43a7febea3f4... |
| CTX-1020740_best_pose_H.mol | MOL | 5.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e0b61e94264b... |
| Energy.csv | CSV | 342 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | b95028cef466... |
| complex.pdb | PDB | 716.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 67a95a20eda8... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 1f409b7a69a0... |
| complex_reres.pdb | PDB | 716.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | cc9fd8c2fdea... |
| index.ndx | NDX | 296.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 95a80cd9a699... |
| CTX-1020741_best_pose_H.mol | MOL | 5.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | f6676d585d07... |
| Energy.csv | CSV | 340 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 860db3b80b4d... |
| complex.pdb | PDB | 716.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | f3f072531a18... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 112b4342ee79... |
| complex_reres.pdb | PDB | 716.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e53a35f52478... |
| index.ndx | NDX | 296.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 73603e5eb32f... |
| CTX-1020742_best_pose_H.mol | MOL | 6.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c445ccc906b2... |
| Energy.csv | CSV | 340 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | a8c0fd5504ed... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 51f864251a92... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 4d532ec7f9a6... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ae70598dc711... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ef996cb27652... |
| CTX-1020743_best_pose_H.mol | MOL | 6.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c12ea4373c0b... |
| Energy.csv | CSV | 333 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | aa2f46ec2918... |
| complex.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e1c9290115a9... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 8c77f3728be9... |
| complex_reres.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e2b9197340e2... |
| CTX-1020744_best_pose_H.mol | MOL | 6.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 4436b8acb9e7... |
| Energy.csv | CSV | 341 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 714cecfce92d... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 357666e19020... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | a26157b8710c... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 7be8d744da26... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ef996cb27652... |
| CTX-1020745_best_pose_H.mol | MOL | 6.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e1122c985d7d... |
| Energy.csv | CSV | 343 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | ed1e6ed150c7... |
| complex.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 91eb1eb276a7... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 3ef8ca3b64b0... |
| complex_reres.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 0e203c5203e5... |
| index.ndx | NDX | 296.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 22e6fdb88e67... |
| CTX-1020746_best_pose_H.mol | MOL | 6.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 5febe66c593b... |
| Energy.csv | CSV | 337 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 034c13894ef7... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 680a97c1ac5f... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | cc09d1765d46... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 6d4bbc1b4f82... |
| CTX-1020747_best_pose_H.mol | MOL | 6.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | edcb7dbab3f0... |
| Energy.csv | CSV | 343 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | df70066edd9b... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 616477987547... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 9f82c24ab646... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | b95133865ef9... |
| CTX-1020748_best_pose_H.mol | MOL | 6.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 632ee627537a... |
| Energy.csv | CSV | 340 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 71c76f9dd60a... |
| complex.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 7d7ec112a0f4... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 3f0832bd6b66... |
| complex_reres.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 0a168c6f60a0... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ce232c22736e... |
| CTX-1020749_best_pose_H.mol | MOL | 6.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | dcc3c99d6ce1... |
| Energy.csv | CSV | 347 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 7b9256e53075... |
| complex.pdb | PDB | 717.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 2d24a2cf2233... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 7eeb9b804aff... |
| complex_reres.pdb | PDB | 717.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 0da02ee6470d... |
| CTX-1020750_best_pose_H.mol | MOL | 5.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 76aba6804f32... |
| Energy.csv | CSV | 334 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 9c9e009b32e9... |
| complex.pdb | PDB | 717.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | f6786e8cf81a... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 1f76e47a64e7... |
| complex_reres.pdb | PDB | 717.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 7bff794e27a6... |
| index.ndx | NDX | 296.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 6cac1bcaa6cc... |
| CTX-1020751_best_pose_H.mol | MOL | 5.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 0db6ce071910... |
| Energy.csv | CSV | 345 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | b69c43cf2229... |
| complex.pdb | PDB | 717.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ff3cf5ddc8c3... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | e6d094492398... |
| complex_reres.pdb | PDB | 717.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 4ea7934ef87f... |
| index.ndx | NDX | 296.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | de61c42f196b... |
| CTX-1020752_best_pose_H.mol | MOL | 7.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c4617c030531... |
| Energy.csv | CSV | 341 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | a9a3e1d859bc... |
| complex.pdb | PDB | 718.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c752e845b3d5... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 2456d8850624... |
| complex_reres.pdb | PDB | 718.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | cb21f34bbae4... |
| index.ndx | NDX | 296.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 3b9bcf5b17a8... |
| CTX-1020753_best_pose_H.mol | MOL | 6.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | d822ed3de476... |
| Energy.csv | CSV | 347 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | b1d8a3f68d80... |
| complex.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 5ce03da70af3... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 0b15f54e8085... |
| complex_reres.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 7bdc64bab743... |
| CTX-1020754_best_pose_H.mol | MOL | 4.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c11cb26dd045... |
| Energy.csv | CSV | 351 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | b40e84775611... |
| complex.pdb | PDB | 716.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | dfe74f0bcbfc... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 275278360aaa... |
| complex_reres.pdb | PDB | 716.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ca96f64f2fd6... |
| CTX-1020755_best_pose_H.mol | MOL | 7.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 0c840b403878... |
| Energy.csv | CSV | 350 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 9f4be215caa5... |
| complex.pdb | PDB | 718.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | a7e13f5b800b... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 1d55d7e7c95a... |
| complex_reres.pdb | PDB | 718.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 80705aaa6e4c... |
| index.ndx | NDX | 296.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 3b9bcf5b17a8... |
| CTX-1020759_best_pose_H.mol | MOL | 7.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 18acde4e722d... |
| Energy.csv | CSV | 340 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | a9b8e4920910... |
| complex.pdb | PDB | 718.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 88a1c749aea0... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 2bcb28769203... |
| complex_reres.pdb | PDB | 718.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | de38c49726d0... |
| index.ndx | NDX | 296.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 983b288dbfba... |
| CTX-1020766_best_pose_H.mol | MOL | 4.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 99813bea8b0c... |
| Energy.csv | CSV | 339 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | b257246503e9... |
| complex.pdb | PDB | 716.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 46553a7a2572... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 1b74ab26a87d... |
| complex_reres.pdb | PDB | 716.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e58ffcf12c51... |
| CTX-1020767_best_pose_H.mol | MOL | 4.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 21561fec5951... |
| Energy.csv | CSV | 336 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | dc7511edb7ee... |
| complex.pdb | PDB | 716.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 32a10dfd95e1... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | d76c712ae54b... |
| complex_reres.pdb | PDB | 716.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 48e1722cf232... |
| index.ndx | NDX | 296.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 43a7febea3f4... |
| CTX-1020769_best_pose_H.mol | MOL | 5.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 2957f893d282... |
| Energy.csv | CSV | 346 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 3453bfd650f8... |
| complex.pdb | PDB | 716.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ba04a15eddea... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 6fffc7ccdb7c... |
| complex_reres.pdb | PDB | 716.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 011a97a539a8... |
| CTX-1020770_best_pose_H.mol | MOL | 4.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 5a708a3141e4... |
| Energy.csv | CSV | 350 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | fda76e5885a1... |
| complex.pdb | PDB | 716.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 102ed2aeff96... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | d5f2ede4f7d0... |
| complex_reres.pdb | PDB | 716.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | d1ff447e6a95... |
| index.ndx | NDX | 296.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 4751fd02695f... |
| CTX-1020772_best_pose_H.mol | MOL | 4.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 5da41a758d65... |
| Energy.csv | CSV | 349 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | b97bf7345c83... |
| complex.pdb | PDB | 716.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 48e0eb3ff79c... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 336d124caaa6... |
| complex_reres.pdb | PDB | 716.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c8a32b17874c... |
| index.ndx | NDX | 296.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 4751fd02695f... |
| CTX-1020795_best_pose_H.mol | MOL | 6.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | bf956b6f65a7... |
| Energy.csv | CSV | 353 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 063a0029725f... |
| complex.pdb | PDB | 718.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 43b54c9615dd... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 8c08c36c44af... |
| complex_reres.pdb | PDB | 718.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e63e5b8f2d62... |
| CTX-1020799_best_pose_H.mol | MOL | 6.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 6c9306a319cf... |
| Energy.csv | CSV | 352 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 27e256408fc6... |
| complex.pdb | PDB | 717.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e268546ef6a2... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 2377afba1bc5... |
| complex_reres.pdb | PDB | 717.8 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 17194a005736... |
| CTX-1020800_best_pose_H.mol | MOL | 6.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 100a8104fd13... |
| Energy.csv | CSV | 347 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 5843267d7d84... |
| complex.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 035fb76324fd... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 14e3ab90ad9d... |
| complex_reres.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 3855374f084b... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ce232c22736e... |
| CTX-1020810_best_pose_H.mol | MOL | 6.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | d5b530036148... |
| Energy.csv | CSV | 346 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 4024ccd5e8ea... |
| complex.pdb | PDB | 718.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 7cc61bd3046c... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 9c56493078e4... |
| complex_reres.pdb | PDB | 718.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 7d6086dd1d82... |
| CTX-1020811_best_pose_H.mol | MOL | 6.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e3870e9cb8f1... |
| Energy.csv | CSV | 347 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | ac77bbeb1fbc... |
| complex.pdb | PDB | 718.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 8416ca80c006... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | b35c1ea40ee0... |
| complex_reres.pdb | PDB | 718.3 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | a040176eee3b... |
| index.ndx | NDX | 296.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 8f0c449e4c6a... |
| CTX-1020816_best_pose_H.mol | MOL | 6.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 2146b6119459... |
| Energy.csv | CSV | 342 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 2d9f68d2a222... |
| complex.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 6a7a86482890... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 30c7ef7d1892... |
| complex_reres.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 05776a1deb4e... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ce232c22736e... |
| CTX-1020817_best_pose_H.mol | MOL | 6.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 0cf7e7593ce1... |
| Energy.csv | CSV | 346 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 781924f282a4... |
| complex.pdb | PDB | 717.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | d826e7c28198... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 4ebf79dc87b5... |
| complex_reres.pdb | PDB | 717.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 17089e40ba88... |
| CTX-1020818_best_pose_H.mol | MOL | 5.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | a2dd61606908... |
| Energy.csv | CSV | 341 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | c98c48152f9c... |
| complex.pdb | PDB | 716.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | f99499246902... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 4f56e6fbeff4... |
| complex_reres.pdb | PDB | 716.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 13be0662ce91... |
| CTX-1020838_best_pose_H.mol | MOL | 6.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ebb578d03c53... |
| Energy.csv | CSV | 341 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 86507a270529... |
| complex.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e928cc58a9e7... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | f4add85704b3... |
| complex_reres.pdb | PDB | 717.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ce0e5ce7476b... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ef996cb27652... |
| CTX-1020842_best_pose_H.mol | MOL | 6.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 768b97c4a045... |
| Energy.csv | CSV | 330 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 3f5105130529... |
| complex.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c356ebb583fb... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | fe083906534e... |
| complex_reres.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | fdab7729d94a... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ce232c22736e... |
| CTX-1020882_best_pose_H.mol | MOL | 6.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c2a71328bce2... |
| Energy.csv | CSV | 346 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 08384ac60e88... |
| complex.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 2849df49c046... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | f4fbb340078d... |
| complex_reres.pdb | PDB | 718.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 9495c0610f75... |
| index.ndx | NDX | 296.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | ce232c22736e... |
| CTX-1020902_best_pose_H.mol | MOL | 6.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | b7aa3c0a9c53... |
| Energy.csv | CSV | 339 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 072cc4901bbd... |
| complex.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | e4bbc0831a87... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | b5fd2a6ff599... |
| complex_reres.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 0fb2c6a180f9... |
| CTX-1020903_best_pose_H.mol | MOL | 6.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | fdc3e934f979... |
| Energy.csv | CSV | 341 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | eae27ff527d0... |
| complex.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 2f7cd70cb931... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 9f7d011409f7... |
| complex_reres.pdb | PDB | 718.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 05f39bd7da15... |
| CTX-1020912_best_pose_H.mol | MOL | 6.2 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 3826ae145e0a... |
| Energy.csv | CSV | 332 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 6c0e56c6b100... |
| complex.pdb | PDB | 717.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | a1455e501ac1... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | f7834a8667c3... |
| complex_reres.pdb | PDB | 717.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | ee898509f8a8... |
| 064_exec.py | PY | 137 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/source | 693428556454... |
| mmgbsa_results.json | JSON | 31.0 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 4808ce6baee6... |
| BindingEnergy.csv | CSV | 389 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | da182423674e... |
| CTX-1020459_best_pose_H.mol | MOL | 6.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 930439c1052b... |
| Energy.csv | CSV | 340 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 576cc8dfd70a... |
| complex.pdb | PDB | 718.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 9b3f82b1dcde... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | dc9e61be2b45... |
| complex_reres.pdb | PDB | 718.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 2e129f126793... |
| CTX-1020695_best_pose_H.mol | MOL | 5.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 9cf2523f7fa5... |
| Energy.csv | CSV | 345 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 438b079b4cf1... |
| complex.pdb | PDB | 717.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 1e2ebbf8cba9... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 27359d4e93f0... |
| complex_reres.pdb | PDB | 717.5 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | bc2fb6997c5d... |
| CTX-1020771_best_pose_H.mol | MOL | 4.9 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | c86ca63b0fc4... |
| Energy.csv | CSV | 340 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | b337e1aef078... |
| complex.pdb | PDB | 716.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 2f79c116ce1c... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | f7fbc53ddb43... |
| complex_reres.pdb | PDB | 716.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 5264ae87cbdd... |
| CTX-1020845_best_pose_H.mol | MOL | 6.1 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 890852c6f46c... |
| Energy.csv | CSV | 349 B | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/tables | 5f6d059e41b2... |
| complex.pdb | PDB | 717.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 4f5077c32bbc... |
| complex.top | TOP | 4.6 MB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/work | 7a760745a9bc... |
| complex_reres.pdb | PDB | 717.6 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/structures | 252185989ab6... |
| 065_path.py | PY | 2.7 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/source | dfc66538f84b... |
| 066_path.py | PY | 1.4 KB | 01_mm_gbsa_binding_free_energies_for_83_cdk2_cyclin/source | 1269c82bfff9... |

## Verification

- 1 tool call(s) ran in this phase, 0 of which reported a failure.
- 476 file(s) were produced and registered, 476 of them with a sha256 digest recorded, so they can be checked against this report.
- Container Image: `registry.rayca.org/rayca-tools/gbsa:latest`

The following numerical claims were independently checked against source files (`mmgbsa_results.json`):

| Claim | Source | Verified value | Result |
| :--- | :--- | :--- | :---: |
| 83 entries in this phase's mmgbsa_results.json (pre-addendum) | `mmgbsa_results.json` length at phase completion | 83 objects | CONFIRMED |
| All 83 have non-null dG_kcal_mol and status "S" | field check across all entries | 0 null, 83 × "S" | CONFIRMED |
| Rank 1 = CTX-1020732, ΔG = −83.188 kcal/mol | `mmgbsa_results.json` row 0 | −83.18772287999909 | CONFIRMED |
| Rank 83 = CTX-1020739, ΔG = −24.691 kcal/mol | `mmgbsa_results.json` row 82 | −24.69146088000033 | CONFIRMED |
| CTX-1017233 at rank 51, ΔG = −49.925 kcal/mol | position and value search | rank 51, −49.925489519998095 | CONFIRMED |
| CTX-1020667 addendum: ΔG = −41.491 kcal/mol, rank 70/84 | `CTX-1020667_mmgbsa_result.json` | −41.490577 | CONFIRMED |
| Merged file has 84 entries, all status "S" | `mmgbsa_results.json` after addendum merge | 84 entries, 0 null | CONFIRMED |

## Limitations

- Versions were not recorded for GNINA, Rayca Modulon. A methods section without a version is not reproducible.

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. J Cheminform. 2021;13:43. doi:10.1186/s13321-021-00522-2
