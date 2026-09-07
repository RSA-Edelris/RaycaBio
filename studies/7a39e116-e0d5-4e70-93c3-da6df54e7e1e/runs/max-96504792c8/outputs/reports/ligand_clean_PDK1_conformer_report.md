
## Input

| Field | Value |
|---|---|
| Source file | `P922_Results.sdf` |
| Molecule name | EL2003A-A2U1 |
| pIC50 (PDK1) | 7.6 |
| Input dimensionality | 2D (all Z = 0.0, V3000 Molfile) |

**SMILES:** `Cc1ccc(Nc2nc(NCCc3c[nH]cn3)c3nc[nH]c3n2)cc1NC(=O)N1CCCC1`

---

## Stereochemistry Analysis

`rdkit.Chem.FindMolChiralCenters` (with `includeUnassigned=True`) returned an empty list. The molecule contains:

- Two fused aromatic/heteroaromatic ring systems (pyrimidine + imidazole)
- A monosubstituted benzene (tolyl)
- A pyrrolidine urea side chain
- An ethylimidazole chain

None of these fragments carry an sp³ carbon with four distinct substituents. **The molecule is achiral — no stereocenters, no racemic mixture, no enantiomer required.**

---

## 3D Conformer Generation Protocol

| Step | Method / Setting |
|---|---|
| Hydrogen addition | `Chem.AddHs` (explicit H, 59 atoms total) |
| Embedding | ETKDGv3, `numConfs=50`, `randomSeed=42`, `numThreads=4` |
| Minimization | MMFF94, `maxIts=2000`, all 50 conformers minimized |
| Selection | Lowest MMFF94 energy conformer retained |

---

## Result

| Metric | Value |
|---|---|
| Conformers embedded | 50 |
| Best conformer index | 38 |
| MMFF94 energy (best) | −80.5413 kcal/mol |
| Z-coordinate range | −5.765 to +3.830 Å (confirmed true 3D) |
| Heavy atoms | 33 |
| Total atoms (with H) | 59 |

---

## Output File

**`ligand_clean_PDK1.sdf`** — single molecule, 3D coordinates, explicit hydrogens, with SDF properties:

| Property | Value |
|---|---|
| `_Name` | EL2003A-A2U1 |
| `pIC50 PDK` | 7.6 |
| `MMFF94_energy_kcal_mol` | −80.5413 |
| `Note` | No stereocenters; single enantiomer (achiral molecule) |

---

## Audit Trail

| File | Role |
|---|---|
| `001_load_molecule.py` | Load SDF and stereocentre enumeration |
| `002_work_single_molecule_already_mol_add_explicit.py` | ETKDGv3 embedding and MMFF94 minimisation of 50 conformers |
| `003_best_cid_38_best_energy_80_5413_mol_h_has_all_50.py` | Best-conformer selection, SDF write, verification read-back |
| `ligand_clean_PDK1.sdf` | Final output — lowest-energy 3D conformer |

---

## Decisions and Rationale

- **No enantiomer created:** RDKit found zero chiral centres; generating a mirror image of an achiral molecule produces the identical structure.
- **ETKDGv3 over ETKDGv2:** ETKDGv3 uses updated torsion-angle statistics and is the current RDKit default for drug-like molecules.
- **50 conformers, MMFF94 minimisation:** Sufficient to sample low-energy conformational space for a molecule of this size (MW ≈ 420); MMFF94 is well-validated for drug-like small molecules and avoids the overhead of a quantum mechanical single-point.
- **Explicit hydrogens retained in output:** Required for downstream docking tools (gnina, Glide) that expect all-atom input.
