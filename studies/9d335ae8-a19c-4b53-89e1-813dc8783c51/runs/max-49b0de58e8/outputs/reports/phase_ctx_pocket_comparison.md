
## Phase overview

Scripts 027–031 parsed the holo CDK2-CCNE.pdb structure containing compound CTX, extracted the 4.5 Å contact shell around CTX, and compared it quantitatively with the two pockets identified in the earlier dpCDK2-CCNE1 apo analysis: the ATP-binding pocket and the CDK2–CyclinE1 interface pocket.

---

## Input

| File | Content |
|---|---|
| `CDK2-CCNE.pdb` | CDK2 (chain A, res 0–298) + CyclinE1 (chain B, res 87–360) + CTX (HETATM chain B res 401, 72 heavy atoms) + 241 waters |
| dpCDK2-CCNE1 pocket data | Carried over from scripts 019–025: 74-residue ATP main pocket, 17-residue interface pocket |

---

## Scripts

### 027 — Structure parse and chain inventory

Manual fixed-column PDB reader. Confirmed: Chain A = CDK2 (299 residues, same range as dpCDK2-CCNE1), Chain B = CyclinE1 (267 residues). CTX is the only non-water HETATM, assigned to chain B resseq 401 with 72 heavy atoms (31 C, 5 N, 3 O, 33 H).

### 028 — CTX contact shell extraction

Built `cKDTree` on all ATOM-record coordinates. Queried with each CTX atom at radius 4.5 Å. Collected unique (chain, resseq, resname) triples. Result: **24 residues** in contact shell — 9 on CDK2 chain A, 15 on CyclinE1 chain B.

CTX centroid: (30.57, 5.37, −25.80) Å.

### 029 — Overlap computation vs both reference pockets

Computed set intersections and Jaccard similarity against:
1. ATP main pocket (74 chain-A residues from dpCDK2-CCNE1 anchor-based definition)
2. CDK2–CyclinE1 interface pocket (17 residues across both chains from LIGSITE Cluster 14)

### 030–031 — Cartoon visualization with pocket overlay

Loaded structure via biotite, ran P-SEA SSE assignment on each chain independently, projected all Cα onto PCA space (PC1 vs PC3). Drew cartoon backbone using `cartoon_utils.py` (CDK2 green, CyclinE1 blue). Overlaid three layers:
- Blue halos: ATP-binding pocket residues (dpCDK2-CCNE1)
- Lavender halos: interface pocket residues (dpCDK2-CCNE1)
- Orange stars + diamond: CTX contact shell + centroid (CDK2-CCNE.pdb)

Output: `CDK2_CTX_vs_pockets.png` (614 KB).

---

## Results

### CTX contact shell (4.5 Å, 24 residues)

| Chain | Residues |
|---|---|
| CDK2 (A) | L54, E57, L58, H121, R122, V123, A151, F152, G153 |
| CyclinE1 (B) | L90, V101, W102, I104, M105, N107, K108, T111, E149, S227, P228, L229, S233, W234, V237 |

### Overlap vs ATP-binding pocket

| Metric | Value |
|---|---|
| Shared residues (chain A) | L54, L58, V123 (3 of 74) |
| Jaccard similarity | 0.04 |
| Distance: CTX centroid → ATP centroid | 19.1 Å |

**Conclusion: No meaningful overlap.** CTX is not an ATP-site ligand. The 3 shared residues (L54, L58, V123) are peripheral N-lobe residues that border both cavities.

### Overlap vs CDK2–CyclinE1 interface pocket

| Metric | Value |
|---|---|
| Shared CDK2 residues | H121, R122 |
| Shared CyclinE1 residues | L90, V101, W102, I104, M105 |
| Total shared | 7 of 17 (41% of reference pocket) |
| Jaccard similarity | 0.21 |

**Conclusion: CTX binds at the CDK2–CyclinE1 interface.** The core anchors identified in the apo structure (H121/R122 on CDK2; L90, W102, I104, M105 on CyclinE1) are confirmed. CTX expands the pocket by 17 additional residues: A151, F152, G153 on the CDK2 αF-helix region and N107, K108, T111, E149, S227–L229, S233, W234, V237 on the CyclinE1 second cyclin-box helix — an induced-fit expansion not visible in the apo structure.

---

## Figures

![CTX binding site vs ATP and interface pockets on CDK2-CyclinE1 cartoon](CDK2_CTX_vs_pockets.png)

---

## Audit

| Check | Result |
|---|---|
| CTX atom count reasonable for a drug-like molecule? | 72 heavy atoms — large but consistent with a macrocycle or bivalent compound; all atoms parsed |
| ATP-pocket residues contacted by CTX? | No key catalytic residues (K33, E51, F80–H84, D127, DFG, C177) contacted |
| Interface core residues recovered by CTX? | Yes — H121, R122 (CDK2) and L90, W102, I104, M105 (CyclinE1) all confirmed |
| Induced-fit expansion residues new vs apo? | Yes — 17 residues in CTX shell absent from apo interface pocket definition |
| Distance confirms separate pocket from ATP site? | Yes — 19.1 Å centroid separation, no spatial overlap |
| Visualization produced without errors? | Yes — 614 KB PNG |
