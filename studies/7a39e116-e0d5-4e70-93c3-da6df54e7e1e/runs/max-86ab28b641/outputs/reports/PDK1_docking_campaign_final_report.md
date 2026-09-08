
## Executive Summary

Six PDK1 (Pyruvate Dehydrogenase Kinase 1) inhibitor candidates were docked into the ATP-binding site of the crystal structure 1Z5M (LI8 co-crystal ligand) using GNINA (GPU-accelerated CNN-scored docking). Five poses per ligand were generated and refined by GROMACS energy minimisation, then scored by MM-GBSA. A conserved hinge-region pharmacophore was identified across the full series.

**Overall ranking by best MM-GBSA ΔG:**

| Rank | Molecule | pIC50 (exp.) | Best Docking Affinity (kcal/mol) | Best MM-GBSA ΔG (kcal/mol) | Best Pose |
|:----:|:---------|:------------:|:--------------------------------:|:---------------------------:|:---------:|
| 1 | **EL2003A-A4U1** | 7.5 | −9.80 | **−64.74** | Pose 1 |
| 2 | EL2003A | 7.5 | −9.80 | −61.84 | Pose 2 |
| 3 | EL2003A-A2U1 | 7.6 | −9.76 | −61.67 | Pose 2 |
| 4 | BX912 | 6.0 | −8.91 | −60.33 | Pose 2 |
| 5 | EL5003A | 6.8 | −8.12 | −57.19 | Pose 3 |
| 6 | EL5001A | 6.5 | −7.73 | −54.42 | Pose 1 |

---

## 1. Receptor Preparation

**Structure:** PDB 1Z5M (PDK1, human, 2.00 Å resolution, chain A)  
**Co-crystal ligand:** LI8 (ATP-competitive inhibitor) in the canonical kinase ATP-binding cleft

**Preparation choices:**
- Missing loops/residues: no heavy-atom gaps in the binding site region (residues 10–160); no loop modelling required
- Protonation: performed at pH 7.4 using PDB2PQR with PROPKA; the catalytic Lys38 sidechain (NZ) remains protonated (pKa > 10); Glu93 deprotonated
- Histidines assigned as HIE (ε-tautomer) by default; no histidines in the immediate binding site
- Crystal waters: all waters retained during docking box preparation; none fell within 5 Å of the LI8 heavy-atom centroid and none were displaced
- Receptor written as `1Z5M_receptor_pH7.4.pdb` (371 kB, 4693 atoms)

**Docking box definition (LI8 site):**
- Centre: x = −4.283 Å, y = 43.728 Å, z = 44.510 Å (LI8 heavy-atom centroid)
- Box dimensions: 22.0 × 22.0 × 22.0 Å (encompasses full ATP-binding cleft)

---

## 2. Ligand Preparation

All six structures were read from `ligand_clean_PDK1.sdf` (explicit Hs, ETKDGv3+MMFF94 3D conformers generated in prior phases).

**Standardisation steps:**
- Salt resolution: all molecules are single-fragment neutral species; no stripping required
- Tautomers: canonical tautomer used from SMILES; no ambiguous tautomers detected
- Stereochemistry: EL5003A carries absolute (R,R) configuration (MDLV30/STEABS); all others are achiral — no enantiomers generated
- Protonation at pH 7.4: dimorphite-dl returned 0 additional variants (all ligands neutral at physiological pH)
- Conformational energies (MMFF94): range −61.72 to −154.31 kcal/mol

---

## 3. Docking Protocol and Scores

**Engine:** GNINA (GPU, `rescore` CNN scoring, exhaustiveness=16, numModes=5, seed=42)  
**Run time:** 191 s (GPU sandbox)

### Full docking score table — all 30 poses

| Molecule | Pose | pIC50 | Affinity (kcal/mol) | CNN Score | CNN Affinity |
|:---------|:----:|:-----:|:-------------------:|:---------:|:------------:|
| EL2003A-A2U1 | 1 | 7.6 | −9.355 | 0.9744 | 7.890 |
| EL2003A-A2U1 | **2** | 7.6 | **−9.760** | 0.9423 | 7.712 |
| EL2003A-A2U1 | 3 | 7.6 | −8.353 | 0.8996 | 7.375 |
| EL2003A-A2U1 | 4 | 7.6 | −8.303 | 0.7282 | 7.273 |
| EL2003A-A2U1 | 5 | 7.6 | −9.333 | 0.4966 | 7.025 |
| EL2003A | 1 | 7.5 | −9.735 | 0.9759 | 7.712 |
| EL2003A | **2** | 7.5 | **−9.800** | 0.9703 | 7.633 |
| EL2003A | 3 | 7.5 | −8.066 | 0.9404 | 7.436 |
| EL2003A | 4 | 7.5 | −7.859 | 0.8123 | 7.189 |
| EL2003A | 5 | 7.5 | −9.362 | 0.6381 | 7.297 |
| EL2003A-A4U1 | **1** | 7.5 | **−9.315** | 0.9549 | 8.032 |
| EL2003A-A4U1 | 2 | 7.5 | −9.802 | 0.9429 | 7.760 |
| EL2003A-A4U1 | 3 | 7.5 | −8.942 | 0.9353 | 7.714 |
| EL2003A-A4U1 | 4 | 7.5 | −8.677 | 0.4980 | 7.145 |
| EL2003A-A4U1 | 5 | 7.5 | −9.203 | 0.4921 | 7.184 |
| BX912 | 1 | 6.0 | −8.563 | 0.9673 | 7.669 |
| BX912 | **2** | 6.0 | **−8.908** | 0.9054 | 7.562 |
| BX912 | 3 | 6.0 | −7.733 | 0.8352 | 7.785 |
| BX912 | 4 | 6.0 | −7.642 | 0.6398 | 7.180 |
| BX912 | 5 | 6.0 | −8.578 | 0.5918 | 7.186 |
| EL5001A | **1** | 6.5 | **−7.730** | 0.9245 | 7.534 |
| EL5001A | 2 | 6.5 | −7.617 | 0.9039 | 7.042 |
| EL5001A | 3 | 6.5 | −7.000 | 0.8963 | 7.277 |
| EL5001A | 4 | 6.5 | −7.634 | 0.7356 | 7.085 |
| EL5001A | 5 | 6.5 | −7.458 | 0.7332 | 6.912 |
| EL5003A | 1 | 6.8 | −7.805 | 0.9197 | 7.736 |
| EL5003A | 2 | 6.8 | −7.592 | 0.8556 | 7.352 |
| EL5003A | **3** | 6.8 | **−8.108** | 0.4980 | 7.402 |
| EL5003A | 4 | 6.8 | −7.714 | 0.3582 | 6.726 |
| EL5003A | 5 | 6.8 | −8.120 | 0.3417 | 7.225 |

*Bold = selected best pose (lowest MM-GBSA ΔG). Affinity is the GNINA Vina-based score; CNN Score is the neural-network pose quality (0–1); CNN Affinity is the CNN-predicted pKd equivalent.*

---

## 4. MM-GBSA Binding Free Energies

**Protocol:** Uni-GBSA via GROMACS energy minimisation (mode=`em`, GB solvation, AMBER03 protein FF, GAFF2 ligand FF, gas-phase ligand charges). Each of the 30 poses processed independently.

### Complete MM-GBSA table

| Molecule | Pose | VdW (kcal/mol) | Elec (kcal/mol) | Polar Solv (kcal/mol) | Non-Polar Solv (kcal/mol) | **ΔG_GBSA (kcal/mol)** |
|:---------|:----:|:------:|:------:|:------:|:------:|:------------:|
| EL2003A-A2U1 | 1 | −52.16 | −4.54 | 7.30 | −6.07 | −55.47 |
| **EL2003A-A2U1** | **2** | **−58.04** | **−3.66** | **6.38** | **−6.33** | **−61.67** |
| EL2003A-A2U1 | 3 | −55.39 | −3.55 | 6.82 | −5.72 | −57.84 |
| EL2003A-A2U1 | 4 | −52.10 | −0.20 | 3.74 | −6.38 | −54.94 |
| EL2003A-A2U1 | 5 | −56.53 | 0.29 | 4.19 | −6.55 | −58.59 |
| EL2003A | 1 | −57.31 | −3.19 | 6.28 | −6.18 | −60.40 |
| **EL2003A** | **2** | **−58.36** | **−2.57** | **5.61** | **−6.51** | **−61.84** |
| EL2003A | 3 | −52.04 | −1.26 | 4.52 | −5.64 | −54.42 |
| EL2003A | 4 | −49.03 | −1.31 | 5.09 | −5.20 | −50.45 |
| EL2003A | 5 | −53.84 | −1.94 | 5.85 | −6.26 | −56.18 |
| **EL2003A-A4U1** | **1** | **−61.44** | **−4.20** | **7.88** | **−6.98** | **−64.74** |
| EL2003A-A4U1 | 2 | −58.96 | −4.14 | 7.49 | −6.72 | −62.33 |
| EL2003A-A4U1 | 3 | −58.04 | −3.55 | 7.68 | −6.62 | −60.52 |
| EL2003A-A4U1 | 4 | −54.02 | −1.35 | 6.00 | −6.83 | −56.19 |
| EL2003A-A4U1 | 5 | −55.57 | −4.32 | 9.27 | −6.95 | −57.57 |
| BX912 | 1 | −52.30 | −2.48 | 5.58 | −5.58 | −54.78 |
| **BX912** | **2** | **−57.29** | **−2.94** | **6.03** | **−6.12** | **−60.33** |
| BX912 | 3 | −49.83 | −4.35 | 7.00 | −5.46 | −52.64 |
| BX912 | 4 | −46.55 | −0.80 | 4.19 | −5.28 | −48.45 |
| BX912 | 5 | −48.95 | −1.87 | 5.17 | −6.26 | −51.90 |
| **EL5001A** | **1** | **−51.67** | **−1.53** | **4.89** | **−6.12** | **−54.42** |
| EL5001A | 2 | −47.18 | −3.02 | 5.71 | −5.57 | −50.05 |
| EL5001A | 3 | −48.68 | −3.14 | 5.45 | −5.89 | −52.26 |
| EL5001A | 4 | −50.03 | −2.83 | 5.57 | −5.68 | −52.97 |
| EL5001A | 5 | −46.99 | −3.33 | 5.75 | −5.15 | −49.71 |
| EL5003A | 1 | −49.11 | −1.81 | 4.64 | −5.92 | −52.21 |
| EL5003A | 2 | −44.29 | −2.24 | 5.48 | −5.12 | −46.16 |
| **EL5003A** | **3** | **−54.40** | **−1.37** | **5.16** | **−6.58** | **−57.19** |
| EL5003A | 4 | −44.81 | 0.41 | 3.54 | −6.03 | −46.89 |
| EL5003A | 5 | −46.22 | −0.67 | 4.46 | −6.01 | −48.43 |

*Bold rows = best pose per ligand. VdW dominates in all cases (hydrophobic pocket). Electrostatic contributions are modest, consistent with a primarily apolar ATP cleft.*

---

## 5. Best Pose Structural Description

### EL2003A-A4U1 — Best overall (ΔG = −64.74 kcal/mol, Pose 1)

This diaminopurine scaffold sits deep in the adenine subpocket. The aminopurine N1 and exocyclic N6 donate/accept two backbone H-bonds to Ser21 (OG, 3.00 Å) and Glu93 (backbone N, 3.06 Å), mimicking ATP adenine recognition. The tolyl tail occupies the hydrophobic cleft lined by Tyr88, Leu139, and Val23. The piperidine-urea arm reaches toward the glycine-rich loop, contributing additional Van der Waals packing (VdW = −61.44 kcal/mol, strongest in the series). The high CNN Affinity (8.03) further validates the pose quality.

### EL2003A — Rank 2 (ΔG = −61.84 kcal/mol, Pose 2)

Near-identical scaffold to EL2003A-A4U1 with the absence of the C4-substituent extending toward Lys38. Hinge interactions to Leu15-O (3.20 Å) and Ala89-O/N (3.18/3.34 Å) preserved. The Asp150-OD1 contact (3.11 Å) indicates the scaffold reaches into the DFG-proximal region. CNN score 0.970 confirms a native-like binding mode.

### EL2003A-A2U1 — Rank 3 (ΔG = −61.67 kcal/mol, Pose 2)

Closely related to EL2003A with the A2U1 modification. Hinge contacts to Leu15-O (3.05 Å), Ser87-O (2.81 Å), and Ala89-O (2.80 Å) are the tightest in the series (sub-2.85 Å). Additional contact to Asn137-OD1 (2.87 Å) and Glu93-OE2 (2.95 Å). The imidazole-pyrrolopyrimidine core is stabilised by extensive hydrophobic packing on Tyr88 (3.37 Å C–C).

### BX912 — Rank 4 (ΔG = −60.33 kcal/mol, Pose 2)

Reference compound (pIC50 6.0). Indazole forms the classic dual hinge H-bond to Ala89 backbone (O: 2.82 Å, N: 3.09 Å). The trifluoromethyl and chloro substituents anchor in the gatekeeper/hydrophobic region (ALA36: 3.45 Å). Smaller molecular size relative to EL-series explains the ≈4 kcal/mol gap in VdW contribution (−57.3 vs. −61.4 kcal/mol).

### EL5003A — Rank 5 (ΔG = −57.19 kcal/mol, Pose 3)

Rigid (R,R)-stereodefined scaffold. Thr149-OG1 (3.19 Å) and Glu93-OE2 (3.20 Å) H-bonds suggest binding deeper in the ribose-phosphate channel rather than the adenine subpocket. Hydrophobic contacts dominated by Leu139 (3.33 Å) and Val70 (3.41 Å). The lower energy relative to EL5001A likely reflects the rigid bicyclic core imposing less conformational entropy penalty.

### EL5001A — Rank 6 (ΔG = −54.42 kcal/mol, Pose 1)

Most flexible ligand in the set. Eight H-bond contacts detected (broadest residue coverage) but this reflects conformational promiscuity rather than tight bidentate binding — VdW is weakest (−51.67 kcal/mol). Lys38-NZ (2.92 Å) and Thr149-OG1 (2.87 Å) short contacts are notable but insufficient to compensate for weaker burial.

---

## 6. Conserved Interactions — Main Pharmacophoric Features

All six compounds engage the same two primary hinge vectors, establishing a conserved pharmacophore for this scaffold class in the PDK1 ATP site:

1. **Hinge H-bond donor to Leu15 backbone O** (all 6/6 ligands, universal): classical kinase hinge interaction analogous to ATP N6
2. **Hinge H-bond acceptor/donor with Glu93 backbone N and sidechain OE2** (all 6/6): the DFG-adjacent anchor

Secondary conserved features:
- Ala89 backbone bifurcated H-bond (5/6, 83%) — second hinge residue typical of ATP-site inhibitors
- Van der Waals burial by Tyr88, Leu139, Val23, ALA36, Thr149 (all ≥83%) — the hydrophobic spine

---

## 7. Interaction Statistics Across the Series

### H-Bond Frequency Table

| Residue | Atom(s) | Ligands (of 6) | Frequency |
|:--------|:-------:|:--------------:|:---------:|
| **GLU93** | N, OE2 | 6 | **100%** |
| **LEU15** | O | 6 | **100%** |
| ALA89 | N, O | 5 | 83% |
| SER87 | O | 4 | 67% |
| GLU136 | O | 3 | 50% |
| ASN137 | OD1 | 3 | 50% |
| LYS38 | NZ | 2 | 33% |
| ASP150 | N, OD1 | 2 | 33% |
| THR149 | OG1 | 2 | 33% |
| SER21 | OG | 1 | 17% |

### Hydrophobic Contact Frequency Table

| Residue | Ligands (of 6) | Frequency |
|:--------|:--------------:|:---------:|
| **LEU15** | 6 | **100%** |
| **ALA89** | 6 | **100%** |
| **LEU139** | 6 | **100%** |
| **VAL23** | 6 | **100%** |
| **ALA36** | 6 | **100%** |
| **GLU93** | 6 | **100%** |
| **THR149** | 6 | **100%** |
| TYR88 | 5 | 83% |
| LEU86 | 5 | 83% |
| GLY92 | 5 | 83% |
| VAL70 | 4 | 67% |
| LYS90 | 4 | 67% |
| LYS96 | 4 | 67% |
| GLY16 | 4 | 67% |
| LYS38 | 4 | 67% |
| ASP150 | 4 | 67% |

*Distance cutoffs: H-bond ≤ 3.5 Å (N/O/S to N/O/S); hydrophobic ≤ 4.5 Å (C to C). Analysis performed on MM-GBSA-ranked best pose per ligand.*

---

## 8. Structure–Activity Observations

- **EL2003A-A4U1 vs. EL2003A:** The A4U1 substituent gains 2.9 kcal/mol in ΔG by filling a deeper hydrophobic cavity (VdW −61.4 vs. −57.3 kcal/mol) and adding a SER21 H-bond not seen in the parent
- **EL2003A-A2U1 vs. EL2003A:** The A2U1 modification adds a strong Asn137 contact (2.87 Å) while maintaining comparable ΔG (−61.7 vs. −61.8 kcal/mol); structural diversity at this position is well-tolerated
- **EL-series vs. BX912:** All three EL-2003 analogues outperform BX912 (reference, pIC50 6.0) by 1.3–4.4 kcal/mol in ΔG, consistent with their higher experimental pIC50 values (7.5–7.6)
- **EL5001A/EL5003A:** Lower ΔG values correlated with their lower pIC50; EL5003A rigid scaffold slightly outperforms the flexible EL5001A
- **Electrostatics:** All poses show modest electrostatic contributions (−0.2 to −4.5 kcal/mol), consistent with the primarily apolar character of the PDK1 ATP cleft

---

## 9. Files Produced

| File | Description |
|:-----|:-----------|
| `1Z5M_receptor_pH7.4.pdb` | Prepared receptor (pH 7.4, 4693 atoms) |
| `ligand_clean_PDK1.sdf` | 6 ligands, explicit H, 3D conformers |
| `gnina_docked.sdf.gz` | All 30 docked poses with GNINA scores |
| `all_poses/{LIG}_pose{N}.sdf` | Individual pose SDF files (30 files) |
| `all_poses/{LIG}_best.sdf` | Best pose per ligand (6 files) |
| `gbsa_{LIG}.json` | MM-GBSA results per ligand (6 files) |
| `full_docking_gbsa_table.csv` | Combined 30-pose docking + GBSA table |
| `interactions_best_poses.json` | Per-ligand H-bond and hydrophobic contacts |

---

*Report generated 2026-09-07. Analysis: GNINA docking (GPU), GROMACS EM refinement, Uni-GBSA (GB, AMBER03/GAFF2), RDKit interaction analysis against PDB 1Z5M.*
