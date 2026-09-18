## Scope

This audit covers the local parameterisation (antechamber, parmchk2) and solvated system build (tleap) for all 9 ternary-complex MD systems, and the staging tarball delivered to LUMI.

## Container image used for docking (phase 2, referenced here for completeness)

Gnina docking was performed using the containerised tool dispatched via `run_aidd_tool`. The tool ID is **`gnina`**. The exact image digest is not surfaced by the platform API, but the session artifact registry records the call under tool ID `gnina` (entries `gnina_docked.sdf.gz` in `01_characterise_5hxb_crystal_structure_and_85c_bind/structures`).

## Inputs verified before parameterisation

| System | Ligand source | Hydrogens | Notes |
|---|---|---|---|
| REF_85C | 5HXB crystal 85C | RDKit AddHs | Crystal pose, docked-frame coordinates |
| CPD1 | lig_00_Compound_1_poses.sdf pose 1 | AddHs(addCoords=True) | |
| CPD4 | lig_01_Compound_4_poses.sdf pose 1 | SDF retained coords | Has sp alkyne carbon c1 |
| CPD7 | lig_02_Compound_7_poses.sdf pose 1 | SDF retained coords | Had missing frcmod (see below) |
| CPD8 | lig_03_Compound_8_poses.sdf pose 1 | AddHs(addCoords=True) | |
| CPD9 | lig_04_Compound_9_poses.sdf pose 1 | AddHs(addCoords=True) | |
| CPD10 | lig_05_Compound_10_poses.sdf pose 1 | SDF retained coords | |
| CPD11 | lig_06_Compound_11_poses.sdf pose 1 | AddHs(addCoords=True) | |
| CPD12 | lig_07_Compound_12_poses.sdf pose 1 | AddHs(addCoords=True) | |

## antechamber settings

- Force field: GAFF2 (`-s gaff2`)
- Charge method: AM1-BCC (`-c bcc`)
- Net charges: all 0 (verified from SDF)
- sqm run locally (sqm fails on LUMI compute nodes — see audit_phase_04)
- Mol2 coordinates injected from AddHs output where SDF had no 3D coords

## parmchk2 settings

All 9 ligands: `parmchk2 -i {LIG}_fixed.mol2 -f mol2 -o {LIG}.frcmod -s gaff2 -a Y`

The `-a Y` flag is required for sp-hybridised alkyne carbon (GAFF2 type `c1`) attached to conjugated-amine nitrogens (`n`, `ns`). Without it, tleap raises "No torsion terms" for atom quartets including `c1-ce-n-c`, `c1-c-ns-hn`, etc.

## Failures encountered and fixed

### CPD4 — 11 missing torsions

- **Root cause**: initial parmchk2 run without `-a Y` omitted torsions for `c1-ce-n-c`, `c1-ce-n-c1`, `c1-c-ns-hn`, `c-ns-c-c1`
- **Fix**: rerun with `-a Y`; analogues found, e.g. `c1-ce-n-c: 4  6.600  180.000  2.000  same as X-n-cc-X`
- **Verified**: tleap built CPD4 system (127k atoms) without warnings

### CPD7 — missing frcmod entirely

- **Root cause**: parmchk2 had silently not written the file during the batch run
- **Fix**: `parmchk2 -i CPD7_fixed.mol2 -f mol2 -o CPD7.frcmod -s gaff2 -a Y` → 3099 bytes
- **Verified**: tleap built CPD7 system without warnings

## tleap build results

All 9 systems built successfully with:
- Water model: TIP3P (truncated octahedron, 12 Å buffer)
- Salt: 150 mM NaCl (50 Na+ + 50 Cl- counter-ions + neutralisation ions)
- Total atoms per system: ~127,000
- Prmtop size: ~22 MB each

Residue numbering in prmtop: GSPT1 1–195, CRBN 196–575, LIG 576.

## AMBER input decks

| Stage | nstlim | dt (ps) | Total time | Restraints |
|---|---|---|---|---|
| min | 10 000 cycles | — | — | 5 kcal/mol Å⁻² on CA,C,N,O |
| heat | 50 000 | 0.002 | 100 ps | 5 kcal/mol Å⁻² on CA,C,N,O |
| equil | 100 000 | 0.002 | 200 ps | 1 kcal/mol Å⁻² on CA,C,N,O |
| prod | 500 000 | 0.002 | 1 ns | none |

## Staging tarball

- File: `systems_stage.tar.gz` (29.9 MB)
- Contents: `inputs/{min,heat,equil,prod}.in` + `systems/{LIG}/system.prmtop` + `systems/{LIG}/system.inpcrd` for all 9 ligands
- Delivered to LUMI via `inputs` parameter of `run_on_cluster`

## LUMI job

- Job ID: 22076147
- Partition: standard (CPU-only, 128 cores, 48 h)
- Execution: 9 background subshells, srun -n 64 each, 2 concurrent at any time
- Analysis: inline cpptraj after all MD tasks complete
- Expected outputs per compound: `{sys}_rmsd_lig.dat`, `{sys}_dist_W380_LIG.dat`, `{sys}_dist_K628_LIG.dat`, `{sys}_dist_PPI.dat`
