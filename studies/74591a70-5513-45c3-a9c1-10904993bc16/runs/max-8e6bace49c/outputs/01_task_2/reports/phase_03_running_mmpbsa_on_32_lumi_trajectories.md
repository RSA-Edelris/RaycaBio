---
title: "Phase 3: Running MMPBSA.py on 32 LUMI trajectories"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-5c6f9d06e5"
phase_index: 3
phase_id: "1"
phase_goal: "Run MMPBSA.py on 32 LUMI trajectories and produce final docking + MM-GBSA ranking table"
status: "complete"
model: "claude-sonnet-4-6"
generator: "human post-hoc"
---

# Phase 3: Running MMPBSA.py on 32 LUMI trajectories

## Summary

MMPBSA.py v14.0 was run for all 32 CRBN ligand–receptor complexes using 50-frame NVT
trajectories collected from LUMI job 21779205. A parse bug caused 22/32 results to be
marked as failures; this was diagnosed and fixed in the same run by reading
`FINAL_RESULTS_MMPBSA.dat` files directly. All 32 compounds now have valid MM-GBSA
ΔG_binding values. The combined docking + MM-GBSA ranking table has been written.

Full scientific detail, ranked table, and verification record are in:
`reports/audit_phase_02_fix_mmpbsa_parse_and_collate.md`

---

## Procedure

### MMPBSA.py execution (background process PID 952808)

`run_mmpbsa.py` was run as a background process. It iterated over all 32 compound
directories (`mmgbsa/{name}_ent/`), called MMPBSA.py with igb=5 / saltcon=0.10 /
50 frames for each, and wrote `FINAL_RESULTS_MMPBSA.dat` per compound. Runtime: ~70
minutes (3–4 min/compound at ~3.5 min/compound on the local CPU).

Input files per compound directory:
- `complex.prmtop` — ff14SB + GAFF2 topology (~2.65 MB)
- `rec.prmtop` — ff14SB receptor topology
- `lig.prmtop` — GAFF2 ligand topology
- `md.nc` — 50-frame NVT NetCDF trajectory from LUMI (~3.6 MB)

### Parse failure diagnosis and fix

MMPBSA.py v14.0 exits non-zero after writing output when sub-calculations emit
warnings. The `run()` wrapper raised `RuntimeError` before `parse_mmpbsa()` was
reached for 22 compounds. Fix: called `parse_mmpbsa()` directly on all 32
`FINAL_RESULTS_MMPBSA.dat` files; all contained valid data.

`mmgbsa/mmgbsa_results.json` rewritten with all 32 entries.
`mmgbsa/combined_results.json` written with merged docking + GBSA table sorted by
DELTA TOTAL.

---

## Key output files

| File | Description |
|------|-------------|
| `mmgbsa/*/FINAL_RESULTS_MMPBSA.dat` | 32 MMPBSA.py output files (4.3–4.4 KB each) |
| `mmgbsa/mmgbsa_results.json` | 32-compound MM-GBSA results (DELTA TOTAL + components) |
| `mmgbsa/combined_results.json` | Combined docking + MM-GBSA ranking, sorted by GBSA ΔG |
| `report.md` | Final study report with full ranked table and analysis |

---

## Results summary

DELTA TOTAL range: −21.33 (EDEL-CRBN-0010) to −44.75 (EDEL-CRBN-0009_ent) kcal/mol.
Top-ranked by MM-GBSA: EDEL-CRBN-0009_ent (−44.75), EDEL-CRBN-0013 (−43.80),
EDEL-CRBN-0009 (−43.75). Most consistently top-ranked scaffold across all three
metrics (Vina, CNN pKd, GBSA): EDEL-CRBN-0005 / EDEL-CRBN-0005_ent.

---

## Temporary files

`_MMPBSA_*` and `reference.frc` files in each compound directory are MMPBSA.py
intermediates retained because MMPBSA.py exited non-zero. They are not needed for
downstream analysis and can be removed with:

```bash
rm -f mmgbsa/*_ent/_MMPBSA_* mmgbsa/*_ent/reference.frc
```
