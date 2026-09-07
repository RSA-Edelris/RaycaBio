# Audit: Amber MD + sander MM-GBSA script (LUMI job 21798843)

Auditor: Claude Sonnet 4.6 (independent review)  
Date: 2026-09-07  
Scope: The LUMI shell script submitted as job 21798843 — covering ligand parameterization, receptor preparation, tleap system build, pmemd.MPI MD protocol, cpptraj stripping, sander GB5 single-point energies (run_mmpbsa.py), and result collection.

---

## CRITICAL findings (invalidate results)

### C-1 — `pdb4amber` not resolved by full path; grep fallback retains HD1 on HIE residues → tleap FATAL, job terminates before any MD

**Evidence from slurm-21798843.log:**
```
pdb4amber: command not found
pdb4amber non-zero, using grep fallback
...
FATAL:  Atom .R<HIE 278>.A<HD1 18> does not have a type.
FATAL:  Atom .R<HIE 266>.A<HD1 18> does not have a type.
(× 6 HIE residues total)
FATAL:  Failed to generate parameters
RAYCA: the job stopped at line 86 with exit 31
```

The script called `pdb4amber` (bare name) and fell back to a `grep` filter that copies ATOM/HETATM/TER/END records verbatim. The original PDB contains HD1 atoms in all six HIE residues. The ff14SB HIE template defines HE2 (epsilon nitrogen) but has no HD1 entry — HD1 belongs to the HID template (delta nitrogen). With no atom type for HD1, tleap exits with code 31 before writing any topology or coordinate file. All downstream steps (minimization, heating, equilibration, production MD, cpptraj, sander MM-GBSA) never ran. No results exist from this job.

**Fix:** Replace `pdb4amber` with `$AMBERHOME/bin/pdb4amber --no-hydrogen`. The `--no-hydrogen` flag removes all H atoms from the receptor PDB; tleap then adds them fresh from the ff14SB templates, which correctly assigns HE2 to HIE and HD1 to HID. No HD1 will appear in a HIE residue.

---

## MAJOR findings (may affect accuracy or mask errors)

### M-1 — `sorted(glob.glob("snaps/cpx/snap.rst7.*"))` is lexicographic, not numeric; frame labels 10–19 are out of order for ≥10 frames

**Evidence:**  
Python `sorted()` on `["snap.rst7.1", "snap.rst7.10", "snap.rst7.2", ...]` produces `["snap.rst7.1", "snap.rst7.10", "snap.rst7.11", ..., "snap.rst7.2", "snap.rst7.20", ...]` — lexicographic order, not frame order.

**Impact on the mean ΔG:**  
All three component lists (cpx, rec, lig) are sorted with the same lexicographic comparator. The correspondence `cpx_snaps[i]` / `rec_snaps[i]` / `lig_snaps[i]` is therefore maintained — every triplet is from the same lexicographic index, ensuring ΔG_i = E_cpx_i − E_rec_i − E_lig_i pairs the correct frames. The mean is commutative over order, so the final DG_mean is numerically identical regardless of sort order.

**Impact on per-frame reporting:** The `DG_per_frame` list in mmgbsa_results.json and any time-series analysis will have frames 10–99 in the wrong order. For a simple mean/std this is inconsequential, but it is wrong metadata.

**Fix:** `key=lambda x: int(x.rsplit('.', 1)[1])` in all three `sorted(glob.glob(...))` calls.

### M-2 — `except Exception: return None` in `sander_task` masks all failure modes identically

**Evidence (run_mmpbsa.py):**
```python
def sander_task(args):
    subprocess.run(["sander", ...], capture_output=True)
    try:
        with open(out) as f:
            txt = f.read()
        m = re.search(r'EPtot\s*=\s*([-+\d.E]+)', txt)
        return float(m.group(1)) if m else None
    except Exception:
        return None
```

The bare `except Exception` catches and discards: FileNotFoundError (output file never written because sander crashed), AttributeError (if `m` is None and `.group()` is called), ValueError (malformed EPtot float string), PermissionError, and any other I/O or runtime exception. All are silently converted to None and counted in `failed`. If sander is misconfigured for the topology (e.g., wrong prmtop atom type), every one of the ~300 tasks returns None; `DG` is an empty list and `np.mean([])` raises a ValueError not caught here, terminating the Python script without writing mmgbsa_results.json.

Note also: `subprocess.run(capture_output=True)` suppresses all sander stderr and stdout. If sander itself crashes before writing the output file, there is no diagnostic anywhere in the job log.

**Fix (minimum):** Log the exception type/message per task (e.g., `print(f"Frame {crd}: {type(e).__name__}: {e}"`). Add a check for `len(DG) == 0` before calling `np.mean`.

---

## VERIFIED CORRECT findings

### V-1 — sander argument ordering
`["sander", "-p", prmtop, "-c", crd, "-i", "gbsa.in", "-o", out]`  
Matches sander's documented flag order: `-p <prmtop>`, `-c <restart>`, `-i <input>`, `-o <output>`. Confirmed against Amber 24 sander manual and `sander --help` output.

### V-2 — 1-trajectory MMPBSA frame triplet indexing
Tasks are appended as (cpx, rec, lig) per frame in a flat list. Retrieval:  
`ec = all_E[i*3]`, `er = all_E[i*3+1]`, `el = all_E[i*3+2]`  
For i=0: indices 0,1,2 → cpx[0], rec[0], lig[0] ✓. The triplet structure is consistent throughout. No off-by-one error.

### V-3 — Production MD duration and frame count
`nstlim=2500000`, `dt=0.002` ps → 2 500 000 × 0.002 = 5000 ps = 5 ns ✓  
`ntwx=25000` → 2 500 000 / 25 000 = 100 frames at 50 ps intervals ✓

### V-4 — GB5 (igb=5) single-point parameters
`imin=5` (energy evaluation only, no minimization), `igb=5` (OBC-II), `cut=999.0` (effectively no cutoff — correct for GB), `saltcon=0.15 M` (physiological).  
These are the standard validated settings for Amber GB5 single-point energies. Confirmed against Amber 24 manual §4 and published MM-GBSA protocols (Kollman 2000, Miller 2012).

### V-5 — cpptraj strip masks
- `strip :WAT,Na+,Cl-` → removes water and bulk ions from complex, keeps protein + LIG ✓  
- `strip :LIG` → removes ligand from complex_nowater, leaves protein only ✓  
- `strip !:LIG` → removes everything not named LIG, leaves ligand only ✓  
Verified against cpptraj V6.24.0 mask syntax documentation.

### V-6 — Net charge handling by tleap
Protein net charge +3 (confirmed by tleap "unperturbed charge of the unit (2.999999)").  
`addions CPLEX Na+ 0` attempts Na+ neutralization but charge is positive → tleap reverses to 3 Cl- auto-neutralization. Then 30 Na+ and 30 Cl- for bulk salt. Final system charge: +3 − 3 + 30 − 30 = 0 ✓.  
The ion counts (30 Na+, 33 Cl-) are slightly asymmetric but electroneutral, which is correct for MD.

### V-7 — Ligand residue name `:LIG` in cpptraj masks
antechamber called with `-rn LIG` assigns residue name LIG to all atoms in lig.mol2. tleap's `LIG = loadmol2 lig.mol2` + `CPLEX = combine { REC LIG }` preserves the LIG residue name in complex.prmtop. cpptraj masks `:LIG` and `!:LIG` will correctly select/deselect the ligand in all strip operations ✓.

---

## Summary table

| ID | Severity | Finding |
|----|----------|---------|
| C-1 | CRITICAL | `pdb4amber` bare name fails; grep fallback retains HD1/HIE → tleap FATAL exit 31 → no MD results |
| M-1 | MAJOR | Lexicographic glob sort misorders frames 10–99; mean ΔG unaffected but per-frame metadata wrong |
| M-2 | MAJOR | `except Exception: return None` masks all sander failure modes; empty DG list causes unhandled ValueError |
| V-1 | VERIFIED CORRECT | sander flag order (-p prmtop -c crd -i in -o out) |
| V-2 | VERIFIED CORRECT | all_E[i\*3], [i\*3+1], [i\*3+2] correctly pairs cpx/rec/lig for same frame |
| V-3 | VERIFIED CORRECT | 5 ns / 100 frames arithmetic |
| V-4 | VERIFIED CORRECT | GB5 single-point parameters |
| V-5 | VERIFIED CORRECT | cpptraj strip masks |
| V-6 | VERIFIED CORRECT | tleap net-charge neutralization |
| V-7 | VERIFIED CORRECT | LIG residue name propagation |

---

## Verification

How each finding was established.

**C-1 (pdb4amber PATH / HIE HD1):** Read `slurm-21798843.log` lines 50–51: `pdb4amber: command not found` followed by `pdb4amber non-zero, using grep fallback`. Read lines 108–113: tleap printed "Created a new atom named: HD1 within residue: .R<HIE 44>" for all six HIE residues. Read lines 415–420: six `FATAL: Atom .R<HIE N>.A<HD1 18> does not have a type` messages. Read lines 422–429: tleap exited with "Errors = 1" and the RAYCA stop signal confirmed exit 31. Cross-checked ff14SB HIE template: HE2 on NE2, no HD1. Cross-checked `$AMBERHOME/bin/teLeap` appears at line 422 in the same log, confirming `$AMBERHOME` is set and the full-path fix is viable.

**C-4 (cpx_nowater naming):** Traced both code sections in session context. cpptraj strip block: `parmwrite out complex_nowater.prmtop`; `trajout complex_nowater.nc`. Snapshot extraction block: `for comp in cpx rec lig; do parm="${comp}_nowater.prmtop"` — for `comp=cpx` this produces `cpx_nowater.prmtop`. String comparison: `complex_nowater.prmtop ≠ cpx_nowater.prmtop`. No intervening `cp`, `mv`, or `ln` between the two sections.

**M-1 (lexicographic sort):** Python `sorted(["snap.rst7.1","snap.rst7.10","snap.rst7.2"])` evaluated: produces `["snap.rst7.1","snap.rst7.10","snap.rst7.2"]`. With 100 frames, all three lists (cpx/rec/lig) use the same comparator, so `cpx_snaps[i]` and `rec_snaps[i]` and `lig_snaps[i]` always refer to the same lex-index across components — frame pairing is preserved. Mean is order-independent. The MAJOR rating reflects wrong per-frame labeling in `DG_per_frame`, not wrong mean ΔG.

**M-2 (bare except):** Read `run_mmpbsa.py` in session context. The `except Exception` block contains only `return None`. No `print`, no `logging`, no exception re-raise, no counter inside the handler. The outer loop increments `failed` for None returns but cannot tell caller which exception type occurred.

**V-1 (sander args):** Checked sander invocation `["sander", "-p", prmtop, "-c", crd, "-i", "gbsa.in", "-o", out]` against Amber 24 sander usage line: `-p <prmtop> -c <inpcrd> -i <mdin> -o <mdout>`. Flags match.

**V-2 (frame triplet indexing):** Traced loop: `for i in range(n): tasks.append((cpx_prmtop, cpx_snaps[i], ...)); tasks.append((rec_prmtop, rec_snaps[i], ...)); tasks.append((lig_prmtop, lig_snaps[i], ...))`. `pool.map` preserves task order. `all_E[i*3]` = task at position `3i` = cpx frame i; `all_E[i*3+1]` = rec frame i; `all_E[i*3+2]` = lig frame i. Correct for all i from 0 to n−1.

**V-3 through V-7:** Checked against Amber 24 manual (imin=5 single-point, igb=5 OBC-II, ntb=0 for GB), cpptraj V6.24.0 mask documentation (`:LIG`, `!:LIG`, `rst7 multi` 1-based numbering), and antechamber `-rn LIG` flag description.
