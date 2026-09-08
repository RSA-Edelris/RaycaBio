# Audit: MM-GBSA MD Refinement of EL2003A Pose 2

**Audit date:** 2026-09-07  
**Script audited:** `mmgbsa_calc.py`  
**Result audited:** `mmgbsa_result.json`  
**Auditor method:** Independent review of script, JSON output, topology, MD parameters, and ParmEd source

---

## Findings

---

### CRITICAL (invalidates results)

None identified. The core computation (arithmetic, topology loading, index partitioning, unit handling) is mechanically correct and produces verifiable numbers. However, see MAJOR items below regarding parameter choices that diverge from the stated reference setup.

---

### MAJOR (may affect accuracy)

---

**MAJOR 1: Internal dielectric mismatch — reference uses ε_in = 4, script uses ε_in = 1**

The reference GBSA setup in `UNIGBSA/mmpbsa.in` specifies `intdiel = 4.0` (line 7 of mmpbsa.in). The script calls `obc2_context` with `soluteDielectric=1.0` (mmgbsa_calc.py line 74). The phase document records this parameter as `ε_in = 1, ε_out = 80` (MD_refinement_EL2003A_pose2.md line 39).

The reference value of 4 is the standard for polar protein interiors and is consistently recommended for GB calculations on protein–ligand complexes (Tsui & Case 2000); ε_in = 1 treats the protein as vacuum. This choice systematically overestimates electrostatic contributions. The phase document does not acknowledge the deviation from the reference.

Evidence: mmpbsa.in line 7 (`intdiel = 4.0`), mmgbsa_calc.py line 74 (`soluteDielectric=1.0`).

---

**MAJOR 2: Missing SASA non-polar solvation term**

The reference `mmpbsa.in` sets `surften = 0.0072` (line 29), indicating that the non-polar solvation free energy is computed via a surface-area dependent term. The script does not pass `useSASA=True` to `obc2_context`, so OpenMM defaults to `useSASA=False` (no SASA correction). This means the non-polar contribution to desolvation is entirely absent from the script's energies.

Evidence: mmpbsa.in line 29 (`surften = 0.0072`), mmgbsa_calc.py line 70–78 (no `useSASA` argument; ParmEd `createSystem` signature confirmed at structure.py line 2019 with default `useSASA=False`).

---

**MAJOR 3: Missing salt screening (0 M vs reference 0.15 M)**

The reference `mmpbsa.in` sets `saltcon = 0.15` M (line 9), applying Debye–Hückel ionic screening. The script does not pass `implicitSolventSaltConc` to `obc2_context`, defaulting to 0.0 mol/L (see ParmEd structure.py line 2015: `implicitSolventSaltConc=0.0*u.moles/u.liters`). At 0 M there is no Debye screening of charged groups, which overestimates the electrostatic contribution to binding relative to physiological 150 mM NaCl.

Evidence: mmpbsa.in line 9 (`saltcon = 0.15`), mmgbsa_calc.py line 70–78 (no `implicitSolventSaltConc` argument), ParmEd structure.py line 2015.

---

**MAJOR 4: Phase document convergence table contains an incorrect value at 200 ps**

The phase document `MD_refinement_EL2003A_pose2.md` (line 75) reports a running mean ΔG_bind of **−43.1 kcal/mol** at 200 ps (frame 20). The actual cumulative running mean of production frames 10–20 (100–200 ps), computed from `mmgbsa_result.json`, is **−40.625 kcal/mol** — a discrepancy of **2.5 kcal/mol**.

The 500 ps and 1000 ps entries in the same table are correct: running mean of frames 10–50 = −43.406 kcal/mol (document: −43.4) and frames 10–100 = −44.510 kcal/mol (document: −44.5).

The erroneous 200 ps value matters because it is the basis for the document's convergence claim. The actual data shows the running mean drifts from −40.6 (200 ps) to −44.5 (1000 ps), a range of ~4 kcal/mol, not the implied ~1.4 kcal/mol drift the document's numbers would suggest.

Evidence: mmgbsa_result.json frames 10–20 `dG_bind` values summed and divided by 11 = −40.625 kcal/mol. MD_refinement_EL2003A_pose2.md line 75 states −43.1.

---

**MAJOR 5: Equilibration cutoff of 100 ps not supported by convergence data**

The script discards the first 10 frames (0–90 ps) as equilibration (mmgbsa_calc.py line 119: `# Discard first 10 frames (100 ps equilibration)`). However, the per-frame data in `mmgbsa_result.json` shows that the production window itself has not equilibrated at 100 ps:

| Epoch | Frames | Mean dG (kcal/mol) | Stdev |
|---|---|---|---|
| "Equilibration" 0–90 ps | 0–9 | −41.03 | 1.74 |
| Early production 100–200 ps | 10–20 | −40.63 | 3.23 |
| Late production 800–1000 ps | 80–100 | −46.10 | 1.94 |
| Full production 100–1000 ps | 10–100 | −44.51 | 2.58 |

The early production frames (100–200 ps, mean −40.6 kcal/mol) are ~3.9 kcal/mol less negative than the late production frames (800–1000 ps, mean −46.1 kcal/mol). No RMSD convergence check or energy drift analysis was performed to validate this cutoff. The 100 ps rule is asserted without justification. A conservative analysis would extend the equilibration cutoff to 200–300 ps based on this data.

Evidence: mmgbsa_result.json per_frame entries, computed above.

---

**MAJOR 6: Print statement labels wrong frame range; script docstring claims wrong frame count**

Two labeling errors, neither affecting the actual computation but misleading in audit and reporting:

1. mmgbsa_calc.py line 126: `print(f"  Frames analysed    : {len(dGs_prod)} (frames 10–99, 100–1000 ps)")` — the production window is `dGs[10:]` over 101 total frames (indices 0–100), which yields frames 10–100 inclusive (91 frames). Frame 100 at t=1000 ps is included (confirmed: `mmgbsa_result.json per_frame[100]["time_ps"] = 1000.0`). The print statement says "frames 10–99" — it should say "frames 10–100."

2. mmgbsa_calc.py line 5 (docstring): `"ΔG_bind = mean(E_complex - E_receptor - E_ligand) over 100 frames (1 ns)"` — the actual production analysis uses 91 frames, not 100.

Evidence: mmgbsa_result.json `n_frames_total: 101`, `n_frames_prod: 91`, `per_frame[100]["time_ps"]: 1000.0`.

---

### VERIFIED CORRECT

---

**VERIFIED CORRECT 1: Phase document exists**

The task prompt asserts "No narrative document exists for this phase." This is incorrect. The file `MD_refinement_EL2003A_pose2.md` exists in the session directory and contains a full methods and results write-up including system preparation, MD protocol table, MM-GBSA parameters, binding free energy table, convergence table, and limitations section. The document covers objective, inputs, parameters, and findings as required.

Evidence: File found at `/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/MD_refinement_EL2003A_pose2.md`, 110 lines.

---

**VERIFIED CORRECT 2: Frame indexing — dGs[10:] correctly discards frames 0–9 and keeps frames 10–100**

`dGs` is built from `records` over `range(traj.n_frames)` = 101 iterations (mmgbsa_calc.py lines 100–113). `dGs[10:]` in Python produces a list of 91 elements corresponding to indices 10–100. Per `mmgbsa_result.json`: `n_frames_total: 101`, `n_frames_prod: 91`, and `per_frame[10]["time_ps"]: 100.0`. Frame 10 = t=100 ps, confirming the window "first 100 ps discarded, keep 100–1000 ps" is arithmetically implemented correctly.

Evidence: mmgbsa_calc.py lines 100, 120; mmgbsa_result.json `n_frames_prod: 91`, `per_frame[10]["time_ps"]: 100.0`.

---

**VERIFIED CORRECT 3: rec_idx and lig_idx partition all atoms correctly; row indexing is correct**

`lig_idx = [a.idx for a in gmx.atoms if a.residue.name == "MOL"]` and `rec_idx = [a.idx for a in gmx.atoms if a.residue.name != "MOL"]` are strict complements on the same `gmx.atoms` list (mmgbsa_calc.py lines 37–38). They are mutually exclusive by construction and their union covers all atoms. The PDB `complex_reres.pdb` has exactly 4730 ATOM/HETATM records (confirmed by `grep -c "^ATOM\|^HETATM"` = 4730), matching the reported topology atom count.

`xyz_nm` has shape `(n_atoms, 3)` (MDTraj frame indexed from `traj.xyz[i]` which is shape `(n_atoms, 3)`). `xyz_nm[rec_idx]` uses NumPy integer array indexing to select rows (atoms), returning shape `(len(rec_idx), 3)`. This correctly selects the receptor atom coordinates, not columns.

Evidence: mmgbsa_calc.py lines 37–38, 101–105; PDB record count = 4730; NumPy integer array indexing semantics.

---

**VERIFIED CORRECT 4: ParmEd Structure.createSystem signature accepts implicitSolvent, soluteDielectric, solventDielectric**

Inspected directly at `/home/ubuntu/rayca-runtime/.venv/lib/python3.12/site-packages/parmed/structure.py` lines 2008–2026. The signature is:

```python
def createSystem(self, nonbondedMethod=None,
                 nonbondedCutoff=8.0*u.angstroms,
                 ...
                 implicitSolvent=None,
                 ...
                 soluteDielectric=1.0,
                 solventDielectric=78.5,
                 ...
```

All three parameters used in the script (`implicitSolvent=app.OBC2`, `soluteDielectric=1.0`, `solventDielectric=80.0`) are valid keyword arguments. No signature error.

Evidence: parmed/structure.py lines 2008–2026.

---

**VERIFIED CORRECT 5: changeRadii fallback handles None/empty element_name without silent NaN propagation**

mmgbsa_calc.py line 57: `elem = a.element_name.capitalize() if a.element_name else 'C'`. If `a.element_name` is `None` or `""` (both falsy), the ternary assigns `'C'` before the dict lookup. Atoms that fall through with an unknown element are assigned the default `1.5` Å radius and `0.80` screen value (lines 58–59) via `.get(elem, 1.5)` and `.get(elem, 0.80)`. These are finite, valid floats. A failed `changeRadii` with this fallback will produce energies with slightly incorrect radii for unknown elements but will not produce NaN, inf, or exceptions that propagate silently.

The `except Exception as e:` block also prints the error (line 50), so the failure is not fully silent.

Evidence: mmgbsa_calc.py lines 49–59.

---

**VERIFIED CORRECT 6: MDTraj xyz units are nanometers — unit.nanometer multiplication is correct**

The MDTraj `Trajectory` class source at `/home/ubuntu/rayca-runtime/.venv/lib/python3.12/site-packages/mdtraj/core/trajectory.py` states:
- Line 690: `"Trajectory uses the nanometer, degree & picosecond unit system."`
- Line 733: `_distance_unit = "nanometers"`
- Line 725: `xyz : np.ndarray, shape=(n_frames, n_atoms, 3)` (units: nanometers)

The script accesses `traj.xyz[i]` (a frame slice of shape `(n_atoms, 3)` in nm) and multiplies by `unit.nanometer` to produce an OpenMM Quantity in nm. This is the correct usage.

Evidence: mdtraj/core/trajectory.py lines 690, 725, 733.

---

**VERIFIED CORRECT 7: ΔG formula sign is correct — frame 10 arithmetic verified exactly**

From `mmgbsa_result.json` frame 10:
- E_complex = −4709.752658636681 kcal/mol
- E_receptor = −4964.4246935524825 kcal/mol
- E_ligand = +293.2334563494832 kcal/mol
- Reported dG_bind = −38.561421433681915 kcal/mol

Computed: −4709.752658636681 − (−4964.4246935524825) − 293.2334563494832 = **−38.561421433681915 kcal/mol** (exact match, no floating-point discrepancy).

The formula `ΔG = E_complex − E_receptor − E_ligand` is physically correct: when the complex is more stable (more negative) than the separated partners, dG is negative. Here E_complex (−4709.75) < E_receptor + E_ligand (−4964.42 + 293.23 = −4671.19), giving a negative dG consistent with favorable binding.

Evidence: mmgbsa_result.json per_frame[10]; arithmetic verified by Python (difference = 0.0).

---

**VERIFIED CORRECT 8: complex_reres.pdb atom count matches GROMACS topology**

`grep -c "^ATOM\|^HETATM" complex_reres.pdb` = **4730**. The PDB is used as the MDTraj topology (`mdt.load(traj_path, top=pdb_file)`, mmgbsa_calc.py line 93), and the GROMACS topology is stated to have 4730 atoms. The atom counts are consistent; MDTraj will load the same number of atoms as ParmEd's GROMACS topology.

Evidence: shell command on complex_reres.pdb returns 4730; mmgbsa_calc.py line 34 prints atom count loaded by ParmEd.

---

## Summary Table

| Check | Status | Key evidence |
|---|---|---|
| 1. Missing phase document | **NOT A FINDING** — document exists | `MD_refinement_EL2003A_pose2.md` (110 lines) |
| 2. Frame indexing (dGs[10:], frame 10 = 100 ps) | VERIFIED CORRECT | JSON per_frame[10].time_ps = 100.0; n_frames_prod = 91 |
| 3. rec_idx/lig_idx partition (no overlap, no gap; row indexing) | VERIFIED CORRECT | 4730 PDB atoms = rec_idx + lig_idx; NumPy fancy indexing selects rows |
| 4. ParmEd createSystem signature (implicitSolvent etc.) | VERIFIED CORRECT | structure.py lines 2008–2026 |
| 5. changeRadii fallback silent failure | VERIFIED CORRECT | Fallback is finite, not silent; None/empty handled at line 57 |
| 6. Equilibration cutoff justified by convergence? | **MAJOR** | Frames 10–20 mean −40.6 vs frames 80–100 mean −46.1 (4 kcal/mol drift) |
| 7. Row vs column indexing (xyz_nm[rec_idx]) | VERIFIED CORRECT | Integer list indexes rows of (n_atoms, 3) array |
| 8. MDTraj xyz units (nm) | VERIFIED CORRECT | trajectory.py: _distance_unit = "nanometers" |
| 9. ΔG formula sign and arithmetic | VERIFIED CORRECT | Frame 10 exact match; formula sign correct |
| 10. PDB atom count vs GROMACS topology | VERIFIED CORRECT | Both = 4730 |
| Additional: soluteDielectric = 1.0 vs reference 4.0 | **MAJOR** | mmpbsa.in intdiel=4.0 vs script line 74 |
| Additional: SASA non-polar term absent | **MAJOR** | mmpbsa.in surften=0.0072 vs useSASA=False |
| Additional: Salt screening absent | **MAJOR** | mmpbsa.in saltcon=0.15 M vs default 0.0 M |
| Additional: Phase document running mean at 200 ps wrong | **MAJOR** | Doc: −43.1; actual: −40.6 kcal/mol (2.5 kcal/mol error) |
| Additional: Print statement frame range wrong | Minor | Line 126 says "frames 10–99"; should be "frames 10–100" |
| Additional: Script docstring wrong frame count | Minor | Docstring says "100 frames"; actual production uses 91 frames |
