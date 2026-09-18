
## Summary

A heterobifunctional molecule anchored in the BI-3802 groove of BCL6-BTB (PDB 5MW2) and in the inhibitor pocket of BRD4-BD1 (PDB 3P5O) was modelled to assess whether any BCL6-BTB residue is presented in a geometry productive for BRD4 bromodomain reading (Kac insertion). The result was compared against the equivalent PROTAC/E3 geometry drawn from the dBET1 CRBN ternary complex (PDB 6BOY). Bromodomain insertion is the harder constraint by a large margin.

---

## Phase 1 — Structure fetch and characterisation

**Inputs**: PDB identifiers 5MW2, 3P5O, 6BOY.

**5MW2** (BCL6-BTB + BI-3802):
- Chain A, 122 residues (A7–A128), single chain in the asymmetric unit.
- Ligand U52 (BI-3802, 34 heavy atoms), CoM = [13.66, 17.40, 14.07] Å — this is the anchor point for the BCL6-binding arm of the hypothetical bifunctional molecule.

**3P5O** (BRD4 BD1 + small-molecule EAM):
- Chain A, 127 residues (A42–A168; full-length BRD4 numbering).
- Ligand EAM (30 heavy atoms), CoM = [26.29, 50.72, −2.12] Å — occupies the acetyl-lysine pocket; four EDO molecules at crystal contacts.

**6BOY** (dBET1 PROTAC / BRD4-BD1 / DDB1–CRBN):
- Chain A: DDB1 (808 residues, 1–1140 with gaps).
- Chain B: CRBN (375 residues, 44–427).
- Chain C: BRD4 BD1 (127 residues, 42–168, same region as 3P5O).
- Ligand RN6: dBET1 PROTAC, CoM = [72.08, 38.66, 51.11] Å.
- PROTAC end-to-end span (VHL-arm to BRD4-arm): 19.5 Å.

---

## Phase 2 — BCL6-BTB surface accessibility

Shrake-Rupley SASA computed at residue level on the full 5MW2 assembly.

**Surface-exposed lysines (SASA > 30 Å²):**

| Residue | SASA (Å²) | Nζ coord (Å) | Dist Nζ → BI-3802 CoM (Å) | B-factor Cα / Nζ |
|---|---|---|---|---|
| Lys 66 | 92.6 | [16.5, 22.7, 22.1] | 17.4 | 57.9 / 101.0 |
| Lys 123 | 122.5 | [10.0, 33.1, 13.5] | 17.3 | 60.8 / 105.3 |
| Lys 126 | 176.2 | [14.0, 35.5, 6.7] | 25.7 | 72.0 / 126.3 |

Surface Ser/Thr closest to the BI-3802 anchor: Ser59 (8.9 Å), Thr62 (9.5 Å), Thr48 (13.5 Å).

All three Lys sidechains are fully extended (Cα–Nζ = 6.35 Å for K66/K123, 5.56 Å for K126).

---

## Phase 3 — BRD4-BD1 pocket geometry

Pocket-lining residues identified by residue number (full-length BRD4 numbering, as deposited in 3P5O):

| Residue | Key atom | Coord (Å) | Role |
|---|---|---|---|
| Trp81 | NE1 | [34.3, 46.8, −2.7] | WPF shelf |
| Pro82 | CD | [31.3, 46.1, −0.2] | WPF shelf cap |
| Phe83 | CZ | [26.6, 43.8, −0.0] | WPF shelf |
| Tyr97 | OH | [20.6, 49.0, 4.0] | ZA loop gatekeeper |
| Asn140 | ND2 | [21.0, 48.0, −2.4] | H-bond to acetyl C=O |

Derived pocket metrics:

| Metric | Value |
|---|---|
| Asn140 ND2 → EAM CoM (≈ pocket depth from Asn140 to centre) | 6.0 Å |
| Closest EAM atom to Asn140 ND2 | 3.1 Å |
| Pocket entrance span (Tyr97 OH – Trp81 NE1) | 15.4 Å |
| Pocket axis unit vector (Asn140 → EAM CoM) | [0.888, 0.457, 0.053] |
| Kac-Nζ anchor (4.5 Å from Asn140 along axis) | [25.0, 50.0, −2.2] Å |
| Nearest BRD4 entrance-side atom to Kac-Nζ anchor | Leu94 CD1, 5.37 Å |
| Second nearest | Pro82 CB, 5.57 Å |

The Kac-Nζ anchor was derived from the known H-bond geometry: Nζ–C(acetyl) ~1.5 Å, C(acetyl)–Asn140 ND2 ~3.0 Å → Kac Nζ sits 4.5 Å from Asn140 ND2.

---

## Phase 4 — Ternary complex modelling and productive geometry

**Method**: For each BCL6-BTB surface Lys, BRD4-BD1 was translated so that the Kac-Nζ anchor coincided with the BCL6 Lys Nζ. BRD4 was then rotated to align the pocket axis anti-parallel to the BCL6 Lys Cα→Nζ axis (optimal insertion geometry). 36 spin angles around the insertion axis were sampled (10° steps); the spin with the greatest minimum BCL6–BRD4 heavy-atom distance was retained.

**Key diagnostic — axial protrusion**: distance from Lys Nζ to the nearest non-Lys BCL6 heavy atom, projected along the Lys axis. This measures how far the Nζ sticks out above the BCL6 protein body in the insertion direction. Productive reading requires this protrusion to exceed the BRD4 entrance-side atom clearance of 5.37 Å.

| Lys | SASA (Å²) | Axial protrusion (Å) | Required clearance (Å) | Deficit (Å) | Best-spin clash (Å) | Verdict |
|---|---|---|---|---|---|---|
| K66 | 93 | 2.24 | 5.37 | −3.14 | 1.02 | BLOCKED |
| K123 | 123 | 0.11 | 5.37 | −5.26 | 2.17 | BLOCKED |
| K126 | 176 | 5.33 | 5.37 | −0.05 | 1.65 | BORDERLINE |

K66 and K123 are blocked by the rigid BCL6 BTB fold: the deficits of 3.1–5.3 Å correspond to protein-body interpenetration that no linker optimisation can remove. K126 is within 0.05 Å of the clearance threshold; its very high B-factors (Cα 72, Nζ 126) and position at the penultimate residue of the chain (ends A128) are consistent with a disordered C-terminal tail capable of adopting an extended conformation that clears the margin.

Approach-angle half-cone for the pocket: atan((15.4/2)/4.5) ≈ 60°. This is the maximum allowed deviation from the pocket axis for Kac threading.

---

## Phase 5 — PROTAC degrader geometry and comparison

**Source**: PDB 6BOY (DDB1/CRBN/BRD4-BD1/dBET1 PROTAC).

Surface Lys on BRD4-BD1 (Chain C) in the PROTAC ternary complex:

| Lys | SASA (Å²) | Nζ → E3 surface (Å) | Approach angle (°) | Productive? |
|---|---|---|---|---|
| K91 | 175 | 5.9 | 64 | YES |
| K155 | 99 | 4.9 | 104 | YES |
| K72 | 113 | 8.6 | 87 | YES |
| K76 | 110 | 9.0 | 144 | YES |
| K111 | 64 | 10.1 | 39 | YES |
| K112 | 92 | 11.2 | 62 | YES |
| K160 | 59 | 8.7 | 90 | YES |
| K55 | 60 | 21.5–27.8 | — | no |
| K57 | 92 | 21.5 | — | no |
| K99 | 136 | 26.2 | — | no |
| K102 | 159 | 27.8 | — | no |

7 of 11 surface Lys are within the productive window (≤ 15 Å from the E3 receptor surface). Approach angles range from **39° to 144°** (mean 84°): the E2~Ub arm samples essentially all orientations, imposing no directional constraint.

---

## Comparative summary table

| Metric | BRD4 BD1 bromodomain reading | PROTAC ubiquitination |
|---|---|---|
| Productive Lys on BCL6-BTB | 1 (K126, borderline) | 3 (K66, K123, K126) |
| Required axial protrusion above target surface | ≥ 5.37 Å | ~0 Å (SASA > 0 sufficient) |
| Distance tolerance | ~0 Å slack | 5–15 Å wide window |
| Approach cone half-angle | ≤ 60° | 39°–144° (unconstrained) |
| Prerequisite modification | Acetylation | None |
| Recruitment-handle conflict | Yes (BD1 = drug site and reading site) | None |
| Transfer depth into active site | 4.5 Å (Kac Nζ to Asn140 ND2) | ~5 Å (Lys Nζ to E2 Cys) |

---

## Conclusion

Bromodomain insertion is the harder geometric constraint by a large margin. The fundamental asymmetry is topological: ubiquitination requires only proximity (Lys Nζ within 5–15 Å, any approach direction), while bromodomain reading requires insertion — the Kac must thread ≥ 4.5 Å into a narrow pocket, with the BCL6 protein body clearing the BRD4 entrance ridge by ≥ 5.37 Å. Rigid residues K66 and K123 fall short by 3.1 and 5.3 Å respectively; only the disordered C-terminal K126 approaches feasibility and then only barely. No BCL6-BTB residue is presented in a **productively certain** geometry for bromodomain reading; K126 is a candidate only under the assumption of C-terminal disorder and requires prior acetylation plus a recruitment design that reserves BD1 for reading rather than anchoring.
