
## Audit scope

Phase: **Create detailed MD report and push to RSA-Edelris/RaycaBio GitHub**
Files audited: `drug_utils.py`, druggability scoring logic (reconstructed from session state), `pocket_analysis_full_report.md`
Auditor: independent verification pass (subagent failed to write file; audit performed by direct code execution)

---

## Finding 1 — MAJOR: No phase document exists

**Finding**: No `write_report` call was made for this phase before the push. The only record is a task-tracker auto-update. The methodology of the push step (which files were staged, how the report was assembled, what the commit contained) is not described in any document associated with this phase.

**Impact**: The phase is not self-documenting. Anyone checking provenance of the GitHub commit cannot verify which analysis outputs were included without inspecting the git tree directly.

**Evidence**: `write_report` tool was not called during the push phase. `audit_push_report_phase.md` (this file) is the first document written for this phase.

---

## Finding 2 — MAJOR: Bare `except Exception` silently converts ConvexHull failure to vol = 0.0

**Location**: `drug_utils.py` line 36–39

```python
try:
    vol = ConvexHull(ca).volume
except Exception:
    pass
```

**Finding**: Any `scipy.spatial.ConvexHull` failure (degenerate coplanar points, collinear Cα trace, < 4 non-coplanar points) silently returns `vol = 0.0`. A pocket scored with `vol = 0` gets a volume bin of 0 (below the minimum 1 assigned to `vol < 500`).

**Wait — re-check**: The code assigns `v = 1 if vol < 500`, so `vol = 0` gives `v = 1`, not 0. The silent failure therefore biases the score toward the lowest non-zero volume bin, not zero. This makes the failure look like "very small pocket" rather than "computation failed."

**Practical impact for this run**: All six pockets had ≥ 15 Cα coords and none were pathologically coplanar; all hulls succeeded (verified by non-zero volumes in output). Risk is latent for future use on very small or linear pockets.

---

## Finding 3 — MAJOR: `n_res` and `len(ca_coords)` can silently diverge

**Location**: `drug_utils.py` lines 17–33

`aa_codes` is populated for every residue triple regardless of whether a CA atom is found. `ca_coords` is only populated when a CA atom exists in the atom dict. Therefore:
- Composition fractions (hydrophobic, aromatic, etc.) use denominator `n = len(aa_codes)` = all triples
- ConvexHull is built from `len(ca_coords)` ≤ `n` points

If any residue triple is not in `all_atoms_dict` (e.g., chain/resseq mismatch), the fractions are correct but the hull underestimates volume with no warning.

**Practical impact for this run**: Triples were built directly from the same parsed atom dicts, so all residues were present. No divergence occurred. Risk is latent for cross-structure reuse.

---

## Finding 4 — MAJOR: Druggability score thresholds are heuristic with no published calibration

**Finding**: The volume bins (<500, 500–1500, 1500–4000, >4000 Å³), hydrophobicity bins, and literature score values (0/1/3) were invented for this run. They are not taken from a validated framework (SiteMap, fpocket, DoGSiteScorer, or similar). The final scores are internally consistent but cannot be compared to scores from other studies.

**Evidence**: No citation to a druggability scoring framework appears in the report or code. The bin boundaries are round numbers with no derivation.

**Impact**: Scores should be treated as relative rankings within this study, not absolute druggability predictions.

---

## Verified Correct

| Item | Check | Result |
|---|---|---|
| Jaccard CTX vs ATP | 3 shared / 80 union = 0.0375 → rounds to 0.04 | **CORRECT** |
| Jaccard CTX vs interface | 7 shared / 34 union = 0.2059 → rounds to 0.21 | **CORRECT** |
| Shared residues CTX vs ATP | L54(54), L58(58), V123(123) in both sets | **CORRECT** |
| Shared residues CTX vs iface | H121, R122 (CDK2); L90, V101, W102, I104, M105 (CyclinE1) | **CORRECT** |
| Druggability score CRBN main | bins: vol=3, hydro=2, arom=2, lit=3 → raw=10/12×10=8.3 | **CORRECT** |
| Druggability score CRBN zinc | bins: vol=1, hydro=0, arom=0, lit=0 → raw=1/12×10=0.8... wait | **SEE NOTE** |
| Druggability score CDK2 ATP | bins: vol=4, hydro=3, arom=1, lit=3 → raw=11/12×10=9.2 | **CORRECT** |
| Druggability score T-loop | bins: vol=2, hydro=3, arom=2, lit=1 → raw=8/12×10=6.7 | **CORRECT** |
| Druggability score Interface apo | bins: vol=2, hydro=2, arom=2, lit=1 → raw=7/12×10=5.8 | **CORRECT** |
| Druggability score CTX holo | bins: vol=3, hydro=3, arom=2, lit=2 → raw=10/12×10=8.3 | **CORRECT** |
| Score formula max (12) matches report | max = 4+3+2+3 = 12 | **CORRECT** |
| No 0-based/1-based index confusion | residue IDs used consistently as parsed integers; no off-by-one | **CORRECT** |
| No reversed positional arguments | `residue_descriptors(res_triples, all_atoms_dict)` — order matches all 6 call sites | **CORRECT** |
| GitHub push target | `RSA-Edelris/RaycaBio` confirmed in repo listing before push | **CORRECT** |

**Note on CRBN zinc score**: vol=518 → bin = 2 (500–1500), hydro=0.13 → bin 0, arom=0.00 → bin 0, lit=0. Raw = 2+0+0+0 = 2. Score = round(2/12×10, 1) = 1.7. Matches reported 1.7. ✓

---

## Summary

| Severity | Count | Items |
|---|---|---|
| CRITICAL | 0 | — |
| MAJOR | 4 | No phase doc; bare except vol=0; n/ca divergence; heuristic thresholds |
| VERIFIED CORRECT | 13 | All numerics, scores, residue sets, formula, push target |

No finding invalidates the reported results. The three code-level findings (bare except, n/ca divergence, no phase doc) are latent risks for future reuse rather than errors in the current outputs.

---

*Audited by: independent verification pass, 2026-09-15*
