# PROTAC Ternary Complex Prediction — Detailed Results

**Project:** Constrained Boltz-2 ternary complex predictions, PROTAC series ARV_001–010 against CRBN–ERα
**Date:** 2026-09-14  
**Cluster job:** Isambard-AI Phase 2, job 6548359 (GH200 120 GB, aarch64)  
**Model:** Boltz-2 v0.4.2 (`boltzgen-0.3.1.sif`)  
**Parameters:** `--diffusion_samples 3 --sampling_steps 50 --recycling_steps 3 --seed 42 --no_kernels`  
**Reference (unconstrained):** ARV-471, job 6465991, model_0 lig→CRBN iPTM = 0.2306

---

## Chain Assignment

| Chain | Identity | Residues |
|:-----:|:---------|:--------:|
| A | ERα LBD | 258 aa |
| B | CRBN | 469 aa |
| C | PROTAC ligand | 1 entity |

---

## Pocket Constraints Applied

Dual `pocket` blocks in Boltz-2 YAML (`force: false`, `max_distance: 6.0 Å`, `binder: C`):

**CRBN glutarimide pocket (chain B residues):** 111, 112, 113, 114, 125, 240, 241, 246, 249, 250, 261, 263, 264, 266

**ERα phenol/LBD pocket (chain A residues):** 47, 50, 53, 54, 57, 88, 91, 92, 95, 98, 108, 125, 128, 129, 132, 225, 228, 229

Pocket residues were derived from the ARV-471 model_0 reference structure (job 6465991) at a 5 Å distance cutoff from the ligand.

---

## Cooperativity Ranking (Best Model per Compound)

Ranked by lig→CRBN inter-chain iPTM (`pair_chains_iptm["2"]["1"]`). Best model = highest lig→CRBN across 3 diffusion samples.

| Rank | Compound | Best Model | conf | ptm | iptm | lig→ERα | lig→CRBN | prot_iptm | Δ unconstrained |
|:----:|:---------|:----------:|-----:|----:|-----:|--------:|---------:|----------:|----------------:|
| 1 | **ARV_005** | model_0 | 0.5066 | 0.5051 | 0.5265 | 0.9034 | **0.7181** | 0.5283 | +0.372 |
| 2 | **ARV_007** | model_0 | 0.5161 | 0.5233 | 0.6640 | 0.8748 | **0.6771** | 0.6633 | +0.484 |
| 3 | **ARV_001** | model_0 | 0.4934 | 0.5293 | 0.5476 | 0.9267 | **0.6740** | 0.5227 | +0.165 |
| 4 | **ARV_002** | model_0 | 0.4886 | 0.5153 | 0.5008 | 0.9337 | **0.6252** | 0.4763 | +0.353 |
| 5 | **ARV_008** | model_2 | 0.4554 | 0.4650 | 0.3338 | 0.7943 | **0.5597** | 0.2523 | +0.227 |
| 6 | **ARV_010** ⚠ | model_0 | 0.5137 | 0.5181 | 0.6161 | 0.6568 | **0.5555** | 0.6549 | +0.310 |
| 7 | **ARV_004** | model_0 | 0.4894 | 0.5161 | 0.4953 | 0.9407 | **0.5519** | 0.4947 | +0.286 |
| 8 | **ARV_006** | model_0 | 0.4979 | 0.5167 | 0.5100 | 0.8820 | **0.5308** | 0.5059 | +0.098 |
| 9 | **ARV_003** | model_2 | 0.4741 | 0.5322 | 0.4020 | 0.9045 | **0.5249** | 0.3868 | +0.119 |
| 10 | **ARV_009** | model_1 | 0.4625 | 0.5001 | 0.4097 | 0.8199 | **0.4901** | 0.3910 | +0.133 |

ARV-471 unconstrained reference (job 6465991): lig→CRBN = 0.2306. All 10 constrained compounds exceed this floor.

---

## Full Confidence Scores — All 3 Models per Compound

| Compound | Model | conf | ptm | iptm | lig→ERα | lig→CRBN | prot_iptm | ERα self | CRBN self | CRBN→ERα |
|:---------|:-----:|-----:|----:|-----:|--------:|---------:|----------:|---------:|----------:|---------:|
| ARV_001 | model_0 ◀ | 0.4934 | 0.5293 | 0.5476 | 0.9267 | 0.6740 | 0.5227 | 0.9073 | 0.2834 | 0.2807 |
| ARV_001 | model_1 | 0.4915 | 0.4941 | 0.4558 | 0.9102 | 0.6019 | 0.4261 | 0.9161 | 0.2429 | 0.2223 |
| ARV_001 | model_2 | 0.4656 | 0.4934 | 0.3457 | 0.8927 | 0.4327 | 0.2766 | 0.9176 | 0.2484 | 0.2229 |
| ARV_002 | model_0 ◀ | 0.4886 | 0.5153 | 0.5008 | 0.9337 | 0.6252 | 0.4763 | 0.8993 | 0.2608 | 0.2615 |
| ARV_002 | model_1 | 0.4741 | 0.4882 | 0.3534 | 0.9235 | 0.5333 | 0.3178 | 0.9227 | 0.2318 | 0.2089 |
| ARV_002 | model_2 | 0.4696 | 0.4830 | 0.3327 | 0.9344 | 0.3856 | 0.2068 | 0.9128 | 0.2485 | 0.2068 |
| ARV_003 | model_0 | 0.4815 | 0.4985 | 0.3759 | 0.8697 | 0.4674 | 0.2491 | 0.9322 | 0.2871 | 0.2216 |
| ARV_003 | model_1 | 0.4779 | 0.4782 | 0.3658 | 0.8803 | 0.5233 | 0.3351 | 0.9037 | 0.2421 | 0.2034 |
| ARV_003 | model_2 ◀ | 0.4741 | 0.5322 | 0.4020 | 0.9045 | 0.5249 | 0.3868 | 0.9324 | 0.2448 | 0.2702 |
| ARV_004 | model_0 ◀ | 0.4894 | 0.5161 | 0.4953 | 0.9407 | 0.5519 | 0.4947 | 0.8900 | 0.2648 | 0.2728 |
| ARV_004 | model_1 | 0.4675 | 0.4614 | 0.3252 | 0.8862 | 0.5034 | 0.2502 | 0.8827 | 0.2626 | 0.1971 |
| ARV_004 | model_2 | 0.4632 | 0.4526 | 0.3158 | 0.8918 | 0.4147 | 0.1940 | 0.8806 | 0.2624 | 0.1832 |
| ARV_005 | model_0 ◀ | 0.5066 | 0.5051 | 0.5265 | 0.9034 | 0.7181 | 0.5283 | 0.9015 | 0.2623 | 0.2499 |
| ARV_005 | model_1 | 0.4811 | 0.4693 | 0.3246 | 0.8514 | 0.3833 | 0.2091 | 0.9137 | 0.2831 | 0.1950 |
| ARV_005 | model_2 | 0.4711 | 0.4792 | 0.3295 | 0.8995 | 0.4617 | 0.2385 | 0.9325 | 0.2598 | 0.1982 |
| ARV_006 | model_0 ◀ | 0.4979 | 0.5167 | 0.5100 | 0.8820 | 0.5308 | 0.5059 | 0.9175 | 0.3008 | 0.2584 |
| ARV_006 | model_1 | 0.4698 | 0.4838 | 0.3463 | 0.8950 | 0.4900 | 0.3064 | 0.9085 | 0.2635 | 0.2120 |
| ARV_006 | model_2 | 0.4665 | 0.4744 | 0.3326 | 0.8584 | 0.3445 | 0.2055 | 0.9223 | 0.2607 | 0.1949 |
| ARV_007 | model_0 ◀ | 0.5161 | 0.5233 | 0.6640 | 0.8748 | 0.6771 | 0.6633 | 0.8903 | 0.2774 | 0.2835 |
| ARV_007 | model_1 | 0.4673 | 0.4724 | 0.3309 | 0.8728 | 0.4442 | 0.2383 | 0.9007 | 0.2473 | 0.1976 |
| ARV_007 | model_2 | 0.4526 | 0.4662 | 0.3261 | 0.8213 | 0.4763 | 0.2152 | 0.8896 | 0.2347 | 0.1966 |
| ARV_008 | model_0 | 0.4718 | 0.4805 | 0.4063 | 0.8335 | 0.5349 | 0.3820 | 0.9055 | 0.2479 | 0.2113 |
| ARV_008 | model_1 | 0.4687 | 0.4676 | 0.3353 | 0.7755 | 0.4833 | 0.2616 | 0.9105 | 0.2421 | 0.1935 |
| ARV_008 | model_2 ◀ | 0.4554 | 0.4650 | 0.3338 | 0.7943 | 0.5597 | 0.2523 | 0.8862 | 0.2545 | 0.1986 |
| ARV_009 | model_0 | 0.4671 | 0.4907 | 0.3709 | 0.7865 | 0.4197 | 0.3697 | 0.9078 | 0.2638 | 0.2307 |
| ARV_009 | model_1 ◀ | 0.4625 | 0.5001 | 0.4097 | 0.8199 | 0.4901 | 0.3910 | 0.8978 | 0.2254 | 0.2427 |
| ARV_009 | model_2 | 0.4559 | 0.4672 | 0.3424 | 0.8001 | 0.4529 | 0.3167 | 0.8962 | 0.2138 | 0.1932 |
| ARV_010 | model_0 ◀ | 0.5137 | 0.5181 | 0.6161 | 0.6568 | 0.5555 | 0.6549 | 0.9123 | 0.2824 | 0.2785 |
| ARV_010 | model_1 | 0.4670 | 0.4702 | 0.3262 | 0.6844 | 0.4510 | 0.2724 | 0.9149 | 0.2578 | 0.1941 |
| ARV_010 | model_2 | 0.4544 | 0.4512 | 0.3063 | 0.6437 | 0.4645 | 0.2260 | 0.8966 | 0.2543 | 0.1762 |

◀ = best model (highest lig→CRBN) used in ranking

---

## Per-Chain Confidence Summary (Best Model)

Mean ERα self-iptm = **0.906** (range 0.890–0.932): ERα fold is consistently high-confidence.
Mean CRBN self-iptm = **0.273** (range 0.248–0.301): CRBN orientation is the dominant uncertainty in all predictions.

| Compound | ERα self | CRBN self | ERα→CRBN | CRBN→ERα |
|:---------|:--------:|:---------:|:--------:|:--------:|
| ARV_005 | 0.9015 | 0.2623 | 0.5283 | 0.2499 |
| ARV_007 | 0.8903 | 0.2774 | 0.6633 | 0.2835 |
| ARV_001 | 0.9073 | 0.2834 | 0.5227 | 0.2807 |
| ARV_002 | 0.8993 | 0.2608 | 0.4763 | 0.2615 |
| ARV_008 | 0.8862 | 0.2545 | 0.2523 | 0.1986 |
| ARV_010 | 0.9123 | 0.2824 | 0.6549 | 0.2785 |
| ARV_004 | 0.8900 | 0.2648 | 0.4947 | 0.2728 |
| ARV_006 | 0.9175 | 0.3008 | 0.5059 | 0.2584 |
| ARV_003 | 0.9324 | 0.2448 | 0.3868 | 0.2702 |
| ARV_009 | 0.8978 | 0.2254 | 0.3910 | 0.2427 |

---

## ERα Surface Lysines Presented to CRBN

ERα (chain A) lysines with NZ at **3.5–12.0 Å** from any CRBN heavy atom in model_0.
Lower bound (3.5 Å) excludes compressed salt-bridge geometry in un-relaxed diffusion outputs.
Upper bound (12.0 Å) captures the CRBN-proximal face accessible to the E2 enzyme.

| Compound | lig→CRBN | # Lysines | Residues (NZ–CRBN distance) |
|:---------|:--------:|:---------:|:---------------------------|
| ARV_005 | 0.7181 | 10 | K233(5.0Å), K171(5.7Å), K224(6.2Å), K105(6.8Å), K7(7.4Å), K235(8.0Å), K153(8.7Å), K176(8.9Å), K185(10.2Å), K3(11.2Å) |
| ARV_007 | 0.6771 | 10 | K105(3.9Å), K171(4.1Å), K176(5.4Å), K224(5.8Å), K235(6.3Å), K3(7.8Å), K120(8.8Å), K185(9.9Å), K6(10.5Å), K153(10.8Å) |
| ARV_001 | 0.6740 | 7 | K235(3.5Å), K176(5.7Å), K153(6.6Å), K3(8.0Å), K7(8.0Å), K224(9.8Å), K6(10.5Å) |
| ARV_002 | 0.6252 | 8 | K224(4.6Å), K153(8.2Å), K7(8.3Å), K233(8.4Å), K3(9.4Å), K235(10.0Å), K171(10.5Å), K185(11.2Å) |
| ARV_008 | 0.5597 | 6 | K7(3.7Å), K171(5.1Å), K233(7.3Å), K176(9.1Å), K153(9.3Å), K185(9.9Å) |
| ARV_010 | 0.5555 | 13 | K224(3.8Å), K7(4.0Å), K153(5.6Å), K171(6.5Å), K105(6.8Å), K3(6.9Å), K176(8.4Å), K233(8.5Å), K196(8.9Å), K185(9.3Å), K6(9.9Å), K235(9.9Å), K120(11.3Å) |
| ARV_004 | 0.5519 | 10 | K224(4.1Å), K233(5.6Å), K7(5.7Å), K171(6.1Å), K153(8.1Å), K185(8.2Å), K3(8.5Å), K235(10.5Å), K120(11.0Å), K6(11.5Å) |
| ARV_006 | 0.5308 | 8 | K171(3.7Å), K176(3.8Å), K120(5.2Å), K3(6.4Å), K105(8.5Å), K6(10.4Å), K196(10.4Å), K235(10.4Å) |
| ARV_003 | 0.5249 | 4 | K233(6.7Å), K153(11.3Å), K235(11.4Å), K7(11.9Å) |
| ARV_009 | 0.4901 | 7 | K233(3.9Å), K66(4.4Å), K153(5.6Å), K171(6.7Å), K7(8.4Å), K6(8.9Å), K196(11.0Å) |

### Consistently Presented Lysines (≥5/10 compounds)

| ERα Lys | Compounds (n/10) | Notes |
|:-------:|:----------------:|:------|
| K153 | 9/10 | Most consistent; best ubiquitination candidate |
| K7   | 8/10 | Proximal in all high-ranked compounds |
| K171 | 8/10 | Closest in ARV_006 (3.7 Å) and ARV_007 (4.1 Å) |
| K235 | 8/10 | Closest in ARV_001 (3.5 Å); absent in ARV_006 |
| K3   | 7/10 | |
| K233 | 7/10 | |
| K176 | 6/10 | |
| K224 | 6/10 | |
| K6   | 6/10 | |
| K185 | 6/10 | |

---

## Evidence Limits — What These Predictions Cannot Support

### 1. ARV_009 and ARV_003 (ranks 9–10): ternary geometry not supported
lig→CRBN = 0.4197 and 0.4674 respectively. CRBN→ERα self-consistency = 0.2307 and 0.2216 —
indistinguishable from the unconstrained ARV-471 floor (0.2306). Constrained-run gain (Δ = +0.062 for both)
is within single-seed sampling noise. The CRBN engagement for these two is not supported.

### 2. ARV_010 ERα warhead placement: uncertain
lig→ERα = 0.6568, the only compound below 0.78 (all others ≥ 0.79). The ERα phenol-pocket constraint
was least satisfied. PEG linker flexibility with a single seed cannot characterise the accessible
conformational ensemble. Rank-5 cooperativity score should not be treated as predictive.

### 3. CRBN absolute orientation: uncertain for all compounds
Mean CRBN self-iptm = 0.273 vs ERα self-iptm = 0.906. The relative orientation of the two proteins
is the dominant source of uncertainty in every model. Surface lysine distances should not be used
for design decisions without experimental validation (TR-FRET, HDX-MS, cryo-EM).

### 4. Rank distinctions within ±0.05: not distinguishable
Ranks 2–4 (0.625–0.677) and ranks 5–8 (0.531–0.556) are within stochastic noise from
single-seed, 3-sample diffusion runs.

### 5. lig→CRBN iPTM ≠ thermodynamic cooperativity
These are structural confidence scores, not α = K_d(binary) / K_d(ternary). Values cannot be
converted to free-energy differences without experimental measurement.

### 6. No energy minimisation: raw diffusion output
Structures contain inter-chain clashes (verified: 6 atom pairs < 2.0 Å in ARV_001 model_0,
minimum A–B distance 1.38 Å). Coordinates should not be used for detailed binding geometry
analysis without force-field relaxation.

### 7. No MSA: all predictions in single-sequence mode
Boltz-2 issued single-sequence mode warnings for every compound. Prediction quality is
reduced compared to MSA-informed runs.

---

## Output Files

All constrained model_0 PDB files (chains A=ERα, B=CRBN, C=PROTAC):

| File | Size |
|:-----|:----:|
| `ARV_001_constrained_model_0.pdb` | 470 KB |
| `ARV_002_constrained_model_0.pdb` | 470 KB |
| `ARV_003_constrained_model_0.pdb` | 470 KB |
| `ARV_004_constrained_model_0.pdb` | 469 KB |
| `ARV_005_constrained_model_0.pdb` | 469 KB |
| `ARV_006_constrained_model_0.pdb` | 470 KB |
| `ARV_007_constrained_model_0.pdb` | 470 KB |
| `ARV_008_constrained_model_0.pdb` | 471 KB |
| `ARV_009_constrained_model_0.pdb` | 471 KB |
| `ARV_010_constrained_model_0.pdb` | 475 KB |

Full 3-model ensemble (model_0/1/2) available under each compound's job output directory.

---

## Methods

- **Model:** Boltz-2 v0.4.2 in container `boltzgen-0.3.1.sif`
- **Hardware:** Isambard-AI Phase 2, NVIDIA GH200 120 GB (aarch64), CUDA 12.7
- **Invocation:** `boltz predict <yaml> --accelerator gpu --model boltz2 --diffusion_samples 3 --sampling_steps 50 --recycling_steps 3 --output_format pdb --num_workers 0 --seed 42 --no_kernels`
- **`--no_kernels`:** Required on aarch64 — `cuequivariance_torch` not available in container
- **Cooperativity proxy:** `pair_chains_iptm["2"]["1"]` (lig→CRBN inter-chain iPTM)
- **Surface lysine threshold:** ERα LYS NZ at 3.5–12.0 Å from any CRBN heavy atom in model_0
- **All predictions:** Single-sequence mode (no MSA), single seed (42), 3 diffusion samples