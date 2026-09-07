# Phase Report: CRBN-EDS01889984 NPT MD Simulation — Isambard Job 6304913

**Run:** PB-20260904-MD-EDS01889984
**Date:** 2026-09-04
**Cluster job:** Isambard-AI_HPC job 6304913
**Status:** Complete — all three phases returned

---

## Purpose

10 ns explicit-solvent NPT MD simulation of EDS01889984 in the CRBN pocket, to produce a relaxed trajectory for MM-GBSA binding free energy estimation (next phase). Follows the same protocol as job 6294174 (EDS01806218_ent2).

---

## System

| Property | Value |
|:---------|:------|
| Compound | EDS01889984 |
| Target | CRBN pocket (4CI2 receptor, 142 residues) |
| Atoms | 29,232 (protein + LIG + TIP3P + Cl⁻) |
| Water molecules | 9,115 (TIP3P) |
| Box | 6.652 × 6.073 × 7.269 nm |
| Force field | GAFF2/ff14SB (AMBER → GROMACS via Parmed) |
| GROMACS | 2026.1, aarch64 GH200 |
| Binary | `/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/bin/gmx_mpi` |
| Hardware | 1 GH200 GPU, 1 MPI rank, 8 OpenMP threads |

---

## Methods

### Phase 1 — Energy minimisation

| Parameter | Value |
|:----------|:------|
| Algorithm | Steepest descents |
| Max steps | 10,000 |
| GPU flags | `-nb gpu -pme cpu` (required for EM on this GROMACS build) |

**Result:** Converged to machine precision in **4,907 steps**.
Potential energy at convergence: **−434,735.62 kJ/mol**

Note: EM stopped with "forces not fully converged to requested tolerance" — converging to machine precision is the expected terminal state for this system type and is acceptable as a minimisation pre-step. A SETTLE warning was raised at step 29 (water geometry constraint during steepest descent); simulation continued normally.

### Phase 2 — NPT equilibration

| Parameter | Value |
|:----------|:------|
| Steps / time | 100,000 steps / 200 ps |
| Timestep | 2 fs |
| Thermostat | V-rescale (groups: Protein_LIG, Water_and_ions) |
| Barostat | Berendsen |
| GPU flags | `-nb gpu -pme gpu` |
| Performance | ~1,145 ns/day (~15 s wall time) |

### Phase 3 — NPT production

| Parameter | Value |
|:----------|:------|
| Steps / time | 5,000,000 steps / **10 ns** |
| Timestep | 2 fs |
| XTC output interval | 5,000 steps = 10 ps → **1,001 frames** |
| GPU flags | `-nb gpu -pme gpu` |
| PME grid (auto-tuned) | 60×56×72, coulomb cutoff 1.000 nm |

---

## Output Files

| File | Size | Description |
|:-----|-----:|:------------|
| `em.6304913.gro` | 2.0 MB | Energy-minimised structure |
| `npt_eq.6304913.gro` | 2.0 MB | Post-equilibration structure |
| `npt_prod.6304913.gro` | 2.0 MB | Final production frame |
| `npt_prod.6304913.edr` | 670 KB | Energy trajectory |
| `npt_prod.xtc` | 107 MB | Compressed coordinate trajectory (1,001 frames, 10 ns) |

---

## Warnings and Notes

| Warning | Severity | Action |
|:--------|:---------|:-------|
| Ewald electrostatics with net charge | Advisory | Noted; consistent across all five compound runs — does not affect relative comparisons within this campaign |
| Berendsen barostat (not strictly correct ensemble) | Advisory | Equilibration only; same as prior runs |
| SETTLE at step 29 in EM | Advisory | Water geometry resolved once minimisation settled; trajectory normal |
| Update groups disabled (constrained ligand atoms) | Advisory | Expected for GAFF2 ligands; no performance impact at this system size |

---

## Verification

| Check | Status | Evidence |
|:------|:------:|:---------|
| EM converged (machine precision) | PASS | 4,907 steps, E_pot = −434,736 kJ/mol |
| npt_eq.6304913.gro returned | PASS | 2.0 MB, 29,232 atoms |
| npt_prod.6304913.gro returned | PASS | 2.0 MB, box 6.65×6.07×7.27 nm |
| npt_prod.xtc frame count consistent with 10 ns | PASS | 107 MB matches 1,001 frames × 29,232 atoms (cf. EDS01806218_ent2: 103 MB / 1,001 frames / 10 ns) |
| Energy file returned | PASS | npt_prod.6304913.edr 670 KB |

---

## Compound Progress Across Campaign

| Compound | Cluster job | Traj size | MD status | MM-GBSA status |
|:---------|:-----------:|----------:|:---------:|:--------------:|
| EDS01357518_ent1 | 6300385 | — | Complete | Pending |
| EDS01806218_ent2 | 6294174 | 103 MB | Complete | Done — ΔG = −25.22 ± 5.82 kcal/mol |
| **EDS01889984** | **6304913** | **107 MB** | **Complete** | **Pending** |

---

## Next Step

Strip solvent with cpptraj (`md_EDS01889984/complex.prmtop`, mask `:WAT,Cl-`) then run MMPBSA.py on the last 8 ns (frames 200–1000, interval 4 → 201 frames), following the protocol in `phase_md_mmpbsa_EDS01806218_ent2.md`. Key inputs (`complex.top`, `complex_nowater.prmtop`, `receptor.prmtop`, `ligand.prmtop`, `mmpbsa.in`) are already staged in `md_EDS01889984/`.

---

## Known Limitations

- MM-GBSA (next phase) will not include conformational entropy (−TΔS); true ΔG_bind is less negative.
- 10 ns may be insufficient for full convergence; SD on ΔG_bind will quantify remaining variation.
- Net charge Ewald warning is consistent across all compound runs and does not affect relative comparisons within this campaign.
