
## Summary

All 18 simulations (6 compounds × 3 replicas × 10 ns) completed on Isambard GH200 (job 6510625, GROMACS 2026.1, AMBER14SB + GAFF2/Gasteiger + TIP3P). Results are extracted from the SLURM job log; output XVG files were not collected to the session workspace (scratch-path mismatch during Rayca collection). All numbers reported here are computed from the raw results table in the log.

**Verdict: MD does not separate the two classes at this timescale.** The between-class RMSD gap (1.39 nm) is smaller than the within-class replica range for three of six compounds. The H-bond metric was unavailable due to a GAFF2/GROMACS 2026.1 incompatibility. BSA showed no class difference.

---

## 1. Per-Replica Results

| Compound | Class | Rep | RMSD mean (nm) | RMSD SD (nm) | MinDist mean (nm) | BSA mean (nm²) |
|----------|-------|-----|---------------|-------------|------------------|----------------|
| EDS00495858 | active | 1 | 2.643 | 2.705 | 0.1679 | 15.35 |
| EDS00495858 | active | 2 | 1.375 | 2.227 | 0.1679 | 14.73 |
| EDS00495858 | active | 3 | 1.236 | 1.994 | 0.1677 | 16.75 |
| EDS00480994 | active | 1 | 1.073 | 2.023 | 0.1671 | 15.54 |
| EDS00480994 | active | 2 | 0.895 | 1.860 | 0.1670 | 16.65 |
| EDS00480994 | active | 3 | 0.148 | 0.245 | 0.1677 | 15.46 |
| EDS00444974 | active | 1 | 2.254 | 2.322 | 0.1682 | 13.83 |
| EDS00444974 | active | 2 | 4.995 | 1.424 | 0.1680 | 14.68 |
| EDS00444974 | active | 3 | 0.543 | 1.164 | 0.1694 | 14.33 |
| EDS00481054 | inactive | 1 | 5.524 | 1.600 | 0.1687 | 14.49 |
| EDS00481054 | inactive | 2 | 4.740 | 2.417 | 0.1699 | 15.57 |
| EDS00481054 | inactive | 3 | 2.376 | 2.795 | 0.1706 | 14.45 |
| EDS00441134 | inactive | 1 | 3.593 | 3.430 | 0.1655 | 17.32 |
| EDS00441134 | inactive | 2 | 0.362 | 1.059 | 0.1674 | 15.69 |
| EDS00441134 | inactive | 3 | 0.224 | 0.296 | 0.1693 | 15.63 |
| EDS00445742 | inactive | 1 | 4.695 | 1.690 | 0.1672 | 14.56 |
| EDS00445742 | inactive | 2 | 1.416 | 2.241 | 0.1673 | 14.45 |
| EDS00445742 | inactive | 3 | 4.769 | 1.882 | 0.1660 | 15.85 |

RMSD is ligand heavy-atom RMSD after Backbone fit (nm). SD is the within-trajectory standard deviation over 1001 frames (0–10 ns). MinDist is the minimum inter-chain atom–atom distance (CDK2 vs Cyclin E). BSA is (SASA_A + SASA_B − SASA_AB) / 2 over 1001 frames.

H-bond count: not available — see section 4.

---

## 2. Per-Compound Summary

| Compound | Class | RMSD mean (nm) | RMSD within-compound range (nm) | BSA mean (nm²) |
|----------|-------|-------------|--------------------------|-------------|
| EDS00495858 | active   | 1.751 | 1.407 | 15.61 |
| EDS00480994 | active   | 0.705 | 0.925 | 15.89 |
| EDS00444974 | active   | 2.597 | 4.451 | 14.28 |
| EDS00481054 | inactive | 4.213 | 3.148 | 14.84 |
| EDS00441134 | inactive | 1.393 | 3.369 | 16.22 |
| EDS00445742 | inactive | 3.627 | 3.353 | 14.95 |

---

## 3. Class Comparison and Separation Test

### Ligand RMSD

Active class mean: **1.685 nm** (SD across three compound means: 0.948 nm)  
Inactive class mean: **3.078 nm** (SD: 1.488 nm)  
Between-class gap: **1.393 nm**

Pre-specified separation criterion: gap must exceed the largest within-compound replica range.

| | Max within-compound range |
|-|--------------------------|
| Actives | 4.451 nm (EDS00444974) |
| Inactives | 3.369 nm (EDS00441134) |

**Gap (1.393 nm) < max active range (4.451 nm) and < max inactive range (3.369 nm).**  
**Criterion not met. RMSD does not separate the classes.**

The trend is in the expected direction (inactives drift more), but the within-class variance is too large to make the separation meaningful. Three of nine active replicas (33%) and six of nine inactive replicas (67%) show RMSD > 2 nm at the trajectory mean, indicating the ligand substantially left the docked starting pose in the majority of runs for both classes.

### Buried Surface Area (BSA)

Active class BSA: **15.26 nm²**  
Inactive class BSA: **15.34 nm²**  
Gap: **0.08 nm²** (within-compound variation ~1–2 nm²)

BSA shows no class difference. The interface area between CDK2 and Cyclin E is unaffected by whether an active or inactive ligand is present, consistent with both classes maintaining protein–protein contact at 10 ns.

### Inter-Chain Minimum Distance

All 18 replicas: mean 1.68 Å, SD 0.01 Å, full range 0.05 Å. The protein complex is stable in every run regardless of ligand class or compound identity. This is a positive control: both actives and inactives hold the CDK2-CCNE interface together at this timescale, which is expected.

---

## 4. H-Bond Metric: Not Available

`gmx hbond` reported `Selection 'LIG' has 0 acceptors and 0 donors` for every compound across all 18 replicas. This is a GAFF2/GROMACS 2026.1 incompatibility: the `gmx hbond` selection interface identifies H-bond donors and acceptors by standard GROMACS atom type (N–H, O–H bonding patterns in AMBER-standard nomenclature). GAFF2 atom types (`ca`, `c3`, `na`, `nh`, `oh`) are not on this recognition list, so all six ligands report zero H-bond capacity regardless of their chemical structure. The bridging contacts to HIS121-A and LYS108-B that motivate this test could not be counted.

This metric would need to be recovered by one of:
- Converting GAFF2 atom types to GROMACS-recognised equivalents in the ITP before analysis
- Using GROMACS' `gmx select` with explicit atom-name selections for the ligand NH/OH atoms
- Running the same analysis in MDAnalysis, which uses element-based H-bond detection

---

## 5. Verdict

**10 ns MD with GAFF2/Gasteiger charges does not separate the active and inactive classes on CDK2-CCNE.**

There are three compounding reasons:

1. **Ligand pose instability:** Large within-trajectory RMSD standard deviations (1–3 nm) indicate most replicas are not sampling a stable pose. They are measuring drift, not occupancy of a bound state. Comparing RMSD means between two drifting ligands is not a meaningful activity discrimination.

2. **Single starting pose:** All three replicas of each compound start from the same gnina rank-1 docked pose, so inter-replica variation comes entirely from thermal noise in initial velocities. Any error in the docked pose propagates to all three replicas.

3. **H-bond metric unavailable:** The most direct measure of whether the two pharmacophoric contacts (HIS121-A and LYS108-B) are bridged was not computable due to the GAFF2 atom-type incompatibility.

---

## 6. What Would Be Needed to Separate the Classes

The pilot motivates three specific improvements, in ascending cost:

**Fix the H-bond analysis (~1 day):** Patch the ligand ITP to use GROMACS-standard atom type strings for heteroatoms (N, O), or write an MDAnalysis script using element-based H-bond detection. Re-run analysis on existing trajectories. No new simulation needed.

**AM1-BCC charges and longer simulation (~1 week):** Replace Gasteiger with AM1-BCC charges (or RESP from a single-point calculation) to improve the electrostatic driving force that keeps the ligand in the binding site. Extend production to 50–100 ns per replica. At 100 ns the pose stability vs. drift distinction is more reliable. Estimated cost on Isambard GH200: ~4 h/run, ~3 jobs of 12 runs each.

**Relative binding FEP on the three active/inactive pairs (~3 days compute):** The three active–inactive pairs (Tanimoto 0.845–0.896) are ideal RBFE candidates. Each pair needs ~5 λ-windows × 2 directions × 5 ns = 50 ns of FEP per pair. Estimated cost: 3 GROMACS FEP jobs × 1 day each. This is the rigorous route to a quantitative activity discrimination that is not confounded by pose uncertainty.

---

## 7. Technical Notes

**All 18 simulations completed** EM → NVT (100 ps) → NPT (500 ps) → production (10 ns), 1001 frames each. EM converged on every system (Fmax < 100 kJ/mol/nm). NVT performance: ~444 ns/day on GH200. Production: ~439 ns/day. Total wall-clock ~19 h.

**Output file collection:** `$RAYCA_OUT` on scratch was not collected by the Rayca platform on job completion (`files: []`). All results are recovered from the SLURM log. The full results table was printed at the end of the job script and matches what is reported here.

**Job history:** Four cluster jobs were required before a successful run. Failures were: (1) `ions.itp` renamed in GROMACS 2026.1; (2) duplicate `[ molecules ]` block in acpype-generated topologies; (3) stale Open MPI temp files causing `cp` to abort. All three were independent and required separate investigation.
