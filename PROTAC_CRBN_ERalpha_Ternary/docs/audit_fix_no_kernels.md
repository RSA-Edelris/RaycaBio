# Audit — `--no_kernels` Fix for cuequivariance_torch

## Phase

ARV-471 GPU prediction — fix `ModuleNotFoundError: No module named 'cuequivariance_torch'`
(job 6464953 → job 6465991)

## Container

All jobs used:

| Item | Value |
|---|---|
| Container image | `boltzgen-0.3.1.sif` |
| Container path | `/projects/u6sp/containers/boltzgen-0.3.1.sif` |
| Python venv | `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv` (Python 3.12, boltz==2.2.1) |

## Problem

**Job 6464953 failed** at the Pairformer triangular multiplication forward pass:

```
File ".../boltz/model/layers/triangular_mult.py", line 22, in kernel_triangular_mult
    from cuequivariance_torch.primitives.triangle import triangle_multiplicative_update
ModuleNotFoundError: No module named 'cuequivariance_torch'
```

This was the fifth failure in the GPU prediction chain. The job had successfully:
- Confirmed GPU: `NVIDIA GH200 120GB, 97871 MiB`
- Loaded both checkpoints from cache (`boltz2_conf.ckpt`, `boltz2_aff.ckpt`)
- Parsed and preprocessed the input YAML
- Started the prediction loop (`Predicting DataLoader 0: 0%`)

The crash happened inside `boltz/model/layers/triangular_mult.py`. When `use_kernels=True`
(the default), the function `kernel_triangular_mult` performs a lazy import of
`cuequivariance_torch.primitives.triangle.triangle_multiplicative_update` — an NVIDIA-specific
fused CUDA kernel for triangular multiplicative updates in the Pairformer. This package is
not available as an aarch64 PyPI wheel and is absent from the boltz predict venv.

## Fix

The boltz predict CLI provides `--no_kernels` (type: bool, default: False) which routes
the triangular multiplication through standard PyTorch operations instead of the
`cuequivariance_torch` fused kernel. The flag was confirmed in the CLI help output
(slurm-6462167.log):

```
--no_kernels     Whether to disable the kernels. Default False
```

**Change:** Add `--no_kernels` to the boltz predict command. No changes to `boltz_run.py`
or the input YAML were required.

Command before fix (job 6464953):
```bash
$VENV/bin/python boltz_run.py predict ARV471_ERalpha_CRBN_boltz_input.yaml \
    --out_dir $RAYCA_OUT/boltz_out --cache $CACHE \
    --accelerator gpu --model boltz2 \
    --diffusion_samples 3 --sampling_steps 50 --recycling_steps 3 \
    --output_format pdb --num_workers 0 --seed 42
```

Command after fix (job 6465991):
```bash
$VENV/bin/python boltz_run.py predict ARV471_ERalpha_CRBN_boltz_input.yaml \
    --out_dir $RAYCA_OUT/boltz_out --cache $CACHE \
    --accelerator gpu --model boltz2 \
    --diffusion_samples 3 --sampling_steps 50 --recycling_steps 3 \
    --output_format pdb --num_workers 0 --seed 42 \
    --no_kernels
```

## Verification

**Flag exists and is correctly typed.** The `boltz predict --help` output (slurm-6462167.log)
lists `--no_kernels` as a boolean flag with `Default False`. The flag disables the
`kernel_triangular_mult` code path; the fallback is the standard `einsum`-based
`TriangularMultiplicativeUpdate` implemented in pure PyTorch within boltz.

**Job 6465991 succeeded.** `slurm-6465991.log` shows the prediction loop completed:
`Predicting DataLoader 0: 100%|██████████| 1/1 [00:35<00:00, 0.03it/s]`
followed by `Number of failed examples: 0`. No `cuequivariance_torch` error appears.

**3 poses returned.** All expected output files were collected:
`ARV471_ERalpha_CRBN_boltz_input_model_{0,1,2}.pdb` and matching confidence JSONs.
Best pose confidence_score = 0.4778 (model_0). See phase_07 for full results.

**Performance cost.** The `--no_kernels` fallback uses standard PyTorch triangular
multiplication rather than the fused CUDA kernel. The 35-second wall time (single
ternary complex, 728 tokens, 3 diffusion samples, 50 sampling steps on GH200) suggests
the fallback is fast enough for practical use at this complex size.

**Root cause note.** `cuequivariance_torch` is an NVIDIA package distributed via PyPI
(`nvidia-cuequivariance-torch`) and requires CUDA wheel builds. At the time of venv
construction no aarch64 wheel was available. The `--no_kernels` workaround is the
intended bypass for this missing optional dependency.
