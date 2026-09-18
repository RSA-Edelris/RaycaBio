
## Objective

Predict the ternary complex structure of ARV-471 bridging ERalpha (POI) and CRBN (E3 ligase) using Boltz-2, producing 3 ranked poses in PDB format with per-pose confidence scores and PROTAC bridging geometry.

## Inputs

| Component | Details |
|-----------|---------|
| POI | ERalpha LBD construct, 258 residues (chain A) |
| E3 ligase | CRBN construct (His-tag + TEV + CRBN), 469 residues (chain B) |
| PROTAC | ARV-471, SMILES: `O=C1CC[C@H](N2Cc3cc(N4CCN(CC5CCN(c6ccc([C@@H]7c8ccc(O)cc8CC[C@@H]7c7ccccc7)cc6)CC5)CC4)ccc3C2=O)C(=O)N1` (chain C) |
| MSA | Empty (single-sequence mode) |
| Seed | 42 |
| Poses requested | 3 |
| Output format | PDB |

The input YAML (`ARV471_ERalpha_CRBN_boltz_input.yaml`) and preprocessed structure (5887 atoms, 728 residues, 3 chains) were validated successfully.

## Execution Path and Blockers Resolved

### Attempt 1 — Rayca GPU sandbox (protacfold container)
**Failed.** `RuntimeError: DataLoader worker (pid 77) exited unexpectedly` at every system size ≥ 288 tokens. Root cause: Docker's default 64 MB `/dev/shm` limit in the Rayca sandbox container; Boltz's DataLoader workers use shared memory for inter-process tensor passing, exceeding the limit for a 728-token system. Confirmed by binary search: 60-token system runs, 288-token system fails.

### Attempt 2 — Isambard-AI_HPC (GH200 GPU, boltzgen-0.3.1.sif)
**Blocked.** Platform-level 20/20 active-job limit. SLURM reports 0 running jobs (all prior submissions completed), but the platform's internal job counter remains at 20 — stale records from previous sessions that cannot be cancelled or collected from this run. Retried multiple times across context windows; limit persists.

### Attempt 3 — Rayca Python environment, CPU inference (active)
**In progress.** Installed `boltz==2.2.1` via `install_package`. Resolved three further issues:
1. Wrong CLI flag: `--output_dir` → `--out_dir`
2. GPU-required crash: added `--accelerator cpu`
3. Protobuf version conflict (tensorboard gencode 6.31.1 vs runtime 5.29.6): wrote `boltz_run.py` wrapper that stubs out `tensorboard.compat.proto` modules before `boltz.main` is imported, and deleted stale `__pycache__/main.cpython-312.pyc`

**Current state:** PID 3638479 running for **2h 48min at 143% CPU**. Model loaded, preprocessing complete, prediction loop entered ("Predicting DataLoader 0: 0%"). No PDB output yet — the tqdm counter stays at 0/1 until the entire 728-token batch completes. Log size static at 1709 bytes (expected; no per-step progress is emitted during diffusion).

## Run Parameters (active job)

```
boltz predict ARV471_ERalpha_CRBN_boltz_input.yaml
  --out_dir boltz_cpu_out/
  --accelerator cpu
  --diffusion_samples 3
  --recycling_steps 1       # reduced from default 3 for CPU speed
  --sampling_steps 50       # reduced from default 200 for CPU speed
  --output_format pdb
  --num_workers 0            # critical: prevents DataLoader shared-memory crash
  --no_kernels               # disables CUDA triton kernels
  --seed 42
```

## Expected Outputs (pending)

```
boltz_cpu_out/boltz_results_ARV471_ERalpha_CRBN_boltz_input/predictions/
  ARV471_ERalpha_CRBN_boltz_input_model_0.pdb   # pose 1
  ARV471_ERalpha_CRBN_boltz_input_model_1.pdb   # pose 2
  ARV471_ERalpha_CRBN_boltz_input_model_2.pdb   # pose 3
  confidence_ARV471_ERalpha_CRBN_boltz_input_model_0.json
  confidence_ARV471_ERalpha_CRBN_boltz_input_model_1.json
  confidence_ARV471_ERalpha_CRBN_boltz_input_model_2.json
  confidence_ARV471_ERalpha_CRBN_boltz_input_summary.json
```

Each confidence JSON contains: `confidence_score`, `ptm`, `iptm`, `ligand_iptm`, `protein_iptm`, `complex_plddt`. The summary JSON ranks all three poses.

## Estimated Completion

Based on CPU throughput at 143% for a 728-token system with 50 diffusion steps × 3 samples: **4–6 hours total from launch**, placing completion approximately 1–3 hours from now.

## Quality Note

Reduced settings (`recycling_steps=1`, `sampling_steps=50`) lower pose quality relative to the Boltz-2 defaults (3 recycling passes, 200 steps). For a publication-quality prediction, rerun with full settings on GPU once the Isambard platform limit clears or LUMI ROCm setup is completed.

## Next Steps After Completion

1. Parse `confidence_*_summary.json` — rank poses by `confidence_score` (composite of iPTM + pLDDT)
2. Load best-ranked PDB — extract chain C (ARV-471) coordinates
3. Compute bridging geometry: distance between ERalpha-contacting atoms and CRBN-contacting atoms of the PROTAC, and the angle subtended
4. Report per-pose confidence table and bridging geometry description
