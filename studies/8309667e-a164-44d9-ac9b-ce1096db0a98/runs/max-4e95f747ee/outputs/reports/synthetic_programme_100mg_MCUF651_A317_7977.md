
## Scope and conventions

This document delivers the bottom-up synthetic programme for 100 mg of each final compound using the best recommended route established in this study. All costs are in EUR. Labour is charged at **€866 per chemist-day (8 h active working time)**; overnight reactions are not charged because no chemist is present. Reaction running time and chemist active time are listed separately. Prices marked **SIG** were taken from Sigma-Aldrich catalogue at 1 g scale; prices marked **CB** from Combi-Blocks catalogue at 1 g scale, both as stated in the retrosynthetic-analysis source files for this session. Prices marked **EST** are not from a live catalogue and carry higher uncertainty. An estimate built on invented prices is worse than no estimate; every line in the reagent tables below is tagged.

MW estimates are derived from SMILES (targets ~355, ~395, ~388 g/mol for MCUF651, A317, 7977 respectively); a ±5% MW error propagates to ±5% in all masses and less than ±3% in total cost.

---

## 1. MCUF651 — Route A (2 steps, 45% overall)

**Route:** (R)-Nipecotic acid + 2-amino-5,6-difluorobenzothiazole → amide coupling (HATU/DIPEA, DMF, 0 °C → rt, 12 h, **72%**) → [A1] → N-alkylation with 2-(DMAE)Cl·HCl (K₂CO₃, MeCN, 80 °C, 8 h, **63%**) → MCUF651

### Mass balance tree

| Stage | Species | mmol | Mass |
| :--- | :--- | ---: | ---: |
| SM input | (R)-Nipecotic acid | 0.776 | 100 mg |
| SM input | 2-Amino-5,6-F₂-benzothiazole | 0.776 | 157 mg |
| Step 1 output | [A1] amide intermediate | 0.559 | 140 mg |
| **Step 2 output** | **MCUF651** | **0.282** | **100 mg** |

Starting scale includes 25% practical excess to account for transfer and workup losses.

### Reagent and material costs

| Reagent | Used (mg) | EUR/g | EUR | Source | Pack | Lead time |
| :--- | ---: | ---: | ---: | :--- | :--- | :--- |
| (R)-Nipecotic acid | 100 | 45 | 4.51 | SIG | 1 g | 1–3 d |
| 2-Amino-5,6-F₂-benzothiazole | 157 | 90 | 14.13 | CB | 500 mg | 1–5 d |
| HATU | 325 | 40 | 12.99 | SIG | 5 g | 1–3 d |
| DIPEA | 251 | 5 | 1.25 | SIG | 100 mL | 1–3 d |
| 2-(DMAE)Cl·HCl | 84 | 25 | 2.09 | SIG | 5 g | 1–3 d |
| K₂CO₃ | 124 | 1 | 0.12 | SIG | 500 g | 1–3 d |
| DMF (step 1, 5 mL) | — | — | 0.08 | SIG | bulk | — |
| MeCN (step 2, 5 mL) | — | — | 0.06 | SIG | bulk | — |
| **Reagents + solvents** | | | **35.23** | | | |
| Purification (1 column + 1 extraction) | — | — | 25 | EST | — | — |
| **Materials subtotal** | | | **60** | | | |

### Labour and schedule

| Step | Reaction time | Chemist active | Calendar span |
| :--- | :--- | :--- | :--- |
| Step 1: amide coupling | 12 h overnight | 2.5 h (setup + workup + column) | Day 1 pm → Day 2 am |
| Step 2: N-alkylation | 8 h (can run overnight) | 2.5 h (setup + workup) | Day 2 pm → Day 3 am |
| **Total** | | **0.6 h + 4 h = ~0.65 cd** | **3 working days** |

Rounding to **1.25 chemist-days** to account for TLC monitoring, product characterisation (¹H NMR), and contingency.

Labour cost: 1.25 × €866 = **€1,082**

### Step 2 can run in parallel with NMR confirmation of [A1] — no waiting bottleneck

### MCUF651 total

| Pool | EUR |
| :--- | ---: |
| Materials + purification | 60 |
| Labour (1.25 cd) | 1,082 |
| **Total** | **1,143** |
| **Range** | **€970 – €1,490** |

Critical path: fully linear (2 steps). Elapsed time from SM receipt to 100 mg isolated: **3 working days.**

---

## 2. A317 — Route A (4 steps + parallel acid synthesis, 15.5% overall)

**Route:** (S)-2-Acetylpyrrolidine + 2-bromopyridine → Buchwald N-arylation (Pd₂(dba)₃/(±)-BINAP, Cs₂CO₃, toluene, 90 °C, 12 h, **65%**) → [A1] → α-bromination (NBS, CHCl₃, −10 °C, **70%**) → [A2] → Hantzsch cyclisation (thiourea, EtOH, reflux, **62%**) → [A3] → amide coupling with 1-(4-picolyl)pyrrole-2-carboxylic acid (HATU/DIPEA, DMF, rt, 12 h, **55%**) → A317

**Parallel (off critical path):** Pyrrole-2-COOH + 4-picolyl chloride·HCl → 1-(4-picolyl)pyrrole-2-carboxylic acid (K₂CO₃, DMF, 60 °C, 6 h, 70%)

Route A is preferred over Route B (Pd-free) because N-arylation at step 1 renders the pyrrolidine nitrogen tertiary throughout; Route B's SNAr at 130 °C as the final step carries a documented epimerisation risk at the α-chiral centre.

### Mass balance tree

| Stage | Species | mmol | Mass |
| :--- | :--- | ---: | ---: |
| SM input | (S)-2-Acetylpyrrolidine | 1.958 | 222 mg |
| SM input | 2-Bromopyridine | 2.056 | 325 mg |
| Step 1 output | [A1] N-arylated ketone | 1.273 | 210 mg |
| Step 2 output | [A2] α-bromoketone | 0.891 | 206 mg |
| Step 3 output | [A3] 2-aminothiazole | 0.553 | 118 mg |
| Parallel output | Picolylpyrrole acid | 0.388 | 98 mg |
| **Step 4 output** | **A317** | **0.253** | **100 mg** |

### Reagent and material costs

**Step 1 — Buchwald N-arylation**

| Reagent | Used (mg) | EUR/g | EUR | Source | Lead |
| :--- | ---: | ---: | ---: | :--- | :--- |
| (S)-2-Acetylpyrrolidine | 222 | 130 | 28.80 | SIG | **2–3 wk** ⚠ |
| 2-Bromopyridine | 325 | 15 | 4.87 | SIG | 1–2 d |
| Pd₂(dba)₃ (2 mol%) | 36 | 250 | 8.96 | SIG | 2–5 d |
| (±)-BINAP (4 mol%) | 49 | 500 | 24.38 | SIG | 2–5 d |
| Cs₂CO₃ (2 eq) | 1276 | 15 | 19.14 | SIG | 1–2 d |
| Toluene (5 mL) | — | — | 0.06 | SIG | — |

**Step 2 — α-Bromination**

| Reagent | Used (mg) | EUR/g | EUR | Source | Lead |
| :--- | ---: | ---: | ---: | :--- | :--- |
| NBS (1.05 eq) | 198 | 5 | 0.99 | SIG | 1–2 d |
| CHCl₃ (5 mL) | — | — | 0.10 | SIG | — |

**Step 3 — Hantzsch cyclisation**

| Reagent | Used (mg) | EUR/g | EUR | Source | Lead |
| :--- | ---: | ---: | ---: | :--- | :--- |
| Thiourea (1.2 eq) | 68 | 1 | 0.07 | SIG | 1–2 d |
| EtOH / K₂CO₃ | — | — | 0.06 | SIG | — |

**Step 4 — Amide coupling**

| Reagent | Used (mg) | EUR/g | EUR | Source | Lead |
| :--- | ---: | ---: | ---: | :--- | :--- |
| HATU (1.1 eq) | 193 | 40 | 7.70 | SIG | 1–2 d |
| DIPEA (2.5 eq) | 149 | 5 | 0.74 | SIG | 1–2 d |
| DMF (5 mL) | — | — | 0.08 | SIG | — |

**Parallel — 1-(4-picolyl)pyrrole-2-carboxylic acid**

| Reagent | Used (mg) | EUR/g | EUR | Source | Lead |
| :--- | ---: | ---: | ---: | :--- | :--- |
| Pyrrole-2-carboxylic acid | 77 | 35 | 2.68 | SIG | 1–2 d |
| 4-Picolyl chloride·HCl | 113 | 30 | 3.40 | CB | 1–5 d |
| K₂CO₃ / DMF | — | — | 0.07 | SIG | — |

| Pool | EUR |
| :--- | ---: |
| All reagents + solvents | 102 |
| Purification (4 columns; step 2 telescoped) | 85 |
| **Materials subtotal** | **187** |

### Labour and schedule

| Step | Reaction time | Chemist active | Calendar day |
| :--- | :--- | :--- | :--- |
| Parallel acid + step 1 Buchwald set-up | 12 h overnight | 3 h | Day 1 |
| Step 1 workup + column | — | 3 h | Day 2 am |
| Step 2 α-bromination (use immediately) | 3 h (−10 °C) | 4 h | Day 2 pm |
| Step 3 Hantzsch (telescoped, same day) | 1 h reflux | 3 h | Day 3 am |
| Step 4 amide coupling | 12 h overnight | 1.5 h set-up | Day 3 pm |
| Step 4 workup + column | — | 3 h | Day 4 am |
| **Total** | | **~2.5 cd** | **4 working days** |

Labour cost: 2.5 × €866 = **€2,165**

Note: [A2] is unstable; it should be used the same day it is prepared (documented warning in the original scheme). This drives the Day 2 pm α-Br → Day 3 am Hantzsch sequence. [A1] column therefore must be completed by early Day 2 pm.

### A317 total

| Pool | EUR |
| :--- | ---: |
| Materials + purification | 187 |
| Labour (2.5 cd) | 2,165 |
| **Total** | **2,352** |
| **Range** | **€1,930 – €3,175** |

Elapsed time from SM receipt to 100 mg isolated: **4 working days.**
Elapsed from ordering: **3–4 weeks** (limited by (S)-2-acetylpyrrolidine lead time).

---

## 3. 7977 — Route B ★ Recommended (5 steps, 17.4% overall)

**Route:** 2-Amino-4-bromo-5-methylpyrimidine + 3-bromo-2-nitropyridine → SNAr (K₂CO₃, DMF, 100 °C, 8 h, **60%**) → [B1] → Suzuki ((2-Cl-4-F-Ph)boronic acid, Pd(PPh₃)₄, K₂CO₃, dioxane/H₂O, 80 °C, **75%**) → [B2] → Fe/AcOH reduction (EtOH, 80 °C, 2 h, **85%**) → [B3] → CDI cyclisation (THF, rt → 60 °C, **70%**) → [B4] → N-alkylation with chloroacetamide (K₂CO₃, DMF, 60 °C, 6 h, **65%**) → 7977

Route B is preferred over Route A (which reverses steps 2 and 3) because Suzuki before reduction avoids palladium-mediated reduction of the nitro group and gives a higher cumulative yield (22% vs 19%).

### Mass balance tree

| Stage | Species | mmol | Mass |
| :--- | :--- | ---: | ---: |
| SM input | 2-Amino-4-bromo-5-Me-pyrimidine | 1.777 | 334 mg |
| SM input | 3-Bromo-2-nitropyridine | 1.866 | 379 mg |
| Step 1 output | [B1] SNAr diarylamine | 1.066 | 288 mg |
| Step 2 output | [B2] Suzuki product | 0.800 | 260 mg |
| Step 3 output | [B3] diamine | 0.680 | 204 mg |
| Step 4 output | [B4] N-H bicycle | 0.476 | 154 mg |
| **Step 5 output** | **7977** | **0.258** | **100 mg** |

### Reagent and material costs

| Reagent | Used (mg) | EUR/g | EUR | Source | Lead |
| :--- | ---: | ---: | ---: | :--- | :--- |
| 2-Amino-4-bromo-5-Me-pyrimidine | 334 | 75 | 25.06 | CB | **1–4 wk** ⚠ |
| 3-Bromo-2-nitropyridine | 379 | 40 | 15.15 | SIG | 1–2 d |
| K₂CO₃ (steps 1 + 5) | 601 | 1 | 0.60 | SIG | 1–2 d |
| (2-Cl-4-F-Ph)boronic acid | 171 | 50 | 8.55 | SIG | 1–3 d |
| Pd(PPh₃)₄ (5 mol%) | 51 | 150 | 7.70 | SIG | 2–5 d |
| Fe powder (3 eq) | 112 | 2 | 0.22 | SIG | 1–2 d |
| Glacial AcOH (step 3) | — | — | 0.05 | SIG | — |
| CDI (1.2 eq) | 110 | 20 | 2.20 | SIG | 1–2 d |
| Chloroacetamide (1.2 eq) | 45 | 5 | 0.22 | SIG | 1–2 d |
| Solvents (DMF/dioxane/EtOH/THF) | — | — | 0.45 | SIG | — |
| **Reagents + solvents** | | | **60** | | |
| Purification (4 columns; step 3 may crystallise) | — | — | 90 | EST | — |
| **Materials subtotal** | | | **150** | | |

### Labour and schedule

| Step | Reaction time | Chemist active | Calendar day |
| :--- | :--- | :--- | :--- |
| Step 1 SNAr (100 °C, 8 h) | 8 h daytime | 2.5 h setup + workup | Day 1 |
| Step 1 column | — | 3 h | Day 2 am |
| Step 2 Suzuki (80 °C, 12 h) | 12 h overnight | 1.5 h setup | Day 2 pm |
| Step 2 workup + column | — | 3 h | Day 3 am |
| Step 3 Fe reduction (80 °C, 2 h) | 2 h | 2 h setup + workup | Day 3 pm |
| Step 4 CDI cyclisation (overnight) | 12 h overnight | 1 h setup | Day 3 pm |
| Step 4 workup | — | 1.5 h | Day 4 am |
| Step 5 N-alkylation (60 °C, 6 h) | 6 h daytime | 0.5 h setup | Day 4 am |
| Step 5 workup + column | — | 3 h | Day 4 pm |
| **Total** | | **~2.5 cd** | **4–5 working days** |

Steps 3 and 4 can be done back-to-back on Day 3 afternoon: Fe reduction takes 2 h, workup 1 h, CDI set-up 30 min, reaction overnight. Steps 4 and 5 can similarly be telescoped on Day 4.

Labour cost: 2.5 × €866 = **€2,165**

### 7977 total

| Pool | EUR |
| :--- | ---: |
| Materials + purification | 150 |
| Labour (2.5 cd) | 2,165 |
| **Total** | **2,315** |
| **Range** | **€1,900 – €3,125** |

Elapsed time from SM receipt: **4–5 working days.**
Elapsed from ordering: **2–5 weeks** (limited by 2-amino-4-bromo-5-Me-pyrimidine; verify stock before ordering other reagents).

---

## Programme summary

| Compound | Route | Steps | Overall yield | Mat + pur | Labour | **Total** | **Range** |
| :--- | :--- | :---: | :---: | ---: | ---: | ---: | ---: |
| MCUF651 | A | 2 | 45% | €60 | €1,082 | **€1,143** | €970–1,490 |
| A317 | A | 4 | 15.5% | €187 | €2,165 | **€2,352** | €1,930–3,175 |
| 7977 | B ★ | 5 | 17.4% | €150 | €2,165 | **€2,315** | €1,900–3,125 |
| **All three** | | | | **€397** | **€5,412** | **€5,810** | **€4,800–7,790** |

Total chemist-days: **6.25 cd** (just over one working week for one chemist, or ~3 days if two chemists work in parallel on different targets after the long-lead building blocks arrive).

Labour accounts for **93%** of total cost at this scale. Material cost is dominated by the precious-metal catalysts (Pd₂(dba)₃/BINAP for A317: €33; Pd(PPh₃)₄ for 7977: €8) and the chiral building blocks ((S)-2-acetylpyrrolidine: €29; 2-amino-4-bromo-5-Me-pyrimidine: €25).

---

## Elapsed-time schedule (single chemist, all three compounds sequential)

```
Week 0   Day 0:   Order all building blocks immediately.
                  Critical: (S)-2-acetylpyrrolidine (SIG, 2–3 wk)
                             2-amino-4-bromo-5-Me-pyrimidine (CB, 1–4 wk)
                  All others: in stock or 1–5 d.

Week 1   Days 1–3: MCUF651 synthesis (reagents arrive in 1–3 d).
                  Day 1 pm: step 1 amide coupling set up, overnight.
                  Day 2:    workup + column [A1]; step 2 N-alkylation, overnight.
                  Day 3 am: workup MCUF651. 100 mg isolated. ✓

         Days 3–7: 7977 synthesis can begin if CB pyrimidine arrives (optimistic 1 wk).
                  If CB building block delayed, 7977 waits until its arrival.

Week 2–3          (S)-2-Acetylpyrrolidine arrives.
         Days 1–4: A317 synthesis.
                  Day 1:    parallel acid + Buchwald set up overnight.
                  Day 2:    [A1] column; α-bromination; Hantzsch same day.
                  Day 3:    amide coupling overnight.
                  Day 4 am: workup A317. 100 mg isolated. ✓

Week 2–5          CB pyrimidine arrives (variable).
         Days 1–5: 7977 synthesis if not already run.
```

**Programme completion: 3–5 weeks from ordering**, dominated by building-block lead times.

---

## Three assumptions the estimate is most sensitive to

**1. Step yields, particularly the SNAr (7977, 60%) and Buchwald (A317, 65%)**
These are literature yields on analogous substrates and have not been measured on these exact substrates. A 10-percentage-point drop in a mid-route yield (e.g., SNAr to 50%) increases starting-material requirement by ~20% and forces a repeat run: effectively adding 0.5–1 chemist-day. The cumulative effect across a 5-step route is non-linear — a simultaneous 10% downgrade on all five 7977 steps shifts the overall yield from 17% to 9%, requiring the programme to start from ~200 mg SM input instead of 340 mg, and adds one full repeat cycle (~€2,000).

**2. Labour rate (€866/chemist-day) and troubleshooting time**
Labour is 93% of the total programme cost. The estimate assumes clean, first-pass success at every step. Any step requiring optimisation (substrate testing for Buchwald, regiochemistry confirmation for Hantzsch, catalyst screening for Suzuki) adds 0.5–2 chemist-days per step. A single failed Buchwald run adds €866 and re-orders the (S)-acetylpyrrolidine scale; two failed Buchwalds double the A317 cost. The range of €1,930–3,175 for A317 is almost entirely driven by this uncertainty.

**3. Building-block availability and lead time**
2-Amino-4-bromo-5-methylpyrimidine is listed as make-on-demand at Combi-Blocks (1–4 weeks stated; real lead for a freshly synthesised batch can reach 6 weeks). This is the hardest dependency to mitigate: 7977 cannot begin until this material is in hand, and there is no practical in-house substitute. The (S)-2-acetylpyrrolidine lead for A317 (2–3 weeks SIG) is lower risk; Sigma lists it as in-catalogue stock. **Order both on Day 0.** If the CB pyrimidine lead exceeds 4 weeks, source 2-bromo-5-methylpyrimidine (broader availability) and consider a Buchwald amination as an alternative first step; this adds 1 step and ~€700 but removes the single-supplier dependency.

---

## Price basis and caveats

All prices tagged **SIG** or **CB** were live catalogue prices at 1 g scale as stated in the retrosynthetic-analysis files for this session (Sigma-Aldrich and Combi-Blocks). They should be re-quoted before purchase; Pd-catalyst prices in particular fluctuate with the Pd spot price (currently ~€45/g Pd metal). Purification costs (silica + solvents + disposables per column) are tagged **EST** at €20–25/column; the dominant purification cost is the included chemist time, not materials. Pack-size minimums (e.g., 500 mg minimum for 2-amino-5,6-difluorobenzothiazole vs. 157 mg needed) mean the actual cash outlay on reagents may be 2–3× the proportional cost stated here, though unused material is retained for follow-up batches.
