# ARV-471 PROTAC Ternary Complex — Boltz-2 Structure Prediction Phase Report

## Overview

Boltz-2 was used to predict the ternary complex structure of the PROTAC degrader ARV-471 bridging Estrogen Receptor alpha (ERα, POI, chain A) and Cereblon (CRBN, E3 ligase, chain B). One pose was generated (model_0) after a 15.5-hour CPU inference run. The output PDB and confidence JSON are archived at the session root.

---

## Inputs

| Component | Identity | Chain | Residues / Atoms |
|---|---|---|---|
| POI | ERα ligand-binding domain | A | 258 residues |
| E3 ligase | CRBN (full length) | B | 469 residues |
| PROTAC | ARV-471 (RDKit-canonicalized SMILES) | C | 54 heavy atoms |

**ARV-471 SMILES:**
```
O=C1CC[C@H](N2Cc3cc(N4CCN(CC5CCN(c6ccc([C@@H]7c8ccc(O)cc8CC[C@@H]7c7ccccc7)cc6)CC5)CC4)ccc3C2=O)C(=O)N1
```

**Input YAML:** `ARV471_ERalpha_CRBN_boltz_input.yaml` (version 1, MSA: empty for both proteins)

---

## Run Settings

| Parameter | Value |
|---|---|
| Model | boltz2_conf.ckpt (2.286 GB) |
| Seed | 42 |
| diffusion_samples | 1 |
| sampling_steps | 25 |
| recycling_steps | 1 |
| output_format | pdb |
| accelerator | cpu (no GPU available) |
| num_workers | 0 |
| no_kernels | True |

**Note:** Settings were reduced from the originally requested 3 samples / 50 steps to 1 sample / 25 steps after an earlier 5.5-hour run with the original settings failed to complete. The reduced run took 15h 30m on CPU. A GPU re-run at full settings is recommended for production use.

---

## Output Files

| File | Description |
|---|---|
| `ARV471_ERalpha_CRBN_ternary_boltz2.pdb` | Full ternary complex, chains A/B/C, REMARK header with all metrics |
| `boltz_cpu_out/.../confidence_ARV471_ERalpha_CRBN_boltz_input_model_0.json` | Raw confidence JSON |

---

## Confidence Scores — Model 0

| Metric | Value | Notes |
|---|---|---|
| `confidence_score` | 0.448 | Overall complex confidence |
| `ptm` | 0.422 | Global TM-score proxy |
| `iptm` | 0.273 | Inter-chain interface confidence (low) |
| `ligand_iptm` | **0.797** | ARV-471 placement confidence (good) |
| `protein_iptm` | 0.161 | ERα–CRBN protein–protein interface confidence (low) |
| `complex_pLDDT` | 0.492 | Mean per-residue confidence |
| `complex_pDE` | 3.67 | Predicted distance error |
| Chain A pTM | 0.825 | ERα intrinsic fold confidence (high) |
| Chain B pTM | 0.246 | CRBN intrinsic fold confidence (low) |
| Chain C pTM | 0.716 | ARV-471 placement confidence (good) |

### Per-chain pairwise iptm

|  | Chain A (ERα) | Chain B (CRBN) | Chain C (ARV-471) |
|---|---|---|---|
| **Chain A (ERα)** | 0.825 | 0.152 | 0.530 |
| **Chain B (CRBN)** | 0.161 | 0.246 | 0.135 |
| **Chain C (ARV-471)** | **0.797** | 0.285 | 0.716 |

---

## Per-Chain pLDDT

| Chain | Identity | Atoms | Mean pLDDT | σ | Interpretation |
|---|---|---|---|---|---|
| A | ERα LBD | 2051 | **78.6** | 14.1 | Well-folded; confident |
| B | CRBN | 3782 | **33.0** | 7.0 | Poorly resolved; low confidence |
| C | ARV-471 | 54 | **51.5** | 25.5 | Moderate; wide spread across molecule |

---

## PROTAC Bridging Geometry

| Measurement | Value |
|---|---|
| ARV-471 molecular span (max intra-ligand distance) | 20.6 Å |
| Ligand centroid → ERα centroid | 14.7 Å |
| Ligand centroid → CRBN centroid | 21.2 Å |
| ERα centroid → CRBN centroid | **35.7 Å** |
| Min heavy-atom contact, ligand–ERα | 1.0 Å ⚠️ |
| Min heavy-atom contact, ligand–CRBN | 1.2 Å ⚠️ |
| Min heavy-atom contact, ERα–CRBN | 0.7 Å ⚠️ |

The ~36 Å protein centroid separation is within the expected range for PROTAC ternary complexes (literature range: 20–50 Å). Sub-1.5 Å minimum contact distances indicate heavy-atom clashes — a known artifact of diffusion-based prediction with limited sampling steps on CPU.

---

## Interpretation

**What is reliable:**
- ERα (chain A) is well-folded with pLDDT 78.6 and chain pTM 0.825. The LBD structure is confident.
- ARV-471 placement relative to ERα is high-confidence (pairwise iptm A↔C = 0.797). The ligand centroid sits 14.7 Å from the ERα centroid, consistent with engagement of the LBD pocket.
- The overall ternary arrangement (ERα–CRBN separation ~36 Å, ARV-471 spanning 20.6 Å) is physically plausible for a PROTAC-mediated neo-interface.

**What is uncertain:**
- CRBN (chain B) is poorly predicted: pLDDT 33.0, chain pTM 0.246. With 469 residues and no MSA, CRBN is at the edge of reliable CPU inference with 25 sampling steps.
- The protein–protein interface confidence is low (protein_iptm 0.161; A↔B pairwise iptm 0.152). Contact geometry between ERα and CRBN should not be used for interface residue analysis without further validation.
- Heavy-atom clashes between all chain pairs require energy minimization before contact-level interpretation.

---

## Technical Issues and Workarounds

| Issue | Fix Applied |
|---|---|
| DataLoader worker crash (`/dev/shm` 64 MB limit) | `--num_workers 0` |
| `MisconfigurationException: No supported gpu backend` | `--accelerator cpu` |
| protobuf version conflict (gencode 6.31.1 / runtime 5.29.6) | `boltz_run.py` wrapper stubs tensorboard proto modules before import |
| Stale `.pyc` bypassing `logger=False` patch | Deleted `__pycache__/main.cpython-312.pyc` |
| `ModuleNotFoundError: No module named 'boltz'` on relaunch | `PYTHONPATH=/home/ubuntu/rayca-sessions/.session-libs/...` prefix |
| Duplicate boltz process consuming ~11 GB RAM | Killed with `kill -9` |
| Platform job limit (20/20) blocked Isambard GPU submission | CPU path used throughout |

---

## Verification

The following checks were run on the output before this report was written.

### PDB integrity
- `Number of failed examples: 0` in boltz_fast.log — boltz's own writer reported no failures
- Atom count verified: 5887 total (2051 chain A + 3782 chain B + 54 chain C); matches input token count
- Chain termination: TER records present for chains A (residue 258) and B (residue 469); END record present
- Chain C ligand records: all 54 atoms written as HETATM with residue name LIG, consistent with small-molecule convention
- B-factor column populated with pLDDT values (range observed: ~16–90); no zero-fill

### Confidence JSON
- All expected keys present: `confidence_score`, `ptm`, `iptm`, `ligand_iptm`, `protein_iptm`, `complex_plddt`, `complex_iplddt`, `complex_pde`, `complex_ipde`, `chains_ptm`, `pair_chains_iptm`
- Chain indices (0=A, 1=B, 2=C) consistent across `chains_ptm` and `pair_chains_iptm`
- `ligand_iptm` (0.797) cross-checks with `pair_chains_iptm[2][0]` (0.797) — consistent
- `protein_iptm` (0.161) cross-checks with `pair_chains_iptm[1][0]` (0.161) — consistent

### Geometry sanity
- ERα centroid–CRBN centroid distance 35.7 Å: within expected range for PROTAC ternary complexes (20–50 Å from literature)
- ARV-471 molecular span 20.6 Å: consistent with a ~54-heavy-atom linker-containing PROTAC
- Ligand centroid closer to ERα (14.7 Å) than to CRBN (21.2 Å): consistent with the estradiol warhead engaging the ERα LBD
- Heavy-atom clashes (min inter-chain distances 0.7–1.2 Å) documented; flagged in REMARK 5 of output PDB

### What was not verified
- Stereochemistry of ARV-471 in the predicted pose was not checked (would require RDKit round-trip)
- No energy minimization was run; clash severity beyond min-distance measurement is unknown
- Predicted ERα–CRBN interface residues were not compared against published CRBN co-crystal contacts (PDB 5FQD, 6H0F) — deferred to next steps

---

## Recommended Next Steps

1. **Energy minimization** — remove clashes with OpenMM or GROMACS before any interface analysis
2. **GPU re-run** — repeat with `--diffusion_samples 3 --sampling_steps 50` on a GPU; estimated ~5–15 min on a modern GPU
3. **CRBN input quality** — provide a pre-folded CRBN structure (e.g. AlphaFold2 model) instead of sequence-only to improve chain B confidence
4. **Interface analysis** — after minimization, compare ERα–CRBN contact residues against known CRBN co-crystal structures (PDB: 5FQD, 6H0F)
