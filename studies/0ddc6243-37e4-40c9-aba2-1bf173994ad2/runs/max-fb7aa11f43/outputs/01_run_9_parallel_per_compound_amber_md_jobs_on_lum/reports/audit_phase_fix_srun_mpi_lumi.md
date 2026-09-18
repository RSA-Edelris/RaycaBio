# Audit: Fix srun MPI Allocation Bug and Resubmit AMBER MD to LUMI

**Auditor:** Claude Code (automated)
**Date:** 2026-09-15
**Subject:** Job 22076604 — LUMI AMBER pmemd.MPI, 9-system ternary complex MD

---

## Preliminary: Phase Document Status

A phase document exists at
`reports/phase_02_fix_srun_mpi_allocation_bug_and_resubmit_amber_m.md`
but it is effectively empty. It contains the statement
"No method records were captured for this phase, so the procedure cannot be
stated" and its only registered artifact is `source/092_glob_glob.py` — a
283-byte diagnostic script that reads `slurm-22076500.log`. No SLURM job
submission, no script text, and no result output are captured. Job ID 22076604
appears in the audit brief but has no corresponding `slurm-22076604.log` in
the session. The fix therefore cannot be verified against an authoritative
phase record; all findings below are evaluated from the script text and
session evidence alone.

Evidence source for execution behaviour: `slurm-22076619.log` is the closest
matching run. It shows `SLURM_CPUS_PER_TASK=128 / SLURM_NTASKS=unset`, the
smoke test passing, and the first MIN srun step starting (step 22076619.1 on
nid001345) before being cancelled by external signal 118 seconds later.

---

## CRITICAL Findings

### CRIT-1 — `iwrap=1` in staged prod.in but no `autoimage` in cpptraj

**Location:** cpptraj heredoc; `job-22076619/md_work/inputs/prod.in`

The production input file extracted from `systems_stage.tar.gz` sets
`iwrap=1`:

```
 &cntrl
  ...
  iwrap=1,
 /
```

With `iwrap=1`, AMBER wraps every atom independently back to the primary
unit cell at each trajectory write. For a ternary complex larger than the
box diagonal, this splits the complex across the periodic boundary: some
atoms from GSPT1 or CRBN appear near coordinate (0,0,0) while the rest appear
near the far wall.

The cpptraj analysis block does not call `autoimage` before computing RMSD or
distances:

```
parm system.prmtop
trajin prod.nc
rms first :1-575@CA
rms lig_rmsd :576&!@H= nofit out rmsd_lig.dat
distance w380_lig :518@CA :576&!@H= out dist_w380.dat
distance k628_lig :189@CA :576&!@H= out dist_k628.dat
distance ppi_com :1-195 :196-575 out dist_ppi.dat
```

Without `autoimage` or equivalent imaging, frames where the complex has
migrated so that its periodic image crosses the box boundary will produce:
- Protein backbone RMSD values that are box-length multiples too large
- W380–ligand and K628–ligand distances computed from non-minimum images
- GSPT1–CRBN CoM distance (`:1-195` vs `:196-575`) that may measure across
  the full box rather than across the interface

The prior script version (job 22076601, verified in its own audit VC-8)
correctly included `autoimage :LIG anchor`. Its removal in this version is a
regression. The fix is a single added line before the first `rms` command:

```
autoimage :576 anchor
```

(`:576` is the ligand; centering the imaging on it keeps all three
components — GSPT1, CRBN, and LIG — in the same image.)

---

### CRIT-2 — Phase document records no fix and no job submission

**Location:** `reports/phase_02_fix_srun_mpi_allocation_bug_and_resubmit_amber_m.md`

The document records "No tool call is on record for this phase" and status
"complete." The only artifact is the diagnostic read-log script above.
There is no captured SBATCH script, no job ID, no module load record, and no
smoke-test result. This means:

- There is no auditable record that the fix (adding `--ntasks=$N_MPI
  --cpus-per-task=1` to every srun call) was actually present in the submitted
  job.
- Any downstream audit of this phase's output must reconstruct intent from the
  script text alone.

The closest evidence is the slurm-22076619.log run, but that job was cancelled
before completing even the first system's minimisation.

---

## MAJOR Findings

### MAJOR-1 — `except Exception: return "NA"` silences all errors in verdict logic

**Location:** Python block, `verdict()` function

```python
def verdict(row):
    try:
        rmsd = float(row.get("lig_rmsd_A","99"))
        w380 = float(row.get("w380_dist_A","99"))
        k628 = float(row.get("k628_dist_A","99"))
        if rmsd < 4.0 and w380 < 10.0 and k628 < 12.0:
            return "STABLE_GLUE"
        elif rmsd < 4.0 and w380 < 10.0:
            return "CRBN_only"
        else:
            return "unstable"
    except Exception:
        return "NA"
```

`except Exception` catches every Python error, not just
`ValueError` from `float("NA")`. A logic error anywhere inside the
`try` block — a mistyped variable name, a wrong key, a changed threshold
variable — silently returns "NA" for the affected systems rather than raising
an error. With 9 systems sharing the same function call, all 9 rows could
silently receive "NA" verdicts if a single code defect exists.

The correct fix is to catch only the expected error and let unexpected
exceptions propagate:

```python
    except ValueError:
        return "NA"
```

---

### MAJOR-2 — ppi_com_A is computed and tabulated but excluded from verdict

**Location:** Python block, `verdict()` function and metrics list

The script computes `dist_ppi.dat` (GSPT1 CoM to CRBN CoM distance) and
writes `ppi_com_A` / `ppi_com_A_sd` to `md_summary.tsv`. However, the
verdict function ignores `ppi_com_A`:

```python
if rmsd < 4.0 and w380 < 10.0 and k628 < 12.0:
    return "STABLE_GLUE"
```

A compound can receive STABLE_GLUE even if the GSPT1–CRBN interface distance
is large, meaning the two proteins have drifted apart while each individual
anchor contact appears intact. For a molecular-glue campaign, maintaining the
protein–protein interface is a primary success criterion. A STABLE_GLUE
verdict that ignores interface separation is misleading.

This issue was identified in the prior-version audit (audit_job_22076601,
MAJOR-4) and has not been addressed.

---

### MAJOR-3 — Smoke test uses 4 MPI tasks, not 128

**Location:** bash script, smoke test block

```bash
srun --ntasks=4 --cpus-per-task=1 hostname && echo "srun OK" || { echo "srun FAILED"; exit 1; }
```

The production MD steps use `--ntasks=128 --cpus-per-task=1`. A 4-task test
confirms that `srun` accepts the `--ntasks/--cpus-per-task` override syntax
and that basic srun connectivity works. It does not confirm that a 128-task
step will succeed within the job's allocation.

With `SLURM_CPUS_PER_TASK=128` and `SLURM_NTASKS=unset` (confirmed from
slurm-22076619.log), the job allocation is 1 task × 128 CPUs = 128 CPUs
total. A 4-task step consumes 4 CPUs (3% of allocation). A 128-task step
consumes 100%. If the 128-task step is rejected (a different failure mode than
"srun doesn't work"), the smoke test would still pass and the job would waste
time extracting the tarball before failing on the first system.

Evidence: job 22076619 shows the smoke test passing and the 128-task MIN step
starting successfully (the step was not rejected; it ran until external
cancellation). The practical risk is therefore low in this run, but the test
does not provide the coverage it implies. A self-consistent smoke test would
use `--ntasks=$N_MPI`.

---

### MAJOR-4 — 128 CPU partition limit stated as rule based on one observation

**Location:** `audit_phase_04_lumi_amber_cpu_probe.md`

The document states: "The platform caps job allocations at 128 CPUs (1 LUMI
standard node) for this account tier. Requests for 1792 CPUs were silently
clamped to 128." This is presented as policy, but it derives from a single
probe run (job 22075127). The evidence is:
- One job allocated 128 CPUs where more were requested.
- slurm-22076619.log confirms `SLURM_CPUS_ON_NODE=128` for a later job.

These observations are consistent but do not prove a policy. "Silently
clamped" is an unusual SLURM behavior (most schedulers reject over-requests
or queue them); if the actual behavior is queue-and-wait rather than clamp,
N_MPI=128 would still be correct for one node but the stated justification
("clamped to 128") would be wrong. The script hardcodes `N_MPI=128` on the
basis of this single-observation rule. If the rule is wrong in any direction,
the job either under-uses the allocation or requests more tasks than the
partition allows.

---

## MINOR Findings

### MINOR-1 — `nativecontacts` uses first production frame as implicit native reference

**Location:** cpptraj heredoc

```
nativecontacts :576 :196-575 distance 4.5 byresidue out nc_crbn.dat
nativecontacts :576 :1-195   distance 4.5 byresidue out nc_gspt1.dat
```

Without a `ref` keyword, cpptraj defines "native" contacts from the first
loaded trajectory frame (first frame of `prod.nc`). If the compound begins to
dissociate in early production, the reference is already a partially
dissociated pose, and contact fractions are reported relative to that
deteriorated state. A crystal structure or the equilibrated restart
(`equil.rst7`) would be a more defensible reference.

This issue was identified in audit_job_22076601 (MAJOR-3) and is unaddressed.

---

### MINOR-2 — `cp ... || true` silently swallows all copy failures

**Location:** bash script, output collection at end of each system loop

```bash
cp rmsd_lig.dat dist_w380.dat dist_k628.dat dist_ppi.dat \
   nc_crbn.dat nc_gspt1.dat cpptraj.out prod.out prod.mdinfo \
   min.mdinfo equil.mdinfo heat.mdinfo \
   2>/dev/null "$OUTDIR/" || true
```

If cpptraj exits with a non-zero code (e.g., a mask error, a corrupt
trajectory, or a missing prmtop) and produces no output files, `cp` will fail
silently. The `|| true` prevents the loop from registering the failure. The
Python summary step will then find no data files and write all-NA rows without
indicating which system's analysis step actually failed. The `2>/dev/null`
further suppresses the `cp: cannot stat` messages that would otherwise appear
in the job log.

Minimum fix: remove `2>/dev/null` so copy errors appear in the SLURM log, and
replace `|| true` with `|| echo "COPY_FAIL ${SYS}"`.

---

### MINOR-3 — Protein backbone RMSD has no output file

**Location:** cpptraj heredoc

```
rms first :1-575@CA
```

No `out` filename is given. cpptraj writes the backbone RMSD series to
stdout, which is redirected to `cpptraj.out 2>&1`. The backbone RMSD is
therefore mixed with module messages, progress lines, and other cpptraj
output. It is preserved in `cpptraj.out` (which is copied to `$OUTDIR`) but
cannot be parsed programmatically without grep-and-awk post-processing. Adding
`out backbone_rmsd.dat` gives a clean per-frame column file consistent with
the other output files.

---

### MINOR-4 — Population standard deviation used instead of sample standard deviation

**Location:** Python block, `stats()` function

```python
sd = math.sqrt(sum((v-m)**2 for v in vals)/n) if n > 1 else 0.0
```

The divisor is `n` (population SD), not `n-1` (sample SD). For the 100
frames per second-half window (1 ns production, `ntwx=2500`, 200 frames total,
second half = 100 frames), the difference is 0.5% and does not affect rank
ordering. Noted for statistical correctness; not a result-altering defect at
this sample size.

---

## VERIFIED CORRECT

### VC-1 — Residue numbers in all cpptraj masks match the provided context

| Mask | Meaning from context | Status |
|:---|:---|:---|
| `:1-575@CA` (rms backbone) | GSPT1 (1–195) + CRBN (196–575) all-protein CA | Correct |
| `:576` and `:576&!@H=` | LIG = AMBER residue 576 | Correct |
| `:518@CA` (w380_lig distance) | CRBN Trp380 = AMBER 518 | Correct |
| `:189@CA` (k628_lig distance) | GSPT1 Lys628 = AMBER 189 | Correct |
| `:196-575` (nativecontacts CRBN) | CRBN chain Z = AMBER 196–575 | Correct |
| `:1-195` (nativecontacts GSPT1) | GSPT1 chain X = AMBER 1–195 | Correct |

No residue-number confusion found.

---

### VC-2 — AMBER pmemd command flags are in correct order for all four stages

All four pmemd.MPI calls use: `-O -i <input> -p system.prmtop -c <coords>
[-ref system.inpcrd] -o <out> -r <rst7> [-x <nc>] -inf <mdinfo>`. These are
the standard AMBER flags. The `-ref` flag is present on min/heat/equil (where
restraints are applied) and absent on prod (unrestrained). The checkpoint chain
is correct: min.rst7 → heat.rst7 → equil.rst7 → prod.rst7/prod.nc.

---

### VC-3 — `rms lig_rmsd :576&!@H= nofit` is correct post-alignment usage

The preceding `rms first :1-575@CA` (without `nofit`) superimposes each frame
onto frame 1 using protein CA atoms and MODIFIES the in-memory frame
coordinates. The subsequent `rms lig_rmsd :576&!@H= nofit` then calculates the
RMSD of ligand heavy atoms in the already-superimposed frame against the frame-1
ligand position, without performing a second superposition. This is the standard
cpptraj pattern for ligand RMSD after protein alignment. Correct.

---

### VC-4 — `srun --ntasks=128 --cpus-per-task=1` correctly fixes the step allocation

With `SLURM_CPUS_PER_TASK=128` in the job environment (confirmed from
slurm-22076619.log), the original `srun -n 128` would request 128 tasks × 128
CPUs each = 16384 CPUs per step, which is correctly the reported root cause.
The fix `--ntasks=128 --cpus-per-task=1` overrides the per-step
cpus-per-task to 1, giving 128 × 1 = 128 CPUs per step, matching the job
allocation. Confirmed working: slurm-22076619.log shows step 22076619.1
(the MIN step) was allocated and started on nid001345 without a
"More processors requested than permitted" rejection.

---

### VC-5 — `!@H=` is correct cpptraj wildcard syntax for heavy atoms

`:576&!@H=` selects residue 576 AND atoms whose names do NOT start with "H"
(using the `=` trailing-wildcard). This is the standard AMBER cpptraj mask for
heavy (non-hydrogen) atoms. The `&` intersection and `!` negation are applied
as documented in the cpptraj manual. Correct.

---

### VC-6 — `continue` in `|| { ...; continue; }` correctly scopes to the for loop

The compound command `{ echo "FAILED ..."; cd "$WORKDIR"; continue; }` runs in
the current shell (not a subshell). `continue` with no argument targets the
nearest enclosing `for` loop, which is `for SYS in "${SYSTEMS[@]}"`. A srun
failure aborts the current system's pipeline and moves to the next system, as
intended. The `cd "$WORKDIR"` before `continue` correctly resets the working
directory to the shared work root so the next system's `cd "$RUNDIR"` resolves
from the right base. Correct.

---

### VC-7 — `parse_col2` reads the correct column

cpptraj `distance` and `rms` output: column 0 = frame number (integer), column
1 = distance or RMSD value (float). `parse_col2` reads `parts[1]`
(0-indexed), which is the numeric value column. Correct.

---

## Finding Summary

| ID | Severity | Description |
|:---|:---|:---|
| CRIT-1 | Critical | `iwrap=1` in prod.in but no `autoimage` in cpptraj; RMSD and distances corrupted when complex spans periodic boundary |
| CRIT-2 | Critical | Phase document records no fix, no job ID, no submission; cannot verify fix was applied |
| MAJOR-1 | Major | `except Exception` in `verdict()` silences all logic errors as "NA" |
| MAJOR-2 | Major | `ppi_com_A` computed but absent from verdict; STABLE_GLUE possible with drifted PPI |
| MAJOR-3 | Major | Smoke test uses 4 tasks instead of 128; passes even if 128-task step fails |
| MAJOR-4 | Major | 128-CPU partition cap stated as policy based on a single probe observation |
| MINOR-1 | Minor | `nativecontacts` uses first production frame as implicit native reference |
| MINOR-2 | Minor | `cp ... \|\| true` silently swallows all output collection failures |
| MINOR-3 | Minor | Backbone RMSD has no `out` file; data buried in cpptraj.out |
| MINOR-4 | Minor | Population SD (÷n) used instead of sample SD (÷n−1) |
| VC-1 | Verified correct | All cpptraj residue/atom masks match the provided numbering context |
| VC-2 | Verified correct | pmemd.MPI flags and checkpoint chain are correct for all four stages |
| VC-3 | Verified correct | `rms … nofit` after `rms first` is correct ligand-RMSD pattern |
| VC-4 | Verified correct | `--ntasks=128 --cpus-per-task=1` step override correctly fixes the 16384-CPU bug |
| VC-5 | Verified correct | `!@H=` is correct cpptraj heavy-atom wildcard syntax |
| VC-6 | Verified correct | `continue` scope and `cd "$WORKDIR"` reset are correct |
| VC-7 | Verified correct | `parse_col2` reads column 1 (value), not column 0 (frame index) |
