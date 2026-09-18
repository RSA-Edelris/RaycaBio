## Scope

Phase "Fix srun MPI allocation bug and resubmit AMBER MD to LUMI", covering the correction of the `--cpus-per-task` / srun interaction bug and the subsequent submission of job 22076604, followed by its cancellation and replacement by job 22076930 after an independent audit caught a second critical defect.

This document also serves as the audit record for the phase, as required by the stop-hook obligation.

---

## Findings from independent audit

The audit was run as a separate subagent with no shared assumptions about what was correct.

### CRITICAL-1 — Missing `autoimage` with `iwrap=1` (fixed before wasted walltime)

`prod.in` (confirmed in tarball at `max-0fcb897abb/in/systems_stage.tar.gz`) contains `iwrap=1`, which wraps each atom independently back to the primary unit cell at every trajectory write step. The cpptraj analysis block in job 22076604 had no `autoimage` call before computing RMSD or any distances. Without reassembly, any component of the ternary complex that migrated across a periodic boundary would yield wrong geometry. Job 22076604 was cancelled after 16 minutes (minimisation of REF_85C only); job 22076930 was submitted with `autoimage anchor :576` inserted before the first `rms` command.

### CRITICAL-2 — Phase document empty

`reports/phase_02_fix_srun_mpi_allocation_bug_and_resubmit_amber_m.md` contained only "No method records were captured". No phase document recording the method existed. This audit document serves as the record.

### MAJOR-1 — Silent `except Exception: return "NA"` in `verdict()` (fixed)

Any Python error inside verdict thresholds returned "NA" silently, masking bugs in the verdict logic. Fixed in job 22076930: explicit `if "NA" in (...)` guard returns `"no_data"`, then `float()` conversions are unguarded so they raise visibly.

### MAJOR-2 — `ppi_com_A` not in verdict thresholds (noted, not changed)

The GSPT1–CRBN CoM distance is computed and reported but not used in verdict classification. A compound could be classified STABLE_GLUE while the two proteins have dissociated. This threshold is left unset because no reference value from the equilibrated crystal complex has been established in this run; adding an unvalidated threshold would be worse than omitting it. The raw `ppi_com_A` column is present in the summary table for manual inspection.

### MAJOR-3 — Smoke test uses 4 tasks (acceptable)

The smoke test runs `srun --ntasks=4 --cpus-per-task=1 hostname`. Job 22076930 upgrades this to `--ntasks=128` so the step that succeeds is identical in resource footprint to the production steps. Low practical risk in either case since the prior failure mode (step rejection) would manifest at 4 tasks too under the original bug.

### VERIFIED CORRECT

- `--ntasks=128 --cpus-per-task=1` on each srun call correctly overrides the job-level `--cpus-per-task=128`; verified by job 22076604 running for 16 min before cancellation (step was accepted).
- All cpptraj residue masks `:576`, `:518@CA`, `:189@CA`, `:1-195`, `:196-575` match the AMBER numbering: GSPT1 1–195, CRBN 196–575, LIG 576, CRBN-W380 = res 518, GSPT1-K628 = res 189.
- `rms first :1-575@CA` followed by `rms lig_rmsd :576&!@H= nofit` is the correct two-step protein-fit + ligand-RMSD protocol.
- pmemd.MPI flag ordering and checkpoint chain (inpcrd→min→heat→equil→prod) is correct.
- `!@H=` is the correct cpptraj heavy-atom wildcard.
- `parse_col2` reads column index 1 (values), not 0 (frame numbers).
- `prod.nc` is now included in the per-system collection so re-analysis is possible without rerunning MD.

---

## Job lineage

| Job | Elapsed | Outcome | Reason |
|-----|---------|---------|--------|
| 22076331 | 1 s | FAILED | srun cpus-per-task bug |
| 22076435 | 21 s | FAILED | same bug |
| 22076604 | 16 min | CANCELLED | autoimage missing (CRIT-1) |
| **22076930** | submitted | **running** | all critical fixes applied |
