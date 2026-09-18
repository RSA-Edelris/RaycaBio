## What was checked

LUMI job 22075127 (standard partition, 128 CPUs) probed whether `amber/24-cpu` provides the required executables on a compute node.

## Findings

| Executable | Path | Status |
|---|---|---|
| pmemd.MPI | `/appl/local/csc/soft/chem/amber/24-cpu/bin/pmemd.MPI` | ✓ present, v24.0 |
| cpptraj | `/appl/local/csc/soft/chem/amber/24-cpu/bin/cpptraj` | ✓ present |
| antechamber | (module-provided) | present on login node |
| sqm | (antechamber dependency) | ✗ **fails on compute nodes** |

## sqm failure

`sqm` (the semi-empirical QM engine used by antechamber for AM1-BCC charges) exits fatally on LUMI compute nodes. Error: `Fatal Error! Cannot properly run sqm -O -i sqm.in -o sqm.out`. This blocks antechamber from completing charge assignment on the cluster.

## Decision

Run antechamber locally (where sqm works), then stage pre-built `system.prmtop` + `system.inpcrd` files to LUMI. Only pmemd.MPI and cpptraj — both confirmed working — are needed on the cluster.

## Module load sequence (confirmed working)

```bash
module load Local-CSC
module load amber/24-cpu
```

Lmod automatically replaces `craype-x86-rome` → `craype-x86-milan`, `PrgEnv-cray` → `PrgEnv-gnu`, and reloads `cray-libsci/25.03.0` and `cray-mpich/8.1.32`. No manual toolchain selection needed.

## CPU clamp

The platform caps job allocations at 128 CPUs (1 LUMI standard node) for this account tier. Requests for 1792 CPUs were silently clamped to 128.

## Container image note

No container image was used in this phase. The amber/24-cpu module is a native CSC installation at `/appl/local/csc/soft/chem/amber/24-cpu/`.
