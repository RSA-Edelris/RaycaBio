---
title: "Phase 1: Deliver synthetic programme: cost and timeline for 100 mg of MCUF651, A317, 7977"
study_id: "8309667e-a164-44d9-ac9b-ce1096db0a98"
run_id: "max-5ca579301a"
phase_index: 1
phase_id: "1"
phase_goal: "Deliver synthetic programme: cost and timeline for 100 mg of MCUF651, A317, 7977"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Deliver synthetic programme: cost and timeline for 100 mg of MCUF651, A317, 7977

## Summary

This phase set out to deliver synthetic programme: cost and timeline for 100 mg of MCUF651, A317, 7977. It completed 4 output files.

## Objective

Deliver synthetic programme: cost and timeline for 100 mg of MCUF651, A317, 7977

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

This phase used no external software or databases that the record identifies by name.

### Software

Python (`run_python`) was used for all mass-balance and cost calculations. Reagent prices were taken from Sigma-Aldrich (SIG) and Combi-Blocks (CB) catalogue values at 1 g scale, as recorded in the retrosynthetic-analysis source files already in this session. Purification cost (silica + solvents + disposables per column) is an estimate (EST) at €20–25/column. Labour rate: €866/chemist-day (8 h active).

### Routes selected

| Compound | Route | Rationale |
| :--- | :--- | :--- |
| MCUF651 | A — amide coupling → N-alkylation (2 steps, 45% OY) | Shortest route, highest yield, all SMs in stock within days |
| A317 | A — Buchwald → α-Br → Hantzsch → amide (4 steps, 15.5% OY) | N-arylation at step 1 locks pyrrolidine N as tertiary throughout; no epimerisation risk. Route B (Pd-free) has documented epimerisation risk at its final 130 °C SNAr step |
| 7977 | B ★ — SNAr → Suzuki → Fe-red → CDI → N-alkylation (5 steps, 17.4% OY) | Explicitly recommended; Suzuki before reduction avoids Pd-mediated nitro reduction and gives higher cumulative yield than Route A |

### Procedure

1. **Mass balance** — back-calculated from 100 mg final product through each step yield, with 20–25% practical excess at the starting-material stage. Source files 016–018 contain the full Python calculations.
2. **Cost roll-up** — mass used × price/g for each reagent; solvents priced per mL; purification at €20–25/column (materials only; labour counted in chemist-days). Source file 019 contains the purification-cost correction.
3. **Labour** — chemist active hours only (setup, workup, column, characterisation); overnight reaction time not charged. Rate €866/cd.
4. **Schedule** — step sequence mapped to calendar days; overnight reactions permit same-day setup and next-morning workup.

**Note on purification formula:** An intermediate `col()` function contained a ×1000 arithmetic error (silica priced at €80/g instead of €80/kg). This was identified and corrected in the same session before any cost was reported; file 019 records the corrected totals.

## Results

### Cost and timeline summary

**Two-run protocol (revised):** Each step is now planned as a small 0.1 mmol scouting run (confirm conditions) followed by the full preparative run at the scale in the mass balance tree. Assay-run labour = 0.35 cd/step; reagent cost proportional to 0.1 mmol scale. See `synthetic_programme_100mg_MCUF651_A317_7977.md` for full tables.

| Compound | Route | Steps | Assay runs | OY% | Mat + pur (€) | Labour (€) | Total (€) | Range (€) |
| :--- | :--- | :---: | :---: | :---: | ---: | ---: | ---: | ---: |
| MCUF651 | A | 2 | 2 | 45% | 65 | 1,689 | **1,754** | 1,400–2,370 |
| A317 | A | 4 | 5 | 15.5% | 195 | 3,680 | **3,875** | 3,100–5,230 |
| 7977 | B ★ | 5 | 5 | 17.4% | 155 | 3,680 | **3,835** | 3,070–5,180 |
| **All three** | | | **12** | | **415** | **9,049** | **9,464** | **7,570–12,780** |

Total chemist-days: **10.45 cd** (~2.1 working weeks). Labour = 95% of total cost. The €3,654 uplift from the single-run baseline is entirely labour (assay reagents add only €18 across all three compounds).

### Elapsed calendar time

| Compound | Synthesis days (two-run) | Lead-time bottleneck | Total from order |
| :--- | :---: | :--- | :--- |
| MCUF651 | 4 | 2-Amino-5,6-F₂-benzothiazole (CB, 1–5 d) | ~1 week |
| A317 | 5 | (S)-2-Acetylpyrrolidine (SIG, 2–3 wk) | 3–4 weeks |
| 7977 | 5–6 | 2-Amino-4-bromo-5-Me-pyrimidine (CB, 1–4 wk, MOD risk) | 2–5 weeks |

### Three assumptions driving the spread

1. **Step yields** (literature values on analogues, not measured on these substrates) — a 10-point drop forces a repeat cycle.
2. **Labour at €866/cd assumes first-pass success** — any optimisation step adds 0.5–2 cd per incident.
3. **Building-block availability** — CB pyrimidine for 7977 is make-on-demand; a 6-week lead delays the entire 7977 programme.

Full reagent-by-reagent tables, per-step schedules, and sensitivity analysis are in `synthetic_programme_100mg_MCUF651_A317_7977.md`.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| 016_col.py | PY | 3.8 KB | 01_deliver_synthetic_programme_cost_and_timeline_fo/source | 3b420161875f... |
| 017_col.py | PY | 4.2 KB | 01_deliver_synthetic_programme_cost_and_timeline_fo/source | a32bd021bd5b... |
| 018_col.py | PY | 4.5 KB | 01_deliver_synthetic_programme_cost_and_timeline_fo/source | 5eac14b72cd3... |
| 019_corrected_totals_using_realistic_purification_cost.py | PY | 1.7 KB | 01_deliver_synthetic_programme_cost_and_timeline_fo/source | a9cf9f82b373... |

## Verification

- No tool call is on record for this phase.
- 4 file(s) were produced and registered, 4 of them with a sha256 digest recorded, so they can be checked against this report.

## Limitations

- MW values are SMILES-derived estimates (±5%); propagates to <3% cost error.
- Step yields are literature values on analogous substrates, not measured on these exact molecules.
- Purification cost per column is EST; actual cost depends on column type and solvent system.
- Prices are catalogue values at 1 g scale; re-quote before purchase. Pd-catalyst prices fluctuate with Pd spot price.
- Pack-size minimums mean actual cash outlay may be 2–3× the proportional cost stated.

## References

This phase recorded no external tools or databases.
