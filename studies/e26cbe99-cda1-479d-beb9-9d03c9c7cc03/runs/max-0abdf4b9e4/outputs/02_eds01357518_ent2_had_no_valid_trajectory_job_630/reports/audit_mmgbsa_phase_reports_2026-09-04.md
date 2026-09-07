# Audit: MM-GBSA Phase Report Writing — 2026-09-04

**Task:** Write phase report for all five MM-GBSA results  
**Date:** 2026-09-04  
**Status:** 4 of 5 compounds complete; EDS01357518_ent2 pending trajectory

---

## Documents Written This Session

| Document | Covers | Status |
|:---------|:-------|:-------|
| `phase_md_EDS01806218_ent1.md` | 10 ns MD trajectory for EDS01806218_ent1 (job 6319835); GROMACS Listed nonbonded warning; output files | Written |
| `phase_mmgbsa_EDS01806218_ent1.md` | cpptraj strip, MMPBSA.py result (−20.75 ± 2.59 kcal/mol), atom-count mismatch investigation, trajectory mis-staging diagnosis | Written |

## Pre-existing Documents Referenced

| Document | Covers |
|:---------|:-------|
| `phase_md_mmpbsa_EDS01806218_ent2.md` | EDS01806218_ent2 MD + MM-GBSA (job 6294174); ΔG = −25.22 ± 5.82 kcal/mol |
| `phase_mmgbsa_EDS01357518_ent1_EDS01889984.md` | EDS01889984 (−23.80 ± 2.64 kcal/mol, reliable) and EDS01357518_ent1 (+68.17 kcal/mol, topology defect) |
| `phase_md_resubmit_EDS01357518_ent2_EDS01806218_ent1.md` | History of trajectory losses and re-submissions |

---

## Findings Surfaced During This Session

1. **Job 6309346 mis-staged:** Labeled "EDS01357518_ent2 re-run" but ran from EDS01806218_ent1 prep files (29,241 atoms, matching `md_EDS01806218_ent1/` not `md_EDS01357518_ent2/` with 29,247). Discovered via atom-count audit across all session GRO files.

2. **Two EDS01806218_ent1 trajectories exist:** `npt_prod.6309346.xtc` (from mis-staged job) and `npt_prod_EDS01806218_ent1.xtc` (from job 6319835, correctly staged). The latter was used for MM-GBSA.

3. **EDS01806218_ent1 BOND artefact:** Absolute BOND energy ~17M kcal/mol in MMPBSA.py output, same GAFF2 artefact visible in the GROMACS Listed nonbonded warning. Does not affect single-trajectory ΔG (ΔBOND = 0 by construction). Result reliable for ranking.

4. **EDS01357518_ent2 has no valid trajectory:** Fresh MD submitted as Isambard job **6321629** (2026-09-04, ~90 min expected). Topology defect investigation pending; both EDS01357518 enantiomers carry a 1-4 VDW/exclusion error that yields unphysical AMBER VDW absolute terms — this must be addressed before MMPBSA.py is trusted for this compound.

---

## Container / Software Provenance

All MM-GBSA calculations ran in the Rayca platform's managed `rayca` mamba environment at `/home/ubuntu/rayca-runtime/.mamba/envs/rayca`. No external container image was invoked. Earlier in the session (2026-09-03), protonation-state predictions were produced by dispatched container tools (recorded in `.rayca-declared.jsonl`). Gnina docking was run via the platform's `gnina` AIDD container tool (image: `gnina`; results in `docked_*.sdf.gz`).

---

## Outstanding Items

| Item | Action required |
|:-----|:----------------|
| EDS01357518_ent2 trajectory | Await job 6321629; retrieve `npt_prod_EDS01357518_ent2.xtc` |
| EDS01357518 AMBER topology defect | Inspect `ligand.mol2` / `ligand.frcmod` for 1-4 exclusion error; rebuild prmtop; re-run MMPBSA.py |
| Final campaign summary | Update ranking table once ent2 result is available |
