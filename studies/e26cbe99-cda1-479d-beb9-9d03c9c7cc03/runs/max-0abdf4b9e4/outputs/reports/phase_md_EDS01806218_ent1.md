# Phase Report: MD Trajectory — EDS01806218_ent1 / CRBN Pocket

**Run:** PB-20260904-MD-EDS01806218ent1  
**Date:** 2026-09-04  
**Cluster job:** Isambard-AI_HPC job 6319835  
**Status:** Complete

---

## Context

EDS01806218 ent1 (the (1R,2R) enantiomer) is one of four compounds carried forward for MD-refined binding energy estimation against the CRBN pocket of 4CI2. It is the companion enantiomer of EDS01806218_ent2, whose MD + MM-GBSA run (job 6294174, ΔG = −25.22 ± 5.82 kcal/mol) established the validated protocol for this campaign.

This job is the **third run attempt** for this compound:

| Attempt | Job | Outcome |
|:--------|:----|:--------|
| 1 | 6300420 | Completed on Isambard but working directory `max-e5315dba0f` was cleaned from scratch before outputs were retrieved — trajectory lost |
| 2 | 6307571 | Failed at step 1: `cp /rayca_inputs/md_EDS01806218_ent1/*` found no such directory — staging error |
| 3 | **6319835** | **Success** — outputs returned with compound-named filenames |

---

## System

| Property | Value |
|:---------|:------|
| Target | CRBN pocket (4CI2 receptor, 142-residue construct) |
| Ligand | EDS01806218 ent1 — (1R,2R) enantiomer |
| Force field | GAFF2 (ligand) + AMBER ff14SB (protein), TIP3P water |
| Total atoms | 29,241 |
| Final box dimensions | 6.647 × 6.069 × 7.264 nm |
| Engine | GROMACS 2026.1 (`gmx_mpi`), 1 GH200 GPU, 8 CPU cores |

Preparation files (topology, GAFF2 parameters, MDP inputs, index) were staged from `md_EDS01806218_ent1/` and are retained there for MM-GBSA input.

---

## Protocol

Three sequential stages, identical to the EDS01806218_ent2 validated recipe:

1. **Energy minimisation** — steepest descent, convergence criterion Fmax < 1000 kJ mol⁻¹ nm⁻¹
2. **NPT equilibration** — position-restrained, 300 K, 1 bar (Berendsen barostat)
3. **NPT production** — 10 ns, 300 K, 1 bar (Parrinello-Rahman barostat), 2 fs timestep, frames every 10 ps

```
gmx_mpi grompp -f em.mdp      -c complex.gro  -p complex.top -n index.ndx -o em.tpr     -maxwarn 5
gmx_mpi mdrun  -v -deffnm em      -ntomp 8 -nb gpu -pme cpu

gmx_mpi grompp -f npt_eq.mdp  -c em.gro       -p complex.top -n index.ndx -o npt_eq.tpr -maxwarn 5
gmx_mpi mdrun  -v -deffnm npt_eq  -ntomp 8 -nb gpu -pme gpu

gmx_mpi grompp -f prod.mdp    -c npt_eq.gro   -p complex.top -n index.ndx -o npt_prod.tpr -maxwarn 5
gmx_mpi mdrun  -v -deffnm npt_prod -ntomp 8 -nb gpu -pme gpu
```

**Performance:** ~902 ns/day (GH200 GPU, 29,241-atom system)

---

## Outputs

| File | Size | Description |
|:-----|:-----|:------------|
| `em_EDS01806218_ent1.gro` | 1.3 MB | Energy-minimised structure |
| `npt_eq_EDS01806218_ent1.gro` | 2.0 MB | Post-equilibration structure |
| `npt_prod_EDS01806218_ent1.gro` | 2.0 MB | Final production frame |
| `npt_prod_EDS01806218_ent1.xtc` | 103 MB (107,205,948 bytes) | Production trajectory, 1001 frames, 10 ps spacing |
| `npt_prod_EDS01806218_ent1.edr` | 670 KB | Energy time series |

All files are in the session root directory.

---

## Warnings

**WARNING 1 — Net charge Ewald artefact (advisory, consistent):**  
`You are using Ewald electrostatics in a system with net charge.`  
Consistent across all five compound runs in this campaign. Does not affect relative comparisons within the series; noted per Kastenholz & Hünenberger (2006).

**WARNING 2 — Listed nonbonded interaction (requires action before MM-GBSA):**  
```
WARNING: Listed nonbonded interaction between particles 944 and 946
WARNING: Listed nonbonded interaction between particles 943 and 949
```
These indicate two pairs of bonded atoms that appear erroneously in the non-bonded pair list — a GAFF2 → GROMACS topology conversion artefact. **This warning was not expected for EDS01806218_ent1**: the prior re-submission phase report (`phase_md_resubmit_EDS01357518_ent2_EDS01806218_ent1.md`) stated "The EDS01806218_ent1 topology does not carry this warning." The log confirms it does.

For EDS01357518 (both enantiomers), this same artefact yielded unphysical absolute VDW terms of +368,000 kcal/mol in MM-GBSA. The same outcome is likely for EDS01806218_ent1 unless the topology is corrected before the energy evaluation.

**Required action:** Inspect the GAFF2 parameters for EDS01806218_ent1, identify the offending bond/angle exclusion, and rebuild the ligand topology with corrected non-bonded exclusions before running MMPBSA.py.

---

## Verification

| Check | Status | Evidence |
|:------|:------:|:---------|
| Job accepted by scheduler | PASS | job ID 6319835, state=submitted |
| Slurm header confirms correct compound | PASS | `=== CRBN-EDS01806218_ent1 MD run ===` |
| EM structure returned | PASS | `em_EDS01806218_ent1.gro` 1.3 MB |
| NPT_eq structure returned | PASS | `npt_eq_EDS01806218_ent1.gro` 2.0 MB |
| Production GRO returned | PASS | `npt_prod_EDS01806218_ent1.gro` 2.0 MB, 29,241 atoms, box 6.65 × 6.07 × 7.26 nm |
| Production XTC returned | PASS | 103 MB — consistent with 1,001 frames × 29,241 atoms (cf. EDS01806218_ent2: 103 MB / 1,001 frames) |
| Energy file returned | PASS | `npt_prod_EDS01806218_ent1.edr` 670 KB |
| Trajectory loss prevented | PASS | Outputs written with compound-named filenames to `$RAYCA_OUT`; previous loss was due to unnamed outputs in a shared working directory |

---

## Next Step

Before running MM-GBSA:

1. Inspect `md_EDS01806218_ent1/ligand.frcmod` and `ligand.mol2` to identify which atoms correspond to particles 944/946 and 943/949 in the GROMACS numbering.
2. Rebuild the ligand topology (tleap → GROMACS conversion) with corrected 1-4 exclusions.
3. Re-check that the "Listed nonbonded interaction" warning is absent from a test `gmx grompp` call before submitting to MM-GBSA.
4. Once clean, run cpptraj strip and MMPBSA.py on `npt_prod_EDS01806218_ent1.xtc` following the validated EDS01806218_ent2 pipeline. Compare ΔG_bind with the ent2 reference of −25.22 ± 5.82 kcal/mol.
