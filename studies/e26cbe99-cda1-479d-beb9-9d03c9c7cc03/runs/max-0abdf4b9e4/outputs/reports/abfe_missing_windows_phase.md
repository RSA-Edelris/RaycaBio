## Summary

This phase aimed to run the 33 missing GROMACS FEP lambda windows needed to complete the double-decoupling ABFE campaign for three ligands: **EDS01806218** (enantiomers ent1 and ent2) and **EDS01889984**.

---

## Status: Blocked — manual submission required

All SLURM queues on Isambard-AI and LUMI are empty (jobs physically complete), but the Rayca platform's session-level job tracker is stuck at its 20-job limit due to completed jobs from earlier runs in this session. No further jobs can be submitted via `run_on_cluster` in this session; the counter cannot be decremented from a different run.

---

## Missing windows

| Compound | Leg | Missing windows | Count |
|---|---|---|---|
| EDS01806218 ent1 | complex | 12–16 | 5 |
| EDS01806218 ent1 | solvent | 16 | 1 |
| EDS01806218 ent2 | complex | 12–16 | 5 |
| EDS01806218 ent2 | solvent | — | 0 (complete) |
| EDS01889984 | complex | 12–16 | 5 |
| EDS01889984 | solvent | 00–16 | 17 |
| **Total** | | | **33** |

---

## Lambda schedule (all legs)

17 windows per leg: 4 coulombic (λ_coul = 0→1) then 13 vdW (λ_vdW = 0→1, soft-core α=0.5).  
Each window: 750,000 steps × 2 fs = 1.5 ns; `nstdhdl=100`; `calc-lambda-neighbors=-1` (all-pairs).

---

## Input files prepared

All 46 input files (GRO, TOP, MDP, NDX) plus `run_abfe_missing.sh` are packaged in:

- **`abfe_missing_inputs.tar.gz`** (2.7 MB, 47 files total)
- **`run_abfe_missing.sh`** — ready-to-submit sbatch script

The script runs 33 windows in batches of 4 (one per GPU, `CUDA_VISIBLE_DEVICES`), using:
- GROMACS: `/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/bin/gmx_mpi`
- Partition: `workq`; 1 node, 32 CPUs, 4 GPUs, 120 min wall time
- `-nb gpu -pme gpu -ntomp 8` per mdrun call

All files are also pushed to **`RaycaBio/abfe-eds-missing-windows`** (private) at:  
`studies/e26cbe99-cda1-479d-beb9-9d03c9c7cc03/runs/max-f6ec66bfd5/`

---

## Manual submission instructions

```bash
# On Isambard
WORK=/scratch/u6sp/hpcuser.u6sp/abfe_missing
mkdir -p $WORK && cd $WORK

git clone https://github.com/RaycaBio/abfe-eds-missing-windows.git repo
RUN=repo/studies/e26cbe99-cda1-479d-beb9-9d03c9c7cc03/runs/max-f6ec66bfd5
cp $RUN/scripts/run_abfe_missing.sh .
tar xzf $RUN/outputs/abfe_missing_inputs.tar.gz

sbatch run_abfe_missing.sh
```

After completion, copy `*_dhdl.xvg` back into the Rayca session directory so MBAR analysis can proceed.

---

## dhdl files already present (51 total)

| Compound | Leg | Windows present |
|---|---|---|
| EDS01806218 ent1 | complex | 00–11 |
| EDS01806218 ent1 | solvent | 00–15 |
| EDS01806218 ent2 | complex | 00–11 |
| EDS01806218 ent2 | solvent | 00–16 ✓ complete |
| EDS01889984 | complex | 00–11 |
| EDS01889984 | solvent | — |

---

## Next step

Once all 33 dhdl files are available, run MBAR via alchemlyb to compute ΔG_bind for each compound/enantiomer. EDS01806218 ent2 solvent is already complete; it is waiting only on the 5 missing complex windows.
