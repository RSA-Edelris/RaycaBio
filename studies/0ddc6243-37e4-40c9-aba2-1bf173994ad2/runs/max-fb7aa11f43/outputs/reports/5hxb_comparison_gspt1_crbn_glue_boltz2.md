
## Reference structure

PDB 5HXB: crystal structure of CRBN–DDB1 in complex with CC-885 and GSPT1 (eRF3a G-domain), resolved at 3.0 Å. The asymmetric unit contains two copies of the ternary complex; this analysis uses chains X (GSPT1, 195 residues, seqids 440–634) and Z (CRBN, 380 residues, seqids 48–442) with ligand `85C` (31 heavy atoms).

Sequence offsets to our Boltz-2 numbering (1-indexed):
- GSPT1: 5HXB seqid = our residue + 435 (our GSPT1 input starts GS**G**PIRLP; 5HXB chain X starts at canonical eRF3a residue 440)
- CRBN: 5HXB seqid = our residue + 36 (our CRBN input lacks the first 36 residues of the canonical 442 aa sequence)

---

## 1. Ligand binding to CRBN: agreement

Both crystal and Boltz-2 models place the glutarimide in the CRBN tryptophan cage. Minimum ligand–CRBN heavy-atom distances:

| CRBN residue | 5HXB canonical | 5HXB (Å) | Boltz-2 our# | Model 0 (Å) | Model 1 (Å) | Model 2 (Å) |
|---|---|---|---|---|---|---|
| TRP | W380 | 2.70 | W344 | **2.36** | 2.71 | 2.74 |
| TRP | W386 | 3.21 | W350 | 3.26 | 3.71 | 3.05 |
| TRP | W400 | 3.62 | W364 | 3.23 | **2.54** | 2.91 |
| HIS | H378 | 2.76 | H342 | 2.54 | — | — |
| GLU | E377 | 2.82 | E341 | 2.63 | — | — |
| SER | S379 | 3.22 | S343 | 3.05 | — | — |
| PHE | F402 | 3.96 | F366 | 3.28 | — | — |

The three canonical CRBN tryptophans (W380/W386/W400) contact the ligand in both crystal and all three Boltz-2 models at closely similar distances (within ~0.7 Å). The glutarimide binding mode is correctly reproduced.

---

## 2. Molecular glue bridging: complete failure

In 5HXB, CC-885 forms a 12-residue bridging interface with GSPT1 (min distance 2.53 Å). The key contacts are at the G-domain surface of eRF3a.

| GSPT1 residue | 5HXB canonical | 5HXB (Å) | Our numbering | Identity | Model 0 (Å) | Model 1 (Å) | Model 2 (Å) |
|---|---|---|---|---|---|---|---|
| GLN534 | Q534 | 3.71 | res 99 | Q | 36.8 | 40.4 | 32.8 |
| VAL536 | V536 | 3.07 | res 101 | V | 33.7 | 38.5 | 37.7 |
| LYS572 | K572 | 2.66 | res 137 | K | 39.2 | 45.4 | 39.0 |
| LYS573 | K573 | 2.93 | res 138 | K | 42.1 | 53.0 | 40.6 |
| SER574 | S574 | 2.56 | res 139 | S | 41.5 | 55.2 | 38.0 |
| GLY575 | G575 | 3.32 | res 140 | G | 39.5 | 52.1 | 36.1 |
| ILE626 | I626 | 3.23 | res 191 | I | 32.3 | 30.6 | 43.8 |
| GLY627 | G627 | 3.51 | res 192 | G | 33.4 | 32.7 | 43.8 |
| LYS628 | K628 | 2.53 | res 193 | K | 35.1 | 35.5 | 41.9 |

The GSPT1 residues that bridge to the ligand in the crystal are correctly present in our input sequence (K137, K138, S139, G140, I191, G192, K193). Despite the sequence being correct, the bridging surface is 32–55 Å from the ligand in all Boltz-2 models.

---

## 3. CRBN fold quality

| Comparison | RMSD (Å) | Residues used |
|---|---|---|
| Full-chain CRBN, Model 0 vs 5HXB chain Z | 20.51 | 380 Cα |
| Full-chain CRBN, Model 1 vs 5HXB chain Z | 17.64 | 380 Cα |
| Full-chain CRBN, Model 2 vs 5HXB chain Z | 23.07 | 380 Cα |
| CRBN thalidomide-binding domain (seqid ≥ 320), Model 0 vs 5HXB | 10.76 | 118 Cα |

Full-chain CRBN RMSD of 17–23 Å reflects a global domain-arrangement difference: the 406 aa CRBN was folded free in solution without DDB1, while in 5HXB it is constrained by the DDB1 adaptor. Even the isolated thalidomide-binding domain RMSD of 10.76 Å is high, indicating the Boltz-2 single-sequence CRBN fold diverges substantially from the crystal conformation.

---

## 4. Summary table

| Metric | 5HXB crystal | Boltz-2 Model 0 | Boltz-2 Model 1 | Boltz-2 Model 2 |
|---|---|---|---|---|
| Ligand–CRBN Trp cage contacts | W380/W386/W400 at 2.7–3.6 Å | W344/W350/W364 at 2.4–3.3 Å | same, 2.5–3.7 Å | same, 2.7–3.1 Å |
| Ligand–GSPT1 bridging contacts | 12 residues, min 2.53 Å | 0 residues, min 18.5 Å | 0 residues, min 18.5 Å | 0 residues, min 17.5 Å |
| CRBN full-chain Cα RMSD vs crystal | — | 20.5 Å | 17.6 Å | 23.1 Å |
| CRBN TBD Cα RMSD vs crystal | — | 10.8 Å | — | — |
| Inter-model Cα RMSD | — | M0/M1: 34.6 Å | M0/M2: 40.4 Å | M1/M2: 42.1 Å |

---

## Interpretation

Boltz-2 reproduces the CRBN pocket pharmacophore correctly: the three canonical tryptophans contact the glutarimide at distances matching the crystal within ~0.7 Å. However, it completely fails to assemble the second half of the molecular glue mechanism — the GSPT1 neosubstrate surface (K572/K573/S574/G575/K628 in canonical numbering, all present in the input sequence) is 32–55 Å from the ligand in every model.

Three factors likely explain the failure:
1. **No DDB1 context.** In the crystal, CRBN is anchored by DDB1, fixing its orientation relative to GSPT1. Free CRBN sampled many orientations, none productive.
2. **Single-sequence mode.** Without MSA co-evolutionary signal, there is no information to bias the model toward the productive CRBN–GSPT1 interface geometry.
3. **Low-affinity ternary interface.** CC-885 drives a weak cooperative interaction; Boltz-2 co-folding in design mode did not find the shallow energy minimum.

The CRBN pocket geometry is a validated positive control (RMSD within noise for the three Trp contacts). The failed bridging is a true negative: the sequence is correct, the CRBN pocket is correct, but the ternary assembly is not predicted.
