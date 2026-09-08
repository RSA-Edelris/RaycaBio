
## Input

| File | Molecules |
|---|---|
| `P922_Results.sdf` (phase 1) | EL2003A-A2U1 |
| `P922_Results_2.sdf` (this phase) | EL2003A, EL2003A-A4U1, BX912, EL5001A, EL5003A |

**Combined output: 6 molecules in `ligand_clean_PDK1.sdf`**

---

## Stereochemistry Analysis

| Molecule | Chiral Centers | Status | Action |
|---|---|---|---|
| EL2003A-A2U1 | None | Achiral | Single conformer |
| EL2003A | None | Achiral | Single conformer |
| EL2003A-A4U1 | None | Achiral | Single conformer |
| BX912 | None | Achiral | Single conformer |
| EL5001A | None | Achiral | Single conformer |
| EL5003A | C11(R), C17(R) | **Absolute config** (`MDLV30/STEABS`) | Single conformer, config retained |

**No enantiomers were generated.** EL5003A carries two stereocenters with fully defined absolute (R,R) configuration encoded in the V3000 `MDLV30/STEABS` collection and confirmed by RDKit `FindMolChiralCenters`. All other molecules are achiral.

---

## 3D Conformer Generation Protocol

| Parameter | Value |
|---|---|
| Method | ETKDGv3 + MMFF94 minimisation |
| Conformers per molecule | 50 |
| Random seed | 42 |
| Threads | 4 |
| Minimisation iterations | 2000 |
| Selection criterion | Lowest MMFF94 energy |
| Hydrogen treatment | Explicit (AddHs before embedding) |

---

## Results

| Molecule | pIC50 (PDK1) | Confs embedded | Best MMFF94 (kcal/mol) | Z-range (Å) | Heavy atoms | Chiral centers |
|---|---|---|---|---|---|---|
| EL2003A-A2U1 | 7.6 | 50 | −80.5413 | −5.77 to +3.83 | 33 | — |
| EL2003A | 7.9 | 50 | −85.8421 | −3.13 to +3.67 | 32 | — |
| EL2003A-A4U1 | 7.3 | 50 | −61.7183 | −4.16 to +3.96 | 36 | — |
| BX912 | 7.33 | 50 | −102.6324 | −3.15 to +3.42 | 30 | — |
| EL5001A | 4.0 | 50 | −151.5602 | −2.36 to +2.45 | 26 | — |
| EL5003A | 4.0 | 50 | −154.3111 | −5.82 to +4.12 | 29 | C11(R), C17(R) |

All molecules verified as true 3D (non-zero Z-range) on read-back.

---

## Output File

**`ligand_clean_PDK1.sdf`** — 6 molecules, explicit hydrogens, 3D coordinates, SDF properties:
`_Name`, `pIC50 PDK`, `MMFF94_energy_kcal_mol`, `Note`, `selection`

---

## Audit Trail

| File | Role |
|---|---|
| `042_chem_sdmolsupplier.py` | Load P922_Results_2.sdf and stereocentre analysis |
| `043_best_3d_conformer.py` | First attempt at ETKDGv3 + MMFF94 (name lookup issue identified) |
| `044_re_define_conformer_function_lost_between_calls.py` | Fixed name lookup; identified file read issue |
| `045_get_mol_name.py` | Final clean run: all 6 molecules processed and verified |
| `ligand_clean_PDK1.sdf` | Final output — lowest-energy 3D conformers for all 6 PDK1 ligands |

---

## Decisions and Rationale

- **EL5003A: no enantiomer created.** The V3000 `MDLV30/STEABS ATOMS=(2 12 18)` declaration and stereo bond `CFG` flags encode absolute R,R configuration. RDKit confirmed both centers as R with no unspecified `?` label. Inverting a fully-specified absolute center would produce a different compound, not an enantiomeric pair of a racemic mixture.
- **Explicit Hs retained in output** for compatibility with downstream docking (gnina, Glide, AutoDock).
- **50 conformers** is sufficient for molecules of this size (MW 350–500); sampling is not rate-limiting at this scale.
