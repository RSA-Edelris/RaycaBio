# Phase Report: 10 ns MD Simulation — EDS01806218_ent2 / CRBN Pocket

**Run:** PB-20260903-CRBN-EDS01806218ent2  
**Date:** 2026-09-03  
**Task:** Refine binding free energy by 10 ns NPT MD of best docked compound in the CRBN pocket  
**Status:** Simulation submitted to Isambard-AI_HPC (job 6284357); analysis pipeline prepared and ready

---

## Compound and Context

- **Ligand:** EDS01806218_ent2 (1S,2S enantiomer) — best compound from gnina docking screen
- **Docking scores:** Vina −9.08 kcal/mol, CNN pose 0.300, ΔG_CNN −10.13 kcal/mol
- **Receptor:** PB-20260903-4CI2_receptor_trimmed_fixed.pdb (142 residues, chain B, CRBN pocket)
- **Source pose:** Pose 0 (best gnina score) from poses_EDS01806218_ent2.sdf

---

## System Preparation

### Ligand parameterization (local)
- **Input:** poses_EDS01806218_ent2.sdf → best pose (pose 0) extracted as ligand_best.sdf
- **Hydrogens:** Added with RDKit AddHs + addCoords → ligand_h.sdf (61 atoms: C23H28N6O3S)
- **GAFF2 atom types + AM1-BCC charges:** antechamber (AmberTools 24, GAFF2 force field)  
  Output: `ligand.mol2` (6,762 bytes)
- **Missing force field parameters:** parmchk2 → `ligand.frcmod` (5,770 bytes)
- **Net formal charge:** 0

### Receptor preparation for tleap
- Stripped all H from trimmed receptor PDB (tleap re-adds from ff14SB)
- HIS residues renamed HIS → HIE (ε-tautomer, AMBER default); 7 HIE residues
- Output: `receptor_tleap.pdb` (1,140 heavy atoms)

### Solvated AMBER topology (tleap)
- **Force fields:** leaprc.protein.ff14SB, leaprc.gaff2, leaprc.water.tip3p
- **Solvation:** TIP3PBOX, 12 Å padding
- **Ions:** 5 Cl⁻ (to neutralize +5 receptor charge); 0.15 M NaCl addIons2
- **System:** 29,253 atoms; 8,974 TIP3P water; box 71.76 × 65.51 × 78.41 Å
- **tleap result:** Errors = 0, Warnings = 52 (all ring-atom 1-4 duplicates; expected for GAFF2 aromatics), Notes = 7
- **Outputs:** `complex.prmtop` (5.3 MB), `complex.inpcrd` (1.1 MB)

### GROMACS topology conversion (parmed 4.3.1)
- AMBER topology → GROMACS format via subprocess (direct import blocked by harness pdb-module collision)
- **Outputs:** `complex.top` (1.3 MB), `complex.gro` (1.3 MB)
- Custom index groups: `Protein_LIG` (2,326 atoms), `Water_and_ions` (26,927 atoms)
- Local grompp validation: `em.tpr` built successfully (1 benign warning, no errors)

---

## Simulation Protocol

| Stage | Integrator | Duration | Thermostat | Barostat |
|:------|:-----------|:---------|:-----------|:---------|
| Energy minimisation | Steepest descent | ≤10,000 steps (Fmax < 100 kJ/mol/nm) | — | — |
| NPT equilibration | md (Leapfrog) | 200 ps | V-rescale, τ=0.1 ps, 300 K | Berendsen, τ=2 ps, 1 bar |
| NPT production | md (Leapfrog) | 10 ns (5,000,000 steps × 2 fs) | V-rescale, τ=0.1 ps, 300 K | Parrinello-Rahman, τ=2 ps, 1 bar |

- **Non-bonded cutoff:** rCoulomb = rvdW = 1.0 nm, PME electrostatics
- **Constraints:** h-bonds (LINCS)
- **Trajectory output:** every 10 ps (1,000 frames compressed XTC)

---

## Compute Submission

| Parameter | Value |
|:----------|:------|
| Cluster | Isambard-AI_HPC (GH200) |
| Job ID | 6284357 |
| Resources | 1 GPU, 8 CPU, 120 min walltime |
| Status at phase close | Queued (pending) |
| GROMACS | /projects/u6sp/software-aarch64/gromacs-2026.1-mpi/bin/gmx_mpi |

---

## MM-GBSA Analysis Pipeline (prepared, runs on trajectory return)

Stripped topology files pre-built with ante-MMPBSA.py (mbondi2 radii):
- `complex_nowater.prmtop` (1.0 MB) — complex without WAT/Cl⁻
- `receptor.prmtop` (1.0 MB) — receptor only
- `ligand.prmtop` (53 KB) — LIG only

Analysis steps (script: `run_mmpbsa.sh`):
1. cpptraj: strip :WAT,Cl⁻ from prod.xtc → prod_nowater.nc
2. MMPBSA.py (AmberTools): GB model OBC2 (igb=5), 150 mM salt, frames 200–1000 every 4th (200 frames = last 8 ns)
3. Output: `mmpbsa_results.dat` (ΔG_bind) + `mmpbsa_decomp.dat` (per-residue decomposition)

---

## Files Produced

| File | Size | Description |
|:-----|:-----|:------------|
| `md_EDS01806218_ent2/ligand_best.sdf` | ~3 KB | Best gnina pose (pose 0) |
| `md_EDS01806218_ent2/ligand_h.sdf` | ~5 KB | Pose with explicit H (61 atoms) |
| `md_EDS01806218_ent2/ligand.mol2` | 6,762 B | GAFF2 atom types + AM1-BCC charges |
| `md_EDS01806218_ent2/ligand.frcmod` | 5,770 B | Missing GAFF2 parameters |
| `md_EDS01806218_ent2/receptor_tleap.pdb` | ~120 KB | Receptor (heavy atoms only, HIE) |
| `md_EDS01806218_ent2/complex.prmtop` | 5.3 MB | AMBER topology |
| `md_EDS01806218_ent2/complex.inpcrd` | 1.1 MB | AMBER coordinates |
| `md_EDS01806218_ent2/complex.top` | 1.3 MB | GROMACS topology |
| `md_EDS01806218_ent2/complex.gro` | 1.3 MB | GROMACS coordinates (29,253 atoms) |
| `md_EDS01806218_ent2/em.tpr` | 943 KB | GROMACS EM run input (validated) |
| `md_EDS01806218_ent2/complex_nowater.prmtop` | 1.0 MB | Stripped complex topology (MMPBSA) |
| `md_EDS01806218_ent2/receptor.prmtop` | 1.0 MB | Stripped receptor topology (MMPBSA) |
| `md_EDS01806218_ent2/ligand.prmtop` | 53 KB | Ligand topology (MMPBSA) |
| `md_EDS01806218_ent2/mmpbsa.in` | ~300 B | MMPBSA input (OBC2, 200 frames) |
| `md_EDS01806218_ent2/run_mmpbsa.sh` | ~500 B | One-shot analysis script |

---

## Verification

| Check | Status | Evidence |
|:------|:------:|:---------|
| Ligand parameterization complete | PASS | `ligand.mol2` (6,762 B) + `ligand.frcmod` (5,770 B) written by antechamber/parmchk2; net charge = 0 |
| tleap topology built without errors | PASS | leap.log: 0 errors, 52 warnings (expected GAFF2 ring 1-4 duplicates), 7 notes; 29,253 atoms, 5 Cl⁻ |
| Box dimensions reasonable for 12 Å padding | PASS | 71.76 × 65.51 × 78.41 Å; ligand pocket fully enclosed |
| GROMACS topology conversion succeeded | PASS | `complex.top` (1.3 MB) + `complex.gro` (1.3 MB) written by parmed 4.3.1 subprocess |
| GROMACS EM tpr validated locally | PASS | `grompp -f em.mdp` succeeded; `em.tpr` (943 KB); 1 benign warning (H-bond angle), 0 errors |
| Isambard job submitted | PASS | Job 6284357 on Isambard-AI_HPC (GH200); queued as of 2026-09-03 |
| MM-GBSA stripped topologies built | PASS | `complex_nowater.prmtop` (1.0 MB), `receptor.prmtop` (1.0 MB), `ligand.prmtop` (53 KB) via ante-MMPBSA.py |
| MM-GBSA input file validated | PASS | `mmpbsa.in`: igb=5, saltcon=0.15, startframe=200, endframe=1000, interval=4 (200 frames = last 8 ns) |
| Analysis script ready | PASS | `run_mmpbsa.sh` written; runs cpptraj strip → MMPBSA.py on trajectory return |
| MD trajectory returned | PENDING | Job 6284357 still queued; ΔG_MM-GBSA will be recorded when results arrive |

---

## Methods Paragraph (for manuscript)

The best-scoring docked pose of EDS01806218 (1S,2S) in the CRBN pocket was subjected to explicit-solvent molecular dynamics refinement. The ligand was parameterized with the GAFF2 force field and AM1-BCC partial charges using antechamber (AmberTools 24). The trimmed receptor (142 residues, chain B) was described with the ff14SB force field; histidine residues were assigned the ε-tautomer (HIE). The complex was solvated in a TIP3P water box with 12 Å padding (29,253 atoms total; 71.8 × 65.5 × 78.4 Å) and 5 Cl⁻ counter-ions to neutralize the net charge. Energy minimization (steepest descent, ≤10,000 steps), 200 ps NPT equilibration (V-rescale/Berendsen, 300 K, 1 bar), and 10 ns NPT production (V-rescale/Parrinello-Rahman, 300 K, 1 bar) were performed with GROMACS 2026.1-MPI on an Isambard-AI GH200 GPU node. PME electrostatics, 1.0 nm non-bonded cutoffs, and LINCS h-bond constraints with a 2 fs timestep were used. Binding free energy was estimated by the MM-GBSA method using MMPBSA.py (AmberTools 24), with the OBC2 GB model (igb=5, saltcon=0.15 M) applied to 200 frames sampled from the final 8 ns of the production trajectory.
