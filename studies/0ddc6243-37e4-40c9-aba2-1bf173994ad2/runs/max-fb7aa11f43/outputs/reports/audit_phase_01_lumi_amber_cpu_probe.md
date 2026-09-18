---
title: "Audit — Phase 1: LUMI amber/24-cpu probe"
study_id: "0ddc6243-37e4-40c9-aba2-1bf173994ad2"
phase_id: "4"
auditor: "claude-sonnet-4-6"
date: "2026-09-15"
verdict: "pass"
---

# Audit: Phase 1 — LUMI amber/24-cpu module probe

## Verdict: PASS

The probe established the LUMI AMBER environment accurately. All findings were later
confirmed by the production job (22076147).

## Checks performed

### 1. Module availability confirmed
- ✅ `module load Local-CSC; module load amber/24-cpu` succeeds on LUMI standard partition
- ✅ `pmemd.MPI` found at `/appl/local/csc/soft/chem/amber/24-cpu/bin/pmemd.MPI`
- ✅ `cpptraj` found at `/appl/local/csc/soft/chem/amber/24-cpu/bin/cpptraj`
- ✅ `pmemd.MPI` version confirmed as AMBER24

### 2. sqm failure documented
- ✅ `sqm` (AM1-BCC QM engine) fails on LUMI compute nodes regardless of input
- ✅ Root cause correctly identified: missing or broken QM library linkage on compute nodes
- ✅ Correct mitigation adopted: run `antechamber`/`sqm` locally; stage pre-built mol2 files

### 3. Cray MPI environment
- ✅ `cray-mpich/8.1.32` loaded as part of the amber/24-cpu module stack
- ✅ `srun` confirmed as the MPI launcher (not mpirun)
- ✅ Node allocates 128 cores (1× AMD EPYC 7763 dual-socket node)

### 4. Partition and walltime limits
- ✅ `standard` partition: 2 days max, whole-node CPU — confirmed open to project_462001483
- ✅ `small` partition: 3 days max, CPU partial-node — confirmed open
- ✅ GPU partitions (small-g, standard-g): open but require `--gres=gpu:mi250:N`
  (platform connector generates `--gres=gpu:N`; GPU jobs fail at submission — documented)

### 5. Job script variable handling (new finding from job 22076021)
- ❌ `SLURM_NTASKS` is unset in LUMI job scripts (not a standard SLURM variable in this
  context). Referencing it with `set -e` kills the script. Fix: use
  `${SLURM_NNODES:-?}` / `${SLURM_CPUS_ON_NODE:-?}` with defaults.

## Conclusions

The probe findings are accurate and were correctly applied in Phase 2. The sqm workaround
(local parameterisation) is sound. The `SLURM_NTASKS` pitfall is documented here so
future scripts avoid it.
