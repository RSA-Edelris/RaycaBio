## Phase: Run 33 missing ABFE lambda windows

**Status:** Blocked — Rayca 20-job session cap exhausted by prior runs. SLURM queues on Isambard and LUMI are empty; blocker is platform-side only.

## Missing windows (33 total)

| Compound | Leg | Windows |
|---|---|---|
| EDS01806218 ent1 | complex | 12–16 |
| EDS01806218 ent1 | solvent | 16 |
| EDS01806218 ent2 | complex | 12–16 |
| EDS01889984 | complex | 12–16 |
| EDS01889984 | solvent | 00–16 |

## Deliverables

- `run_abfe_missing.sh` — sbatch script (workq partition, 1 node, 4×GH200 GPU, 120 min, batches of 4 windows per GPU)
- `abfe_missing_inputs.tar.gz` — 46 input files (GRO/TOP/MDP/NDX) + script (2.7 MB)
- GitHub repo `RaycaBio/abfe-eds-missing-windows` (private) — all files pushed

## Manual submission (Isambard)

```bash
WORK=/scratch/u6sp/hpcuser.u6sp/abfe_missing && mkdir -p $WORK && cd $WORK
git clone https://github.com/RaycaBio/abfe-eds-missing-windows.git repo
RUN=repo/studies/e26cbe99-cda1-479d-beb9-9d03c9c7cc03/runs/max-f6ec66bfd5
cp $RUN/scripts/run_abfe_missing.sh . && tar xzf $RUN/outputs/abfe_missing_inputs.tar.gz
sbatch run_abfe_missing.sh
```

After completion, copy `*_dhdl.xvg` back to the session directory for MBAR analysis.
