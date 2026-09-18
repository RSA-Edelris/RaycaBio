# Audit Report — Job 22076601 LUMI AMBER MD Submission

**Auditor:** Claude Code (automated)
**Date:** 2026-09-15
**Job:** 22076601, LUMI, AMBER MPI pmemd, 9-ligand ternary complex MD

---

## Preliminary Finding: No Phase Document

No prior phase document exists for this phase. All claims in this audit are evaluated from the
script text alone and from the provided context summary. The stated intent of each analysis
choice (verdict thresholds, distance pairs, nativecontacts selection, production length) cannot
be checked against documented scientific decisions. This is reported as a structural gap — any
finding below that relies on intent is necessarily uncertain.

---

## MAJOR Findings

### MAJOR-1 — `cd` inside the ligand loop has no error check

**Location:** loop body, before the first `srun` call

```bash
mkdir -p "${WORK}/${LIG}"
cd "${WORK}/${LIG}"
```

There is no `|| { echo "CD_FAIL ${LIG}" >> ...; continue; }` guard on the `cd`. If the
`cd` fails — for example, due to a transient permission change, a filesystem flush delay on
Lustre, or a node that re-mounts the scratch with altered UIDs — the shell remains in whichever
directory was current from the previous iteration (or from the job's launch directory on the
first iteration). Every subsequent relative path in that iteration then silently targets the
wrong location:

- Output files `mini.out`, `mini.rst`, `nvt.rst`, `nvt.nc`, `npt.rst`, `npt.nc`,
  `prod_r1.nc`, `prod_r2.nc`, `prod_r3.nc` are written to the wrong directory.
- cpptraj `trajin prod_r1.nc` / `prod_r2.nc` / `prod_r3.nc` in the heredoc are relative and
  resolve against the wrong directory; cpptraj will fail or read stale data from a prior ligand.

The practical risk is low because `mkdir -p` guarantees the directory exists immediately before
`cd`, but the absence of the guard is a correctness hazard and inconsistent with the defensive
pattern used on every `srun` call. Recommended fix:

```bash
cd "${WORK}/${LIG}" || { echo "CD_FAIL ${LIG}" >> "${RESULTS}/progress.txt"; continue; }
```

---

### MAJOR-2 — `nativecontacts` data generated and copied but never read; verdict is blind to contact counts

**Location:** cpptraj heredoc and Python summary block

The script collects:

```
nativecontacts :LIG :196-575 distance 4.5 out ${WORK}/${LIG}/${LIG}_crbn_nc.dat
nativecontacts :LIG :1-195  distance 4.5 out ${WORK}/${LIG}/${LIG}_gspt1_nc.dat
```

Both files are then copied to `${RESULTS}/`. However, the Python summary block never opens
them and the verdict does not incorporate them:

```python
rmsd = read_col(f"{lig}_lig_rmsd.dat")
crbn = read_col(f"{lig}_crbn_anchor.dat")
gspt = read_col(f"{lig}_gspt1_bridge.dat")
ppi  = read_col(f"{lig}_ppi_com.dat")
# _crbn_nc.dat and _gspt1_nc.dat: never read
```

For a molecular glue campaign the number of simultaneously maintained contacts to both CRBN and
GSPT1 is a primary stability indicator. The STABLE_GLUE verdict is computed without this
information. The files are present for manual inspection, but any automated ranking or
prioritisation based on `summary_table.txt` is missing this dimension.

---

### MAJOR-3 — `nativecontacts` uses first production frame as implicit native reference

**Location:** cpptraj heredoc, `nativecontacts` calls

The cpptraj `nativecontacts` command, without an explicit `ref` keyword, defines "native"
contacts from the first loaded frame — in this case the first frame of `prod_r1.nc`. If the
ternary complex drifts early in production (e.g., a weak glue that begins to dissociate within
the first 100 ps), the "native" reference is already a partially dissociated structure, and
contact fractions for all subsequent frames will be reported relative to that deteriorated state
rather than the initial bound pose. The correct practice is to supply a reference:

```
nativecontacts :LIG :196-575 distance 4.5 ref <minimised_or_crystal.rst> out ...
```

Without a phase document there is no way to confirm whether using the first production frame was
intentional. If it was, the rationale should be stated.

---

### MAJOR-4 — PPI_COM distance computed and shown in table but absent from verdict

**Location:** Python summary, verdict block

```python
ppi  = read_col(f"{lig}_ppi_com.dat")
pm=float(np.mean(ppi[h:]));  ps=float(np.std(ppi[h:]))
...
if rm < 4.0 and cm < 10.0 and gm < 12.0:
    v = "STABLE_GLUE"
elif rm < 4.0 and cm < 10.0:
    v = "CRBN_only"
else:
    v = "unstable"
```

`pm` (CRBN–GSPT1 CoM distance) is read, averaged, and reported in the table, but no threshold
on it appears in the verdict logic. A compound could receive STABLE_GLUE even if the
protein–protein interface distance is large, meaning the glue held its individual anchor
contacts but the two proteins drifted apart — the defining failure mode for a molecular glue.
The stated verdict criteria (LigRMSD < 4 Å, W380 < 10 Å, K628 < 12 Å) do not mention a PPI
distance cutoff, but because no phase document exists this cannot be confirmed as a deliberate
omission. If it is intentional, it should be documented; if it is not, a PPI check should be
added to the verdict.

---

## VERIFIED CORRECT

### VC-1 — RAYCA_OUT captured before module loads

```bash
RESULTS="${RAYCA_OUT}"
mkdir -p "${RESULTS}"
echo "job_start=$(date)" > "${RESULTS}/run_start.txt"
module load Local-CSC
module load amber/24-cpu
```

`RESULTS` is assigned before both module loads. The known behaviour (confirmed by jobs
22076465/484/500 per session memory) that `module load Local-CSC` / `amber/24-cpu` unsets
`RAYCA_OUT` is correctly handled. Every subsequent write uses `${RESULTS}`, never
`${RAYCA_OUT}`. Fix is correctly applied.

---

### VC-2 — `read_col` column index reads distance/RMSD, not frame index

```python
def read_col(path, col=1):  # 0-indexed; col=1 → second column
    ...
    vals.append(float(p[col]))
```

cpptraj distance output format: column 0 = frame index, column 1 = distance in Å.
cpptraj rmsd output format: column 0 = frame index, column 1 = RMSD in Å.

`p[1]` (0-indexed) reads the second column, which is the numeric distance or RMSD value in
both cases. Correct.

---

### VC-3 — `continue` in `|| { ...; continue; }` correctly scopes to the for loop

```bash
srun ... || { echo "MINI_FAIL ${LIG}" >> ...; continue; }
```

In bash, `{ ...; }` is a compound command that executes in the current shell, not a subshell.
`continue` with no argument targets the nearest enclosing for/while/until loop, which is
`for LIG in $LIGS`. If `srun` exits non-zero, the block runs, `echo` writes the failure tag,
and `continue` skips the remainder of the current ligand iteration and begins the next. The
`echo` failure cannot prevent `continue` from executing (they are sequential statements, not
conditional). This pattern is correct on all six `srun` calls.

---

### VC-4 — `h = n // 2` last-50% slice spans adequate production time

Total production frames: 3 runs × (1,000,000 steps ÷ ntwx=10,000) = 300 frames.
`h = 300 // 2 = 150`. The last 150 frames represent:

  150 frames × 10,000 steps/frame × 0.002 ps/step = 3,000 ps = 3 ns

of a 6 ns production total. Discarding the first 3 ns as equilibration while retaining 3 ns
for statistics is standard practice for a 6 ns run. The slice is correctly computed and
adequately sized.

---

### VC-5 — Residue numbering in distance and nativecontacts masks matches provided context

| Mask used in script | Context mapping | Match |
|---|---|---|
| `:518@CA` (crbn_anchor distance) | W380(CRBN) = AMBER 518 | Correct |
| `:189@CA` (gspt1_bridge distance) | K628(GSPT1) = AMBER 189 | Correct |
| `:196-575` (nativecontacts CRBN) | CRBN chain Z = AMBER 196–575 | Correct |
| `:1-195` (nativecontacts GSPT1) | GSPT1 chain X = AMBER 1–195 | Correct |
| `:LIG` | LIG = AMBER residue 576; `:LIG` selects by residue name | Correct |

The Python summary table header (`W380_dist` = cm from `_crbn_anchor.dat`, `K628_dist` = gm
from `_gspt1_bridge.dat`) correctly labels the columns matching the cpptraj output files.

---

### VC-6 — Centroid-to-CA distance metric is internally consistent with verdict thresholds

`:LIG :518@CA` computes the distance between the ligand heavy-atom centroid and the Cα of
W380(CRBN). `:LIG :189@CA` computes the same to K628(GSPT1) Cα. These are centroid-to-point
distances, not atom-to-atom minimums. This is a standard coarse proximity metric for molecular
glue anchor residues. The verdict thresholds (10 Å for W380, 12 Å for K628) are applied
consistently with the metric as computed.

---

### VC-7 — Production run restart chain is correct

```
run 1: -c npt.rst   → writes prod_r1.rst
run 2: -c prod_r1.rst → writes prod_r2.rst
run 3: -c prod_r2.rst → writes prod_r3.rst
```

`prod.in` has `irest=1, ntx=5` (restart with velocities from restart file). The chain is
sequential within each ligand iteration, and each `||` guard aborts with `continue` if a stage
fails, so a failed r1 will never write a plausible `prod_r1.rst` that tricks r2 into running.
Correct.

---

### VC-8 — Autoimage anchor and RMSD mask are appropriate

`autoimage :LIG anchor` sets the molecular glue as the imaging origin, which is correct for a
ternary complex where the ligand should remain centered. `:LIG & !@H=` selects non-hydrogen
ligand atoms for RMSD; `& !@H=` is standard AMBER mask syntax for the hydrogen exclusion.
`first` sets the first frame as RMSD reference. Both choices are appropriate.

---

## Finding Summary

| ID | Severity | Description |
|---|---|---|
| — | Structural | No phase document; intent cannot be verified against prior documentation |
| MAJOR-1 | Major | `cd` in loop has no error check; silent wrong-directory writes possible |
| MAJOR-2 | Major | nativecontacts data generated but never read; verdict omits contact counts |
| MAJOR-3 | Major | nativecontacts native reference is first production frame, not a true native structure |
| MAJOR-4 | Major | PPI_COM distance computed but excluded from verdict; STABLE_GLUE possible without PPI maintenance |
| VC-1 | Verified correct | RAYCA_OUT fix applied correctly |
| VC-2 | Verified correct | read_col col=1 reads distance/RMSD values |
| VC-3 | Verified correct | continue scope in \|\| block is correct |
| VC-4 | Verified correct | last-50% slice spans 3 ns of 6 ns production |
| VC-5 | Verified correct | All residue numbers match provided context |
| VC-6 | Verified correct | Centroid-to-CA metric consistent with thresholds |
| VC-7 | Verified correct | Production restart chain is correct |
| VC-8 | Verified correct | Autoimage and RMSD mask are appropriate |

No CRITICAL findings. No result-invalidating indexing errors, reversed positional arguments,
or silent exception swallowing were found. Four MAJOR findings affect completeness and
robustness of the analysis; none corrupt the MD trajectories themselves.
