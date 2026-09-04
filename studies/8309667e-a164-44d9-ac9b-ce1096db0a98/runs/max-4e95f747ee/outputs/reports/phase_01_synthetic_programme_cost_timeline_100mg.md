# Phase 1: Deliver synthetic programme — cost and timeline for 100 mg of MCUF651, A317, 7977

---
study_id: "8309667e-a164-44d9-ac9b-ce1096db0a98"
run_id: "max-e5095bffca"
phase_goal: "Deliver synthetic programme: cost and timeline for 100 mg of MCUF651, A317, 7977"
status: "complete"
---

## Objective

Deliver the number chemists will be judged against: what it costs and how long it takes to make 100 mg of each of MCUF651, A317, and 7977 using the best recommended route from this session's retrosynthetic analysis. The estimate must be built from the bottom up — mass balance tree, reagent quantities and prices, solvent volumes, purification cost per step, labour as chemist-days, and elapsed calendar time including building-block lead times.

## Methods

### Environment

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software

Python (`run_python`) was used to compute all mass balances and cost roll-ups. No external databases were queried; reagent prices were taken directly from the retrosynthetic-analysis source files already in this session (Sigma-Aldrich and Combi-Blocks catalogue prices at 1 g scale, tagged SIG or CB). Purification cost per column (€20–25 for silica + solvents + disposables, excluding labour) is tagged EST.

### Routes selected

| Compound | Route | Basis for selection |
| :--- | :--- | :--- |
| MCUF651 | A — amide coupling → N-alkylation (2 steps) | Shortest route, highest overall yield (45%), all SMs in stock |
| A317 | A — Buchwald → α-Br → Hantzsch → amide (4 steps) | N-arylation at step 1 renders pyrrolidine N tertiary throughout; no epimerisation risk at chiral centre. Route B (Pd-free) carries documented epimerisation risk at the final 130 °C SNAr step |
| 7977 | B ★ — SNAr → Suzuki → Fe-red → CDI → N-alkylation (5 steps) | Explicitly recommended in retrosynthetic analysis; Suzuki before reduction avoids Pd-mediated nitro reduction and gives higher cumulative yield (17.4% vs 14.6% for Route A) |

### Costing approach

1. **Mass balance** — back-calculated from 100 mg final product through each step yield. Practical input scale includes 20–25% excess to account for transfer and workup losses.
2. **Reagent costs** — mass used × price per gram, with source tag on each line.
3. **Purification** — €20–25 per column (materials only; labour already counted in chemist-days). Telescoped steps or aqueous-workup-only steps assigned lower allowance.
4. **Labour** — chemist active hours only (setup, workup, column loading, product characterisation). Overnight reaction time not charged. Rounded to nearest 0.25 cd. Rate: €866/cd.
5. **Elapsed calendar time** — step sequence mapped to calendar days; overnight reactions permit same-day set-up and next-morning workup.

### Note on purification cost formula

An intermediate `col()` function in the Python source contained a ×1000 arithmetic error that overstated silica cost by three orders of magnitude (computed €80/g instead of €80/kg). This was identified and corrected before finalising totals; the correct per-column material cost is €5–7 silica plus ~€15 solvents/disposables = €20–25 total.

## Results

### Mass balances

**MCUF651 Route A** (MW ~355, yields 72%/63%)

| Stage | mmol | Mass |
| :--- | ---: | ---: |
| SM input (each) | 0.776 | 100–157 mg |
| [A1] amide intermediate | 0.559 | 140 mg |
| MCUF651 final | 0.282 | 100 mg |

**A317 Route A** (MW ~395, yields 65%/70%/62%/55%)

| Stage | mmol | Mass |
| :--- | ---: | ---: |
| SM input | 1.958 | 222–325 mg |
| [A1] N-arylated ketone | 1.273 | 210 mg |
| [A2] α-bromoketone | 0.891 | 206 mg |
| [A3] 2-aminothiazole | 0.553 | 118 mg |
| Picolylpyrrole acid (parallel) | 0.388 | 98 mg |
| A317 final | 0.253 | 100 mg |

**7977 Route B** (MW ~388, yields 60%/75%/85%/70%/65%)

| Stage | mmol | Mass |
| :--- | ---: | ---: |
| SM input | 1.777 | 334–379 mg |
| [B1] SNAr product | 1.066 | 288 mg |
| [B2] Suzuki product | 0.800 | 260 mg |
| [B3] diamine | 0.680 | 204 mg |
| [B4] N-H bicycle | 0.476 | 154 mg |
| 7977 final | 0.258 | 100 mg |

### Cost summary

| Compound | Route | Steps | OY% | Mat + pur (EUR) | Labour (EUR) | Total (EUR) | Range (EUR) |
| :--- | :--- | :---: | :---: | ---: | ---: | ---: | ---: |
| MCUF651 | A | 2 | 45% | 60 | 1,082 | **1,143** | 970–1,490 |
| A317 | A | 4 | 15.5% | 187 | 2,165 | **2,352** | 1,930–3,175 |
| 7977 | B ★ | 5 | 17.4% | 150 | 2,165 | **2,315** | 1,900–3,125 |
| **All three** | | | | **397** | **5,412** | **5,810** | **4,800–7,790** |

Labour accounts for 93% of total cost. Total chemist-days: 6.25.

### Elapsed calendar time

| Compound | Synthesis days (from SM receipt) | Lead-time bottleneck | Programme start to finish |
| :--- | :---: | :--- | :--- |
| MCUF651 | 3 | 2-Amino-5,6-F₂-benzothiazole, 1–5 d (CB) | ~1 week |
| A317 | 4 | (S)-2-Acetylpyrrolidine, 2–3 wk (SIG) | 3–4 weeks |
| 7977 | 4–5 | 2-Amino-4-bromo-5-Me-pyrimidine, 1–4 wk (CB, MOD risk) | 2–5 weeks |

Parallel running of all three (two chemists, staggered by lead time): **5–6 weeks** from ordering to all 100 mg batches in hand.

### Three assumptions driving the spread

1. **Step yields** — literature values on analogous substrates. A 10-point drop on any single step in a 5-step route forces a repeat cycle.
2. **Labour rate / first-pass success** — €866/cd assumes clean execution. Any step requiring optimisation adds 0.5–2 cd per incident and dominates the upper bound of the range.
3. **Building-block availability** — 2-amino-4-bromo-5-methylpyrimidine is make-on-demand at Combi-Blocks; a 6-week lead time delays 7977 entirely. Mitigation: Buchwald amination from a more available precursor (+1 step, ~+€700).

### Output artifacts

| File | Description |
| :--- | :--- |
| `synthetic_programme_100mg_MCUF651_A317_7977.md` | Full programme document with per-reagent tables, schedules, sensitivity analysis |
| `016_col.py` | MCUF651 cost calculation source |
| `017_col.py` | A317 cost calculation source |
| `018_col.py` | 7977 cost calculation source |
| `019_corrected_totals_using_realistic_purification_cost.py` | Correction of purification arithmetic error |

## Limitations

- MW values are SMILES-derived estimates (±5%); a 5% MW error propagates to <3% cost error.
- Purification cost per column is an estimate (EST); actual cost depends on column type, solvent system, and whether cartridge or packed-bed silica is used.
- Prices are Sigma-Aldrich/Combi-Blocks catalogue at 1 g scale as stated in session source files; they should be re-quoted before purchase. Pd-catalyst prices fluctuate with the Pd spot price.
- Pack-size minimums mean actual cash outlay may be 2–3× the proportional cost stated; unused material is available for follow-up batches.
