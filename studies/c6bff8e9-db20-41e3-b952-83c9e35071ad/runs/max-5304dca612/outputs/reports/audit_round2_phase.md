
# Independent Audit — Round 2 HTE Plate Design
## Buchwald-Hartwig C–N Coupling, 4 × 2 × 12 Full Factorial

**Auditor:** Independent reviewer (not involved in design)
**Files reviewed:**
- `HTE_BH_round2_4x2x12.md` (main design document)
- `phase_HTE_round2_4x2x12.md` (phase write-up)
- `source/006_plate_2_design_4_bases_2_solvents_12_pd_catalysts_96.py` (grid construction)
- `source/007_plt_subplots.py` (plate map rendering)
- `generate_platemap.py` (Round 1 reference)
- `HTE_BH_campaign_design.md` (Round 1 design reference)
- `/home/ubuntu/rayca-artifacts/9b531d029532706a25e7a959/files/HTE_Edelris.sdf` (reagent kit, 74 entries)

---

## MAJOR FINDINGS

### MAJOR-1: `007_plt_subplots.py` is not self-contained — will fail with NameError at runtime

**File:** `source/007_plt_subplots.py`
**Severity:** Major — the script cannot be executed standalone

`007_plt_subplots.py` uses four variables (`CATALYSTS`, `SOLVENTS`, `BASES`, `ROWS`) that are **never defined anywhere in that file**. All four are defined in `006_plate_2_design_4_bases_2_solvents_12_pd_catalysts_96.py`. Running `007_plt_subplots.py` from a clean Python interpreter will fail immediately:

| Variable | First use in 007 | Defined in 007? | Defined in 006? |
|---|---|---|---|
| `SOLVENTS` | line 24: `SOLVENTS[sol_idx]` | No | Yes |
| `CATALYSTS` | line 36: `enumerate(CATALYSTS)` | No | Yes |
| `ROWS` | line 60: `row_ltr = ROWS[ri]` | No | Yes |
| `BASES` | line 63: `BASES[base_idx]` | No | Yes |

The script also redefines `BASE_ROW_ALPHA` (line 14) and `SOLVENT_BG` (line 13) internally — both are needed and correctly present — but the four missing variables above are fatal. The script only executes correctly if `006_...py` was run first in the **same Python session**, leaving the variables in the namespace.

`phase_HTE_round2_4x2x12.md` describes `007_plt_subplots.py` as the "Rendering script" in a separate source-file table, implying standalone reuse. That is not possible in its current state.

**Impact:** Anyone who checks out the `source/` directory and runs `python 007_plt_subplots.py` receives a `NameError` at line 24. The plate map PNG cannot be reproduced from `007` alone, only from a session where `006` was already executed.

**Fix required:** Either (a) add all four definitions to the top of `007_plt_subplots.py` (making it truly self-contained), or (b) change `007` to `import`/`from` `006` explicitly and document that `006` must be imported. Option (a) is preferred for reproducibility.

---

## MINOR FINDINGS

### MINOR-1: Short label "PEPSI" is a typo — the catalyst acronym is "PEPPSI"

**Files:** `HTE_BH_round2_4x2x12.md` line 48; `source/006_...py` line 24

The design document catalyst table shows:
```
| 12 | PEPSI | **PEPPSI [NHC-Pd]** | 1158652-41-5 |
```

The script encodes:
```python
("PEPPSI [NHC-Pd]",     "PEPSI",  "#E76F51", "1158652-41-5", "NHC"),
```

The short label `"PEPSI"` (5 characters) is missing one `P`. The correct acronym is **PEPPSI** = Pyridine-Enhanced Precatalyst Preparation Stabilization and Initiation (6 letters). The short label is what appears on every well circle (line 91 of `007`) and on the column header chip (line 50 of `007`). The rendered plate map therefore shows "PEPSI" — a soft-drink brand — for all 8 PEPPSI wells (B12, C12 … H12) and in the column 12 header.

This does not affect the CAS number, well position, or scientific classification, but it creates a labeling error that will propagate into any ELN transcription from the plate image.

**Fix:** Change `"PEPSI"` to `"PEPPSI"` in `006_...py` line 24 and the corresponding row in `HTE_BH_round2_4x2x12.md`.

---

### MINOR-2: Internal inconsistency — "at least two wells in common" but only one anchor named

**File:** `HTE_BH_round2_4x2x12.md`, section "Cannot estimate without replicates"

The document states:
> "Run at least two wells in common between the two plates (e.g., BrettPhos G3 / Cs₂CO₃ / dioxane, which appears at B1 in Round 2) to verify assay drift."

Only one well (B1) is named. The actual Round 2 layout contains multiple conditions that overlap with Round 1:
- Round 2 row B (Cs₂CO₃/dioxane), columns 1–6 (the six R1-tagged catalysts): these all appeared in Round 1 as unique wells in the Dioxane/Cs₂CO₃ column block.
- Round 2 row C (K₃PO₄/dioxane), columns 1–6: likewise all appeared in Round 1.

The "at least two" recommendation is therefore already satisfied by the full design — there are roughly 12 overlap wells — but the document (a) only explicitly names B1, and (b) does not instruct the analyst to use the others for drift detection.

**Impact:** Minor documentation gap. The analysis plan (section 1) only references "well B1" for the drift check. An analyst following this document literally performs a single-point drift comparison instead of using the full set of overlapping anchor wells, weakening drift detection.

**Fix:** Either cite the complete list of anchor wells (B1–B6 and C1–C6 for R1-tagged catalysts) in the analysis plan, or remove the "at least two" clause if a single anchor is accepted.

---

### MINOR-3: Single unreplicated anchor well reduces drift detection power

**File:** `HTE_BH_round2_4x2x12.md`, Controls note and Analysis plan section 1

B1 (BPG3/Cs₂CO₃/dioxane) is an unreplicated experimental well in Round 2. Round 1 used H11/H12 as a duplicate pair to establish assay precision for this condition. In Round 2, there is only one measurement at B1. The proposed drift check — "Difference > 15% absolute triggers assay-drift investigation" — compares a single Round 2 data point against the mean of two Round 1 controls. Because Round 2 B1 has no within-plate replicate, it is impossible to distinguish assay drift from natural well-to-well variability (the ±3–5% noise floor documented in `HTE_BH_campaign_design.md`).

This is an inherent limitation of the fully saturated design rather than an error, and the document acknowledges it; however, the ±15% tolerance is not justified from first principles. The Round 1 REP1–REP9 pairs give σ ≈ 2%, making the 15% threshold approximately 7.5σ — a conservative enough bound that genuine drift (>15%) would be unmistakable, but a 10% drift would go undetected. The threshold should be stated with reference to the Round 1 σ estimate.

---

## VERIFIED CORRECT

### VERIFIED-1: Well-count arithmetic

`source/006_...py` constructs an 8 × 12 grid via `for ri in range(8): for ci in range(12)` and asserts the total at line 51:
```python
assert total == 96
```
The loop produces exactly 96 non-overlapping well assignments. The factorial decomposition 4 bases × 2 solvents × 12 catalysts = 96 is correct, matches the document claim, and is verified by the assert. No gaps or overlaps exist.

---

### VERIFIED-2: Non-phosphine requirement — PEPPSI present and correctly classified

Column 12 of the design is assigned CAS 1158652-41-5, tagged `"NHC"` in the script. The Edelris SDF (entry 64) confirms:
```
CAS: 1158652-41-5
NAME: [1,3-bis[2,6-bis(1-ethylpropyl)phenyl]-4,5-dichloro-2H-imidazol-2-yl]-dichloro-palladium;3-chloropyridine
```
This is an N-heterocyclic carbene Pd(II) complex with a 3-chloropyridine labile ligand — correctly classified as non-phosphine. The scientific description in `HTE_BH_round2_4x2x12.md` ("The 3-chloropyridine leaving group gives a well-defined active Pd(0) species") is consistent with the SDF structure. The non-phosphine requirement is met.

Note: This compound is a 4,5-dichloro NHC variant with 2,6-di(pentan-3-yl)phenyl substituents — not the more commonly cited PEPPSI-IPr (CAS 905459-27-0). The SDF name and the phase document description ("[1,3-bis[2,6-bis(1-ethylpropyl)phenyl]-4,5-dichloro-imidazol-2-ylidene]Pd(II)") are consistent with each other and accurate for this compound. The "PEPPSI" label in the main document is a generic class name, which is acceptable.

---

### VERIFIED-3: All 12 catalyst CAS numbers present in Edelris SDF

All 12 catalysts in the Round 2 design were checked against the 74-entry Edelris SDF. All 12 are confirmed present with matching CAS numbers:

| Col | Short | CAS claimed | SDF entry | SDF name match |
|---|---|---|---|---|
| 1 | BPG3 | 1470372-59-8 | Entry 33 | "BrettPhos Pd G3" ✓ |
| 2 | tBBG3 | 1536473-72-9 | Entry 62 | "tBuBrettPhos Pd G3" ✓ |
| 3 | RuPG3 | 1445085-77-7 | Entry 10 | "RuPhos-Pd-G3" ✓ |
| 4 | tBXG3 | 1447963-75-8 | Entry 4 | "tBuXPhos Pd G3" ✓ |
| 5 | EPG3 | 2940916-90-3 | Entry 66 | "EPhos-Pd-G3" ✓ |
| 6 | SPG3 | 1445085-82-4 | Entry 1 | "SPhos Pd G3" ✓ |
| 7 | MorG3 | 2222690-89-1 | Entry 22 | "MorDalPhos-Pd-G3" ✓ |
| 8 | APG3 | 1820817-64-8 | Entry 20 | "APhos-Pd-G3" ✓ |
| 9 | GPG3 | 2489525-82-6 | Entry 21 | "GPhos-Pd-G3" ✓ |
| 10 | CatG3 | 1651823-59-4 | Entry 59 | "cataCXium-A-Pd-G3" ✓ |
| 11 | dppf | 1445086-28-1 | Entry 17 | "dppf-Pd-G3" ✓ |
| 12 | PEPPSI | 1158652-41-5 | Entry 64 | NHC-Pd / 3-chloropyridine ✓ |

No CAS number errors found.

---

### VERIFIED-4: NaOtBu not present in Round 2 base list

The four Round 2 bases (`BASES = ["K₂CO₃", "Cs₂CO₃", "K₃PO₄", "DIPEA"]` in `006_...py` line 29) do not include NaOtBu. The Edelris SDF confirms NaOtBu (CAS 865-48-5, entry 46) is in the kit but was correctly excluded. The design document rationale ("NaOtBu is dropped. It caused the greatest risk of glutarimide NH deprotonation", `HTE_BH_round2_4x2x12.md`) is consistent with the base selection and with the pKa argument documented in `HTE_BH_campaign_design.md` Round 1 critical note.

---

### VERIFIED-5: Cross-plate anchor B1 = BPG3/Cs₂CO₃/dioxane is correctly placed

The `006_...py` row/column logic:
```python
for ri in range(8):
    sol_idx  = ri // 4   # 0=Dioxane rows A-D, 1=t-AmylOH rows E-H
    base_idx = ri  % 4
```

Row index `ri=1` (Row B): `sol_idx=0` (Dioxane), `base_idx=1` → `BASES[1]` = `"Cs₂CO₃"`.
Column index `ci=0` (Col 1): `CATALYSTS[0]` = `("BrettPhos Pd G3", "BPG3", ...)`.

Therefore B1 = BPG3/Cs₂CO₃/dioxane. This matches the claim in both documents. The Round 1 plate (`generate_platemap.py`) confirms BPG3/Cs₂CO₃/dioxane appeared as H11 and H12 (positive controls) in Round 1, making it a valid cross-plate comparator.

---

### VERIFIED-6: Internal consistency — script layout matches document description

| Claim in document | What the script does | Match? |
|---|---|---|
| Rows A–D = dioxane | `sol_idx = ri // 4` → 0 for ri 0–3 | ✓ |
| Rows E–H = t-AmylOH | `sol_idx = ri // 4` → 1 for ri 4–7 | ✓ |
| Row order: K₂CO₃, Cs₂CO₃, K₃PO₄, DIPEA | `BASES = ["K₂CO₃","Cs₂CO₃","K₃PO₄","DIPEA"]`; `base_idx = ri % 4` | ✓ |
| Cols 1–12 = 12 catalysts | Outer `for ci in range(12)` | ✓ |
| Gold ring = NHC; dashed white = bidentate | Lines 81–89 of 007 | ✓ |
| Warm yellow background = dioxane rows | `SOLVENT_BG = ["#FFF4E6", "#EBF9F1"]` | ✓ |

---

### VERIFIED-7: Controls rationale is scientifically acceptable (with noted caveats)

Omitting dedicated controls from a fully saturated 96-well factorial is acceptable given: (a) Round 1 qualified the assay with a full negative-control suite on the same substrate lot; (b) the cross-plate anchor (B1) provides a quantitative check against Round 1 H11/H12; (c) the design specifies identical internal standard, quench, and UPLC method between plates. The scientific logic is sound. The caveats (B1 unreplicated, no intra-plate negatives) are acknowledged in MINOR-3 above and are inherent to the fully saturated design choice, which is explicitly justified in the document.

---

## Summary Table

| # | Finding | Severity | File | Location |
|---|---|---|---|---|
| 1 | `007_plt_subplots.py` missing `CATALYSTS`, `SOLVENTS`, `BASES`, `ROWS` — NameError on standalone run | **MAJOR** | `source/007_plt_subplots.py` | Lines 24, 36, 60, 63 |
| 2 | Short label "PEPSI" should be "PEPPSI" — propagates to plate image | MINOR | `source/006_...py` line 24; `HTE_BH_round2_4x2x12.md` line 48 | Short name column |
| 3 | "At least two wells in common" stated but only B1 named; 10+ additional anchor wells exist but are not identified in analysis plan | MINOR | `HTE_BH_round2_4x2x12.md` | "Cannot estimate" section; Analysis plan §1 |
| 4 | Single unreplicated anchor B1; ±15% drift threshold not referenced to Round 1 σ ≈ 2% | MINOR | `HTE_BH_round2_4x2x12.md` | Analysis plan §1; Controls note |
| 5 | Well-count arithmetic: 4 × 2 × 12 = 96, assert confirmed | VERIFIED CORRECT | `source/006_...py` | Line 51 |
| 6 | Non-phosphine: PEPPSI (NHC) at col 12, CAS 1158652-41-5 confirmed in SDF | VERIFIED CORRECT | `source/006_...py` line 24; SDF entry 64 | — |
| 7 | All 12 catalyst CAS numbers confirmed present in Edelris SDF | VERIFIED CORRECT | `source/006_...py` lines 13–25; SDF entries 1–74 | — |
| 8 | NaOtBu absent from Round 2 base list | VERIFIED CORRECT | `source/006_...py` line 29 | BASES array |
| 9 | B1 = BPG3/Cs₂CO₃/dioxane correctly placed per script logic | VERIFIED CORRECT | `source/006_...py` lines 41–48 | Row/column mapping |
| 10 | Script layout matches document description (row blocks, base order, column decoration) | VERIFIED CORRECT | `source/006_...py` + `source/007_plt_subplots.py` | Lines 41–48; 17–89 |
| 11 | Controls rationale acceptable; B1 anchor is scientifically justified | VERIFIED CORRECT | `HTE_BH_round2_4x2x12.md` | Controls note |

---

## Actions Required Before Running the Plate

1. **[BLOCKING] Fix `007_plt_subplots.py`** — add the four missing variable definitions (copy from `006`, or import from it). Standalone reproducibility of the plate map PNG requires this fix. Do not record the current `007` as the canonical rendering script without it.

2. **[NON-BLOCKING] Correct "PEPSI" → "PEPPSI"** in `006_...py` line 24 and in the design document table. Re-render the plate map PNG after fixing. Do not dispense from the current image without noting the label discrepancy.

3. **[NON-BLOCKING] Expand the drift-detection protocol** to reference all six R1-tagged catalyst rows in the Cs₂CO₃/dioxane (row B) and K₃PO₄/dioxane (row C) blocks, not just B1. This strengthens the assay-drift check without adding any wells.
