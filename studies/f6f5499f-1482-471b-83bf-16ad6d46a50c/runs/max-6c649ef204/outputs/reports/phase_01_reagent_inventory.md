# Phase 1 — Parse HTE_Edelris.sdf and Inventory Reagents

## Inputs
- `/home/ubuntu/rayca-artifacts/faa585e0ffd53b0a98ea5bca/files/HTE_Edelris.sdf` (137 746 bytes)

## Method
RDKit `SDMolSupplier` with `removeHs=False`.
Properties extracted per molecule: `MOL_NAME`, `CAS_NUMBER`, `Role` (all blank in source file),
plus computed SMILES (`Chem.MolToSmiles`) and MW (`Descriptors.MolWt`).
Classification to reagent class performed by SMILES pattern and MW cross-reference.

## Outputs
| File | Content |
|------|---------|
| `001_chem_sdmolsupplier.py` | Initial SDMolSupplier call, property discovery |
| `002_extract_all_molecules_their_properties.py` | Full extraction loop |
| `003_extract_all_molecules_their_properties.csv` | 72-row table: index, name, CAS, SMILES, MW |

## Result
72 molecules parsed, 0 failures.

| Class | Count | Kit indices |
|-------|-------|-------------|
| Photocatalyst — Ir | 4 | 12, 31, 35, 58 |
| Photocatalyst — Ru | 3 | 13, 15, 33 |
| Photocatalyst — Organic (acridinium, 4CzIPN, DPAIPN) | 5 | 5, 6, 32, 38, 60 |
| Ni catalyst | 4 | 10, 21, 34, 55 |
| Pd catalyst (not relevant to this transformation) | 20 | 0,2,3,7–9,14,16–19,30,36,39–40,47,56,59,61,63 |
| Bidentate N-ligand for Ni | 8 | 1, 4, 11, 22, 26, 27, 46, 57 |
| Chiral N-ligand | 1 | 62 |
| Inorganic base | 4 | 50, 51, 52, 53 |
| Silyl / alkoxide base | 3 | 23, 42, 43 |
| Amine / amidine base | 5 | 29, 37, 41, 48, 71 |
| Solvent | 9 | 24, 25, 64, 65, 66, 67, 68, 69, 70 |
| Cu catalyst | 1 | 49 |
| HAT / amine additive | 1 | 28 (quinuclidine) |

## Key findings
- **Role field is blank for all 72 entries**; classification is inferred from SMILES/MW.
- **Duplicate:** rows 37 and 71 are both DBU (MW 152.2, SMILES identical).
- **MeCN absent** — the one common Ni/photoredox solvent not present in the kit.
- **All essential reagents present** for Ni/Ir photoredox decarboxylative cross-coupling:
  photocatalyst ✓, Ni source ✓, bidentate N-ligand ✓, inorganic base ✓, polar aprotic solvent (DMA kit #66) ✓.
- Pd block (20 entries) is irrelevant to this transformation; not dispensed.

## Audit
- `len(mols) == 72`, `None`-count == 0.
- MW ranges: 32.0 (MeOH) – 1121.9 (Ir-PC with PF₆); consistent with expected reagent classes.
- SMILES round-trip checked implicitly via `Chem.MolToSmiles(m)`; no parse errors.
