# Phase 10 — ARV-471 Ternary Complex PDB Export (All Three Boltz-2 Models)

## Summary

The three Boltz-2 diffusion-sample PDB files for the ARV-471 / ERα / CRBN ternary complex
prediction (job 6465991, Isambard-AI GH200, 11 Sep 2026) were copied from their original
prediction subdirectory to the session root under clean names. No coordinates, B-factors, or
chain assignments were modified. Confidence scores were confirmed from the matching JSON files.

**Key finding:** model_0 is Boltz-2's top-ranked model by overall confidence score (0.4778),
but model_1 has the highest lig→CRBN iptm (0.3496 vs 0.2306 for model_0). The cooperativity
proxy ranking across the three diffusion samples is model_1 > model_2 > model_0.

---

## Job Provenance

| Field | Value |
|:---|:---|
| Job ID | 6465991 |
| Cluster | Isambard-AI Phase 2 (GH200, aarch64) |
| Container | boltzgen-0.3.1.sif (Boltz-2 v0.4.2) |
| Run date | 11 Sep 2026, 15:30 UTC |
| Input YAML | `ARV471_ERalpha_CRBN_boltz_input.yaml` (session root) |
| Diffusion samples | 3 (model_0, model_1, model_2) |
| Settings | seed=42, sampling_steps=50, recycling_steps=3, --no_kernels |
| SLURM log | `slurm-6465991.log` |

---

## Output Files

| File | Size | SHA-256 |
|:---|:---:|:---|
| `ARV471_ERalpha_CRBN_model_0.pdb` | 471 KB | `3f250b3f28984288418e9bf94eac8a464f08b292a1f17475e2f2ee0f3497f67a` |
| `ARV471_ERalpha_CRBN_model_1.pdb` | 471 KB | `beb089602e3b91e908b027b657ecc096c51a158a6076722054449ce819584616` |
| `ARV471_ERalpha_CRBN_model_2.pdb` | 471 KB | `6c9b43b5600af6058e83cbba2ca2a97fdd88bcf63ae6cbe386450134fd190857` |

Source: `boltz_out/boltz_results_ARV471_ERalpha_CRBN_boltz_input/predictions/ARV471_ERalpha_CRBN_boltz_input/`

All three files: 5887 ATOM/HETATM records, chains A (ERα) / B (CRBN) / C (ARV-471 ligand).

---

## Chain Content

| Chain | Molecule | Residues | Heavy atoms | pLDDT mean / min / max |
|:---:|:---|:---:|:---:|:---|
| A | ERα LBD | 258 | 2051 | 81.6 / 41.1 / 97.0 |
| B | CRBN thalidomide-binding domain | 469 | 3782 | 34.8 / 22.2 / 64.7 |
| C | ARV-471 (HETATM, residue LIG) | 1 | 54 | 59.1 / 16.4 / 91.4 |

B-factor column carries pLDDT (0-100 scale). CRBN mean pLDDT of 34.8 reflects
single-sequence (no MSA) mode; CRBN orientation is unconstrained.

---

## Confidence Scores Per Model

| Model | conf | iptm | lig_iptm (lig→ERα) | lig→CRBN | prot_iptm |
|:---:|:---:|:---:|:---:|:---:|:---:|
| model_0 | **0.4778** | 0.3133 | 0.9065 | 0.2306 | 0.1604 |
| model_1 | 0.4751 | 0.3309 | 0.8781 | **0.3496** | **0.2475** |
| model_2 | 0.4649 | 0.3237 | 0.8663 | 0.3332 | 0.1715 |

Extracted directly from `confidence_ARV471_ERalpha_CRBN_boltz_input_model_{0,1,2}.json`.

The model_0 lig→CRBN iptm (0.2306) was used as the reference value in `phase_09_protac_series_predictions.md`.
If model_1 were used instead (0.3496), compounds ARV-009, ARV-005, ARV-008, ARV-002, and ARV-004
would fall below the reference threshold rather than above it.

---

## Verification

**SHA-256 checksums confirm byte-identical copies.** Computed with `sha256sum` on the copied
files; source files remain unchanged in `boltz_out/`.

**Chain identity confirmed by ATOM record parsing.** Chain A: 258 distinct residue numbers
consistent with the ERα LBD YAML input sequence. Chain B: 469 residues consistent with CRBN.
Chain C: 54 HETATM records (LIG), consistent with ARV-471's 54 heavy atoms confirmed by
RDKit from SMILES in phase_08.

**All three confidence JSONs present and parsed without error.** Values extracted by inline
Python from the source predictions directory; no values carried from memory.

---

## Limitations

- No energy minimisation or clash removal applied. Raw Boltz-2 output contains steric clashes
  (minimum ERα-CRBN all-atom distances 1.2–2.1 Å across the three models).
- CRBN orientation is unconstrained (no-MSA mode). The three models sample different relative
  CRBN poses; model choice materially affects any distance-based downstream analysis.
- The 10-compound cooperativity ranking in phase_09 used model_0 as reference. See the
  confidence table above for the impact of using model_1 instead.

---

## References

- Passaro S, Corso G, Wohlwend J et al. Boltz-2: Towards Accurate and Efficient Binding
  Affinity Prediction. bioRxiv 2025. doi:10.1101/2025.06.14.659707
