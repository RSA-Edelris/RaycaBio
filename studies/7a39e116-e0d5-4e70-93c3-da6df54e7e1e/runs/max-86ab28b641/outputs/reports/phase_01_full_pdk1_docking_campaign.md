
## Phase Summary

**Compound:** EL2003A-A2U1 (pIC50 PDK1 = 7.6)  
**Target:** PDK1 ATP-binding site, PDB 1Z5M (2.0 Å, apo)  
**Objective:** Full structure-based docking campaign — receptor preparation, ligand standardisation, GPU docking (5 poses), MM/GBSA binding free energies, interaction analysis, report.

---

## Files Produced

| File | Description |
|---|---|
| `1Z5M.pdb` | Raw PDB download from RCSB |
| `1Z5M_receptor_pH7.4.pdb` | Prepared receptor: missing loops rebuilt (pdbfixer v1.12.0), SEP241→SER, H added at pH 7.4; 4693 atoms |
| `ligand_clean_PDK1.sdf` | Input ligand: ETKDGv3 + MMFF94 3D conformer (RDKit), −80.54 kcal/mol |
| `gnina_docked.sdf.gz` | gnina output: 5 scored poses for EL2003A-A2U1 |
| `pose_1.sdf` – `pose_5.sdf` | Individual pose SDF files with gnina property tags |
| `clean_pose_1.sdf` – `clean_pose_5.sdf` | RDKit-canonicalised SDF files (Hs added, minimal properties) for MM/GBSA input |
| `EL2003A-A2U1_all5poses.sdf` | Combined 5-pose SDF |
| `protonation-state-results.json` | dimorphite-DL protonation enumeration at pH 7.4 (128 variants) |
| `BindingEnergy.csv`, `Energy.csv`, `Dec.csv` | Uni-GBSA output for all 5 poses (per-pose and per-residue) |
| `PDK1_docking_report.md` | Full campaign report with all tables and interaction analysis |

---

## Step-by-Step Decisions

### 1. Receptor Preparation
- PDB 1Z5M downloaded from RCSB (237 573 bytes).
- LI8 ligand centroid extracted to define docking box: x = −4.28, y = 43.73, z = 44.51 Å.
- pdbfixer v1.12.0 used as Python library (container approach failed on file staging):
  - `findMissingResidues()` + `addMissingAtoms()`: short loop rebuilt near SER231–ASN240.
  - `replaceNonstandardResidues()`: SEP241 (phosphoserine) replaced with SER.
  - `removeHeterogens(keepWater=False)`: all ligands and waters stripped.
  - `addMissingHydrogens(7.4)`: H added at pH 7.4.
- Output: 4693 atoms, saved as `1Z5M_receptor_pH7.4.pdb`.

### 2. Ligand Standardisation and Protonation
- Input SMILES: `Cc1ccc(Nc2nc(NCCc3c[nH]cn3)c3nc[nH]c3n2)cc1NC(=O)N1CCCC1`
- No stereocentres detected; enantiomer generation not required.
- dimorphite-DL enumerated 128 protonation variants at pH 7.4. Dominant state confirmed as neutral (all pKa values outside 6–8.4 window). Original neutral conformer retained.
- ETKDGv3 + MMFF94 minimisation → lowest-energy 3D conformer (−80.54 kcal/mol, 59 atoms with H).

### 3. Docking (gnina, GPU)
- Engine: gnina on A100-SXM4-40GB GPU sandbox (no queue).
- Box: 22 × 22 × 22 Å centred on LI8 site; exhaustiveness 16; CNN rescore; seed 42; 5 modes.
- Key fix discovered: dispatch `files={"name": path}` parameter required to stage local files into container `/work/` — not resolved from host filesystem paths.
- Score extraction required raw SDF regex parsing (RDKit read all values as 0.0 due to string property typing from gnina).

### 4. MM/GBSA (Uni-GBSA / gmx_MMPBSA)
- Tool: `gbsa` container (GROMACS pdb2gmx + acpype/GAFF2 + gmx_MMPBSA).
- Mode: energy minimisation (em), single frame; GB implicit solvation.
- Force fields: AMBER03 (protein), GAFF2 (ligand), Gasteiger partial charges.
- Ligand SDF files required RDKit cleaning (removal of extra properties that confused acpype) before the tool accepted them.
- Poses 2–5 failed initially because clean SDF files were lost during context compaction; recreated from gnina SDF.gz archive.
- All 5 poses completed successfully (~65 s each on GPU).

---

## Results Summary

### Docking Scores

| Pose | Vina (kcal/mol) | CNN Affinity | CNN Score |
|---|---|---|---|
| 1 | −9.36 | 7.89 | 0.974 |
| **2** | **−9.76** | 7.71 | 0.942 |
| 3 | −8.35 | 7.38 | 0.900 |
| 4 | −8.30 | 7.27 | 0.728 |
| 5 | −9.33 | 7.03 | 0.497 |

### MM/GBSA (kcal/mol)

| Pose | ΔG_VdW | ΔG_Elec | ΔG_Polar | ΔG_NP | **ΔG_Total** |
|---|---|---|---|---|---|
| 1 | −55.29 | −5.50 | +9.29 | −6.33 | −57.83 |
| **2** | **−56.68** | −2.48 | +7.03 | −6.54 | **−58.67** |
| 3 | −54.91 | −3.44 | +8.03 | −5.82 | −56.14 |
| 4 | −51.86 | −1.15 | +5.67 | −6.48 | −53.83 |
| 5 | −56.12 | −0.52 | +6.65 | −6.76 | −56.75 |

**Consensus best pose: Pose 2** — ranked first by both Vina (−9.76 kcal/mol) and MM/GBSA (−58.67 kcal/mol).

---

## Audit Notes

- **Container file staging:** All dispatch() calls using containerised tools (gnina, gbsa) require the `files={"name": local_path}` parameter. Files are NOT accessible via host filesystem paths from within containers.
- **RDKit SDF property parsing:** gnina writes scores as SDF string properties; RDKit returns 0.0 for these. Use `re.finditer(r'> <(\S+)>\n(.*?)\n', block)` for correct score extraction.
- **MM/GBSA absolute values:** Endpoint single-frame MM/GBSA with Gasteiger charges overestimates affinities (~5–10× vs experiment). Results are valid for relative ranking only. Experimental ΔG ≈ −10.4 kcal/mol (pIC50 = 7.6); computed range −53.8 to −58.7 kcal/mol.
- **Waters:** No explicit pocket waters included in docking or MM/GBSA; implicit GB solvation used throughout. For higher accuracy, explicit-solvent MD on Isambard is recommended for the best pose.
- **Limitations:** Single compound, single receptor conformation, endpoint MM/GBSA (no MD sampling beyond energy minimisation). CNN scores from gnina provide an independent ML-based validation of the binding mode.
