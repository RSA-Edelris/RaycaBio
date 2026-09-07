# Audit: MD-Refined MM-GBSA — EDS01806218_ent2

**Date:** 2026-09-04
**Phase:** MM-GBSA analysis on 10 ns MD trajectory (job 6294174)

---

## Claims vs Evidence

| Claim | Evidence | Pass? |
|:------|:---------|:-----:|
| Cluster job 6294174 completed | `check_cluster_job` → state=done, scheduler_state=completed | PASS |
| Trajectory 1001 frames at 10 ps | `npt_prod.xtc` 103 MB; cpptraj stdout: "Read 1001 frames" | PASS |
| cpptraj stripped 26,927 solvent atoms | stdout: "Stripping 26,927 atoms; Stripped topology: 2326 atoms" | PASS |
| 201 frames analysed (last 8 ns) | MMPBSA.py stdout: "201.0 complex frames" | PASS |
| Internal energy differences cancel | BOND/ANGLE/DIHED Δ = 0.0000 kcal/mol in `mmpbsa_results.dat` | PASS |
| ΔG_bind = −25.22 kcal/mol | `mmpbsa_results.dat` line: "DELTA TOTAL −25.2231 5.8225 0.4107" | PASS |

---

## Failure History

| Job | Error | Fix |
|:----|:------|:----|
| 6284357 | `-ntmpi 1` not valid for MPI-compiled GROMACS | Use `mpirun`/`srun` launcher |
| 6292928 | `srun` launch failed at EM step | Switch to absolute `mpirun` path |
| 6293949 | `mpirun` not on PATH | Use absolute mpirun path found via `query_cluster` |
| 6294042 | `-pme gpu` not supported for steepest-descent integrator | Use `-pme cpu` for EM stage only |
| 6294174 | Succeeded — EM + 200 ps equil + 10 ns prod | — |

---

## Analysis Fixes

| Issue | Fix |
|:------|:----|
| `cpptraj_strip.in` pointed to `prod.xtc` (absent) | Updated to `npt_prod.xtc` (session root) |
| `mmpbsa.in` inline `!` comments broke integer parsing | Removed all inline comments |
| MMPBSA.py call used `-sp` (solvated topology) with pre-stripped trajectory | Removed `-sp`; use `-cp complex_nowater.prmtop` only |

---

## Verification

| Check | Status | Evidence |
|:------|:------:|:---------|
| Trajectory present and non-empty | PASS | `npt_prod.xtc` 103 MB, dated Sep 4 09:08 |
| cpptraj processed all 1001 frames | PASS | stdout: "Read 1001 frames and processed 1001 frames" |
| Stripped topology 2326 atoms (protein + LIG only) | PASS | cpptraj: "Stripped topology: 2326 atoms, 143 res" |
| `prod_nowater.nc` written non-empty | PASS | 28.0 MB on disk |
| MMPBSA.py exit code 0 | PASS | rc=0, stdout: "MMPBSA.py Finished!" |
| Frame count matches input spec (200–1000, interval 4) | PASS | MMPBSA.py stdout: "201 frames were processed by cpptraj" |
| BOND/ANGLE/DIHED differences cancel to zero | PASS | `mmpbsa_results.dat`: BOND Δ = 0.0000, ANGLE Δ = −0.0000, DIHED Δ = 0.0000 |
| ΔG_bind negative and physically plausible | PASS | DELTA TOTAL = −25.2231 ± 5.8225 kcal/mol |

---

## Known Limitations

- MM-GBSA does not account for conformational entropy (−TΔS); true ΔG_bind is less negative.
- 10 ns may be insufficient for full convergence on a flexible ligand; SD = 5.82 kcal/mol reflects conformational sampling variation.
- Single-point solvation model (OBC2); no explicit ion screening beyond Debye–Hückel.
- No per-residue decomposition analysis performed in this phase (file available: `mmpbsa_decomp.dat`).
