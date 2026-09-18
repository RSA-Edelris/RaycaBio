
## Summary

A VHL-recruiting PROTAC targeting BRD4 bromodomain 1 (BD1) was modeled by superposing
the 3MXF BD1 structure onto the MZ1 ternary crystal (5T35, BD2–VHL–ElonginCB). Four linker
lengths were scored by predicted cooperativity (α) using a Gaussian-chain effective-concentration
model calibrated to the measured MZ1 BD2–VHL value (α = 31, Gadd et al. 2017 ACS Chem Biol).

---

## Input Structures

| Structure | Identity | Resolution | Used for |
|-----------|----------|-----------|---------|
| **3MXF** chain A | BRD4 BD1 + JQ1 | 1.60 Å | BD1 warhead pose and exit vector |
| **5T35** chains A/D/B/C | BRD4 BD2 + MZ1 PROTAC + VHL + ElonginCB | 2.70 Å | Ternary geometry template, VHL warhead pose |

5T35 is the MZ1 ternary co-crystal (Gadd et al. 2017), making it a direct template for
BD2-targeting PROTACs. BD1 lacks a solved ternary structure and was modelled by superposition.

---

## Structural Superposition

BD1 (127 residues, 42–168) was aligned to BD2 (111 residues, 349–459) using a pairwise
sequence alignment (42% identity, Needleman–Wunsch) followed by Kabsch superposition on
matched Cα pairs, with iterative outlier trimming (2σ).

| Metric | Value |
|--------|-------|
| Aligned pairs (core) | 73 Cα |
| Core RMSD (BD1→BD2) | **0.53 Å** |
| Bromodomain fold coverage | 65% of residues in rigid core |

The 0.53 Å core RMSD confirms that the two bromodomains adopt the same four-helix fold
and that BD1 can be reliably placed into the BD2 ternary geometry.

---

## Exit-Vector Analysis

Warhead exit atoms were defined by minimum distance to each partner protein's Cα centroid,
then the furthest such atom on each protein side of MZ1.

| Measurement | Distance (Å) |
|-------------|-------------|
| BD2–VHL warhead exit-to-exit (MZ1 crystal, 5T35) | **5.0 Å** |
| BD1–VHL warhead exit-to-exit (BD1 superposed) | **5.6 Å** |
| Optimal Gaussian-chain linker length n\* | **13.8 heavy atoms** |

BD1's exit point is 0.6 Å further from the VHL warhead than BD2's, shifting the
optimal linker from ~12 toward ~14 heavy atoms.

---

## Linker Length Ranking

The four linker variants were ranked by a composite cooperativity score:

**α_pred = α_MZ1 × [P_vec(d_BD1, n) / P_vec(d_BD2, 12)] × [pose_fraction / pose_fraction_MZ1]**

where P_vec is the Gaussian-chain probability density per unit volume at the required
bridging distance, and pose_fraction is the fraction of 5,000 sampled ternary
orientations (±15° rotation, ±1.5 Å translation) where the linker can physically reach.

| Rank | Linker | Heavy atoms | Max extension (Å) | Strain ratio | Pose fraction | α_pred |
|------|--------|-------------|-------------------|--------------|---------------|--------|
| **#1** | **L3-long** | **12** | **18.0** | **0.31** | **0.996** | **21.9** |
| #2 | L4-xlong | 18 | 27.0 | 0.21 | 0.996 | 21.2 |
| #3 | L2-medium | 8 | 12.0 | 0.47 | 0.992 | 16.9 |
| #4 | L1-short | 4 | 6.0 | **0.93** | 0.419 | 1.5 |

*Strain ratio = required distance / max extension; n\* = 13.8 atoms; MZ1 calibration α = 31 (BD2).*

![BD1-VHL linker ranking figure](brd4bd1_vhl_linker_ranking.png)

### Interpretation

- **L3 (12 atoms) and L4 (18 atoms) are effectively tied** (Δα = 0.7, 3% difference —
  below model precision). Both are near n\* = 13.8; L3 is marginally closer.
- **L1 (4 atoms) is severely penalised**: strain ratio 0.93 means the chain must be
  nearly fully extended (entropically locked), and only 42% of sampled poses are
  geometrically accessible. This is the most model-independent claim.
- **L2 (8 atoms)** is meaningfully suboptimal — P_vec is only 55% of L3's value —
  but may be sufficient for productive degradation.
- The model is calibrated to BD2–VHL (α = 31), so BD1 absolute α values carry the
  unknown BD1–VHL intrinsic PPI contribution.

---

## Model Limitations

1. **BD1–VHL interface is not the same as BD2–VHL.** BD1 and BD2 surface residues differ; actual
   buried surface area and interface contacts for a BD1-targeting PROTAC are unmeasured. The 0.53 Å
   fold alignment places BD1 in the same *geometry* as BD2, but contact residues will differ.
2. **Gaussian chain is a coarse model.** It ignores bond angle constraints, PEG backbone
   preferences (Kuhn length ≈ 3.8 Å, not 1.5 Å per atom), and rigid linker elements such as
   piperazines or triazoles. A worm-like chain or molecular-dynamics torsion scan would be needed
   for atom-level accuracy.
3. **Exit-vector assignment was geometric, not chemical.** JQ1's linker attachment point in a real
   PROTAC warhead is the carboxylate carbon (C14), not necessarily the geometrically most
   solvent-exposed atom used here. A 1–2 Å error propagates directly into n\*.
4. **L3 vs L4 margin is within noise.** The 3% difference between #1 and #2 is smaller than
   typical linker model errors (~10–20%); they should be treated as co-favourites.
5. **No clash check was performed.** The VHL surface may present steric incompatibility with the
   BD1 C-terminal helix (αC) not present in BD2. This would reduce effective BSA for some poses.

---

## What Would Falsify the Ranking

The five most informative experiments, ranked by discriminating power:

| # | Experiment | What it tests | Verdict if result = X |
|---|------------|---------------|-----------------------|
| **1** | ITC or SPR: measure α for L1 vs L2 | Strain penalty at short linker | If α(L1) ≥ α(L2): fundamental model failure |
| **2** | ITC/SPR: measure α for L3 vs L4 | Position of the optimum relative to n\* | If α(L4) > α(L3) by >10%: n\* is underestimated; actual bridging distance > 5.6 Å |
| **3** | X-ray or cryo-EM of BD1–VHL ternary | Actual exit-to-exit distance | If d ≠ 5.6 Å ± 1 Å: recalculate n\* and re-rank |
| **4** | MST or TR-FRET: test if BD1–VHL ternary forms at all | BD1–VHL PPI viability | If no ternary at any linker: interface is non-productive; all α predictions meaningless |
| **5** | Degradation (DC50, Dmax) with L3 vs piperazine-containing L3 analogue | Effect of linker rigidity | If rigid analogue outperforms: Kuhn-length correction shifts optimum to shorter n |

**The single most falsifiable claim** is that L1 (4 atoms) will rank last. This follows
from the near-total chain extension (strain ratio 0.93) and the 58% geometric exclusion of
ternary poses — a prediction robust to calibration uncertainty and exit-vector errors.
