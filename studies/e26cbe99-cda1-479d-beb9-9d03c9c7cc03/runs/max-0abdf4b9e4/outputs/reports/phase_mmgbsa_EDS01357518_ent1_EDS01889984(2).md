# Phase Report: MM-GBSA — EDS01357518_ent1 and EDS01889984 / CRBN Pocket

**Date:** 2026-09-04
**Status:** Complete (EDS01889984 reliable; EDS01357518_ent1 flagged unreliable)

---

## Context

Following the successful MM-GBSA analysis of EDS01806218_ent2 (job 6294174, ΔG = −25.22 kcal/mol), the same protocol was applied to the two remaining compounds whose 10 ns NPT trajectories were present in session:

- **EDS01357518_ent1** — trajectory from Isambard job 6300385 (`npt_prod.6300385.xtc`, 103 MB, 1001 frames)
- **EDS01889984** — trajectory from Isambard job 6304913 (`npt_prod.6304913.xtc`, 103 MB, 1001 frames)

---

## Methods

### Solvent stripping (cpptraj)

Both trajectories were stripped with cpptraj using the solvated topology (`complex.prmtop`) and mask `:WAT,Cl-`.

| Property | EDS01357518_ent1 | EDS01889984 |
|:---------|:----------------:|:-----------:|
| Input frames | 1001 | 1001 |
| Frames processed | 1001 | 1001 |
| Stripped atoms retained | 2326 | 2326 |
| Output (NetCDF) | `md_EDS01357518_ent1/prod_nowater.nc` (28.0 MB) | `md_EDS01889984/prod_nowater.nc` (28.0 MB) |
| Throughput | 805 frames/s | 902 frames/s |

### MM-GBSA (MMPBSA.py v14.0)

Both analyses ran in parallel with `AMBERHOME=/home/ubuntu/rayca-runtime/.mamba/envs/rayca`.

| Parameter | Value |
|:----------|:------|
| Frames analysed | 201 (startframe=200, endframe=1000, interval=4 — last 8 ns) |
| GB model | OBC2 (igb=5) |
| Salt concentration | 0.15 M NaCl |
| Surface area | LCPO |
| Protocol | Single-trajectory (complex, receptor, ligand from same frames) |
| Entropy | Off |

---

## Results

### EDS01889984

| Component | Average (kcal/mol) | SD | SEM |
|:----------|-------------------:|---:|----:|
| VDWAALS (Δ) | −35.50 | 2.50 | 0.18 |
| EEL (Δ) | −12.98 | 6.31 | 0.45 |
| EGB (Δ) | +28.39 | 5.82 | 0.41 |
| ESURF (Δ) | −3.71 | 0.22 | 0.02 |
| **DELTA TOTAL** | **−23.80** | **2.64** | **0.19** |

Result is well-converged (SD/mean = 11%, SEM = 0.19 kcal/mol). Absolute VDW terms for complex (~−1013 kcal/mol) and receptor (~−973 kcal/mol) are physically normal.

### EDS01357518_ent1 — FLAGGED UNRELIABLE

| Component | Average (kcal/mol) | SD | SEM |
|:----------|-------------------:|---:|----:|
| VDWAALS (Δ) | +14.92 | 55.60 | 3.92 |
| EEL (Δ) | −17.97 | 10.94 | 0.77 |
| EGB (Δ) | +75.03 | 11.09 | 0.78 |
| ESURF (Δ) | −3.82 | 0.34 | 0.02 |
| **DELTA TOTAL** | **+68.17** | **57.57** | **4.06** |

**This result should not be used.** Two indicators of a topology defect:

1. **Unphysical absolute VDW energies** — complex VDWAALS = +368,312 kcal/mol (should be ~ −1000 kcal/mol for a stable complex). The receptor block is normal (−965 kcal/mol); the anomaly is concentrated in the complex and the isolated-ligand evaluations, suggesting a 1-4 VDW or exclusion-list error in the GAFF2 parameterisation of this ligand.
2. **GROMACS topology warning** — `slurm-6300385.log` reports `WARNING: Listed nonbonded interaction between particles 944 and 946`, indicating two bonded atoms are erroneously included in the non-bonded pair list. The same warning appears in the EDS01357518_ent2 log (job 6300401), confirming it is a systematic defect in the EDS01357518 ligand topology shared by both enantiomers.

The SD of 57.57 kcal/mol (84% of the mean) confirms extreme frame-to-frame instability in the MM energy evaluation. The DELTA TOTAL of +68 kcal/mol is the residual after imperfect cancellation of large erroneous terms and does not represent a physical binding free energy estimate.

---

## Summary Across All Five Compounds

| Compound | ΔG_bind (kcal/mol) | SD | SEM | Reliability | Source |
|:---------|-------------------:|---:|----:|:-----------:|:-------|
| EDS01806218_ent2 | −25.22 | 5.82 | 0.41 | ✓ | Job 6294174 |
| EDS01889984 | −23.80 | 2.64 | 0.19 | ✓ | Job 6304913 |
| EDS01357518_ent1 | +68.17 | 57.57 | 4.06 | ✗ topology defect | Job 6300385 |
| EDS01357518_ent2 | — | — | — | pending | Re-run job 6307560 |
| EDS01806218_ent1 | — | — | — | pending | Re-run job 6307571 |

---

## Troubleshooting Notes

1. **AMBERHOME not set** — `MMPBSA.py` failed on first invocation with `TypeError: expected str, bytes or os.PathLike object, not NoneType` because `os.getenv('AMBERHOME')` returned `None`. Fixed by setting `AMBERHOME=/home/ubuntu/rayca-runtime/.mamba/envs/rayca` (where `spc.xvv` was confirmed to exist at `dat/mmpbsa/spc.xvv`).
2. **Parallel execution** — both MMPBSA.py calls ran concurrently via `threading.Thread`; no resource conflicts observed.

---

## Files Produced

| File | Description |
|:-----|:------------|
| `md_EDS01357518_ent1/prod_nowater.nc` (28.0 MB) | Stripped trajectory |
| `md_EDS01357518_ent1/cpptraj_strip.in` | cpptraj input |
| `md_EDS01357518_ent1/mmpbsa_results.dat` | MM-GBSA summary (unreliable) |
| `md_EDS01357518_ent1/mmpbsa_decomp.dat` | Per-residue decomposition (unreliable) |
| `md_EDS01889984/prod_nowater.nc` (28.0 MB) | Stripped trajectory |
| `md_EDS01889984/cpptraj_strip.in` | cpptraj input |
| `md_EDS01889984/mmpbsa_results.dat` | MM-GBSA summary |
| `md_EDS01889984/mmpbsa_decomp.dat` | Per-residue decomposition |

---

## Verification

| Check | Status | Evidence |
|:------|:------:|:---------|
| cpptraj EDS01357518_ent1: 1001 frames read and processed | PASS | stdout: "Read 1001 frames and processed 1001 frames" |
| cpptraj EDS01889984: 1001 frames read and processed | PASS | stdout: "Read 1001 frames and processed 1001 frames" |
| Stripped atom count consistent with prior runs | PASS | 2326 atoms (= 2265 receptor + 61 ligand), same as EDS01806218_ent2 |
| `prod_nowater.nc` written — EDS01357518_ent1 | PASS | 28.0 MB |
| `prod_nowater.nc` written — EDS01889984 | PASS | 28.0 MB |
| MMPBSA.py completed without error — EDS01357518_ent1 | PASS | rc=0 |
| MMPBSA.py completed without error — EDS01889984 | PASS | rc=0 |
| 201 frames analysed (startframe=200, interval=4) | PASS | both runs report "201.0 complex frames" |
| Internal energy differences (BOND/ANGLE/DIHED) cancel | PASS | single-trajectory protocol; Δ = 0.0000 kcal/mol |
| EDS01889984 absolute VDW physically plausible | PASS | complex VDWAALS ~ −1013 kcal/mol (normal range) |
| EDS01357518_ent1 absolute VDW physically plausible | FAIL | complex VDWAALS = +368,312 kcal/mol — unphysical; result flagged unreliable |
| EDS01889984 SD acceptable relative to mean | PASS | SD = 2.64 kcal/mol (11% of mean) |
| EDS01357518_ent1 SD acceptable relative to mean | FAIL | SD = 57.57 kcal/mol (84% of mean) — confirms instability |

---

## Known Limitations

- MM-GBSA does not include conformational entropy; true ΔG_bind is less negative.
- EDS01357518_ent1 result is physically meaningless due to the topology defect; the EDS01357518 series requires re-parameterisation before MM-GBSA can be trusted.
- The EDS01889984 result (SD = 2.64 kcal/mol) is better converged than EDS01806218_ent2 (SD = 5.82), but 8 ns of production sampling remains limited.

---

## Methods Paragraph (for manuscript — EDS01889984 only)

Binding free energy of EDS01889984 was estimated by the MM-GBSA method. The 10 ns production trajectory (1001 frames at 10 ps intervals) was stripped of solvent and counter-ions with cpptraj (AmberTools 24). MMPBSA.py (v14.0) was applied to 201 frames sampled from the final 8 ns (frames 200–1000, every 4th frame), using the OBC2 GB model (igb=5) and 0.15 M salt concentration. The reported ΔG_bind = −23.80 ± 2.64 kcal/mol (mean ± SD; SEM = 0.19 kcal/mol).
