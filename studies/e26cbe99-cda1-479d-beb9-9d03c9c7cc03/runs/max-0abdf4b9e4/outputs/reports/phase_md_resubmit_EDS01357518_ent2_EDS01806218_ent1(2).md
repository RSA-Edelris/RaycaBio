# Phase Report: MD Re-submission — EDS01357518_ent2 and EDS01806218_ent1

**Date:** 2026-09-04
**Status:** Jobs submitted; awaiting completion

---

## Context

Trajectories for EDS01357518_ent2 (Isambard job 6300401) and EDS01806218_ent1 (job 6300420) completed on 2026-09-04 but were not returned with job-numbered filenames. Both ran in the shared working directory `max-e5315dba0f`, which was subsequently cleaned from Isambard scratch before the trajectories could be recovered. Re-submission is required.

---

## Re-submission

Both jobs were submitted to Isambard-AI_HPC on 2026-09-04 with identical protocol to all prior compound runs.

| Property | EDS01357518_ent2 | EDS01806218_ent1 |
|:---------|:----------------:|:----------------:|
| Cluster job | **6307560** | **6307571** |
| Run ID | max-e50b1dcbb3 | max-e50b1dcbb3 |
| CPUs / GPUs | 8 / 1 | 8 / 1 |
| Walltime requested | 120 min | 120 min |

### Protocol (identical to prior runs)

```
gmx_mpi grompp -f em.mdp      -c complex.gro  -p complex.top -n index.ndx -o em.tpr     -maxwarn 5
gmx_mpi mdrun  -v -deffnm em      -ntomp 8 -nb gpu -pme cpu

gmx_mpi grompp -f npt_eq.mdp  -c em.gro       -p complex.top -n index.ndx -o npt_eq.tpr -maxwarn 5
gmx_mpi mdrun  -v -deffnm npt_eq  -ntomp 8 -nb gpu -pme gpu

gmx_mpi grompp -f prod.mdp    -c npt_eq.gro   -p complex.top -n index.ndx -o npt_prod.tpr -maxwarn 5
gmx_mpi mdrun  -v -deffnm npt_prod -ntomp 8 -nb gpu -pme gpu
```

GROMACS 2026.1, `/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/bin/gmx_mpi`, 1 GH200 GPU.

### Expected outputs (returned with compound-named filenames)

| File | Description |
|:-----|:------------|
| `em.<compound>.gro` | Energy-minimised structure |
| `npt_eq.<compound>.gro` | Post-equilibration structure |
| `npt_prod.<compound>.gro` | Final production frame |
| `npt_prod.<compound>.xtc` | 10 ns trajectory (~103 MB, 1001 frames) |
| `npt_prod.<compound>.edr` | Energy file |

---

## Known Issue: EDS01357518 Ligand Topology Warning

Both EDS01357518 enantiomers carry a GROMACS warning: `Listed nonbonded interaction between particles 944 and 946`. This indicates two bonded atoms erroneously appear in the non-bonded pair list — a GAFF2 → GROMACS conversion artefact. The warning does not prevent the simulation from running (both previous runs completed 10 ns), but it corrupts the MMPBSA energy evaluation of the EDS01357518 compounds, yielding unphysical absolute VDW terms (+368,000 kcal/mol). The same defect will affect EDS01357518_ent2.

**Recommendation:** Before running MM-GBSA on EDS01357518_ent2, inspect the GAFF2 parameters and rebuild the ligand topology with corrected exclusions. The EDS01806218_ent1 topology does not carry this warning and is expected to yield a reliable MM-GBSA result.

---

## Reason for Trajectory Loss

Both jobs 6300401 and 6300420 completed successfully (confirmed via `slurm-6300401.log` and `slurm-6300420.log`: "5000000 steps, 10000.0 ps. Performance: ~190 ns/day. Done."). The working directory (`max-e5315dba0f`) was shared between multiple jobs in that batch and was cleaned from Isambard scratch before outputs could be re-collected. Future jobs write outputs with compound-named filenames to `$RAYCA_OUT` immediately upon job completion, preventing this loss.

---

## Verification

| Check | Status | Evidence |
|:------|:------:|:---------|
| Previous jobs confirmed complete before re-submission | PASS | `slurm-6300401.log` and `slurm-6300420.log` both end "5000000 steps, 10000.0 ps … Done." |
| Working directory confirmed absent from scratch | PASS | `ls /lus/lfs1aip2/scratch/u6sp/hpcuser.u6sp/rayca/max-e5315dba0f/npt_prod*.xtc` → No such file or directory (rc=2) |
| Prep files present for EDS01357518_ent2 re-run | PASS | `complex.gro`, `complex.top`, `em.tpr`, `npt_eq.mdp`, `prod.mdp`, `index.ndx` all confirmed in `md_EDS01357518_ent2/` |
| Prep files present for EDS01806218_ent1 re-run | PASS | same file set confirmed in `md_EDS01806218_ent1/` |
| EDS01357518_ent2 job accepted by scheduler | PASS | job ID 6307560, state=submitted |
| EDS01806218_ent1 job accepted by scheduler | PASS | job ID 6307571, state=submitted |
| Output filenames include compound name to prevent overwrite | PASS | script copies to `$RAYCA_OUT/npt_prod.<compound>.xtc` etc. |

---

## Next Step

When jobs 6307560 and 6307571 return:
1. Run cpptraj strip and MMPBSA.py on `npt_prod.EDS01806218_ent1.xtc` — expected to yield a reliable ΔG_bind.
2. Investigate and fix the EDS01357518 ligand topology before running MM-GBSA on `npt_prod.EDS01357518_ent2.xtc`.
