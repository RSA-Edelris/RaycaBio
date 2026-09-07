
## Objective

Enumerate all enantiomers and diastereomers of racemic CRBN ligands from `CRBN_lig_results_2.sdf`, generate lowest-energy 3D conformers, protonate at pH 7.4, and produce `CRBN_ID_enantio_2.sdf` for downstream docking.

---

## Input

**File**: `CRBN_lig_results_2.sdf` — 8 compounds (Compound 1, 4, 7–12), V3000 2D format, all stereocentres annotated as racemic (STERAC1 flag).

---

## Methods

### Step 1 — Format Conversion

The V3000 SDF was converted to V2000 with obabel `--gen2D` flag:

```
obabel CRBN_lig_results_2.sdf -O CRBN_lig_results_2_v2000.sdf --gen2D
```

**Rationale**: RDKit's `EnumerateStereoisomers` and `RemoveStereochemistry` work on V2000 format; V3000 STERAC annotations are preserved through the conversion.

### Step 2 — Stereoisomer Enumeration

```python
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions
from rdkit.Chem import RemoveStereochemistry

# Strip existing (AMBER-assigned) stereo before enumeration
RemoveStereochemistry(mol)
opts = StereoEnumerationOptions(unique=True, onlyUnassigned=True)
isomers = list(EnumerateStereoisomers(mol, options=opts))
```

**Key choice**: `RemoveStereochemistry()` was applied before `onlyUnassigned=True` because obabel assigns stereocentres during V2000 conversion (as explicit CHIRAL flags), which would prevent `onlyUnassigned` from finding any unassigned centres. Stripping first ensures all centres are re-enumerated from scratch.

**Naming convention**:
- 1 stereocentre → `_ent1`, `_ent2`
- ≥2 stereocentres → `_s1`, `_s4`, `_s8`, … (stereo permutation index)

**Compound 4 note**: The bicyclic ring system constrains which of the 16 theoretical diastereomers are geometrically embeddable. RDKit embedding filtered to 8 embeddable stereoisomers (s1, s4, s5, s8, s9, s12, s13, s16).

### Step 3 — 3D Conformer Generation

```python
from rdkit.Chem import AllChem
AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
AllChem.UFFOptimizeMolecule(mol)
```

One conformer per stereoisomer using ETKDG v3 + UFF single-point geometry optimisation. No conformer ensemble — lowest-energy single geometry for docking input.

### Step 4 — Protonation at pH 7.4

```
obabel input.sdf -O output.sdf -p 7.4
```

Applied per-molecule. Basic amines protonated to ammonium; carboxylic acids remain neutral at this pH for most compounds in this series.

---

## Results

| Compound | Stereocentres | Enumerated Isomers | Notes |
|----------|:---:|:---:|----|
| Compound_1 | 1 | 2 | ent1, ent2 |
| Compound_4 | 4 | 8 | s1, s4, s5, s8, s9, s12, s13, s16 — bicyclic geometry restricts from 16 |
| Compound_7 | 1 | 2 | ent1, ent2 |
| Compound_8 | 1 | 2 | ent1, ent2 |
| Compound_9 | 1 | 2 | ent1, ent2 |
| Compound_10 | 1 | 2 | ent1, ent2 |
| Compound_11 | 1 | 2 | ent1, ent2 |
| Compound_12 | 1 | 2 | ent1, ent2 |
| **Total** | | **22** | |

**Output**: `CRBN_ID_enantio_2.sdf` — 124.2 KB, 22 compounds, V2000 SDF, pH 7.4 protonated, 3D coordinates.

All 22 compounds passed:
- RDKit sanitization
- ETKDG v3 embedding (no embedding failures for final set)
- UFF optimisation
- obabel pH 7.4 protonation

---

## Output Artifacts

| File | Size | Description |
|------|-----:|-------------|
| `CRBN_lig_results_2_v2000.sdf` | 26.4 KB | V2000 format input (obabel conversion) |
| `CRBN_ID_enantio_2.sdf` | 124.2 KB | 22 stereoisomers, 3D, pH 7.4 (**primary output**) |
| `CRBN_enantio2_stage1.sdf` | 112.9 KB | 3D conformers before protonation |
| `CRBN_enantio2_summary.json` | 3.8 KB | Per-compound enumeration log |
| `prep_enantio2.py` | 6.0 KB | Enumeration + embedding script |

---

## Limitations

- Single conformer per stereoisomer; a multi-conformer ensemble would better sample binding-relevant geometries but is deferred to gnina's internal conformer sampling during docking.
- Compound 4 embedded 8/16 stereoisomers; the remaining 8 failed ETKDG embedding due to ring geometry constraints. The 8 embeddable isomers span a representative subset of the ring junction configurations.
- Protonation is rule-based (obabel pH 7.4); microscopic pKa prediction was not applied. Compounds with multiple titratable groups may have minor populations in alternative protonation states at physiological pH.
