# Audit Report — Phase: Submit 9 parallel per-compound AMBER MD jobs to LUMI

**Auditor:** Claude Code (automated)
**Date:** 2026-09-15
**Session root:** `/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/`

---

## Files examined

| File | Disposition |
|:---|:---|
| `slurm-22076500.log` | Read in full — module probe output, no cpptraj line |
| `job-22076500/step1_before.txt` | Read in full — RAYCA_OUT and pmemd.MPI path only |
| `job-22076484/` | Directory not found on disk |
| `md/stage/` | Listed — 18 topology files enumerated |
| `md/param/CPD4/` | Listed — CPD4.frcmod, CPD4_v2.frcmod, CPD4.mol2, CPD4_fixed.mol2 present |
| `md/param/CPD7/` | Listed — CPD7.frcmod, CPD7.mol2, CPD7_fixed.mol2 present |
| `slurm-22076611/619/621/643/647/694/698/714/729/809.log` | Read — all parallel job logs |
| `job-22076619/step_before.txt` | Not present; `md_work/` and progress files read |
| `job-22076619/md_work/inputs/prod.in` | Read — `iwrap=1`, 1 ns production |
| `reports/phase_02_submit_9_parallel_per_compound_amber_md_jobs_to_.md` | Read in full |
| `reports/audit_job_22076601_lumi_md_submission.md` | Read in full |
| `reports/audit_job_22076601_md_submission.md` | Read in full |
| `reports/audit_phase_fix_srun_mpi_lumi.md` | Read in full |
| `reports/audit_job_22076435_recovery.md` | Read in full |
| `reports/audit_phase_12_md_status_report_job22076601.md` | Read in full |
| `report.md` | Read — performance numbers |
| `jobB_log.txt` | Read — compound assignments for job B |
| `amber_md/` and `amber_md_B/` input files | Read |
| `probe.txt`, `probe.22076465.txt` | Read |

---

## What the phase document says

`reports/phase_02_submit_9_parallel_per_compound_amber_md_jobs_to_.md` exists but is substantively empty. It records:

- Status: complete
- "No method records were captured for this phase, so the procedure cannot be stated."
- "No tool call is on record for this phase."
- Six artifacts listed: two progress text files, two SLURM logs, one audit md, one progress log.

No script text, no job IDs for the 9 parallel submissions, no sbatch parameters, and no analysis of results are present in this document. It cannot support reproduction or independent audit from the document alone.

---

## What the SLURM logs show actually happened

| Job ID | SLURM log verdict |
|:---|:---|
| 22076611 | `srun: error: Unable to create step for job 22076611: More processors requested than permitted` |
| 22076619 | Smoke test PASS; MIN step started (step 22076619.1 on nid001345); cancelled 118 s later by external signal |
| 22076621 | `srun: error: Unable to create step for job 22076621: More processors requested than permitted` |
| 22076643 | `srun: error: Unable to create step for job 22076643: More processors requested than permitted` |
| 22076647 | `srun: error: Unable to create step for job 22076647: More processors requested than permitted` |
| 22076694 | `srun: error: Unable to create step for job 22076694: More processors requested than permitted` |
| 22076698 | `srun: error: Unable to create step for job 22076698: More processors requested than permitted` |
| 22076714 | `srun: error: Unable to create step for job 22076714: More processors requested than permitted` |
| 22076729 | `srun: error: Unable to create step for job 22076729: More processors requested than permitted` |
| 22076809 | `srun: error: Unable to create step for job 22076809: More processors requested than permitted` |

No trajectory data was produced for any compound in the parallel per-compound approach.
The approach was subsequently superseded by a sequential 9-system job (22076673 / 22076604).

---

## CRITICAL Findings

### CRIT-1 — `iwrap=1` in prod.in with no `autoimage` in the cpptraj analysis block

**Evidence:** `job-22076619/md_work/inputs/prod.in` line 12 sets `iwrap=1`. The cpptraj analysis block recorded in `reports/audit_phase_fix_srun_mpi_lumi.md` (CRIT-1 in that audit) does not call `autoimage` before computing RMSD or distances:

```
parm system.prmtop
trajin prod.nc
rms first :1-575@CA
rms lig_rmsd :576&!@H= nofit out rmsd_lig.dat
distance w380_lig :518@CA :576&!@H= out dist_w380.dat
distance k628_lig :189@CA :576&!@H= out dist_k628.dat
distance ppi_com :1-195 :196-575 out dist_ppi.dat
```

With `iwrap=1`, AMBER wraps atoms independently to the primary unit cell at each write. For a ternary complex larger than the box diagonal, this splits the complex across the periodic boundary. Without `autoimage`, the RMSD and inter-residue distances will be corrupted whenever the complex drifts so that any component crosses the boundary. This renders the LigRMSD, W380 distance, K628 distance, and PPI COM distance metrics unreliable for affected frames. This issue was identified by a prior audit (`audit_phase_fix_srun_mpi_lumi.md` CRIT-1) and the `prod.in` file on disk still carries `iwrap=1`.

Note: the earlier script version (job 22076601, audited in `audit_job_22076601_lumi_md_submission.md`) correctly included `autoimage :LIG anchor`; its omission in the version extracted from `job-22076619/md_work/inputs/` is a regression.

---

### CRIT-2 — Phase document records no fix, no job submission, no script text

**Evidence:** `reports/phase_02_submit_9_parallel_per_compound_amber_md_jobs_to_.md` contains "No tool call is on record for this phase" and its six artifacts are limited to two progress txt files, two SLURM logs, one audit md, and one progress log. No SBATCH script, no job IDs, no module-load record, and no MD output are captured. The description says the procedure "cannot be stated." Status is marked "complete."

This means there is no auditable record of what script was actually submitted for any of the 9 parallel jobs. The failure mode of each job (srun step-creation error) was verified from the SLURM logs, but the exact script text that caused the failures cannot be confirmed from this phase document.

---

## MAJOR Findings

### MAJOR-1 — Phase document is substantively empty for a phase marked "complete"

**Evidence:** `reports/phase_02_submit_9_parallel_per_compound_amber_md_jobs_to_.md` explicitly states "No method records were captured for this phase, so the procedure cannot be stated. This is a gap in the record, not a phase that did no work." Six artifacts are listed; of these, only the two SLURM logs are primary evidence. The document cannot support independent reproduction or peer review of any decision made in this phase.

This is distinct from CRIT-2, which addresses the specific inability to verify the submitted script. The gap here is systemic: every design decision (N_MPI per compound, CPU allocation per job, production length, analysis thresholds) is absent from the record.

---

### MAJOR-2 — cpptraj availability was NOT confirmed in the designated probe job (22076500); confirmation appears only in a later job

**Evidence:** `job-22076500/step1_before.txt` contains five lines:
```
BEFORE_MODULES: RAYCA_OUT=[...]
AFTER_Local-CSC: RAYCA_OUT=[...]
AFTER_amber_24cpu: RAYCA_OUT=[...]
AFTER_ALL_MODULES: RAYCA_OUT=[...] SAVED=[...]
/appl/local/csc/soft/chem/amber/24-cpu/bin/pmemd.MPI
```
The file ends at the `pmemd.MPI` path. There is no `cpptraj` line.

`slurm-22076500.log` records only the module-load output and does not contain a `cpptraj` path either.

cpptraj IS confirmed in `slurm-22076619.log` (a later job that got further): `cpptraj : /appl/local/csc/soft/chem/amber/24-cpu/bin/cpptraj`. However, that confirmation came from a job that was cancelled 118 seconds after launch, not from the dedicated probe.

Any decision that relied on "cpptraj confirmed in the probe" is not supported by `step1_before.txt`. If the probe script omitted the `which cpptraj` call, the omission is not recoverable.

---

### MAJOR-3 — Job B compound assignment: CPD8 absent, CPD10 present instead of the stated composition

**Evidence:** `reports/audit_job_22076435_recovery.md` (the contemporaneous recovery document) states Job B was intended to cover "CPD8, CPD9." `jobB_log.txt` shows:

```
>>> CPD9 start 20:07:32
  CPD9 mini FAILED (exit 1)
>>> CPD10 start 20:07:32
  CPD10 mini FAILED (exit 1)
>>> CPD11 start 20:07:32
  CPD11 mini FAILED (exit 1)
>>> CPD12 start 20:07:32
  CPD12 mini FAILED (exit 1)
```

CPD8 does not appear in jobB_log.txt. CPD10 appears instead. Whether this is a mis-labelling of the job or a genuine omission of CPD8 from the job script cannot be determined because no job script was captured (CRIT-2). CPD8 has a staged topology (`md/stage/CPD8.prmtop` and `md/stage/CPD8.inpcrd` both present). The log also covers CPD11 and CPD12, which the recovery document assigns to Job C. It is not clear whether jobB_log covers a different job than the one documented as "Job B," or whether the LIGS list in the submitted script differed from the documented intent.

---

### MAJOR-4 — Performance estimate (~22 h/compound, 4.22 ns/day) derived from a single compound in a single partially complete NVT run

**Evidence:** `report.md` and `reports/audit_phase_12_md_status_report_job22076601.md` both use 4.22 ns/day as the basis for all timeline projections. This number comes from CPD4 NVT at step 120,000/250,000 (48% complete) in job 22075127. No other compound has measured performance numbers in the session record. The schedule estimate "~22 h per compound, ~44 h per job — within 2880-min walltime" in `reports/audit_job_22076435_recovery.md` depends entirely on this single-compound, partially-complete measurement. A different compound (different topology size, solvation, or box dimensions) could produce materially different performance; no uncertainty bound is documented.

Note: the "2 ns/day" figure mentioned in the audit brief was NOT found in any session file. The actual figure used throughout the record is 4.22 ns/day. The "1.75 days fits in 2-day walltime" formulation was also not found verbatim; the closest evidence is the 42.6 h/compound estimate against a 48 h cap, both in `report.md`.

---

### MAJOR-5 — `except Exception: return "NA"` in verdict() silences all logic errors

**Evidence:** Confirmed in `reports/audit_phase_fix_srun_mpi_lumi.md` (MAJOR-1) for the version analysed against job 22076619-era scripts:

```python
def verdict(row):
    try:
        ...
    except Exception:
        return "NA"
```

`except Exception` catches all Python exceptions, not only the expected `ValueError` from `float("NA")`. Any misspelled variable, wrong dict key, or changed threshold name inside the try block silently returns "NA" for all 9 systems rather than raising a diagnostic error. This was identified and not corrected before the next submission.

---

### MAJOR-6 — `nativecontacts` data generated, copied, but never read; verdict ignores contact counts

**Evidence:** Confirmed in `reports/audit_job_22076601_lumi_md_submission.md` (MAJOR-2):

The script collects per-compound `_crbn_nc.dat` and `_gspt1_nc.dat` but the Python summary block never opens them. For a molecular-glue campaign, the number of simultaneously maintained contacts to CRBN and GSPT1 is a primary stability indicator. The STABLE_GLUE verdict is computed without this information.

---

### MAJOR-7 — PPI COM distance computed and tabulated but excluded from verdict

**Evidence:** Confirmed in both `reports/audit_job_22076601_lumi_md_submission.md` (MAJOR-4) and `reports/audit_phase_fix_srun_mpi_lumi.md` (MAJOR-2). The `ppi_com_A` column appears in `md_summary.tsv` but the verdict logic contains no threshold on it. A compound can receive STABLE_GLUE even if the GSPT1-CRBN interface distance is large. This issue was flagged in an earlier audit and remained unaddressed in the version used for job 22076619.

---

### MAJOR-8 — 128-CPU partition limit stated as policy based on a single probe observation

**Evidence:** Confirmed in `reports/audit_phase_fix_srun_mpi_lumi.md` (MAJOR-4). The hardcoded `N_MPI=128` is justified by the statement "the platform caps job allocations at 128 CPUs," which derives from one probe run (job 22075127). `slurm-22076619.log` confirms `SLURM_CPUS_ON_NODE=128` for one later job. These observations are consistent but do not establish policy. The word "silently clamped" is not standard SLURM behaviour; if the actual mechanism differs (e.g., reject vs clamp), the N_MPI value could be wrong in either direction.

---

## VERIFIED CORRECT

### VC-1 — All 18 expected topology files present in `md/stage/`

`md/stage/` contains exactly: CPD1.inpcrd, CPD1.prmtop, CPD4.inpcrd, CPD4.prmtop, CPD7.inpcrd, CPD7.prmtop, CPD8.inpcrd, CPD8.prmtop, CPD9.inpcrd, CPD9.prmtop, CPD10.inpcrd, CPD10.prmtop, CPD11.inpcrd, CPD11.prmtop, CPD12.inpcrd, CPD12.prmtop, REF_85C.inpcrd, REF_85C.prmtop — 9 compounds × 2 files = 18 files, matching the expected count.

---

### VC-2 — CPD4 and CPD7 topology rebuilds are supported by present param files

`md/param/CPD4/` contains CPD4.frcmod, CPD4_v2.frcmod, CPD4.mol2, CPD4_fixed.mol2 plus intermediate antechamber files. `md/param/CPD7/` contains CPD7.frcmod, CPD7.mol2, CPD7_fixed.mol2. Both directories contain the artefacts expected from a completed antechamber+parmchk2 parameterisation. The presence of `CPD4_v2.frcmod` indicates a second parameterisation pass was performed for CPD4; only `CPD4_v2.frcmod` is expected to be the current one, but both versions are present on disk.

---

### VC-3 — RAYCA_OUT capture before module loads is confirmed for job-22076500

`job-22076500/step1_before.txt` shows `RAYCA_OUT` is captured in a variable at four checkpoints (BEFORE_MODULES, AFTER_Local-CSC, AFTER_amber_24cpu, AFTER_ALL_MODULES), all holding the same value. The known issue that `module load Local-CSC` unsets `RAYCA_OUT` is handled by saving it before any module load. Fix is correctly applied for this job.

---

### VC-4 — pmemd.MPI path confirmed on a LUMI compute node

`job-22076500/step1_before.txt` line 5: `/appl/local/csc/soft/chem/amber/24-cpu/bin/pmemd.MPI`. `slurm-22076619.log` confirms the same path in a compute-node environment and shows the smoke test passing (`rank OK` × 4, `SMOKE PASS`). pmemd.MPI is present and executable on LUMI compute nodes.

---

### VC-5 — AMBER residue numbering for CRBN W380 and GSPT1 K628 is consistent across all scripts

All cpptraj masks in all script versions examined use `:518@CA` for CRBN Trp380 and `:189@CA` for GSPT1 Lys628. Confirmed correct by `reports/audit_job_22076601_md_submission.md` (VC), `reports/audit_phase_fix_srun_mpi_lumi.md` (VC-1), and `reports/audit_job_22076601_lumi_md_submission.md` (VC-5). No off-by-one or 0-vs-1 numbering error is present in any examined script version.

---

### VC-6 — `read_col col=1` correctly reads the data column in cpptraj output

cpptraj distance and RMSD output: column 0 = frame index, column 1 = value in Å. `read_col(path, col=1)` with `p[1]` (0-indexed) reads the data column. Confirmed by `reports/audit_job_22076601_lumi_md_submission.md` (VC) and `reports/audit_phase_fix_srun_mpi_lumi.md` (VC-7).

---

### VC-7 — Module load sequence is confirmed correct on LUMI

`slurm-22076500.log` and `slurm-22076619.log` both show the sequence `module load Local-CSC` then `module load amber/24-cpu` succeeds, triggering the expected Lmod replacement chain (craype-x86-rome → craype-x86-milan; cce/19.0.0 → gcc-native/14.2; PrgEnv-cray/8.6.0 → PrgEnv-gnu/8.6.0) and loading Amber24 (CPU-version) with cray-mpich/8.1.32.

---

### VC-8 — `srun --ntasks=128 --cpus-per-task=1` step override correctly fixes the 16384-CPU bug

`slurm-22076619.log` records `SLURM_CPUS_PER_TASK=128` and `SLURM_NTASKS=unset`. With this environment, bare `srun -n 128` requests 128 × 128 = 16,384 CPUs per step. The override `--ntasks=128 --cpus-per-task=1` reduces the per-step request to 128 × 1 = 128 CPUs, matching the job allocation. The slurm log shows step 22076619.1 was allocated and started on nid001345 without a step-creation error, confirming the fix works.

---

### VC-9 — `continue` in `|| { ...; continue; }` correctly scopes to the enclosing for loop

Confirmed correct by `reports/audit_job_22076601_lumi_md_submission.md` (VC-3) and `reports/audit_phase_fix_srun_mpi_lumi.md` (VC-6). `{ ... }` is a compound command in the current shell; `continue` without an argument targets the nearest enclosing for/while/until loop. A srun failure aborts the current compound's pipeline and moves to the next compound.

---

### VC-10 — GSPT1 (residues 1–195) and CRBN (residues 196–575) mask ranges are consistent

All examined script versions use `:1-195` for GSPT1 and `:196-575` for CRBN in both nativecontacts and PPI-COM distance calls. Confirmed by `reports/audit_job_22076601_md_submission.md` (VC) and `reports/audit_phase_fix_srun_mpi_lumi.md` (VC-1). No mask transposition found.

---

## Finding Summary

| ID | Severity | Description |
|:---|:---|:---|
| CRIT-1 | CRITICAL | `iwrap=1` in prod.in; no `autoimage` in cpptraj analysis — RMSD and distances corrupted across periodic boundary |
| CRIT-2 | CRITICAL | Phase document records no script, no job IDs, no method; submitted scripts cannot be verified |
| MAJOR-1 | MAJOR | Phase document is substantively empty for a phase marked "complete" — no reproducible record |
| MAJOR-2 | MAJOR | cpptraj not confirmed in probe job 22076500 (step1_before.txt ends at pmemd.MPI path); confirmed only in later job 22076619 |
| MAJOR-3 | MAJOR | Job B compound assignment: CPD8 absent from jobB_log.txt; CPD10 present instead; composition cannot be verified |
| MAJOR-4 | MAJOR | Per-compound walltime estimate (4.22 ns/day → 22 h) derived from a single partially-complete CPD4 NVT run |
| MAJOR-5 | MAJOR | `except Exception: return "NA"` in verdict() silences all logic errors |
| MAJOR-6 | MAJOR | nativecontacts data generated but never read; verdict omits contact counts |
| MAJOR-7 | MAJOR | PPI COM distance computed but excluded from verdict; STABLE_GLUE possible with drifted protein-protein interface |
| MAJOR-8 | MAJOR | N_MPI=128 justified by 128-CPU cap stated as policy from a single probe observation |
| VC-1 | VERIFIED CORRECT | All 18 topology files present in md/stage/ |
| VC-2 | VERIFIED CORRECT | CPD4 and CPD7 param rebuild artefacts present |
| VC-3 | VERIFIED CORRECT | RAYCA_OUT saved before module loads in job-22076500 |
| VC-4 | VERIFIED CORRECT | pmemd.MPI path confirmed on LUMI compute node |
| VC-5 | VERIFIED CORRECT | AMBER residue numbers (W380=518, K628=189) consistent and correct across all scripts |
| VC-6 | VERIFIED CORRECT | `read_col col=1` reads data column, not frame-index column |
| VC-7 | VERIFIED CORRECT | Module load sequence confirmed correct on LUMI |
| VC-8 | VERIFIED CORRECT | `--ntasks=128 --cpus-per-task=1` step override correctly fixes the 16384-CPU allocation bug |
| VC-9 | VERIFIED CORRECT | `continue` scope in `\|\|` block correctly targets the for loop |
| VC-10 | VERIFIED CORRECT | GSPT1 (:1-195) and CRBN (:196-575) mask ranges consistent and non-transposed |

---

## Notes on audit brief checklist items not found in evidence

- **"2 ns/day performance estimate"**: No file examined contains "2 ns/day." The actual figure used throughout the session record is 4.22 ns/day. This audit reports only what the files show.
- **"1.75 days fits in 2-day walltime"**: Not found verbatim. The closest evidence is report.md which states 42.6 h/compound against a 48 h walltime cap. Reported under MAJOR-4.
- **Frame numbering in cpptraj**: `h = n // 2` last-half slice was verified as correct (3 ns from 6 ns production) in `audit_job_22076601_lumi_md_submission.md` VC-4. The `prod.in` in `job-22076619/md_work/inputs/` specifies 1 ns production (nstlim=500000, dt=0.002) with ntwx=2500, giving 200 frames; the production length differs across script versions.
- **Reversed pmemd.MPI flag assignments**: All pmemd.MPI calls examined were verified correct in `audit_phase_fix_srun_mpi_lumi.md` VC-2. No reversed flags found.
