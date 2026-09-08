# Phase 3: Failure Analysis and Corrected Resubmission — EL2003A Amber MD + MM-GBSA

**Study:** PDK1 / EL2003A MD refinement (run max-2b162eedac)  
**Date:** 2026-09-07  
**Author:** Claude Sonnet 4.6  
**Prior phase:** Phase 2 — Submit Amber MD + MM-GBSA to LUMI CPU partition (job 21798843)  
**This phase produces:** Corrected LUMI job 21798969 (128 CPUs, 16 h, `small` partition)

---

## Objective

Diagnose the failure of LUMI job 21798843, audit the submitted script, fix all identified bugs, and resubmit a corrected job.

---

## Background

The target is EL2003A pose 2 — the best-ranked docking pose for EL2003A against PDK1 (PDB 1Z5M), with GNINA affinity −9.80 kcal/mol and static MM-GBSA (EM mode) ΔG = −61.835 kcal/mol. The goal is explicit-solvent Amber MD refinement followed by 1-trajectory MM-GBSA on the MD ensemble to obtain a dynamic binding free energy estimate.

---

## Failure Analysis: Job 21798843

### What was submitted

A LUMI `small`-partition CPU job (128 tasks, 8 h walltime) running:
1. antechamber / parmchk2 — GAFF2 ligand parameterisation
2. pdb4amber — receptor PDB preparation
3. tleap — solvated complex topology build (TIP3PBOX 12 Å, ff14SB + GAFF2 + TIP3P, ~0.15 M NaCl)
4. pmemd.MPI — minimisation (2×) → heating (100 ps) → equilibration (500 ps) → production (5 ns, 100 frames)
5. cpptraj — strip water/ions; extract per-frame rst7 snapshots
6. sander (parallel, Python multiprocessing) — GB5 single-point energies per frame
7. Result collection — mmgbsa_results.json, FINAL_complex.pdb, FINAL_lig.pdb

### What actually ran

The job terminated at **tleap** (pipeline step 3), exit code 31. Reading `slurm-21798843.log` (17.9 KB):

- Line 50–51: `pdb4amber: command not found` → grep fallback used for receptor preparation
- Lines 108–113: tleap created HD1 atoms on all six HIE residues (HIE 44, 66, 130, 145, 266, 278)
- Lines 415–420: six `FATAL: Atom .R<HIE N>.A<HD1 18> does not have a type`
- Line 422: `teLeap: Fatal Error! Failed to generate parameters`
- Line 427: `RAYCA: the job stopped at line 86 with exit 31`

**No pmemd.MPI, cpptraj, sander, or Python steps ran.** No topology, trajectory, snapshot, or MM-GBSA result files were produced.

### Root cause

`pdb4amber` was invoked by bare name (`pdb4amber`) rather than its full path (`$AMBERHOME/bin/pdb4amber`). Even though the `amber/24-gpu` module was loaded, `pdb4amber` was not placed in `$PATH`. The fallback was a `grep` filter that copied ATOM/HETATM/TER/END records verbatim — it does not rename non-standard atoms or remove incorrect hydrogens. The source PDB (`1Z5M_receptor_pH7.4.pdb`) contains HD1 atoms on its six HIE residues. HIE (epsilon-protonated histidine) requires HE2 on NE2; HD1 on ND1 belongs to HID. The ff14SB HIE template has no HD1 entry, so tleap could not assign an atom type and exited fatally.

### Additional bugs found by audit

Two further bugs were identified that would have prevented correct results even if tleap had succeeded:

**C-4 (naming mismatch):** The cpptraj strip step wrote `complex_nowater.prmtop` / `complex_nowater.nc` for the desolvated complex. The snapshot extraction loop constructed filenames as `${comp}_nowater.prmtop` for `comp ∈ {cpx, rec, lig}`, yielding `cpx_nowater.prmtop` for the complex component — a file that is never written. cpptraj would fail silently; `cpx_snaps` would be empty; `n = min(...) = 0`; the sander task list would be empty; no binding energies would be computed.

**M-4 (missing sander -O):** The sander subprocess call in `run_mmpbsa.py` lacked the `-O` (overwrite) flag. On any rerun where partial output files remain in `sander_out/`, sander would prompt interactively. With `capture_output=True` and no `input=` argument, all 300 processes would hang indefinitely, exhausting walltime.

Full audit findings are in:
- `audit_amber_md_mmpbsa_script.md` (4 CRITICAL, 2 MAJOR, 7 VERIFIED CORRECT)
- `audit_md_lumi_cpu_EL2003A.md` (4 CRITICAL, 4 MAJOR, 10 VERIFIED CORRECT)

---

## Corrected Script: Changes Applied

| Bug | Fix |
|-----|-----|
| C-2/C-3: pdb4amber bare name → HD1/HIE FATAL | `$AMBERHOME/bin/pdb4amber --no-hydrogen`; awk fallback strips ` HD1` from `HIE` records |
| C-4: `complex_nowater.*` vs `cpx_nowater.*` naming mismatch | Consistent `cpx_nowater.*` prefix throughout; case statement in snapshot loop |
| M-4: sander missing `-O` flag | Added `-O` to every sander invocation |
| M-1 (sort): lexicographic glob sorts frames 10–99 out of order | `key=lambda x: int(x.rsplit('.',1)[1])` numeric sort |
| M-3 (except): bare `except Exception` masks failures silently | Per-exception type + message logging; `sys.exit(1)` when `len(DG) == 0` |

---

## Resubmission: Job 21798969

| Parameter | Value |
|-----------|-------|
| Cluster | LUMI (`small` partition, CPU-only) |
| SLURM job ID | **21798969** |
| CPUs | 128 |
| GPUs | 0 |
| Walltime requested | 16 h (960 min) |
| Inputs staged | `EL2003A_pose2.sdf`, `1Z5M_receptor_pH7.4.pdb` |
| Status at submission | `submitted` |

Walltime increased from 8 h to 16 h because 5 ns NPT production of a ~37 K-atom TIP3P system at 128 CPU cores is estimated to take 8–20 h depending on Amber/24 MPI performance on LUMI Milan nodes.

---

## Expected Outputs (if successful)

All written to `$RAYCA_OUT = /scratch/project_462001483/`:

| File | Contents |
|------|----------|
| `mmgbsa_results.json` | DG_mean ± DG_std kcal/mol, n_frames, per-frame DG array, method metadata |
| `prod.out` | Amber production MD output (energy, temperature, pressure time series) |
| `prod.rst7` | Final restart coordinate file |
| `FINAL_complex.pdb` | Last MD frame, desolvated complex (protein + LIG) |
| `FINAL_lig.pdb` | Last MD frame, ligand only |
| `tleap.log` | tleap system-build log (for verification) |
| `pdb4amber.err` | pdb4amber stderr (for verification) |

---

## Open Items

- **Job 21798969 in queue/running.** Results will be processed when the job completes.
- Audit obligation for the prior phase (phase 2) is satisfied by `audit_md_lumi_cpu_EL2003A.md` and `audit_amber_md_mmpbsa_script.md`, both with Verification sections.

---

## Verification

- `slurm-21798843.log` read in full (430 lines, 17.9 KB); all critical and major findings are grounded in specific line numbers cited in the audit files.
- Corrected script submitted via `run_on_cluster`; tool confirmed job ID 21798969, state `submitted`, cluster LUMI, workdir `/scratch/project_462001483/rayca/max-2b162eedac`.
- The two audit files (`audit_amber_md_mmpbsa_script.md`, `audit_md_lumi_cpu_EL2003A.md`) and the CPU connectivity test (`cpu_test.txt`) each have Verification sections confirming how their claims were established.
