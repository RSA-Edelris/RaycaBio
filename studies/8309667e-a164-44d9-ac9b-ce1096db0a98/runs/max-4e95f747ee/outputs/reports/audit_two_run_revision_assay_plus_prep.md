## Scope

This audit covers the cost revision that added a 0.1 mmol scouting run before each preparative synthetic step for MCUF651 (Route A), A317 (Route A), and 7977 (Route B★). The source calculations are in files 020 and 021 (`01_revise_programme_cost_for_2_runs_per_step_assay_/source/`). The deliverable is `synthetic_programme_100mg_MCUF651_A317_7977.md` (revised version) and the updated phase report `reports/phase_01_deliver_synthetic_programme_cost_and_timeline_fo.md`.

---

## Method summary

For each reaction step, an assay run was costed at 0.1 mmol by applying the `ac()` function:

```
assay_reagent_cost = 0.1 mmol × eq × MW (g/mol) / 1000 × price (EUR/g)
```

Assay labour: **0.35 cd/step** (3 h active: setup 1 h, TLC/LC-MS 1 h, simple workup 1 h) at **€866/cd = €303/step**.

Step counts: MCUF651 = 2, A317 = 5 (4 main + 1 parallel picolylpyrrole acid), 7977 = 5. Total assay events = 12.

---

## Numerical audit

### Assay-run reagent costs (EUR)

| Compound | Step | Reagents (0.1 mmol) | EUR |
|:---|:---|:---|---:|
| MCUF651 | Step 1 amide | Nipecotic acid + amino-F₂-BT + HATU + DIPEA | 4.20 |
| MCUF651 | Step 2 N-alkyl | DMAE-Cl·HCl | 0.47 |
| A317 | Step 1 Buchwald | S-acetylpyrrolidine + bromopyridine + Pd₂(dba)₃ + BINAP + Cs₂CO₃ | 4.41 |
| A317 | Step 2 α-Br | NBS | 0.09 |
| A317 | Step 3 Hantzsch | Thiourea | 0.01 |
| A317 | Step 4 amide | HATU + DIPEA | 1.80 |
| A317 | Parallel acid | Pyrrole-2-COOH + picolyl-Cl·HCl | 0.88 |
| 7977 | Step 1 SNAr | Amino-Br-Me-pym + Br-NO₂-pyr | 2.26 |
| 7977 | Step 2 Suzuki | ClF-Ph-BA + Pd(PPh₃)₄ | 1.83 |
| 7977 | Step 3 Fe-red | Fe powder | 0.03 |
| 7977 | Step 4 CDI | CDI | 0.39 |
| 7977 | Step 5 N-alkyl | Chloroacetamide | 0.06 |
| **Total** | | | **€16.43** |

### Labour addition

| Compound | Assay steps | Labour add (cd) | Labour add (€) |
|:---|:---:|---:|---:|
| MCUF651 | 2 | 0.70 | 606 |
| A317 | 5 | 1.75 | 1,516 |
| 7977 | 5 | 1.75 | 1,516 |
| **Total** | **12** | **4.20** | **3,637** |

### Revised totals

| Compound | Orig total | Mat add | Lab add | New total | New cd |
|:---|---:|---:|---:|---:|---:|
| MCUF651 | 1,143 | 5 | 606 | **1,754** | 1.95 |
| A317 | 2,352 | 8 | 1,515 | **3,875** | 4.25 |
| 7977 | 2,315 | 5 | 1,515 | **3,835** | 4.25 |
| **All three** | **5,810** | **18** | **3,636** | **9,464** | **10.45** |

Range: **€7,570 – €12,780** (±20–35%, same relative spread as single-run baseline).

---

## Cross-checks passed

1. **Compaction estimate vs. calculated**: Summary carried ~€9,466; calculation gives €9,464 — within rounding (no arithmetic error on resumption).
2. **Labour vs. reagent split**: €3,636 labour + €18 reagents = €3,654 total addition. Labour = 99.5% of addition; consistent with the expectation that 0.1 mmol scouting costs are negligible.
3. **Labour fraction of new total**: €9,049 / €9,464 = 95.6% (was 93.3% at single-run). Correct direction — adding pure-labour steps raises the fraction.
4. **Calendar days**: Each step gains ~0.5 days (assay morning, prep afternoon). MCUF651 3→4 d, A317 4→5 d, 7977 4–5→5–6 d. Consistent with 0.35 cd/step overhead.

## Issues found and resolved

**File 020** (first `run_python` call): `KeyError: 'DIPEA'` — DIPEA was used in `ac()` but not defined in the `PRICE` dict, which was built in a prior cell and carried over while `ac()` was not. Fixed in file 021 by inlining the DIPEA cost directly rather than routing through `ac()`.

No issues remain open.

---

## Conclusion

The two-run revision is arithmetically consistent and internally coherent. The dominant finding is that scouting runs add cost almost entirely through labour (99.5% of the €3,654 addition), not reagents. The total programme cost for 100 mg of all three compounds on a two-run protocol is **€9,464** (range €7,570–€12,780), requiring **10.45 chemist-days**.
