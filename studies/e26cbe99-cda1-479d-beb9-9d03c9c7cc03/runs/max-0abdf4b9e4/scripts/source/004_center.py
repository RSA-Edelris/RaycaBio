
doc = """## Enantiomer Generation and 3D Conformer Production

### Input
Three molecules from enantio.sdf were analysed:
- EDS01357518: 1 racemic center (STERAC1, atom 18) → C17 = S as drawn
- EDS01806218: 2 racemic centers (STERAC1, atoms 10–11) → C9 = R, C10 = S as drawn
- EDS01889984: no stereocenters → achiral, passed through unchanged

### Method
1. Stereocenters detected with `Chem.FindMolChiralCenters`.
2. Enantiomer created by inverting all tetrahedral chiral tags (CW ↔ CCW) — preserves relative configuration where two centers are present.
3. 3D conformer generated with `AllChem.EmbedMolecule` (ETKDGv3, seed 42) on H-added molecule.
4. Optimised with `AllChem.MMFFOptimizeMolecule` (MMFF94, 2000 iterations).

### Results

| Structure | Config | MMFF94 energy (kcal/mol) | Converged |
|---|---|---|---|
| EDS01357518_ent1 | C17 = S (original) | 77.48 | yes |
| EDS01357518_ent2 | C17 = R (enantiomer) | 73.67 | yes |
| EDS01806218_ent1 | C9=R, C10=S (original) | −25.93 | yes |
| EDS01806218_ent2 | C9=S, C10=R (enantiomer) | −18.28 | yes |
| EDS01889984 | achiral | −27.71 | yes |

### Audit
- All stereocenters correctly inverted (S→R, R→S); no diastereomers introduced.
- EDS01889984 passed through as a single structure (no stereocenters).
- All five MMFF94 minimisations converged (return code 0).
- Output: enantio_structure.sdf, 5 structures, explicit H, MMFF94_energy_kcal_mol SD tag.
"""

finish(doc)
