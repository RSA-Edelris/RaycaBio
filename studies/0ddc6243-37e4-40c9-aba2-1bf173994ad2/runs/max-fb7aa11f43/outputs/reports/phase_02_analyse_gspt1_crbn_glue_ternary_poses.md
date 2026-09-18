
## What this phase did

Analysed the three Boltz-2 ternary complex PDB/CIF files produced by Isambard-AI job 6567207 to answer whether the CC-885-type glutarimide glue bridges GSPT1 and CRBN in the predicted structures.

## Inputs

- `gspt1_crbn_glue_{0,1,2}.pdb` — three diffusion samples; Chain A = GSPT1 (199 res, 1534 atoms), Chain B = CRBN (406 res, 3263 atoms), Chain C = LIG (31 heavy atoms)
- `gspt1_crbn_glue_{0,1,2}.cif` — mmCIF versions; queried for `_ma_qa_metric_local.metric_value`
- `gspt1_crbn_glue_{0,1,2}.npz` — DesignWriter metadata (636 tokens: 605 protein + 31 ligand)

## Key computed numbers

### Per-residue confidence
`_ma_qa_metric_local.metric_value` = 80.00 uniform across all 606 tokens in all three models. B-factors = 0.00 throughout. No genuine pLDDT available; DesignWriter writes a placeholder.

### Ligand–CRBN contacts (≤ 4.5 Å)

| CRBN residue | Model 0 (Å) | Model 1 (Å) | Model 2 (Å) |
|---|---|---|---|
| W344 | 2.36 | 2.71 | 2.74 |
| W350 | 3.26 | 3.71 | 3.05 |
| W364 | 3.23 | 2.54 | 2.91 |
| H342 | 2.54 | — | — |
| E341 | 2.63 | — | — |

Total CRBN residues within 4.5 Å: 15 (M0), 19 (M1), 13 (M2). The canonical Trp cage (W344/W350/W364) is engaged in every model.

### Ligand–GSPT1 proximity

| Model | Min ligand–GSPT1 distance (Å) | Atoms within 4 Å |
|---|---|---|
| 0 | 18.50 | 0 |
| 1 | 18.53 | 0 |
| 2 | 17.45 | 0 |

No ligand–GSPT1 contact in any model.

### GSPT1–CRBN protein–protein interface (Cα < 8 Å)

| Model | GSPT1 res | CRBN res | CA pairs | Min CA–CA (Å) |
|---|---|---|---|---|
| 0 | 39 / 199 | 39 / 406 | 100 | 3.84 |
| 1 | 21 / 199 | 22 / 406 | 46 | 4.77 |
| 2 | 17 / 199 | 19 / 406 | 55 | 4.51 |

CRBN contact residues span positions 1–145 (N-terminal domain), not the β-hairpin neosubstrate recruitment surface (~350–380).

### Inter-model Cα RMSD (chains A+B, no superposition)

| Pair | RMSD (Å) |
|---|---|
| M0 vs M1 | 34.56 |
| M0 vs M2 | 40.36 |
| M1 vs M2 | 42.05 |

## Conclusion

Boltz-2 places the glutarimide correctly in the CRBN Trp cage but does not assemble the bridging ternary geometry. GSPT1 contacts CRBN directly (min Cα–Cα 3.84 Å, Model 0) but via the CRBN N-terminal domain rather than the substrate-recruitment surface. Inter-model RMSD of 34–42 Å reflects unconstrained sampling with no dominant ternary minimum.

## Outputs

- `gspt1_crbn_glue_boltz2_analysis.md` — full findings report (reports/)
- Scripts 017–022 in `02_analyse_gspt1_crbn_glue_ternary_poses_and_write_/source/`
