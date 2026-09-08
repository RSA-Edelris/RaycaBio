
## Phase Identity

**Phase:** Full PDK1 Docking Campaign  
**Input:** `ligand_clean_PDK1.sdf` (6 ligands, explicit H, ETKDGv3+MMFF94 3D conformers)  
**Receptor:** PDB 1Z5M, chain A (PDK1, 2.00 Å resolution)  
**Status:** Completed successfully  
**Date:** 2026-09-07

---

## What Was Done

### Step 1 — Receptor preparation
- Fetched 1Z5M from RCSB; extracted chain A
- Removed HETATM records (LI8 co-crystal ligand, water)
- Protonated at pH 7.4 using PDB2PQR + PROPKA; Lys38 NZ remains +1, Glu/Asp deprotonated
- No missing loops in the binding-site region (residues 10–160)
- Output: `1Z5M_receptor_pH7.4.pdb` (4693 atoms, 371 kB)

### Step 2 — Docking box definition
- Extracted LI8 HETATM coordinates from raw 1Z5M.pdb
- LI8 heavy-atom centroid: x = −4.283 Å, y = 43.728 Å, z = 44.510 Å
- Box dimensions: 22.0 × 22.0 × 22.0 Å (covers full ATP-binding cleft with margin)
- No active-site waters within 5 Å of centroid; none kept as explicit docking waters

### Step 3 — Ligand standardisation
- All 6 ligands already prepared (3D, explicit H, MMFF94 minimised) from prior phases
- pH 7.4 protonation check via dimorphite-dl: all 6 returned 0 additional variants (neutral at physiological pH)
- Stereochemistry: EL5003A confirmed as absolute (R,R) by MDLV30/STEABS collection; no enantiomers generated
- Protonation results saved: `protonation-state-results-2.json`, `protonation-state-results-3.json`, `protonation-state-results-4.json`

### Step 4 — GNINA docking
- Engine: GNINA (GPU sandbox, `cnnScoring=rescore`, `exhaustiveness=16`, `numModes=5`, `seed=42`)
- All 6 ligands submitted in one batch (`ligand_clean_PDK1.sdf`)
- Runtime: 191 s (GPU); rc = 0
- Output: `gnina_docked.sdf.gz` (30 poses, 5 per ligand)
- Per-pose scores parsed from gzipped SDF: `minimizedAffinity`, `CNNscore`, `CNNaffinity`
- Individual pose files written to `all_poses/` (30 files: `{LIG}_pose{1-5}.sdf` + `{LIG}_best.sdf` + `{LIG}_5poses.sdf`)
- Result JSON: `gnina_all6_result.json`

### Step 5 — MM-GBSA refinement and binding free energies
- Protocol: Uni-GBSA via GROMACS energy minimisation (`mode=em`, `method=gb`, AMBER03 protein, GAFF2 ligand, gas-phase charges)
- 6 dispatch calls (one per ligand), each submitting all 5 pose SDF files via `ligandFiles` parameter
- All 6 completed rc = 0 (GPU sandbox used); 30 ΔG values obtained
- Per-ligand JSON results: `gbsa_EL2003A-A2U1.json`, `gbsa_EL2003A.json`, `gbsa_EL2003A-A4U1.json`, `gbsa_BX912.json`, `gbsa_EL5001A.json`, `gbsa_EL5003A.json`

### Step 6 — Interaction analysis
- Receptor atoms parsed from `1Z5M_receptor_pH7.4.pdb` (4693 atoms)
- Best pose per ligand selected by lowest MM-GBSA ΔG
- H-bonds detected: N/O/S–N/O/S distance ≤ 3.5 Å
- Hydrophobic contacts: C–C distance ≤ 4.5 Å
- General contacts: any heavy-atom pair ≤ 5.0 Å
- Results saved: `interactions_best_poses.json`

### Step 7 — Reporting
- Full 30-pose combined table (docking + MM-GBSA): `full_docking_gbsa_table.csv`
- Comprehensive campaign report: `PDK1_docking_campaign_final_report.md`

---

## Key Numerical Results

### Best MM-GBSA ΔG per ligand (best pose)

| Molecule | Best Pose | MM-GBSA ΔG (kcal/mol) | GNINA Affinity (kcal/mol) | pIC50 (exp.) |
|:---------|:---------:|:---------------------:|:-------------------------:|:------------:|
| EL2003A-A4U1 | 1 | **−64.74** | −9.315 | 7.5 |
| EL2003A | 2 | −61.84 | −9.800 | 7.5 |
| EL2003A-A2U1 | 2 | −61.67 | −9.760 | 7.6 |
| BX912 | 2 | −60.33 | −8.908 | 6.0 |
| EL5003A | 3 | −57.19 | −8.108 | 6.8 |
| EL5001A | 1 | −54.42 | −7.730 | 6.5 |

### Universal pharmacophoric contacts (6/6 ligands)
- **H-bonds:** GLU93 (backbone N + sidechain OE2), LEU15 (backbone O) — canonical PDK1 hinge
- **Hydrophobic:** LEU15, ALA89, LEU139, VAL23, ALA36, GLU93, THR149

---

## Files Produced by This Phase

| File | Type | Description |
|:-----|:----:|:-----------|
| `1Z5M_receptor_pH7.4.pdb` | Structure | Prepared receptor (pH 7.4) |
| `gnina_docked.sdf.gz` | Structure | 30 docked poses |
| `gnina_all6_result.json` | Data | GNINA dispatch result |
| `all_poses/{LIG}_pose{N}.sdf` | Structure | 30 individual pose files |
| `all_poses/{LIG}_best.sdf` | Structure | 6 best-docking-score poses |
| `gbsa_{LIG}.json` | Data | MM-GBSA results (6 files) |
| `full_docking_gbsa_table.csv` | Table | Combined 30-pose score table |
| `interactions_best_poses.json` | Data | H-bond/hydrophobic contacts per ligand |
| `PDK1_docking_campaign_final_report.md` | Report | Full campaign report |

---

## Audit Notes

- Box centre recovered from LI8 HETATM records in raw PDB (script `048_read_dispatch_script_succeeded_get_actual_cx_cy_cz.py`)
- gnina SDF property regex fixed to `> {1,2}<field>` (1 space, not 2) after initial parse failure
- Ligand-name matching used longest-first ordering to prevent EL2003A absorbing EL2003A-A4U1 records
- All 6 GBSA dispatches returned rc=0; no failed poses; 30/30 ΔG values obtained
- Interaction cutoffs: H-bond 3.5 Å, hydrophobic 4.5 Å, general contact 5.0 Å — standard values, no tuning applied
