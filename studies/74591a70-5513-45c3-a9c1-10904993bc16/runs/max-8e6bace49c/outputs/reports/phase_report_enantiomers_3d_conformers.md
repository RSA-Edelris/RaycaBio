
## Objective

Process `CRBN_ID.sdf` (16 molecules) to enumerate enantiomers for all racemic stereocenters and generate a lowest-energy 3D conformer for each stereoisomer.

## Input

| Property | Value |
|---|---|
| File | `CRBN_ID.sdf` |
| Format | V3000 Molfile (Actelion Java MolfileCreator 2.0) |
| Number of molecules | 16 (EDEL-CRBN-0001 to EDEL-CRBN-0016) |
| Stereochemistry encoding | `MDLV30/STERAC1` (all 16 molecules) — absolute configuration undefined (racemic), relative configuration drawn via bond CFG wedge notation |

## Stereocenter inventory

| Molecule | Stereocenters | Atom indices (0-based) | Config (as drawn) |
|---|---|---|---|
| EDEL-CRBN-0001 | 1 | 16 | CCW |
| EDEL-CRBN-0002 | 1 | 18 | CCW |
| EDEL-CRBN-0003 | 1 | 18 | CCW |
| EDEL-CRBN-0004 | 1 | 20 | CCW |
| EDEL-CRBN-0005 | 2 | 3, 5 | CCW, CCW |
| EDEL-CRBN-0006 | 2 | 3, 5 | CCW, CCW |
| EDEL-CRBN-0007 | 2 | 3, 5 | CCW, CCW |
| EDEL-CRBN-0008 | 1 | 16 | CW |
| EDEL-CRBN-0009 | 2 | 14, 15 | CW, CW |
| EDEL-CRBN-0010 | 2 | 3, 5 | CCW, CCW |
| EDEL-CRBN-0011 | 1 | 16 | CW |
| EDEL-CRBN-0012 | 1 | 16 | CW |
| EDEL-CRBN-0013 | 2 | 16, 17 | CCW, CCW |
| EDEL-CRBN-0014 | 2 | 16, 17 | CW, CW |
| EDEL-CRBN-0015 | 1 | 16 | CW |
| EDEL-CRBN-0016 | 2 | 17, 19 | CW, CW |

## Method

1. **Reading**: RDKit `SDMolSupplier` with `removeHs=False, sanitize=True`; `AssignStereochemistry(cleanIt=True, force=True)` to perceive chirality from V3000 wedge/CFG annotations.
2. **Enantiomer generation**: All defined chiral tags inverted (CW ↔ CCW) via `SetChiralTag`. For 2-stereocenter molecules sharing a single STERAC1 group, both centers are inverted simultaneously, preserving the drawn relative configuration in the enantiomeric series.
3. **3D conformer generation**: `AllChem.ETKDGv3` (torsion-angle knowledge base, `enforceChirality=True`, `randomSeed=42`); fallback to `ETKDG` if ETKDGv3 fails. Hydrogens added before embedding, removed after.
4. **Energy minimization**: MMFF94 force field (`maxIts=2000`); fallback to UFF if MMFF94 parameters unavailable.

## Output

| File | Molecules | Notes |
|---|---|---|
| `CRBN_ID_enantio.sdf` | 32 | V2000 SDF; `ID` and `Stereoisomer` (original / enantiomer) properties per record; enantiomers named with `_ent` suffix |

All 16 originals and all 16 enantiomers embedded and minimized successfully (0 failures).

## Audit notes

- All stereocenters in the input carry `MDLV30/STERAC1` — no molecule had defined absolute configuration. Enantiomers therefore represent both members of each racemate, not an inversion of a known configuration.
- Chirality was enforced during embedding; stereo integrity should be verified with `Chem.FindMolChiralCenters` on the output if downstream docking requires confirmed absolute config.
- Code archived in `001_lowest_energy_conformer.py`.
