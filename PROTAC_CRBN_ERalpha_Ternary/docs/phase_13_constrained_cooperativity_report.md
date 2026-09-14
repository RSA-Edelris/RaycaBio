
## Summary

Ten PROTAC compounds (ARV_001–010) were modelled as ternary complexes against the CRBN–ERα best reference geometry using Boltz-2 v0.4.2 (job 6548359, GH200, seed 42, 3 diffusion samples). Dual pocket constraints enforced the glutarimide warhead into the CRBN thalidomide-binding pocket (14 residues) and the phenol warhead into the ERα LBD ligand-binding pocket (18 residues). All 10 compounds produced PDB and confidence output. Compounds are ranked here by **lig→CRBN inter-chain iPTM** (`pair_chains_iptm["2"]["1"]`), the best available proxy for cooperativity in a Boltz-2 single-seed run. The ARV-471 unconstrained reference (model_0, job 6465991) sets a floor at **0.2306**.

---

## 1. Cooperativity Ranking

Ranked by model_0 lig→CRBN iPTM. Δ is the gain over the unconstrained run for the same compound.

| Rank | Compound | conf | iptm | lig→ERα | lig→CRBN | prot_iptm | Δ unconstrained |
|:----:|:---------|-----:|-----:|--------:|---------:|----------:|----------------:|
| 1 | **ARV_005** | 0.5066 | 0.5265 | 0.9034 | **0.7181** | 0.5283 | +0.372 |
| 2 | **ARV_007** | 0.5161 | 0.6640 | 0.8748 | **0.6771** | 0.6633 | +0.484 |
| 3 | ARV_001 | 0.4934 | 0.5476 | 0.9267 | 0.6740 | 0.5227 | +0.165 |
| 4 | ARV_002 | 0.4886 | 0.5008 | 0.9337 | 0.6252 | 0.4763 | +0.353 |
| 5 | ARV_010 ⚠ | 0.5137 | 0.6161 | 0.6568 | 0.5555 | 0.6549 | +0.310 |
| 6 | ARV_004 | 0.4894 | 0.4953 | 0.9407 | 0.5519 | 0.4947 | +0.286 |
| 7 | ARV_008 | 0.4718 | 0.4063 | 0.8335 | 0.5349 | 0.3820 | +0.202 |
| 8 | ARV_006 | 0.4979 | 0.5100 | 0.8820 | 0.5308 | 0.5059 | +0.098 |
| 9 | ARV_003 | 0.4815 | 0.3759 | 0.8697 | 0.4674 | 0.2491 | +0.062 |
| 10 | ARV_009 | 0.4671 | 0.3709 | 0.7865 | 0.4197 | 0.3697 | +0.062 |

ARV-471 unconstrained reference (job 6465991): lig→CRBN = 0.2306.
All 10 constrained compounds exceed this reference.

**ARV_007 underwent the largest rank reversal**: rank 10 unconstrained (lig→CRBN = 0.1932) → rank 2 constrained (0.6771), a +0.484 gain. This indicates its warhead geometry is only productive when the CRBN pocket is explicitly constrained — the unconstrained run placed the ligand in an unproductive orientation.

---

## 2. Per-Chain Confidence

| Compound | ERα self-iptm | CRBN self-iptm | ERα→CRBN | CRBN→ERα |
|:---------|:------------:|:--------------:|:--------:|:--------:|
| ARV_001 | 0.9073 | 0.2834 | 0.5227 | 0.2807 |
| ARV_002 | 0.8993 | 0.2608 | 0.4763 | 0.2615 |
| ARV_003 | 0.9322 | 0.2871 | 0.2491 | 0.2216 |
| ARV_004 | 0.8900 | 0.2648 | 0.4947 | 0.2728 |
| ARV_005 | 0.9015 | 0.2623 | 0.5283 | 0.2499 |
| ARV_006 | 0.9175 | 0.3008 | 0.5059 | 0.2584 |
| ARV_007 | 0.8903 | 0.2774 | 0.6633 | 0.2835 |
| ARV_008 | 0.9055 | 0.2479 | 0.3820 | 0.2113 |
| ARV_009 | 0.9078 | 0.2638 | 0.3697 | 0.2307 |
| ARV_010 | 0.9123 | 0.2824 | 0.6549 | 0.2785 |
| **Mean** | **0.906** | **0.273** | | |

ERα fold is consistently high-confidence (self-iptm ≈ 0.91). CRBN self-iptm is uniformly low (≈ 0.27), reflecting genuine uncertainty in the CRBN conformation relative to ERα. The CRBN→ERα direction is the principal source of ambiguity in every model.

---

## 3. Surface Lysines Presented to the Ligase

ERα (chain A) lysines with NZ at 3.5–12.0 Å from any CRBN heavy atom in model_0. Distances < 3.5 Å are sub-threshold (compressed salt-bridge geometry in un-relaxed structures). The 12 Å outer shell captures residues on the CRBN-facing surface that are accessible to the E2 enzyme.

| Compound | lig→CRBN | Lysines within 3.5–12 Å of CRBN | Count |
|:---------|:--------:|:-------------------------------|:-----:|
| ARV_005 | 0.7181 | K233(5.0), K171(5.7), K224(6.2), K105(6.8), K7(7.4), K235(8.0), K153(8.7), K176(8.9), K185(10.2), K3(11.2) | 10 |
| ARV_007 | 0.6771 | K105(3.9), K171(4.1), K176(5.4), K224(5.8), K235(6.3), K3(7.8), K120(8.8), K185(9.9), K6(10.5), K153(10.8) | 10 |
| ARV_001 | 0.6740 | K235(3.5), K176(5.7), K153(6.6), K3(8.0), K7(8.0), K224(9.8), K6(10.5) | 7 |
| ARV_002 | 0.6252 | K224(4.6), K153(8.2), K7(8.3), K233(8.4), K3(9.4), K235(10.0), K171(10.5), K185(11.2) | 8 |
| ARV_010 | 0.5555 | K224(3.8), K7(4.0), K153(5.6), K171(6.5), K105(6.8), K3(6.9), K176(8.4), K233(8.5), K196(8.9), K185(9.3), K6(9.9), K235(9.9), K120(11.3) | 13 |
| ARV_004 | 0.5519 | K224(4.1), K233(5.6), K7(5.7), K171(6.1), K153(8.1), K185(8.2), K3(8.5), K235(10.5), K120(11.0), K6(11.5) | 10 |
| ARV_008 | 0.5349 | K7(3.7), K171(5.1), K233(7.3), K176(9.1), K153(9.3), K185(9.9) | 6 |
| ARV_006 | 0.5308 | K171(3.7), K176(3.8), K120(5.2), K3(6.4), K105(8.5), K6(10.4), K196(10.4), K235(10.4) | 8 |
| ARV_003 | 0.4674 | K233(6.7), K153(11.3), K235(11.4), K7(11.9) | 4 |
| ARV_009 | 0.4197 | K233(3.9), K66(4.4), K153(5.6), K171(6.7), K7(8.4), K6(8.9), K196(11.0) | 7 |

**All 10 linkers present at least one ERα surface lysine to CRBN.** The consistently presented lysines (≥ 8/10 compounds) are:

| ERα Lys | Compounds presented | Notes |
|:-------:|:-------------------:|:------|
| **K153** | 9/10 | Most consistent; absent only in ARV_006 |
| **K7** | 8/10 | Proximal (~3.7–11.9 Å) in all high-ranked compounds |
| **K171** | 8/10 | Closest in ARV_006 (3.7 Å) and ARV_007 (4.1 Å) |
| **K235** | 8/10 | Absent from ARV_006; closest in ARV_001 (3.5 Å) |

K233 (7/10), K176 (6/10), K224 (6/10), K3 (7/10), K6 (6/10), K185 (6/10) are linker-dependent. K66 appears only in ARV_009, and K120/K196/K105 appear in subsets.

The linker geometry modulates which of these lysines sits closest to CRBN, but no linker eliminates the presented-lysine set — the ERα LBD surface toward CRBN is rich in lysines.

---

## 4. Which Predictions the Evidence Cannot Support

### 4a. Cannot support — ARV_009 and ARV_003 (ranks 9–10)

lig→CRBN = 0.4197 and 0.4674. CRBN→ERα self-consistency = 0.2307 and 0.2216 — indistinguishable from the ARV-471 unconstrained floor (0.2306). prot_iptm = 0.370 and 0.249. The ternary geometry for these two compounds is not supported: the model reports near-baseline confidence that the ligand bridges to CRBN even when constrained. The constrained-run gain (Δ = +0.062 for both) is within sampling noise.

### 4b. Cannot support — ARV_010 warhead placement in ERα pocket

lig→ERα = 0.6568, the only compound below 0.78. Every other compound achieves lig→ERα ≥ 0.79. The ERα phenol-pocket constraint was least satisfied for ARV_010. The PEG linker's extreme flexibility means the model sampled one of many possible conformations; this single-seed, 3-sample run is insufficient to characterise the conformational ensemble. The rank-5 cooperativity score for ARV_010 should not be interpreted as predictive of ternary complex formation because the ERα warhead occupation is uncertain.

### 4c. Cannot support — absolute CRBN orientation for any compound

Mean CRBN self-iptm = 0.273 (range 0.248–0.301). ERα self-iptm = 0.906 (range 0.890–0.932). The model is confident about the ERα fold but not about where CRBN sits relative to it. CRBN→ERα inter-chain iptm (0.211–0.284) is the lowest value in the pair_chains_iptm matrix for every compound. The relative orientation of the two proteins, and therefore the geometry of the ternary complex interface, is the dominant uncertainty in all 10 predictions.

### 4d. Cannot support — ranking within ±0.05

The spread from ARV_001 (0.6740) to ARV_007 (0.6771) is 0.003; from ARV_004 (0.5519) to ARV_008 (0.5349) is 0.017. Given single-seed sampling with three diffusion samples and soft constraints, differences smaller than ~0.05 in lig→CRBN are within stochastic noise. Ranks 2–4 (0.6252–0.6771) and ranks 5–8 (0.5308–0.5555) are not distinguishable by this metric.

### 4e. Cannot support — converting lig→CRBN iPTM to thermodynamic cooperativity

lig→CRBN iPTM is a structural confidence score — how well the model believes the ligand bridges to CRBN in the predicted geometry. It is not α = Kd,binary / Kd,ternary. The ranking is informative for identifying which linkers adopt productive ternary geometries, but none of these values can be converted to free-energy differences without experimental validation (TR-FRET, SPR ternary, or HDX-MS).

---

## 5. Warhead Pocket Retention

Constraints enforced: glutarimide contacts to CRBN residues 111–114, 125, 240–241, 246, 249–250, 261, 263–264, 266; phenol contacts to ERα residues 47, 50, 53–54, 57, 88, 91–92, 95, 98, 108, 125, 128–129, 132, 225, 228–229 (`force: false`, `max_distance: 6.0 Å`).

The soft constraints (`force: false`) in Boltz-2 bias rather than enforce pocket placement. The high lig→ERα scores (≥ 0.88 for 9/10 compounds) indicate the phenol warhead was retained in the ERα pocket for all compounds except ARV_010. The lig→CRBN improvement over unconstrained runs (Δ > +0.06 for all 10) indicates the glutarimide warhead is engaging the CRBN pocket in constrained predictions. Neither warhead can be claimed as definitively placed without experimental structure or post-minimisation contact analysis.

---

## 6. Methods Note

- Model: Boltz-2 v0.4.2 in container `boltzgen-0.3.1.sif` on Isambard-AI Phase 2 (GH200 120 GB, aarch64)
- Parameters: `--diffusion_samples 3 --sampling_steps 50 --recycling_steps 3 --seed 42 --no_kernels`
- Chains: A = ERα LBD (258 aa), B = CRBN (469 aa), C = PROTAC ligand
- Cooperativity proxy: `pair_chains_iptm["2"]["1"]` (lig→CRBN inter-chain iPTM)
- Surface lysine threshold: ERα LYS NZ at 3.5–12.0 Å from any CRBN heavy atom; lower bound excludes compressed salt-bridge geometry artefacts in un-relaxed diffusion outputs (6 sub-2 Å clashes detected in ARV_001 model_0; minimum A–B distance 1.38 Å; consistent with DL output before force-field relaxation)
- No MSA: all predictions ran in single-sequence mode; Boltz-2 warned for every compound
