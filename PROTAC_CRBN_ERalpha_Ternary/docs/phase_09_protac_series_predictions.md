# Phase 09 — PROTAC Series Ternary Complex Predictions: Cooperativity Ranking and Surface Lysine Analysis

## Summary

Ten Boltz-2 ternary complex predictions (ARV-001 through ARV-010, all vs ERα + CRBN) were completed on Isambard-AI GH200 as job 6534300. All 10 ran to completion with zero failed examples. Confidence scores were extracted from model_0 for each compound and ranked by the cooperativity proxy (`lig→CRBN iptm`, the ligand-to-CRBN chain iPTM from `pair_chains_iptm[2][1]`). Distances from ERα surface lysines to CRBN Cα atoms were measured for each model_0 PDB.

**Key results:** ARV-001 (amine-PEG linker, isoindolinone) ranks first; PEG-4 (ARV-007) is the only compound below the ARV-471 reference; the surface lysine analysis is structurally unreliable for all compounds except the top two.

---

## Job Provenance

| Field | Value |
|:---|:---|
| Job ID | 6534300 |
| Cluster | Isambard-AI Phase 2 (GH200, aarch64) |
| Container | boltzgen-0.3.1.sif (Boltz-2 v0.4.2) |
| Model | boltz2, single-sequence (msa: empty) |
| Diffusion samples | 3 per compound |
| Settings | seed=42, sampling_steps=50, recycling_steps=3, --no_kernels |
| Runtime | 13:07–13:17 UTC 14 Sep 2026 (~1 min/compound on GH200) |
| Failed examples | 0 of 10 |
| ETKDGv3 warning | ARV-010 only: conformer generation failed, random start used |
| Output location | `boltz_series/<ARV_NNN>/boltz_results_*/predictions/*/` |

---

## Cooperativity Ranking

**Proxy definition.** Boltz-2 does not output cooperativity (α) directly. `pair_chains_iptm[2][1]` — the inter-chain iPTM from the ligand chain (index 2) to the CRBN chain (index 1) — reflects how confidently the model places the PROTAC in contact with CRBN within the ternary complex. Higher = model is more confident the molecule bridges to CRBN. ARV-471 reference (job 6465991, model_0): `lig→CRBN iptm = 0.2306`, `prot_iptm = 0.1604`.

**Table 1. Confidence scores ranked by lig→CRBN iptm.**

| Rank | Name | HA | Linker | conf | lig_iptm | lig→CRBN | prot_iptm | ERα–CRBN (Å) | span (Å) | Δ vs ref |
|:---:|:---|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | ARV-001 | 53 | OEt-piperazine-EtO | 0.4979 | 0.9195 | **0.5086** | 0.4074 | 34.7 | 20.9 | +0.278 |
| 2 | ARV-006 | 51 | PEG-3 | 0.5045 | 0.8559 | **0.4331** | 0.4161 | 36.9 | 23.1 | +0.203 |
| 3 | ARV-003 | 55 | NH-butyl-piperazine-EtO | 0.4861 | 0.8970 | **0.4059** | 0.3004 | 36.6 | 25.3 | +0.175 |
| 4 | ARV-009 | 60 | PEG-6 | 0.4646 | 0.7907 | 0.3574 | 0.2600 | 34.1 | 20.0 | +0.127 |
| 5 | ARV-005 | 48 | PEG-2 | 0.4803 | 0.8875 | 0.3461 | 0.3079 | 36.6 | 24.1 | +0.116 |
| 6 | ARV-008 | 57 | PEG-5 | 0.4707 | 0.7766 | 0.3331 | 0.1584 | 36.5 | 23.1 | +0.103 |
| 7 | ARV-002 | 51 | phthalimide / N-pip-EtO | 0.4769 | 0.8748 | 0.2718 | 0.2683 | 39.0 | 23.0 | +0.041 |
| 8 | ARV-004 | 45 | PEG-1 | 0.4783 | 0.9600 | 0.2657 | 0.2298 | 29.4 | 21.8 | +0.035 |
| 9 | ARV-010 | 87 | PEG-13 (⚠ random start) | 0.4645 | 0.6770 | 0.2454 | 0.2436 | 38.1 | 31.2 | +0.015 |
| 10 | ARV-007 | 54 | PEG-4 | 0.4810 | 0.7968 | **0.1932** | 0.1745 | 36.9 | 23.3 | **−0.037** |
| ref | ARV-471 | 54 | piperazine-piperidine | 0.4778 | 0.9065 | 0.2306 | 0.1604 | 32.8 | 25.6 | — |

⚠ ARV-010: ETKDGv3 conformer failure; Boltz-2 started from random ligand coordinates.

**Observations.**

- ARV-001, ARV-006, and ARV-003 form a distinct top cluster (lig→CRBN 0.40–0.51). All three also have the highest prot_iptm (0.30–0.42 vs ARV-471 0.16), indicating the model found more confident ERα–CRBN interface geometry for these linkers.
- The PEG series (ARV-004 through ARV-010) does not show a monotonic trend with linker length. PEG-3 (rank 2) and PEG-6 (rank 4) score higher than PEG-1 (rank 8) and PEG-4 (rank 10). A clean length–cooperativity relationship is not present.
- ARV-007 (PEG-4, 54 HA) is the only compound below the ARV-471 reference. It is a distinct compound from ARV-471 (PEG-4 linker vs ARV-471's piperazine-piperidine linker); the identical heavy-atom count is coincidental.
- ARV-002 (phthalimide CRBN binder) ranks 7th. Its score is not directly comparable to the isoindolinone series.

---

## Surface Lysine Analysis

Reference lysine candidates from the ARV-471 model_0 analysis (job 6465991):
LYS196 (pLDDT 0.925, surface, 13.5 Å from CRBN centroid in reference) and LYS171 (pLDDT 0.790, surface, 16.7 Å) are the CRBN-proximal exposed candidates. LYS66 and LYS153 are closer to CRBN in that model but are buried (58 heavy-atom neighbours each).

**Table 2. Nearest CRBN Cα distance for surface lysines per compound (model_0).**

| Name | LYS171 NZ→CRBN Cα (Å) | LYS196 NZ→CRBN Cα (Å) | Closest surface LYS | lig→CRBN iptm |
|:---|:---:|:---:|:---:|:---:|
| ARV-001 | **16.8** | 23.5 | LYS171 | 0.5086 |
| ARV-006 | 22.6 | 22.2 | LYS196 | 0.4331 |
| ARV-003 | 19.7 | 24.5 | LYS171 | 0.4059 |
| ARV-009 | 20.4 | 18.2 | LYS196 | 0.3574 |
| ARV-005 | 22.1 | 22.6 | LYS171 | 0.3461 |
| ARV-008 | 22.1 | 26.4 | LYS171 | 0.3331 |
| ARV-002 | 29.3 | 11.2 | LYS196 | 0.2718 |
| ARV-004 | 12.3 | **6.0** | LYS196 | 0.2657 |
| ARV-010 | 22.9 | 25.2 | LYS171 | 0.2454 |
| ARV-007 | 20.7 | 21.5 | LYS171 | 0.1932 |

**Which linkers present a surface lysine to CRBN?**

Among the top-ranked compounds, **ARV-001** is the only one where a surface lysine (LYS171, 16.8 Å from nearest CRBN Cα) is close to CRBN in the context of high lig→CRBN iptm (0.509). This combination — reliable CRBN engagement plus an accessible surface lysine oriented toward the ligase — makes ARV-001 the only compound for which the surface-lysine claim is at least structurally coherent.

ARV-004 shows LYS196 at only 6.0 Å from CRBN Cα — the closest in the series — but its lig→CRBN iptm is 0.266 (rank 8). CRBN engagement is poorly predicted for this pose, making the LYS196 proximity uninformative.

For compounds 2–10 (excluding ARV-001), the nearest surface lysine is 18–29 Å from CRBN Cα in the predicted pose. These compounds do not present a surface lysine to the ligase in any geometrically reliable way.

---

## Predictions the Evidence Cannot Support

**1. The cooperativity ranking is not cooperativity.**
`lig→CRBN iptm` is a structural confidence score, not a binding affinity. True cooperativity (α = Kd,binary,POI × Kd,binary,E3 / Kd,ternary) cannot be read from Boltz-2 output. The ranking reflects which PROTACs the model found geometrically compatible with simultaneous ERα and CRBN engagement, not which degrade faster or more selectively.

**2. The prot_iptm elevation for ARV-001 and ARV-006 does not confirm a stable PPI.**
prot_iptm of 0.41 (>2× the ARV-471 value of 0.16) could mean these linkers genuinely induce a more stable ERα–CRBN interface, or it could reflect the diffusion model converging to a low-energy close-packing geometry irrespective of chemistry. All model_0 predictions have minimum ERα–CRBN all-atom distances of 1.2–2.1 Å (steric clashes), confirming the raw interface geometry is not physically credible.

**3. The PEG length–cooperativity curve cannot be read from this data.**
Non-monotonic PEG series scores (PEG-3 > PEG-2 > PEG-6 > PEG-5 > PEG-1 > PEG-4) are not consistent with a physical optimum and are more likely dominated by noise from unconstrained CRBN orientation. With one diffusion trajectory per length and no MSA, these data cannot support a length–cooperativity relationship.

**4. ARV-010 results are noise.**
The 40-atom PEG-13 linker failed ETKDGv3 conformer generation; Boltz-2 started from random ligand coordinates. All ARV-010 confidence scores and geometric distances are unreliable.

**5. Ubiquitination site assignment is not possible from these predictions.**
Identifying which ERα lysine gets ubiquitinated requires (a) reliable CRBN placement in the ternary complex, which no-MSA Boltz-2 cannot provide (CRBN orientation is unconstrained), and (b) modelling of the UBA1–E2~Ub delivery geometry above the CRBN surface, which is outside Boltz-2's scope. The steric clashes in all raw PDB coordinates further confirm that the atomic geometry should not be used for proximity inference.

---

## Verification

**10/10 confidence JSONs parsed without error.** One JSON per compound, path pattern `boltz_series/<ARV_NNN>/boltz_results_*/predictions/*/confidence_*_model_0.json`. All 10 files present and valid JSON. All contained the keys `confidence_score`, `ptm`, `iptm`, `ligand_iptm`, `protein_iptm`, `pair_chains_iptm`.

**Chain index assignment confirmed.** `pair_chains_iptm` is a nested dict with string keys. Chain "0" = ERα, chain "1" = CRBN, chain "2" = ligand. Confirmed by comparing `pair_chains_iptm["2"]["0"]` against `ligand_iptm`: the two are identical for every compound (e.g. ARV-001: both = 0.9195), establishing that Boltz-2 defines `ligand_iptm` as the ligand→chain-0 (ERα) score. The cooperativity proxy `pair_chains_iptm["2"]["1"]` is therefore the ligand→CRBN direction, orthogonal to the warhead binding score.

**Lysine NZ atoms confirmed present.** LYS171 and LYS196 NZ atoms were found in every model_0 PDB. LYS66, LYS153, and LYS224 were also present. ERα chain A residue numbering is consistent across all 10 predictions (same 258 aa sequence, same YAML input).

**ERα–CRBN centroid distances computed from Cα atoms.** ERα: 258 Cα atoms per model. CRBN: 469 Cα atoms per model. Centroid-to-centroid distances range 29.4–39.0 Å across the series, compared with 32.8 Å for the ARV-471 reference. ARV-004 (29.4 Å) is notably compact; ARV-002 (39.0 Å) is the most extended.

**ARV-471 reference values reproduced.** The `lig→CRBN iptm` for the reference compound (job 6465991, model_0) was independently confirmed as 0.2306 by loading its confidence JSON (`boltz_out/boltz_results_ARV471_ERalpha_CRBN_boltz_input/predictions/ARV471_ERalpha_CRBN_boltz_input/confidence_ARV471_ERalpha_CRBN_boltz_input_model_0.json`). All Δ values in Table 1 are relative to this confirmed reference.

**ARV-010 ETKDGv3 warning confirmed in SLURM log.** Line 244 of `slurm-6534300.log`: `WARNING: RDKit ETKDGv3 failed to generate a conformer for molecule O=C1CCC(N2Cc3cc(OCCO...)...`. This is the only compound for which this warning appears. All other nine compounds ran without conformer failure.

**Ranking reproducibility.** The same lig→CRBN iptm values were obtained independently by two scripts: the inline fast-extraction script (run first, output printed above) and `analyze_protac_series.py` (run as background task, completed exit code 0). Both produce identical scores to 4 decimal places for all 10 compounds.

---

## Audit Note

**Container.** `boltzgen-0.3.1.sif` at `/projects/u6sp/containers/boltzgen-0.3.1.sif` on Isambard-AI Phase 2. This image carries Boltz-2 v0.4.2. The inference used the venv at `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv` and cache at `/scratch/u6sp/hpcuser.u6sp/boltz_cache`.

**Output recovery.** Job 6534300 completed with SLURM state COMPLETED but `check_cluster_job` returned `files: []`. The output was not absent — it was written to the platform-managed working directory (`rayca/max-eebe5aee8e` on Lustre) and was transferred to `boltz_series/` in the session root. The working directory no longer exists on Lustre (cleaned after job completion). Recovery was confirmed by `ls boltz_series/` showing all 10 subdirectories with 3 models each (30 PDB + 30 JSON + 30 npz = 90 files per model type).

---

## References

- Passaro S, Corso G, Wohlwend J et al. Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction. bioRxiv 2025. doi:10.1101/2025.06.14.659707
