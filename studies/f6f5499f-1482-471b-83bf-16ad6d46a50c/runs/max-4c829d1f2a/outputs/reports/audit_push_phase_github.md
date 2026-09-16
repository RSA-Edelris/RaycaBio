# Audit Report: Phase "Push session files to RSA-Edelris/RaycaBio on GitHub"

**Auditor:** Independent review agent  
**Date:** 2026-09-16  
**Commit audited:** `da27bb16986df591bf9ee27227f2998f198e71d9`  
**Repository path:** `RSA-Edelris/RaycaBio/tree/main/studies/f6f5499f-1482-471b-83bf-16ad6d46a50c/runs/max-6c649ef204`  
**Evidence basis:** Push tool return value; workspace filesystem (`ls -la` of root, source/, results/, reports/); all 14 source files read in full.

---

## Findings

### MAJOR — M1: Phase report records no procedure

**File:** `reports/phase_01_push_session_files_to_rsa_edelris_raycabio_on_gi.md`

A phase document exists (contrary to the simplest reading of the audit brief), but its procedure section is empty. The document explicitly states: "No tool call is on record for this phase, so the procedure cannot be stated. This is a gap in the record, not a phase that did no work." The verification section repeats: "No tool call is on record for this phase." There is no record of which files were staged, what selection criteria were applied, or what pre-push checks (if any) ran.

**Consequence:** The push cannot be reproduced or reconstructed from this phase report alone. An auditor relying on the report to understand what was pushed must instead reverse-engineer Table A.

---

### MAJOR — M2: Committed file count unexplained

**Evidence:** Push tool → `files_committed: 48`. Phase report Table A → 34 registered artifacts (counted by rows). Workspace filesystem → approximately 27 unique files (8 root + 12 Python + 1 CSV in source/results + 6 result MD files; two SDF inputs are in the artifact store, not the workspace).

The surplus of 14 files (48 committed minus 34 registered) is consistent with auto-generated scaffolding such as a README, directory index, or manifest, but no document confirms this. The phase report does not mention any auto-generated additions. A reader cannot identify which 48 files are in the commit without fetching it from GitHub.

---

### MAJOR — M3: Multiple versions of the same filename committed

**Evidence:** Phase report Table A shows:
- `phase_01_minisci_reagent_inventory.md` registered 4 times with distinct SHA-256 digests and sizes: 1.9 KB (path `01_parse_hte_edelris_2_sdf_and_inventory_reagents/reports`), 3.1 KB (same path), 3.2 KB (path `reports`), 3.5 KB (same path).
- `phase_02_minisci_campaign_design.md` registered 3 times: 6.2 KB, 7.8 KB, 8.4 KB across overlapping paths.

These are successive in-session versions — the files were opened in append mode and grew as verification sections were added (visible in `011_len.py` which appends phase1_verification and phase2_verification to the existing documents). The push tool committed multiple intermediary snapshots, possibly under distinct directory paths on GitHub. The phase report does not identify which version is canonical. A reader browsing the repository may encounter earlier incomplete versions.

---

### MAJOR — M4: Cross-phase directory placement on GitHub

**Evidence:** Phase report Table A, row for `phase_01_parse_hte_edelris_sdf_and_inventory_reagents.md`:

| File | Location on GitHub |
|------|--------------------|
| `phase_01_parse_hte_edelris_sdf_and_inventory_reagents.md` | `02_design_hte_campaign_factor_selection_design_type/reports` |

A Phase 1 result document was committed under Phase 2's directory. A researcher navigating `01_parse.../reports/` on GitHub would not find it. The platform's artifact-to-phase assignment appears to record file creation by phase of registration, not by phase of origin. No note in the phase report explains this placement.

---

### MAJOR — M5: Flawed acid-detection method committed without inline annotation

**File:** `source/008_classify_all_74_reagents_check_acid_additives.py`, lines 91–95

The Brønsted-acid check uses Python substring matching:

```python
if 'C(=O)O' in smi and 'N' not in smi and '[O-]' not in smi:
```

RDKit's `MolToSmiles` canonicalizes trifluoroacetic acid as `O=C(O)C(F)(F)F`. This string does **not** contain the literal substring `C(=O)O`. The check would return a false negative for TFA — the very compound being sought. The conclusion (TFA absent from kit) was correct because TFA was genuinely absent, but the method is broken for the stated purpose.

The corrected SMARTS-based version appears in `source/012_major_3_fix_re_run_br_nsted_acid_search_using_smarts.py` and at the workspace root as `012_acid_smarts_recheck.py`. Both were pushed alongside the original. Neither `008_...py` nor any inline comment marks the original file as containing a known defect. A reader of `008_...py` in the repository will see apparently functional code with an unflagged silent failure mode.

**Note on the silent-failure pattern specifically:** The SMARTS fix script resolves the failure with a print statement `"→ 0 hits confirmed. TFA is absent. Purchase flag is CORRECT."` — meaning the code path where the check finds nothing now explicitly confirms the expected result rather than failing silently. The original code had no such confirmation, so a false-negative result would have looked identical to a true-negative.

---

### MAJOR — M6: Workspace listing in audit evidence is partially inaccurate

**Evidence:** The workspace listing provided as audit evidence places `003_extract_all_molecules_their_properties.csv` in `source/`. Direct filesystem inspection (`ls -la`) shows it in `results/` (4596 bytes, created 07:21). The `ls` output is unambiguous: the `total 16` block after the source/ listing corresponds to results/.

The phase report Table A records the CSV committed to `01_parse_hte_edelris_sdf_and_inventory_reagents/tables/`, which is a sensible location regardless of workspace placement. The push destination appears correct. However, the inaccuracy in the provided evidence listing means any tracing that relied solely on the provided listing (rather than the filesystem directly) would have the CSV's workspace location wrong.

---

## Verified Correct

### V1: study_id and run_id — no identifier confusion

The phase report frontmatter declares:
- `study_id: "f6f5499f-1482-471b-83bf-16ad6d46a50c"`
- `run_id: "max-6c649ef204"`

The GitHub URL returned by the push tool is:
`studies/f6f5499f-1482-471b-83bf-16ad6d46a50c/runs/max-6c649ef204`

Both match exactly. The workspace directory name `f6f5499f-1482-471b-83bf-16ad6d46a50c-faa585e0ffd5` is the study_id with a session sub-suffix (`-faa585e0ffd5`), not the run_id, and is not used in any push path. No study/run/session identifier has been swapped at the URL or frontmatter level.

### V2: files_referenced: 0 is consistent with file sizes

The largest files in the workspace are `plate_map_minisci_round1.png` (671 KB) and `plate_map_round1.png` (551 KB). Both SDF inputs are under 140 KB. All are well within git's normal size tolerance. The push tool's stated behavior is to record files "too large for git" by hash rather than commit; `files_referenced: 0` is correct for this file set.

### V3: Dispensing rank is correctly 1-based in display

In `source/005_full_experiment_table_randomised_dispensing_order.py` (line 37) and `source/009_design_definition.py` (line 251), the display column is rendered with `rank+1` where `rank` is the 0-based loop variable from `enumerate`. The dispensing sequence is displayed as 1–24, not 0–23. No off-by-one error in either file.

### V4: Kit indices are consistently 0-based and match SDMolSupplier

All classification dictionaries in `003_classify_all_72_reagents.py` and `008_classify_all_74_reagents_check_acid_additives.py` use 0-based integer keys matching the position of each molecule in the SDF file as returned by `Chem.SDMolSupplier`. The verification in `011_len.py` spot-checks Water at index 73 (MW 18.0) and fac-Ir(ppy)₃ at index 58 (MW 657.8 — plausible for this complex). The `df2.loc[idx, 'smiles']` access pattern in `008_...py` relies on the pandas default integer label index coinciding with the SDF position. This holds only when None-count is zero; None-count was independently confirmed as zero in `011_len.py` (`len(mols2) == 74, None-count == 0`). The dependency is documented and verified.

### V5: SMARTS patterns in the corrected acid check are appropriate

`source/012_major_3_fix_re_run_br_nsted_acid_search_using_smarts.py` uses:
- `[CX3](=O)[OX2H1]` — standard SMARTS for a carboxylic acid carbon
- `[SX4](=O)(=O)[OX2H1]` — standard SMARTS for a free sulfonic acid

Both patterns are correct for the intended detection. They would match TFA (`O=C(O)C(F)(F)F`). The confirmation of 0 hits from the SMARTS search is reliable.

### V6: Two-seed randomization is intentional, not a confusion

`005_full_experiment_table_randomised_dispensing_order.py` uses `random.seed(42)` for the Ni/photoredox Round 1 plate; `009_design_definition.py` uses `random.seed(7)` for the Minisci plate. These are two separate experimental designs on two separate plates. Using different seeds is appropriate and the seed values are recorded in the committed source files.

---

## Summary Table

| ID | Severity | Finding |
|----|----------|---------|
| M1 | MAJOR | Phase document exists but records no procedure; push is not reproducible from the report |
| M2 | MAJOR | 48 files committed vs. 34 registered artifacts; 14-file surplus unexplained |
| M3 | MAJOR | 4 versions of `phase_01_minisci_reagent_inventory.md` and 3 of `phase_02_minisci_campaign_design.md` committed; canonical version not identified |
| M4 | MAJOR | Phase 1 result document committed under Phase 2's GitHub directory |
| M5 | MAJOR | Original acid-detection code (substring matching) has known false-negative failure mode; committed without inline defect annotation alongside the fix |
| M6 | MAJOR | Provided workspace listing misplaces the CSV file; listing is partially unreliable as evidence |
| V1 | VERIFIED CORRECT | study_id and run_id in frontmatter match GitHub URL exactly; no identifier confusion |
| V2 | VERIFIED CORRECT | files_referenced: 0 consistent with all files under git size threshold |
| V3 | VERIFIED CORRECT | Dispensing rank display uses rank+1 correctly in both plate design files |
| V4 | VERIFIED CORRECT | 0-based kit indices consistent with SDMolSupplier; dependency on None-count==0 documented and verified |
| V5 | VERIFIED CORRECT | SMARTS patterns in corrected acid check are correct; 0-hit result is reliable |
| V6 | VERIFIED CORRECT | Dual random seeds are intentional (two separate plates); values committed in source |

No CRITICAL findings were identified. No reversed positional arguments, no function signatures inconsistent with installed packages, and no rule derived from a single data point were found in the files reviewed.
