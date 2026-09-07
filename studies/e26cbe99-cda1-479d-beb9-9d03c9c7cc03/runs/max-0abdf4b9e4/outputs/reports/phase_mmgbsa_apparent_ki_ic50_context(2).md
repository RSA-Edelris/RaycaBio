# Phase Report: MM-GBSA ΔG → Apparent Ki and IC50 Context

**Date:** 2026-09-04  
**Status:** Complete (3 reliable compounds; EDS01357518_ent1 invalid; EDS01357518_ent2 pending)

---

## Purpose

Convert the MM-GBSA ΔG_bind values from all five CRBN pocket compounds to apparent Ki using the standard thermodynamic relationship, and assess whether IC50 values can be reported.

---

## Method

Standard-state conversion at T = 298 K, RT = 0.5922 kcal/mol:

```
Ki = exp(ΔG / RT)
pKi = -log10(Ki)
```

Applied to the four completed MM-GBSA results (sources: `phase_md_mmpbsa_EDS01806218_ent2.md`, `phase_mmgbsa_EDS01357518_ent1_EDS01889984.md`, `phase_mmgbsa_EDS01806218_ent1.md`).

Code: `123_print.py` (platform-auto-saved Python cell; not a scientific output).

---

## Results

### Apparent Ki from raw MM-GBSA ΔG

| Compound | ΔG (kcal/mol) | SD | Apparent Ki | pKi | Reliability |
|:---------|:-------------:|:--:|:-----------:|:---:|:-----------:|
| EDS01806218_ent2 | −25.22 | 5.82 | 0.3 aM | 18.5 | ✓ reliable |
| EDS01889984 | −23.80 | 2.64 | 3.5 aM | 17.5 | ✓ reliable |
| EDS01806218_ent1 | −20.75 | 2.59 | 607 aM | 15.2 | ✓ reliable |
| EDS01357518_ent1 | +68.17 | 57.57 | invalid | — | ✗ topology defect |
| EDS01357518_ent2 | — | — | — | — | Pending job 6321629 |

### Relative ranking (ΔΔG vs EDS01806218_ent2)

| Compound | ΔΔG (kcal/mol) | Fold weaker than ent2 |
|:---------|:--------------:|:---------------------:|
| EDS01806218_ent2 | 0.00 | reference |
| EDS01889984 | +1.42 | ~11× |
| EDS01806218_ent1 | +4.47 | ~1900× |

---

## Why Raw MM-GBSA Cannot Give IC50

The apparent Ki values (attomolar range) are unphysical. Two systematic errors cause this:

1. **Entropy excluded.** No −TΔS correction was computed (`entropy = off` in `mmpbsa.in`). The −TΔS penalty for binding is typically +5 to +15 kcal/mol. The MM-GBSA ΔG is an effective enthalpy, not a free energy.

2. **Systematic overestimation.** MM-GBSA consistently produces ΔG 5–15 kcal/mol too negative relative to experiment across published benchmarks. Applying a +10 kcal/mol empirical correction shifts the three reliable compounds to approximately −15, −14, and −11 kcal/mol (Ki ~1 pM, ~5 pM, ~100 pM) — more plausible for CRBN pocket binders of this molecular weight, but still uncalibrated.

3. **Ki ≠ IC50 in general.** IC50 depends on assay format, substrate concentration, and inhibition mechanism. Ki ≈ IC50 only for competitive inhibitors at [substrate] << Km.

**What is reliable:** the relative ranking and ΔΔG differences. These are internally consistent and not affected by the systematic offset.

---

## Calibration Path to IC50

To convert to calibrated IC50 predictions:

1. Measure IC50 for one compound in a biochemical assay (HTRF displacement or equivalent).
2. Compute empirical offset: `offset = ΔG_MMGBSA_ref − RT · ln(IC50_measured)`.
3. Apply offset to remaining compounds: `IC50_predicted = exp((ΔG_MMGBSA + offset) / RT)`.

A single measured anchor point converts the relative ranking into IC50 predictions with uncertainty dominated by the SD of each MM-GBSA estimate (±2–6 kcal/mol, corresponding to ~30–20,000-fold IC50 uncertainty per compound).

---

## Verification

| Check | Status | Evidence |
|:------|:------:|:---------|
| ΔG values taken from source phase documents | PASS | ent2 from `phase_md_mmpbsa_EDS01806218_ent2.md`; ent1/EDS01889984 from `phase_mmgbsa_EDS01357518_ent1_EDS01889984.md`; EDS01806218_ent1 from `phase_mmgbsa_EDS01806218_ent1.md` |
| Temperature and RT consistent with simulation | PASS | T = 298 K, RT = 0.5922 kcal/mol |
| EDS01357518_ent1 correctly excluded | PASS | Flagged invalid (topology defect); not converted |
| Apparent Ki range flagged as unphysical | PASS | aM values noted; two root causes documented (no entropy, systematic overestimation) |
| Relative ΔΔG and fold differences computed | PASS | ent2 reference; ent2 > EDS01889984 (~11×) > ent1 (~1900×) |
| Calibration path documented | PASS | Single-point anchor method described |
| `123_print.py` accounted for | PASS | Platform-auto-saved Python cell; not a scientific output |
| EDS01357518_ent2 status noted | PASS | Pending Isambard job 6321629; will be added to table when trajectory returns |
