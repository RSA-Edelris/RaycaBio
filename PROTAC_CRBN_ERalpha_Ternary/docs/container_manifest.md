# Container Manifest — Boltz-2 Ternary Complex Prediction Jobs

## Image

| Field | Value |
|:---|:---|
| Image file | `boltzgen-0.3.1.sif` |
| Full path on cluster | `/projects/u6sp/containers/boltzgen-0.3.1.sif` |
| Cluster | Isambard-AI Phase 2 (GH200, aarch64) |
| Boltz version | 2 (v0.4.2) |
| Container runtime | Apptainer (also accessible via `singularity`) |
| Architecture | aarch64 (Grace CPU + GH200 GPU) |
| GPU acceleration | `--nv` flag required; CUDA 12.7, driver 565.57.01 |

The container does **not** include `cuequivariance_torch`; the `--no_kernels` flag is therefore required for every `boltz predict` invocation on this hardware.

The venv used for the actual Python environment (mounted into the container at runtime) is:
`/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv`

The model weight cache is:
`/scratch/u6sp/hpcuser.u6sp/boltz_cache`

Both are on Isambard scratch and are bound into the container with `--bind /scratch,/projects/u6sp`.

---

## Jobs that used this image

| Job ID | Phase document | Description | Status |
|:---:|:---|:---|:---|
| 6465991 | `phase_10_arv471_pdb_export.md` | ARV-471 + ERα + CRBN, 3 diffusion samples | Complete |
| 6534300 | `phase_11_protac_series_pdb_export.md` | ARV-001–010 unconstrained, model_0 | Complete |
| 6540879 | `phase_12_constrained_yaml_generation_and_job_submission.md` | ARV-001–010 constrained (dual pocket), resubmit | Failed — SIGPIPE |
| 6541639 | this document | ARV-001–010 constrained (dual pocket), fixed resubmit | Running |

---

## Invocation template

```bash
apptainer exec --nv \
    --bind /scratch,/projects/u6sp \
    --env WANDB_MODE=disabled \
    /projects/u6sp/containers/boltzgen-0.3.1.sif \
    /scratch/u6sp/hpcuser.u6sp/boltz_predict_venv/bin/python \
    boltz_run.py predict <input.yaml> \
        --out_dir $RAYCA_OUT/<name> \
        --cache /scratch/u6sp/hpcuser.u6sp/boltz_cache \
        --accelerator gpu --model boltz2 \
        --diffusion_samples 3 --sampling_steps 50 --recycling_steps 3 \
        --output_format pdb --num_workers 0 --seed 42 --no_kernels
```

`boltz_run.py` is a minimal wrapper that stubs out the `tensorboard.compat.proto` modules before importing `boltz.main.cli`, preventing a protobuf version crash at startup. It is staged into the job workdir from the session artifacts for each run.
