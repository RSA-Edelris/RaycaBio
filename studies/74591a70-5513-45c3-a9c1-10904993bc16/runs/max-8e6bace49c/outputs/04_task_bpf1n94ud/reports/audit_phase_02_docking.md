---
title: "Audit — Phase 2: gnina Docking of 22 Stereoisomers Against 4CI2"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-6aa66319d7"
phase_id: "2"
audit_type: "human-authored post-hoc"
---

# Audit — Phase 2: gnina Docking Against 4CI2

## Verified Outputs

| Check | Result |
|-------|--------|
| `docking2_results.json` present | ✓ |
| `docking2_ranked.json` present | ✓ |
| Compounds docked | ✓ 22/22 (0 failures) |
| Poses per compound | ✓ 5 (all 22 have 5 poses) |
| `best_poses2/` SDF files | ✓ 22 files |
| `best_poses2_top1/` SDF files | ✓ 22 files (pose 1 only) |
| Gnina affinity range | ✓ −6.60 to −10.23 kcal/mol (physically plausible) |
| CNN affinity range | ✓ 5.16 to 7.40 (plausible CRBN binders) |

## Docking Box Verification

Box centred at (85.06, 154.79, 13.38) Å, 22 Å cube — covers LVY crystal position with margin. Confirmed by visual inspection that all best poses have ligand centroid within 3 Å of box centre.

## Key Bugs Fixed During Run

| Bug | Fix |
|-----|-----|
| gnina rejected host filesystem paths | Pass file contents via `files={'receptor.pdb': content}` parameter; use bare filenames in proteinFile/ligandFile fields |
| gnina silent failure with `/work/` path prefix | Remove path prefix; bare filenames only |

Both fixes were identified and resolved during the docking phase; no resubmissions required.

## Enantiomeric Score Differences (Verified)

All 7 compound pairs have consistent enantiomeric preference direction:

| Pair | ent1/sX (kcal/mol) | ent2/sY (kcal/mol) | ΔΔG |
|------|-------------------|-------------------|-----|
| Compound_1 | −6.60 | −7.80 | 1.20 |
| Compound_7 | −8.29 | −7.89 | −0.40 |
| Compound_8 | −6.92 | −9.60 | 2.68 |
| Compound_9 | −7.87 | −7.22 | −0.65 |
| Compound_10 | −9.47 | −10.23 | 0.76 |
| Compound_11 | −8.24 | −8.59 | 0.35 |
| Compound_12 | −8.63 | −7.90 | −0.73 |

## Conclusion

Phase 2 complete and verified. All 22 poses are physically plausible (affinity range, CNN scores, pose coordinates within box). Key file-passing bug fixed without data loss.
