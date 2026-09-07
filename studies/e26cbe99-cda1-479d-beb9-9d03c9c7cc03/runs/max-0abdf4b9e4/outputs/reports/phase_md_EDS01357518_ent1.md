# Phase Report: MD Trajectory — EDS01357518_ent1 / CRBN Pocket

**Run:** PB-20260904-MD-EDS01357518ent1
**Date:** 2026-09-04
**Task:** 10 ns NPT MD simulation of EDS01357518 ent1 in the CRBN pocket (Isambard-AI_HPC job 6300385)
**Status:** MD complete — trajectory returned; MM-GBSA pending

---

## Context

EDS01357518 (ent1) is one of two enantiomers of compound EDS01357518 carried forward for MD-refined binding energy estimation. The companion ent2 run was submitted in the same batch (job 6300401). This phase covers only the GROMACS MD steps; solvent stripping and MMPBSA.py analysis are a separate downstream phase.

The protocol and system preparation are identical to the previously completed EDS01806218_ent2 run (job 6294174), which established the working recipe for this target.

---

## System

| Property | Value |
|:---------|:------|
| System | 142-residue CRBN pocket + EDS01357518_ent1 + TIP3P water + counter-ions |
| Total atoms | 29,232 |
| Force field (protein) | ff14SB (via tleap, converted to GROMACS topology) |
| Force field (ligand) | GAFF2, AM1-BCC charges (sqm) |
| Water model | TIP3P |
| Cluster | Isambard-AI_HPC (GH200, aarch64) |
| GROMACS binary | `/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/bin/gmx_mpi` |

---

## Protocol

Three sequential stages, identical to the EDS01806218_ent2 recipe:

| Stage | Duration | Key settings |
|:------|:---------|:-------------|
| Energy minimisation | steepest descent until Fmax < 1000 kJ/mol/nm | `-pme cpu` |
| NPT equilibration | 200 ps | Parrinello–Rahman barostat, V-rescale thermostat |
| NPT production | 10 ns, 1001 frames at 10 ps intervals | `-pme gpu`, `-ntomp 8`, `-nb gpu` |

Invocation (no MPI launcher; this build uses Open MPI, incompatible with Cray PMI srun):

```
gmx_mpi mdrun -v -deffnm em      -ntomp 8 -nb gpu -pme cpu
gmx_mpi mdrun -v -deffnm npt_eq  -ntomp 8 -nb gpu -pme gpu
gmx_mpi mdrun -v -deffnm npt_prod -ntomp 8 -nb gpu -pme gpu
```

---

## Performance

| Stage | Performance |
|:------|:------------|
| NPT equilibration | 193.3 ns/day (0.124 hr/ns) |
| NPT production | 185.1 ns/day (0.130 hr/ns) |

---

## Output Files

| File | Size | Description |
|:-----|-----:|:------------|
| `em.6300385.gro` | 1.3 MB | Energy-minimised structure |
| `npt_eq.6300385.gro` | 2.0 MB | Post-equilibration structure |
| `npt_prod.6300385.gro` | 2.0 MB | Final production frame |
| `npt_prod.6300385.xtc` | 103 MB | Production trajectory (1001 frames, 10 ps spacing) |
| `npt_prod.6300385.edr` | 670 KB | Energy time series |
| `md_EDS01357518_ent1/` | — | Input topology, MDP files, GAFF2 parameters, tleap inputs |

---

## Notes

- Net charge warning: system carries −0.001001 e (non-integer from GAFF2 AM1-BCC partial charges), triggering a GROMACS Ewald artefact WARNING. Same issue was present and accepted for EDS01806218_ent2.
- One water settle failure at step 29 of equilibration; GROMACS recovered automatically.

---

## Next Step

Run MM-GBSA on `npt_prod.6300385.xtc`:

1. Copy/link trajectory into `md_EDS01357518_ent1/` and update cpptraj input path.
2. Strip solvent (mask `:WAT,Cl-`) → `prod_nowater.nc`.
3. Run MMPBSA.py: OBC2 GB (igb=5), 0.15 M salt, startframe=200, endframe=1000, interval=4 (201 frames from final 8 ns).
4. Report ΔG_bind mean ± SD alongside EDS01806218_ent2 reference (−25.22 ± 5.82 kcal/mol).
