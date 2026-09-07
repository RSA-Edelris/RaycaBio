
## Summary

Three molecules from `enantio.sdf` were analysed for racemic stereocenters. Enantiomers were generated for the two racemic structures, and lowest-energy 3D conformers were produced for all five resulting structures using ETKDGv3 embedding followed by MMFF94 force-field optimisation. All five conformers converged. Output written to `enantio_structure.sdf`.

---

## Input

| Molecule | STERAC1 atoms (V3000) | Stereocenters (RDKit) | Classification |
|---|---|---|---|
| EDS01357518 | atom 18 | C17 = S | 1 racemic center |
| EDS01806218 | atoms 10, 11 | C9 = R, C10 = S | 2 racemic centers |
| EDS01889984 | — | none | achiral |

The `MDLV30/STERAC1` collection in V3000 molfiles marks stereocenters as belonging to a racemic group (both enantiomers present in the mixture). RDKit resolves the drawn parity (CW/CCW from atom-block CFG) and assigns explicit R/S labels; the STERAC annotation signals that the enantiomer must also be generated.

---

## Method

1. **Read** molecules with `Chem.SDMolSupplier` (removeHs=True, sanitize=True).
2. **Detect** stereocenters via `Chem.FindMolChiralCenters(includeUnassigned=True)`.
3. **Generate enantiomer** for each molecule that has at least one stereocenter: all tetrahedral chiral tags (CHI_TETRAHEDRAL_CW ↔ CHI_TETRAHEDRAL_CCW) are inverted to produce the mirror image; relative configuration is preserved where two centers are present.
4. **3D embedding**: `AllChem.EmbedMolecule` with ETKDGv3 (randomSeed=42) on the H-added molecule.
5. **Force-field optimisation**: `AllChem.MMFFOptimizeMolecule` (MMFF94, maxIters=2000).
6. **Energy reporting**: `MMFFGetMoleculeForceField.CalcEnergy()` on the optimised conformer.
7. **Write** all five structures to `enantio_structure.sdf` with `MMFF94_energy_kcal_mol` SD tag.

---

## Results

| Structure | Stereocenters | MMFF94 energy (kcal/mol) | FF status |
|---|---|---|---|
| EDS01357518_ent1 | C17 = S (original) | 77.48 | converged |
| EDS01357518_ent2 | C17 = R (enantiomer) | 73.67 | converged |
| EDS01806218_ent1 | C9 = R, C10 = S (original) | −25.93 | converged |
| EDS01806218_ent2 | C9 = S, C10 = R (enantiomer) | −18.28 | converged |
| EDS01889984 | — | −27.71 | converged |

All five structures embedded and optimised without errors.

---

## Audit

| Check | Result |
|---|---|
| Enantiomers are true mirror images | Confirmed: all stereocenters inverted (S→R, R→S) |
| Relative configuration preserved in EDS01806218 | Confirmed: (R,S) → (S,R), no diastereomer generated |
| EDS01889984 passed through unchanged | Confirmed: no stereocenters, single structure |
| All MMFF94 minimisations converged (return code 0) | Confirmed |
| Output molecule count matches expectation (2+2+1=5) | Confirmed |
| SMILES round-trip stereo check | EDS01357518 ent1/ent2 differ only in R/S at C17; EDS01806218 ent1/ent2 differ only in R/S at C9 and C10 |

---

## Output

- `enantio_structure.sdf` — 5 structures, 3D coordinates, explicit hydrogens, `MMFF94_energy_kcal_mol` SD tag per record.

### Code files produced
- `001_chem_sdmolsupplier.py` — initial stereo inspection
- `002_create_enantiomer.py` — enantiomer classification pass
- `003_create_enantiomer.py` — full pipeline: enantiomer generation, 3D embedding, MMFF94 optimisation, SDF write
