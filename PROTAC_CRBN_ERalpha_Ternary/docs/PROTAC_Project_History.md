# PROTAC Ternary Complex Prediction — Project History

**Project:** Boltz-2 constrained ternary complex modelling, CRBN–ERα PROTAC series  
**Date:** 2026-09-14  
**Platform:** Rayca / Isambard-AI Phase 2 (GH200 aarch64)

---

## What Was Asked

> "Use the best model and use it as the reference ternary geometry. Use the PROTACs in
> Protacs.sdf and model the ternary complex for each against the CRBN–ERα best model
> complex. Rank them by cooperativity rather than by binary affinity, tell me which
> linkers still present a surface lysine to the ligase, and say plainly which of these
> predictions the evidence cannot support. Make sure that the CRBN warhead (glutarimide)
> and the POI warhead (phenol) stay in each of the corresponding target pocket."

In short: run Boltz-2 on 10 PROTACs (ARV_001–010 from Protacs.sdf) as CRBN–ERα ternary
complexes, enforce both warhead pockets via dual constraints, rank by cooperativity proxy
(lig→CRBN iPTM), identify surface lysines presented to CRBN, and state evidence limits.

---

## What Was Produced

| Artefact | Description |
|:---------|:------------|
| 10 × `ARV_00N_constrained_model_0.pdb` | Dual-constrained ternary complex structures (chains A=ERα, B=CRBN, C=PROTAC) |
| 10 × 3 confidence JSON files | Full iPTM/pTM/pair_chains_iptm for model_0/1/2 of each compound |
| `PROTAC_CRBN_ERalpha_Ternary_Results.md` | Detailed results: cooperativity ranking, all confidence scores, surface lysine analysis, evidence limits |
| `phase_13_constrained_cooperativity_report.md` | Narrative report with methodology |
| `audit_phase13_constrained_analysis.md` | Independent subagent audit of analysis code and provenance |
| Boltz-2 YAML inputs (10 files, `ARV_001_constrained.yaml` … `ARV_010_constrained.yaml`) | Dual pocket constraint inputs used for job 6548359 |

### Key Results

| Rank | Compound | lig→CRBN (model_0) | Best surface lysines |
|:----:|:---------|:------------------:|:---------------------|
| 1 | ARV_005 | 0.7181 | K233, K171, K224, K7 |
| 2 | ARV_007 | 0.6771 | K105, K171, K176, K224 |
| 3 | ARV_001 | 0.6740 | K235, K176, K153 |
| 4 | ARV_002 | 0.6252 | K224, K153, K7 |
| 5 | ARV_010 ⚠ | 0.5555 | K224, K7, K153 |
| 6 | ARV_004 | 0.5519 | K224, K233, K7 |
| 7 | ARV_008 | 0.5349 | K7, K171, K233 |
| 8 | ARV_006 | 0.5308 | K171, K176, K120 |
| 9 | ARV_003 | 0.4674 | K233, K153 |
| 10 | ARV_009 | 0.4197 | K233, K66, K153 |

Most consistently presented ERα lysines: **K153** (9/10), **K7, K171, K235** (8/10 each).  
Predictions not supported by evidence: ARV_009, ARV_003 (ranks 9–10); ARV_010 ERα warhead.

---

## Errors Encountered and How They Were Solved

### Error 1 — SIGPIPE crash from `nvidia-smi | head -14` (job 6540879)

**What happened:** The Slurm script used `set -o pipefail` and `nvidia-smi | head -14`.
When `head` exits after 14 lines, the still-running `nvidia-smi` receives SIGPIPE (exit 141),
which propagates as a pipeline failure and aborts the job before Boltz starts.

**Fix:** Appended `|| true` to the pipeline:
```bash
nvidia-smi | head -14 || true
```

---

### Error 2 — Self-copy failure: `cp` tried to copy a file onto itself (job 6541639)

**What happened:** The script contained `cp "$PREV_WD/boltz_run.py" .`
where `$PREV_WD` was the current working directory (same run ID). `cp` refused to
copy a file onto itself (exit 1) and the job aborted.

**Fix:** Removed the `cp` line entirely and staged `boltz_run.py` as an explicit
`inputs:` entry so the platform copied it to the cluster before the script ran.

---

### Error 3 — `torch.utils.tensorboard` version check raises `ImportError` (job 6547343)

**What happened:**
```
ImportError: TensorBoard logging requires TensorBoard version 1.15 or above
```
PyTorch's `torch/utils/tensorboard/__init__.py` imports `tensorboard.version.VERSION`
and raises `ImportError` if the value is absent or below 1.15. Our early stub for
`tensorboard` lacked a `.version` submodule entirely.

**Fix:** Added a `tensorboard.version` stub with `VERSION = "2.17.0"` before Boltz
is imported, and pre-registered `torch.utils.tensorboard` as a package stub (with
`__path__ = []`) containing a `_NoOpWriter` as `SummaryWriter`.

---

### Error 4 — `ModuleNotFoundError: 'torch.utils.tensorboard' is not a package` (job 6548166)

**What happened:**
```
ModuleNotFoundError: No module named 'torch.utils.tensorboard.summary';
'torch.utils.tensorboard' is not a package
```
Python cannot find submodules of a stub object that lacks `__path__`. The earlier fix
registered `torch.utils.tensorboard` as a plain `types.ModuleType` without `__path__`,
so `from torch.utils.tensorboard.summary import hparams` failed.

**Fix:** Used `_pkg_stub()` (sets `m.__path__ = []`) for all parent stubs that need
submodule support; pre-registered `torch.utils.tensorboard.summary` with the
`hparams` no-op function; pre-registered `torch.utils.tensorboard.writer` and
`torch.utils.tensorboard._utils`.

---

### Error 5 — `AttributeError: '_NoOpWriter' has no attribute '_get_file_writer'` (job 6548227)

**What happened:**
```
AttributeError: '_NoOpWriter' object has no attribute '_get_file_writer'.
Did you mean: 'file_writer'?
```
`lightning_fabric/loggers/tensorboard.py:259` calls `self.experiment._get_file_writer()`
on the `SummaryWriter` returned by our stub's `experiment` property. Each fix to the
writer stub revealed a new method the chain required.

**Fix:** Changed approach entirely — instead of patching individual methods on the
`SummaryWriter` stub, replaced the entire `pytorch_lightning.loggers.TensorBoardLogger`
and `lightning_fabric.loggers.TensorBoardLogger` classes with a complete `_NoOpTBLogger`
class. This class has a `__getattr__` fallback so any method PL calls returns a no-op.
Also added `_get_file_writer` to `_NoOpWriter` as `return self`.

**Decisive fix** — job 6548359 succeeded with this version of `boltz_run.py`.

---

### Error 6 — `TypeError: unsupported format string passed to NoneType.__format__` (Python analysis)

**What happened:** Analysis script `045_range.py` used `d.get("prot_iptm", None)`.
The actual JSON key is `"protein_iptm"`. All 10 compounds returned `None`, and the
downstream formatting `{value:.4f}` raised `TypeError`.

**Fix:** Used the correct key `"protein_iptm"` in all subsequent analysis scripts
(scripts 048 onward and script 053). All reported values were extracted with the
correct key.

---

### Error 7 — `boltz_run.py` wrapper not available inside Apptainer container

**What happened (jobs 6547343–6548227):** The wrapper script existed locally but
was not staged as an input for the cluster job. Once staged via `inputs:`, the
container working directory received a fresh copy on every submission, eliminating
the version-mismatch problem that caused confusion across job iterations.

---

## Technical Details

### boltz_run.py — Final Tensorboard Suppression Strategy

The venv at `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv` contains PyTorch Lightning
which tries to instantiate a `TensorBoardLogger` on every `trainer.predict()` call.
The TensorBoard Python package in the container is absent or incompatible. Four
separate crash paths were encountered and fixed:

1. `tensorboard.version` absent → ImportError in torch init
2. `torch.utils.tensorboard` not a package → ModuleNotFoundError for submodules
3. `_NoOpWriter` missing methods called by lightning_fabric → AttributeError
4. Final fix: replace `TensorBoardLogger` class itself with `_NoOpTBLogger`

The final wrapper pre-stubs all tensorboard modules, registers the torch tensorboard
package stubs with `__path__`, then monkey-patches both
`pytorch_lightning.loggers.tensorboard.TensorBoardLogger` and
`lightning_fabric.loggers.tensorboard.TensorBoardLogger` with a no-op class before
importing `boltz.main.cli`.

### Constraint YAML Format (Boltz-2)

Dual warhead constraints require two separate `pocket` blocks under `constraints:`:
```yaml
constraints:
  - pocket:
      binder: C
      contacts: [[B, 111], [B, 112], ...]   # CRBN glutarimide pocket
      max_distance: 6.0
      force: false
  - pocket:
      binder: C
      contacts: [[A, 47], [A, 50], ...]     # ERα phenol pocket
      max_distance: 6.0
      force: false
```
Residue numbering is 1-indexed and per-chain (resets to 1 for each chain). Chain
letters in contacts match the chain identifiers in the `sequences:` block.

### Cluster Invocation

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

`--no_kernels` is required on aarch64 GH200 — `cuequivariance_torch` is not
available in `boltzgen-0.3.1.sif`.

---

## Job History

| Job ID | Status | Description |
|:------:|:------:|:------------|
| 6465991 | Complete | ARV-471 + ERα + CRBN unconstrained, reference model |
| 6534300 | Complete | ARV_001–010 unconstrained, model_0 baseline |
| 6540879 | Failed | ARV_001–010 constrained; SIGPIPE from `nvidia-smi | head -14` |
| 6541639 | Failed | Resubmit; self-copy error (`cp file file`) |
| 6547343 | Failed | `boltz_run.py` v2; `tensorboard.version` stub missing |
| 6548166 | Failed | `boltz_run.py` v3; `torch.utils.tensorboard` not a package |
| 6548227 | Failed | `boltz_run.py` v4; `_get_file_writer` missing from `_NoOpWriter` |
| **6548359** | **Complete** | `boltz_run.py` v5 (no-op TBLogger class); all 10 compounds, 180+ output files |

---

## Verification

### Error fixes — how each was confirmed

Each `boltz_run.py` fix was verified by the outcome of the next cluster job submission.
The fix was considered correct when the previously failing line no longer appeared in the
Slurm log and execution advanced further into Boltz-2.

| Fix | Confirmed by |
|:----|:------------|
| `|| true` after `nvidia-smi \| head -14` | Job 6541639 started Boltz-2 (different error) |
| Remove self-copy `cp` line; stage via `inputs:` | Job 6547343 reached `trainer.predict()` (different error) |
| Add `tensorboard.version` stub with `VERSION="2.17.0"` | Job 6548166 passed version check (different error) |
| Use `_pkg_stub()` with `__path__=[]` for all parent stubs | Job 6548227 passed submodule import (different error) |
| Replace `TensorBoardLogger` with `_NoOpTBLogger` class | Job 6548359 ran to completion; 180+ output files collected |

Each job log is retained at `slurm-<jobid>.log` in the session root for reference.

### Results analysis — what was verified

**Confidence values**: Three compounds (ARV_001, ARV_005, ARV_007) were spot-checked by
opening the raw JSON from job 6548359 and comparing to the reported table. All values
matched to 4 decimal places. Full details in `PROTAC_CRBN_ERalpha_Ternary_Results.md`
Verification section.

**Chain assignment**: Confirmed from PDB file structure (ARV_001 model_0): chain A = SER 1
through residue 258, chain B = MET 1 through residue 469, chain C = HETATM LIG 1. Matches
the YAML input chain ordering (ERα = chain 0/A, CRBN = chain 1/B, PROTAC = chain 2/C).

**Cooperativity proxy**: `pair_chains_iptm["2"]["1"]` confirmed correct by cross-checking
chain identity from self-iptm values and reading the key path directly from ARV_001 JSON.

**Independent audit**: An independent subagent (a03c0880c9efb654c) read the analysis scripts
and source JSON without access to the analyst's reasoning. Findings (2026-09-14):
- **VERIFIED**: All spot-checked numeric values correct; key paths correct; chain indexing consistent
- **CRITICAL**: `prot_iptm` column documented as produced by scripts 045/046, which cannot
  run to completion (key name error `prot_iptm` vs `protein_iptm`). Actual source is script 053.
  Numeric values are correct for ARV_001; provenance trail is broken for the other 9.
- **MAJOR**: `Δ unconstrained` column uses hardcoded reference values with no file-level
  provenance; ARV_007 rank-reversal claim rests on two single-seed values; silent `None`
  fallback in confidence_score retrieval (not triggered, but fragile).

Full audit record: `audit_phase13_constrained_analysis.md`.

### What was not verified

- PDB coordinate geometry beyond ARV_001 clash check (no energy minimisation on any compound)
- Model_1 and model_2 outputs (not analysed; model_0 used throughout)
- Unconstrained lig→CRBN reference values (ARV_001–010 from job 6534300) have no
  independently traceable source within this run's artefacts
- Surface lysine analysis performed only on model_0 for each compound
