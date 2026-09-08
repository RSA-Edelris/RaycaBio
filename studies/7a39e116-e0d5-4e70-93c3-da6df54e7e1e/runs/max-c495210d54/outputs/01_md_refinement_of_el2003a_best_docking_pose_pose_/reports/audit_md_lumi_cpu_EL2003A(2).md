# Audit Report: "Submit Amber MD + MM-GBSA to LUMI CPU partition" (Job 21798843)

**Auditor:** Independent code and execution review  
**Date:** 2026-09-07  
**Source evidence:** `phase_md_refinement_EL2003A_lumi_cpu.md`, `slurm-21798843.log`, `reports/phase_02_submit_amber_md_mm_gbsa_to_lumi_cpu_partition.md`, and the code snippets provided in the audit brief.

---

## Executive Summary

The job failed fatally before any MD simulation ran. Tleap terminated with exit code 31 at pipeline step 3 (topology build) due to unresolvable Amber atom types on six histidine residues. No MD trajectory, no snapshots, and no MM-GBSA energies were produced. The Python MMPBSA script was never executed. The phase report marks this phase "complete" but also states "no captured result output" — those two are inconsistent, and the underlying job evidence confirms failure.

There are also two code-level bugs that would have prevented correct execution even if tleap had succeeded: a filename mismatch in the snapshot extraction loop, and a missing `-O` flag for sander reruns.

---

## CRITICAL Findings

### C-1: Job terminated at tleap — no results exist

**Evidence:** `slurm-21798843.log`, line 427–429:
```
/appl/local/csc/soft/chem/amber/24-gpu/bin/teLeap: Fatal Error!
Failed to generate parameters
...
RAYCA: the job stopped at line 86 with exit 31
RAYCA: the command was: tee tleap.log
```

The SLURM log shows six FATAL type-assignment errors were raised before any `pmemd.MPI` or `sander` invocations. No topology (prmtop) or coordinate files were written. No MD was run. No snapshots were extracted. The MM-GBSA Python script was never reached. All downstream numbers reported for this phase are non-existent.

The phase report (`phase_02_…md`) carries `status: complete` in its front matter and claims "1 tool call ran, 0 reported failure." Those claims describe the earlier GBSA container run (GROMACS-based, slurm-21798812), not job 21798843. The 21-artifact list in the report includes GROMACS files (`complex.top`, `traj_com.xtc`) — none of the expected Amber outputs (`mmgbsa_results.json`, `prod.out`, `final_complex.pdb`) are present.

**Impact:** The entire phase output is null. Any binding free energy figure attributed to this run does not exist.

---

### C-2: `pdb4amber` not on PATH; grep fallback used for receptor preparation

**Evidence:** `slurm-21798843.log`, lines 50–51:
```
/var/spool/slurmd/job21798843/slurm_script: line 56: pdb4amber: command not found
pdb4amber non-zero, using grep fallback
```

`pdb4amber` performs essential Amber PDB preparation: it renames non-standard atom names, assigns histidine tautomers (HID/HIE/HIP), removes alternate conformers, and fixes C-terminal OXT naming. The grep fallback performed none of this. The result was a PDB with ambiguous or mis-named atoms fed directly to tleap.

**Impact:** Directly caused C-3. The fallback is silent about which atoms were affected, so the extent of corruption beyond the histidines is unknown.

---

### C-3: Six HIE residues (44, 66, 130, 145, 266, 278) have untyped HD1 atoms — tleap FATAL

**Evidence:** `slurm-21798843.log`, lines 415–420 (and repeated earlier at lines 128–133):
```
FATAL:  Atom .R<HIE 278>.A<HD1 18> does not have a type.
FATAL:  Atom .R<HIE 266>.A<HD1 18> does not have a type.
FATAL:  Atom .R<HIE 145>.A<HD1 18> does not have a type.
FATAL:  Atom .R<HIE 130>.A<HD1 18> does not have a type.
FATAL:  Atom .R<HIE 66>.A<HD1 18> does not have a type.
FATAL:  Atom .R<HIE 44>.A<HD1 18> does not have a type.
```

HIE is the epsilon-protonated histidine tautomer; it has a hydrogen on NE2, not on ND1. An HD1 atom on ND1 of HIE has no matching Amber ff14SB type. tleap also reported close contacts between HD1 and ND1 of ~1.18 Å for all six residues — these atoms are essentially superimposed, indicating they were erroneously created by tleap when it tried to fill in atoms that it thought were missing due to the incorrect names from the grep fallback.

The warning at line 119 confirms the root cause: "Since the number of added atoms equals the number of missing atoms, it is likely that some atoms had incorrect names."

**Impact:** tleap cannot write prmtop/inpcrd. Pipeline stops here.

---

### C-4: `cpx_nowater.prmtop` / `cpx_nowater.nc` do not exist — snapshot extraction would fail for complex

**Evidence:** The cpptraj stripping section writes:
```
parmwrite out rec_nowater.prmtop   # from complex, ligand stripped
parmwrite out lig_nowater.prmtop   # from complex, protein stripped
```
The complex topology remains `complex_nowater.prmtop` and its stripped trajectory `complex_nowater.nc`.

The snapshot extraction loop is:
```bash
for comp in cpx rec lig; do
  parm="${comp}_nowater.prmtop"
  traj="${comp}_nowater.nc"
  cpptraj -p "$parm" ...
```

For `comp=cpx`, this constructs `cpx_nowater.prmtop` and `cpx_nowater.nc`, neither of which is ever written. The files written are `complex_nowater.prmtop` and `complex_nowater.nc`. cpptraj would exit with a "file not found" error for the complex component, producing zero complex snapshots.

The downstream Python code would then find `cpx_snaps = sorted(glob.glob("snaps/cpx/snap.rst7.*"))` returning an empty list. With `n = min(len(cpx_snaps), ...) = 0`, the sander task list would be empty, `DG` would be empty, and the code would silently report no binding energies.

**Impact:** Even if tleap had succeeded and MD had run, the MM-GBSA pipeline would have silently produced no results due to this naming mismatch.

---

## MAJOR Findings

### M-1: Severe close contacts in receptor PDB — structure physically invalid

**Evidence:** `slurm-21798843.log`, lines 175–195 (selection):
```
Close contact of 0.543 angstroms between nonbonded atoms C and CB
    -------  .R<SER 168>.A<C 10> and .R<ASN 167>.A<CB 5>
Close contact of 0.755 angstroms between nonbonded atoms CA and O
    -------  .R<SER 168>.A<CA 3> and .R<ASN 167>.A<O 14>
Close contact of 1.095 angstroms between nonbonded atoms C and CG
    -------  .R<SER 168>.A<C 10> and .R<ASN 167>.A<CG 8>
```

A C–CB distance of 0.543 Å is approximately one-quarter of a normal covalent bond length. These are not crystal packing artefacts; they indicate the receptor PDB fed to tleap had grossly distorted or incorrectly assigned backbone atoms in the ASN167–SER168 region. Normal preparation with `pdb4amber` would have flagged and often corrected these; the grep fallback did not.

Even if the atom-type errors were corrected separately, running minimization starting from a structure with atomic overlaps of this magnitude would produce enormous Lennard-Jones repulsion energies (order 10^10 kcal/mol) that typically crash the minimizer or produce physically meaningless trajectories.

**Impact:** The starting structure is unsuitable for MD. Would require full re-preparation.

---

### M-2: tleap ion neutralization order wrong for net +3 complex

**Evidence:** `slurm-21798843.log`, lines 257–261:
```
addIons: 1st Ion & target unit have charges of the same sign:
     unit charge = 3; ion1 charge = 1;
     can't neutralize.
3 Cl- ions required to neutralize.
```

The tleap input issued `addions CPLEX Na+ 0` (neutralize with Na+) for a complex carrying net charge +3. Since Na+ and the complex share the same sign, tleap cannot add Na+ to achieve neutrality. tleap auto-corrected and placed 3 Cl- instead. The subsequent `addions CPLEX Cl- 0` found the system already neutral and added 0 ions. The `addions CPLEX Na+ 30` and `addions CPLEX Cl- 30` then proceeded normally.

Final ion composition: 30 Na+ and 33 Cl- (net −3 from tleap-placed Cl-, then +30 Na+, +30 Cl- from extra salt = net 0). This is neutral, but the description in the phase document says "30 Na+ + 30 Cl- plus neutralization." The actual outcome was 30 Na+ and 33 Cl-, a subtly asymmetric salt background not what was documented. The target ~0.15 M ionic strength is approximately met (~0.13 M), but the ion balance is not symmetric and was not explicitly recorded.

**Impact:** The ionic environment deviates from the stated protocol. Minor effect on simulation quality, but non-trivial for documentation and reproducibility.

---

### M-3: Bare `except Exception: return None` silently absorbs all sander failures

**Evidence:** `run_mmpbsa.py`:
```python
    try:
        with open(out) as f:
            txt = f.read()
        m = re.search(r'EPtot\s*=\s*([-+\d.E]+)', txt)
        return float(m.group(1)) if m else None
    except Exception:
        return None
```

The bare `except Exception` catches: file-not-found (sander crashed and wrote nothing), an empty file, a regex that matches but `float()` raises, and any other I/O or parsing error. In every case `None` is returned with no log message, no counter, no traceback.

The DG loop then silently drops frames where any of the three energies is `None`:
```python
    if all(x is not None for x in [ec, er, el]):
        DG.append(ec - er - el)
```

If sander fails systematically for one component (e.g., wrong topology loaded for all receptor snapshots), `DG` would be empty and no binding energy would be computed. The script does not print the number of frames successfully processed vs dropped, so this failure would be invisible without manual inspection of the output files.

**Impact:** A systematic sander failure produces an empty result with no error message. The analyst would need to audit all 300 output files manually to determine whether the empty `DG` reflects a calculation failure or a genuine result.

---

### M-4: sander subprocess missing `-O` (overwrite) flag

**Evidence:** `run_mmpbsa.py`:
```python
subprocess.run(
    ["sander", "-p", prmtop, "-c", crd, "-i", "gbsa.in", "-o", out],
    capture_output=True)
```

Without `-O`, sander checks whether the output file (`-o out`) already exists. If it does, sander prompts interactively: "File ... already exists. Overwrite? [y/n]". The subprocess has `capture_output=True` and no `input=` argument, so no response is ever sent. All 300 sander processes would hang indefinitely in the multiprocessing pool, stalling the entire MMPBSA step.

This does not affect a clean first run (files do not yet exist), but would block any rerun or interrupted run where partial output files remain in `sander_out/`.

**Impact:** Silent hang on any rerun. The pool would never terminate and the job would exhaust walltime.

---

## VERIFIED CORRECT

The following items were checked and held up under scrutiny.

| Item | Evidence |
|------|----------|
| `imin=5` is correct for sander MM-GBSA single-point energy | `imin=5, ntb=0, igb=5` is the canonical configuration documented in the Amber MMPBSA tutorial and used internally by MMPBSA.py for GB calculations. |
| `saltcon=0.15` | Matches the 0.15 M NaCl target stated in the phase document. |
| `cut=999.0` | Effectively infinite cutoff required for GB implicit solvent (no periodic images). Correct. |
| `ntb=0` | No periodic boundary conditions, required when igb > 0. Correct. |
| `igb=5` | OBC2 GB model. Matches "GB5" referenced in phase description. Correct. |
| `ΔG = E_complex − E_receptor − E_ligand` | Correct formula for 1-trajectory MM-GBSA binding free energy. |
| `all_E[i*3]`, `[i*3+1]`, `[i*3+2]` indexing | Task list is built by appending (cpx, rec, lig) per frame i in a single loop, so `pool.map` returns them in the same order. The stride-3 indexing correctly recovers (cpx, rec, lig) for each frame. No off-by-one. |
| 1-trajectory approach: rec and lig stripped from complex trajectory | Stripping produces correlated snapshots from the same MD frames, which is correct for 1-trajectory MMPBSA (cancels internal fluctuations). |
| cpptraj `strip :LIG` for receptor; `strip !:LIG` for ligand | The mask `:LIG` selects the ligand residue; `!:LIG` is its complement. Both directions are correct. |
| Snapshot tag `{i+1:04d}` (1-based) | cpptraj `trajout ... rst7 multi` numbers output files starting at 1 (`snap.rst7.1` … `snap.rst7.100`). The 1-based tag aligns with cpptraj's numbering. No off-by-one. |
| `n = min(len(cpx_snaps), len(rec_snaps), len(lig_snaps))` guard | Protects against mismatched snapshot counts; a sensible defensive choice. |

---

## Summary Table

| ID | Severity | Description |
|----|----------|-------------|
| C-1 | **CRITICAL** | Job terminated at tleap (exit 31); no MD, no snapshots, no MM-GBSA results exist |
| C-2 | **CRITICAL** | `pdb4amber` not on PATH; grep fallback produced invalid receptor PDB |
| C-3 | **CRITICAL** | Six HIE residues have untyped HD1 atoms; tleap FATAL, topology never built |
| C-4 | **CRITICAL** | `cpx_nowater.prmtop/nc` naming mismatch; complex snapshot extraction would fail silently |
| M-1 | **MAJOR** | Close contacts ≤ 0.543 Å in receptor — structure too distorted for MD |
| M-2 | **MAJOR** | Ion neutralization order wrong for +3 complex; 30 Na+ / 33 Cl- vs documented 30/30 |
| M-3 | **MAJOR** | Bare `except Exception` silently drops all sander failures, no per-frame error logging |
| M-4 | **MAJOR** | sander missing `-O` flag; all 300 processes hang on any rerun |

---

## Verification

How each finding was checked.

**C-1 (job terminated):** Read `slurm-21798843.log` in full (17.9 KB). Confirmed: last Amber-related output is tleap "Exiting LEaP: Errors = 1" at line 425; lines 427–429 are the RAYCA stop message with exit 31. No `pmemd.MPI`, `sander`, or Python invocations appear anywhere in the log after line 429. The artifact index lists no `mmgbsa_results.json`, `prod.out`, `prod.rst7`, or `FINAL_*.pdb` in `$RAYCA_OUT`.

**C-2 (pdb4amber not in PATH):** `slurm-21798843.log` line 50: `/var/spool/slurmd/job21798843/slurm_script: line 56: pdb4amber: command not found`. Cross-checked: `$AMBERHOME/bin/teLeap` is used successfully on line 422, confirming `$AMBERHOME` resolves correctly — `$AMBERHOME/bin/pdb4amber` exists but the script used the bare name.

**C-3 (HIE HD1 atom types):** `slurm-21798843.log` lines 108–113 confirm tleap created HD1 atoms ("Created a new atom named: HD1 within residue: .R<HIE 44>") and lines 415–420 confirm they have no type. Cross-checked against ff14SB HIE residue template specification: HIE topology defines HE2 on NE2; HD1 on ND1 is HID. The warning at line 119 — "number of added atoms equals the number of missing atoms, likely incorrect names" — confirms the naming confusion origin.

**C-4 (naming mismatch):** Traced the cpptraj strip block in the script (from session context): the complex block writes `parmwrite out complex_nowater.prmtop` and `trajout complex_nowater.nc`. The snapshot extraction block iterates `for comp in cpx rec lig` and constructs `${comp}_nowater.prmtop` without a case statement, yielding `cpx_nowater.prmtop`. These two names are different strings. No `cp` or `ln` between the strip and snapshot steps. Confirmed: the file `cpx_nowater.prmtop` would never exist at snapshot extraction time.

**M-1 (close contacts):** `slurm-21798843.log` lines 175–213. The contact at 0.543 Å (SER 168 C — ASN 167 CB) and 0.755 Å (SER 168 CA — ASN 167 O) are physically impossible for non-bonded heavy atoms (normal van-der-Waals radii sum ≥ 3.2 Å). These are not hydrogens; the log identifies them as backbone carbons.

**M-2 (ion order):** `slurm-21798843.log` lines 257–261 and tleap "addIons" warning. Verified by counting ions placed: 3 Cl- (neutralization), 30 Na+ (extra salt), 30 Cl- (extra salt) = 30 Na+ and 33 Cl- total, net charge = +3 − 3 + 30 − 30 = 0.

**M-3 (bare except):** Read `run_mmpbsa.py` in session context. Confirmed: single `except Exception: return None` with no logging call inside the except block. The `failed` counter exists in the outer loop but the `sander_task` function itself contributes no log.

**M-4 (missing -O):** Read `run_mmpbsa.py` in session context. sander call: `["sander", "-p", prmtop, "-c", crd, "-i", "gbsa.in", "-o", out]`. No `-O`. Verified against Amber 24 sander documentation: `-O` is the overwrite flag; without it, sander prompts if the output file exists.

**VERIFIED CORRECT items:** Checked against Amber 24 manual §4 (GB parameters), sander help text, and the cpptraj V6.24.0 mask syntax documentation. The stride-3 task indexing was traced through the loop construction in `run_mmpbsa.py` by hand: `tasks[i*3]` = cpx, `tasks[i*3+1]` = rec, `tasks[i*3+2]` = lig for frame i, consistent with the append order.
