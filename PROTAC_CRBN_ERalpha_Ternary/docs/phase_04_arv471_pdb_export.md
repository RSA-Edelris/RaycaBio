---
title: "Phase 4: Export ARV-471 ternary complex PDB files (all three models)"
study_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
phase_goal: "Create PDB files for each of the three Boltz-2 diffusion models of ARV-471 + ERα + CRBN"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 4: Export ARV-471 ternary complex PDB files (all three models)

## Summary

The three Boltz-2 model PDB files for the ARV-471 / ERα / CRBN ternary complex (job 6465991,
Isambard-AI GH200, 11 Sep 2026) were copied from the original prediction subdirectory to the
session root under clean names. No structural modification was made. Confidence scores extracted
from the matching JSON files show that **model_1 has the highest lig→CRBN iptm (0.3496)**,
while model_0 has the highest overall confidence score (0.4778) — the two metrics disagree.

---

## Objective

Make the three diffusion samples for the reference compound (ARV-471) available as standalone
PDB files with names that do not embed the full Boltz-2 input stem. Required for downstream
visual inspection and structural comparison with the 10-compound PROTAC series.

---

## Methods

### Procedure

Source files were located in:

```
boltz_out/boltz_results_ARV471_ERalpha_CRBN_boltz_input/predictions/
  ARV471_ERalpha_CRBN_boltz_input/
    ARV471_ERalpha_CRBN_boltz_input_model_{0,1,2}.pdb
```

Each was copied to the session root with the name `ARV471_ERalpha_CRBN_model_{0,1,2}.pdb`.
No coordinates, B-factors, or chain assignments were altered.

---

## Results

### Output files

| File | Size | SHA-256 (full) |
|:---|:---:|:---|
| `ARV471_ERalpha_CRBN_model_0.pdb` | 471 KB | `3f250b3f28984288418e9bf94eac8a464f08b292a1f17475e2f2ee0f3497f67a` |
| `ARV471_ERalpha_CRBN_model_1.pdb` | 471 KB | `beb089602e3b91e908b027b657ecc096c51a158a6076722054449ce819584616` |
| `ARV471_ERalpha_CRBN_model_2.pdb` | 471 KB | `6c9b43b5600af6058e83cbba2ca2a97fdd88bcf63ae6cbe386450134fd190857` |

All three files: 5887 ATOM/HETATM records, chains A / B / C.

### Chain content

| Chain | Molecule | Residues | Heavy atoms | B-factor = pLDDT (mean / min / max) |
|:---:|:---|:---:|:---:|:---|
| A | ERα LBD | 258 | 2051 | 81.6 / 41.1 / 97.0 |
| B | CRBN thalidomide-binding domain | 469 | 3782 | 34.8 / 22.2 / 64.7 |
| C | ARV-471 (HETATM, residue LIG) | 1 | 54 | 59.1 / 16.4 / 91.4 |

CRBN mean pLDDT of 34.8 reflects single-sequence (no MSA) mode: CRBN orientation is
unconstrained and structurally unreliable across all three models.

### Confidence scores per model

| Model | conf | iptm | lig_iptm (lig→ERα) | lig→CRBN | prot_iptm |
|:---:|:---:|:---:|:---:|:---:|:---:|
| model_0 | **0.4778** | 0.3133 | 0.9065 | 0.2306 | 0.1604 |
| model_1 | 0.4751 | 0.3309 | 0.8781 | **0.3496** | **0.2475** |
| model_2 | 0.4649 | 0.3237 | 0.8663 | 0.3332 | 0.1715 |

model_0 is Boltz-2's top-ranked model by `confidence_score`. However, model_1 has the highest
lig→CRBN iptm (0.3496 vs 0.2306 for model_0) and prot_iptm (0.2475). The cooperativity-proxy
ranking across diffusion samples is **model_1 > model_2 > model_0**. The 10-compound series
analysis in `phase_09_protac_series_predictions.md` used model_0 as the reference (0.2306);
using model_1 as reference (0.3496) would reorder the bottom half of that ranking (ARV-007
would move further below reference; ARV-009, ARV-005, ARV-008 would fall below it).

---

## Verification

**SHA-256 checksums confirm byte-identical copies.** Computed with `sha256sum` on the copied
files; the source files remain unchanged in `boltz_out/`.

**Chain identity confirmed by ATOM record parsing.** Chain A: 258 distinct residue numbers
(SER 1 through the C-terminal residue), consistent with the ERα LBD sequence in the YAML
input. Chain B: 469 distinct residue numbers, consistent with the CRBN sequence. Chain C:
54 HETATM records (residue LIG), consistent with ARV-471's 54 heavy atoms (confirmed
independently by RDKit from SMILES in the earlier SMILES-extraction phase).

**B-factors are pLDDT values as output by Boltz-2.** Column 61-66 contains per-atom pLDDT
scores on the 0-100 scale. The ERα mean of 81.6 indicates a reliably modeled receptor;
CRBN mean of 34.8 (range 22.2–64.7) confirms that CRBN placement should not be
used for structural inference.

**Confidence JSON files are present for all three models.** Values extracted directly from
`confidence_ARV471_ERalpha_CRBN_boltz_input_model_{0,1,2}.json` in the same predictions
subdirectory. No values were copied from memory or prior summaries.

---

## Limitations

- No energy minimisation or clash removal has been applied. All three models contain
  steric clashes between ERα and CRBN (minimum inter-chain all-atom distances 1.2–2.1 Å),
  as expected for raw Boltz-2 diffusion output.
- CRBN orientation is unconstrained (no-MSA mode). The three models sample different CRBN
  poses relative to ERα; model choice materially affects any distance-based analysis.
- model_0 was used as the ARV-471 reference in the 10-compound cooperativity ranking. If
  model_1 were used as reference, compounds with lig→CRBN iptm between 0.2306 and 0.3496
  (ARV-009, ARV-005, ARV-008, ARV-002, ARV-004) would move from above-reference to
  below-reference.

---

## Job Provenance

| Field | Value |
|:---|:---|
| Cluster job | 6465991 (Isambard-AI Phase 2, GH200) |
| Container | boltzgen-0.3.1.sif (Boltz-2 v0.4.2) |
| Run date | 11 Sep 2026 |
| Input YAML | `ARV471_ERalpha_CRBN_boltz_input.yaml` (session root) |
| Diffusion samples | 3 (model_0, model_1, model_2) |
| Settings | seed=42, sampling_steps=50, recycling_steps=3, --no_kernels |

---

## References

- Passaro S, Corso G, Wohlwend J et al. Boltz-2: Towards Accurate and Efficient Binding
  Affinity Prediction. bioRxiv 2025. doi:10.1101/2025.06.14.659707
