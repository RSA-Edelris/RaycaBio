---
title: "Independent Audit: Phase 1 — Kinome Selectivity Profile for 6 PDK1 Ligands"
study_id: "7a39e116-e0d5-4e70-93c3-da6df54e7e1e"
run_id: "max-c0850e7424"
audited_phase: "Phase 1: Kinome selectivity profile for 6 PDK1 ligands"
auditor: "independent (re-computed from raw CSVs)"
date: "2026-09-07"
---

# Independent Audit: Kinome Selectivity Profile for 6 PDK1 Ligands

## Scope

This audit independently re-reads the five raw docking result CSVs, re-builds the compound–kinase pivot from scratch, and checks every key numerical claim in `phase_kinome_selectivity_profile.md` against that recomputed data. No values from the original analysis session are trusted without verification.

---

## Data Integrity

| Check | Result |
|:---|:---|
| All 5 CSVs present on disk | ✓ |
| Total rows across all CSVs | 475 (AGC 150 + probe5 81 + batch2 64 + batch3 114 + batch4 66) |
| Unique kinases | 43 |
| Unique SMILES (compounds) | 6 |
| All 6 SMILES map correctly to compound names | ✓ |
| Pivot shape after max-aggregation | (6, 43) — 6 compounds × 43 kinases |
| No unmapped SMILES | ✓ |

---

## PDK1 Engagement Claims

Phase document reports:

| Compound | Reported pIC50 | Audited pIC50 | Verdict |
|:---|:---|:---|:---|
| BX912 | 6.89 | **6.893** | ✓ |
| EL2003A | 6.47 | **6.473** | ✓ |
| EL2003A-A2U1 | 6.86 | **6.860** | ✓ |
| EL2003A-A4U1 | 6.91 | **6.913** | ✓ |
| EL5001A | 6.87 | **6.867** | ✓ |
| EL5003A | 6.93 | **6.933** | ✓ |
| Mean | 6.82 | **6.823** | ✓ |
| Weakest compound | EL2003A | **EL2003A** | ✓ |

All PDK1 values are consistent (differences are rounding to 2 d.p.).

---

## Universal Off-Target Claim (AurA)

Phase document: "AurA is the only kinase meeting this criterion (min 6.98, max 7.40, mean 7.28, CV 0.025)"

| Compound | Audited AurA pIC50 |
|:---|:---|
| BX912 | 7.403 |
| EL2003A | 7.360 |
| EL2003A-A2U1 | 7.400 |
| EL2003A-A4U1 | 7.403 |
| EL5001A | **6.980** (minimum) |
| EL5003A | 7.130 |

Recomputed: min 6.980, max 7.403, mean 7.279, CV 0.025. All six ≥ 6.90.

Audit confirms **no other kinase** achieves pIC50 ≥ 6.90 in all six compounds.

**Verdict: VERIFIED CORRECT.**

---

## Top Kinases by Mean pIC50

Phase document table vs. recomputed (top 10):

| Kinase | Reported mean | Audited mean | Reported Δ | Audited Δ | Verdict |
|:---|:---|:---|:---|:---|:---|
| AurA | 7.28 | **7.279** | +0.46 | +0.456 | ✓ |
| FLT3 | 7.04 | **7.042** | +0.22 | +0.219 | ✓ |
| JAK2 | 7.04 | **7.036** (as "JAK2-b") | +0.21 | +0.212 | ✓ (name note below) |
| FGFR1 | 7.03 | **7.026** | +0.20 | +0.202 | ✓ |
| MET | 6.96 | **6.958** | +0.13 | +0.134 | ✓ |
| CDK4 | 6.95 | **6.951** | +0.13 | +0.128 | ✓ |
| BRAF | 6.95 | **6.948** | +0.12 | +0.125 | ✓ |
| EGFR | 6.95 | **6.947** | +0.12 | +0.124 | ✓ |
| ROCK2 | 6.94 | **6.943** | +0.12 | +0.120 | ✓ |
| p38α | 6.93 | **6.929** | +0.11 | +0.106 | ✓ |

All values consistent with the reported figures to 2 d.p. **VERIFIED CORRECT.**

---

## Compound-Specific Off-Targets

Phase document criteria: max pIC50 ≥ 7.05 AND std ≥ 0.12.

Recomputed table (excluding AurA, which is classified as universal):

| Kinase | Reported max | Audited max | Top compound | Std | Verdict |
|:---|:---|:---|:---|:---|:---|
| FGFR1 | 7.32 | **7.323** | EL2003A-A4U1 | 0.195 | ✓ |
| BRAF | 7.28 | **7.277** | EL2003A-A4U1 | 0.234 | ✓ |
| CDK4 | 7.23 | **7.230** | EL2003A-A4U1 | 0.199 | ✓ |
| ROCK2 | 7.23 | **7.227** | EL2003A-A2U1 | 0.214 | ✓ |
| FLT3 | 7.21 | **7.213** | EL5003A | 0.151 | ✓ |
| PKACa | 7.08 | **7.077** | EL5001A | 0.196 | ✓ |
| BTK | 7.06 | **7.063** | EL2003A-A2U1 | 0.162 | ✓ |
| ABL1 | 7.05 | **7.053** | EL2003A-A2U1 | 0.133 | ✓ |

All entries verified. **VERIFIED CORRECT.**

---

## EL5001A Selectivity Claim

Phase document: "most selective; top off-target (PKACa) only +0.21 above PDK1"

Recomputed: PDK1 = 6.867. Top off-target = PKACa at 7.077, delta = +0.210. Second off-target = JAK2-b at 7.070, delta = +0.203.

The claim about PKACa being the top off-target is correct. Note that JAK2-b (+0.203) is a near-tied second, which the phase document did not flag; however, at this pIC50 level (< 7.1) and with ±0.3 scorer uncertainty, both are within noise of PDK1. **Substantively CORRECT; JAK2-b deserves mention as co-top-1.**

---

## Output Files

| File | Claimed size | Audited size | Verdict |
|:---|:---|:---|:---|
| `kinome_selectivity_matrix.csv` | 4,216 bytes | **4,216 bytes** | ✓ |
| `kinome_heatmap.png` | 256 KB | **262,432 bytes (256 KB)** | ✓ |
| `kinome_per_compound.png` | 176 KB | **181,066 bytes (176 KB)** | ✓ |

---

## Findings

### MINOR — F1: Kinase label "JAK2" vs. "JAK2-b"

The raw KLIFS data contains this kinase as `JAK2-b`. The phase document refers to it as `JAK2`. This is a label normalization — `JAK2-b` is a KLIFS-specific suffix distinguishing alternative crystal structures; the gene and protein are JAK2 (O60674). The reported mean pIC50 (7.04) is correct. No numerical error.

**Impact:** None on scores or conclusions. Traceability between phase document and raw data requires knowing this mapping.

### MINOR — F2: AurA also satisfies compound-specific criteria

AurA has max 7.403 and std 0.181, which exceeds the compound-specific thresholds (max ≥ 7.05, std ≥ 0.12). It was correctly excluded from the compound-specific table because it was already classified as universal. However, the phase document does not explicitly state this exclusion rule, which could confuse a reader who tries to reproduce the compound-specific table independently.

**Impact:** None on conclusions. Recommend adding a note: "AurA satisfies both criteria but is classified under universal off-targets."

### MINOR — F3: EL5001A JAK2-b not flagged

JAK2-b at 7.070 (delta +0.203) is effectively tied with PKACa as EL5001A's top off-target within scorer uncertainty (±0.3). The phase document describes only PKACa. At these pIC50 levels neither is distinguishable from the other, so the omission does not change the overall selectivity ranking but should be noted for clinical risk assessment.

**Impact:** None on compound ranking. Recommend noting JAK2-b as co-equal top off-target for EL5001A.

---

## Summary

| Severity | Count | Items |
|:---|:---|:---|
| CRITICAL | 0 | — |
| MAJOR | 0 | — |
| MINOR | 3 | F1 (JAK2 label), F2 (AurA exclusion rule undocumented), F3 (JAK2-b omitted for EL5001A) |

All numerical claims in the phase document are **confirmed correct** against the raw docking CSV files. The three minor findings are limited to labeling clarity and one small omission; none affect the compound rankings, off-target identification, or clinical recommendations.

The primary conclusions stand:
1. AurA is the only universal off-target (verified: only kinase ≥ 6.90 in all 6 compounds).
2. EL2003A has the weakest PDK1 engagement (6.47) and is not a selective PDK1 tool compound.
3. EL2003A-A4U1's CF₃ group drives the worst selectivity profile (FGFR1 7.32, BRAF 7.28, CDK4 7.23).
4. EL5001A and EL5003A are the primary advancement candidates.
