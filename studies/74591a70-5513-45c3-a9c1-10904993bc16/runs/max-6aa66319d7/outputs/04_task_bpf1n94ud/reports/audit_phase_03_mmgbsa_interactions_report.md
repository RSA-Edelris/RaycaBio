---
title: "Audit — Phase 3: MM-GBSA, Interaction Analysis, and Final Report"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-6aa66319d7"
phase_id: "3"
audit_type: "human-authored post-hoc"
---

# Audit — Phase 3: MM-GBSA, Interaction Analysis, and Final Report

## MM-GBSA Audit

| Check | Result |
|-------|--------|
| `mmgbsa2_results.json` present | ✓ |
| Compounds with ΔG_GBSA | ✓ 22/22 |
| tleap receptor topology built | ✓ 2.7 MB `receptor.prmtop` |
| All per-compound topologies built | ✓ 22/22 |
| MMPBSA.py exit codes | ✓ All 0 |
| ΔG range | −37.6 to +9.4 kcal/mol |
| Positive ΔG outlier | Compound_11_ent1: +9.4 kcal/mol — flagged in report |

### Bugs Fixed During MM-GBSA Runs (Documented)

| Task | Bug | Fix |
|------|-----|-----|
| bvh8nqsvc | AM1BCC timeout (180 s) on 30–38 HA compounds | Switched to Gasteiger (`-c gas`) |
| bk04326pc | tleap failed: `HIS` with `HD1` atoms unrecognised in `HIE` template; `NMET H` not matching `H1` | Renamed HIS→HID/HIE by atom inventory; renamed H→H1 at N-terminal Met47 |
| bt3i0n9lx | ProLIF segfault (exit 139) even with 8 Å pocket selection | Replaced ProLIF with custom RDKit geometry analysis |

All bugs resolved; no compound skipped.

## Interaction Analysis Audit

| Check | Result |
|-------|--------|
| `interaction_fingerprints.json` present | ✓ |
| Compounds analysed | ✓ 22/22 |
| Most frequent residue | TRP388 Hydrophobic — 100% |
| H-bond partner | HID380 — 77% donor, 73% acceptor |
| Consistent with known CRBN pharmacophore | ✓ Tri-Trp cage + His380 H-bond |

Interaction script runtime: ~2 s for 22 compounds — no performance issues.

## Annotated SDF Audit

| Check | Result |
|-------|--------|
| `CRBN_ID_enantio2_docking_GBSA.sdf` present | ✓ 82,259 bytes |
| All 22 compounds present | ✓ |
| SD tags verified | ✓ Affinity, CNN, MMGBSA_dG, Interacting_Residues, HBond_Residues |
| Poses valid 3D | ✓ (from gnina output) |

## Report Audit

| Check | Result |
|-------|--------|
| `CRBN_docking_mmgbsa_report.md` present | ✓ 11,921 bytes |
| Ranked table complete | ✓ 22 rows |
| MM-GBSA values in table | ✓ |
| Interaction frequency table | ✓ Top 25 residue×type pairs |
| Pharmacophore described | ✓ Tri-Trp cage + HID380 |
| Limitations section | ✓ Single-frame, Gasteiger, no water, ProLIF failure |
| Compound_11_ent1 anomaly flagged | ✓ |

## GitHub Push

Committed to RSA-Edelris/RaycaBio at:
`studies/74591a70-5513-45c3-a9c1-10904993bc16/runs/max-6aa66319d7`
Commit: 669ba37f49ef74c7cdeede9ffffb75902348c75e

## Conclusion

Phase 3 complete. All 22 MM-GBSA calculations succeeded. Interactions profiled for all 22 poses. Annotated SDF and report written and pushed to GitHub.
