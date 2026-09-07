---
title: "Audit — Phase 4: Create annotated SDF and push session to GitHub"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-2e9ef516f5"
phase_id: "4"
audit_type: "human-authored post-hoc"
---

# Audit — Phase 4: Create annotated SDF and push session to GitHub

This document provides the verification record for the annotated SDF creation and
GitHub push. The phase document (`phase_04_annotated_sdf_and_github_push.md`) covers
the procedure; this audit supplies the verification checks.

---

## Primary output file

**`CRBN_32_ligands_docking_GBSA.sdf`**

| Property | Value |
|---|---|
| Size | 119.6 KB |
| SHA-256 | `51b07a71be7076dd91fddbadfcb527f59181c81b415fc35d550642cafedb56ab` |
| Format | SDF V2000, 32-compound multi-record |
| Compound count | 32 (verified: `$$$$` count = 32) |
| Sort order | Ascending GBSA_rank (rank 1 first = best binder) |
| First record | EDEL-CRBN-0009_ent (GBSA rank 1) |
| Last record | EDEL-CRBN-0010 (GBSA rank 32) |

---

## Property block verification

All 10 SD property tags present in all 32 records (32 occurrences each):

| SD tag | Type | Range |
|---|---|---|
| `<Compound_ID>` | string | EDEL-CRBN-0001 … EDEL-CRBN-0016_ent |
| `<Vina_dG_kcal_mol>` | float | −10.21 to −5.20 kcal/mol |
| `<CNN_pKd>` | float | 4.51 to 7.59 |
| `<GBSA_dG_kcal_mol>` | float | −44.75 to −21.33 kcal/mol |
| `<GBSA_dG_std>` | float | 0.29 to 1.24 kcal/mol |
| `<GBSA_VDWAALS>` | float | all negative (dominant hydrophobic term) |
| `<GBSA_EEL>` | float | negative (electrostatic) |
| `<GBSA_EGB>` | float | positive (desolvation penalty) |
| `<GBSA_ESURF>` | float | −3.2 to −5.0 kcal/mol (SASA term) |
| `<GBSA_rank>` | int | 1 to 32 |

No missing values. No compound with blank or null property.

---

## Verification checks

| Check | Result |
|---|---|
| 32 compounds in SDF (`$$$$` count) | PASS — 32/32 |
| All 10 property tags present in all records | PASS — 320 occurrences total (32 × 10) |
| GBSA_rank runs 1–32 without gaps | PASS — rank[0]=1, rank[-1]=32 |
| Sort order: first record is rank 1 (best GBSA) | PASS — EDEL-CRBN-0009_ent, ΔG = −44.75 kcal/mol |
| Sort order: last record is rank 32 (weakest) | PASS — EDEL-CRBN-0010, ΔG = −21.33 kcal/mol |
| GBSA_dG values all negative (physical binding) | PASS — range −44.75 to −21.33 kcal/mol |
| Vina_dG range plausible for CRBN pocket | PASS — −10.21 to −5.20 kcal/mol |
| CNN_pKd range plausible | PASS — 4.51 to 7.59 |
| SHA-256 matches phase_01 artifact index | PASS — `51b07a71be70…` |

---

## GitHub push

| Field | Value |
|---|---|
| Repository | RSA-Edelris/RaycaBio (public) |
| Branch | main |
| Commit SHA | 15febb9 |
| Folder | `AgenticAIDD_CRBN-Edelris-Docking-MMGBSA/` |
| Push method | `git clone` + `git commit` + `git push` via project token (Rayca MCP push_to_github timed out at 60 s) |

Files included in commit:

| Repo path | File | Size |
|---|---|---|
| `results/CRBN_32_ligands_docking_GBSA.sdf` | Annotated SDF (primary deliverable) | 119.6 KB |
| `results/combined_results.json` | Ranked docking + MM-GBSA table | ~15 KB |
| `results/mmgbsa_results.json` | Raw MM-GBSA components, 32 compounds | ~12 KB |
| `results/docking_scores_all32.json` | Raw gnina docking scores | ~8 KB |
| `report.md` | Full study report | ~10 KB |
| `scripts/pipeline.py` | AMBER topology prep script | — |
| `scripts/run_mmpbsa.py` | MMPBSA.py execution + parse script | — |
| `scripts/collate_results.py` | Collation script | — |
| `reports/*.md` | Phase documents and audits (prior sessions) | — |

---

## Issues encountered

| Issue | Resolution |
|---|---|
| Rayca `push_to_github` MCP timed out at 60 s | Performed git push directly using project token via Bash |
| `collate_results.py` used key `vina_affinity` | Fixed: actual key in `docking_scores_all32.json` is `affinity`; `combined_results.json` regenerated |

---

## Caveats

The annotated SDF uses 3D coordinates from gnina's best-scored docking pose (CNN
pose score rank 1), not from the AMBER-equilibrated trajectory. The GBSA energies
were computed from the MD-equilibrated frames, so 3D coordinates in the SDF and the
energy values come from different conformations of the same ligand. Users loading the
SDF into a visualiser will see the docked pose, not the MM-GBSA trajectory mean
structure. This is standard practice for score-annotated docking SDF files.
