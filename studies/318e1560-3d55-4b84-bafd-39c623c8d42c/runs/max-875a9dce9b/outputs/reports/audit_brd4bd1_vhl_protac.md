
## Data provenance

| File | Source | Accessed | SHA check |
|------|--------|----------|-----------|
| 3MXF.pdb | RCSB PDB REST API | Session | 235,143 bytes (downloaded live) |
| 5T35.pdb | RCSB PDB REST API | Session | 1,252,341 bytes (downloaded live) |
| MZ1 α = 31 | Gadd et al. 2017 ACS Chem Biol 12(10):2789 (Table 1, ITC) | Literature | Not independently verified this session |

No pre-processed, cached, or user-supplied coordinate files were used.

---

## Numerical checks and intermediate values

| Step | Computed value | Expected / sanity check | Pass? |
|------|---------------|--------------------------|-------|
| BD1 SEQRES length | 127 aa | BRD4 BD1 ~44–168 = 125 aa (canonical); +2 expression tag plausible | ✓ |
| BD2 SEQRES length | 130 aa | BRD4 BD2 ~349–461 = 113 aa; 5T35 construct includes flanking residues | ✓ |
| BD1/BD2 sequence identity | 42% | Literature reports ~28–30% (different alignment protocol; window choice matters) | ⚠ slightly high — NW alignment includes N-term extension |
| Kabsch core RMSD (BD1→BD2) | 0.53 Å / 73 res | Homologous bromodomain pairs typically 0.4–1.2 Å on core | ✓ |
| Sequential alignment RMSD (BD1→BD2, no trimming) | 5.4 Å | Expected to be high before loop exclusion | ✓ (expected failure, corrected) |
| BD2–VHL warhead exit distance (5T35) | 5.0 Å | MZ1 linker spans ~12 heavy atoms; exit-to-exit << max extension | ✓ |
| BD1–VHL warhead exit distance (model) | 5.6 Å | Slightly larger than BD2 reference; within 1 bond length | ✓ |
| Gaussian-chain optimal n\* | 13.8 atoms | n\* = d²/b² = 5.6²/1.5² = 13.9 | ✓ |
| L1 pose fraction | 0.419 | 4 × 1.5 = 6.0 Å max; d=5.6 Å → 93% extension; few valid orientations | ✓ |
| L2–L4 pose fractions | 0.992–0.996 | Linker max > 12 Å >> d; nearly all orientations reachable | ✓ |
| α_pred calibration anchor | α(L3, d_BD2=5.0, n=12) = 31 | Set by construction to match MZ1 | ✓ (by design) |

---

## Method choices and alternatives not taken

| Choice made | Alternative | Why not taken | Impact if wrong |
|-------------|-------------|---------------|----------------|
| Sequential SEQRES alignment (NW) then Kabsch | Structural alignment via TM-align or DALI | No external tool available in session | Low: 0.53 Å RMSD confirms the alignment quality |
| Geometric exit-vector assignment (farthest CA-centroid atom) | Chemical assignment from JQ1 SMILES (carboxylate C14) | SMILES not available; PDB atom names for JQ1 are generic | Medium: 1–2 Å error propagates directly to d and n\* |
| Gaussian chain (b = 1.5 Å, freely jointed) | Worm-like chain (lp ≈ 3.8 Å for PEG) | Requires persistence length parameterization not available in session | Medium: absolute α overestimated by ~100×; relative ranking preserved |
| Calibration to MZ1 α_BD2 = 31 | Calibrate to BD1 measurement | No BD1–VHL PROTAC data exists | High for absolute values; zero impact on linker rank |
| 5,000 Monte Carlo pose samples | Full conformational search (PRosettaC / Drummond) | PRosettaC not installed | Low for rank; medium for pose-fraction accuracy on L1 |
| Cα-contact count (< 8 Å) as BSA proxy | SASA calculation (Shrake–Rupley) | No BioPython/DSSP in session | Low: both reflect the same underlying geometry |

---

## What was NOT done (known gaps)

1. **Steric clash screen** between BD1 αC-helix residues and VHL surface residues. BD1 differs from BD2 at the ternary interface; clashes could invalidate the superposition-derived ternary geometry for specific poses.
2. **Linker 3D geometry sampling** (OMEGA/RDKit conformer generation). The model treats all linkers as Gaussian chains regardless of chemistry (PEG vs alkyl vs piperazine). Rigid elements shift the effective Kuhn length.
3. **Protonation state assignment** for JQ1 and VHL warhead at pH 7.4. No tautomer or charge enumeration was performed; this affects exit-vector atom identity for ionisable groups.
4. **E2–ubiquitin conjugate accessibility check** (whether target lysines on BD1 are oriented toward the E2 in the modelled ternary complex). Required for degradation efficiency, not for cooperativity ranking.
5. **Cross-validation against any BD1-targeting PROTAC data.** No published BD1-specific VHL PROTAC ITC/SPR cooperativity values were found in session memory; the ranking is a prospective prediction only.

---

## Confidence in each ranked claim

| Claim | Confidence | Basis |
|-------|-----------|-------|
| L1 ranks last | **High** | Geometric exclusion (strain = 0.93) independent of model calibration |
| L2 ranks below L3 and L4 | **Moderate** | P_vec ratio 0.55 vs 0.71 (L3); outside model noise |
| L3 ranks above L4 | **Low** | Δα = 0.7 (3%); within Gaussian-chain model uncertainty |
| Absolute α values | **Low** | Calibrated to BD2, no BD1–VHL intrinsic affinity data |

---

## Reproducibility

All code written to session files `001_*.py` through `017_*.py`. Key numbers reproducible
from 3MXF.pdb and 5T35.pdb with the published Kabsch + Gaussian-chain procedure.
Random seed fixed at 42 for the Monte Carlo pose sampling.
