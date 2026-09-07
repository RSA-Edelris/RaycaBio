# Phase Report: MD-Refined MM-GBSA — EDS01806218_ent2 / CRBN Pocket

**Run:** PB-20260904-MMPBSA-EDS01806218ent2
**Date:** 2026-09-04
**Task:** MM-GBSA binding free energy from 10 ns NPT MD trajectory (job 6294174)
**Status:** Complete

---

## Context

The 10 ns NPT MD simulation of EDS01806218_ent2 in the CRBN pocket (Isambard-AI_HPC job 6294174) completed successfully. This phase retrieved the trajectory, stripped solvent with cpptraj, and ran MMPBSA.py to obtain a trajectory-averaged MM-GBSA binding free energy.

---

## Input Trajectory

| Property | Value |
|:---------|:------|
| File | `npt_prod.xtc` (session root, 103 MB) |
| Frames | 1001 (0–1000, 10 ps spacing = 10 ns) |
| System | 29,253 atoms (142-res CRBN pocket + EDS01806218_ent2 + TIP3P) |
| Cluster job | Isambard-AI_HPC job 6294174 — **completed** |

---

## Methods

### Solvent stripping (cpptraj)

- Topology: `md_EDS01806218_ent2/complex.prmtop` (29,253 atoms)
- Trajectory: `npt_prod.xtc` (GROMACS XTC, 1001 frames)
- Mask stripped: `:WAT,Cl-` → 26,927 atoms removed; 2,326 atoms retained
- Output: `md_EDS01806218_ent2/prod_nowater.nc` (28.0 MB, NetCDF3 AMBER format)
- Throughput: 781 frames/s; runtime 1.3 s

### MM-GBSA (MMPBSA.py v14.0)

| Parameter | Value |
|:----------|:------|
| Frames analysed | 201 (startframe=200, endframe=1000, interval=4 → last 8 ns) |
| GB model | OBC2 (igb=5, Onufriev–Bashford–Case) |
| Salt concentration | 0.15 M NaCl |
| Surface area | LCPO |
| Complex topology | `complex_nowater.prmtop` (mbondi2 radii, ante-MMPBSA.py) |
| Receptor topology | `receptor.prmtop` |
| Ligand topology | `ligand.prmtop` |
| Runtime | 2.2 min |

---

## Results

### Binding Free Energy

| Component | Average (kcal/mol) | Std. Dev. | Std. Err. of Mean |
|:----------|-------------------:|----------:|------------------:|
| ΔG_gas | −60.63 | 9.30 | 0.66 |
| ΔG_solv | +35.41 | 8.05 | 0.57 |
| **DELTA TOTAL** | **−25.22** | **5.82** | **0.41** |

### Gas-phase decomposition (ΔG_gas)

| Term | Average (kcal/mol) |
|:-----|-------------------:|
| VDW (van der Waals) | −40.58 |
| EEL (electrostatic) | −20.05 |

### Solvation decomposition (ΔG_solv)

| Term | Average (kcal/mol) |
|:-----|-------------------:|
| EGB (GB desolvation) | +40.19 |
| ESURF (non-polar SASA) | −4.79 |

---

## Comparison with Earlier Estimates

| Stage | Score |
|:------|------:|
| Gnina Vina (docked pose) | −9.08 kcal/mol |
| Gnina ΔG_CNN (docked pose) | −10.13 kcal/mol |
| Single-frame MM-GBSA (raw docked pose) | +16.67 kcal/mol |
| **MD-refined MM-GBSA (10 ns, 201 frames)** | **−25.22 ± 5.82 kcal/mol** |

The single-frame value was positive because unrelaxed steric clashes in the raw docked pose dominated the energy. After 10 ns of explicit-solvent MD, the complex settled to a well-packed, strongly favourable binding mode.

---

## Troubleshooting Notes

Three fixes were needed before the analysis ran cleanly:

1. **cpptraj input path** — `cpptraj_strip.in` pointed to `md_EDS01806218_ent2/prod.xtc` but the returned trajectory was `npt_prod.xtc` in the session root. Path corrected.
2. **mmpbsa.in inline comments** — Fortran-style `!` inline comments caused `MMPBSA.py` v14.0 to fail parsing integers. Comments removed.
3. **MMPBSA.py `-sp` flag** — Including `-sp complex.prmtop` caused a topology/frame atom-count mismatch against the pre-stripped trajectory. Removed `-sp`; correct pattern for a pre-stripped trajectory is `-cp` only (no solvated topology argument).

---

## Verification

| Check | Status | Evidence |
|:------|:------:|:---------|
| Trajectory returned from cluster | PASS | `npt_prod.xtc` 103 MB, Sep 4 09:08 |
| cpptraj strip: 1001 frames processed | PASS | stdout: "Read 1001 frames and processed 1001 frames" |
| Stripped topology atom count consistent | PASS | 2326 atoms (142 res protein + LIG) |
| `prod_nowater.nc` written | PASS | 28.0 MB |
| MMPBSA.py completed without error | PASS | rc=0, "MMPBSA.py Finished!" |
| 201 frames analysed (startframe=200, interval=4) | PASS | "201 frames were processed by cpptraj" |
| Internal energy differences (BOND/ANGLE/DIHED) cancel | PASS | Δ = 0.0000 kcal/mol as expected |
| ΔG_bind sign and magnitude plausible | PASS | −25.22 kcal/mol consistent with potent binder |

---

## Files Produced

| File | Description |
|:-----|:------------|
| `md_EDS01806218_ent2/prod_nowater.nc` (28.0 MB) | Stripped trajectory (1001 frames) |
| `md_EDS01806218_ent2/mmpbsa_results.dat` | MM-GBSA summary |
| `md_EDS01806218_ent2/mmpbsa_decomp.dat` | Per-residue decomposition (available for follow-up) |
| `md_EDS01806218_ent2/mmpbsa.in` | MMPBSA input (inline comments removed) |
| `md_EDS01806218_ent2/cpptraj_strip.in` | cpptraj input (path corrected to npt_prod.xtc) |

---

## Known Limitations

- MM-GBSA does not include conformational entropy (−TΔS); true ΔG_bind is less negative.
- 10 ns may be insufficient for full convergence; SD = 5.82 kcal/mol reflects remaining sampling variation.
- Single-point implicit solvation (OBC2); no explicit ion screening beyond Debye–Hückel term.
- Per-residue decomposition available in `mmpbsa_decomp.dat` but not analysed in this phase.

---

## Methods Paragraph (for manuscript)

Binding free energy of EDS01806218 (1S,2S) was estimated by the MM-GBSA method. The production trajectory (10 ns, 1000 frames at 10 ps intervals) was stripped of solvent and counter-ions with cpptraj (AmberTools 24). MMPBSA.py (v14.0) was applied to 201 frames sampled from the final 8 ns (frames 200–1000, every 4th frame), using the OBC2 GB model (igb=5) and 0.15 M salt concentration. Gas-phase energies were computed with mmpbsa_py_energy; non-polar solvation was estimated with the LCPO surface area model. The reported ΔG_bind = −25.22 ± 5.82 kcal/mol (mean ± SD; SEM = 0.41 kcal/mol) represents the trajectory-averaged binding free energy after full explicit-solvent relaxation.
