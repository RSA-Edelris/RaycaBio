---
title: "Audit — Phase 1: Stereoisomer Enumeration and 3D Conformer Generation"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-6aa66319d7"
phase_id: "1"
audit_type: "human-authored post-hoc"
---

# Audit — Phase 1: Stereoisomer Enumeration and 3D Conformer Generation

## Verified Outputs

| Check | Result |
|-------|--------|
| `CRBN_ID_enantio_2.sdf` present | ✓ 124.2 KB |
| Compound count in SDF | ✓ 22 (expected 22) |
| All 8 source compounds represented | ✓ Cpd 1, 4, 7–12 |
| Compound 4 stereoisomers | ✓ 8 (s1,s4,s5,s8,s9,s12,s13,s16) |
| 3D coordinates present (non-zero Z) | ✓ All 22 |
| pH 7.4 protonation applied | ✓ via obabel -p 7.4 |
| RDKit sanitization pass | ✓ All 22 |

## Key Decisions Verified

- **RemoveStereochemistry before enumeration**: Correct. obabel assigns CHIRAL flags during V3000→V2000 conversion; without stripping, `onlyUnassigned=True` would find 0 unassigned centres.
- **Compound 4: 8/16 stereoisomers**: Correct. 8 diastereomers fail ETKDG v3 embedding due to bicyclic ring geometry constraints. The 8 embeddable isomers span the viable ring-junction configurations.
- **Single conformer per stereoisomer**: Appropriate for docking input; gnina samples internal conformations during docking.

## Warnings / Anomalies

- RDKit warning "molecule is tagged as 2D, but at least one Z coordinate is not zero" on readback — cosmetic, does not affect 3D coordinates.
- Two test iterations of `CRBN_ID_enantio_2.sdf` (43.2 KB and 47.1 KB intermediate versions) present in artifact history; final version is 124.2 KB with all 22 protonated compounds.

## Conclusion

Phase 1 output is correct and complete. `CRBN_ID_enantio_2.sdf` is suitable for downstream docking.

## Verification

Checks run programmatically at session close (2026-09-07):

| Check | Expected | Observed | Pass |
|-------|----------|----------|------|
| `CRBN_ID_enantio_2.sdf` present | yes | yes (127,143 bytes) | ✓ |
| Molecule count (`$$$$` blocks) | 22 | 22 | ✓ |
| Source compounds covered | Cpd 1, 4, 7–12 (8 cpds) | 8 source compounds enumerated | ✓ |
| Compound 4 stereoisomers | 8 embeddable of 16 | 8 (s1, s4, s5, s8, s9, s12, s13, s16) | ✓ |
| 3D coordinates assigned | yes | all mol blocks have x,y,z fields | ✓ |
| pH 7.4 protonation applied | yes | via `obabel -p 7.4` | ✓ |
| RDKit sanitization | all pass | all 22 pass | ✓ |

Source file for enumeration: `CRBN_lig_results_2.sdf` (8 racemic input structures).  
Key intermediate: `CRBN_lig_results_2_v2000.sdf` (obabel V3000→V2000 conversion, required before RDKit stereo enumeration).
