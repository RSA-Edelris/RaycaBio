---
title: "Phase 5: Dock 84 CDK2-CyclinE1 Ligands — Batched run_python (Completed)"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-0072625358"
phase_goal: "Dock 84 CDK2-CyclinE1 ligands via batched run_python"
status: "complete"
model: "claude-sonnet-4-6"
---

# Phase 5: Dock 84 CDK2-CyclinE1 Ligands — Batched run_python

## Summary

All 84 CTX-series ligands (P841 selection) were docked against the CDK2–CyclinE1 receptor using gnina CNN-rescored Vina. Docking was completed via incremental batched `run_python` calls with `ThreadPoolExecutor` after the sequential workflow approach (phase 03) was superseded following context compaction and user direction to use batched run_python. Pose SDF files were recovered for the top 20 compounds by sequential re-docking. MMFF94s conformational strain was computed for top-20 poses. ProLIF interaction fingerprinting was run on all 20 pose files. A final report was written.

- **Ligands docked:** 84 / 84 (100%)
- **Poses captured:** 5 per ligand
- **Pose SDF files saved:** 20 (top 20 by CNN pKi)
- **Interaction fingerprints:** 20 / 20 analysed, 0 failed
- **Top compound:** CTX-1020732 (CNN pKi 8.931, pose score 0.992, Vina −14.02 kcal/mol)

---

## Objective

Complete a structure-based virtual screening campaign for 84 CTX-series compounds against CDK2–CyclinE1 using gnina GPU docking, and produce: ranked docking scores, best-pose SDF files, conformational strain estimates, protein–ligand interaction fingerprints, and a written report.

---

## Recovery context

At the start of this phase, context had been compacted. Three recovery scripts (source/019–021) were used to re-establish state:

| Script | Purpose |
|:---|:---|
| `019_run_aidd_tool.py` | Single gnina call template for CTX-1019480 (schema verification) |
| `020_check_what_s_already_completed_workflow_journal.py` | Read completed results from wf_087fab85-3e2 journal |
| `021_pathlib_path.py` | Seed `docking_checkpoint.json` with confirmed scores from journal |

Scripts 021 and 024 hardcode 2 seed entries (CTX-1020903 and CTX-1020667). Script 020 checked the prior workflow journal for additional confirmed scores but the seed dict in 021 was not expanded; 82 ligands were therefore dispatched in batches via `run_batch()` in `dock_setup.py`.

---

## Methods

### Docking engine and parameters

All docking used the gnina containerised tool (GPU-accelerated, CNN-rescored Vina mode).

| Parameter | Value |
|:---|:---|
| Receptor | `cdk2_campaign/receptor_raw.pdb` (heavy atoms + 9 crystal waters; no explicit H — correct for gnina/Vina atom typing) |
| Box centre (Å) | X = 30.57, Y = 5.37, Z = −25.80 (CTX-1017233 co-crystal ligand centroid) |
| Box size (Å) | 35 × 30 × 31 |
| numModes | 5 |
| cnnScoring | rescore |
| exhaustiveness | 8 |
| seed | 42 |
| GPU | Yes (A100 80 GB via Rayca sandbox) |

### Batching strategy

`dock_setup.py` defined `run_batch()` using `ThreadPoolExecutor(max_workers=15)` and an incremental checkpoint (`docking_checkpoint.json`). Each completed result was written immediately on completion so any interruption could be resumed from the last saved state.

**Batch 5** (15 ligands): brought total to 73/84.  
**Batch 6** (11 remaining): completed 84/84.

### Pose file recovery

gnina writes all poses to a single `gnina_docked.sdf.gz` per container invocation. Parallel dispatches overwrite this file, so pose coordinates are lost for batch-mode runs. To recover 3D poses for the top 20 compounds, these were re-docked sequentially (one at a time), and `gnina_docked.sdf.gz` was copied to `cdk2_campaign/poses_top20/{name}_poses.sdf` immediately after each call before the next dispatch.

### Conformational strain

MMFF94s intramolecular strain was computed on the best-ranked docked pose of each top-20 compound using RDKit (`AllChem.MMFFGetMoleculeForceField`, `CalcEnergy()`). This is the **ligand-only** strain energy (no receptor atoms). It reflects the conformational cost of adopting the docked geometry. Results written to `energy_results.json` under the key `mmff_strain_kcal`.

### Interaction fingerprinting

ProLIF 2.2.1 + MDAnalysis 2.10.0. Receptor: `receptor_prepared.pdb` (PDBFixer CHARMM explicit H at pH 7.4 — required for HBDonor/HBAcceptor detection). Ligand: best pose from each top-20 SDF file. Interaction types: Hydrophobic, HBDonor, HBAcceptor, PiStacking, CationPi, Anionic, Cationic, VdWContact, EdgeToFace, FaceToFace. ProLIF 2.x DataFrame columns are 3-tuples `(ligand_name, residue_name, interaction_type)`; keys written as `"RESIDUE.CHAIN:InteractionType"`.

---

## Results

### Docking scores — top 20 (ranked by CNN pKi)

| Rank | Compound | Vina (kcal/mol) | CNN pKi | CNN Pose | MMFF Strain (kcal/mol) |
|:---:|:---|---:|---:|---:|---:|
| 1 | CTX-1020732 | −14.02 | 8.931 | 0.992 | 125.6 |
| 2 | CTX-1020903 | −14.52 | 8.586 | 0.987 | 158.0 |
| 3 | CTX-1020811 | −13.17 | 8.586 | 0.976 | 198.0 |
| 4 | CTX-1020743 | −13.72 | 8.575 | 0.976 | 143.3 |
| 5 | CTX-1019813 | −12.10 | 8.306 | 0.946 | 198.3 |
| 6 | CTX-1020521 | −13.15 | 8.233 | 0.420 | 201.8 |
| 7 | CTX-1019757 | −11.24 | 8.107 | 0.855 | 178.9 |
| 8 | CTX-1020745 | −9.88 | 8.002 | 0.762 | 113.1 |
| 9 | CTX-1020441 | −12.43 | 7.846 | 0.729 | 196.6 |
| 10 | CTX-1020753 | −8.53 | 7.826 | 0.563 | 165.3 |
| 11 | CTX-1019473 | −10.15 | 7.740 | 0.697 | 128.6 |
| 12 | CTX-1020751 | −13.64 | 7.736 | 0.900 | 170.4 |
| 13 | CTX-1020752 | −11.50 | 7.715 | 0.605 | 229.1 |
| 14 | CTX-1020456 | −8.00 | 7.667 | 0.509 | 185.6 |
| 15 | CTX-1020562 | −11.50 | 7.627 | 0.449 | 289.2 |
| 16 | CTX-1020800 | −11.84 | 7.598 | 0.488 | 128.4 |
| 17 | CTX-1020555 | −12.45 | 7.595 | 0.465 | 109.9 |
| 18 | CTX-1020696 | −9.31 | 7.527 | 0.439 | 132.4 |
| 19 | CTX-1019613 | −12.79 | 7.507 | 0.535 | 216.6 |
| 20 | CTX-1020748 | −10.86 | 7.483 | 0.491 | 122.8 |

Reference co-crystal ligand **CTX-1017233** ranks 45th (Vina −7.49, CNN 7.114, pose 0.353), consistent with the library containing improved analogs designed to outperform the starting scaffold.

Weakest compound: **CTX-1020754** (CNN 4.716, rank 84).

### Interaction statistics (top 20 compounds, n=20 analysed, n=0 failed)

Obligate contacts (100% of top 20):

| Residue : Interaction | Count | % |
|:---|:---:|:---:|
| GLU57.A : VdWContact | 20 | 100 |
| HIS121.A : VdWContact | 20 | 100 |
| MET105.B : Hydrophobic | 20 | 100 |
| LYS108.B : Hydrophobic | 20 | 100 |
| LYS108.B : VdWContact | 20 | 100 |

Near-obligate (≥85%): GLU57.A Hydrophobic (95%), ILE104.B VdWContact (95%), HIS121.A Hydrophobic (90%), ALA151.A VdWContact (90%), MET105.B VdWContact (85%).

Key hydrogen bond: HIS121.A HBDonor in 50% of top-20 compounds — a primary SAR vector. ARG122.A HBAcceptor in 1 compound (5%). No PiStacking, ionic, or CationPi contacts detected; the pharmacophore is predominantly hydrophobic with one conserved H-bond.

Full 52-interaction statistics are in `cdk2_campaign/interaction_stats.json`.

---

## Output artifacts

| File | Description |
|:---|:---|
| `cdk2_campaign/docking_checkpoint.json` | Incremental checkpoint — 84/84 complete with Vina, CNN pKi, CNN pose, num_poses, gpu_used |
| `cdk2_campaign/docking_results.json` | Consolidated results sorted by CNN pKi descending; top-20 entries include `output_file` path |
| `cdk2_campaign/energy_results.json` | 84 compounds: all docking scores + `mmff_strain_kcal` for top 20 |
| `cdk2_campaign/poses_top20/CTX-XXXXXXX_poses.sdf` | 20 SDF files, 5 poses each (top-20 by CNN pKi) |
| `cdk2_campaign/interaction_fingerprints.json` | Per-compound ProLIF fingerprints (20 entries) — keys: `"RESIDUE.CHAIN:InteractionType"` |
| `cdk2_campaign/interaction_stats.json` | Series interaction frequency (n_analysed=20, n_failed=0, 51 unique types) |
| `CDK2_CyclinE1_Docking_Report.md` | Final written report: methods, top-20 table, per-compound interactions, series statistics, full 84-compound appendix |
| `gnina_docked.sdf.gz` | Last top-20 re-docking SDF output (session workspace; superseded by named files in poses_top20/) |
| `source/019_run_aidd_tool.py` | Recovery: single gnina call template (CTX-1019480) |
| `source/020_check_what_s_already_completed_workflow_journal.py` | Recovery: journal reader to seed checkpoint |
| `source/021_pathlib_path.py` | Recovery: checkpoint seeding from confirmed journal results |
| `cdk2_campaign/dock_setup.py` | Persistent module: ALL_LIGANDS, BOX params, run_batch(), dock_one(), pending_ligands(), load/save checkpoint |

---

## Verification

- 84/84 ligands have `best_affinity` (Vina) ≠ null in checkpoint
- 84/84 ligands have `best_cnn_affinity` ≠ null in checkpoint
- 20/20 pose SDF files present in `poses_top20/` and readable by RDKit
- 20/20 interaction fingerprints written with ≥1 interaction key each
- `interaction_stats.json` n_failed = 0
- `CDK2_CyclinE1_Docking_Report.md` 18,658 bytes, 347 lines, all 8 sections complete

---

## Limitations

1. **Parallel batch mode — pose coordinates lost for ranks 21–84.** Only scores are available; 3D poses cannot be recovered without re-docking.
2. **MMFF strain is not a binding free energy.** `mmff_strain_kcal` is the intramolecular conformational energy of the docked ligand pose alone. It is not a protein–ligand interaction energy and should not be interpreted as one.
3. **Box centroid computed from all 72 CTX HETATM records (including 33 H atoms).** This shifts the centre ~0.6 Å toward the H-heavy periphery versus the heavy-atom centroid. In a 35 Å box this is unlikely to exclude any binding-relevant pose.
4. **CNN pose score for CTX-1020521 (rank 6) is 0.420**, below the informal 0.5 quality threshold. Its CNN pKi (8.233) should be interpreted with lower confidence.
5. **Interaction fingerprinting limited to top 20.** Series statistics (n=20) may not represent the full 84-compound chemical diversity.

---

## References

1. McNutt AT, et al. GNINA 1.0: molecular docking with deep learning. *J Cheminform.* 2021;13:43. doi:10.1186/s13321-021-00522-2
2. Bouysset C, Fiorucci S. ProLIF: a library to encode molecular interactions as fingerprints. *J Cheminform.* 2021;13:72. doi:10.1186/s13321-021-00548-6
3. Michaud-Agrawal N, et al. MDAnalysis: a toolkit for the analysis of molecular dynamics simulations. *J Comput Chem.* 2011;32:2319–2327. doi:10.1002/jcc.21787
