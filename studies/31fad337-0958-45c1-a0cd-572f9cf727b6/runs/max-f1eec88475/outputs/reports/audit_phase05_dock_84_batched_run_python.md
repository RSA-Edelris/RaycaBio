# Audit — Phase 05: Dock 84 CDK2-CyclinE1 Ligands via Batched run_python

**Auditor:** Claude Sonnet 4.6 (independent verification agent)
**Date:** 2026-09-06
**Files examined:**
- `reports/phase_05_dock_84_ligands_batched_run_python.md` (phase document)
- `cdk2_campaign/docking_checkpoint.json`
- `cdk2_campaign/docking_results.json`
- `cdk2_campaign/energy_results.json`
- `cdk2_campaign/interaction_stats.json`
- `cdk2_campaign/interaction_fingerprints.json`
- `cdk2_campaign/poses_top20/` (directory listing + RDKit readability check)
- `CDK2_CyclinE1_Docking_Report.md`
- `gnina_docked.sdf.gz` (decompressed and inspected)
- `source/019_run_aidd_tool.py`
- `source/020_check_what_s_already_completed_workflow_journal.py`
- `source/021_pathlib_path.py`
- `source/022_str.py`
- `source/023_inspect_checkpoint_see_what_actually_came_back.py`
- `source/024_correct_field_mapping_results_live_under_r_output.py`
- `cdk2_campaign/dock_setup.py`

---

## CRITICAL findings

None found. All 84 compounds have valid non-null docking scores. The top-20 ranked results, strain values, and interaction fingerprints are internally self-consistent.

---

## MAJOR findings

### M1 — Script 022 used the wrong field path; batch 1 necessarily produced null scores and was silently re-run

`source/022_str.py` (the first batch-1 dispatch) defines `dock_one()` as:

```python
r = run_aidd_tool("gnina", {...})
return {"best_affinity": r.get("best_affinity_kcal_mol"), ...}
```

`gnina` returns scores under `r["output"]`, not at the top level of `r`. The correct extraction is `o = r.get("output", {}); o.get("best_affinity_kcal_mol")`, as established in `source/023_inspect_checkpoint_see_what_actually_came_back.py` (diagnostic re-dock of CTX-1020670) and implemented in `source/024_correct_field_mapping_results_live_under_r_output.py`.

Script 024 reset the checkpoint to the 2-entry seed and re-ran batch 1 with the corrected field path. The phase document does not mention this batch-1 failure and re-run. The final checkpoint reflects the corrected scores and appears correct, but the unmentioned failure means the workflow had 15 extra dockings run twice (wasted compute, no data corruption).

**Evidence:** `source/022_str.py` lines 10–20; `source/024_correct_field_mapping_results_live_under_r_output.py` lines 5–46.

---

### M2 — interaction_stats.json contains 52 unique interaction types, not 51 as reported

The phase document states: "Full 51-interaction statistics are in `cdk2_campaign/interaction_stats.json`."

Actual count from the file:

```
python3 -c "import json; s=json.load(open('cdk2_campaign/interaction_stats.json')); print(len(s['interactions']))"
52
```

The 52nd entry is `"ASN59.A:VdWContact"` at the bottom of the list. The count of 51 in the report is off by one.

**Evidence:** `cdk2_campaign/interaction_stats.json` — 52 entries in the `interactions` list.

---

### M3 — Report narrative claims "58 of 84 seeded from journal" but scripts seed only 2

The phase document states: "At the time of seeding, 58 of 84 ligands had confirmed scores from the prior sequential workflow."

Scripts 021 and 024 both hardcode exactly 2 seed entries: CTX-1020903 and CTX-1020667. Script 020 reads the journal file but its output is not reflected in the 2-entry seed dict in script 021. Script 024 also resets the checkpoint to exactly 2 entries before re-running batches.

If only 2 were seeded, then 82 were docked in batches during this phase. With batch 5 bringing the total to 73 and batch 6 completing the last 11, arithmetic requires batches 1–4 to have covered 71 ligands (2 seeded + 71 = 73). The exact batch counts across scripts 025–041 (not audited here) would need to confirm this.

The claim of "58 seeded from journal" is not supported by any script examined. It may be a narrative error introduced during report writing, or it reflects results from an earlier phase not captured in scripts 019–024.

**Evidence:** `source/021_pathlib_path.py` lines 8–13 (2 seeds hardcoded); `source/024_correct_field_mapping_results_live_under_r_output.py` lines 30–33 (same 2 seeds on reset).

---

### M4 — CTX-1020667 has null best_cnn_pose in checkpoint

`docking_checkpoint.json` entry for CTX-1020667: `"best_cnn_pose": null`. All other 83 entries have a numeric best_cnn_pose value.

The phase document's verification section states "84/84 ligands have `best_affinity` (Vina) ≠ null" and "84/84 ligands have `best_cnn_affinity` ≠ null" — both of these are confirmed true. The report does not claim all CNN pose scores are non-null, so this is not a contradiction, but the null value is unreported. CTX-1020667 ranks outside the top 20 (CNN=6.76) so it does not affect pose or interaction analyses. The score data for this compound is partially incomplete.

**Evidence:** `cdk2_campaign/docking_checkpoint.json` lines 12–19.

---

## VERIFIED CORRECT

The following claims were checked against source files. Numbers were re-derived independently.

| Claim | File checked | Actual value | Result |
|:---|:---|:---|:---:|
| 84 entries in checkpoint | `docking_checkpoint.json` | 84 keys | CONFIRMED |
| All 84 have non-null best_affinity | `docking_checkpoint.json` | 0 null | CONFIRMED |
| All 84 have non-null best_cnn_affinity | `docking_checkpoint.json` | 0 null | CONFIRMED |
| docking_results.json has 84 entries | `docking_results.json` | 84 entries | CONFIRMED |
| docking_results.json sorted by CNN pKi descending | `docking_results.json` | strict descending | CONFIRMED |
| Rank 1 = CTX-1020732, Vina=−14.02, CNN pKi=8.931, pose=0.992 | `docking_results.json` row 0 | −14.02 / 8.931 / 0.9922 | CONFIRMED |
| Rank 2 = CTX-1020903, Vina=−14.52, CNN pKi=8.586, pose=0.987 | `docking_results.json` row 1 | −14.52 / 8.586 / 0.9871 | CONFIRMED |
| CTX-1017233 ranks 45th, CNN=7.114, Vina=−7.49 | `docking_results.json` row 44 | rank 45 / 7.114 / −7.49 | CONFIRMED |
| CTX-1020754 is rank 84 (weakest), CNN=4.716 | `docking_results.json` row 83 | CNN=4.716 | CONFIRMED |
| 20 SDF files in poses_top20/ | `poses_top20/` listing | 20 files | CONFIRMED |
| Top-20 output_file paths point to poses_top20/ | `docking_results.json` rows 0–19 | all non-empty, correct paths | CONFIRMED |
| Rank 21 (CTX-1020582) has empty output_file | `docking_results.json` row 20 | "" | CONFIRMED |
| Top-20 SDF files readable with real 3D coordinates | RDKit SDMolSupplier on CTX-1020732_poses.sdf | 5 poses read; atom 0: (25.613, 1.974, −24.809) Å | CONFIRMED |
| energy_results.json has 84 entries | `energy_results.json` | 84 entries | CONFIRMED |
| energy_results.json has mmff_strain_kcal for exactly 20 | `energy_results.json` | 20 non-null | CONFIRMED |
| All 20 top-compound strain values match report table | `energy_results.json` vs report table | all within 0.05 kcal/mol of reported | CONFIRMED |
| CTX-1020732 MMFF strain = 125.6 kcal/mol | `energy_results.json` | 125.598 | CONFIRMED |
| CTX-1020562 MMFF strain = 289.2 kcal/mol (highest in top 20) | `energy_results.json` | 289.2 | CONFIRMED |
| interaction_stats.json: n_analysed=20, n_failed=0 | `interaction_stats.json` lines 2–3 | 20 / 0 | CONFIRMED |
| 5 obligate contacts (100%): GLU57.A:VdWContact, HIS121.A:VdWContact, MET105.B:Hydrophobic, LYS108.B:Hydrophobic, LYS108.B:VdWContact | `interaction_stats.json` entries 1–5 | all count=20, pct=100.0 | CONFIRMED |
| HIS121.A:HBDonor at 50% | `interaction_stats.json` entry 17 | count=10, pct=50.0 | CONFIRMED |
| ARG122.A:HBAcceptor at 5% (1 compound) | `interaction_stats.json` entry 38 | count=1, pct=5.0 | CONFIRMED |
| interaction_fingerprints.json: 20 entries | `interaction_fingerprints.json` | 20 items (list) | CONFIRMED |
| All 20 fingerprint entries have ≥1 interaction key | `interaction_fingerprints.json` | all have 13–26 keys | CONFIRMED |
| CDK2_CyclinE1_Docking_Report.md: 18,658 bytes, 347 lines | file stats | 18658 bytes / 347 lines | CONFIRMED |
| gnina_docked.sdf.gz contains real 3D coordinates | decompressed SDF header | V2000 molfile with X,Y,Z atoms (first molecule: CTX-1020748) | CONFIRMED |
| gnina_docked.sdf.gz contains gnina score properties | property block in SDF | `<minimizedAffinity>`, `<CNNscore>`, `<CNNaffinity>` present | CONFIRMED |
| dock_setup.py ALL_LIGANDS: 84 entries, no duplicates, matches checkpoint exactly | dock_setup.py + checkpoint | 84 / 0 duplicates / exact match | CONFIRMED |
| poses_top20/ SDF files cover exactly the top-20 compounds in docking_results.json | listing vs ranks 1–20 | all 20 names match | CONFIRMED |

---

## Riskiest assumptions in source scripts

**`019_run_aidd_tool.py`**
The script calls `r.get("best_affinity_kcal_mol")` at the top level of the gnina return value in the except fallback, and prints `json.dumps(r)` on success. The assumption is that gnina's return is flat. This is wrong — the correct path is `r["output"]["best_affinity_kcal_mol"]`. The script was used for schema inspection (prints raw JSON) rather than for storing results, so it did not corrupt data. The misidentified field path is what motivated scripts 023–024.

**`020_check_what_s_already_completed_workflow_journal.py`**
Assumes the journal file exists at a hardcoded path tied to a specific workflow run (`wf_087fab85-3e2`). If the journal does not exist, the script prints "Journal not found" and falls through. The field name `d.get("best_affinity")` matches the prior sequential workflow schema. The risk: silent failure if the journal path changes or the run ID is wrong, resulting in zero seeds from the journal and all ligands needing re-docking.

**`021_pathlib_path.py`**
Hardcodes exactly 2 seed scores from memory (CTX-1020903 and CTX-1020667). These values are not re-verified against any stored raw gnina output. If either value was recalled incorrectly, it would enter the checkpoint as authoritative without re-docking. CTX-1020903 was later re-docked for poses (confirming Vina=−14.52, CNN=8.586), so the seeded value is confirmed correct. CTX-1020667 was never re-docked (not top-20), so its seeded scores (Vina=−9.39, CNN=6.76, pose=null) remain unconfirmed. This is the single instance where a seeded value from memory cannot be independently verified from source data in this audit.

**`022_str.py`**
Accesses gnina scores as `r.get("best_affinity_kcal_mol")` directly (no `r.get("output", {})` indirection). This is confirmed wrong: all 15 batch-1 compounds in this script's run would have received null scores. The file also references `WDIR`, `CK_FILE`, `REC`, `LIG_DIR`, and `remaining` without defining them, relying on namespace state from script 021. The entire batch-1 run was discarded and re-run in script 024.

**`023_inspect_checkpoint_see_what_actually_came_back.py`**
Re-docks exactly one compound (CTX-1020670) and prints the raw return value to discover the `r["output"]` field path. The riskiest assumption: CTX-1020670 is representative of all compounds. If gnina had returned data differently for this compound (e.g., an unusual compound class or a container quirk), the inferred field path could have been wrong for others. All 82 subsequently docked ligands returned valid scores, so the inference was correct.

**`024_correct_field_mapping_results_live_under_r_output.py`**
Uses `o = r.get("output", {})` with `.get()` defaults throughout. If gnina returns a result where the `"output"` key is absent (e.g., a container API change), `o` would be an empty dict and all scores would silently be `None`. However, `pending_ligands()` in `dock_setup.py` checks `best_affinity is None` and would re-queue such ligands, making silent failures recoverable. The `.get("output", {})` design is intentional but the default-value pattern means any schema mismatch is detectable only after the fact (null scores in checkpoint).

**`cdk2_campaign/dock_setup.py`**
Same field-extraction risk as script 024. The `run_batch()` function iterates `as_completed()` in the main thread, so checkpoint writes are sequential — no race condition despite the ThreadPoolExecutor. The `pending_ligands()` definition (`best_affinity is None`) correctly retries any compound where the field path failed. One subtle point: `pending_ligands()` does not retry compounds where docking succeeded but `best_cnn_affinity` or `best_cnn_pose` are null (e.g., CTX-1020667). If CNN scores are missing, the compound is not retried.

---

## Summary table

| ID | Severity | One-line description |
|:---|:---|:---|
| M1 | MAJOR | Script 022 used wrong gnina field path; batch-1 failed silently and was re-run in script 024 |
| M2 | MAJOR | interaction_stats.json has 52 unique interaction types, not 51 as stated in the report |
| M3 | MAJOR | Report claims 58 ligands seeded from journal; scripts 021 and 024 seed only 2 |
| M4 | MAJOR | CTX-1020667 has null best_cnn_pose in checkpoint; unreported incomplete record |
| m5 | MINOR | SDF files tagged "2D" in V2000 header but contain valid 3D coordinates; RDKit warns on load |
| m6 | MINOR | CTX-1019473 CNN pKi reported as 7.740; file value is 7.74 (trailing zero cosmetic) |
