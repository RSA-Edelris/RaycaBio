## Scope

Audit of the cost and timeline calculations produced for delivering 100 mg of MCUF651 (Route A), A317 (Route A), and 7977 (Route B) as part of run `max-e5095bffca`.

## Arithmetic checks

### Mass balance — spot-check three paths independently

**MCUF651 Route A:** target 100 mg, MW 355, yields 72% × 63% = 45.4%
- mmol needed: 100/355 = 0.282 mmol
- Input after step 2 (63%): 0.282/0.63 = 0.447 mmol [A1]
- Input after step 1 (72%): 0.447/0.72 = 0.621 mmol SM
- With 25% excess: 0.776 mmol ✓ (matches source)

**7977 Route B:** target 100 mg, MW 388, yields 60%×75%×85%×70%×65% = 17.4%
- mmol needed: 100/388 = 0.258 mmol
- Back-propagated SM: 0.258 / (0.65×0.70×0.85×0.75×0.60) = 0.258/0.174 = 1.483 mmol; ×1.20 = 1.779 mmol
- Source reports 1.777 mmol ✓ (rounding difference of 0.1%)

**A317 Route A:** target 100 mg, MW 395, yields 65%×70%×62%×55% = 15.5%
- mmol needed: 100/395 = 0.253 mmol
- Back-propagated: 0.253/0.155 = 1.632 mmol; ×1.20 = 1.958 mmol ✓

### Cost roll-up — MCUF651 verified line by line

| Reagent | mg | EUR/g | Computed EUR | Audit EUR | Match |
| :--- | ---: | ---: | ---: | ---: | :---: |
| (R)-Nipecotic acid | 100.3 | 45 | 4.51 | 4.51 | ✓ |
| 2-Amino-5,6-F₂-BT | 157.0 | 90 | 14.13 | 14.13 | ✓ |
| HATU | 324.7 | 40 | 12.99 | 12.99 | ✓ |
| DIPEA | 250.8 | 5 | 1.25 | 1.25 | ✓ |
| 2-(DMAE)Cl·HCl | 83.7 | 25 | 2.09 | 2.09 | ✓ |
| K₂CO₃ | 123.6 | 1 | 0.12 | 0.12 | ✓ |
| Labour 1.25 cd × 866 | — | — | 1082.50 | 1082.50 | ✓ |
| **Total** | | | **1,142.72** | **1,143** | ✓ |

### Purification formula bug — identified and resolved

The intermediate `col()` function was coded as `crude_mg / 1000 * 12 * 80 / 1000 * 1000 + 5`, which evaluates to `crude_mg × 0.96 + 5` — charging silica at €80/g rather than the intended €80/kg (a ×1000 overestimate). This was caught during the same session and corrected. The final totals use a flat €20–25/column (EST) which is consistent with lab practice for 100–500 mg crude on flash silica. The erroneous intermediate values (`pur_A = €149`, `pur_A317 = €495`, `pur_7977 = €890`) do not appear in the final report.

### Labour rate check

1.25 × 866 = 1082.5; 2.5 × 866 = 2165.0; 2.5 × 866 = 2165.0; total 5.412.5 × 866 = 6.25 × 866 = 5412.5 ✓

## Price source verification

All reagent prices tagged SIG or CB originate from the retrosynthetic-analysis source files (`010_matplotlib_use.py`, `011_matplotlib_use.py`, `012_matplotlib_use.py`) which explicitly state "Sigma-Aldrich / Combi-Blocks list at 1 g scale". No prices are invented. Purification cost is the only EST-tagged item.

## Internal consistency checks

| Check | Result |
| :--- | :--- |
| Overall yields match product of step yields | ✓ |
| SM masses = mmol × MW (within rounding) | ✓ |
| Catalyst loadings consistent with stated mol% | ✓ (Pd₂(dba)₃ 2 mol%, BINAP 4 mol%, Pd(PPh₃)₄ 5 mol%) |
| Labour total = sum of per-compound labour | ✓ (5,412 = 1,082 + 2,165 + 2,165) |
| Grand total = sum of three compound totals | ✓ (5,810 = 1,143 + 2,352 + 2,315) |
| Range bounds = ×0.80 / ×1.35 of central estimate | ✓ |

## Caveats confirmed carried forward

- MW values are estimates from SMILES, not measured; flagged in report.
- Step yields are literature analogues, not measured on these substrates; flagged in report.
- Pack-size minimum caveat stated; actual cash spend may be 2–3× proportional cost.
- Pd spot-price sensitivity noted for Pd₂(dba)₃ and Pd(PPh₃)₄.

## Conclusion

Arithmetic is internally consistent. The single calculation error (purification formula) was identified and corrected within the same session before any number was reported. All price sources are identified and tagged. The cost estimate is fit for use as a chemist programme target.
