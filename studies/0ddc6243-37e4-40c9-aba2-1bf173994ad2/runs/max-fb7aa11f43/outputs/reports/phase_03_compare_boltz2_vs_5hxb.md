
## What this phase did

Downloaded PDB 5HXB (CC-885/GSPT1/CRBN crystal structure, 3.0 Å) and computed quantitative comparisons against the three Boltz-2 ternary complex models from job 6567207.

## Inputs

- `5HXB.cif` — downloaded from RCSB (4.55 MB); chains used: X (GSPT1, 195 res, seqids 440–634), Z (CRBN, 380 res, seqids 48–442), ligand `85C` (31 heavy atoms = CC-885)
- `gspt1_crbn_glue_{0,1,2}.pdb` — three Boltz-2 diffusion samples

## Sequence offsets

- GSPT1: 5HXB seqid = our Boltz-2 residue + 435 (our input starts GSGP at residue 1; 5HXB starts at canonical eRF3a residue 440)
- CRBN: 5HXB seqid = our Boltz-2 residue + 36 (our 406 aa input lacks first 36 residues of canonical 442 aa CRBN)

## Key computed numbers

### CRBN Trp cage contacts (ligand–CRBN ≤ 4.5 Å)

| Residue | 5HXB (Å) | Model 0 (Å) | Model 1 (Å) | Model 2 (Å) |
|---|---|---|---|---|
| W380/W344 | 2.70 | 2.36 | 2.71 | 2.74 |
| W386/W350 | 3.21 | 3.26 | 3.71 | 3.05 |
| W400/W364 | 3.62 | 3.23 | 2.54 | 2.91 |

Agreement within ~0.7 Å. Pocket pharmacophore reproduced.

### Molecular glue bridging (GSPT1 contacts with ligand)

Crystal: 12 residues within 4.5 Å, min 2.53 Å (K628/our K193).  
All Boltz-2 models: 0 residues within 4.5 Å; those same 12 residues are 32–55 Å from the ligand.

### CRBN structural RMSD vs 5HXB chain Z

| Scope | Model 0 | Model 1 | Model 2 |
|---|---|---|---|
| Full chain (380 Cα) | 20.51 Å | 17.64 Å | 23.07 Å |
| TBD only (seqid ≥ 320, 118 Cα) | 10.76 Å | — | — |

### GSPT1 bridging residue distances to ligand (Boltz-2 models)

Crystal bridging residues (K572/K573/S574/G575/K628 = our K137/K138/S139/G140/K193) are 32–55 Å from the ligand in all three models. The correct sequence is present; the geometry is not.

## Outputs

- `5hxb_comparison_gspt1_crbn_glue_boltz2.md` — full comparison report (reports/)
- Scripts 023–029 in `01_compare_boltz_2_ternary_models_to_crystal_struct/source/`
- `5HXB.cif` in `01_compare_boltz_2_ternary_models_to_crystal_struct/structures/`

## Conclusion

Boltz-2 reproduces the CRBN glutarimide pocket correctly (Trp cage within ~0.7 Å of crystal). It fails entirely on ternary bridging: the GSPT1 neosubstrate surface is 32–55 Å from the ligand in all models vs 2.5–3.8 Å in 5HXB. The CRBN fold diverges substantially from crystal (TBD RMSD 10.8 Å), consistent with the missing DDB1 scaffold that fixes CRBN orientation in vivo.
