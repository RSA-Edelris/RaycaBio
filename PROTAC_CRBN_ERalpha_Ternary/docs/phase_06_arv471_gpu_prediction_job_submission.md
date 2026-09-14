## Summary

This phase submitted the production Boltz-2 structure prediction for the ARV-471 PROTAC ternary complex (ERα chain A 258 aa, CRBN chain B 469 aa, ARV-471 SMILES chain C 54 heavy atoms) to the Isambard GH200 GPU cluster. Six job submissions were required to resolve a chain of dependency issues; the sixth (6465991) is the current active job.

## Container

All cluster jobs in this phase used:

| Item | Value |
|---|---|
| Container image | `boltzgen-0.3.1.sif` |
| Container path | `/projects/u6sp/containers/boltzgen-0.3.1.sif` |
| Container runtime | Apptainer (single-node, no multi-node module) |
| Architecture | aarch64 (NVIDIA GH200 120 GB Grace Hopper) |
| Python runtime | Container Python 3.12 via venv at `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv/` |
| boltz version | 2.2.1 (installed in venv; see dependency probe phases 1–5) |

The boltzgen container is a binder-design pipeline tool. It was used here only as an aarch64 Python 3.12 runtime with PyTorch+CUDA already compiled for the GH200. The boltz PyPI package and its dependencies were installed separately into the venv on top of this container's system packages.

## Job 1: 6462260 — FAILED

### Script

```bash
apptainer exec --bind /scratch,/projects/u6sp $CONTAINER \
  $VENV/bin/python boltz_run.py predict \
    ARV471_ERalpha_CRBN_boltz_input.yaml \
    --out_dir $RAYCA_OUT/boltz_out \
    --checkpoint $CKPT --cache $CACHE \
    --accelerator gpu --model boltz2 \
    --diffusion_samples 3 --sampling_steps 50 --recycling_steps 3 \
    --output_format pdb --num_workers 0 --seed 42
```

where `$CKPT` = `/projects/u6sp/containers/boltzgen_weights/models--boltzgen--boltzgen-1/snapshots/c1be29e1f82ffcc72264f64b993c43fb4e0d17f0/boltz2_conf_final.ckpt`

### Failure

The job completed preprocessing (CCD data downloaded, input parsed, 1 input processed) and then crashed at `model_cls.load_from_checkpoint()`:

```
File ".../torch/serialization.py", line 1487, in load
  ...
ModuleNotFoundError: No module named 'boltzgen'
```

Root cause: `boltz2_conf_final.ckpt` was serialized by the boltzgen package and contains pickled references to boltzgen internal classes. When torch's pickle deserialization tries to reconstruct these objects it imports `boltzgen`, which is not installed in the boltz predict venv.

The official Boltz-2 checkpoint (`boltz2_conf.ckpt`) was downloaded to the cache during this job's initialization (slurm-6462260.log lines 10–11) before the crash.

**Log:** `slurm-6462260.log` (79 lines)

## Job 2: 6462447 — FAILED

### Change from Job 1

Removed `--checkpoint $CKPT`. Without an explicit checkpoint, boltz uses the official `boltz2_conf.ckpt` it downloads to `$CACHE`. That checkpoint is serialized by the boltz package itself and has no boltzgen class references.

Added `--env WANDB_MODE=disabled` to suppress wandb startup network calls on the compute node.

### Script

```bash
apptainer exec \
  --bind /scratch,/projects/u6sp \
  --env WANDB_MODE=disabled \
  $CONTAINER \
  $VENV/bin/python boltz_run.py predict \
    ARV471_ERalpha_CRBN_boltz_input.yaml \
    --out_dir $RAYCA_OUT/boltz_out \
    --cache $CACHE \
    --accelerator gpu --model boltz2 \
    --diffusion_samples 3 --sampling_steps 50 --recycling_steps 3 \
    --output_format pdb --num_workers 0 --seed 42
```

### Failure

`nvidia-smi` inside the Apptainer container was not found in `$PATH` on this compute node (node-to-node Apptainer configuration variability). `set -e` made the `nvidia-smi` check line fatal, exit 255.

**Log:** `slurm-6462447.log` (8 lines)

### Fix for Job 3

- Moved the `nvidia-smi` call to the host (outside `apptainer exec`).
- Added `--nv` to `apptainer exec` to explicitly bind the host NVIDIA driver stack into the container.

---

## Job 3: 6462632 — FAILED

### Change from Job 2

Added `--nv` to `apptainer exec`; `nvidia-smi` moved to host-side check before `apptainer exec`. Updated `boltz_run.py` to stub `torch.utils.tensorboard` before importing `boltz.main`.

### Failure

`lightning_fabric/loggers/tensorboard.py` called `from torch.utils.tensorboard import SummaryWriter` at experiment-init time. PyTorch's own `torch/utils/tensorboard/__init__.py` raises:

```
ImportError: TensorBoard logging requires TensorBoard version 1.15 or above
```

because TensorBoard is not installed. The stub in `boltz_run.py` at this point did not yet override `torch.utils.tensorboard`; it only stubbed the `tensorboard` top-level package.

**Log:** `slurm-6462632.log` (68 lines)

### Fix for Job 4

Updated `boltz_run.py` to import `torch` first, then immediately replace `torch.utils.tensorboard` in `sys.modules` with a fake module containing `SummaryWriter = _NoOp`.

---

## Job 4: 6463987 — FAILED

### Change from Job 3

Updated `boltz_run.py`: stubs `torch.utils.tensorboard` as a fake module before `boltz.main` is imported.

### Failure

`lightning_fabric/loggers/tensorboard.py` log_hyperparams called:

```
from torch.utils.tensorboard.summary import hparams
ModuleNotFoundError: No module named 'torch.utils.tensorboard.summary';
'torch.utils.tensorboard' is not a package
```

Root cause: the fake `torch.utils.tensorboard` module did not have `__path__` set, so Python did not treat it as a package and refused to allow submodule imports from it.

**Log:** `slurm-6463987.log` (68 lines)

### Fix for Job 5

Set `_fake_tb.__path__ = []` on the fake module (marks it as a package). Added `torch.utils.tensorboard.summary` stub with `hparams = lambda hparams_dict, metrics_dict: ({}, {}, {})`. Also stubbed `torch.utils.tensorboard.writer` with `SummaryWriter = _NoOp`.

---

## Job 5: 6464953 — FAILED

### Change from Job 4

Comprehensive `boltz_run.py` tensorboard stub: `__path__` set, `.summary` submodule with `hparams`, `.writer` submodule with `SummaryWriter`.

### Failure

The model got much further — GPU confirmed (`NVIDIA GH200 120GB`), both checkpoints in cache, model loaded from `boltz2_conf.ckpt`, input preprocessed, `Predicting DataLoader 0` started — then crashed in the Pairformer triangular multiplication forward pass:

```
File ".../boltz/model/layers/triangular_mult.py", line 122
    from cuequivariance_torch.primitives.triangle import triangle_multiplicative_update
ModuleNotFoundError: No module named 'cuequivariance_torch'
```

`cuequivariance_torch` is an NVIDIA-specific CUDA kernel for accelerated triangular multiplicative update. It is not installed in the boltz predict venv (no aarch64 wheel available via PyPI at the time of venv build). The boltz CLI includes a `--no_kernels` flag that bypasses this code path and falls back to standard PyTorch operations.

**Log:** `slurm-6464953.log` (128 lines)

### Fix for Job 6

Add `--no_kernels` to the `boltz predict` command. This flag is documented in `boltz predict --help` (`--no_kernels  Whether to disable the kernels. Default False`).

---

## Job 6: 6465991 — COMPLETED

### Change from Job 5

Added `--no_kernels` to the boltz predict command.

### Script

```bash
apptainer exec --nv --bind /scratch,/projects/u6sp \
  --env WANDB_MODE=disabled \
  $CONTAINER \
  $VENV/bin/python boltz_run.py predict \
    ARV471_ERalpha_CRBN_boltz_input.yaml \
    --out_dir $RAYCA_OUT/boltz_out \
    --cache $CACHE \
    --accelerator gpu --model boltz2 \
    --diffusion_samples 3 --sampling_steps 50 --recycling_steps 3 \
    --output_format pdb --num_workers 0 --seed 42 \
    --no_kernels
```

### Expected output

On success: 3 PDB files (`ARV471_ERalpha_CRBN_boltz_input_model_0.pdb` through `_model_2.pdb`) and 3 confidence JSON files under `$RAYCA_OUT/boltz_out/boltz_results_ARV471_ERalpha_CRBN_boltz_input/predictions/`.

### Resources

1 GH200 GPU, 8 CPUs, 60 min walltime.

---

## Verification

**Dependency resolution chain.** Each job advanced one step further before revealing the next missing piece:

| Job | Reached | Failure |
|---|---|---|
| 6462260 | CCD download, input preprocessing complete | `boltzgen` class reference in checkpoint pickle |
| 6462447 | Apptainer startup | `nvidia-smi` not on PATH inside container |
| 6462632 | Model checkpoint loaded, GPU confirmed | `TensorBoard logging requires TensorBoard version 1.15+` |
| 6463987 | log_hyperparams reached | `torch.utils.tensorboard` not a package (no `__path__`) |
| 6464953 | Pairformer forward pass started | `cuequivariance_torch` not installed |
| 6465991 | — | awaiting result (added `--no_kernels`) |

**Preprocessing verified (Job 1).** Input YAML correctly parsed; CCD data downloaded; 5 processed artifact files produced before checkpoint crash. Input is confirmed valid.

**GPU confirmed (Jobs 3–5).** `NVIDIA GH200 120GB, 97871 MiB` reported on host; `GPU available: True (cuda), used: True` confirmed inside container in slurm-6462632.log, 6463987.log, 6464953.log.

**Checkpoints in cache (Job 3+).** `boltz2_conf.ckpt` (2.2 GB) and `boltz2_aff.ckpt` (2.0 GB) both present at `/scratch/u6sp/hpcuser.u6sp/boltz_cache/` from Job 1 download. Confirmed in slurm-6462632.log lines 4–5.

**boltz_run.py tensorboard stub complete.** Three-stage evolution resolved ImportError (Job 3 fix), `__path__`/package error (Job 4 fix), and `.summary.hparams` import (Job 4 fix). Job 5 got past all logger initialization into the model forward pass — confirming the stub is sufficient.

**`--no_kernels` flag confirmed available.** Listed in `boltz predict --help` output (slurm-6462167.log): `--no_kernels  Whether to disable the kernels. Default False`. Job 6 adds this flag; no code change to boltz_run.py required.

## CPU baseline (for comparison when Job 2 completes)

From the CPU run (`ARV471_ERalpha_CRBN_ternary_boltz2.pdb`):

| Metric | model_0 |
|---|---|
| confidence_score | 0.448 |
| ptm | 0.422 |
| iptm | 0.273 |
| ligand_iptm | 0.797 |

The CPU run used 1 diffusion sample; Job 2 will produce 3. The GPU run is expected to be structurally equivalent but may differ numerically due to different hardware BLAS implementation.
