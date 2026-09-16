# Phase 1 — Parse HTE_Edelris_2.sdf and Inventory Reagents

## Inputs
- `/home/ubuntu/rayca-artifacts/faa585e0ffd53b0a98ea5bca/files/HTE_Edelris_2.sdf` (138 481 bytes)

## Method
RDKit `SDMolSupplier` with `removeHs=False`. Properties: MOL_NAME, CAS_NUMBER, Role
(Role blank for all 74 entries; names taken from MOL_NAME; class assigned by SMILES/MW).

## Outputs
| File | Content |
|------|---------|
| `007_chem_sdmolsupplier.py` | Parse + full 74-row table |
| `008_classify_all_74_reagents_check_acid_additives.py` | Classification + Brønsted-acid check |

## Result — 74 molecules, 0 failures

| Class | Count | Kit indices |
|-------|-------|-------------|
| Photocatalyst — Ir | 4 | 12, 31, 35, 58 |
| Photocatalyst — Ru | 3 | 13, 15, 33 |
| Photocatalyst — Organic | 5 | 5, 6, 32, 38, 60 |
| Ni catalyst | 4 | 10, 21, 34, 55 |
| Pd catalyst (not relevant) | 20 | 0,2,3,7–9,14,16–19,30,36,39,40,47,56,59,61,63 |
| Bidentate N-ligand | 8 | 1, 4, 11, 22, 26, 27, 46, 57 |
| Monodentate N-ligand | 2 | 44 (2,6-lutidine), 54 (pyridine) |
| Chiral N-ligand | 1 | 62 |
| Base (inorganic/organic) | 12 | 23,29,37,41,42,43,48,50,51,52,53,71 |
| Solvent | 11 | 24,25,64,65,66,67,68,69,70,72,73 |
| Cu catalyst | 1 | 49 |
| HAT/amine additive | 1 | 28 |
| P-Ligand | 2 | 20, 45 |

## Key findings vs. HTE_Edelris.sdf (kit 1)
- **MeCN (kit #72) ADDED** — absent from kit 1, now present ✓
- **Water (kit #73) ADDED** — new cosolvent option ✓
- **DCE (kit #68)** replaces DCM from kit 1
- **Dioxane (kit #70)** confirmed (C1COCCO1, MW 88.1)
- Duplicate DBU: rows 37 and 71 (identical SMILES, identical MW 152.2)

## Critical gap: NO Brønsted acid anywhere in the 74 entries
Automated search for free COOH and SO₃H found zero hits.
TFA is absent. This is the absolutely necessary missing reagent for the Minisci reaction.

## Audit
- len(mols2) == 74, None-count == 0
- MW range: 18.0 (Water) – 1121.9 (Ir-PC)
- SMILES round-trip clean for all 74 entries

## Verification

### Parse integrity
- `len(mols2) == 74` confirmed; `None`-count == 0 (no failed parses).
- MW spot-checks: Water idx 73 → 18.0 ✓; fac-Ir(ppy)₃ idx 58 → 657.8 ✓;
  Mes-Acr⁺·BF₄ idx 32 → 399.2 ✓; MeCN idx 72 → 41.1 ✓.
- Duplicate confirmed: rows 37 and 71 both return SMILES `C1CCC2=NCCCN2CC1`, MW 152.2 (DBU).

### Brønsted-acid check
- Search criteria: SMILES containing `C(=O)O` with no `N` and no `[O-]`
  (free carboxylic acid), plus `S(=O)(=O)O` with no `[` (free sulfonic acid).
- Result: **0 hits across all 74 entries**.
- Manual scan of full SMILES list confirmed: no TFA (`OC(=O)C(F)(F)F`),
  no AcOH, no p-TsOH, no H₂SO₄ surrogate.
- Conclusion: TFA must be purchased before running the plate.

### Comparison with HTE_Edelris.sdf (kit 1, 72 entries)
- Kit 2 adds MeCN (idx 72) and Water (idx 73) — both absent from kit 1.
- Kit 2 has DCE (idx 68, MW 99.0, SMILES ClCCCl) where kit 1 had DCM (same SMILES, same MW) — effectively the same solvent under a different name.
- Kit 2 row 70: C1COCCO1, MW 88.1 = 1,4-dioxane (confirmed by ring SMILES and MW; kit 1 listed the same entry as DME, which is an error in kit 1's labelling).
- All photocatalysts, Ni sources, and N-ligands are identical between the two kits.
