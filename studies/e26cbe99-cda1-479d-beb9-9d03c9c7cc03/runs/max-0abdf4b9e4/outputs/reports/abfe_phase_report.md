## Scope

Absolute binding free energy (double-decoupling with Boresch restraints) for three CRBN-pocket compounds ready for simulation: **EDS01806218_ent1**, **EDS01806218_ent2**, and **EDS01889984**. Two further compounds (EDS01357518_ent1 and EDS01357518_ent2) are not included in this phase due to preparation blockers described below.

---

## System preparation

### Force field and topology
- Protein: ff14SB (AMBER port to GROMACS)
- Ligand: GAFF2, AM1-BCC charges via ACPYPE
- Water: TIP3P, periodic box, ~150 mM NaCl
- Each complex system: ~20,000 atoms solvated and neutralised

### Starting structures
For each compound the following files were produced and staged at the session root:

| File pattern | Contents |
|---|---|
| `{NAME}_abfe_start.gro` | Equilibrated complex starting coordinates |
| `{NAME}_complex_abfe.top` | GROMACS topology with `[ intermolecular_interactions ]` Boresch restraints |
| `{NAME}_index.ndx` | GROMACS index with `Protein_LIG` and `Water_and_ions` groups |
| `{NAME}_lig_solv.gro` | Ligand-in-water box for solvent leg |
| `{NAME}_lig_solv.top` | Ligand-in-water topology |

### Boresch restraint anchors and force constants (k = 4184 kJ mol⁻¹ nm⁻²)

| Compound | r1–r2–r3 (protein) | l1–l2–l3 (ligand) | r0 (nm) |
|---|---|---|---|
| EDS01806218_ent1 | atoms from CRBN pocket | — | 0.8406 |
| EDS01806218_ent2 | atoms from CRBN pocket | — | 0.8128 |
| EDS01889984 | atoms from CRBN pocket | — | 0.7066 |

Boresch analytical standard-state corrections:
- EDS01806218_ent1: **+7.33 kcal/mol**
- EDS01806218_ent2: **+7.36 kcal/mol**
- EDS01889984: **+7.89 kcal/mol**

### Lambda schedule (17 windows)
```
COUL: [0, 0.25, 0.50, 0.75, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
VDW:  [0, 0,    0,    0,    0, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.85,0.9,0.95,1]
```
Production per window: 750,000 steps × 2 fs = 1.5 ns. `calc-lambda-neighbors = -1` enables MBAR overlap with all windows.

### Key MDP settings resolved during preparation
- `rcoulomb` / `rvdw` = **1.2 nm** (raised from 1.0 to prevent rlist auto-expansion exceeding pair-list cutoff)
- `couple-intramol = yes` (changed from `no` to prevent GROMACS 2026.1 exclusionchecker failure for flexible ligands; intramolecular terms cancel between legs, ΔG_bind is unchanged)
- `couple-moltype = LIG`, `couple-lambda0 = vdw-q`, `couple-lambda1 = none`
- Boresch bond in `[ intermolecular_interactions ]`: **ftype 6** (harmonic restraint, not ftype 1 harmonic bond — ftype 1 creates 1-2 exclusions, rejected by GROMACS 2026.1)
- Complex leg `tc-grps = Protein_LIG Water_and_ions` (requires index.ndx); solvent leg `tc-grps = System`

---

## Compounds excluded from this phase

| Compound | Reason |
|---|---|
| EDS01357518_ent1 | GAFF2 topology defect: incorrect 1-4 exclusions in the ACPYPE output; requires manual itp repair before ABFE prep |
| EDS01357518_ent2 | No equilibrated complex available; a 10 ns production MD run (job 6324829) was submitted and has **completed** — trajectory available for Boresch anchor selection and ABFE prep in the next phase |

---

## Jobs submitted (attempt 3 — all fixes applied)

| Job ID | Compound | Leg | Walltime | Status at phase close |
|---|---|---|---|---|
| 6325310 | EDS01806218_ent1 | complex | 300 min | **running** (window 02+ in progress) |
| 6325329 | EDS01806218_ent2 | complex | 300 min | running |
| 6325334 | EDS01889984 | complex | 300 min | running |
| 6325340 | EDS01806218_ent1 | solvent | 150 min | running |
| 6325348 | EDS01806218_ent2 | solvent | 150 min | running |
| **pending** | EDS01889984 | solvent | 150 min | blocked by 20-job platform limit; submit once a slot opens |

Prior attempts (1 and 2) failed due to: `$RAYCA_INPUTS` staging path not set (attempt 1); ftype 1 bond in `[ intermolecular_interactions ]` rejected by GROMACS 2026.1 (attempt 2 complex); rlist too small for `couple-intramol=no` with large flexible ligand (attempt 2 solvent). All three issues resolved in attempt 3.

---

## MBAR analysis plan (post-simulation)

Script: `abfe_mbar_analysis.py` at session root. Uses alchemlyb 2.5.0 + pymbar 4.0.3.

Formula:
```
ΔG°_bind = (ΔG_solvent_MBAR − ΔG_complex_MBAR) × kT + ΔG°_restr_analytic
```

Expected output files: `complex_{NAME}_win{00-16}_dhdl.xvg` and `solvent_{NAME}_win{00-16}_dhdl.xvg` collected into `$RAYCA_OUT` by each job.
