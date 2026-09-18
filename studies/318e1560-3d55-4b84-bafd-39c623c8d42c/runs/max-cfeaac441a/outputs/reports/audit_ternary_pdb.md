
## Data provenance

| File | Source | Role |
|------|--------|------|
| 3MXF.pdb | RCSB, downloaded session | BD1 + JQ1 coordinates |
| 5T35.pdb | RCSB, downloaded session | VHL:ElonginCB + MZ1 coordinates |
| Rf, tf (transform) | Re-derived this phase from scratch | BD1→BD2 Kabsch rotation/translation |

Transform reproducibility confirmed: re-derived RMSD = 0.53 Å, identical to prior phase.

---

## Numerical checks

| Check | Expected | Observed | Pass? |
|-------|----------|----------|-------|
| VHL centroid displacement (chain B vs 5T35-D) | 0.00 Å | 0.00 Å | ✓ |
| ElonginC displacement | 0.00 Å | 0.00 Å | ✓ |
| ElonginB displacement | 0.00 Å | 0.00 Å | ✓ |
| BD1 centroid vs BD2 centroid | < 5 Å | 2.25 Å | ✓ |
| BD1–VHL centroid distance | 30–50 Å (chain-to-chain) | 39.4 Å | ✓ |
| Total ATOM+HETATM records | ~3,800–4,000 | 3,892 | ✓ |
| Waters/additives excluded | None present | None found | ✓ |

---

## What was excluded and why

| Excluded content | Reason |
|-----------------|--------|
| 5T35 chains E–H (second ASU copy) | Redundant; first copy (A–D) is sufficient |
| HOH, WAT, DMS, EDO, IOD records | Crystallographic additives not relevant to ternary model |
| BD2 atoms from 5T35 chain A | Replaced by transformed BD1 from 3MXF |
| Non-JQ1 HETATM from 3MXF (IOD, EDO, DMS) | Crystallographic additives |

---

## Known gaps

1. **No energy minimisation.** Side-chain clashes at the BD1–VHL interface are unresolved.
   Recommended next step: restrained minimisation (e.g. GROMACS `gmx grompp/mdrun` with
   position restraints on Cα, or Rosetta FastRelax) before any docking run.
2. **No linker modelled.** The file contains both warheads but no connecting chain.
3. **No clash report.** MolProbity or `gmx check` should be run before downstream use.
4. **Chain B MZ1 (759) is BD2-specific.** It is present for VHL warhead reference; a
   BD1-specific PROTAC warhead would differ at the BD-facing atoms.

---

## Reproducibility

All code in `018_pathlib_path.py`, `019_*.py`, `020_*.py` (session artifact store).
Random seed not required (deterministic transform). Re-running from 3MXF.pdb and
5T35.pdb with the same Kabsch procedure will produce an identical file.
