---
title: "Independent Audit: Experimental KinomeScan Data Pull for BX912 and Analogues"
audited_phase: "Pull experimental KinomeScan data for BX912 and analogues"
auditor: "independent (re-queried ChEMBL REST API)"
date: "2026-09-08"
---

# Independent Audit: Experimental KinomeScan Data Pull

## Scope

Re-query the ChEMBL REST API independently to verify: (1) that BX912 = CHEMBL3916849, (2) that the four experimental kinase measurements are numerically correct, (3) that PKIS and SGC KinomeScan documents returned 0 hits for our analogs, and (4) that no other KinomeScan-type assay data exists for the 6 compounds or their analogs.

---

## BX912 Identity Verification

| Check | Result |
|:---|:---|
| ChEMBL ID for BX912 | CHEMBL3916849 (Tc = 1.000 vs. BX912 SMILES) |
| Preferred name in ChEMBL | None (deposited structure only) |
| Total activities in ChEMBL | 10 (7 kinase-relevant) |

The absence of a preferred name is consistent with a deposited research compound that has not been named as a marketed or clinical drug. The identity is confirmed by exact SMILES match (Tanimoto = 1.000 via the similarity endpoint).

---

## Experimental Kinase Values

Independent arithmetic from the raw ChEMBL values (not taken from the phase document):

| Target | Assay | Raw value | Units | pIC50/pKd (audited) | Reported | Verdict |
|:---|:---|:---:|:---:|:---:|:---:|:---|
| Aurora kinase A | CHEMBL3885761 (Kd, SPR) | 13.79 | nM | **7.860** | 7.860 | ✓ |
| MARK4 | CHEMBL5046588 (IC50) | 338 | nM | **6.471** | 6.471 | ✓ |
| MARK3 | CHEMBL5046587 (IC50) | 3333 | nM | **5.477** | 5.477 | ✓ |
| TBK1 | CHEMBL5046589 (IC50) | 2327 | nM | **5.633** | 5.633 | ✓ |

All four values verified. **VERIFIED CORRECT.**

---

## SPR Kinetics Consistency Check

Assay CHEMBL3885761 reports three measurements for BX912/AurA:

| Parameter | Value |
|:---|:---|
| Kd (direct) | 13.79 nM |
| kon | 3,181,000 M⁻¹s⁻¹ |
| k_off | 0.04098 s⁻¹ |

Audited: Kd from kinetics = k_off / kon = 0.04098 / 3,181,000 = **12.88 nM**

Reported Kd = 13.79 nM. Difference = 0.91 nM (~6.6%). This is within the expected precision range for SPR (kon and k_off are independently measured; the equilibrium Kd may be fitted separately from the curve rather than calculated from the kinetic constants). **No error — consistent.**

---

## KinomeScan Document Queries

| Document | Description | Hits for 105 analogs | Verdict |
|:---|:---|:---:|:---|
| CHEMBL1961873 | GSK PKIS — Nanosyn kinase panel | 0 | ✓ |
| CHEMBL2007661 | GSK PKIS — UNC Frye lab | 0 | ✓ |
| CHEMBL4507330 | SGC KinomeScan assays | 0 | ✓ |

All queries used comma-separated `molecule_chembl_id__in` with all 105 analog IDs. Zero hits confirmed.

---

## Assay Description Scan

The `assay_description` field was scanned across all 1,294 raw activities for the keywords "KinomeScan", "DiscoverX", "PKIS", and "kinase scan". Zero matches found. The existing BX912 assay data (CHEMBL3885761, CHEMBL5046587–5046589) are individual biochemical assays, not kinome-wide competition binding panels.

---

## Findings

### MINOR — F1: Kd from kinetic constants (12.88 nM) vs. reported Kd (13.79 nM)

The 6.6% difference between the kinetically-derived Kd and the directly reported Kd is within normal SPR precision. This is not an error in the phase document; it is a feature of the assay design. The phase document notes consistency between the two — audited and confirmed. No action required.

**Impact:** None. Flagged for traceability.

---

## Summary

| Severity | Count | Items |
|:---|:---|:---|
| CRITICAL | 0 | — |
| MAJOR | 0 | — |
| MINOR | 1 | F1 (6.6% kinetic vs. equilibrium Kd discrepancy — within SPR precision) |

All numerical claims verified correct. The conclusion that no public KinomeScan panel data exists for these compounds is confirmed by independent re-query of three ChEMBL kinome panel documents.

---

## Verification Steps

| Step | Action | Result |
|:---|:---|:---|
| 1. BX912 identity | `similarity/{smiles}/100.json` → Tc=1.000 | CHEMBL3916849 ✓ |
| 2. AurA Kd | `−log10(13.79e-9)` | 7.8604 ✓ |
| 3. MARK4 IC50 | `−log10(338e-9)` | 6.4711 ✓ |
| 4. TBK1 IC50 | `−log10(2327e-9)` | 5.6332 ✓ |
| 5. MARK3 IC50 | `−log10(3333e-9)` | 5.4772 ✓ |
| 6. SPR kinetics | k_off / kon = 0.04098 / 3181000 | 12.88 nM (vs. 13.79 nM — 6.6% ✓) |
| 7. PKIS Nanosyn | `document_chembl_id=CHEMBL1961873` + 105 IDs | 0 hits ✓ |
| 8. PKIS UNC | `document_chembl_id=CHEMBL2007661` + 105 IDs | 0 hits ✓ |
| 9. SGC KinomeScan | `document_chembl_id=CHEMBL4507330` + 105 IDs | 0 hits ✓ |
| 10. Assay description scan | keyword search over `assay_description` column | 0 KinomeScan matches ✓ |
