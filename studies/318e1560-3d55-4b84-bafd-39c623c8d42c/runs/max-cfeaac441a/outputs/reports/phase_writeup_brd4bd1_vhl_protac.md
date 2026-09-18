
## Phase objective

Model a VHL-recruiting PROTAC ternary complex against BRD4 bromodomain 1 (BD1) and rank
four linker lengths by predicted cooperativity (α), not by binary warhead affinity.
Inputs: PDB 3MXF (BRD4 BD1 + JQ1, 1.60 Å) and PDB 5T35 (MZ1 ternary: BRD4 BD2 +
VHL:ElonginCB, 2.70 Å).

---

## What was done, step by step

### 1. Structure identification
Both PDB files were downloaded and parsed. 5T35 was confirmed as the MZ1 ternary
co-crystal (Gadd et al. 2017 ACS Chem Biol), containing BRD4 **BD2** (chains A/E,
res 349–459), VHL (chains D/H, res 61–209), ElonginB (chains B/F), ElonginC (chains C/G),
and the bifunctional PROTAC MZ1 (CCD code 759, in chains D/H). 3MXF contains BD1
(chain A, res 42–168) with JQ1 bound.

### 2. Sequence-guided superposition of BD1 onto BD2
A pairwise Needleman–Wunsch alignment (match +2, mismatch −1, gap −2) of the SEQRES
sequences yielded 42% identity over 108 matched positions. CA coordinates for aligned,
gap-free residue pairs (127 BD1 positions vs 130 BD2 SEQRES, 111 modelled BD2 CA) were
extracted and iteratively trimmed at 2σ. Kabsch superposition on the 73-residue core
gave **0.53 Å RMSD**, confirming that BD1 and BD2 share the same four-helix bromodomain
fold and that BD1 can be placed reliably into the MZ1 ternary geometry.

### 3. Exit-vector extraction
For each warhead, the linker-attachment atom was estimated geometrically:
- **JQ1 (BD1):** the heavy atom farthest from the BD1 Cα centroid, transformed into the
  ternary frame via the Kabsch rotation/translation (Rf, tf).
- **VHL warhead (MZ1):** the VHL-side MZ1 atom with the greatest minimum distance to
  VHL Cα coordinates (i.e. most exposed toward the linker).

BD2-crystal reference exit-to-exit distance: **5.0 Å** (MZ1 in 5T35).
BD1-model exit-to-exit distance: **5.6 Å** (BD1 superposed, slightly larger due to
pocket orientation difference between BD1 and BD2).

### 4. Interface contact count
Cα–Cα contacts < 8 Å between BD1 (superposed) and VHL gave 80 contact pairs,
identical to the BD2-crystal count—confirming that the Kabsch superposition preserves
the ternary interface geometry.

### 5. Linker cooperativity model
Four linker lengths were scored using the normalised Gaussian-chain probability density:

**P_vec(r=d, n) = (1 / 2πσ²)^(3/2) × exp(−d² / 2σ²)**  where  **σ² = nb² / 3**

with b = 1.5 Å/bond and required bridging distance d = 5.6 Å. A predicted cooperativity
was computed as:

**α_pred = α_MZ1 × [P_vec(d_BD1, n) / P_vec(d_BD2, 12)] × [pose_fraction / pose_fraction_ref]**

calibrated to MZ1 (n=12, d_BD2=5.0 Å, α_BD2=31). Pose fractions came from 5,000
Monte Carlo perturbations (±15° rotation, ±1.5 Å translation) of BD1 in the ternary
frame, accepting only poses where the linker could physically reach (d ≤ n × 1.5 Å).

---

## Results

| Rank | Linker | n (heavy atoms) | Strain ratio | Pose fraction | α_pred |
|------|--------|-----------------|-------------|---------------|--------|
| 1 | L3-long | 12 | 0.31 | 0.996 | 21.9 |
| 2 | L4-xlong | 18 | 0.21 | 0.996 | 21.2 |
| 3 | L2-medium | 8 | 0.47 | 0.992 | 16.9 |
| 4 | L1-short | 4 | 0.93 | 0.419 | 1.5 |

Optimal Gaussian-chain length: n\* = 13.8 heavy atoms. L3 and L4 are statistically
indistinguishable (3% margin). L1 is robustly last: strain ratio 0.93 means near-total
chain extension, and 58% of sampled ternary orientations are geometrically excluded.

![Linker ranking figure](brd4bd1_vhl_linker_ranking.png)

---

## Limitations declared before interpretation

1. BD1 and BD2 have different surface residues at the VHL contact face; actual BSA is
   unmeasured for BD1.
2. The Gaussian chain ignores PEG Kuhn length (~3.8 Å), linker rigidity, and directional
   exit constraints — absolute α values are calibrated estimates, not predictions.
3. Exit-vector assignment was geometric, not chemically assigned from the warhead SMILES.
4. No steric clash screen was run on the BD1–VHL interface.
5. L3 vs L4 Δα = 0.7 (3%) is within model noise; they are co-first.

---

## Falsification criteria (ordered by discriminating power)

1. ITC/SPR: α(L1) ≥ α(L2) → fundamental model failure.
2. ITC/SPR: α(L4) > α(L3) by > 10% → n\* underestimated; bridging distance > 5.6 Å.
3. BD1–VHL co-crystal: d ≠ 5.6 ± 1 Å → recalculate n\*, re-rank.
4. No ternary complex forms at any linker → BD1–VHL PPI non-productive.
5. Rigid L3 analogue outperforms flexible L3 → Kuhn-length correction needed.

Most falsifiable single claim: **L1 ranks last** (geometrically robust, model-independent).
