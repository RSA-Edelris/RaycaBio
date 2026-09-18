# Audit: PROTAC_CRBN_ERalpha_Ternary_Results.md and PROTAC_Project_History.md

**Date:** 2026-09-16  
**Audited by:** Main session auditor (write blocked by stop hook on first attempt; file created retroactively)  
**Documents examined:** `PROTAC_CRBN_ERalpha_Ternary_Results.md`, `PROTAC_Project_History.md`  
**Trigger:** Phase-14 quality gate on result and history documents

---

## CRITICAL

### C-1 — Evidence Limits §1 cites model_0 values as if they are best-model values

**Source:** Results.md, "Evidence Limits" §1 (ARV_009 and ARV_003).

The section states: *"lig→CRBN = 0.4197 and 0.4674 respectively"* for ARV_009 and ARV_003.

Cross-checking against the Full Confidence Scores table in the same document:
- ARV_009 model_0: lig→CRBN = **0.4197** ← model_0 value
- ARV_003 model_0: lig→CRBN = **0.4674** ← model_0 value

The Cooperativity Ranking table (best-model methodology, documented at the header) identifies:
- ARV_009 best = **model_1**, lig→CRBN = **0.4901** (Δ +0.133)
- ARV_003 best = **model_2**, lig→CRBN = **0.5249** (Δ +0.119)

The Evidence Limits section reverts silently to model_0 for these two compounds without disclosure. A reader who reads only the Evidence Limits section encounters values 16% (ARV_009) and 11% (ARV_003) lower than the best-model values used in the ranking.

**Impact on conclusion:** The qualitative claim ("CRBN engagement not supported") is partially preserved — ARV_003 and ARV_009 are the two lowest-ranked compounds even under best-model ranking. However, the stated Δ = +0.062 for both cannot be reproduced from any values in the document under any interpretation (see MAJOR M-1 below).

---

## MAJOR

### M-1 — "Δ = +0.062 for both" in Evidence Limits §1 is numerically unsupported

**Source:** Results.md, Evidence Limits §1.

The section states: *"Constrained-run gain (Δ = +0.062 for both) is within single-seed sampling noise."*

Under no documented interpretation does +0.062 arise:
- If Δ = model_0 constrained − ARV-471 reference (0.2306): ARV_009 gives 0.4197 − 0.2306 = **0.1891**, ARV_003 gives 0.4674 − 0.2306 = **0.2368**. Neither is 0.062.
- If Δ = best-model constrained − ARV-471 reference: ARV_009 gives 0.4901 − 0.2306 = **0.2595**, ARV_003 gives 0.5249 − 0.2306 = **0.2943**. Neither is 0.062.
- If Δ = per-compound constrained − per-compound unconstrained (from job 6534300): no per-compound unconstrained lig→CRBN values are stated in either document, so the calculation cannot be verified.

An independent Phase-13 audit (see `PROTAC_Project_History.md` Verification section) already flagged: *"Δ unconstrained column uses hardcoded reference values with no file-level provenance."* The Δ = +0.062 value in the Evidence Limits section inherits this same provenance gap.

The Δ column in the Ranking table shows Δ = +0.119 and +0.133 for ARV_003 and ARV_009 respectively under the best-model ranking. Neither of these is +0.062 either, and their computational basis is equally untraceable.

**Affected claim:** The specific claim "within single-seed sampling noise" cannot be verified without the per-compound unconstrained reference values.

---

### M-2 — Project History Key Results table uses model_0 throughout; ranking differs from Results.md

**Source:** `PROTAC_Project_History.md`, "Key Results" table (header reads `lig→CRBN (model_0)`).

The Project History table reports model_0 values for all compounds. For three compounds, the best model is not model_0:
- ARV_008: History shows 0.5349 (model_0); Results.md best = 0.5597 (model_2)
- ARV_003: History shows 0.4674 (model_0); Results.md best = 0.5249 (model_2)
- ARV_009: History shows 0.4197 (model_0); Results.md best = 0.4901 (model_1)

**Rank-order difference:** The History table ranks ARV_010 (0.5555) above ARV_008 (0.5349) at positions 5 and 7. The Results.md ranking reverses this: ARV_008 (0.5597) at rank 5, ARV_010 (0.5555) at rank 6. A reader comparing the two documents finds contradictory rank assignments for compounds at ranks 5–8.

The Project History header correctly labels these as model_0, so the values are internally consistent within that document; the inconsistency is between documents.

---

### M-3 — Surface lysine analysis was performed only on model_0 for each compound

**Source:** `PROTAC_Project_History.md`, "What was not verified" section (documented as known gap).

The Results.md lysine table sources NZ–CRBN distances from model_0 for all compounds, including ARV_003 and ARV_009 where model_0 is not the best-scoring pose. For these two compounds the lysine presentation geometry is the most uncertain, and the geometric analysis is drawn from the least confident pose.

This was noted as an acknowledged limitation in the Project History; it is recorded here for completeness.

---

## VERIFIED CORRECT

**V1 — Cooperativity Ranking table uses best-model values.**  
The Ranking table in Results.md correctly identifies model_1 for ARV_009 (0.4901), model_2 for ARV_003 (0.5249), and model_2 for ARV_008 (0.5597). These are the correct best models from the Full Confidence Scores table. ✓

**V2 — CRBN self-iptm mean = 0.273, ERα self-iptm mean = 0.906.**  
Computed from best-model rows: ERα self-iptm values 0.8862–0.9324 (mean 0.906), CRBN self-iptm values 0.2254–0.3008 (mean 0.273). Both values appear in Results.md Per-Chain Confidence Summary. Verified from the Full Confidence Scores table. ✓

**V3 — ARV-471 unconstrained reference lig→CRBN = 0.2306.**  
Stated in the Results.md header and cross-referenced in Project History. This value appears in multiple places; it is the model_0 value from job 6465991. ✓

**V4 — All 10 constrained best-model values exceed 0.2306.**  
Lowest best-model lig→CRBN is ARV_009 = 0.4901 > 0.2306. Confirmed from ranking table. ✓

**V5 — Evidence Limits §2–§7 cite compound-specific values that are consistent with the Ranking table.**  
Sections 2–7 are qualitative or cite values from the ranking table (lig→ERα for ARV_010 = 0.6568, CRBN self-iptm floor, clash count for ARV_001). These are traceable to source values. ✓

---

## Summary

| ID | Severity | Finding | Affects main ranking? |
|:--:|:--------:|:--------|:---------------------:|
| C-1 | CRITICAL | Evidence Limits §1 uses model_0 lig→CRBN values (0.4197/0.4674), not best-model (0.4901/0.5249) | Partially — bottom-2 qualitative conclusion preserved; cited values are wrong |
| M-1 | MAJOR | "Δ = +0.062 for both" cannot be reproduced from any stated value in either document | Yes — noise claim unverifiable |
| M-2 | MAJOR | Project History Key Results uses model_0; contradicts Results.md ranking at ranks 5–8 | Yes — rank-5 vs rank-7 for ARV_008 depends on the document read |
| M-3 | MAJOR | Lysine geometry for ARV_003/ARV_009 drawn from model_0 (non-best pose) | Acknowledged limitation |

The best-model cooperativity ranking, CRBN self-iptm statistics, and qualitative conclusions are verified correct. The per-document provenance of the Δ column and the Evidence Limits model-selection error should be corrected before citing these documents in publications.
