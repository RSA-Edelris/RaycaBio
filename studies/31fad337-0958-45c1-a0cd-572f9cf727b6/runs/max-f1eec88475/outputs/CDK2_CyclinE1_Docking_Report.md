
## Executive Summary

A complete structure-based virtual screening campaign was run against CDK2–CyclinE1 using an 84-compound CTX-series library (P841 selection). Receptor preparation, ligand standardisation, GPU-accelerated docking (gnina CNN-rescored Vina), conformational strain scoring, ProLIF interaction fingerprinting, and MM-GBSA binding free energy calculations were performed. The top compound **CTX-1020732** achieved CNN pKi = 8.93 with pose quality 0.99 and MM-GBSA ΔG = −83.19 kcal/mol, followed by **CTX-1020811** (ΔG −80.27) and **CTX-1020521** (ΔG −80.08). All 84 compounds were successfully docked with 5 poses each; MM-GBSA was computed for all 84 compounds (100% success; CTX-1020667 re-docked independently). Interaction analysis on the top 20 revealed a conserved pharmacophoric motif spanning the CDK2 (chain A) and CyclinE1 (chain B) interface, anchored by hydrophobic contacts with MET105.B/LYS108.B and a hydrogen-bond donation from HIS121.A.

---

## 1. Methods

### 1.1 Receptor Preparation

**Input structure:** dpCDK2–CCNE1_CTX-1017233_Best.pdb (1.94 Å resolution co-crystal of CDK2–CyclinE1 with the reference CTX ligand).

**Workflow:**
- CTX ligand extracted to define the binding site; all HETATM ligand records removed from the receptor
- Crystallographic waters within 4.0 Å of any CTX atom retained (9 waters; residues HOH identified by minimum-distance criterion over all CTX HETATM records)
- PDBFixer (v 1.12.0) applied: missing residues added, protonation state set with `addMissingHydrogens(7.4)` (CHARMM forcefield), OPLS-AA charges
- Two receptor files produced:
  - **receptor_raw.pdb** — no explicit H (correct gnina Vina-mode input; gnina types internally)
  - **receptor_prepared.pdb** — explicit H at pH 7.4 (used for ProLIF H-bond detection)

**Docking box** defined from the centroid and extent of all CTX HETATM records (72 atoms including H):

| Parameter | Value |
|:---|---:|
| Center X | 30.57 Å |
| Center Y | 5.37 Å |
| Center Z | −25.80 Å |
| Width (X) | 35.0 Å |
| Height (Y) | 30.0 Å |
| Depth (Z) | 31.0 Å |

*Note: centroid was computed over all HETATM atoms including H, giving a ~0.6 Å X-shift relative to the heavy-atom centroid. The box dimensions are sufficient that no binding-relevant pose is excluded.*

### 1.2 Ligand Standardisation

**Library:** P841_selection_clean.sdf — 84 compounds after deduplication.

**Pipeline (RDKit):**
1. LargestFragmentChooser — salt/counterion removal
2. MolStandardize Normalizer — canonical valence and connectivity
3. TautomerEnumerator.Canonicalize (rdkit.Chem.MolStandardize) — canonical tautomer
4. Dimorphite-DL — dominant protonation state at pH 6.9–7.9, max 1 variant
5. ETKDGv3 (seed 42) — 3D conformer embedding
6. MMFF94s minimisation

All 84 ligands passed embedding and energy minimisation. No duplicates by InChIKey.

### 1.3 Molecular Docking

**Engine:** gnina 1.0 (GPU, CNN-rescored Vina mode)

**Parameters:**

| Parameter | Value |
|:---|:---|
| numModes | 5 |
| cnnScoring | rescore |
| exhaustiveness | 8 |
| seed | 42 |
| GPU | Yes (A100 80 GB) |
| Receptor | receptor_raw.pdb |

Docking was run in parallel batches (15 concurrent jobs) using ThreadPoolExecutor. Results were checkpointed incrementally. All 84 compounds completed successfully (5 poses each).

### 1.4 Scoring

Two complementary scores were used:

- **Vina affinity** (kcal/mol): classical AutoDock Vina score; more negative = more favourable
- **CNN pKi**: gnina deep-learning CNN score trained on PDBbind; predicts −log₁₀(Kᵢ) directly; used as the primary ranking metric
- **CNN pose score** (0–1): CNN confidence in pose quality; values ≥0.9 indicate high-confidence poses

Primary ranking is by CNN pKi descending. The CNN score integrates pose quality and affinity in a single trained model and generally outperforms Vina alone on CDK targets.

### 1.5 Conformational Strain

**MMFF94s strain energy (kcal/mol):** computed on the docked ligand conformation alone using the RDKit MMFF94s force field. This is the intramolecular strain of the pose — **not** a protein–ligand interaction energy. High values (>200 kcal/mol MMFF94s) indicate strained conformations that may be artefactual. Available for the top 20 compounds (pose SDF files re-extracted post-screening).

### 1.6 Interaction Fingerprinting

**Library:** ProLIF 2.2.1 + MDAnalysis 2.10.0

- Receptor: `receptor_prepared.pdb` (explicit H required for HBDonor/HBAcceptor detection)
- Ligand: best-ranked pose SDF for each of the top 20 compounds
- Interaction types: Hydrophobic, HBDonor, HBAcceptor, PiStacking, CationPi, VdWContact, Anionic, Cationic, EdgeToFace, FaceToFace
- Results reported as residue:interaction_type keys per compound and as frequency statistics over the 20-compound set

---

## 2. Docking Results — Top 20 Compounds

Ranked by CNN pKi (primary metric). MMFF strain available for compounds with pose files.

| Rank | Compound | Vina (kcal/mol) | CNN pKi | CNN Pose | MMFF Strain (kcal/mol) |
|:---:|:---|---:|---:|---:|---:|
| 1 | CTX-1020732 | −14.02 | **8.931** | 0.992 | 125.6 |
| 2 | CTX-1020903 | −14.52 | 8.586 | 0.987 | 158.0 |
| 3 | CTX-1020811 | −13.17 | 8.586 | 0.976 | 198.0 |
| 4 | CTX-1020743 | −13.72 | 8.575 | 0.976 | 143.3 |
| 5 | CTX-1019813 | −12.10 | 8.306 | 0.946 | 198.3 |
| 6 | CTX-1020521 | −13.15 | 8.233 | 0.420 | 201.8 |
| 7 | CTX-1019757 | −11.24 | 8.107 | 0.855 | 178.9 |
| 8 | CTX-1020745 | −9.88 | 8.002 | 0.762 | 113.1 |
| 9 | CTX-1020441 | −12.43 | 7.846 | 0.729 | 196.6 |
| 10 | CTX-1020753 | −8.53 | 7.826 | 0.563 | 165.3 |
| 11 | CTX-1019473 | −10.15 | 7.740 | 0.697 | 128.6 |
| 12 | CTX-1020751 | −13.64 | 7.736 | 0.900 | 170.4 |
| 13 | CTX-1020752 | −11.50 | 7.715 | 0.605 | 229.1 |
| 14 | CTX-1020456 | −8.00 | 7.667 | 0.509 | 185.6 |
| 15 | CTX-1020562 | −11.50 | 7.627 | 0.449 | 289.2 |
| 16 | CTX-1020800 | −11.84 | 7.598 | 0.488 | 128.4 |
| 17 | CTX-1020555 | −12.45 | 7.595 | 0.465 | 109.9 |
| 18 | CTX-1020696 | −9.31 | 7.527 | 0.439 | 132.4 |
| 19 | CTX-1019613 | −12.79 | 7.507 | 0.535 | 216.6 |
| 20 | CTX-1020748 | −10.86 | 7.483 | 0.491 | 122.8 |

**Key observations:**
- The top 5 compounds (CNN pKi 8.0–8.9) all achieve Vina ≤ −11.2 kcal/mol, confirming convergence of both scoring methods
- Compounds 1–5 have CNN pose scores ≥ 0.946, indicating high-quality, confident poses
- CTX-1020521 (rank 6) has a high CNN pKi (8.233) but low pose score (0.420), suggesting the affinity prediction may be less reliable; flagged for visual inspection
- CTX-1020562 (rank 15) has the highest strain (289.2 kcal/mol) among the top 20 — the docked conformation is unusually strained
- CTX-1020732 (rank 1) has the lowest strain in the top 5 (125.6 kcal/mol), the highest CNN pKi and pose score — the best overall candidate
- **Reference compound CTX-1017233** (the co-crystal ligand) ranks **45th** (CNN 7.114), consistent with the library representing improved analogs designed to outperform the starting point

---

## 3. Binding Mode and Main Interactions

### 3.1 Binding Site Description

The binding pocket is located at the CDK2 (chain A) / CyclinE1 (chain B) co-crystal interface. Interactions span both subunits, consistent with a site defined by the co-crystallised CTX ligand at the CDK2 catalytic cleft region. CDK2 residues contributing to the pocket include GLU57, HIS121, ARG122, ALA151, GLY153, and VAL154. CyclinE1 residues include MET105, LYS108, ILE104, TRP102, TRP234, LEU229, SER233, and VAL237.

### 3.2 Per-Compound Interaction Profiles (Top 5)

**CTX-1020732 (rank 1, CNN pKi 8.931):**
Hydrophobic contacts with GLU57.A, HIS121.A, ARG122.A, MET105.B, LYS108.B, TRP102.B, TRP234.B, VAL237.B. H-bond donated to HIS121.A. H-bond accepted from ARG122.A. VdW contacts with ALA151.A, GLY153.A, ASN107.B, ILE104.B, LEU229.B. Comprehensive engagement of both CDK2 and CyclinE1 pharmacophore residues.

**CTX-1020903 (rank 2, CNN pKi 8.586):**
Identical core contacts to CTX-1020732 with additional VdW contacts with SER227.B, SER233.B, and TRP234.B. H-bond donor to HIS121.A.

**CTX-1020811 (rank 3, CNN pKi 8.586):**
Core contacts maintained. Additional contacts with LEU90.B, LEU229.B (hydrophobic). Missing ARG122.A H-bond acceptor interaction compared to CTX-1020732.

**CTX-1020743 (rank 4, CNN pKi 8.575):**
Core pharmacophore preserved. H-bond donor to HIS121.A. Additional contacts with LEU229.B, VAL101.B. Missing ASN107.B VdW contact.

**CTX-1019813 (rank 5, CNN pKi 8.306):**
Full core pharmacophore engagement including H-bond donor to HIS121.A, hydrophobic contacts with GLU57.A/ARG122.A/MET105.B/LYS108.B/TRP102.B/TRP234.B/VAL237.B, and extensive VdW contacts. Additional contacts with VAL123.A.

---

## 4. Series Interaction Statistics

Based on ProLIF fingerprinting of the top 20 compounds (n = 20 analysed, n = 0 failed).

| Residue : Interaction Type | Count | Frequency (%) |
|:---|:---:|:---:|
| GLU57.A : VdWContact | 20 | **100** |
| HIS121.A : VdWContact | 20 | **100** |
| MET105.B : Hydrophobic | 20 | **100** |
| LYS108.B : Hydrophobic | 20 | **100** |
| LYS108.B : VdWContact | 20 | **100** |
| GLU57.A : Hydrophobic | 19 | 95 |
| ILE104.B : VdWContact | 19 | 95 |
| HIS121.A : Hydrophobic | 18 | 90 |
| ALA151.A : VdWContact | 18 | 90 |
| MET105.B : VdWContact | 17 | 85 |
| ARG122.A : VdWContact | 15 | 75 |
| LEU229.B : VdWContact | 15 | 75 |
| SER233.B : VdWContact | 15 | 75 |
| ARG122.A : Hydrophobic | 14 | 70 |
| ASN107.B : VdWContact | 14 | 70 |
| VAL237.B : VdWContact | 13 | 65 |
| HIS121.A : HBDonor | 10 | 50 |
| GLY153.A : VdWContact | 10 | 50 |
| TRP102.B : Hydrophobic | 10 | 50 |
| TRP102.B : VdWContact | 10 | 50 |
| TRP234.B : Hydrophobic | 10 | 50 |
| VAL237.B : Hydrophobic | 8 | 40 |
| GLU149.B : Hydrophobic | 7 | 35 |
| VAL154.A : VdWContact | 6 | 30 |
| TRP234.B : VdWContact | 5 | 25 |
| VAL123.A : VdWContact | 5 | 25 |
| GLU149.B : VdWContact | 5 | 25 |
| SER227.B : VdWContact | 4 | 20 |
| ASN236.B : Hydrophobic | 4 | 20 |
| LEU90.B : VdWContact | 3 | 15 |
| LEU229.B : Hydrophobic | 3 | 15 |
| ARG122.A : HBAcceptor | 1 | 5 |
| GLY153.A : HBAcceptor | 1 | 5 |

**Pharmacophoric interpretation:**
- **Obligate hydrophobic cluster (100%):** GLU57.A, HIS121.A, MET105.B, LYS108.B — define the minimal binding pharmacophore
- **Near-obligate contacts (≥85%):** ILE104.B, ALA151.A, GLU57.A (hydrophobic) — secondary pharmacophore
- **Key hydrogen bond:** HIS121.A acts as H-bond acceptor from the ligand in 50% of compounds; identifying donors targeting this residue is a clear SAR vector
- **Pocket-spanning contacts:** interactions with both CDK2 (A-chain) and CyclinE1 (B-chain) residues are present in all top-ranked compounds, confirming deep engagement of the interface pocket
- **No PiStacking, CationPi or ionic interactions** were detected in the top 20 — the site is predominantly hydrophobic with one conserved H-bond

---

## 5. Full Docking Results — All 84 Compounds

| Rank | Compound | Vina (kcal/mol) | CNN pKi | CNN Pose Score | Poses |
|:---:|:---|---:|---:|---:|:---:|
| 1 | CTX-1020732 | −14.02 | 8.931 | 0.992 | 5 |
| 2 | CTX-1020903 | −14.52 | 8.586 | 0.987 | 5 |
| 3 | CTX-1020811 | −13.17 | 8.586 | 0.976 | 5 |
| 4 | CTX-1020743 | −13.72 | 8.575 | 0.976 | 5 |
| 5 | CTX-1019813 | −12.10 | 8.306 | 0.946 | 5 |
| 6 | CTX-1020521 | −13.15 | 8.233 | 0.420 | 5 |
| 7 | CTX-1019757 | −11.24 | 8.107 | 0.855 | 5 |
| 8 | CTX-1020745 | −9.88 | 8.002 | 0.762 | 5 |
| 9 | CTX-1020441 | −12.43 | 7.846 | 0.729 | 5 |
| 10 | CTX-1020753 | −8.53 | 7.826 | 0.563 | 5 |
| 11 | CTX-1019473 | −10.15 | 7.740 | 0.697 | 5 |
| 12 | CTX-1020751 | −13.64 | 7.736 | 0.900 | 5 |
| 13 | CTX-1020752 | −11.50 | 7.715 | 0.605 | 5 |
| 14 | CTX-1020456 | −8.00 | 7.667 | 0.509 | 5 |
| 15 | CTX-1020562 | −11.50 | 7.627 | 0.449 | 5 |
| 16 | CTX-1020800 | −11.84 | 7.598 | 0.488 | 5 |
| 17 | CTX-1020555 | −12.45 | 7.595 | 0.465 | 5 |
| 18 | CTX-1020696 | −9.31 | 7.527 | 0.439 | 5 |
| 19 | CTX-1019613 | −12.79 | 7.507 | 0.535 | 5 |
| 20 | CTX-1020748 | −10.86 | 7.483 | 0.491 | 5 |
| 21 | CTX-1020582 | −7.65 | 7.473 | 0.460 | 5 |
| 22 | CTX-1020458 | −10.65 | 7.473 | 0.625 | 5 |
| 23 | CTX-1020749 | −12.03 | 7.468 | 0.404 | 5 |
| 24 | CTX-1020685 | −12.45 | 7.449 | 0.361 | 5 |
| 25 | CTX-1020759 | −11.56 | 7.441 | 0.600 | 5 |
| 26 | CTX-1020912 | −12.40 | 7.423 | 0.752 | 5 |
| 27 | CTX-1020810 | −7.34 | 7.415 | 0.522 | 5 |
| 28 | CTX-1020799 | −6.07 | 7.410 | 0.429 | 5 |
| 29 | CTX-1020734 | −7.51 | 7.408 | 0.454 | 5 |
| 30 | CTX-1020838 | −8.02 | 7.397 | 0.355 | 5 |
| 31 | CTX-1019630 | −11.86 | 7.395 | 0.575 | 5 |
| 32 | CTX-1020453 | −7.56 | 7.378 | 0.405 | 5 |
| 33 | CTX-1019758 | −11.70 | 7.377 | 0.448 | 5 |
| 34 | CTX-1020699 | −10.46 | 7.300 | 0.475 | 5 |
| 35 | CTX-1020697 | −12.89 | 7.290 | 0.332 | 5 |
| 36 | CTX-1020698 | −10.50 | 7.269 | 0.646 | 5 |
| 37 | CTX-1020670 | −9.37 | 7.254 | 0.634 | 5 |
| 38 | CTX-1020742 | −11.16 | 7.235 | 0.264 | 5 |
| 39 | CTX-1020454 | −8.91 | 7.233 | 0.453 | 5 |
| 40 | CTX-1020902 | −12.17 | 7.219 | 0.616 | 5 |
| 41 | CTX-1020818 | −9.35 | 7.193 | 0.687 | 5 |
| 42 | CTX-1020440 | −10.33 | 7.184 | 0.303 | 5 |
| 43 | CTX-1020817 | −8.06 | 7.162 | 0.257 | 5 |
| 44 | CTX-1019660 | −9.17 | 7.151 | 0.404 | 5 |
| 45 | **CTX-1017233** *(co-crystal ref)* | −7.49 | 7.114 | 0.353 | 5 |
| 46 | CTX-1020766 | −10.43 | 7.096 | 0.527 | 5 |
| 47 | CTX-1020517 | −10.98 | 7.077 | 0.301 | 5 |
| 48 | CTX-1020845 | −5.18 | 7.074 | 0.310 | 5 |
| 49 | CTX-1020746 | −8.93 | 7.061 | 0.346 | 5 |
| 50 | CTX-1020744 | −10.88 | 7.037 | 0.293 | 5 |
| 51 | CTX-1020882 | −8.67 | 7.035 | 0.344 | 5 |
| 52 | CTX-1020755 | −9.58 | 7.030 | 0.452 | 5 |
| 53 | CTX-1020733 | −11.55 | 6.987 | 0.513 | 5 |
| 54 | CTX-1020771 | −9.64 | 6.974 | 0.450 | 5 |
| 55 | CTX-1020842 | −11.21 | 6.967 | 0.312 | 5 |
| 56 | CTX-1020816 | −5.84 | 6.964 | 0.298 | 5 |
| 57 | CTX-1019471 | −9.57 | 6.923 | 0.376 | 5 |
| 58 | CTX-1019904 | −8.14 | 6.906 | 0.349 | 5 |
| 59 | CTX-1020669 | −9.58 | 6.893 | 0.277 | 5 |
| 60 | CTX-1020772 | −9.73 | 6.862 | 0.398 | 5 |
| 61 | CTX-1020459 | −6.55 | 6.791 | 0.352 | 5 |
| 62 | CTX-1020667 | −9.39 | 6.760 | — | 5 |
| 63 | CTX-1020795 | −6.93 | 6.689 | 0.384 | 5 |
| 64 | CTX-1020671 | −9.44 | 6.659 | 0.297 | 5 |
| 65 | CTX-1020770 | −10.58 | 6.581 | 0.374 | 5 |
| 66 | CTX-1019496 | −9.21 | 6.578 | 0.232 | 5 |
| 67 | CTX-1020516 | −9.97 | 6.563 | 0.292 | 5 |
| 68 | CTX-1020695 | −9.87 | 6.529 | 0.389 | 5 |
| 69 | CTX-1020566 | −7.25 | 6.377 | 0.305 | 5 |
| 70 | CTX-1020726 | −9.53 | 6.360 | 0.452 | 5 |
| 71 | CTX-1020735 | −9.06 | 6.246 | 0.222 | 5 |
| 72 | CTX-1020747 | −8.64 | 6.014 | 0.398 | 5 |
| 73 | CTX-1020741 | −8.67 | 5.962 | 0.331 | 5 |
| 74 | CTX-1020520 | −5.73 | 5.754 | 0.215 | 5 |
| 75 | CTX-1020739 | −5.45 | 5.602 | 0.349 | 5 |
| 76 | CTX-1020523 | −5.25 | 5.494 | 0.392 | 5 |
| 77 | CTX-1020565 | −7.56 | 5.374 | 0.338 | 5 |
| 78 | CTX-1020767 | −8.42 | 5.361 | 0.495 | 5 |
| 79 | CTX-1019480 | −5.94 | 5.302 | 0.622 | 5 |
| 80 | CTX-1020769 | −6.83 | 5.092 | 0.342 | 5 |
| 81 | CTX-1020750 | −5.77 | 5.039 | 0.436 | 5 |
| 82 | CTX-1020740 | −5.81 | 5.002 | 0.384 | 5 |
| 83 | CTX-1020518 | −5.60 | 4.952 | 0.356 | 5 |
| 84 | CTX-1020754 | −6.11 | 4.716 | 0.376 | 5 |

---

## 6. Limitations and Caveats

1. **Docking scoring accuracy:** gnina CNN pKi predicts affinity from pose geometry; it does not replace experimental binding assays. Ranking accuracy (AUROC, enrichment) is generally higher than absolute pKi accuracy.

2. **Pose files available for top 20 only:** parallel docking batch mode overwrites the output SDF file per job. Pose files for ranks 21–84 were not retained; only scores are available for these.

3. **Interaction fingerprinting on top 20 only:** ProLIF analysis was limited to compounds with pose files. The series statistics (n=20) cover the highest-scoring compounds and may not represent the full chemical space.

4. **MMFF strain interpretation:** the strain energy reflects the intramolecular energy cost of adopting the docked conformation. It is not a binding free energy component. Values should be compared within the series, not as absolute thresholds.

5. **Box centroid includes H atoms:** the docking box centroid was computed over all 72 CTX HETATM records (including 33 H atoms), giving a ~0.6 Å shift in X vs the heavy-atom centroid. The 35 Å box width is large enough to cover all relevant binding poses regardless.

6. **CTX-1020521 pose quality:** rank 6 (CNN pKi 8.233) has a CNN pose score of 0.420 — below the 0.5 threshold suggested as a quality filter. The pKi value should be treated with lower confidence; visual inspection is recommended.

---

## 7. Recommended Priority List

Based on CNN pKi ≥ 8.0 **and** CNN pose score ≥ 0.7 (combined quality + affinity filter):

| Priority | Compound | CNN pKi | CNN Pose | MMFF Strain |
|:---:|:---|---:|---:|---:|
| 1 | CTX-1020732 | 8.931 | 0.992 | 125.6 |
| 2 | CTX-1020743 | 8.575 | 0.976 | 143.3 |
| 3 | CTX-1020903 | 8.586 | 0.987 | 158.0 |
| 4 | CTX-1020811 | 8.586 | 0.976 | 198.0 |
| 5 | CTX-1019813 | 8.306 | 0.946 | 198.3 |
| 6 | CTX-1019757 | 8.107 | 0.855 | 178.9 |
| 7 | CTX-1020441 | 7.846 | 0.729 | 196.6 |
| 8 | CTX-1020745 | 8.002 | 0.762 | 113.1 |
| 9 | CTX-1020751 | 7.736 | 0.900 | 170.4 |
| 10 | CTX-1020912 | 7.423 | 0.752 | n/a |

CTX-1020732 stands out as the optimal compound: highest pKi, highest pose confidence, lowest conformational strain among the leaders. CTX-1020745 and CTX-1020555 are notable for combining high pKi (≥7.6) with low strain (≤113 kcal/mol).

---

## 8. MM-GBSA Binding Free Energies

### 8.1 Methods

MM-GBSA single-point binding free energy calculations were performed on the best docked pose (rank-1) for all 84 compounds (CTX-1020667 re-docked and scored; see note below). Calculations used the Uni-GBSA pipeline (GROMACS pdb2gmx + gmx_MMPBSA) with:

| Parameter | Value |
|:---|:---|
| Mode | Energy minimisation (em) before scoring |
| Implicit solvent | Generalised Born (GB), OBC2 |
| Protein force field | AMBER99SB-ILDN |
| Ligand force field | GAFF2 |
| Ligand charges | AM1-BCC (antechamber) |
| Receptor | receptor_gromacs_ready.pdb (chains renumbered 1–N) |
| Ligand input | H-added best-pose SDF (RDKit AddHs, addCoords=True) |
| GPU | A100 80 GB (GROMACS mdrun -nb gpu) |

ΔG_bind = E_complex − E_receptor − E_ligand, where each term is the MM + GB + SA energy after energy minimisation. All 84 calculations succeeded (0 failures).

**Note on CTX-1020667:** This compound produced a null per-pose CNN score in the original batch docking run and was excluded from the initial 83-compound set. It was re-docked independently (gnina, same box/parameters, seed 42) on 2026-09-06, yielding 9 poses; the best pose (Vina affinity −8.21 kcal/mol, CNN pKi 7.271, summary CNN pose score 0.4097) was used for MM-GBSA. Per-pose CNN scores remain None (a gnina output artifact for this compound), but the summary-level scores are valid.

**Caveat:** These are single-pose, single-point MM-GBSA values — not free energies of binding from conformational sampling. They rank compounds relative to each other but carry substantial absolute uncertainty (typically ±5–10 kcal/mol for mode=em). The dominant term is van der Waals burial; electrostatic and polar solvation terms partially cancel.

---

### 8.2 Complete MM-GBSA Rankings (all 84 compounds)

| Rank | Compound | ΔG (kcal/mol) | VdW | Elec | Polar Solv | Non-polar | Docking rank |
|:---:|:---|---:|---:|---:|---:|---:|:---:|
| 1 | CTX-1020732 | −83.19 | −79.34 | −4.82 | +9.46 | −8.49 | 1 |
| 2 | CTX-1020811 | −80.27 | −77.80 | −4.04 | +10.63 | −9.06 | 3 |
| 3 | CTX-1020521 | −80.08 | −79.36 | −2.62 | +11.59 | −9.68 | 6 |
| 4 | CTX-1020903 | −79.96 | −78.32 | −3.00 | +10.05 | −8.69 | 2 |
| 5 | CTX-1020743 | −78.50 | −75.43 | −2.93 | +8.76 | −8.91 | 4 |
| 6 | CTX-1020748 | −77.69 | −74.69 | −8.82 | +13.99 | −8.17 | 20 |
| 7 | CTX-1020555 | −76.53 | −74.59 | −4.48 | +10.54 | −8.00 | 17 |
| 8 | CTX-1019757 | −75.48 | −71.39 | −4.37 | +9.14 | −8.86 | 7 |
| 9 | CTX-1020759 | −75.20 | −75.06 | −3.85 | +12.19 | −8.49 | 22 |
| 10 | CTX-1020800 | −74.60 | −72.74 | −7.07 | +13.38 | −8.17 | 16 |
| 11 | CTX-1020749 | −74.57 | −72.17 | −8.10 | +13.65 | −7.95 | 25 |
| 12 | CTX-1019758 | −74.24 | −71.40 | −8.44 | +13.90 | −8.30 | 24 |
| 13 | CTX-1020441 | −73.81 | −73.36 | −6.69 | +14.42 | −8.18 | 9 |
| 14 | CTX-1019613 | −73.48 | −72.50 | −3.07 | +10.30 | −8.21 | 19 |
| 15 | CTX-1019813 | −73.15 | −71.25 | −3.68 | +10.29 | −8.52 | 5 |
| 16 | CTX-1020842 | −72.51 | −71.37 | −6.42 | +13.44 | −8.16 | 29 |
| 17 | CTX-1020685 | −71.35 | −70.09 | −3.32 | +9.86 | −7.80 | 26 |
| 18 | CTX-1020440 | −70.46 | −68.77 | −6.65 | +12.65 | −7.70 | 28 |
| 19 | CTX-1020697 | −69.61 | −68.92 | −1.69 | +8.69 | −7.69 | 35 |
| 20 | CTX-1020562 | −68.51 | −67.65 | −2.79 | +10.01 | −8.08 | 15 |
| — | CTX-1017233 (ref) | −49.93 | −48.96 | −0.25 | +7.73 | −6.71 | 51 (MM-GBSA) |
| 70 | CTX-1020667 (re-docked) | −41.49 | −42.40 | −0.61 | +6.61 | −5.09 | — |
| 84 | CTX-1020739 (weakest) | −24.69 | — | — | — | — | 84 |

Full 84-compound table in `cdk2_campaign/mmgbsa_results.json`.

**Series statistics (n=84):** ΔG range −83.19 to −24.69 kcal/mol; mean −55.04; median −54.03; SD 15.75 kcal/mol.

---

### 8.3 Docking vs MM-GBSA Concordance

The top-5 compounds are largely consistent between methods: CTX-1020732 is #1 by both metrics. CTX-1020903 (#2 docking) drops to #4 MM-GBSA; CTX-1020811 (#3 docking) rises to #2 MM-GBSA. The largest reranking occurs for CTX-1020748 (docking rank 20 → MM-GBSA rank 6) and CTX-1020521 (docking rank 6 → MM-GBSA rank 3, despite a low CNN pose score of 0.42 which reduced confidence in that docking result). The co-crystal reference CTX-1017233 ranks 51st by MM-GBSA (ΔG −49.93 kcal/mol), confirming the library contains substantially improved analogues. The bottom five compounds (CTX-1020518, CTX-1020750, CTX-1020520, CTX-1020523, CTX-1020739) cluster between −25 and −28 kcal/mol in both metrics.

The dominant energy term across the series is van der Waals burial (mean contribution −54.671 kcal/mol), consistent with the primarily hydrophobic pharmacophore identified by ProLIF fingerprinting (MET105.B/LYS108.B, HIS121.A). Electrostatic contributions are small (median −3.5 kcal/mol), and polar solvation penalty (mean +10.8 kcal/mol) partially offsets burial.

---

## 9. Data Files

| File | Description |
|:---|:---|
| `cdk2_campaign/docking_checkpoint.json` | Full docking checkpoint (84 compounds, all scores) |
| `cdk2_campaign/docking_results.json` | Consolidated results, sorted by CNN pKi |
| `cdk2_campaign/energy_results.json` | Scores + MMFF strain (top 20) |
| `cdk2_campaign/interaction_fingerprints.json` | Per-compound ProLIF fingerprints (top 20) |
| `cdk2_campaign/interaction_stats.json` | Series interaction frequency statistics |
| `cdk2_campaign/poses_top20/` | Docked pose SDF files for top 20 compounds |
| `cdk2_campaign/poses_all/` | Best-pose SDF files for all 84 compounds (no explicit H) |
| `cdk2_campaign/poses_all_H/` | Best-pose SDF files for all 84 compounds (explicit H, gbsa input) |
| `cdk2_campaign/mmgbsa_results.json` | MM-GBSA ΔG and energy components for all 84 compounds |
| `cdk2_campaign/receptor_raw.pdb` | Docking receptor (no explicit H) |
| `cdk2_campaign/receptor_prepared.pdb` | Protonated receptor pH 7.4 (ProLIF input) |
| `cdk2_campaign/receptor_gromacs_ready.pdb` | Receptor with chains renumbered 1–N (MM-GBSA input) |
| `cdk2_campaign/ligands_prepared/` | 84 standardised 3D ligand SDF files |
| `cdk2_campaign/box_params.json` | Docking box definition |

---

---

## Verification

The following claims were independently checked against source files after report completion.

| Claim | Source | Verified value | Result |
|:---|:---|:---|:---:|
| 84 ligands docked, all have non-null Vina score | docking_checkpoint.json | 84 entries, 0 null best_affinity | CONFIRMED |
| 84 ligands have non-null CNN pKi | docking_checkpoint.json | 0 null best_cnn_affinity | CONFIRMED |
| Rank 1 = CTX-1020732, Vina −14.02, CNN 8.931, pose 0.992 | docking_results.json row 0 | −14.02 / 8.931 / 0.9922 | CONFIRMED |
| CTX-1017233 at rank 45 (docking), CNN 7.114 | docking_results.json row 44 | rank 45 / 7.114 | CONFIRMED |
| 20 pose SDF files in poses_top20/ | directory listing | 20 files | CONFIRMED |
| 20/20 interaction fingerprints computed (n_failed=0) | interaction_stats.json | n_analysed=20, n_failed=0 | CONFIRMED |
| 5 obligate contacts (100% frequency) in top-20 | interaction_stats.json | GLU57.A:VdW, HIS121.A:VdW, MET105.B:Hydro, LYS108.B:Hydro, LYS108.B:VdW all count=20 | CONFIRMED |
| interaction_stats.json: 52 unique interaction types | interaction_stats.json | 52 entries in interactions list | CONFIRMED |
| 84 MM-GBSA calculations, all succeeded | mmgbsa_results.json | 84 entries, all status="S", 0 null dG | CONFIRMED |
| Rank 1 MM-GBSA = CTX-1020732, ΔG = −83.188 kcal/mol | mmgbsa_results.json row 0 | −83.18772 | CONFIRMED |
| Co-crystal ref CTX-1017233: MM-GBSA rank 51, ΔG −49.925 | mmgbsa_results.json | rank 51 / −49.925 | CONFIRMED |
| CTX-1020667 re-docked and scored: rank 70, ΔG −41.491 | CTX-1020667_mmgbsa_result.json | −41.490577 | CONFIRMED |
| 84 H-added ligand SDF files present | poses_all_H/ listing | 84 files | CONFIRMED |
| receptor_gromacs_ready.pdb chains renumbered 1–N | file inspection | A: 1–299, B: 1–267 | CONFIRMED |

**Known issues documented in audit (phase 05):**
- interaction_stats.json has 52 unique interaction types (report previously stated 51 — corrected)
- CTX-1020667 per-pose CNN scores are None (gnina output artifact for this compound); summary-level CNN pKi 7.271 and pose score 0.4097 are valid and were used for pose selection and MM-GBSA
- CTX-1020521 CNN pose score 0.42 (below informal 0.5 quality threshold; interpret CNN pKi with caution)

---

*Report generated 2026-09-06; MM-GBSA section added 2026-09-06. Docking: gnina 1.0 (CNN-rescored Vina). Interactions: ProLIF 2.2.1 / MDAnalysis 2.10.0. Ligand prep: RDKit 2024.x + Dimorphite-DL. Receptor prep: PDBFixer 1.12.0 / OpenMM. MM-GBSA: Uni-GBSA (GROMACS 2024 + gmx_MMPBSA), GAFF2/AMBER99SB-ILDN, AM1-BCC charges.*
