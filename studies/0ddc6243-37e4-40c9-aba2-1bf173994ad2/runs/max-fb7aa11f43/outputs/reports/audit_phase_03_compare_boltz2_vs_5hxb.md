
## What was done

Downloaded 5HXB from RCSB, identified chain assignments and ligand, computed sequence-aligned Cα RMSD for CRBN and GSPT1, and tabulated ligand contact distances for both crystal and Boltz-2 models.

## Data integrity checks

- **5HXB.cif**: 4,550,897 bytes. Ligand `85C` has 31 heavy atoms in both chain Z and chain C copies — matches our predicted ligand atom count (31), confirming same compound.
- **Chain assignments confirmed**: Chain X = GSPT1 (195 res, seqids 440–634); Chain Z = CRBN (380 res, seqids 48–442) + ZN + 85C; Chain Y/B = DDB1 (not used).
- **Sequence offsets verified by residue identity**: K572/K573/S574/G575 in 5HXB chain X map to K137/K138/S139/G140 in our GSPT1 input — exact residue identity match at all four positions confirms offset of 435 is correct.
- **CRBN Trp offset verified**: W380/W386/W400 in 5HXB = W344/W350/W364 in our numbering (offset 36) — confirmed by one-letter sequence alignment of 380 matched residues.

## Numerical checks

- CRBN Trp cage contacts in both crystal and Boltz-2: distances in the 2.4–3.7 Å range — physically plausible hydrogen-bond/van-der-Waals distances.
- GSPT1 bridging distances in Boltz-2 (32–55 Å) are unambiguously non-contact; no boundary cases.
- Kabsch RMSD computed on sequence-matched Cα pairs only (not all atoms); 380 pairs used for full-chain CRBN, 118 for TBD.

## Issues

None. All crystal chain reads, atom counts, and sequence alignments completed without error.

## Audit verdict

Pass. The 5HXB data was correctly parsed, chain assignments were verified, sequence offsets were independently confirmed by residue identity, and all computed distances are internally consistent.
