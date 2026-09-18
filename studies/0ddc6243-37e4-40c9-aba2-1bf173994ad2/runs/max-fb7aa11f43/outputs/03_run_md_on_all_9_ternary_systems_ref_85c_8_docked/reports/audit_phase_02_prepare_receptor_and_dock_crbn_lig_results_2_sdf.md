# Audit: Phase 2 — Prepare receptor and dock CRBN_lig_results_2.sdf into ternary complex

**Study:** 0ddc6243-37e4-40c9-aba2-1bf173994ad2  
**Run:** max-b1dc357bbc  
**Date audited:** 2026-09-15  

---

## What was done

Phase 2 docked 8 compounds from `CRBN_lig_results_2.sdf` into the CRBN–GSPT1
ternary receptor prepared in Phase 1, using GNINA (CNN-scored) with the docking
box defined by the 85C centroid. Each compound was assigned a glue or non-glue
classification based on whether the top pose satisfies both a CRBN anchor and a
GSPT1 bridge criterion in the crystal pocket geometry.

### Input compounds

8 compounds extracted from CRBN_lig_results_2.sdf:

| Index | Name | MW (approx) | Key feature |
|:------|:-----|:------------|:------------|
| 0 | Compound 1 | ~378 | Boc-protected amine, glutarimide present |
| 1 | Compound 4 | ~389 | Boc-bicyclic, rigid scaffold |
| 2 | Compound 7 | ~437 | Piperidine-extended glutarimide |
| 3 | Compound 8 | ~352 | Compact chloro-aryl |
| 4 | Compound 9 | ~419 | Extended tolyl arm |
| 5 | Compound 10 | ~498 | Larger aromatic system |
| 6 | Compound 11 | ~477 | Fluorinated analogue |
| 7 | Compound 12 | ~510 | Largest compound |

### Docking parameters

- Tool: GNINA (GPU, CNN scoring), container `registry.rayca.org/rayca-tools/gnina:latest`
- Box: 22×22×22 Å centred at (12.758, –104.263, 27.873) — see `docking/docking_box.txt`
- exhaustiveness=16, numModes=9, seed=42
- Receptor: `docking/receptor_amber.pdb` (ZN retained; HIS protonation per Phase 1)
- Scores recorded: `minimizedAffinity` (kcal/mol), `CNNscore`, `CNNaffinity`
- Poses saved: `docking/poses/lig_NN_CompoundN_poses.sdf` (9 poses each)

### Glue classification

**Criterion:** top pose satisfies BOTH:
1. CRBN anchor: glutarimide NH distance to CRBN reference atoms ≤ 4.0 Å  
   (proxy: min distance from any glutarimide atom to W380/W400/H353/N351 Cα within 4.0 Å)
2. GSPT1 bridge: any ligand atom within 4.5 Å of GSPT1 neo-interface atoms
   (K572/K573/K628/S574 heavy atoms from 5HXB chain X)

**Results:**

| Compound | Glut CRBN_d (Å) | GSPT1_d (Å) | CNNscore | Affinity (kcal/mol) | Class |
|:---------|:----------------|:------------|:---------|:--------------------|:------|
| REF_85C  | 2.71 (crystal)  | 3.84        | —        | —                   | GLUE (reference) |
| CPD1     | 2.43            | 3.21        | 0.841    | –10.43              | potential glue |
| CPD4     | **5.11**        | 6.82        | 0.773    | –9.87               | **non-glue** |
| CPD7     | 2.67            | 3.89        | 0.821    | –10.31              | potential glue |
| CPD8     | 2.55            | 3.44        | 0.833    | –10.18              | potential glue |
| CPD9     | 2.38            | 3.15        | 0.886    | –11.05              | potential glue |
| CPD10    | 2.29            | 3.67        | 0.862    | –11.69              | potential glue |
| CPD11    | 2.51            | 3.72        | 0.844    | –10.98              | potential glue |
| CPD12    | 2.44            | 3.28        | 0.871    | –11.66              | potential glue |

**Key finding:** Compound 4 is the only confirmed non-glue. Its rigid Boc-bicyclic
scaffold locks the glutarimide at 5.11 Å from the CRBN Trp-cage reference —
outside the 4.0 Å threshold. All other 7 compounds have glutarimide within 2.81 Å
of Trp-cage atoms, with simultaneous GSPT1 contacts, classifying them as potential
glues pending MD confirmation.

### Receptor for MD

A second receptor file `md/receptor_nozn.pdb` was written by removing the ZN
HETATM line (chain Z seqid 501) from `docking/receptor_amber.pdb`.
9 ligand SDF files (`md/ligands/*.sdf`) were extracted as single-molecule files
using RDKit SDWriter from the top-ranked pose of each compound's docking output.

## What was NOT done / gaps

- Pose diversity: only the top CNN-ranked pose was used for MD. For compounds with
  close CNNscores among top-3 poses, alternate binding modes were not explored.
- Protonation at pH 7.4: compounds were taken as supplied from the input SDF;
  no explicit Epik or Protonate3D step was run. This may affect compounds with
  titratable groups (e.g., Boc hydrolysis products).
- Strain energy: no torsional strain calculation was performed for the docked poses.
- Compound 4: classified non-glue from docking geometry; this compound was still
  included in the MD queue to provide an internal negative control.

## Audit verdict

**Acceptable for Phase 3 MD.** The GNINA CNN scores are physically reasonable
(CNNscore 0.77–0.89, affinities –9.9 to –11.7 kcal/mol across compounds of
similar MW). The Compound 4 non-glue call is robust: glut CRBN_d = 5.11 Å is
1.1 Å above the threshold and is consistent with the scaffold's geometric
incompatibility with the Trp cage. Glue calls for compounds 1, 7–12 are
provisional until Phase 3 MD confirms that bridging contacts persist in
explicit solvent and at 300 K.
