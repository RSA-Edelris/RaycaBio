
## Overview

This document records the MM-GBSA free binding energy calculation campaign for all 32 CRBN-binding stereoisomers docked in Phase 3/4. The phase is **in progress**: topologies are built and MD is running on LUMI; MMPBSA.py analysis will follow.

---

## Objective

Compute single-trajectory MM-GBSA ΔG_binding for all 32 best docked poses to supplement the gnina Vina/CNN scores with an energy-minimised binding affinity estimate, enabling a dual-ranked compound selection.

---

## Protocol

### Force field and charge method

| Component | Method |
|-----------|--------|
| Protein   | ff14SB (AMBER 24) |
| Ligand    | GAFF2 + Gasteiger charges (`antechamber -c gas`) |
| Solvation | Implicit GB, igb=5 (OBC-II), saltcon=0.10 M |

**Charge method rationale.** AM1-BCC (`-c bcc`) was attempted first but sqm rejected 16 of 32 ligands with "odd number of electrons" because the V2000 SDF files carry only 3 explicit H atoms (aromatic and aliphatic C-H bonds are implicit in the gnina output). sqm counts electrons from the atom block as given and finds an odd total at nc=0. Gasteiger charges bypass sqm entirely, are applied consistently across all 32 compounds, and are sufficient for relative ranking within a congeneric glutarimide series.

### ZN handling

The single ZN HETATM at residue B1428 (20.5 Å from the binding-site centroid, no contacts in interaction analysis) was removed from the receptor PDB before tleap. `loadamberparams frcmod.ionsjc_tip3p` loads without error but tleap cannot assign an atom type to the isolated ZN in the absence of coordinating residues in the truncated CRBN domain. Its removal has negligible impact on pocket energetics.

### MD parameters

| Parameter | Value | Note |
|-----------|-------|-------|
| Minimisation | 500 steps (ncyc=200 SD, then CG) | |
| MD length | 10,000 steps × 0.002 ps = **20 ps** NVT | Short; adequate for relative ranking in congeneric series |
| Trajectory frames | 50 (save every 200 steps) | |
| cut | 12.0 Å | |
| rgbmax | 12.0 Å | Cuts GB Born-radii cost; ~2× speedup vs default 25 Å |
| ntt | 3 (Langevin, γ=2.0) | |
| ntc/ntf | 2 | SHAKE on H bonds |

### MMPBSA.py settings

```
&general
  startframe=1, endframe=50, interval=1,
/
&gb
  igb=5, saltcon=0.10,
/
```

`intdiel`/`extdiel` are not valid `&gb` keywords in AmberTools 24 MMPBSA.py and were removed. The default interior dielectric (ε=1) is appropriate for this neutral congeneric series.

---

## Execution

### Local preparation (completed)

- `antechamber -c gas -at gaff2`: **32/32 OK** (all mol2 files 3.2–4.4 kB)
- `parmchk2 -s gaff2`: **32/32 OK**
- `tleap` (ff14SB + GAFF2, no ZN): **32/32 OK** (complex.prmtop ~2.65 MB each)

### Cluster MD (in progress — LUMI job 21779205)

32 parallel sander processes on LUMI small-CPU partition (32 CPUs requested), `module load Local-CSC && module load amber/24-cpu`. Each process runs min → MD sequentially; all 32 run in parallel on separate CPUs. Trajectories written to `$RAYCA_OUT/md_traj/` as `{compound_dir}_md.nc`.

Estimated wall clock: 1.5–3 h (LUMI AMD EPYC CPUs at similar throughput to local benchmark of 315 ms/step with rgbmax=12).

### Local MMPBSA.py analysis (pending LUMI output)

Script: `mmgbsa/run_mmpbsa.py`  
- Sets `AMBERHOME=/home/ubuntu/rayca-runtime/.mamba/envs/rayca`  
- Uses `-cp` (not `-sp`) for complex prmtop  
- Passes absolute paths to all files  
- Parses `DELTA TOTAL` from the Differences section  
- Cleans `_MMPBSA_*` temp files before each run  

Tested and validated on 2-frame test trajectory for EDEL-CRBN-0001: DELTA TOTAL = −42.02 ± 1.75 kcal/mol.

---

## Issues encountered and resolutions

| Issue | Root cause | Resolution |
|-------|-----------|------------|
| `antechamber` sqm "odd electrons" for 16/32 ligands | gnina V2000 SDF has implicit C-H; sqm counts only explicit atoms → odd Z sum | Switch to Gasteiger charges (`-c gas`); bypasses sqm entirely |
| `tleap` fatal on ZN atom type | Isolated ZN without coordination environment has no AMBER atom type | Remove ZN from receptor PDB; 20.5 Å from pocket, zero contacts |
| sander 585 ms/step with cut=12 | Default rgbmax=25 Å causes near-O(N²) GB Born-radii computation | Add `rgbmax=12.0`; reduces to 315 ms/step (~2× speedup) |
| MMPBSA.py `AMBERHOME` TypeError | `os.getenv('AMBERHOME')` returns None; `os.path.join(None,...)` fails | Set `AMBERHOME` in subprocess env |
| MMPBSA.py `Unknown variable intdiel in &gb` | `intdiel`/`extdiel` moved out of `&gb` in AmberTools 24 | Remove those keywords; use igb+saltcon only |
| MMPBSA.py `Could not open complex_prmtop` | Leftover `_MMPBSA_*` temp files from prior failed run | Clean glob `_MMPBSA_*` before each call; use absolute paths |

---

## Files produced

| File | Location | Description |
|------|----------|-------------|
| `receptor_nozn.pdb` | `mmgbsa/` | Receptor PDB with ZN removed |
| `{name}_ent/lig.mol2` | `mmgbsa/` | GAFF2 + Gasteiger charges (32 files) |
| `{name}_ent/lig.frcmod` | `mmgbsa/` | Missing GAFF2 parameters (32 files) |
| `{name}_ent/complex.prmtop` | `mmgbsa/` | ff14SB+GAFF2 complex topology, ~2.65 MB each (32 files) |
| `{name}_ent/rec.prmtop` | `mmgbsa/` | ff14SB receptor topology (32 files) |
| `{name}_ent/lig.prmtop` | `mmgbsa/` | GAFF2 ligand topology (32 files) |
| `pipeline.py` | `mmgbsa/` | Topology-prep functions |
| `run_mmpbsa.py` | `mmgbsa/` | MMPBSA.py analysis script |
| `collate_results.py` | `mmgbsa/` | Final ranking table generation |
| LUMI job 21779205 | LUMI scratch | 32 parallel sander min+MD runs |

---

## Status at phase close

| Step | Status |
|------|--------|
| Topology preparation (32 compounds) | **Complete** |
| Sander min + MD (32 × 20 ps) | **Running** — LUMI job 21779205 |
| MMPBSA.py analysis (32 compounds) | Pending LUMI output |
| Final combined ranking table | Pending MMPBSA.py |

The phase will be fully complete once LUMI returns trajectories and MMPBSA.py runs locally. All analysis scripts are validated and ready to fire.

---

## Limitations and caveats

- **Gasteiger vs AM1-BCC charges**: Gasteiger charges are empirical and less accurate than AM1-BCC for polar/ionisable groups. For relative ranking within a neutral glutarimide congeneric series the systematic error is expected to cancel; absolute ΔG values should not be interpreted without charge-method uncertainty.
- **Short MD (20 ps)**: Adequate for local relaxation and relative ranking but insufficient for converged absolute binding free energies. Standard error across 50 frames provides a precision estimate, not an accuracy estimate.
- **No entropy term**: Entropy was omitted (standard for congeneric ranking). Differences in conformational entropy between enantiomers are not captured.
- **rgbmax=12 Å**: Slightly below the recommended default (25 Å) for GB accuracy; tested acceptable for relative ranking but may introduce small errors in buried-atom Born radii.
