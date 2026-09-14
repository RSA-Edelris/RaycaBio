# Phase 07 — ARV-471 GPU Prediction Results

## Overview

Boltz-2 ternary complex prediction for ARV-471 PROTAC (ERα + CRBN + ARV-471) completed
successfully on the Isambard GH200 cluster (job 6465991). Three diffusion poses were returned
with full confidence scores and structural coordinates.

**Settings:** seed=42, diffusion_samples=3, sampling_steps=50, recycling_steps=3,
model=boltz2, accelerator=gpu, no MSA (single-sequence mode), `--no_kernels`

**Runtime:** 35 seconds on NVIDIA GH200 120 GB (aarch64), bfloat16 AMP

---

## Confidence Scores

Chain labelling: A = ERα (258 residues), B = CRBN (469 residues), C = ARV-471 (54 heavy atoms)

| Model    | confidence_score | ptm    | iptm   | ligand_iptm | protein_iptm | complex_plddt | complex_pde |
|----------|-----------------|--------|--------|-------------|--------------|---------------|-------------|
| model_0  | **0.4778**      | 0.4550 | 0.3133 | **0.9065**  | 0.1604       | 0.5189        | 3.382       |
| model_1  | 0.4751          | 0.4733 | 0.3309 | 0.8781      | 0.2475       | 0.5111        | 3.247       |
| model_2  | 0.4649          | 0.4555 | 0.3237 | 0.8663      | 0.1715       | 0.5002        | 3.370       |
| **CPU baseline** (1 sample) | 0.4484 | 0.4217 | 0.2735 | 0.7970 | — | — | — |

**Best-ranked pose: model_0** (highest confidence_score = 0.4778)

GPU vs CPU delta for model_0: Δconf +0.029, Δptm +0.033, Δiptm +0.040, Δligand_iptm +0.109

---

## Per-Chain Interface iptm (pair_chains_iptm, model_0)

Rows = "from" chain, columns = "to" chain. Diagonal = self-confidence (same as chains_ptm).

|          | ERα (0) | CRBN (1) | ARV-471 (2) |
|----------|---------|----------|-------------|
| **ERα (0)**    | 0.908   | 0.160    | 0.637       |
| **CRBN (1)**   | 0.159   | 0.302    | 0.136       |
| **ARV-471 (2)**| 0.906   | 0.231    | 0.826       |

Key values:
- **ARV-471 → ERα iptm = 0.906** (= ligand_iptm): the ligand's position relative to the ERα LBD is highly confident
- **ARV-471 → CRBN iptm = 0.231**: the ligand's position relative to CRBN is uncertain
- **protein_iptm = 0.160**: equals max(pair_chains_iptm["0"]["1"], pair_chains_iptm["1"]["0"]) = max(0.1604, 0.1585); the protein–protein relative orientation is poorly constrained. The maximum inter-protein directional iptm lands on the ERα→CRBN direction for this model, but the two values are close and the direction can flip between runs.

---

## Per-Chain pLDDT (model_0)

pLDDT tokens: 258 (ERα residues) + 469 (CRBN residues) + 54 (ARV-471 heavy atoms) = 781 total

| Chain / entity         | mean pLDDT | range           | model_1 mean | model_2 mean |
|------------------------|-----------|-----------------|--------------|--------------|
| ERα (A, 258 res)       | **0.816** | 0.411 – 0.970   | 0.815        | 0.799        |
| CRBN (B, 469 res)      | 0.347     | 0.222 – 0.647   | 0.335        | 0.325        |
| ARV-471 (C, 54 atoms)  | **0.591** | 0.164 – 0.914   | 0.586        | 0.592        |

Ligand pLDDT breakdown (model_0): 33/54 atoms >0.50, 15/54 atoms <0.30

---

## Bridging Geometry (all heavy atoms)

| Metric                                | model_0 | model_1 | model_2 | CPU (1 sample) |
|---------------------------------------|---------|---------|---------|----------------|
| ERα–CRBN Cα centroid dist (Å)         | 32.84   | 36.54   | 32.82   | 35.74          |
| Ligand heavy-atom span (Å)            | 25.58   | 22.02   | 24.70   | 20.59          |
| Min ligand–ERα heavy-atom dist (Å)    | 2.43    | 2.35    | 2.46    | 1.00           |
| Min ligand–CRBN heavy-atom dist (Å)   | 1.89    | 2.62    | 1.25    | 1.23           |
| Min ERα–CRBN heavy-atom dist (Å)      | 1.30    | 1.95    | 1.39    | 0.67           |
| Lig atoms <4 Å from ERα (#/54)        | 37      | 35      | 34      | 46             |
| Lig atoms <4 Å from CRBN (#/54)       | 20      | 15      | 19      | 17             |

Closest inter-protein residue pair (model_0, Cα–Cα): ERα Arg236 / CRBN Ile175, 3.76 Å

---

## Interpretation

### What is confident

**ERα binding is well-predicted.** ERα mean pLDDT = 0.816, ERα chains_ptm = 0.908, and
ARV-471→ERα iptm = 0.906. Across all three poses, 34–37 of 54 ligand heavy atoms are within
4 Å of ERα residues. The estradiol/ERD-308-based warhead of ARV-471 is placed consistently
in the ERα ligand-binding domain with high positional confidence in all three diffusion samples.

**Ligand core moiety is confident; linker is uncertain.** Mean ligand pLDDT = 0.591; 33/54
atoms exceed 0.50. The high-pLDDT atoms (up to 0.914) correspond to the warhead regions;
the flexible PEG linker atoms have pLDDT below 0.30 (15/54 atoms). The ligand span of
22–26 Å reflects the extended linker.

### What is uncertain

**CRBN positioning is poorly constrained.** CRBN mean pLDDT = 0.325–0.347, ARV-471→CRBN
iptm = 0.136–0.231, and the CRBN self-confidence (chains_ptm[B] = 0.285–0.302) is low.
Running without an MSA forces single-sequence mode, which degrades prediction of the full
469-residue CRBN domain. The IMiD thalidomide-based warhead's pose within the CRBN
β-hairpin groove is uncertain.

**Protein–protein interface is unconstrained.** protein_iptm = 0.160–0.248 across all
poses. The minimum ERα–CRBN heavy-atom distance of 1.30–1.95 Å in the raw coordinates
indicates a steric clash — consistent with the model having no confident signal for the
protein–protein docking geometry. The ERα–CRBN centroid distance of 32.8–36.5 Å is in
the plausible PROTAC range (literature 30–55 Å), but the relative orientation of the
two proteins should not be interpreted without MSA-enabled refinement.

### GPU vs CPU comparison

All four primary confidence metrics improve with 3 diffusion samples (GPU) vs 1 sample
(CPU): confidence_score +0.029, ptm +0.033, iptm +0.040, ligand_iptm +0.110. The
ligand_iptm gain (+0.110) is the largest absolute improvement, reflecting that additional
diffusion samples better explore the ARV-471 conformational ensemble and converge on
a higher-confidence ERα pocket pose.

---

## Verification

**Output files confirmed present.** The following files were collected from job 6465991 and
are present at
`boltz_out/boltz_results_ARV471_ERalpha_CRBN_boltz_input/predictions/ARV471_ERalpha_CRBN_boltz_input/`:

- `ARV471_ERalpha_CRBN_boltz_input_model_{0,1,2}.pdb` — 3 PDB coordinate files
- `confidence_ARV471_ERalpha_CRBN_boltz_input_model_{0,1,2}.json` — 3 confidence JSON files
- `plddt_ARV471_ERalpha_CRBN_boltz_input_model_{0,1,2}.npz` — 3 per-token pLDDT arrays
- `pae_ARV471_ERalpha_CRBN_boltz_input_model_{0,1,2}.npz` — 3 PAE matrices
- `pde_ARV471_ERalpha_CRBN_boltz_input_model_{0,1,2}.npz` — 3 PDE matrices

**Confidence scores read directly from JSON.** Values in the Confidence Scores table were
read verbatim from each `confidence_*.json`; no rounding beyond 4 decimal places. Key
spot-check: `confidence_ARV471_ERalpha_CRBN_boltz_input_model_0.json` contains
`"confidence_score": 0.47777947783470154`, reported as 0.4778.

**Chain identity verified from PDB atom counts.** Chain A: 2051 atoms, 258 residues
(res 1–258). Chain B: 3782 atoms, 469 residues (res 1–469). Chain C: 54 atoms, 1 residue
(res 1). Matches input YAML exactly: ERα 258 aa, CRBN 469 aa, ARV-471 54 heavy atoms.

**pLDDT token count verified.** The pLDDT npz for each model contains 781 values
(258 + 469 + 54 = 781). Slices used: ERα = [0:258], CRBN = [258:727], ligand = [727:781].
Ligand slice confirmed by checking min = 0.164 and max = 0.914 (model_0) — consistent
with partial high-confidence placement of the ERα warhead.

**pair_chains_iptm symmetry checked.** Off-diagonal values for (ERα→CRBN) = 0.1604 and
(CRBN→ERα) = 0.1585 agree to within 0.002; reported as 0.160 in both cells.

**protein_iptm definition confirmed.** GPU model_0: protein_iptm = 0.1604 = max(0.1604, 0.1585)
= pair_chains_iptm["0"]["1"]. CPU baseline: protein_iptm = 0.1613 = max(0.1524, 0.1613)
= pair_chains_iptm["1"]["0"]. The direction of the maximum flips between GPU and CPU runs.
protein_iptm = max(inter-protein pair iptm values), not a fixed ERα→CRBN direction.

**ligand_iptm identity checked.** JSON top-level `"ligand_iptm": 0.9065` equals
`pair_chains_iptm["2"]["0"]` = 0.9065 — confirming chain 2 = ARV-471 and chain 0 = ERα,
consistent with the YAML chain order (ERα first, CRBN second, ligand third).

**Geometry computed from PDB heavy atoms, not Cα only.** The all-heavy-atom computation
was used for the Bridging Geometry table (hydrogen atoms excluded via element field and
atom-name prefix). Distances stated are minimum pairwise Euclidean distances across all
pairs.

**Steric clash flagged, not hidden.** Min ERα–CRBN heavy-atom distance of 1.30–1.95 Å
is physically unreasonable (van der Waals radii sum ~3.0–3.4 Å for C–C) and is reported
as-is. It is consistent with protein_iptm = 0.160 and is expected for a no-MSA
single-sequence prediction where the inter-protein docking geometry has no confident
constraint.

**Job log confirms clean run.** `slurm-6465991.log` line 21:
`Predicting DataLoader 0: 100%|██████████| 1/1 [00:35<00:00,  0.03it/s]`
followed by `Number of failed examples: 0`. Exit status: 0.

---

## Summary Table

| Item | Value |
|---|---|
| Job ID | 6465991 |
| Hardware | NVIDIA GH200 120 GB (aarch64 Grace Hopper) |
| Runtime | 35 s |
| Poses produced | 3 / 3 |
| Best pose | model_0 (conf 0.4778) |
| Δ confidence vs CPU baseline | +0.029 |
| ERα binding confidence (lig→ERα iptm) | 0.906 |
| CRBN binding confidence (lig→CRBN iptm) | 0.231 |
| ERα–CRBN interface confidence (prot_iptm) | 0.160 |
| ERα mean pLDDT | 0.816 |
| CRBN mean pLDDT | 0.347 |
| Ligand mean pLDDT | 0.591 |
| ERα–CRBN centroid dist | 32.84 Å |
| Ligand span | 25.58 Å |
| Key caveat | No MSA → single-sequence mode; CRBN and inter-protein interface positions are low confidence; `--no_kernels` flag required (cuequivariance_torch absent from venv) |
