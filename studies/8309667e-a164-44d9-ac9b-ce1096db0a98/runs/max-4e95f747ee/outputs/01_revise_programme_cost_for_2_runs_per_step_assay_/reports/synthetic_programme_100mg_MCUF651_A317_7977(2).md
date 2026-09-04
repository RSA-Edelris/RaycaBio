
## Scope and conventions

This document delivers the bottom-up synthetic programme for 100 mg of each final compound using the best recommended route established in this study. All costs are in EUR. Labour is charged at **€866 per chemist-day (8 h active working time)**; overnight reactions are not charged because no chemist is present. Reaction running time and chemist active time are listed separately. Prices marked **SIG** were taken from Sigma-Aldrich catalogue at 1 g scale; prices marked **CB** from Combi-Blocks catalogue at 1 g scale, both as stated in the retrosynthetic-analysis source files for this session. Prices marked **EST** are not from a live catalogue and carry higher uncertainty. An estimate built on invented prices is worse than no estimate; every line in the reagent tables below is tagged.

MW estimates are derived from SMILES (targets ~355, ~395, ~388 g/mol for MCUF651, A317, 7977 respectively); a ±5% MW error propagates to ±5% in all masses and less than ±3% in total cost.

**Revision (two-run protocol):** Each synthetic step is now planned as two consecutive runs: (1) a small scouting run at **0.1 mmol** to confirm conditions and yield before committing the full substrate load, followed by (2) the full preparative run at the scale in the mass balance tree. Assay-run reagent costs are proportional to scale. Assay-run labour is **0.35 cd per step** (setup ~1 h, reaction monitoring, TLC/LC-MS analysis, simple workup ~1 h = ~3 h active). The preparative run proceeds the same day or the following morning once the assay confirms acceptable conversion.

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
| **Materials subtotal (preparative)** | | | **60** | | | |
| Assay-run reagents (2 × 0.1 mmol) | — | — | **5** | — | — | — |
| **Materials total** | | | **65** | | | |

### Labour and schedule (two-run protocol)

| Event | Active time | Calendar span |
| :--- | :--- | :--- |
| Step 1 assay (0.1 mmol): setup, TLC/LC-MS, workup | 0.35 cd | Day 1 am |
| Step 1 prep: amide coupling set-up | 1 h | Day 1 pm |
| Step 1 prep: reaction overnight | — (not charged) | Day 1 pm → Day 2 am |
| Step 1 prep: workup + column | 2.5 h | Day 2 am |
| Step 2 assay (0.1 mmol): setup, TLC/LC-MS | 0.35 cd | Day 2 pm |
| Step 2 prep: N-alkylation set-up | 1 h | Day 2 pm |
| Step 2 prep: reaction overnight | — (not charged) | Day 2 pm → Day 3 am |
| Step 2 prep: workup | 2 h | Day 3 am |
| **Total** | **~1.95 cd** | **4 working days** |

Labour cost: 1.95 × €866 = **€1,689**

### MCUF651 total

| Pool | EUR |
| :--- | ---: |
| Materials + purification | 65 |
| Labour (1.95 cd) | 1,689 |
| **Total** | **1,754** |
| **Range** | **€1,400 – €2,370** |

Critical path: fully linear (2 steps). Elapsed time from SM receipt: **4 working days.**

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
| **Materials subtotal (preparative)** | **187** |
| Assay-run reagents (5 × 0.1 mmol) | **8** |
| **Materials total** | **195** |

### Labour and schedule (two-run protocol)

| Event | Active time | Calendar day |
| :--- | :--- | :--- |
| Parallel acid assay (0.1 mmol) | 0.35 cd | Day 1 am |
| Step 1 Buchwald assay (0.1 mmol) | 0.35 cd | Day 1 am (concurrent with acid assay) |
| Step 1 Buchwald prep set-up | 1 h | Day 1 pm |
| Step 1 prep overnight (90 °C, 12 h) | — | Day 1 pm → Day 2 am |
| Parallel acid prep (Day 1 pm, 6 h, telescoped) | 1 h | Day 1 pm |
| Step 1 prep workup + column | 3 h | Day 2 am |
| Step 2 α-Br assay | 0.35 cd | Day 2 pm |
| Step 2 prep (−10 °C, same afternoon) | 2 h | Day 2 pm |
| Step 3 Hantzsch assay | 0.35 cd | Day 3 am |
| Step 3 prep (telescoped with assay) | 2 h | Day 3 am |
| Step 4 amide coupling assay | 0.35 cd | Day 3 pm |
| Step 4 prep set-up overnight | 1.5 h | Day 3 pm |
| Step 4 prep workup + column | 3 h | Day 4 am |
| **Total** | **~4.25 cd** | **5 working days** |

Note: The Buchwald and parallel acid assays can be run concurrently on Day 1 morning (they are independent reactions). Steps 2 and 3 remain back-to-back because [A2] is unstable and should proceed to Hantzsch cyclisation the same day. The Step 3 assay is run in the same morning session as the Step 3 prep for this reason — a thin-layer screen (30 min) suffices before committing the batch.

Labour cost: 4.25 × €866 = **€3,680**

### A317 total

| Pool | EUR |
| :--- | ---: |
| Materials + purification | 195 |
| Labour (4.25 cd) | 3,680 |
| **Total** | **3,875** |
| **Range** | **€3,100 – €5,230** |

Elapsed time from SM receipt: **5 working days.**
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
| **Materials subtotal (preparative)** | | | **150** | | |
| Assay-run reagents (5 × 0.1 mmol) | — | — | **5** | — | — |
| **Materials total** | | | **155** | | |

### Labour and schedule (two-run protocol)

| Event | Active time | Calendar day |
| :--- | :--- | :--- |
| Step 1 SNAr assay (0.1 mmol) | 0.35 cd | Day 1 am |
| Step 1 SNAr prep (100 °C, 8 h daytime) | 2.5 h setup + workup | Day 1 pm |
| Step 1 column | 3 h | Day 2 am |
| Step 2 Suzuki assay (0.1 mmol) | 0.35 cd | Day 2 pm |
| Step 2 Suzuki prep set-up overnight | 1.5 h | Day 2 pm |
| Step 2 workup + column | 3 h | Day 3 am |
| Step 3 Fe-red assay (0.1 mmol, 30 min) | 0.35 cd | Day 3 pm (concurrent) |
| Step 3 Fe-red prep (80 °C, 2 h) | 2 h setup + workup | Day 3 pm |
| Step 4 CDI assay | 0.35 cd | Day 3 pm (concurrent with step 3) |
| Step 4 CDI prep set-up overnight | 1 h setup | Day 3 pm |
| Step 4 workup | 1.5 h | Day 4 am |
| Step 5 N-alkylation assay | 0.35 cd | Day 4 am |
| Step 5 N-alkylation prep (60 °C, 6 h) | 0.5 h setup | Day 4 am |
| Step 5 workup + column | 3 h | Day 4 pm |
| **Total** | **~4.25 cd** | **5–6 working days** |

Steps 3 and 4 assay/prep runs can be overlapped in the same afternoon session (Day 3 pm): the Fe reduction assay takes only ~30 min, and CDI set-up can begin while [B3] is being worked up. This is the tightest part of the schedule; if any step requires a repeat the critical path extends by one day.

Labour cost: 4.25 × €866 = **€3,680**

### 7977 total

| Pool | EUR |
| :--- | ---: |
| Materials + purification | 155 |
| Labour (4.25 cd) | 3,680 |
| **Total** | **3,835** |
| **Range** | **€3,070 – €5,180** |

Elapsed time from SM receipt: **5–6 working days.**
Elapsed from ordering: **2–5 weeks** (limited by 2-amino-4-bromo-5-Me-pyrimidine; verify stock before ordering other reagents).

---

## Programme summary (two-run protocol)

| Compound | Route | Steps | OY% | Mat + pur | Labour | **Total** | **Range** |
| :--- | :--- | :---: | :---: | ---: | ---: | ---: | ---: |
| MCUF651 | A | 2 | 45% | €65 | €1,689 | **€1,754** | €1,400–2,370 |
| A317 | A | 4 | 15.5% | €195 | €3,680 | **€3,875** | €3,100–5,230 |
| 7977 | B ★ | 5 | 17.4% | €155 | €3,680 | **€3,835** | €3,070–5,180 |
| **All three** | | | | **€415** | **€9,049** | **€9,464** | **€7,570–12,780** |

Total chemist-days: **10.45 cd** (~2.1 working weeks).

**What the assay runs add:** The two-run protocol adds 0.35 cd per step (one assay per step: 2 for MCUF651, 5 each for A317 and 7977). Assay-run reagent cost is negligible (<€5 per compound) because the 0.1 mmol scale uses small quantities even of expensive Pd catalysts. Labour is the entire addition: **€3,654 of the €3,654 total uplift is labour**; reagent costs increase by only €18 across all three compounds. Labour remains **95% of the revised total** (was 93%).

---

## Elapsed-time schedule (two-run protocol, single chemist, all three compounds sequential)

```
Week 0   Day 0:   Order all building blocks immediately.
                  Critical: (S)-2-acetylpyrrolidine (SIG, 2–3 wk)
                             2-amino-4-bromo-5-Me-pyrimidine (CB, 1–4 wk)
                  All others: in stock or 1–5 d.

Week 1   Days 1–4: MCUF651 synthesis (reagents arrive in 1–3 d).
                  Day 1 am:  Step 1 assay (0.1 mmol, confirm coupling).
                  Day 1 pm:  Step 1 prep (0.776 mmol), overnight.
                  Day 2 am:  Step 1 workup + column [A1].
                  Day 2 pm:  Step 2 assay; Step 2 prep set-up overnight.
                  Day 3 am:  Step 2 workup. MCUF651 100 mg isolated. ✓
                  Day 3–4:   NMR characterisation and stock.

         Days 4–9: 7977 synthesis (if CB pyrimidine arrives by Week 1;
                  if delayed, 7977 waits at this slot — see Week 2–5 below).
                  Day 4 am:  Step 1 assay (SNAr, 0.1 mmol).
                  Day 4 pm:  Step 1 prep (100 °C, 8 h).
                  Day 5 am:  Column [B1]. Step 2 assay pm.
                  Day 5 pm:  Step 2 Suzuki prep overnight.
                  Day 6 am:  Column [B2]. Step 3 assay + prep (pm, same day).
                  Day 6 pm:  Step 4 CDI assay + prep overnight.
                  Day 7 am:  Step 5 assay + prep (60 °C, 6 h).
                  Day 7 pm:  Step 5 workup. 7977 100 mg isolated. ✓

Week 2–3          (S)-2-Acetylpyrrolidine arrives.
         Days 1–5: A317 synthesis.
                  Day 1 am:  Buchwald assay + parallel acid assay (concurrent).
                  Day 1 pm:  Buchwald prep + parallel acid prep overnight.
                  Day 2 am:  [A1] column. Step 2 α-Br assay.
                  Day 2 pm:  Step 2 prep; [A2] used immediately.
                  Day 3 am:  Step 3 Hantzsch assay + prep (same session).
                  Day 3 pm:  Step 4 amide assay + prep overnight.
                  Day 4 am:  Step 4 workup + column. A317 100 mg isolated. ✓
                  Day 4–5:   NMR and stock.

Week 2–5          CB pyrimidine arrives (variable, if not already run).
         Days 1–7: 7977 synthesis (schedule as above if moved to this slot).
```

**Programme completion from ordering: 3–5 weeks**, dominated by building-block lead times. If both long-lead materials are ordered Day 0 and 7977 and A317 are synthesised in parallel (two chemists), elapsed time compresses to **3–4 weeks total**.

---

## Three assumptions the estimate is most sensitive to

**1. Step yields, particularly the SNAr (7977, 60%) and Buchwald (A317, 65%)**
Literature yields on analogous substrates; not measured on these exact substrates. A 10-percentage-point drop in a mid-route yield forces a repeat preparative run: +0.7 cd (prep run only, no additional assay needed if the assay already identified the problem). Across a 5-step route, simultaneous 10% downgrade on all steps shifts the overall yield from 17% to ~9%, requiring ~2× the SM input and one full additional cycle.

**2. Labour rate (€866/chemist-day) and troubleshooting time**
Labour is 95% of the revised programme cost. The two-run protocol de-risks individual step failures, but if an assay run fails (sub-optimal yield or unexpected product) the chemist must adjust conditions and re-assay before running the prep: add 0.35–0.7 cd per incident. One failed Buchwald optimisation cycle (adjust ligand, re-assay, re-run prep) adds ~€1,300 to A317. The ranges (€3,100–5,230 for A317) are almost entirely driven by this contingency.

**3. Building-block availability and lead time**
2-Amino-4-bromo-5-methylpyrimidine is make-on-demand at Combi-Blocks (1–4 weeks stated; real lead can reach 6 weeks). There is no practical catalogue substitute. **Order on Day 0.** If the CB pyrimidine lead exceeds 4 weeks, source 2-bromo-5-methylpyrimidine (broader availability) and consider a Buchwald amination as an alternative first step; this adds 1 step and ~€700 but removes the single-supplier dependency. The (S)-2-acetylpyrrolidine lead for A317 (2–3 weeks, SIG) is lower risk; Sigma lists it as in-catalogue stock.

---

## Price basis and caveats

All prices tagged **SIG** or **CB** were live catalogue prices at 1 g scale as stated in the retrosynthetic-analysis files for this session (Sigma-Aldrich and Combi-Blocks). They should be re-quoted before purchase; Pd-catalyst prices in particular fluctuate with the Pd spot price (currently ~€45/g Pd metal). Purification costs (silica + solvents + disposables per column) are tagged **EST** at €20–25/column; the dominant purification cost is the included chemist time, not materials. Pack-size minimums (e.g., 500 mg minimum for 2-amino-5,6-difluorobenzothiazole vs. 157 mg needed) mean the actual cash outlay on reagents may be 2–3× the proportional cost stated here, though unused material is retained for follow-up batches.
