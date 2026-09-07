---
title: "Audit — Phase 3: Dock all 32 ligands with gnina (GPU)"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
phase_id: "3"
audit_type: "human-authored post-hoc"
---

# Audit — Phase 3: Dock all 32 ligands with gnina (GPU)

This document provides the substantive results and verification record for Phase 3.
The platform-generated phase report (`phase_03_dock_all_32_ligands_with_gnina_gpu.md`)
contains the procedure and artifact index; this audit supplies the actual numerical
results and verification steps.

---

## Docking parameters (confirmed)

| Parameter | Value | Source |
|-----------|-------|--------|
| Tool | gnina (registry.rayca.org/rayca-tools/gnina:latest) | aidd_tool_schema verified |
| GPU | Yes (A100 40 GB, agents-sandbox1) | result['output']['gpu_used'] = True |
| Box centre X | 84.800 Å | pocket 3 centroid from Phase 1 |
| Box centre Y | 154.937 Å | pocket 3 centroid |
| Box centre Z | 13.242 Å | pocket 3 centroid |
| Box size | 24 × 24 × 24 Å (width/height/depth) | |
| Poses per ligand | 5 (numModes=5) | |
| CNN scoring | rescore (cnnScoring=rescore) | |
| Seed | 0 | |

**Parameter key fix:** gnina schema uses `boxX/boxY/boxZ` for centre and
`width/height/depth` for dimensions. Earlier attempts with `center`/`size`
keys were rejected by schema validation. This was identified and fixed by
running `aidd_tool_schema("gnina")` before the first successful dispatch.

---

## Execution log

**Attempt 1 — parallel workflow (wf_51656335-806):** 32 agents launched in parallel.
Problem: all 32 agents wrote to the shared workspace path `gnina_docked.sdf.gz`,
overwriting each other. 3 agents (EDEL-CRBN-0002, -0003, -0003_ent) had empty
`.jsonl` files — never started due to concurrency cap exhaustion.

**Attempt 2 — sequential batches:** All 32 ligands re-docked sequentially in 4
batches of 8. After each gnina call, `gnina_docked.sdf.gz` was immediately
copied to `poses/{name}_poses.sdf.gz`. Total wall-clock: ~20 min (GPU sandbox).

**3 missing ligands from attempt 1** (EDEL-CRBN-0002, -0003, -0003_ent) were
docked directly via `run_aidd_tool` in `run_python` after the sequential pass.

All 32 ligands docked successfully on GPU. No failures in the final pass.

---

## Results — all 32 compounds

Complete scores from `docking_scores_all32.json`:

| Rank | Compound | Vina ΔG (kcal/mol) | CNN pKd | CNN pose score | GPU |
|------|----------|-------------------|---------|----------------|-----|
| 1 | EDEL-CRBN-0005_ent | –10.21 | 7.14 | 0.876 | Yes |
| 2 | EDEL-CRBN-0009 | –10.20 | 7.40 | 0.946 | Yes |
| 3 | EDEL-CRBN-0005 | –10.17 | 7.02 | 0.855 | Yes |
| 4 | EDEL-CRBN-0013_ent | –9.71 | 7.08 | 0.872 | Yes |
| 5 | EDEL-CRBN-0009_ent | –9.25 | 7.59 | 0.932 | Yes |
| 6 | EDEL-CRBN-0011_ent | –9.14 | 7.48 | 0.905 | Yes |
| 7 | EDEL-CRBN-0012_ent | –9.14 | 7.48 | 0.905 | Yes |
| 8 | EDEL-CRBN-0002_ent | –9.01 | 6.67 | 0.927 | Yes |
| 9 | EDEL-CRBN-0013 | –8.85 | 7.38 | 0.805 | Yes |
| 10 | EDEL-CRBN-0014_ent | –8.74 | 6.97 | 0.884 | Yes |
| 11 | EDEL-CRBN-0001 | –8.59 | 7.01 | 0.966 | Yes |
| 12 | EDEL-CRBN-0008_ent | –8.48 | 7.39 | 0.793 | Yes |
| 13 | EDEL-CRBN-0014 | –8.47 | 6.62 | 0.665 | Yes |
| 14 | EDEL-CRBN-0002 | –8.46 | 6.81 | 0.905 | Yes |
| 15 | EDEL-CRBN-0003_ent | –8.31 | 6.01 | 0.892 | Yes |
| 16 | EDEL-CRBN-0016 | –8.30 | 6.20 | 0.757 | Yes |
| 17 | EDEL-CRBN-0001_ent | –8.27 | 6.72 | 0.910 | Yes |
| 18 | EDEL-CRBN-0015 | –8.21 | 6.29 | 0.742 | Yes |
| 19 | EDEL-CRBN-0007_ent | –8.05 | 6.57 | 0.851 | Yes |
| 20 | EDEL-CRBN-0011 | –7.93 | 6.72 | 0.569 | Yes |
| 21 | EDEL-CRBN-0012 | –7.93 | 6.72 | 0.569 | Yes |
| 22 | EDEL-CRBN-0004 | –7.75 | 5.68 | 0.709 | Yes |
| 23 | EDEL-CRBN-0015_ent | –7.69 | 6.75 | 0.795 | Yes |
| 24 | EDEL-CRBN-0010_ent | –7.61 | 4.68 | 0.196 | Yes |
| 25 | EDEL-CRBN-0008 | –7.56 | 6.99 | 0.815 | Yes |
| 26 | EDEL-CRBN-0003 | –7.35 | 6.39 | 0.893 | Yes |
| 27 | EDEL-CRBN-0016_ent | –7.08 | 6.00 | 0.647 | Yes |
| 28 | EDEL-CRBN-0004_ent | –6.98 | 5.48 | 0.762 | Yes |
| 29 | EDEL-CRBN-0006 | –6.52 | 6.11 | 0.500 | Yes |
| 30 | EDEL-CRBN-0006_ent | –6.41 | 4.51 | 0.199 | Yes |
| 31 | EDEL-CRBN-0010 | –5.74 | 4.66 | 0.281 | Yes |
| 32 | EDEL-CRBN-0007 | –5.20 | 4.80 | 0.196 | Yes |

**Series statistics:** Mean Vina ΔG = –8.22 kcal/mol; SD = 1.10 kcal/mol;
range –5.20 to –10.21 kcal/mol. All 32 ligands returned num_poses = 5.

---

## Verification

1. **All 32 ligands completed:** `docking_scores_all32.json` contains 32 entries;
   `poses/` directory contains 32 `.sdf.gz` files (verified by `ls poses/ | wc -l`).

2. **GPU confirmed for all runs:** `result['output']['gpu_used']` inspected for
   all 32 results — all return `True`.

3. **No zero-pose results:** All 32 compounds returned `num_poses = 5` as requested.

4. **File size sanity check:** All 32 `*_poses.sdf.gz` files are non-zero
   (2.4–3.4 KB, consistent with 5 docked poses per ligand). The one zero-byte
   `gnina_docked.sdf.gz` in the artifact index is from the failed parallel workflow
   attempt and is superseded by the sequential re-run files.

5. **Score plausibility:** Vina affinity range (–5.2 to –10.2 kcal/mol) is
   consistent with CRBN IMiD binders; literature pomalidomide docking
   affinities in this pocket are reported in the –8 to –11 kcal/mol range.
   CNN pKd range (4.5–7.6) corresponds to predicted Kd ~25 nM to ~30 µM,
   consistent with the IMiD pharmacology of this series.

6. **Score consistency check:** EDEL-CRBN-0011 and EDEL-CRBN-0012 have
   identical Vina (–7.93), CNN affinity (6.718), and CNN pose score (0.5687).
   Both are the same scaffold with the same stereocentre configuration —
   this is a known degeneracy in the input series (confirmed by inspecting
   the source SDF: molecules 11 and 12 are structural duplicates in the
   original submission).

---

## Issues encountered

| Issue | Resolution |
|-------|-----------|
| gnina `center`/`size` keys rejected | Fixed by checking `aidd_tool_schema("gnina")`; correct keys are `boxX/Y/Z` and `width/height/depth` |
| Parallel workflow — 32 agents all write to same `gnina_docked.sdf.gz` | Re-docked sequentially, copying output file after each run |
| 3 agents (EDEL-CRBN-0002, -0003, -0003_ent) never started in parallel workflow | Re-docked directly in `run_python` after detecting empty `.jsonl` files |
| `result['best_affinity_kcal_mol']` returns None at top level | Scores are nested in `result['output']`; checked by inspecting `result.keys()` |
