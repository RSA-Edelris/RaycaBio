
## Phase overview

Scripts 032–035 computed pocket druggability descriptors for all six binding sites identified across the three structures in this run (CRBN, dpCDK2–CyclinE1 apo, CDK2–CCNE holo) and produced a scored, annotated summary figure.

---

## Scripts

### 032 — Atom dictionary construction

Parsed all three PDB files with a manual fixed-column reader and built per-structure atom dictionaries keyed by `(chain, resseq)` for fast per-residue coordinate lookup:

| Structure | Keys (unique residues) |
|---|---|
| CRBN | 370 |
| dpCDK2–CyclinE1 (apo) | 566 |
| CDK2–CCNE (holo) | 566 |

### 033 — Helper module `drug_utils.py`

Wrote `residue_descriptors()` to disk so it persists across interpreter calls. Given a list of `(chain, resseq, resname)` triples and an atom dictionary, the function:
- Collects Cα coordinates for each residue
- Computes a convex hull volume over those Cα positions (Å³ proxy for pocket size)
- Counts amino acid fractions: hydrophobic (AILVMFYWP), polar (STNQ), positively charged (KRH), negatively charged (DE), aromatic (FYW)

### 034 — Pocket residue triple assembly and descriptor computation

Defined all six pocket residue sets from the previous phases:

| Pocket | Source | n residues |
|---|---|---|
| CRBN main (IMiD) | LVY 4.5 Å contact shell (phase 1) | 36 |
| CRBN allosteric (zinc shell) | LIGSITE cluster + Cys/His zinc ligands | 15 |
| CDK2 ATP-binding | Canonical anchor 5 Å shell (phase 3) | 74 |
| CDK2 T-loop allosteric | LIGSITE Cluster 4 (phase 3) | 16 |
| CDK2–CyclinE1 interface (apo) | LIGSITE Cluster 14 (phase 3) | 17 |
| CDK2–CCNE CTX binding (holo) | CTX 4.5 Å contact shell (phase 4) | 24 |

### 035 — Composite scoring and figure

Scored each pocket on four criteria (max raw 12, normalised to 10):

| Criterion | Bins | Max pts |
|---|---|---|
| Volume (Cα hull) | <500 Å³=1, 500–1500=2, 1500–4000=3, >4000=4 | 4 |
| Hydrophobicity | <0.25=0, 0.25–0.40=1, 0.40–0.50=2, >0.50=3 | 3 |
| Aromatic fraction | <0.05=0, 0.05–0.12=1, >0.12=2 | 2 |
| Literature confirmation | none=0, leads=1, drugs approved=3 | 3 |

Output: `druggability_all_pockets.png` — horizontal bar chart (left) and descriptor table (right), colour-coded by verdict tier.

---

## Results

| Score | Verdict | Target | Pocket | Vol (Å³) | Hydro | Arom |
|---|---|---|---|---|---|---|
| 9.2 | Highly druggable | dpCDK2–CyclinE1 | ATP-binding | 9 790 | 0.55 | 0.09 |
| 8.3 | Highly druggable | CRBN | Main (IMiD) | 2 585 | 0.42 | 0.22 |
| 8.3 | Druggable | CDK2–CCNE (holo) | CTX binding | 2 196 | 0.58 | 0.12 |
| 6.7 | Moderately druggable | dpCDK2–CyclinE1 | T-loop allosteric | 604 | 0.50 | 0.19 |
| 5.8 | Moderately druggable | dpCDK2–CyclinE1 | Interface (apo) | 695 | 0.47 | 0.12 |
| 1.7 | Challenging | CRBN | Allosteric (zinc shell) | 518 | 0.13 | 0.00 |

---

## Figures

![Druggability scores for all six pockets across CRBN, dpCDK2-CyclinE1 and CDK2-CCNE](druggability_all_pockets.png)

---

## Audit

| Check | Result |
|---|---|
| All six pockets from previous phases included? | Yes — CRBN ×2, dpCDK2–CyclinE1 ×3, CDK2–CCNE ×1 |
| Volume proxy consistent (Cα convex hull throughout)? | Yes — same method applied uniformly; not absolute cavity volumes |
| Hydrophobicity fractions directionally consistent with literature? | Yes — ATP site (0.55) and CTX interface (0.58) highest, zinc shell lowest (0.13) |
| Literature scores independently assigned before computing total? | Yes — assigned per pocket before scoring loop |
| CRBN zinc shell correctly flagged as challenging? | Yes — no aromatic content, lowest hydrophobicity, smallest volume |
| CDK2 apo vs holo interface comparison valid? | Yes — apo score (5.8) correctly lower than holo CTX-expanded pocket (8.3) |
| Figure produced without errors? | Yes — 168 KB PNG |
| Scoring formula documented in this writeup? | Yes — bin thresholds and max points recorded above |
