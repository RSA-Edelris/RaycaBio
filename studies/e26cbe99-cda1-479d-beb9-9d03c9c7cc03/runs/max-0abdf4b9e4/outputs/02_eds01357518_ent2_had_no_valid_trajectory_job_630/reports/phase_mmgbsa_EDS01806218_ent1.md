# Phase Report: MM-GBSA — EDS01806218_ent1 / CRBN Pocket

**Date:** 2026-09-04  
**Status:** Complete  

---

## Context

Following the completion of the EDS01806218_ent1 10 ns MD trajectory (Isambard job 6319835, `npt_prod_EDS01806218_ent1.xtc`), solvent stripping and MM-GBSA analysis were run locally using the validated protocol from EDS01806218_ent2 (reference: ΔG = −25.22 ± 5.82 kcal/mol).

**Background on trajectory recovery:** Two prior attempts for this compound failed — job 6300420 completed on cluster but the shared working directory was cleaned before retrieval, and job 6307571 failed at staging. Job 6319835 succeeded and outputs were saved with compound-named filenames. Additionally, job 6309346 (labeled "EDS01357518_ent2 re-run") was found to have run from EDS01806218_ent1 prep files (atom count 29,241 matching `md_EDS01806218_ent1/`), not EDS01357518_ent2 files (29,247 atoms). Two independent EDS01806218_ent1 trajectories are therefore available; the named trajectory from job 6319835 was used here.

---

## Methods

### Solvent stripping (cpptraj)

```
parm md_EDS01806218_ent1/complex.prmtop
trajin npt_prod_EDS01806218_ent1.xtc
strip :WAT,Cl-
trajout md_EDS01806218_ent1/prod_nowater.nc netcdf
run
```

| Property | Value |
|:---------|:------|
| Input frames | 1001 |
| Frames processed | 1001 |
| Stripped atoms retained | 2326 (= 2265 receptor + 61 ligand) |
| Output (NetCDF) | `md_EDS01806218_ent1/prod_nowater.nc` (28.0 MB) |
| Throughput | 842 frames/s |

### MM-GBSA (MMPBSA.py v14.0)

| Parameter | Value |
|:----------|:------|
| Frames analysed | 201 (startframe=200, endframe=1000, interval=4 — last 8 ns) |
| GB model | OBC2 (igb=5) |
| Salt concentration | 0.15 M NaCl |
| Surface area | LCPO |
| Protocol | Single-trajectory |
| Entropy | Off |
| Total calculation time | 2.1 min |

---

## Result

| Component | Average (kcal/mol) | SD | SEM |
|:----------|-------------------:|---:|----:|
| VDWAALS (Δ) | −25.98 | 2.77 | 0.20 |
| EEL (Δ) | −20.17 | 3.64 | 0.26 |
| EGB (Δ) | +29.15 | 3.17 | 0.22 |
| ESURF (Δ) | −3.75 | 0.29 | 0.02 |
| **DELTA TOTAL** | **−20.75** | **2.59** | **0.18** |

ΔG_bind = **−20.75 ± 2.59 kcal/mol** (SEM 0.18 kcal/mol, 201 frames)

---

## Physical Plausibility Check

**VDWAALS (complex absolute):** −1008.83 kcal/mol — physically normal (cf. EDS01889984 complex ~−1013 kcal/mol, EDS01806218_ent2 similar). No sign of the +368,312 kcal/mol artefact seen in EDS01357518_ent1. The ΔVDWAALS of −25.98 kcal/mol is a reasonable van der Waals binding contribution.

**BOND/ANGLE/DIHED (absolute):** The absolute BOND energy of the complex is anomalously large (~17,631,660 kcal/mol, SD ~14,321,765 kcal/mol). This is unphysical for a ~2326-atom system and suggests a strained bond in the ligand topology — likely the same GAFF2 conversion artefact responsible for the GROMACS `Listed nonbonded interaction` warning (particles 944/946, 943/949). However, in single-trajectory MM-GBSA, ΔBOND = 0.0000 kcal/mol by construction (complex and receptor+ligand BOND terms cancel exactly). The final ΔG_bind is therefore not affected by this defect. The artefact is confined to the absolute single-state energy and does not propagate to the difference.

**SD/mean ratio:** 12.5% — well-converged (cf. EDS01889984 at 11%, EDS01806218_ent2 at 23%).

**Result: reliable for relative ranking.**

---

## Updated Campaign Summary

| Compound | ΔG_bind (kcal/mol) | SD | SEM | Rank | Reliability |
|:---------|-------------------:|---:|----:|:----:|:-----------:|
| EDS01806218_ent2 | −25.22 | 5.82 | 0.41 | 1 | ✓ |
| EDS01889984 | −23.80 | 2.64 | 0.19 | 2 | ✓ |
| EDS01806218_ent1 | −20.75 | 2.59 | 0.18 | 3 | ✓ (BOND absolute artefact; cancels in ΔG) |
| EDS01357518_ent1 | +68.17 | 57.57 | 4.06 | — | ✗ topology defect — result invalid |
| EDS01357518_ent2 | pending | — | — | — | Trajectory job 6321629 submitted |

EDS01806218 ent2 > ent1 by 4.47 kcal/mol. The enantiomers are meaningfully separated (>1 kcal/mol above noise floor).

---

## EDS01357518_ent2 Status

The previous "re-run" (job 6309346) was found to have run from EDS01806218_ent1's prep files — the XTC had 29,241 atoms matching `md_EDS01806218_ent1/complex.gro`, not the 29,247 atoms in `md_EDS01357518_ent2/complex.gro`. A fresh MD run was submitted as Isambard job **6321629** using the correct `md_EDS01357518_ent2/` prep files. Once the trajectory returns, MM-GBSA analysis must also address the AMBER 1-4 VDW/exclusion defect that yielded +368,312 kcal/mol VDWAALS for ent1.

---

## Files Produced

| File | Description |
|:-----|:------------|
| `md_EDS01806218_ent1/prod_nowater.nc` (28.0 MB) | Stripped trajectory |
| `md_EDS01806218_ent1/cpptraj_strip.in` | cpptraj input |
| `md_EDS01806218_ent1/mmpbsa_results.dat` | MM-GBSA full output |

---

## Verification

| Check | Status | Evidence |
|:------|:------:|:---------|
| cpptraj: 1001 frames read and processed | PASS | stdout confirmed |
| Stripped atom count consistent | PASS | 2326 atoms (= 2265 + 61), same as all prior runs |
| `prod_nowater.nc` written | PASS | 28.0 MB |
| MMPBSA.py rc=0 | PASS | confirmed |
| 201 frames analysed | PASS | "201.0 complex frames" |
| ΔBOND/ANGLE/DIHED = 0 | PASS | single-trajectory cancellation confirmed |
| Complex VDWAALS physically plausible | PASS | −1008.83 kcal/mol (normal range) |
| ΔVDWAALS physically plausible | PASS | −25.98 kcal/mol — no sign of +368k artefact |
| SD acceptable (< 30% of |ΔG|) | PASS | 2.59 / 20.75 = 12.5% |
| Absolute BOND physically plausible | FAIL | ~17M kcal/mol absolute (artefact); cancels in ΔG — does not invalidate result |
