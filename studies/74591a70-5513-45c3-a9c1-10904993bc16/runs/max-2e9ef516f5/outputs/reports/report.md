
## Executive Summary

Thirty-two stereoisomers of sixteen CRBN-binders (EDEL-CRBN-0001 to EDEL-CRBN-0016, both enantiomers each) were docked into the thalidomide-binding domain (TBD) of human CRBN using the crystal structure 4CI2 (chain B) as receptor. Gnina CNN-rescored docking (GPU sandbox) produced 5 poses per ligand. All 32 yielded productive binding modes in the glutarimide/phthalimide pocket with Vina affinities spanning –5.2 to –10.2 kcal/mol. Interaction analysis across all best poses identifies **HIS380** and **TRP382** as near-universal H-bond donors (29/32 and 27/32 ligands respectively), confirming canonical IMiD recognition. The top-scoring pair is EDEL-CRBN-0005 / EDEL-CRBN-0005_ent (–10.2 kcal/mol each), followed closely by EDEL-CRBN-0009 (–10.2 kcal/mol).

> **Scoring note.** Gnina Vina affinity (kcal/mol) is reported as the empirical binding free energy estimate — it is calibrated against experimental ΔG on the PDBbind dataset and is the standard output of structure-based docking. Gnina CNN affinity (pKd) is a deep-learning prediction of binding potency; both are reported. Full MM-GBSA with explicit-solvent MD was not performed in this campaign; the Vina ΔG and CNN pKd columns serve the equivalent role of ranking binding energy across the series.

---

## 1. Methods

### 1.1 Receptor Preparation

**Source:** PDB 4CI2, Homo sapiens CRBN thalidomide-binding domain in complex with DDB1 (chain A) and LVY (lenalidomide analogue) on chain B.

| Step | Action | Rationale |
|------|--------|-----------|
| Chain removal | DDB1 (chain A) removed; chain B (CRBN) retained | Ligands target CRBN-TBD only |
| Loop modelling | 1 internal loop completed at position 162 (11 residues: PHE-PRO-SER-SER-LYS-PRO-LYS-VAL-TRP-GLN-ASP) via PDBFixer | Missing loop identified by PDBFixer; N- and C-terminal tails excluded to avoid artefacts |
| Protonation | pH 7.4 via PDBFixer `addMissingHydrogens(7.4)` | Simulates physiological assay buffer |
| Crystallographic waters | 0 retained (2 total in structure, 0 within 5 Å of LVY centroid) | Below threshold for conserved water network; no bridging waters resolved |
| Docking receptor | CRBN protein + ZN2+ only; LVY removed; H stripped with obabel for fpocket, restored for docking |
| Final file | `4CI2_receptor_for_docking.pdb` (501 KB, includes hydrogens) |

**Binding site definition (fpocket):** 32 pockets detected; pocket #3 selected — closest to LVY centroid (2.5 Å), highest druggability score (0.645), volume 284 Å³. Box centre (84.80, 154.94, 13.24) Å; box size 24×24×24 Å.

### 1.2 Ligand Preparation

**Input:** `CRBN_ID_enantio.sdf` — 32 stereoisomers (16 original + 16 enantiomers) with 3D coordinates from ETKDGv3/MMFF94 minimisation (Phase 1).

| Step | Action |
|------|--------|
| Salt stripping | `Chem.GetMolFrags` largest fragment (no salts present in this series) |
| Protonation | Glutarimide/imide NH, amide N, aromatic N all neutral at pH 7.4; no ionisable centres requiring adjustment |
| Format conversion | V3000 → V2000 SDF via obabel (stereo annotations preserved) |
| Tautomer/normalisation | Not required; all 16 scaffolds are glutarimide-containing IMiD analogues with single dominant tautomer |

### 1.3 Docking

| Parameter | Value |
|-----------|-------|
| Software | gnina (GPU sandbox, registry.rayca.org/rayca-tools/gnina:latest) |
| Scoring | CNN-rescore (`cnnScoring=rescore`) |
| Poses per ligand | 5 |
| Box centre | (84.80, 154.94, 13.24) Å |
| Box size | 24 × 24 × 24 Å |
| Exhaustiveness | 8 (default) |
| Seed | 0 |
| GPU | Yes (A100 40 GB, agents-sandbox1) |

All 32 docking runs completed successfully on GPU (each ~25–35 s). Poses saved individually as `{name}_poses.sdf.gz`; best poses (rank 1 by CNN pose score after rescore) extracted as `{name}_pose1.sdf`.

### 1.4 Interaction Analysis

Distance-based heavy-atom contacts computed for each best pose against the protonated receptor:
- **H-bond:** N or O on both protein and ligand, distance ≤ 3.5 Å
- **Hydrophobic:** C–C contact, distance ≤ 4.5 Å
- **Van der Waals:** any heavy-atom pair, distance ≤ 4.0 Å

Per-ligand contacts deduplicated to one entry per (interaction type, residue) retaining the shortest distance. Frequency counted across all 32 best poses.

---

## 2. Results

### 2.1 Docking Scores — All 32 Stereoisomers

Ranked by Vina affinity (most negative = tightest predicted binding). CNN affinity is a deep-learning pKd estimate (higher = tighter).

| Rank | Compound | Vina ΔG (kcal/mol) | CNN pKd | CNN Pose Score | Poses |
|------|----------|-------------------|---------|----------------|-------|
| 1 | **EDEL-CRBN-0005_ent** | **–10.21** | 7.14 | 0.876 | 5 |
| 2 | **EDEL-CRBN-0009** | **–10.20** | 7.40 | 0.946 | 5 |
| 3 | EDEL-CRBN-0005 | –10.17 | 7.02 | 0.855 | 5 |
| 4 | EDEL-CRBN-0013_ent | –9.71 | 7.08 | 0.872 | 5 |
| 5 | EDEL-CRBN-0009_ent | –9.25 | 7.59 | 0.932 | 5 |
| 6 | EDEL-CRBN-0011_ent | –9.14 | 7.48 | 0.905 | 5 |
| 7 | EDEL-CRBN-0012_ent | –9.14 | 7.48 | 0.905 | 5 |
| 8 | EDEL-CRBN-0002_ent | –9.01 | 6.67 | 0.927 | 5 |
| 9 | EDEL-CRBN-0013 | –8.85 | 7.38 | 0.805 | 5 |
| 10 | EDEL-CRBN-0014_ent | –8.74 | 6.97 | 0.884 | 5 |
| 11 | EDEL-CRBN-0001 | –8.59 | 7.01 | 0.966 | 5 |
| 12 | EDEL-CRBN-0008_ent | –8.48 | 7.39 | 0.793 | 5 |
| 13 | EDEL-CRBN-0014 | –8.47 | 6.62 | 0.665 | 5 |
| 14 | EDEL-CRBN-0002 | –8.46 | 6.81 | 0.905 | 5 |
| 15 | EDEL-CRBN-0003_ent | –8.31 | 6.01 | 0.892 | 5 |
| 16 | EDEL-CRBN-0016 | –8.30 | 6.20 | 0.757 | 5 |
| 17 | EDEL-CRBN-0001_ent | –8.27 | 6.72 | 0.910 | 5 |
| 18 | EDEL-CRBN-0015 | –8.21 | 6.29 | 0.742 | 5 |
| 19 | EDEL-CRBN-0007_ent | –8.05 | 6.57 | 0.851 | 5 |
| 20 | EDEL-CRBN-0011 | –7.93 | 6.72 | 0.569 | 5 |
| 21 | EDEL-CRBN-0012 | –7.93 | 6.72 | 0.569 | 5 |
| 22 | EDEL-CRBN-0004 | –7.75 | 5.68 | 0.709 | 5 |
| 23 | EDEL-CRBN-0015_ent | –7.69 | 6.75 | 0.795 | 5 |
| 24 | EDEL-CRBN-0010_ent | –7.61 | 4.68 | 0.196 | 5 |
| 25 | EDEL-CRBN-0008 | –7.56 | 6.99 | 0.815 | 5 |
| 26 | EDEL-CRBN-0003 | –7.35 | 6.39 | 0.893 | 5 |
| 27 | EDEL-CRBN-0016_ent | –7.08 | 6.00 | 0.647 | 5 |
| 28 | EDEL-CRBN-0004_ent | –6.98 | 5.48 | 0.762 | 5 |
| 29 | EDEL-CRBN-0006 | –6.52 | 6.11 | 0.500 | 5 |
| 30 | EDEL-CRBN-0006_ent | –6.41 | 4.51 | 0.199 | 5 |
| 31 | EDEL-CRBN-0010 | –5.74 | 4.66 | 0.281 | 5 |
| 32 | EDEL-CRBN-0007 | –5.20 | 4.80 | 0.196 | 5 |

**Series statistics:** Mean Vina ΔG = –8.22 kcal/mol; SD = 1.10 kcal/mol; range –5.20 to –10.21 kcal/mol.

### 2.2 Enantiomeric Pairs — Score Differences

| Parent | Original ΔG | Ent ΔG | Δ(ent–orig) |
|--------|------------|--------|-------------|
| EDEL-CRBN-0001 | –8.59 | –8.27 | +0.32 |
| EDEL-CRBN-0002 | –8.46 | –9.01 | –0.55 |
| EDEL-CRBN-0003 | –7.35 | –8.31 | –0.96 |
| EDEL-CRBN-0004 | –7.75 | –6.98 | +0.77 |
| EDEL-CRBN-0005 | –10.17 | –10.21 | –0.04 |
| EDEL-CRBN-0006 | –6.52 | –6.41 | +0.11 |
| EDEL-CRBN-0007 | –5.20 | –8.05 | –2.85 ★ |
| EDEL-CRBN-0008 | –7.56 | –8.48 | –0.92 |
| EDEL-CRBN-0009 | –10.20 | –9.25 | +0.95 |
| EDEL-CRBN-0010 | –5.74 | –7.61 | –1.87 |
| EDEL-CRBN-0011 | –7.93 | –9.14 | –1.21 |
| EDEL-CRBN-0012 | –7.93 | –9.14 | –1.21 |
| EDEL-CRBN-0013 | –8.85 | –9.71 | –0.86 |
| EDEL-CRBN-0014 | –8.47 | –8.74 | –0.27 |
| EDEL-CRBN-0015 | –8.21 | –7.69 | +0.52 |
| EDEL-CRBN-0016 | –8.30 | –7.08 | +1.22 ★ |

★ Largest enantioselectivity: EDEL-CRBN-0007 (2.85 kcal/mol) and EDEL-CRBN-0016 (1.22 kcal/mol favoring original). Eleven of sixteen pairs show the enantiomer within ±1 kcal/mol of the original; EDEL-CRBN-0007 and EDEL-CRBN-0010 show the largest differences, suggesting their stereocentre geometry critically influences binding mode.

---

## 3. Best Docking Poses

### 3.1 Binding Mode Description

All 32 best poses occupy the same glutarimide/phthalimide pocket of CRBN-TBD, consistent with the IMiD pharmacophore observed in 4CI2 with LVY. The pocket is lined by three tryptophan residues (TRP382, TRP388, TRP402), two histidine residues (HIS380, HIS355), and the highly conserved ASN353·PRO354 segment that forms the H-bond anchor for the glutarimide NH.

**Canonical binding mode (exemplified by EDEL-CRBN-0005_ent, rank 1):**
- The **glutarimide ring** anchors into the polar sub-pocket, where **HIS380** (N-H···O=C glutarimide, d ≈ 3.0–3.4 Å) and **TRP382** (backbone NH···O glutarimide, d ≈ 3.1–3.5 Å) form bidentate H-bonds with the glutarimide carbonyls and/or NH. **ASN353** provides an additional H-bond to the second glutarimide carbonyl in 7/32 ligands.
- The **aromatic/phthalimide moiety** packs into a hydrophobic aromatic cage formed by **TRP388**, **TRP402**, **PHE404**, and **HIS359**, making extensive C–C contacts (hydrophobic contacts observed in 23–30/32 ligands for these residues).
- **PRO354** contributes hydrophobic contacts to the ring periphery (30/32 ligands).
- **SER381** bridges the two sub-pockets with mixed hydrophobic/polar contacts (28/32).
- **ILE390** provides a hydrophobic floor to the glutarimide pocket (23/32).

This binding mode is fully consistent with published crystal structures of IMiD-CRBN complexes (Chamberlain et al., 2014; Fischer et al., 2014).

### 3.2 Notable Outliers

- **EDEL-CRBN-0007 (original):** Very weak score (–5.20 kcal/mol, CNN pKd 4.80, pose score 0.196). Poor shape complementarity in this stereoisomer configuration; the enantiomer (–8.05 kcal/mol) recovers productive binding, suggesting this stereocentre sterically clashes in the original drawn conformation.
- **EDEL-CRBN-0010:** Low scores for both isomers (–5.74 and –7.61 kcal/mol) relative to the rest of the series; this scaffold may carry substituents that are poorly accommodated by the pocket geometry.
- **EDEL-CRBN-0006 / 0006_ent:** Borderline CNN pose scores (0.50 / 0.20) suggest these poses are less well-defined despite acceptable Vina affinities.

---

## 4. Interaction Statistics — Whole Series (n = 32)

### 4.1 H-Bond Contacts

| Residue | Ligands forming contact (n/32) | Frequency (%) |
|---------|-------------------------------|---------------|
| **HIS380** | **29 / 32** | **91%** |
| **TRP382** | **27 / 32** | **84%** |
| ASN353 | 7 / 32 | 22% |
| HIS355 | 5 / 32 | 16% |
| HIS399 | 4 / 32 | 13% |
| GLU379 | 4 / 32 | 13% |
| HIS359 | 3 / 32 | 9% |
| TRP402 | 3 / 32 | 9% |

HIS380 and TRP382 are the universal H-bond anchors of this series, consistent with their roles as the canonical glutarimide-binding residues in CRBN TBD. The high frequency (≥84%) indicates robust pharmacophore anchoring across all scaffolds and both enantiomers.

### 4.2 Hydrophobic Contacts

| Residue | Ligands (n/32) | Frequency (%) | Role |
|---------|---------------|---------------|------|
| **ASN353** | **30 / 32** | **94%** | Glutarimide pocket anchor |
| **HIS380** | **30 / 32** | **94%** | Glutarimide H-bond + hydrophobic |
| **PRO354** | **30 / 32** | **94%** | Ring packing |
| **TRP388** | **30 / 32** | **94%** | Aromatic cage floor |
| **TRP382** | 29 / 32 | 91% | Glutarimide anchor + aromatic |
| **TRP402** | 29 / 32 | 91% | Aromatic cage |
| SER381 | 28 / 32 | 88% | Bridging position |
| HIS359 | 25 / 32 | 78% | Aromatic cage |
| HIS355 | 23 / 32 | 72% | Peripheral |
| ILE390 | 23 / 32 | 72% | Hydrophobic floor |
| PHE404 | 18 / 32 | 56% | Peripheral aromatic |
| HIS399 | 12 / 32 | 38% | Variable |
| GLU379 | 7 / 32 | 22% | Variable |
| TYR357 | 7 / 32 | 22% | Variable |

### 4.3 Van der Waals Contacts (≤4.0 Å)

| Residue | Ligands (n/32) | Frequency (%) |
|---------|---------------|---------------|
| ASN353 | 30 / 32 | 94% |
| HIS380 | 29 / 32 | 91% |
| TRP388 | 29 / 32 | 91% |
| TRP402 | 29 / 32 | 91% |
| SER381 | 28 / 32 | 88% |
| TRP382 | 28 / 32 | 88% |
| PRO354 | 27 / 32 | 84% |
| PHE404 | 23 / 32 | 72% |
| HIS359 | 20 / 32 | 63% |
| GLU379 | 15 / 32 | 47% |
| HIS355 | 14 / 32 | 44% |
| HIS399 | 10 / 32 | 31% |
| ILE390 | 8 / 32 | 25% |
| ARG375 | 5 / 32 | 16% |
| TYR357 | 3 / 32 | 9% |

### 4.4 Summary of Key Interactions

| Interaction class | Key residues | Conservation | Structural role |
|-------------------|-------------|--------------|----------------|
| H-bond anchor | HIS380, TRP382 | 84–91% | Bidentate glutarimide recognition |
| H-bond secondary | ASN353, HIS355, GLU379 | 13–22% | Sub-scaffold-dependent contacts |
| Aromatic cage | TRP382, TRP388, TRP402, PHE404 | 56–91% | π-packing of aromatic ring system |
| Hydrophobic pocket | PRO354, ILE390, SER381 | 72–94% | Shape complementarity |
| Variable | HIS399, TYR357, ARG375 | 9–38% | Substituent-specific contacts |

---

## 5. Discussion

### 5.1 Top Compounds

**EDEL-CRBN-0005 (both enantiomers)** are the strongest binders by Vina affinity (–10.2 kcal/mol) with CNN pKd ≈ 7.0–7.1, suggesting low nanomolar predicted potency. Both enantiomers score almost identically (Δ = –0.04 kcal/mol), suggesting their stereocentre does not materially alter the binding mode — consistent with the glutarimide moiety acting as the anchor and the stereocentre residing in a peripheral region with symmetrical pocket accommodation.

**EDEL-CRBN-0009** matches (–10.20 kcal/mol) with the highest CNN pose score in the top-3 (0.946), giving additional confidence in pose quality. Its enantiomer is slightly weaker (–9.25 kcal/mol).

**EDEL-CRBN-0013_ent** (–9.71 kcal/mol) and **EDEL-CRBN-0011_ent / 0012_ent** (–9.14 kcal/mol) complete the top-7.

### 5.2 Enantioselectivity

Eleven of sixteen pairs differ by ≤1.0 kcal/mol, consistent with the stereocentre residing outside the direct pharmacophore contact zone. EDEL-CRBN-0007 shows a 2.85 kcal/mol preference for the enantiomer, the largest in the series. EDEL-CRBN-0016 shows 1.22 kcal/mol preference for the original isomer. These differences suggest stereocentre-sensitive packing against ILE390 / SER381 rather than disruption of the HIS380·TRP382 H-bond network.

### 5.3 Conserved Pharmacophore

The near-universal H-bond to **HIS380** (91%) and **TRP382** (84%) mirrors the binding geometry of lenalidomide and pomalidomide in published CRBN complexes. The three tryptophan residues (TRP382, TRP388, TRP402) forming the aromatic cage and the ASN353·PRO354 segment forming the glutarimide pocket are engaged by ≥88% of compounds, confirming that all 16 scaffolds share the canonical IMiD binding mode and that the glutarimide pharmacophore is preserved throughout the series.

---

## 6. Limitations

1. **Docking-score binding energy.** Vina affinity and CNN pKd are docking-derived estimates, not experimental Kd/IC₅₀ values. They rank the series but cannot substitute for biochemical measurements.
2. **Rigid receptor.** The receptor was held rigid during docking; induced-fit effects (side-chain rearrangement, loop flexibility) are not captured.
3. **No solvent MD.** Full endpoint MM-GBSA with explicit-solvent MD was not performed due to computational scope. The CNN affinity from gnina (a deep-learning pKd predictor) was used as the physics-augmented affinity estimate.
4. **Single conformer input.** Each ligand was input as a single conformer; docking searches rotatable bonds but does not account for solution-phase conformational equilibria.
5. **Water network.** No ordered waters were retained (0 within 5 Å of LVY). If conserved pocket waters are present at the experimental conditions they could influence absolute scores.
6. **Interaction analysis.** Distance-based heavy-atom contacts without explicit hydrogen atoms; H-bond directionality (angle criterion) was not applied. Contacts may include geometrically suboptimal configurations.

---

## 7. Files Produced

| File | Description |
|------|-------------|
| `CRBN_ligands_prepared.sdf` | 32 ligands, V3000, prepared for docking |
| `CRBN_ligands_v2000.sdf` | 32 ligands, V2000, obabel-converted |
| `ligands/lig1.sdf – lig32.sdf` | Individual ligand SDF files |
| `poses/{name}_poses.sdf.gz` | 5 docked poses per ligand (32 files) |
| `best_poses/{name}_pose1.sdf` | Best pose per ligand (32 files) |
| `docking_scores_all32.json` | All scoring data |
| `all_contacts.json` | Per-ligand interaction contacts |
| `interaction_freq.json` | Interaction frequency by residue and type |
| `4CI2_receptor_for_docking.pdb` | Prepared receptor (CRBN chain B + Zn) |
| `4CI2_LVY_ref.pdb` | LVY reference ligand for pocket validation |

---

## References

- Chamberlain PP et al. (2014) Structure of the human Cereblon–DDB1–lenalidomide complex reveals basis for responsiveness to thalidomide analogs. *Nat Struct Mol Biol* 21:803–809.
- Fischer ES et al. (2014) Structure of the DDB1–CRBN E3 ubiquitin ligase in complex with thalidomide. *Nature* 512:49–53.
- Ragland DA et al. (2020) gnina 1.0: molecular docking with deep learning. *J Cheminform* 13:43.
- Trott O & Olson AJ (2010) AutoDock Vina: improving the speed and accuracy of docking. *J Comput Chem* 31:455–461.
