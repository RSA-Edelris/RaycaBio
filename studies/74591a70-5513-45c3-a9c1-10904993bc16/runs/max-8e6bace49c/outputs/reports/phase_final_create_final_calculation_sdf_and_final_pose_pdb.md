## Objective

Consolidate all results from the CRBN docking campaign into two deliverable files:

1. **`final_calculation.sdf`** — 22 compounds with best docked 3D poses and all computed scores as SD tags
2. **`final_calculation_2d.sdf`** — 22 compounds with 2D structures of the correct enantiomers and identical score tags
3. **`final_pose.pdb`** — CRBN receptor + LVY crystal reference ligand + all 22 docked best poses in a single multi-chain PDB file

---

## Source Data

| File | Description |
|------|-------------|
| `best_poses2_top1/*.sdf` | 22 top-ranked docked poses (gnina, rank 1 per compound) |
| `docking2_results.json` | gnina affinity and CNN scores per compound |
| `mmgbsa2_results.json` | MM-GBSA DELTA_TOTAL, VdW, EEL, EGB, ESURF per compound |
| `interaction_fingerprints.json` | Per-compound interaction profiles (H-bond, hydrophobic, π) |
| `4CI2_LVY_ref.pdb` | LVY crystal reference ligand extracted from 4CI2 |
| `4CI2_receptor_for_docking.pdb` | Prepared CRBN receptor, chain B, pH 7.4 protonation |

---

## Method

### SDF files (`build_final_outputs.py`)

For each of the 22 compounds:

1. Load the top-ranked docked pose from `best_poses2_top1/{name}_pose1.sdf` (gnina V2000 SDF, heavy atoms).
2. Clear all gnina-provided SD properties from the mol object (gnina embeds an extra `$$$$` in its property block which would corrupt the output; stripping upstream properties avoids this).
3. Call `Chem.AssignStereochemistryFrom3D()` and `Chem.AssignStereochemistry()` to assign R/S and E/Z from the 3D geometry.
4. Generate canonical isomeric SMILES with `Chem.MolToSmiles(isomericSmiles=True)` and store as `SMILES_stereo` tag.
5. Build a 2D mol object: strip hydrogens, remove all conformers, run `rdDepictor.Compute2DCoords()` with CoordGen (`SetPreferCoordGen(True)`) to generate high-quality 2D depiction with correct stereo wedges.
6. Set identical SD tags on both the 3D mol and the 2D mol:

| SD Tag | Source | Notes |
|--------|--------|-------|
| `SMILES_stereo` | RDKit | Isomeric SMILES from 3D-assigned stereo |
| `Docking_Affinity_kcal_mol` | gnina best pose | Vina-style affinity |
| `CNN_Affinity` | gnina best pose | CNN-predicted pKi |
| `CNN_Pose_Score` | gnina best pose | CNN pose quality score |
| `N_Docking_Poses` | gnina | Number of poses generated (5) |
| `MMGBSA_dG_kcal_mol` | AMBER MMPBSA.py | DELTA_TOTAL (4 d.p.) |
| `MMGBSA_dG_std` | AMBER MMPBSA.py | Standard deviation |
| `MMGBSA_VdW_kcal_mol` | AMBER MMPBSA.py | van der Waals energy |
| `MMGBSA_EEL_kcal_mol` | AMBER MMPBSA.py | Electrostatic energy |
| `MMGBSA_EGB_kcal_mol` | AMBER MMPBSA.py | Generalised Born solvation |
| `MMGBSA_ESURF_kcal_mol` | AMBER MMPBSA.py | Non-polar solvation |
| `Interacting_Residues` | RDKit geometry analysis | All residues with any contact |
| `HBond_Residues` | RDKit geometry analysis | H-bond partners only |
| `Hydrophobic_Residues` | RDKit geometry analysis | Hydrophobic contact partners |
| `PiStacking_Residues` | RDKit geometry analysis | π-stacking partners |
| `N_Interactions` | RDKit geometry analysis | Total interaction count |

7. Write the 3D mol to `final_calculation.sdf` and the 2D mol to `final_calculation_2d.sdf`.

### PDB file

1. Extract all `ATOM` records from `4CI2_receptor_for_docking.pdb` (chain B, 6,188 ATOM records).
2. Append LVY crystal reference ligand HETATM records from `4CI2_LVY_ref.pdb` (chain B, residue 1429, 32 atoms).
3. For each of the 22 docked best poses (sorted by name):
   - Assign unique chain letter C–X (one per compound).
   - Write each heavy atom as a HETATM record with residue name `LIG`.
   - Prepend a REMARK line per compound: compound name, chain, docking affinity, MM-GBSA ΔG.
4. Terminate with `END`.

---

## Results

### final_calculation.sdf (3D poses)

- **22/22 compounds**, all valid, no None records
- 3D coordinates present for all (max |z| > 0.01 Å for all)
- Stereo-annotated SMILES present for all (contains `@` or `/`)
- All 17 SD tags present for all 22 compounds

### final_calculation_2d.sdf (2D enantiomers)

- **22/22 compounds**, all valid
- All z-coordinates = 0.000 (pure 2D)
- Same 17 SD tags as the 3D file

### final_pose.pdb

| Component | Chain | Records |
|-----------|-------|---------|
| CRBN receptor | B | 6,188 ATOM |
| LVY crystal ligand | B, res 1429 | 32 HETATM |
| Compound_10_ent1 | C | ~31 HETATM LIG |
| Compound_10_ent2 | D | ~31 HETATM LIG |
| … (22 compounds) | C–X | 698 HETATM LIG total |

Total: 6,964 PDB lines, 562,949 bytes.

---

## Key Technical Issue Resolved

**gnina SDF `$$$$` contamination**: gnina writes its own `$$$$` record terminator as part of the SDF property block. When the mol is loaded by RDKit and re-written via `SDWriter`, this embedded `$$$$` splits each record in two — the SDMolSupplier reads 44 records (22 valid + 22 split fragments) instead of 22. Fix: call `mol.ClearProp(pname)` for all existing properties immediately after loading, before setting any new properties. This removes all gnina-provided SD data (including the embedded terminator) and results in a clean 22-record output.

---

## Files Produced

| File | Size | Records |
|------|------|---------|
| `final_calculation.sdf` | 78,229 bytes | 22 (3D docked poses) |
| `final_calculation_2d.sdf` | 78,229 bytes | 22 (2D enantiomers) |
| `final_pose.pdb` | 562,949 bytes | receptor + LVY + 22 ligands |
| `build_final_outputs.py` | — | Source script |
