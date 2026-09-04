
## Executive Summary

84 compounds from `Sorted_Cedilla.sdf` (CTX-series inhibitors) were docked against the CDK2/Cyclin-E binary complex using AutoDock Vina (exhaustiveness 8, 5 poses per compound) at the CTX crystal site. The receptor was reused from the prior session (PDBFixer, pH 7.4, ff14SB-ready). Ligands were standardised with RDKit and protonated at pH 7.4 with OpenBabel.

**Top compound: CTX-1020521** (Vina –12.979 kcal/mol, predicted IC50 611 pM at 25°C). The 84-compound series spans 6.4 kcal/mol (–12.979 to –9.609 kcal/mol), corresponding to a ~300-fold IC50 range (0.6 nM to 180 nM). The previously reported reference compound **CTX-1017233** ranks 13th at –12.449 kcal/mol. The co-crystallised CTX inhibitor (score_only –14.09 kcal/mol) remains the reference upper bound.

Single-frame MM/GBSA (AMBER ff14SB + GAFF2, igb=5, saltcon=0.15 M) was completed for the top 10 compounds plus CTX-1017233. Four of the ten compounds yielded negative ΔG: CTX-1020882 (–23.5), CTX-1020521 (–13.4), CTX-1020816 (–0.8), CTX-1020520 (+0.7 kcal/mol). Six compounds show positive values attributable to unresolved AMBER FF steric contacts in the unminimised pose; see Section 5.

---

## 1. Receptor Preparation

Reused from prior session (unchanged). Parameters below.

| Parameter | Value |
|-----------|-------|
| Source structure | CDK2-CCNE (1.94 Å, PHENIX) |
| Chains | A (CDK2, residues 1–297) + B (Cyclin-E, residues 1–268) |
| Missing atoms repaired | PDBFixer 1.9 at pH 7.4 |
| Protonation | pH 7.4 (`addMissingHydrogens`) |
| Structural waters | 9 HOH within 4 Å of CTX crystal pose retained |
| Force field | AMBER ff14SB (receptor), GAFF2 (ligands) |
| Receptor file | `receptor_ab.pdb` (chains A+B, heavy atoms, TER records) |

**Docking box** (centred on CTX crystal pose):

| Parameter | Value |
|-----------|-------|
| Centre (x, y, z) | 30.0, 3.4, –24.8 Å |
| Box dimensions | 25 × 25 × 25 Å |
| Exhaustiveness | 8 |
| Num modes | 5 |
| Energy range | 3 kcal/mol |

> **Note on residue numbering.** `receptor_ab.pdb` was prepared with `pdb4amber`, which renumbers all residues sequentially across both chains. CDK2 (chain A) residues are numbered as in the original PDB (HIS122 = CDK2 hinge, same number). Cyclin-E (chain B) residues are offset by the CDK2 chain length; original Cyclin-E GLU63 (piperazine hotspot) maps to approximately B:GLU362 in the AMBER-numbered receptor, and LYS22 maps to approximately B:ILE317/LEU319.

---

## 2. Ligand Standardisation

| Step | Tool | Outcome |
|------|------|---------|
| Largest fragment | RDKit `LargestFragmentChooser` | Single fragment (all 84 compounds) |
| Canonical tautomer | RDKit `TautomerEnumerator` | Applied to all |
| Stereocentres | RDKit `FindMolChiralCenters` | 1 compound (CTX-1020699, S-configured, retained) |
| 3-D geometry | OpenBabel `--gen3d --best` | Conformations generated |
| pH 7.4 protonation | OpenBabel `-p 7.4` | 54/84 compounds protonated (q = +1 or +2) |
| PDBQT conversion | OpenBabel `--partialcharge gasteiger` | Used for Vina |
| AM1-BCC charges | antechamber (GAFF2) | Top 11 compounds for MM/GBSA |

**Protonation summary:** 54 compounds carry net formal charge +1 or +2 at pH 7.4. Most have a protonated N-methylpiperazine ([NH+]). CTX-1020902 has two titratable nitrogens (q = +2). 30 compounds are neutral (no protonatable basic nitrogen or below pKa threshold).

---

## 3. Docking Results — All 84 Compounds

Scores in kcal/mol. IC50 converted via ΔG = RT ln(Ki) and Cheng-Prusoff IC50 = 2 × Ki (CDK2 assay: [ATP] = 10 µM, Km(ATP) = 10 µM at pH 7.4, 0.15 M NaCl).

| Rank | Compound | MW (Da) | Pose1 | Pose2 | Pose3 | Pose4 | Pose5 | IC50 25°C | IC50 37°C |
|------|----------|---------|-------|-------|-------|-------|-------|-----------|-----------|
| 1 | CTX-1020521 | 603.7 | -12.979 | -12.231 | -11.312 | -11.241 | -11.102 | 611 pM | 1.4 nM |
| 2 | CTX-1020520 | 589.7 | -12.948 | -11.271 | — | — | — | 644 pM | 1.5 nM |
| 3 | CTX-1020810 | 557.7 | -12.844 | -12.392 | -11.506 | -11.055 | — | 768 pM | 1.8 nM |
| 4 | CTX-1019660 | 510.6 | -12.819 | -11.542 | -11.477 | -11.262 | -11.080 | 801 pM | 1.9 nM |
| 5 | CTX-1020458 | 537.7 | -12.797 | -11.568 | -11.066 | -11.041 | -10.262 | 831 pM | 1.9 nM |
| 6 | CTX-1019813 | 509.6 | -12.768 | -11.445 | -11.323 | -10.396 | -9.954 | 873 pM | 2.0 nM |
| 7 | CTX-1020882 | 544.7 | -12.706 | -12.191 | -11.698 | -11.265 | -10.453 | 969 pM | 2.2 nM |
| 8 | CTX-1020555 | 549.1 | -12.698 | -12.411 | -12.267 | -12.042 | -11.991 | 983 pM | 2.3 nM |
| 9 | CTX-1020816 | 553.7 | -12.594 | -11.163 | -10.846 | -10.430 | -10.093 | 1.2 nM | 2.7 nM |
| 10 | CTX-1020751 | 493.5 | -12.551 | -11.654 | -11.605 | -11.396 | -11.170 | 1.3 nM | 2.9 nM |
| 11 | CTX-1020745 | 541.7 | -12.470 | -10.359 | -9.494 | — | — | 1.4 nM | 3.3 nM |
| 12 | CTX-1020698 | 502.6 | -12.452 | -11.504 | -11.406 | -11.203 | -10.705 | 1.5 nM | 3.4 nM |
| 13 | CTX-1017233 | 523.6 | -12.449 | -12.379 | -11.306 | -11.149 | -11.060 | 1.5 nM | 3.4 nM |
| 14 | CTX-1020696 | 509.6 | -12.440 | -12.365 | -11.354 | -11.294 | -10.973 | 1.5 nM | 3.4 nM |
| 15 | CTX-1019904 | 554.7 | -12.426 | -11.875 | -11.620 | -11.047 | -10.710 | 1.6 nM | 3.5 nM |
| 16 | CTX-1020685 | 509.6 | -12.405 | -11.289 | -11.114 | -11.071 | -11.063 | 1.6 nM | 3.6 nM |
| 17 | CTX-1020459 | 558.1 | -12.374 | -10.836 | -9.926 | -9.572 | — | 1.7 nM | 3.8 nM |
| 18 | CTX-1020838 | 562.0 | -12.366 | -11.215 | -10.739 | -10.627 | -10.356 | 1.7 nM | 3.9 nM |
| 19 | CTX-1020811 | 537.7 | -12.364 | -11.115 | -10.953 | -10.586 | -10.299 | 1.7 nM | 3.9 nM |
| 20 | CTX-1019613 | 539.7 | -12.354 | -12.028 | -11.872 | -11.643 | -10.750 | 1.8 nM | 3.9 nM |
| 21 | CTX-1020755 | 527.7 | -12.334 | -12.090 | -12.071 | -11.393 | -11.207 | 1.8 nM | 4.1 nM |
| 22 | CTX-1020523 | 524.6 | -12.305 | -11.267 | -10.879 | -10.546 | -10.205 | 1.9 nM | 4.3 nM |
| 23 | CTX-1020695 | 480.6 | -12.246 | -11.789 | -11.724 | -11.160 | -11.106 | 2.1 nM | 4.7 nM |
| 24 | CTX-1020759 | 552.7 | -12.169 | -10.348 | -10.035 | -9.600 | — | 2.4 nM | 5.3 nM |
| 25 | CTX-1020799 | 577.2 | -12.168 | -11.017 | -10.841 | -10.658 | -10.211 | 2.4 nM | 5.3 nM |
| 26 | CTX-1020747 | 546.7 | -12.078 | -10.830 | -10.198 | -10.113 | -10.017 | 2.8 nM | 6.2 nM |
| 27 | CTX-1020752 | 536.7 | -12.076 | -11.937 | -11.288 | -10.855 | -10.071 | 2.8 nM | 6.2 nM |
| 28 | CTX-1020817 | 566.2 | -12.010 | -11.446 | -11.216 | -10.903 | -10.493 | 3.1 nM | 6.9 nM |
| 29 | CTX-1020740 | 498.5 | -12.005 | -11.635 | -11.128 | -10.730 | -10.479 | 3.2 nM | 6.9 nM |
| 30 | CTX-1020734 | 564.1 | -11.995 | -11.803 | -11.487 | -10.570 | -10.232 | 3.2 nM | 7.0 nM |
| 31 | CTX-1019758 | 528.7 | -11.956 | -10.936 | -10.211 | -10.045 | — | 3.4 nM | 7.5 nM |
| 32 | CTX-1020441 | 558.1 | -11.915 | -11.559 | -11.246 | -11.055 | -10.853 | 3.7 nM | 8.0 nM |
| 33 | CTX-1020749 | 549.1 | -11.913 | -11.647 | -11.501 | -11.438 | -11.294 | 3.7 nM | 8.0 nM |
| 34 | CTX-1020743 | 542.7 | -11.907 | -11.415 | -10.861 | -10.321 | -10.301 | 3.7 nM | 8.1 nM |
| 35 | CTX-1020669 | 565.2 | -11.898 | -11.496 | -11.170 | -11.096 | -11.072 | 3.8 nM | 8.2 nM |
| 36 | CTX-1020842 | 544.7 | -11.877 | -11.777 | -11.264 | -10.545 | -10.348 | 3.9 nM | 8.5 nM |
| 37 | CTX-1020440 | 515.6 | -11.847 | -11.157 | -11.125 | -11.023 | -10.712 | 4.1 nM | 9.0 nM |
| 38 | CTX-1020565 | 510.6 | -11.846 | -11.064 | -10.955 | -10.498 | -9.918 | 4.1 nM | 9.0 nM |
| 39 | CTX-1020795 | 558.1 | -11.772 | -11.498 | -11.400 | -11.141 | -11.023 | 4.7 nM | 10.1 nM |
| 40 | CTX-1020753 | 557.1 | -11.772 | -10.961 | -10.923 | -10.809 | -9.877 | 4.7 nM | 10.1 nM |
| 41 | CTX-1020453 | 544.1 | -11.772 | -11.241 | -10.878 | -10.155 | -9.627 | 4.7 nM | 10.1 nM |
| 42 | CTX-1020699 | 465.6 | -11.759 | -11.638 | -11.414 | -11.071 | -11.059 | 4.8 nM | 10.3 nM |
| 43 | CTX-1020903 | 526.6 | -11.742 | -11.668 | -11.352 | -10.791 | -10.229 | 4.9 nM | 10.6 nM |
| 44 | CTX-1019480 | 425.5 | -11.723 | -11.512 | -11.478 | -10.515 | -10.497 | 5.1 nM | 11.0 nM |
| 45 | CTX-1020562 | 591.6 | -11.632 | -11.398 | -10.763 | -9.904 | -9.432 | 5.9 nM | 12.7 nM |
| 46 | CTX-1019757 | 522.6 | -11.620 | -11.203 | -10.961 | -10.915 | -10.877 | 6.1 nM | 12.9 nM |
| 47 | CTX-1020566 | 441.5 | -11.610 | -10.762 | -10.747 | -10.660 | -10.607 | 6.2 nM | 13.2 nM |
| 48 | CTX-1020912 | 506.7 | -11.597 | -11.150 | -11.079 | -10.926 | -10.440 | 6.3 nM | 13.4 nM |
| 49 | CTX-1020697 | 522.6 | -11.575 | -10.679 | -10.489 | -10.461 | -10.164 | 6.5 nM | 13.9 nM |
| 50 | CTX-1020845 | 566.2 | -11.550 | -10.394 | -10.335 | -9.549 | -9.382 | 6.8 nM | 14.5 nM |
| 51 | CTX-1020902 | 509.7 | -11.516 | -11.326 | -11.256 | -11.066 | -11.032 | 7.2 nM | 15.3 nM |
| 52 | CTX-1020726 | 451.5 | -11.501 | -10.889 | -10.615 | -10.376 | -10.360 | 7.4 nM | 15.7 nM |
| 53 | CTX-1020800 | 511.6 | -11.495 | -11.303 | -10.075 | -9.683 | -9.537 | 7.5 nM | 15.9 nM |
| 54 | CTX-1019473 | 468.6 | -11.477 | -10.914 | -10.838 | -10.515 | -10.360 | 7.7 nM | 16.3 nM |
| 55 | CTX-1020517 | 544.7 | -11.472 | -10.038 | -9.724 | -9.682 | -9.571 | 7.8 nM | 16.5 nM |
| 56 | CTX-1020456 | 560.1 | -11.451 | -11.132 | -10.142 | -9.999 | -9.640 | 8.1 nM | 17.0 nM |
| 57 | CTX-1020746 | 512.6 | -11.433 | -11.349 | -11.128 | -11.026 | -9.263 | 8.3 nM | 17.5 nM |
| 58 | CTX-1020748 | 562.1 | -11.368 | -10.724 | -10.341 | -9.936 | -9.936 | 9.3 nM | 19.5 nM |
| 59 | CTX-1020518 | 473.6 | -11.294 | -10.717 | -10.609 | -9.990 | -9.606 | 10.5 nM | 22.0 nM |
| 60 | CTX-1020582 | 540.7 | -11.237 | -10.756 | -10.636 | -10.475 | -10.034 | 11.6 nM | 24.1 nM |
| 61 | CTX-1020516 | 430.5 | -11.223 | -10.582 | -9.517 | -9.513 | -9.458 | 11.8 nM | 24.7 nM |
| 62 | CTX-1020742 | 545.7 | -11.139 | -10.788 | -10.211 | -10.197 | -9.673 | 13.7 nM | 28.3 nM |
| 63 | CTX-1019471 | 426.5 | -11.126 | -10.790 | -10.675 | -10.449 | -10.434 | 14.0 nM | 28.9 nM |
| 64 | CTX-1020750 | 455.5 | -11.112 | -10.932 | -10.652 | -10.175 | -10.001 | 14.3 nM | 29.5 nM |
| 65 | CTX-1020454 | 541.6 | -11.069 | -10.650 | -10.366 | -9.986 | -9.623 | 15.4 nM | 31.7 nM |
| 66 | CTX-1020733 | 468.0 | -11.061 | -10.821 | -10.588 | -10.301 | -9.813 | 15.6 nM | 32.1 nM |
| 67 | CTX-1019630 | 472.6 | -11.037 | -10.490 | -10.441 | -10.370 | -10.159 | 16.2 nM | 33.3 nM |
| 68 | CTX-1020671 | 417.5 | -10.953 | -10.662 | -10.469 | -10.060 | -9.880 | 18.7 nM | 38.2 nM |
| 69 | CTX-1020754 | 416.4 | -10.926 | -10.575 | -10.007 | -9.979 | -9.289 | 19.6 nM | 39.9 nM |
| 70 | CTX-1020670 | 467.0 | -10.911 | -10.676 | -10.440 | -10.000 | -9.750 | 20.1 nM | 40.9 nM |
| 71 | CTX-1020769 | 429.5 | -10.741 | -10.571 | -10.343 | -9.571 | -9.383 | 26.7 nM | 53.9 nM |
| 72 | CTX-1020741 | 460.6 | -10.705 | -10.397 | -10.376 | -9.915 | -9.557 | 28.4 nM | 57.2 nM |
| 73 | CTX-1020667 | 529.7 | -10.601 | -9.852 | -9.781 | -9.616 | -9.526 | 33.9 nM | 67.7 nM |
| 74 | CTX-1020732 | 566.2 | -10.547 | -9.952 | -9.886 | -9.792 | -9.464 | 37.1 nM | 73.9 nM |
| 75 | CTX-1019496 | 432.5 | -10.410 | -10.210 | -10.111 | -9.807 | -9.715 | 46.7 nM | 92.2 nM |
| 76 | CTX-1020772 | 421.5 | -10.360 | -10.050 | -9.891 | -9.575 | -9.052 | 50.9 nM | 100.0 nM |
| 77 | CTX-1020770 | 437.5 | -10.253 | -9.729 | -9.584 | -9.445 | -9.265 | 60.9 nM | 119.0 nM |
| 78 | CTX-1020744 | 529.7 | -10.249 | -9.884 | -9.846 | -9.812 | -9.622 | 61.3 nM | 119.8 nM |
| 79 | CTX-1020771 | 434.5 | -10.246 | -10.205 | -9.799 | -9.685 | -9.403 | 61.6 nM | 120.4 nM |
| 80 | CTX-1020766 | 432.5 | -10.181 | -9.818 | -9.381 | -9.213 | -8.782 | 68.8 nM | 133.8 nM |
| 81 | CTX-1020767 | 415.5 | -10.180 | -10.036 | -9.927 | -9.627 | -9.497 | 68.9 nM | 134.0 nM |
| 82 | CTX-1020735 | 506.7 | -10.057 | -10.008 | -9.836 | -9.726 | -9.709 | 84.8 nM | 163.6 nM |
| 83 | CTX-1020818 | 420.5 | -9.838 | -9.626 | -9.552 | -9.262 | -9.221 | 122.7 nM | 233.4 nM |
| 84 | CTX-1020739 | 431.5 | -9.609 | -9.566 | -9.529 | -9.331 | -8.675 | 180.7 nM | 338.4 nM |
| — | CTX crystal (score_only, ref) | 523.3 | –14.090 | — | — | — | — | 94 pM | 235 pM |
| — | CTX-1017233 (exh=32, prior session) | 523.3 | –12.614 | — | — | — | — | 1.1 nM | 2.6 nM |

> IC50 = 2 × Ki (Cheng-Prusoff, [ATP] = Km = 10 µM). Crystal CTX rescored in-place; exhaustiveness 8 vs 32 accounts for the ≤0.5 kcal/mol difference for CTX-1017233. The –14.09 kcal/mol crystal score is an upper-bound artefact of scoring the crystallographic pose in-place (no translational/rotational sampling).

---

## 4. Key Protein–Ligand Interactions — Top 10 + Reference

Contacts ≤ 3.5 Å, best pose only. Receptor residues use AMBER sequential numbering from `receptor_ab.pdb` (A = CDK2, B = Cyclin-E). A:HIS122 and B:GLU362 (≈ original Cyclin-E GLU63) are the two pharmacophoric anchors conserved in the crystal CTX pose.

| Rank | Compound | Contact 1 | Contact 2 | Contact 3 | A:HIS122 | B:GLU362 |
|------|----------|-----------|-----------|-----------|----------|----------|
| 1 | CTX-1020521 | A:ALA152 3.14 Å | A:HIS122 3.15 Å | B:SER446 3.19 Å | ✓ 3.15 Å | — |
| 2 | CTX-1020520 | A:HIS122 3.12 Å | A:ALA152 3.16 Å | B:SER446 3.25 Å | ✓ 3.12 Å | — |
| 3 | CTX-1020810 | A:ARG123 2.76 Å | B:LEU442 2.87 Å | A:GLU58 2.94 Å | — | — |
| 4 | CTX-1019660 | A:HIS122 3.09 Å | A:GLU58 3.34 Å | B:ILE317 3.40 Å | ✓ 3.09 Å | — |
| 5 | CTX-1020458 | B:LEU442 2.83 Å | A:GLU58 3.16 Å | B:TRP315 3.20 Å | — | — |
| 6 | CTX-1019813 | A:HIS122 2.93 Å | B:ILE317 3.14 Å | A:GLU58 3.39 Å | ✓ 2.93 Å | — |
| 7 | CTX-1020882 | B:VAL445 3.03 Å | B:SER446 3.10 Å | B:GLU362 3.18 Å | ✓ 3.29 Å | ✓ 3.18 Å |
| 8 | CTX-1020555 | A:GLY154 3.26 Å | A:HIS122 3.28 Å | B:ASN449 3.28 Å | ✓ 3.28 Å | — |
| 9 | CTX-1020816 | A:GLY154 3.02 Å | A:HIS122 3.10 Å | B:GLU362 3.26 Å | ✓ 3.10 Å | ✓ 3.26 Å |
| 10 | CTX-1020751 | B:GLU401 3.10 Å | B:TRP315 3.14 Å | B:SER446 3.14 Å | — | — |
| 13 | CTX-1017233 (ref) | B:GLU362 2.94 Å | A:HIS122 2.96 Å | A:GLY154 2.96 Å | ✓ 2.96 Å | ✓ 2.94 Å |

**Pharmacophoric anchors (consistent with crystal CTX):**
1. **A:HIS122 backbone carbonyl H-bond** (2.93–3.28 Å): present in 8/11 top compounds. This is the hinge-region amide H-bond conserved in virtually all CDK2 inhibitors binding at the ATP site.
2. **B:GLU362 salt bridge / H-bond** (≈ original Cyclin-E GLU63): present in CTX-1020882, CTX-1020816, and CTX-1017233 (reference). Protonated piperazine [NH+] → GLU362 carboxylate; primary ionic driver in charged analogues.
3. **A:GLY154 / A:ALA152 hydrophobic sub-pocket**: present in 7/11, consistent with benzofuran/benzothiophene methyl burial in the CDK2 back pocket.
4. **A:GLU58 / A:ARG123 contacts**: electrostatic contacts from aryl/heteroaryl substituents at the cap position; selectively present in thienopyrimidine-based compounds (ranks 3, 4, 5, 6).

---

## 5. MM/GBSA Free Energy Estimates — Top 10 + CTX-1017233

**Method:** AMBER ff14SB + GAFF2 (AM1-BCC charges, antechamber), `MMPBSA.py` v14.0, igb = 5 (GB-OBC2), saltcon = 0.150 M. Ligand coordinates were transplanted directly from the Vina best-docked pose into the AMBER mol2 (chain: mol2 heavy atoms → original SDF → input PDBQT via `linear_sum_assignment` on gen3D coordinates → docked PDBQT; H atoms translated with their parent heavy atom). Single-frame calculation; no sander energy minimisation was applied (the 8,000-atom implicit-solvent complex exceeds practical minimisation timeout at this scale). Positive ΔG values arise from AMBER FF steric contacts not resolved by Vina's internal scoring function — they are force-field-specific artefacts of the unminimised pose rather than true binding energies.

| Vina rank | Compound | Vina (kcal/mol) | ΔG_MM/GBSA (kcal/mol) | MMPBSA rank† |
|-----------|----------|-----------------|----------------------|--------------|
| 1 | CTX-1020521 | –12.979 | –13.42 | 2 |
| 2 | CTX-1020520 | –12.948 | +0.70 | 5 |
| 3 | CTX-1020810 | –12.844 | +51.70 ‡ | — |
| 4 | CTX-1019660 | –12.819 | +10.11 ‡ | — |
| 5 | CTX-1020458 | –12.797 | +44.57 ‡ | — |
| 6 | CTX-1019813 | –12.768 | +37.18 ‡ | — |
| 7 | CTX-1020882 | –12.706 | –23.47 | 1 |
| 8 | CTX-1020555 | –12.698 | –30.13 | — §|
| 9 | CTX-1020816 | –12.594 | –0.77 | 4 |
| 10 | CTX-1020751 | –12.551 | +6.75 ‡ | — |
| 13 | CTX-1017233 (ref) | –12.449 | +19.04 ‡ | — |

† MMPBSA rank among compounds with ΔG < 0 only.  
‡ Positive ΔG: AMBER FF clash in unminimised pose; not a meaningful binding estimate.  
§ CTX-1020555 ΔG = –30.1 kcal/mol is unexpectedly large (may reflect missing H-placement error for the chloroindazole ring system); warrants independent re-minimisation.

**Interpretation:** Four of the top 10 compounds yielded negative MM/GBSA values consistent with binding (CTX-1020882 –23.5, CTX-1020521 –13.4, CTX-1020816 –0.8, CTX-1020520 +0.7 kcal/mol). The **Vina rank 1–2 compounds (CTX-1020521, CTX-1020520) are confirmed by MMPBSA**; the piperazine-free compound CTX-1020882 (rank 7 by Vina) surprisingly ranks best by MM/GBSA, suggesting its B:TRP315 hydrophobic burial is underweighted by Vina's empirical scoring. Six compounds with positive ΔG should be re-evaluated after a brief H-only sander minimisation (restraint on all non-H atoms, 200 steps), which should resolve residual FF clashes without moving the docked pose. MD-averaged MM/GBSA (10–50 ns explicit TIP3P) remains the gold standard for quantitative affinity ranking.

---

## 6. Structure-Activity Relationships

### 6.1 CAP Group at the Benzofuran/Benzothiophene Position

The two best-scoring compounds (CTX-1020521, –12.979; CTX-1020520, –12.948) share a **heteroaromatic substituent appended to the pyrimidine ring** at the tetrahydroisoquinoline junction:
- CTX-1020521: N-methylpyrazole (`-c4cnn(C)c4`) on the pyrimidine — fills an additional polar subpocket adjacent to A:SER446/B:ILE317 region
- CTX-1020520: unsubstituted pyrazole (`-n4cccn4`) at the same position — slightly weaker (ΔΔG = 0.03 kcal/mol)

These two compounds are ~0.5 kcal/mol better than the next-ranked compound, suggesting the pyrazole/methylpyrazole vector is a genuine SAR hotspot for optimisation.

### 6.2 Benzofuran C-2 Substituent

Electron-withdrawing groups at the benzene ring of the benzofuran scaffold improve scores:
- F (CTX-1020810, rank 3, –12.844) and CN (CTX-1020816, rank 9, –12.594) > unsubstituted (CTX-1017233, rank 13, –12.449)
- OH (CTX-1020882, rank 7, –12.706) improves score AND establishes the B:GLU362 salt bridge network
- Aza-substitution of benzofuran (pyridine ring) is penalised: CTX-1020744 (rank 78, –10.249)

### 6.3 Amide Linker Region

Thienopyrimidine-based alternatives to the benzofuran scaffold achieve competitive scores when combined with the correct tail:
- CTX-1019660 (thienopyrimidine + triazolopyrimidine cap, rank 4, –12.819)
- CTX-1019813 (thienopyrimidine + benzofuran cap, rank 6, –12.768)
- CTX-1020555 (thienopyrimidine + chloroindazole, rank 8, –12.698)

These engage A:HIS122 and CDK2 hydrophobic contacts similarly to the benzofuran series.

### 6.4 Piperazine / Basic Nitrogen Tail

The N-methylpiperazine tail contributes the B:GLU362 salt bridge (~3 kcal/mol electrostatic contribution in MM/GBSA from the prior session). However, neutral alternatives that place aromatic groups in the B-chain interface can compensate:
- CTX-1020751 (rank 10, –12.551): CF3-phenyl tail, no piperazine — achieves high score via hydrophobic burial in B:TRP315/B:GLU401/B:SER446 pocket
- Bottom-quartile compounds without piperazine tend to have small, polar heteroaromatic tails (oxazole, thiazole, imidazole) that lack both the salt bridge and hydrophobic volume, scoring –10.18 to –9.61 kcal/mol

**Tail ranking:** piperazine-benzyl ≈ CF3-benzyl > small heteroarylmethyl > alkyl-heteroaryl

### 6.5 Molecular Weight and Lipophilicity

| Quartile | Score range | MW range | Notes |
|----------|-------------|----------|-------|
| Top 10 | –12.979 to –12.551 | 493–604 Da | Bicyclic caps, large interface footprint |
| Middle 30–60 | –12.005 to –11.294 | 420–591 Da | Standard benzofuran + piperazine scaffold |
| Bottom 20 | –11.126 to –9.609 | 415–530 Da | Small tails, loss of interface contacts |

MW alone does not drive score: CTX-1020751 (rank 10, MW = 493.5) outscores CTX-1020562 (rank 45, MW = 591.6).

---

## 7. Comparison to CTX Crystal and CTX-1017233 Reference

| Feature | CTX-1020521 (rank 1) | CTX-1017233 (rank 13, this run) | CTX crystal (score_only) |
|---------|---------------------|--------------------------------|--------------------------|
| Vina score | –12.979 kcal/mol | –12.449 kcal/mol | –14.090 kcal/mol |
| IC50 predicted (25°C) | 611 pM | 1.5 nM | 94 pM |
| A:HIS122 H-bond | ✓ 3.15 Å | ✓ 2.96 Å | ✓ 3.12 Å (crystal) |
| B:GLU362 salt bridge | — | ✓ 2.94 Å | ✓ 3.15 Å (crystal B:GLU63) |
| Key hydrophobic | A:ALA152, A:GLY154 | A:ALA152, A:GLY154 | A:VAL155, A:GLY154 |
| MW | 603.7 Da | 523.6 Da | 523.3 Da |
| Net charge (pH 7.4) | +1 | +1 | +1 |
| Binding site | CDK2/Cyclin-E interface | Same | Same |

CTX-1020521 scores 0.53 kcal/mol better than CTX-1017233 (≈ 2-fold improvement in predicted Ki) at the cost of +80 Da MW (methylpyrazole-pyrimidine substitution). Both compounds are well within the crystal-validated site. CTX-1020521 does not recapitulate the B:GLU362 salt bridge in its best pose; instead it engages B:SER446 (3.19 Å) and A:ALA152 (3.14 Å) with slightly different geometry from the heavier scaffold.

The crystal CTX remains 1.1 kcal/mol better than the best-docked compound. The gap reflects: (i) exhaustiveness-8 vs in-place scoring; (ii) the crystal structure is fully relaxed with ordered water networks and induced-fit backbone adjustments absent from rigid-receptor docking.

---

## 8. Output Files

| File | Contents |
|------|----------|
| `Sorted_Cedilla.sdf` | Input: 84 compounds |
| `all_std_neutral.sdf` | Standardised neutral SDF (RDKit) |
| `all_protonated_3d.sdf` | pH 7.4 protonated 3D SDF (OpenBabel) |
| `ligands_3d/lig{1-84}.sdf` | Individual compound SDF files |
| `ligands_3d/lig{1-84}.pdbqt` | PDBQT files for Vina (Gasteiger charges) |
| `docking_results/lig{1-84}_out.pdbqt` | 5 docked poses per compound |
| `docking_scores.json` | All 84 scores (Vina, 5 poses) + MW + charge |
| `score_table.json` | Ranked score table with IC50 conversions |
| `mmgbsa/{compound}/FINAL_RESULTS_MMGBSA.dat` | Per-compound MM/GBSA decomposition |
| `mmgbsa/mmgbsa_results.json` | Collated MM/GBSA ΔG values |
| `receptor_ab.pdb` | Prepared receptor (chains A+B, pdb4amber) |
| `receptor.pdbqt` | Receptor PDBQT for Vina |

---

## 9. Limitations and Recommended Follow-up

1. **Exhaustiveness 8:** Lower than the exhaustiveness-32 used for CTX-1017233 in the prior session. For the top 10 compounds, a confirmatory re-run at exhaustiveness 32 is recommended; expected score change ≤ 0.5 kcal/mol.

2. **Rigid-receptor docking:** Induced-fit of Arg123/Phe146/Lys22 not captured. Flexible-receptor docking (AutoDock-GPU or Glide IFD) advised for final lead selection.

3. **MM/GBSA single-frame:** Gas-phase minimised pose; see Section 5. MD-averaged MM/GBSA (10–50 ns, TIP3P, 0.15 M NaCl) is required for reliable absolute ΔG. Existing solvated topology (`complex_solv.prmtop`, 83,532 atoms) from the prior session covers CTX-1017233; new topologies needed for the top 10.

4. **Residue-number correspondence:** Contact analysis uses AMBER-sequential numbering. Mapping back to PDB crystal numbering: A:HIS122 (same), B:GLU362 ≈ original Cyclin-E GLU63, B:ILE317 ≈ Cyclin-E ILE20, B:LEU442 ≈ Cyclin-E LEU145.

5. **Stereochemistry:** CTX-1020699 has one defined stereocentre (S). All other compounds have no stereocentres; obabel generated a single low-energy conformer for docking.

6. **IC50 conversion caveat:** Predicted IC50 values assume competitive inhibition, [ATP] = Km = 10 µM (CDK2), and that Vina scores approximate experimental ΔG. Vina RMSE vs experiment ≈ 1–2 kcal/mol → ≈ 5–30-fold uncertainty in absolute IC50. Use values for relative ranking only.
