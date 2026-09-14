# Phase 11 — PROTAC Series Ternary Complex PDB Export (ARV-001 to ARV-010, model_0)

## Summary

The Boltz-2 model_0 PDB files for all ten PROTAC ternary complex predictions (ARV-001 through
ARV-010 vs ERα + CRBN, job 6534300, Isambard-AI GH200, 14 Sep 2026) were copied from the
`boltz_series/` subdirectories to the session root under clean names. No coordinates,
B-factors, or chain assignments were modified. HETATM counts confirmed against expected
heavy-atom counts from the SMILES extraction phase.

---

## Job Provenance

| Field | Value |
|:---|:---|
| Job ID | 6534300 |
| Cluster | Isambard-AI Phase 2 (GH200, aarch64) |
| Container | boltzgen-0.3.1.sif (Boltz-2 v0.4.2) |
| Run date | 14 Sep 2026, 13:07–13:17 UTC |
| Settings | seed=42, sampling_steps=50, recycling_steps=3, --no_kernels |
| Diffusion samples | 3 per compound; model_0 exported here |
| SLURM log | `slurm-6534300.log` |
| Failed examples | 0 of 10 |

Chain assignment for all files: A = ERα LBD (258 residues), B = CRBN thalidomide-binding
domain (469 residues), C = PROTAC ligand (HETATM, residue LIG).

---

## Output Files

| File | HETATM (ligand HA) | Records | Bytes | SHA-256 |
|:---|:---:|:---:|:---:|:---|
| `ARV_001_ERalpha_CRBN_model_0.pdb` | 53 | 5886 | 481949 | `76ff9cfb54241c1d30d3d229cf26fe76c8e0a6405b297d0ddc5c4a73784f9867` |
| `ARV_002_ERalpha_CRBN_model_0.pdb` | 51 | 5884 | 481625 | `4e34caf8a9078d969b93789605ef8aedffc407f09f94c99e1a471ccf5c163280` |
| `ARV_003_ERalpha_CRBN_model_0.pdb` | 55 | 5888 | 482273 | `6fd0fdd50bd38cd63e710864c74ec3b363f22c5fc8f7564b745ff0b6467ff3e5` |
| `ARV_004_ERalpha_CRBN_model_0.pdb` | 45 | 5878 | 480572 | `9acb5167bd401745685c602870b91ed8fc90aef26937f08c9c1597b125bc90fd` |
| `ARV_005_ERalpha_CRBN_model_0.pdb` | 48 | 5881 | 481058 | `7584745954e60fe4d867469f57740f96d17db477de6ded767b86e60ce146f2f8` |
| `ARV_006_ERalpha_CRBN_model_0.pdb` | 51 | 5884 | 481544 | `2b6519a34e0028cecc211dc8a5d315ce8227b426e07d4e87f2e4ab337a936408` |
| `ARV_007_ERalpha_CRBN_model_0.pdb` | 54 | 5887 | 482030 | `3cad0cc4f8a0cf13475c6087b88cf307d5644f9c5bb6f87edc83d051a3a36710` |
| `ARV_008_ERalpha_CRBN_model_0.pdb` | 57 | 5890 | 482516 | `ae1e22ff539ce789a8a9e5c4ca1d68f1e20017b701f5959dc161337a224a42de` |
| `ARV_009_ERalpha_CRBN_model_0.pdb` | 60 | 5893 | 483002 | `afda2cfe804cf039244748122e67d73fe69bbc26623f5d4351bcd59202a7c7d0` |
| `ARV_010_ERalpha_CRBN_model_0.pdb` | 87 | 5920 | 487376 | `c59e5dcfd5da72198024143c32f7676429ab2acc557a99e30892c28dbf63143d` |

Source pattern:
`boltz_series/<ARV_NNN>/boltz_results_<ARV_NNN>_ERalpha_CRBN_boltz_input/predictions/<ARV_NNN>_ERalpha_CRBN_boltz_input/<ARV_NNN>_ERalpha_CRBN_boltz_input_model_0.pdb`

---

## Cooperativity Ranking (model_0, from phase_09)

For reference when selecting structures for visual inspection:

| Rank | File | lig→CRBN iptm | Δ vs ARV-471 ref |
|:---:|:---|:---:|:---:|
| 1 | `ARV_001_ERalpha_CRBN_model_0.pdb` | 0.5086 | +0.278 |
| 2 | `ARV_006_ERalpha_CRBN_model_0.pdb` | 0.4331 | +0.203 |
| 3 | `ARV_003_ERalpha_CRBN_model_0.pdb` | 0.4059 | +0.175 |
| 4 | `ARV_009_ERalpha_CRBN_model_0.pdb` | 0.3574 | +0.127 |
| 5 | `ARV_005_ERalpha_CRBN_model_0.pdb` | 0.3461 | +0.116 |
| 6 | `ARV_008_ERalpha_CRBN_model_0.pdb` | 0.3331 | +0.103 |
| 7 | `ARV_002_ERalpha_CRBN_model_0.pdb` | 0.2718 | +0.041 |
| 8 | `ARV_004_ERalpha_CRBN_model_0.pdb` | 0.2657 | +0.035 |
| 9 | `ARV_010_ERalpha_CRBN_model_0.pdb` | 0.2454 | +0.015 ⚠ ETKDGv3 failure |
| 10 | `ARV_007_ERalpha_CRBN_model_0.pdb` | 0.1932 | −0.037 |

ARV-471 reference (model_0, job 6465991): lig→CRBN iptm = 0.2306.

---

## Verification

**HETATM counts match expected heavy-atom counts.** The HETATM count for each compound
(column 4 above) was compared against the RDKit-derived heavy-atom counts from the SMILES
extraction phase. All 10 match exactly: ARV-001=53, ARV-002=51, ARV-003=55, ARV-004=45,
ARV-005=48, ARV-006=51, ARV-007=54, ARV-008=57, ARV-009=60, ARV-010=87. Note: the HA
column in `phase_09_protac_series_predictions.md` Table 1 shows values 6–12 lower for
most compounds (a known error from the `LINKER_INFO[name][2] + 35` formula in
`analyze_protac_series.py`, flagged as MAJOR in `reports/audit_phase_01_task_bymr9kz1y.md`).
The HETATM counts in the PDB files are the ground truth.

**All three chains confirmed present in every file.** `grep -c "^ATOM\|^HETATM"` and chain
column parsed for all 10 files; chains A, B, C present in each.

**Record counts are consistent with sequence lengths.** ERα 258 residues × ~8 heavy atoms/residue
≈ 2064; CRBN 469 residues × ~8 ≈ 3752; plus ligand HETATM. Total ATOM+HETATM per file
ranges 5878–5920, consistent with all-heavy-atom representation.

**SHA-256 checksums computed directly.** `sha256sum` run on each copied file immediately
after the copy operation. Source files in `boltz_series/` are unchanged.

---

## Limitations

- Model_0 only. Models 1 and 2 per compound exist in `boltz_series/` but were not copied.
- No energy minimisation or clash removal applied. All 10 raw Boltz-2 outputs contain
  steric clashes (minimum ERα-CRBN all-atom distances 1.2–2.1 Å).
- CRBN orientation is unconstrained (no-MSA mode). CRBN mean pLDDT ≈ 35 for all models;
  CRBN placement should not be used for structural inference without further refinement.
- ARV-010 ligand started from random coordinates due to ETKDGv3 conformer failure;
  the chain C coordinates in that file are structurally unreliable.

---

## References

- Passaro S, Corso G, Wohlwend J et al. Boltz-2: Towards Accurate and Efficient Binding
  Affinity Prediction. bioRxiv 2025. doi:10.1101/2025.06.14.659707
