## Objective
Refine EL2003A docking pose 2 (best docking pose, MM-GBSA ΔG = −61.835 kcal/mol from EM scoring) via explicit-solvent molecular dynamics and recalculate binding free energy from the MD ensemble.

## Strategy Decisions

### GPU partition unavailable via platform
All `gpus=1` submissions to LUMI were rejected with "Requested node configuration is not available". Diagnostic confirmed that CPU-only jobs (`gpus=0`) submit successfully. Root cause: the `run_on_cluster` platform does not route to the GPU partition (`small-g`) when `gpus=1` is requested on LUMI. A minimal echo-script with `gpus=1` also failed identically, ruling out script content as the cause.

### MMPBSA.py absent from Amber 24 on LUMI
`MMPBSA.py` is not installed in `$AMBERHOME/bin` and the Python module `MMPBSA_mmpbsa` is not importable. The legacy `mm_pbsa.pl` script is present along with `cpptraj`, `sander`, and `pmemd.MPI`.

### cpptraj energy does not support GB
cpptraj V6.24.0 (OpenMP build) reports only `nonbond`, `elec`, `vdw`, `bond`, `angle`, `dihedral` energy terms — no `igb` option. GB single-point calculations must go through `sander`.

### Final pipeline: pmemd.MPI + sander MMPBSA
- **Force field**: ff14SB (protein) + GAFF2 (ligand, gas charges, neutral) + TIP3P (water)
- **Box**: truncated octahedron, 12 Å buffer, ~0.15 M NaCl
- **MD stages**: min1 (restrained 5k) → min2 (unrestrained 10k) → heat NVT 200 ps → equil NPT 1 ns → prod NPT 5 ns
- **MMPBSA**: 100 frames (50 ps intervals), sander IGB=5 SALTCON=0.15, 1-trajectory approach
- **Parallelism**: 128 MPI ranks (pmemd.MPI) for MD; 64 parallel workers (Python multiprocessing) for sander loop

## LUMI Job
- **Job ID**: 21798843
- **Cluster**: LUMI (lumi.csc.fi)
- **Partition**: small (CPU-only, 128 cores, EPYC 7763)
- **Walltime requested**: 8 hours
- **Resources**: 128 CPUs, 0 GPUs

## Expected Outputs (in $RAYCA_OUT)
| File | Description |
|------|-------------|
| `mmgbsa_results.json` | ΔG_bind mean ± SD over 100 frames, per-frame values |
| `mmgbsa_output.log` | Sander MMPBSA calculation log |
| `final_complex.pdb` | Last MD frame, protein + ligand, no solvent |
| `final_lig.mol2` | MD-refined ligand pose (mol2 format) |
| `prod.out` | Amber production MD log (temperature, pressure, energy) |
| `equil.out` | Equilibration log |
| `tleap.log` | Topology build log |

## Prior Attempts (GBSA container, mode="md")
Three prior dispatches of the GBSA containerised tool with `mode="md"` all ran MD successfully (1 ns, GPU 33–79%) but failed identically at `gmx_MMPBSA MPI -cg 14 2` because the container hardcodes group indices 14 and 2, which do not correspond to the receptor and ligand in the PDK1+EL2003A+TIP3P system. The container is not modifiable and provides no fallback.

## Reference Values for Comparison
- Docking pose 2 GNINA affinity: −9.80 kcal/mol
- EM-mode MM-GBSA ΔG: −61.835 kcal/mol (GROMACS amber03+GAFF2 GB)
- This MD run uses ff14SB+GAFF2+IGB5 — absolute values not directly comparable across force-field/GB combinations, but the relative change is informative
