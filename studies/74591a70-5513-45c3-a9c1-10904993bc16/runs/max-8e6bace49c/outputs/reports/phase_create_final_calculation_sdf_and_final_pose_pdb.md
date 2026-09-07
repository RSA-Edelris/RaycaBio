## Objective

Consolidate all CRBN docking campaign results into three deliverable files.

## Files Produced

| File | Size | Content |
|------|------|---------|
| `final_calculation.sdf` | 78,229 bytes | 22 compounds, best docked 3D pose, 17 SD tags |
| `final_calculation_2d.sdf` | 78,229 bytes | 22 compounds, 2D depiction of correct enantiomer, 17 SD tags |
| `final_pose.pdb` | 562,949 bytes | CRBN receptor (chain B) + LVY crystal ligand + 22 docked poses (chains C–X) |

## Method

**SDF generation** (`build_final_outputs.py`):
1. Load each compound's top-ranked gnina pose from `best_poses2_top1/{name}_pose1.sdf`
2. Strip all gnina-provided SD properties (gnina embeds a stray `$$$$` terminator that splits records on re-write)
3. Call `AssignStereochemistryFrom3D()` + `AssignStereochemistry()` to derive R/S from 3D geometry
4. Generate isomeric SMILES as `SMILES_stereo` tag
5. Compute 2D coordinates via `rdDepictor.Compute2DCoords()` with CoordGen for a second SDF with correct stereo wedges
6. Write 17 SD tags per compound (docking scores, MM-GBSA energy components, interaction residues)

**SD tags written per compound:**
`SMILES_stereo`, `Docking_Affinity_kcal_mol`, `CNN_Affinity`, `CNN_Pose_Score`, `N_Docking_Poses`, `MMGBSA_dG_kcal_mol`, `MMGBSA_dG_std`, `MMGBSA_VdW_kcal_mol`, `MMGBSA_EEL_kcal_mol`, `MMGBSA_EGB_kcal_mol`, `MMGBSA_ESURF_kcal_mol`, `Interacting_Residues`, `HBond_Residues`, `Hydrophobic_Residues`, `PiStacking_Residues`, `N_Interactions`

**PDB generation:**
- Chain B ATOM records from `4CI2_receptor_for_docking.pdb` (6,188 atoms, pH 7.4 protonation)
- LVY crystal reference HETATM records from `4CI2_LVY_ref.pdb` (32 atoms, chain B residue 1429)
- Each docked pose written as HETATM `LIG` with a unique chain letter (C–X), preceded by a REMARK line with compound name, affinity, and MM-GBSA ΔG

## Key Bug Fixed

gnina writes an extra `$$$$` record terminator inside the SDF property block. When RDKit re-writes the mol, this creates a second split record per compound (44 records instead of 22). Fix: call `mol.ClearProp(pname)` for all existing properties after loading, before setting our own.

## Verification

- `final_calculation.sdf`: 22/22 valid records, 3D coords confirmed (max|z|>0.01 Å), stereo SMILES present, all 17 SD tags present
- `final_calculation_2d.sdf`: 22/22 valid records, all z=0.000 (pure 2D)
- `final_pose.pdb`: 6,188 ATOM + 32 LVY + 698 docked LIG HETATM, 23 chains (B + C–X)
