---
title: "Phase 2: Create Boltz-2 YAML inputs and submit 10 PROTAC ternary complex jobs"
study_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-eebe5aee8e"
phase_index: 2
phase_id: "2"
phase_goal: "Create Boltz-2 YAML inputs and submit 10 PROTAC ternary complex jobs"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 2: Create Boltz-2 YAML inputs and submit 10 PROTAC ternary complex jobs

## Summary

Generated ten Boltz-2 YAML input files (ARV_001 through ARV_010) from the SMILES
extracted in Phase 1, combined with the shared ERα (258 aa) and CRBN (469 aa) sequences
from the ARV-471 reference YAML. Submitted all ten as a single batch job (Isambard job
6534300) on the GH200 cluster using identical settings to the successful ARV-471 reference
job (6465991). Also wrote `analyze_protac_series.py`, the post-processing script for
parsing Boltz-2 confidence JSONs and ranking by cooperativity proxy.

## Objective

Create Boltz-2 YAML inputs and submit 10 PROTAC ternary complex jobs

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 (local) |
| Cluster | Isambard-AI Phase 2 GH200 (aarch64) |

### Software and Databases

**Table R.** Key resources used in this phase.

| Resource | Type | Version | Notes |
| :--- | :--- | :--- | :--- |
| Boltz-2 | software | 0.4.2 | via boltzgen-0.3.1.sif container; `boltz_predict_venv` on Isambard |
| boltz_run.py | script | session | Tensorboard stub + `boltz.main.cli()` wrapper; handles cuequivariance_torch absence |

### Procedure

#### 1. YAML input generation

A Python script was used to generate one YAML per compound. Each YAML encodes:
- `protein A`: ERα (258 aa sequence, `msa: empty`)
- `protein B`: CRBN (469 aa sequence, `msa: empty`)
- `ligand C`: compound-specific canonical SMILES from Phase 1

The ERα and CRBN sequences were taken verbatim from `ARV471_ERalpha_CRBN_boltz_input.yaml`
(the reference YAML, itself verified against job 6465991 model_0). YAML format is Boltz-2
version 1 input format; `msa: empty` disables MSA for single-sequence prediction.

#### 2. Cluster job submission

Eleven input files were staged to Isambard (`boltz_run.py` + 10 YAMLs). The batch script
looped over all 10 YAMLs and ran Boltz-2 prediction on each, activating
`boltz_predict_venv` from `/scratch/u6sp/hpcuser.u6sp/` and using
`/scratch/u6sp/hpcuser.u6sp/boltz_cache` as the Boltz-2 cache directory.

| Field | Value |
| :--- | :--- |
| Job ID | 6534300 |
| Cluster | Isambard-AI Phase 2 (GH200, aarch64) |
| Container | boltzgen-0.3.1.sif |
| Status at submission | submitted/queued |

Prediction parameters (identical to reference job 6465991):

```yaml
accelerator: gpu
model: boltz2
diffusion_samples: 3
sampling_steps: 50
recycling_steps: 3
output_format: pdb
num_workers: 0
seed: 42
no_kernels: true    # required: cuequivariance_torch absent on aarch64
```

**Rationale for `--no_kernels`.** Isambard GH200 is aarch64; the `cuequivariance_torch`
package that provides fused equivariant kernels is x86-only and absent. Without
`--no_kernels` Boltz-2 raises an import error and exits. This flag was identified from
the reference job failure logs and confirmed by job 6465991 (which succeeded with it).

#### 3. Post-processing script

`analyze_protac_series.py` was written in anticipation of job 6534300 results. It parses
confidence JSON files and PDB outputs from the Boltz-2 `boltz_series/` output directory
and extracts: `confidence_score`, `ptm`, `iptm`, `lig→ERα iptm` ([2][0]),
`lig→CRBN iptm` ([2][1]) as cooperativity proxy, `protein_iptm`, centroid distance,
ligand span, and contact counts. Compounds are ranked by `lig→CRBN iptm` descending.

## Results

### YAML files produced

Ten Boltz-2 YAML files, one per compound, verified by round-trip before staging to Isambard.

| File | SMILES HA | SHA-256 (first 12) |
| :--- | :--- | :--- |
| ARV_001_ERalpha_CRBN_boltz_input.yaml | 53 | 7bf6e32eac79... |
| ARV_002_ERalpha_CRBN_boltz_input.yaml | 51 | 7a69fdeebee4... |
| ARV_003_ERalpha_CRBN_boltz_input.yaml | 55 | 2033828ac9dc... |
| ARV_004_ERalpha_CRBN_boltz_input.yaml | 45 | 278f3947b9c7... |
| ARV_005_ERalpha_CRBN_boltz_input.yaml | 48 | 9c519bd578fa... |
| ARV_006_ERalpha_CRBN_boltz_input.yaml | 51 | 332974848224... |
| ARV_007_ERalpha_CRBN_boltz_input.yaml | 54 | 7fbb377afd7b... |
| ARV_008_ERalpha_CRBN_boltz_input.yaml | 57 | aae01f04c5f0... |
| ARV_009_ERalpha_CRBN_boltz_input.yaml | 60 | 8a346619af47... |
| ARV_010_ERalpha_CRBN_boltz_input.yaml | 87 | e01fdc8b567c... |

### Cluster job

**Job 6534300** submitted to Isambard-AI Phase 2 (GH200, aarch64). Job was in the SLURM
queue at phase close. Prediction outputs are consumed by Phase 3 (Collect confidence
scores and rank by cooperativity proxy).

### Output Artifacts

**Table A.** Files produced by this phase.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| ARV_001_ERalpha_CRBN_boltz_input.yaml | YAML | 994 B | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/inputs | 7bf6e32eac79... |
| ARV_002_ERalpha_CRBN_boltz_input.yaml | YAML | 995 B | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/inputs | 7a69fdeebee4... |
| ARV_003_ERalpha_CRBN_boltz_input.yaml | YAML | 996 B | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/inputs | 2033828ac9dc... |
| ARV_004_ERalpha_CRBN_boltz_input.yaml | YAML | 982 B | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/inputs | 278f3947b9c7... |
| ARV_005_ERalpha_CRBN_boltz_input.yaml | YAML | 985 B | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/inputs | 9c519bd578fa... |
| ARV_006_ERalpha_CRBN_boltz_input.yaml | YAML | 988 B | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/inputs | 332974848224... |
| ARV_007_ERalpha_CRBN_boltz_input.yaml | YAML | 991 B | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/inputs | 7fbb377afd7b... |
| ARV_008_ERalpha_CRBN_boltz_input.yaml | YAML | 994 B | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/inputs | aae01f04c5f0... |
| ARV_009_ERalpha_CRBN_boltz_input.yaml | YAML | 997 B | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/inputs | 8a346619af47... |
| ARV_010_ERalpha_CRBN_boltz_input.yaml | YAML | 1.0 KB | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/inputs | e01fdc8b567c... |
| analyze_protac_series.py | PY | 8.4 KB | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/source | c3eed540af8f... |
| phase_08_protac_series_smiles_extraction.md | MD | 7.6 KB | 02_create_boltz_2_yaml_inputs_and_submit_10_protac_/reports | c68a320668c1... |

## Verification

**YAML round-trip.** Each YAML was re-parsed after writing; SMILES in the `ligand` block
was re-loaded with RDKit and heavy-atom count confirmed to match the Phase 1 table. All
10 passed.

**Sequence identity.** ERα (258 aa) and CRBN (469 aa) sequences in all 10 YAMLs are byte-
for-byte identical to `ARV471_ERalpha_CRBN_boltz_input.yaml` (the reference confirmed by
job 6465991 model_0).

**Settings parity.** All 10 jobs use identical flags to job 6465991 (the successful
reference): seed=42, diffusion_samples=3, sampling_steps=50, recycling_steps=3,
output_format=pdb, num_workers=0, accelerator=gpu, --no_kernels. Confidence scores will be
directly comparable to the reference.

## Limitations

- Cluster job 6534300 was in the SLURM queue at phase close; prediction outputs do not
  yet exist. Phase 3 consumes the results when the job completes.
- ARV-002 has a phthalimide CRBN binder; its lig→CRBN iptm score is not directly
  comparable to the isoindolinone series (different CRBN pharmacophore).
- `msa: empty` disables coevolution information; this is standard for designed PROTACs but
  reduces per-residue pLDDT relative to natural protein pairs.
- Boltz-2 version 0.4.2 (boltzgen-0.3.1.sif). Boltz-2 does not directly predict
  cooperativity (α); lig→CRBN iptm is used as a proxy — see Phase 3 for the full
  derivation and its limitations.

## References

- Passaro S, Corso G, Wohlwend J et al. Boltz-2: Towards Accurate and Efficient Binding
  Affinity Prediction. bioRxiv 2025. doi:10.1101/2025.06.14.659707
