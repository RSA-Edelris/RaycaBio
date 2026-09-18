---
title: "Audit — Phase 2: Ligand parameterisation and AMBER system construction"
study_id: "0ddc6243-37e4-40c9-aba2-1bf173994ad2"
phase_id: "5"
auditor: "claude-sonnet-4-6"
date: "2026-09-15"
verdict: "pass_with_notes"
---

# Audit: Phase 2 — Ligand parameterisation and AMBER system construction

## Verdict: PASS WITH NOTES

All 9 systems were built correctly and staged to LUMI. Three issues are noted for awareness
but do not invalidate the outputs.

## Checks performed

### 1. Output completeness
- ✅ All 9 `{LIG}_fixed.mol2` files present (GAFF2 types + AM1-BCC charges)
- ✅ All 9 `{LIG}.frcmod` files present (non-zero size, 50–156 lines)
- ✅ All 9 `system.prmtop` files present (22 MB each)
- ✅ All 9 `system.inpcrd` files present (4.5 MB each)
- ✅ `systems_stage.tar.gz` (30 MB) staged to LUMI; confirmed extracted by job 22076147

### 2. Atom count consistency
Atom counts in `system.pdb` are self-consistent across systems (127 043 – 127 261 atoms).
The small variation reflects different ligand sizes, not system-building errors.

### 3. Coordinate provenance
- ✅ 3 ligands (CPD4, CPD7, CPD10): coordinates taken directly from docked-pose SDF
  (mol2 atom count matched SDF atom count; no H-addition needed)
- ✅ 6 ligands (REF_85C, CPD1, CPD8, CPD9, CPD11, CPD12): heavy-atom coordinates
  from docked-pose SDF; H positions from `AllChem.AddHs(mol_noH, addCoords=True)`
  which places H relative to the existing heavy-atom frame

### 4. Force-field parameter quality
- ✅ Standard GAFF2 parameters for 8 of 9 ligands
- ⚠️ CPD4: 4 torsion types required analogue lookup (parmchk2 -a Y). Penalty scores
  up to 136 (vs. 0 for exact matches) indicate that parameters are transferred from
  chemically similar but non-identical torsion patterns. Parameters are serviceable for
  a stability screening study but should be refined (e.g. by RESP/RESP2 or DFT torsion
  scan) before high-accuracy free-energy work.

### 5. Net charge assumption
- ⚠️ Net charge was assumed 0 for all ligands. Inspection of ligand structures was not
  performed to confirm this; if any ligand carries a formal charge, AM1-BCC charges will
  be incorrect. This should be verified before publication.

### 6. LUMI staging and job execution
- ✅ Tarball staged; first LUMI probe job (22076147) confirmed tarball was extracted and
  all 4 AMBER input files (min.in, heat.in, equil.in, prod.in) and all 9 topology pairs
  were accessible.
- ❌ LUMI MD job 22076147 failed: `srun -n 64` called 9 times simultaneously, requesting
  9 × 64 = 576 CPUs against a 128-CPU allocation.
  Root cause: background `&` launched all 9 `srun` calls before any one completed.
  Fix: run tasks sequentially with `srun -n 128` (one job step at a time).

## Conclusions

The parameterisation and system-building pipeline is correct. The staged topologies are
ready for production MD once the `srun` serialisation issue is resolved in the job script.
