# Recovery Audit: Corrected Per-Residue RMSD Statistics
## ARV-471 Boltz-2 CRBN Models vs. Crystal Structure (CRBN.pdb)

**Date:** 2026-09-18  
**Auditor:** Claude Sonnet 4.6 (Rayca session, run max-7c6043180f)  
**Corrects:** M-1 finding in `audit_crbn_crystal_comparison.md`  
**Scripts:** 068\_get\_seq\_ca.py (corrected recomputation; stored in session source/)

---

## What Was Wrong

Scripts `062_get_seq_ca.py` (line 41) and `064_get_seq_ca.py` (line 52) applied the rotation matrix as:

```python
mod_transformed = mod_coords @ rot.T + tran   # WRONG — inverse rotation
```

BioPython's `SVDSuperimposer.get_rotran()` returns a right-multiplying rotation; the correct transform is `coords @ rot + tran`. Applying `rot.T` rotates model coordinates *away* from the reference, making all per-residue distance statistics wrong.

**Diagnostic:** model_0 previously reported mean=28.41 Å > RMSD=24.01 Å, which violates the power-mean inequality (mean per-residue distance ≤ RMSD always). This confirms the rotation was inverted.

The global and per-domain RMSD values from `sup.rms` were unaffected (BioPython computes those internally without `rotran`).

---

## Corrected Per-Residue Statistics

All three models, 370 matched Cα pairs (local alignment, crystal residues 47–427).

### Validation

| Model | sup.rms (Å) | Recomputed RMSD (Å) | Mean dist (Å) | Jensen check |
|:-----:|:-----------:|:-------------------:|:-------------:|:------------:|
| 0     | 24.01       | 24.01               | 21.62         | OK (21.62 ≤ 24.01) |
| 1     | 20.86       | 20.86               | 18.06         | OK (18.06 ≤ 20.86) |
| 2     | 22.51       | 22.51               | 19.46         | OK (19.46 ≤ 22.51) |

Recomputed RMSD matches `sup.rms` to four decimal places in all cases. Jensen's inequality holds for all models. The correction is confirmed.

---

### Summary Table

| Model | Global RMSD (Å) | Mean (Å) | Median (Å) | Max (Å) | < 2 Å | < 5 Å | Pocket RMSD (74 Cα, Å) |
|:-----:|:-----------:|:--------:|:----------:|:-------:|:-----:|:-----:|:-------------------:|
| 0     | 24.01       | 21.62    | 19.07      | 54.47   | 0%    | 0%    | 17.56               |
| 1     | 20.86       | 18.06    | 16.46      | 50.85   | 1%    | 9%    | 20.01               |
| 2     | 22.51       | 19.46    | 16.66      | 54.60   | 1%    | 4%    | 20.01               |

Pocket residues defined as crystal residues 127–164 ∪ 374–409 (74 Cα total, near LVY ligand).

---

### Per-Domain RMSD (from `sup.rms`, unchanged)

| Domain | Residues | Cα | model_0 (Å) | model_1 (Å) | model_2 (Å) |
|:-------|:--------:|:--:|:-----------:|:-----------:|:-----------:|
| N-lobe (47–165)  | 47–165   | 119 | 14.50 | 12.41 | 15.94 |
| C-lobe (166–320) | 166–320  | 144 | 20.71 | 14.65 | 21.44 |
| TBD (321–427)    | 321–427  | 107 | 12.91 | 13.90 | 13.76 |

---

### Worst Residues (5 per model, after correction)

**model_0** — worst cluster in C-lobe (228–238):

| Crystal res | Distance (Å) |
|:-----------:|:------------:|
| 231 | 54.5 |
| 232 | 52.6 |
| 238 | 51.0 |
| 207 | 50.5 |
| 228 | 50.4 |

**model_1** — worst cluster at N-terminus and C-lobe (238–241, res 47):

| Crystal res | Distance (Å) |
|:-----------:|:------------:|
| 239 | 50.9 |
| 238 | 50.8 |
| 240 | 50.6 |
| 241 | 49.7 |
|  47 | 49.4 |

**model_2** — worst cluster in C-lobe (228–236):

| Crystal res | Distance (Å) |
|:-----------:|:------------:|
| 231 | 54.6 |
| 232 | 53.8 |
| 228 | 52.1 |
| 236 | 50.0 |
| 235 | 50.0 |

---

### Best Residues (5 per model, after correction)

**model_0** — best near TBD/C-lobe boundary (364, 396–403); no residue < 5 Å:

| Crystal res | Distance (Å) |
|:-----------:|:------------:|
| 364 | 5.33 |
| 402 | 5.69 |
| 403 | 5.84 |
| 396 | 6.01 |
| 189 | 6.21 |

**model_1** — best in C-lobe (173, 179–181); 3 residues < 2 Å (best model):

| Crystal res | Distance (Å) |
|:-----------:|:------------:|
| 180 | 1.17 |
| 173 | 1.35 |
| 179 | 1.78 |
|  82 | 1.83 |
| 181 | 2.16 |

**model_2** — best in N-lobe/TBD (139, 190–192, 161); 2 residues < 1 Å:

| Crystal res | Distance (Å) |
|:-----------:|:------------:|
| 139 | 0.82 |
| 190 | 0.99 |
| 191 | 2.36 |
| 192 | 2.62 |
| 161 | 3.56 |

---

### pLDDT (B-factor column, corrected window)

pLDDT computed over the 370 matched residues only (excludes N-terminal expression tag).

| Model | Mean | Min  | Max  |
|:-----:|:----:|:----:|:----:|
| 0     | 35.8 | 22.2 | 64.7 |
| 1     | 34.4 | 20.9 | 61.8 |
| 2     | 33.4 | 19.8 | 61.7 |

Note: M-3 in the original audit flagged `plddt[:180]` as mixing tag residues with N-lobe. These values are computed over matched-residue indices and are not affected by that label error.

---

## What Remains Unchanged

- Global RMSD values: 24.01, 20.86, 22.51 Å (model_0, 1, 2) — from `sup.rms`, unchanged.
- Per-domain RMSD values: same as script 065 output — from `sup.rms`, unchanged.
- Overall conclusion: CRBN is not reliably predicted. Mean per-residue distance 18–22 Å, pocket RMSD 18–20 Å, pLDDT 33–36 (very low confidence throughout). The best model (model_1) has a small cluster of 3–5 residues near the C-lobe centre (173–181) that superimpose within 2 Å, but even the best-fitting domain (N-lobe of model_1) has RMSD 12.4 Å.

## Open Audit Items Not Addressed Here

- **M-2** (domain boundary citations): CRBN domain cuts (47–165, 166–320, 321–427) are used above without citation. The TBD boundary in particular varies 318–330 across publications.
- **C-1** (no phase document): the phase_01_compare document lists only scripts 059–064 and records no numerical results. Script 065 (domain RMSD + pLDDT) and this corrected re-analysis are not reflected there.
