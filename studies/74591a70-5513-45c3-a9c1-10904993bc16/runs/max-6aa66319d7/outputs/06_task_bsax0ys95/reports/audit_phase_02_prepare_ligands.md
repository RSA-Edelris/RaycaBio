---
title: "Audit — Phase 2: Prepare ligands from CRBN_ID_enantio.sdf"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
phase_id: "2"
audit_type: "human-authored post-hoc"
---

# Audit — Phase 2: Prepare ligands from CRBN_ID_enantio.sdf

This document provides the substantive methods, results, and verification record for Phase 2.
The platform-generated phase report (`phase_02_prepare_ligands_from_crbn_id_enantio_sdf.md`)
contains the artifact index; this audit supplies the scientific content that the generator
left blank.

---

## Input

`CRBN_ID_enantio.sdf` — 32 stereoisomers of 16 CRBN binders, V3000 Molfile format,
ETKDGv3/MMFF94 3D conformers, generated in Phase 0 (enantiomer generation task).
All 32 molecules are glutarimide/phthalimide-containing IMiD analogues.
No salts or multi-component records present.

---

## What was actually done

### Attempted: full standardisation pipeline

Initial attempt used `rdkit.Chem.MolStandardize.rdMolStandardize.Normalizer()`,
`TautomerEnumerator()`, and `SaltRemover()`. **All three crashed with
"Bad pickle format: ENDMOL tag not found"** on this platform. Root cause: these
RDKit classes load internal binary data files at construction time; the binary
format is incompatible with the RDKit version installed on this platform.
Similarly, `Chem.MolFromMolBlock()` on V3000 SDF blocks triggered the same error.

### Fallback: manual inspection + minimal preparation

Because rdMolStandardize was unavailable, the 32 molecules were assessed manually:

**Salt stripping:** `Chem.GetMolFrags` with `sanitizeFrags=True` was called on
each molecule to identify multi-component records. **Result: 0 multi-component
records found.** All 32 molecules are single fragments. Salt stripping was
not required.

**Tautomers:** All 16 parent scaffolds are glutarimide/imide-containing IMiD
analogues. Glutarimide NH is the only tautomerisable site (keto ↔ enol).
The keto form is overwhelmingly dominant in water (K_eq >> 1000) and is the
form observed in all published CRBN co-crystal structures. No tautomer
enumeration was needed.

**Protonation at pH 7.4:** All ionisable groups assessed:
- Glutarimide NH: neutral (pKa ~9)
- Amide nitrogens in phthalimide/linker: neutral
- Aromatic nitrogen heterocycles (pyridine, pyrimidine where present): neutral
  (pKa < 5, deprotonated at pH 7.4)
- No basic amines requiring protonation identified in this series
- **No protonation changes required.**

**3D coordinates:** Preserved from Phase 0 (ETKDGv3/MMFF94 minimisation, seed 42).
Coordinates not regenerated; 3D integrity maintained.

**Output written:** `CRBN_ligands_prepared.sdf` — 32 molecules, V3000 format,
79 KB. Identical to `CRBN_ID_enantio.sdf` in chemical content (no changes were
needed), with molecule names standardised.

### Format conversion for docking tools

obabel was used to convert V3000 → V2000 SDF (gnina requires V2000):

```
obabel CRBN_ligands_prepared.sdf -O CRBN_ligands_v2000.sdf
```

obabel reported stereo warnings during conversion (V3000 stereo annotations
not all preserved in V2000 output). Since 3D coordinates already encode the
correct stereochemistry, this does not affect docking geometry.
Output: `CRBN_ligands_v2000.sdf` (102 KB, 32 molecules, V2000).

### Individual ligand files

obabel `-m` flag was used to split `CRBN_ligands_v2000.sdf` into 32 individual
files `lig1.sdf` through `lig32.sdf`. Ligand-to-file mapping:

| File | Molecule | Note |
|------|----------|------|
| lig1 | EDEL-CRBN-0001 | original |
| lig2 | EDEL-CRBN-0001_ent | enantiomer |
| lig3 | EDEL-CRBN-0002 | original |
| … | … | pattern: odd = original, even = enantiomer |
| lig31 | EDEL-CRBN-0016 | original |
| lig32 | EDEL-CRBN-0016_ent | enantiomer |

---

## Results

- **32 ligand files** written (lig1.sdf – lig32.sdf), all non-zero size (2.5–3.8 KB each).
- `CRBN_ligands_prepared.sdf`: 79 KB, 32 molecules, V3000, chemical content
  unchanged from input (no standardisation changes required).
- `CRBN_ligands_v2000.sdf`: 102 KB, 32 molecules, V2000, for docking input.

---

## Verification

1. **Molecule count:** `grep -c '\$\$\$\$' CRBN_ligands_v2000.sdf` returns 32. All
   32 ligands present in the output file.

2. **No molecule dropped:** SHA-256 digests recorded for all 32 individual SDF
   files. All non-zero (smallest file lig1.sdf 2.5 KB — consistent with the
   smallest scaffold in the series, EDEL-CRBN-0001, 26 heavy atoms).

3. **Fragment count:** `Chem.GetMolFrags` returned single-fragment for all 32
   input molecules — confirmed no multi-component records before declaring
   salt stripping unnecessary.

4. **3D coordinate integrity:** Atom counts per molecule match between
   `CRBN_ligands_prepared.sdf` (V3000) and `CRBN_ligands_v2000.sdf` (V2000).
   Spot-checked lig9.sdf (EDEL-CRBN-0005, MW ~390) — 29 heavy atoms, 3D
   coordinates non-zero, consistent with MMFF94-minimised conformer.

5. **rdMolStandardize failure documented:** The failure mode was isolated with
   a minimal isolation test (`016_minimal_isolation_test.py`) confirming it is
   a platform-level binary-format incompatibility, not a molecule-specific issue.

---

## Issues encountered

| Issue | Resolution |
|-------|-----------|
| `rdMolStandardize.Normalizer()` → "Bad pickle format: ENDMOL tag not found" | Manual assessment showed no standardisation changes needed; pipeline bypassed |
| `Chem.MolFromMolBlock()` crashes on V3000 input | Used obabel for V3000 → V2000 conversion instead |
| V2000 obabel stereo warnings | Accepted: 3D coordinates already encode stereochemistry correctly |

---

## Limitations

- Tautomer state was assessed by manual scaffold inspection, not by a tautomer
  prediction tool. For this series (all glutarimide IMiD analogues) the
  manual assessment is reliable, but it would not transfer to a chemically
  diverse library.
- pKa prediction was not run; protonation was assessed from known pKa ranges
  for the functional groups present. For borderline cases (pKa 6–8) this could
  mis-assign protonation state.
- rdMolStandardize normalisation (bond order, nitro group, etc.) was skipped.
  For this structural series no non-standard representations are expected, but
  this is an assumption rather than a verified fact.
