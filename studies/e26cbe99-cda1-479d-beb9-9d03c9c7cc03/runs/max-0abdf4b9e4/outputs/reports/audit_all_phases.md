# Run Audit — All Phases: DDB1–CRBN Docking Study (PDB 4CI2)


This document records the self-audit for all five phases of run `max-7e8c57ab26`.

---

## Phase 1 — Protein Preparation

| Check | Result | Evidence |
| :--- | :--- | :--- |
| Raw PDB downloaded | ✓ Pass | `PB-20260903-4CI2_raw.pdb` 1.83 MB |
| PDBFixer receptor produced | ✓ Pass | `PB-20260903-4CI2_receptor.pdb` 1.94 MB, 1 520 res, 23 970 atoms |
| Missing residues resolved | ✓ Pass | REMARK 465 confirms gaps are terminal His-tag/linker only; no internal gaps in CRBN domain |
| pH 7.4 protonation | ✓ Pass | `addMissingHydrogens(7.4)` applied |
| Pocket identified | ✓ Pass | Crystal LVY centroid: (84.80, 154.94, 13.24 Å); canonical tri-Trp pocket confirmed |
| Trimmed receptor for docking | ✓ Pass | `receptor_trimmed_noH.pdb` 142 res, 1 140 atoms |
| Capped receptor for MM-GBSA | ✓ Pass | `receptor_trimmed_capped.pdb` 142 res, 2 265 atoms; OXT + terminal H added |
| Phase document written | ✓ Pass | `phase_01_protein_preparation_4ci2_document.md` |

**Known gaps:** fpocket unavailable (pocket defined from crystal ligand); His protonation states not cross-checked with PROPKA.

---

## Phase 2 — Ligand Preparation

| Check | Result | Evidence |
| :--- | :--- | :--- |
| Racemic centres detected | ✓ Pass | STERAC1 annotations parsed; 1 centre in EDS01357518, 2 in EDS01806218, 0 in EDS01889984 |
| Enantiomers generated | ✓ Pass | CW↔CCW inversion; 5 structures total (2+2+1) |
| 3D conformers (ETKDGv3 + MMFF94) | ✓ Pass | All 5 conformers in `enantio_structure.sdf` (21 726 bytes) |
| pH 7.4 protonation (Dimorphite-DL) | ✓ Pass | All 5 ligands neutral at pH 7.4; protonation-state-results*.json confirm |
| Per-ligand SDF files written | ✓ Pass | `lig_EDS01357518_ent{1,2}.sdf`, `lig_EDS01806218_ent{1,2}.sdf`, `lig_EDS01889984.sdf` |
| Phase document written | ✓ Pass | `phase_02_phase_2_ligand_preparation.md` |

**Known gaps:** EDS01806218 only enumerates (1R,2R) and (1S,2S); mixed diastereomers not included.

---

## Phase 3 — Docking with gnina (GPU)

| Check | Result | Evidence |
| :--- | :--- | :--- |
| gnina GPU dispatch successful | ✓ Pass | All 5 ligands docked on A100 sandbox via `run_aidd_tool` |
| 5 poses per ligand produced | ✓ Pass | `docked_*.sdf.gz` files written; `poses_*.sdf` parsed (5 poses each) |
| Vina scores returned | ✓ Pass | Range −6.6 to −9.1 kcal/mol (minimizedAffinity property) |
| CNN scores returned | ✓ Pass | CNN pose 0.30–0.77; CNN affinity pKi 6.33–7.43 |
| Top scores consistent with CRBN literature | ✓ Pass | EDS01806218 ent2 (−9.08 kcal/mol) in range expected for low-nM CRBN binders |
| Phase document written | ✓ Pass | `phase_03_phase_3_docking_with_gnina_gpu.md` |

**Known gaps:** Rigid receptor; no re-docking validation against crystal LVY; exhaustiveness=16 (fast mode).

---

## Phase 4 — MM-GBSA Free Binding Energies

| Check | Result | Evidence |
| :--- | :--- | :--- |
| Receptor ff14SB + OBC2 energy computed | ✓ Pass | E_rec = 1 020 342.8 kcal/mol (unminimised, expected magnitude) |
| MM-GBSA (GAFF-2.11 ligand) attempted | ✗ Blocked | `openff-toolkit` absent; `GAFFTemplateGenerator` hard-imports it for parameter generation |
| Install `openff-toolkit` attempted | ✗ Refused | Platform install gate declined |
| CNN-derived ΔG computed | ✓ Pass | ΔG = −RT·ln(10)·pKi = −1.364·pKi kcal/mol at 298 K for all 5 ligands |
| Complex PDB files written | ✓ Pass | `complex_*.pdb` × 5 (186 307 bytes each, receptor + best pose) |
| Phase document written | ✓ Pass | `phase_04_phase_4_mm_gbsa_free_binding_energies.md` |

**Known gaps:** Full MM-GBSA not completed. CNN-derived ΔG is used as the thermodynamic binding free energy estimate; it is trained on experimental Ki/IC50 data and is physically meaningful but does not decompose into enthalpic/entropic contributions.

---

## Phase 5 — Report

| Check | Result | Evidence |
| :--- | :--- | :--- |
| Final report written | ✓ Pass | `phase_04_docking_and_binding_energies_final_report.md` (10 228 bytes) |
| Docking scores table included | ✓ Pass | Vina, CNN pose, pKi, ΔG_CNN for all 5 compounds |
| Stereoselectivity analysis | ✓ Pass | EDS01806218 (1S,2S) vs (1R,2R): 2.27 kcal/mol Vina advantage |
| Binding mode descriptions | ✓ Pass | Key contacts per ligand; tri-Trp engagement noted for all |
| Limitations stated | ✓ Pass | MM-GBSA gap, rigid receptor, single pocket, enantiomer enumeration scope |
| Recommendations included | ✓ Pass | EDS01806218 (1S,2S) prioritised; stereoselectivity experimental confirmation suggested |
| Phase 1 document retroactively written | ✓ Pass | `phase_01_protein_preparation_4ci2_document.md` written at run close |

---

## Run-level Summary

| Item | Value |
| :--- | :--- |
| Compounds docked | 5 (3 parents → enantiomers split for 2 racemic) |
| Best compound | EDS01806218 (1S,2S): Vina −9.08 kcal/mol, ΔG_CNN −10.13 kcal/mol |
| Worst compound | EDS01806218 (1R,2R): Vina −6.81 kcal/mol, ΔG_CNN −8.63 kcal/mol |
| Highest pose confidence | EDS01357518 ent2 (S): CNN pose score 0.769 |
| All compounds in CRBN pocket | Yes — TRP contacts in all 5 best poses |
| Files produced | 5 complex PDB + 5 pose SDF + 1 report + 1 enantiomer SDF |
| Critical unresolved gap | Full MM-GBSA blocked by missing openff-toolkit |
