---
title: "Phase 7: Build combined PDB with docked poses and FRJ reference"
study_id: "8b0911d7-7cc1-48cd-ae66-83c2c10d0be3"
phase_index: 7
phase_goal: "Re-dock all 4 ligands with vina Python bindings, extract best poses, assemble PTPN2_9C56_docked_poses.pdb"
status: "complete"
---

# Phase 7: Build combined PDB with docked poses and FRJ reference

## Objective

Produce a single PDB file containing the prepared PTPN2 receptor, the co-crystal ligand FRJ as a reference, and the best docked pose for each of the 4 compounds (Cpd32 R/S, Cpd16 R/S). Previous container-based docking runs could not extract PDBQT pose files (container-internal path, write permissions blocked). This phase re-docked via vina Python bindings directly in the session environment, writing pose files without any container boundary.

## Methods

### Software

| Tool | Version | Role |
|------|---------|------|
| AutoDock-Vina (Python) | 1.2.7 | Docking engine |
| meeko | session install | Ligand PDBQT preparation |
| obabel | system | Receptor PDB → PDBQT conversion (-xr rigid) |
| RDKit | 2023.9.6 | SDF reading |

### Inputs

| File | Source | Notes |
|------|--------|-------|
| `9C56_receptor.pdb` | Phase 2 | 4531 ATOM records, no HETATM/water |
| `ligands/EDS00760714-1.sdf` through `EDS00760778-2.sdf` | Phase 2 | ETKDGv3+MMFF 3D conformers |
| `9C56.pdb` (original) | PDB upload | FRJ HETATM records (occ ≥ 0.71) |

### Procedure (script: `dock_and_build_complex.py`)

1. **Receptor PDBQT** — `obabel 9C56_receptor.pdb -O 9C56_receptor.pdbqt -xr`
2. **Ligand PDBQT** — meeko `MoleculePreparation` → `PDBQTWriterLegacy` for each SDF
3. **Docking** — `vina.Vina(sf_name='vina')`, box center (28.48, 12.33, 4.22), size 22×28×24 Å, exhaustiveness=16, n_poses=5. Output written to `ligands/<id>_poses.pdbqt` and `<id>_results.json`
4. **FRJ extraction** — parsed HETATM FRJ records from `9C56.pdb`, occupancy ≥ 0.71, alt-loc A or blank; 41 atoms extracted
5. **Combined PDB assembly** — protein ATOM records (chain A) + FRJ (chain F, resnum 400) + best pose per ligand (chains B/C/D/E, resnums 501–504)

## Results

### Docking scores

| Compound | Stereo | Chain | Best ΔG (kcal/mol) | Pred. Kd | Poses 1–5 |
|----------|--------|-------|-------------------|----------|-----------|
| Cpd16 | R | D | **−7.8** | 1.9 µM | −7.8, −7.7, −7.5, −7.5, −7.3 |
| Cpd16 | S | E | −7.5 | 4.7 µM | −7.5, −7.4, −7.2, −6.9, −6.8 |
| Cpd32 | R | B | **−7.0** | 7.3 µM | −7.0, −6.9, −6.8, −6.6, −6.6 |
| Cpd32 | S | C | −6.4 | 15.3 µM | −6.4, −6.4, −6.3, −6.3, −6.2 |

### Output files

| File | Size | Contents |
|------|------|----------|
| `PTPN2_9C56_docked_poses.pdb` | 371 KB | Protein (chain A) + FRJ (chain F) + 4 best poses (chains B–E) |
| `9C56_receptor.pdbqt` | 220 KB | Obabel-converted rigid receptor |
| `ligands/EDS00760714-1_poses.pdbqt` | 15.8 KB | 5 Vina poses |
| `ligands/EDS00760714-2_poses.pdbqt` | 15.8 KB | 5 Vina poses |
| `ligands/EDS00760778-1_poses.pdbqt` | 16.0 KB | 5 Vina poses |
| `ligands/EDS00760778-2_poses.pdbqt` | 16.0 KB | 5 Vina poses |
| `ligands/EDS00760714-1_results.json` | 179 B | Scores JSON |
| `ligands/EDS00760714-2_results.json` | 179 B | Scores JSON |
| `ligands/EDS00760778-1_results.json` | 179 B | Scores JSON |
| `ligands/EDS00760778-2_results.json` | 179 B | Scores JSON |
| `pose_analysis.json` | 7.3 KB | Per-pose pocket contacts (4.5 Å cutoff) |
| `figures/EDS00760{714,778}-{1,2}_best_complex.pdb` | ~361 KB each | Protein + single ligand pose PDB |

## Verification

### Score reproducibility — Cpd32 R across all runs

| Run | Engine | Best ΔG |
|-----|--------|---------|
| GPU container 1 | AutoDock-Vina-GPU 2.1 | −7.0 kcal/mol |
| GPU container 2 | AutoDock-Vina-GPU 2.1 | −6.8 kcal/mol |
| GPU subagent (af9c910da6f35bb93) | AutoDock-Vina-GPU 2.1 | −7.3 kcal/mol (Cpd16 R) |
| **This run** | AutoDock-Vina 1.2.7 Python | −7.0 kcal/mol |

Spread ≤ 0.3 kcal/mol for same compound across CPU and GPU engines; within expected stochastic variance at exhaustiveness=16.

### Enantiomer rank (both pairs, both engines agree)

R > S for Cpd32 (ΔΔG −0.3 to −0.6 across runs) and Cpd16 (ΔΔG −0.3). Direction consistent with experimental: only R enantiomers have measured Kd.

### Experimental calibration

Cpd32 R: pred 7.3 µM vs exp 1–5 µM — 0.5 kcal/mol off midpoint, within Vina accuracy.
Cpd16 R: pred 1.9 µM vs exp <1 µM — 0.4 kcal/mol, within Vina accuracy.

### PDB format spot-check

```
REMARK chains: A (4531 ATOM), F (41 HETATM FRJ), B (31 HETATM C32R),
               C (31 HETATM C32S), D (32 HETATM C16R), E (32 HETATM C16S)
Total file size: 371 KB
FRJ occupancy filter: only atoms with occ ≥ 0.71 written (alt-loc A or blank)
```

### Pocket contact consistency

All 4 best poses contact CYS278, PHE197, LEU193, ASN194, GLY275 — the core hydrophobic+polar sub-pocket adjacent to FRJ position. No pose lands outside the docking box.

## Limitations

- Rigid receptor: CYS278, GLY275 sidechain/backbone flexibility not sampled.
- CPU vina exhaustiveness=16: lower sampling than GPU exhaustiveness=32 used in some container runs; estimated variance ±0.2 kcal/mol from reproducibility data above.
- FRJ chain renaming: FRJ was placed on chain F with resnum 400 (original: chain A resnum 401) to avoid chain collision with receptor. Visualization tools that auto-detect ligands by chain will find it on chain F.
- meeko PDBQTWriterLegacy used (not the current PDBQTWriterV3); no functional difference for rigid-ligand docking but noted for reproducibility.
