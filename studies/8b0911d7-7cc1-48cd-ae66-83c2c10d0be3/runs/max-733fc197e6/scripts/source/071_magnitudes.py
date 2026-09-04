
verification_block = """

### Verification

**Sign and magnitude.** E_complex < E_receptor for both compounds → ΔG is
negative → binding is favourable. ΔG_MM-GBSA magnitudes (−24 to −25 kcal/mol)
are in the expected range for single-point enthalpic OBC2 estimates in the
literature (Genheden & Ryde, 2015). Ligand self-energies (+120 to +147 kcal/mol)
are positive, consistent with a compact organic molecule in GB continuum with
no explicit solvation — expected for this method.

**Pre-minimisation sanity check.** Raw E_complex before minimisation was
+7 × 10⁶ kcal/mol for Cpd32 R (severe steric clashes from rigid docking),
confirming that the 500-step minimisation was necessary and effective.

**Ranking vs experiment.**

| Method | Cpd16 R more potent | ΔΔG |
|--------|---------------------|-----|
| ASMS experiment | Yes (Kd <1 µM vs 1–5 µM) | ~1–2 kcal/mol |
| AutoDock-Vina | Yes | −0.79 kcal/mol |
| MM-GBSA (this section) | Yes | −0.66 kcal/mol |

All three agree on direction. The relative ranking is robust to method.

**sqm convergence failure — resolved.** AM1-BCC charge calculation (antechamber/sqm)
failed for Cpd16 R on PDBQT-derived coordinates (SCF non-convergence after 1000 steps).
Root cause: strained docked-pose geometry. Fixed by running antechamber on a
fully-optimised MMFF geometry, then patching mol2 coordinates to the docked pose.
Both compounds completed successfully in the final run (rc=0).
"""

report_path = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/docking_report.md'
with open(report_path, 'a') as fh:
    fh.write(verification_block)

import os, subprocess
print("Report size:", os.path.getsize(report_path), "bytes")

# sync to artifact dir
dst = '/home/ubuntu/rayca-artifacts/c43f8bb507fc1b0b669eeb63/files/docking_report.md'
r = subprocess.run(['cp', report_path, dst], capture_output=True, text=True)
print("cp:", r.returncode)

# also copy the phase report
r2 = subprocess.run([
    'cp',
    '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/phase_08_mmgbsa_free_energy.md',
    '/home/ubuntu/rayca-artifacts/c43f8bb507fc1b0b669eeb63/files/phase_08_mmgbsa_free_energy.md'
], capture_output=True, text=True)
print("cp phase report:", r2.returncode)
