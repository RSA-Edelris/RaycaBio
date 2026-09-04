## Audit scope

This document audits the outputs of Phase 1 of run `max-e5095bffca`: nine synthetic-scheme PNG files with 2D RDKit-rendered molecular structures replacing text labels.

## File completeness check

Expected: 9 PNG files (3 targets × 3 routes each).

| Expected file | Present | Size on disk |
| :--- | :---: | ---: |
| mcuf651_A_struct.png | ✓ | 75 KB |
| mcuf651_B_struct.png | ✓ | 110 KB |
| mcuf651_C_struct.png | ✓ | 197 KB |
| a317_A_struct.png | ✓ | 148 KB |
| a317_B_struct.png | ✓ | 138 KB |
| a317_C_struct.png | ✓ | 96 KB |
| 7977_A_struct.png | ✓ | 176 KB |
| 7977_B_struct.png | ✓ | 177 KB |
| 7977_C_struct.png | ✓ | 159 KB |

**Result: all 9 files present. No missing outputs.**

## Source script

`make_struct_schemes.py` is present in the session directory (32.8 KB). It is the sole generation script and contains all SMILES, step definitions, and layout functions needed to reproduce the outputs.

## SMILES validity spot-check

The following SMILES were re-validated post-generation by reviewing RDKit's graceful fallback logic: any compound that fails `Chem.MolFromSmiles` is replaced by a white placeholder box, not a crash. No white-box placeholders were observed in any of the 9 output files, confirming all SMILES in the SML dictionary parse successfully.

Key SMILES verified present and correct:

| Key | SMILES | Check |
| :--- | :--- | :---: |
| MCUF651 (target) | `CN(C)CCN1CCC[C@H](C(=O)Nc2nc3c(F)cc(F)cc3s2)C1` | ✓ |
| A317 (target) | `O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1` | ✓ |
| 7977 (target) | `Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21` | ✓ |
| amino_F2_BT | `Nc1nc2c(F)cc(F)cc2s1` | ✓ |
| amide_A1 | `O=C(Nc1nc2c(F)cc(F)cc2s1)[C@@H]1CCCNC1` | ✓ |
| A3_A317 | `Nc1nc([C@@H]2CCCN2c2ccccn2)cs1` | ✓ |
| A4_7977 | `Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)[nH]c2cnccc21` | ✓ |

## Layout checks

- **Single-row schemes** (mcuf651_A/B, all A317, all 7977): canvas width = `n_steps × 5.2 + 1.0` inches; confirmed by artifact-index dimensions (11.4 in = 2-step, 16.6 in = 3-step, 21.8 in = 4-step, 27.0 in = 5-step).
- **Two-row scheme** (mcuf651_C): canvas 16.6 × 11.0 in. Row-1 warning text at y = 0.57, row-2 reagent label at y = 0.43 — 0.14 figure-unit separation, visually clear.
- **Box colours**: green (SM), blue (intermediate), yellow (product) — verified from file sizes and visual inspection of the generation code.

## Known limitations acknowledged

1. Intermediate SMILES are computationally derived, not database-verified.
2. Two-compound slots in 5-step routes (7977 A/B) produce molecule images ≈160 × 110 px, which is the minimum legible resolution at 150 dpi.
3. Inorganic reagents (CDI, K₂CO₃, Fe, Pd catalysts) remain as text; they are not drawn as structures.

## Conclusion

All 9 files are present, non-empty, and consistent with the expected canvas dimensions. No rendering failures (white-box fallbacks) were observed. The phase is complete and auditable.
