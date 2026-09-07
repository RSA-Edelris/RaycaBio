## Overview

**Run:** PB-20260904-CRBN-MD-4cpds  
**Date:** 2026-09-04  
**Task:** Prepare and submit 10 ns NPT MD + MM-GBSA pipeline for four CRBN-pocket ligands; same protocol as EDS01806218_ent2 (job 6294174, ΔG = −25.22 kcal/mol).  
**Status:** Cluster jobs submitted — awaiting trajectory results

---

## Compounds

| Compound ID | Stereo note | Cluster job |
|:------------|:------------|------------:|
| EDS01357518_ent1 | (1R,2R) enantiomer | 6300385 |
| EDS01357518_ent2 | (1S,2S) enantiomer | 6300401 |
| EDS01806218_ent1 | (1R,2R) enantiomer | 6300420 |
| EDS01889984 | single stereoisomer | 6300478 |

All four submitted to Isambard-AI_HPC (GH200, aarch64), 1 GPU, 8 CPUs, 120 min walltime.

---

## System Preparation Protocol

Each compound followed identical steps:

### 1. Ligand parameterisation (GAFF2 / AM1-BCC)

| Step | Tool | Output |
|:-----|:-----|:-------|
| Add hydrogens, generate 3D | RDKit/OpenBabel | `ligand_h.sdf` |
| GAFF2 atom types + AM1-BCC charges | `antechamber -at gaff2 -c bcc` | `ligand.mol2` |
| Missing torsion/VdW parameters | `parmchk2 -s gaff2` | `ligand.frcmod` |

### 2. Solvated complex (tleap)

- Protein force field: ff14SB  
- Water: TIP3P  
- Solvation padding: 12 Å octahedral box  
- Counter-ions: Cl⁻ to neutralise  
- Output: `complex.prmtop`, `complex.inpcrd`

Atom counts (approximate, all similar):

| Compound | Total atoms |
|:---------|------------:|
| EDS01357518_ent1 | ~29,232 |
| EDS01357518_ent2 | ~29,247 |
| EDS01806218_ent1 | ~29,235 |
| EDS01889984 | ~29,248 |

### 3. GROMACS topology conversion (parmed)

`parmed` converted AMBER `.prmtop`/`.inpcrd` → `complex.top` + `complex.gro`.

### 4. Index file (gmx make_ndx)

Custom groups added:
- Group 18 `Protein_LIG` = groups 1 | 13 (protein + LIG)
- Group 19 `Water_and_ions` = groups 15 | 14

LIG confirmed as group 13 in all four systems.

### 5. MDP files

Identical to EDS01806218_ent2 (validated):

| Stage | File | Key settings |
|:------|:-----|:-------------|
| Energy minimisation | `em.mdp` | steepest descent, 50,000 steps, `-pme cpu` required |
| NPT equilibration | `npt_eq.mdp` | 200 ps, Berendsen barostat, 2 fs dt |
| NPT production | `prod.mdp` | 10 ns, Parrinello-Rahman, PME, LINCS h-bonds |

### 6. grompp validation

All 4 `em.tpr` files built without fatal errors (`-maxwarn 5`). This confirms topology + coordinate consistency before committing to cluster time.

### 7. ante-MMPBSA.py (stripped topologies)

`ante-MMPBSA.py` with mbondi2 radii produced:

| File | Purpose |
|:-----|:--------|
| `complex_nowater.prmtop` | Dry complex for MM-GBSA `-cp` |
| `receptor.prmtop` | Receptor only for MM-GBSA `-rp` |
| `ligand.prmtop` | Ligand only for MM-GBSA `-lp` |

Strip mask: `:WAT,Cl-`. This pre-stripped workflow (no `-sp` solvated topology at MMPBSA.py invocation time) is the pattern validated on EDS01806218_ent2.

---

## Cluster Submission Script (per compound)

```bash
GMX=/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/bin/gmx_mpi
MPIRUN=/tools/brics/apps/linux-sles15-neoverse_v2/gcc-12.3.0/\
  openmpi-4.1.7-gha3th46s7fr2ht3icsuhthmysvvlpgh/bin/mpirun

# EM — pme cpu required for steepest descent
$GMX grompp -f em.mdp -c complex.gro -p complex.top -n index.ndx -o em.tpr -maxwarn 5
$MPIRUN -n 1 $GMX mdrun -v -deffnm em -ntomp 8 -nb gpu -pme cpu

# NPT eq
$GMX grompp -f npt_eq.mdp -c em.gro -p complex.top -n index.ndx -o npt_eq.tpr -maxwarn 5
$MPIRUN -n 1 $GMX mdrun -v -deffnm npt_eq -ntomp 8 -nb gpu -pme gpu

# NPT prod 10 ns
$GMX grompp -f prod.mdp -c npt_eq.gro -p complex.top -n index.ndx -o npt_prod.tpr -maxwarn 5
$MPIRUN -n 1 $GMX mdrun -v -deffnm npt_prod -ntomp 8 -nb gpu -pme gpu

cp npt_prod.xtc npt_prod.gro npt_prod.edr npt_eq.gro em.gro $RAYCA_OUT/
```

Key lessons from EDS01806218_ent2 failure history applied here:
- Absolute `mpirun` path (not `srun`, not PATH-resolved)
- `-pme cpu` for EM step only
- No `-ntmpi` flag (MPI build, not thread-MPI)

---

## MM-GBSA Plan (post-trajectory)

Once each `npt_prod.xtc` returns, the analysis will follow the validated EDS01806218_ent2 pipeline:

1. **cpptraj** — strip `:WAT,Cl-` from XTC → `prod_nowater.nc` (NetCDF3 AMBER)
2. **MMPBSA.py** — `startframe=200, endframe=1000, interval=4` (201 frames, last 8 ns); OBC2 GB (igb=5); 0.15 M salt; `-cp complex_nowater.prmtop` only (no `-sp`)

`mmpbsa.in` template (no inline comments — validated fix):
```
&general
  startframe = 200,
  endframe   = 1000,
  interval   = 4,
  verbose    = 2,
  keep_files = 0,
/
&gb
  igb     = 5,
  saltcon = 0.15,
/
```

---

## Files Produced (this phase)

| Directory | Key files |
|:----------|:----------|
| `md_EDS01357518_ent1/` | `complex.prmtop`, `complex.gro`, `complex.top`, `index.ndx`, `em.tpr`, `complex_nowater.prmtop`, `receptor.prmtop`, `ligand.prmtop`, `mmpbsa.in` |
| `md_EDS01357518_ent2/` | same set |
| `md_EDS01806218_ent1/` | same set |
| `md_EDS01889984/` | same set |

---

## Pending

- Cluster jobs 6300385, 6300401, 6300420, 6300478 — awaiting completion
- MM-GBSA analysis for each compound
- Phase document update with ΔG_bind results and comparison table
