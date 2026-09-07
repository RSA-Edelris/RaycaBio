
## Input

Five 2D V3000 Molfile structures from `P922_Results_2.sdf`, combined with the one molecule from `P922_Results.sdf` (phase 1) to produce a unified 6-molecule output file.

| Molecule | pIC50 (PDK1) | Source file |
|---|---|---|
| EL2003A-A2U1 | 7.6 | P922_Results.sdf |
| EL2003A | 7.9 | P922_Results_2.sdf |
| EL2003A-A4U1 | 7.3 | P922_Results_2.sdf |
| BX912 | 7.33 | P922_Results_2.sdf |
| EL5001A | 4.0 | P922_Results_2.sdf |
| EL5003A | 4.0 | P922_Results_2.sdf |

---

## Stereochemistry Analysis

`rdkit.Chem.FindMolChiralCenters` (with `includeUnassigned=True`) was run on each molecule after sanitization and stereo assignment.

| Molecule | Specified centers | Unspecified (racemic) | Action |
|---|---|---|---|
| EL2003A-A2U1 | — | — | Achiral; single conformer |
| EL2003A | — | — | Achiral; single conformer |
| EL2003A-A4U1 | — | — | Achiral; single conformer |
| BX912 | — | — | Achiral; single conformer |
| EL5001A | — | — | Achiral; single conformer |
| EL5003A | C11(R), C17(R) | — | Absolute config; single conformer, config retained |

**No enantiomers were generated.** EL5003A carries `MDLV30/STEABS ATOMS=(2 12 18)` in the input V3000 block together with stereo-bond `CFG` flags, encoding fully defined absolute R,R configuration. No molecule in either input file had unspecified (`?`) stereocenters.

---

## 3D Conformer Generation Protocol

| Setting | Value |
|---|---|
| Embedding | ETKDGv3, `numConfs=50`, `randomSeed=42`, `numThreads=4` |
| Minimisation | MMFF94, `maxIts=2000`, all 50 conformers |
| Selection | Lowest MMFF94 energy conformer |
| Hydrogens | Explicit (`Chem.AddHs`) before embedding; retained in output |

---

## Results

| Molecule | Confs embedded | Best MMFF94 (kcal/mol) | Z-range (Å) | Atoms (with H) |
|---|---|---|---|---|
| EL2003A-A2U1 | 50 | −80.5413 | −5.77 to +3.83 | 59 |
| EL2003A | 50 | −85.8421 | −3.13 to +3.67 | 56 |
| EL2003A-A4U1 | 50 | −61.7183 | −4.16 to +3.96 | 59 |
| BX912 | 50 | −102.6324 | −3.15 to +3.42 | 53 |
| EL5001A | 50 | −151.5602 | −2.36 to +2.45 | 49 |
| EL5003A | 50 | −154.3111 | −5.82 to +4.12 | 56 |

All 6 molecules verified as true 3D (non-zero Z-range) by read-back after writing.

---

## Output

**`ligand_clean_PDK1.sdf`** — 6 molecules, explicit hydrogens, 3D coordinates.

SDF properties per entry: `_Name`, `pIC50 PDK`, `MMFF94_energy_kcal_mol`, `Note`, `selection`.

---

## Audit Trail

| Script | Action |
|---|---|
| `042_chem_sdmolsupplier.py` | Load `P922_Results_2.sdf`; stereocentre analysis for all 5 molecules |
| `043_best_3d_conformer.py` | First conformer generation attempt; name-lookup issue identified |
| `044_re_define_conformer_function_lost_between_calls.py` | Fixed function scope; SDF read issue identified |
| `045_get_mol_name.py` | Final clean run: all 6 molecules processed, conformers written and verified |
| `ligand_clean_PDK1.sdf` | Final output (28.6 kB) |
