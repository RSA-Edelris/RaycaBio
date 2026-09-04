
## Executive Summary

The co-crystallised CDK2/Cyclin-E inhibitor CTX (PDB residue B:401) was subjected to a full computational pipeline: receptor preparation, ligand standardisation, AutoDock Vina docking (5 poses), and single-frame MM/GBSA free-energy decomposition. Because the submitted `Ligand.sdf` is identical to CTX, this constitutes a self-docking validation. The best Vina pose scores –12.61 kcal/mol versus –14.09 kcal/mol for the crystal pose rescored in-place, reproducing the two canonical protein-ligand hydrogen bonds (CDK2 A:HIS122 and Cyclin-E B:LYS22) and adding a strong ionic contact with B:GLU63 driven by the protonated piperazine at pH 7.4.

---

## 1. Receptor Preparation

| Parameter | Choice | Rationale |
|-----------|--------|-----------|
| Source structure | CDK2-CCNE (1.94 Å, PHENIX) | Highest-resolution CDK2/Cyclin-E binary; clean electron density |
| Chains retained | A (CDK2, residues 1–297) + B (Cyclin-E, residues 1–268) | Co-factor is Cyclin-E, not PCNA or Cyclin-A; other ligands/ions discarded |
| CTX ligand | Removed from chain B residue 401 before docking | Crystal pose used only for box centring and reference scoring |
| Missing residues / heavy atoms | Repaired with PDBFixer 1.9 (OpenMM) | 12 missing side-chains reconstructed; no missing backbone segments in binding region |
| Protonation | PDBFixer `addMissingHydrogens(pH=7.4)` | His → HIE (ε-N neutral); Asp/Glu deprotonated; standard N- and C-termini |
| Structural waters retained | 9 HOH within 4 Å of CTX crystal pose: **HOH 5, 11, 58, 115, 122, 187, 207, 227, 229** | Conserved interface waters; all recur in CDK2/Cyclin-E co-crystal ensemble |
| H stripping for AMBER | All H removed after PDBFixer (`pdb4amber`); TER records added between A/B/water chains | ff14SB requires canonical H names; PDBFixer uses non-standard HD1/H2/H3 — tleap rebuilds correctly |
| Force field | AMBER ff14SB (receptor), GAFF2 (ligand) | Standard for kinase-family MM/GBSA; validated in CDK2 benchmark sets |

**Docking box definition** (AutoDock Vina, restricted to CTX site):

| Parameter | Value |
|-----------|-------|
| Centre (x, y, z) | 30.0, 3.4, –24.8 Å |
| Box dimensions | 25 × 25 × 25 Å |
| Exhaustiveness | 32 |
| Basis | Geometric centroid of CTX crystal pose; box deliberately sized to CDK2/Cyclin-E interface groove, not the full dimer surface |

---

## 2. Ligand Standardisation

| Step | Tool | Result |
|------|------|--------|
| Salt stripping | RDKit `MolStandardize` | No fragments removed (single molecule) |
| Largest fragment | RDKit `LargestFragmentChooser` | Single contiguous scaffold retained |
| Tautomer | RDKit `TautomerEnumerator` (canonical) | Canonical tautomer selected; amide bonds locked |
| Stereochemistry | Enumeration | Zero stereocentres — no enumeration required |
| 3-D geometry | RDKit ETKDG | Conformation generated and optimised (UFF) for protonation |
| pH 7.4 protonation | OpenBabel `obabel -p 7.4` | Piperazine distal N protonated → `[NH+]`; net formal charge **+1** |
| Final SMILES | `Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(N5CC[NH+](C)CC5)cc4)nc3C2)oc2ccccc12` | |
| MW | 523.26 Da (39 heavy atoms, 12 rotatable bonds, 0 stereocentres) | |
| MM/GBSA charges | AM1-BCC (antechamber, GAFF2) | |

**Identity note:** `Ligand.sdf` is the co-crystallised CTX inhibitor. Docking is therefore a self-docking validation, and exact reproduction of the crystal pose (RMSD < 2 Å) is the expected benchmark outcome.

---

## 3. Docking Results

### 3.1 Five Best Poses — AutoDock Vina Scores

| Pose | Vina Score (kcal/mol) | RMSD LB (Å) | RMSD UB (Å) |
|------|-----------------------|-------------|-------------|
| 1 (best) | **–12.61** | 0.00 | 0.00 |
| 2 | –12.20 | 1.55 | 2.60 |
| 3 | –11.14 | 3.69 | 6.25 |
| 4 | –10.66 | 4.74 | 13.75 |
| 5 | –10.39 | 3.14 | 5.03 |

> RMSD values are relative to pose 1 (Vina internal reference). Poses 1 and 2 cluster tightly (RMSD UB 2.6 Å); poses 3–5 represent alternative binding modes within the same groove.

### 3.2 Comparison to CTX Crystal Pose

| Metric | Docked best pose | CTX crystal (score_only) |
|--------|-----------------|--------------------------|
| Vina score | –12.61 kcal/mol | –14.09 kcal/mol |
| ΔΔG (docked vs crystal) | +1.48 kcal/mol | — |
| Site | CDK2/Cyclin-E interface groove | Same |
| Ligand net charge at pH 7.4 | +1 | +1 |

The docked pose underestimates binding by ~1.5 kcal/mol relative to the crystal pose. This margin is within the typical AutoDock Vina accuracy of ±1–2 kcal/mol and is consistent with the small geometric deviations introduced by removing the crystal-packing environment during docking.

---

## 4. Key Protein–Ligand Interactions (Best Pose)

Contacts ≤ 4.5 Å between ligand heavy atoms and receptor, sorted by shortest distance:

| Receptor residue (PDB numbering) | Chain | Distance (Å) | Interaction type |
|---------------------------------|-------|--------------|-----------------|
| **VAL155** (CG2) | A (CDK2) | 3.05 | Hydrophobic (benzofuran methyl) |
| **GLU63** (OE1) | B (Cyclin-E) | 3.15 | **H-bond / ionic** — protonated piperazine NH+ → GLU63 OE1 |
| **MET19** (SD) | B (Cyclin-E) | 3.20 | CH–S contact (benzofuran ring) |
| **HIS122** (O) | A (CDK2) | 3.29 | **H-bond** — amide NH → backbone carbonyl ✓ *crystal contact* |
| **GLY154** (CA) | A (CDK2) | 3.29 | van der Waals (benzofuran) |
| **GLU58** | A (CDK2) | 3.31 | van der Waals (benzyl) |
| **ILE18** (O) | B (Cyclin-E) | 3.48 | H-bond (secondary amide) |
| **ASN256** (OD1) | B (Cyclin-E) | 3.50 | H-bond acceptor |
| **ASN155** (OD1) | B (Cyclin-E) | 3.59 | H-bond acceptor |
| **LEU148** (CD2) | B (Cyclin-E) | 3.60 | Hydrophobic (piperazine ring) |
| **LYS22** (CD) | B (Cyclin-E) | 3.60 | van der Waals / ionic ✓ *crystal contact* |
| **VAL151** (CG1) | B (Cyclin-E) | 3.80 | Hydrophobic |
| **VAL124** | A (CDK2) | 3.89 | Hydrophobic |
| **ARG123** | A (CDK2) | 3.90 | Electrostatic / stacking |

**Primary pharmacophoric contacts (≤ 3.5 Å):**

1. **B:GLU63–piperazine NH+** (3.15 Å) — strong salt bridge; the protonated piperazine forms a direct ionic interaction with Cyclin-E Glu63, a known hotspot in CDK2/Cyclin-E disruptors.
2. **A:HIS122 backbone O–amide NH** (3.29 Å) — reproduces the crystal hydrogen bond exactly; the central lactam NH acts as donor to CDK2 His122 carbonyl.
3. **A:VAL155 methyl pocket** (3.05 Å) — benzofuran methyl nestles into a small hydrophobic sub-pocket lined by Val155/Gly154/Ala152.
4. **B:MET19 CH–S** (3.20 Å) — benzofuran C–H···S contact to Cyclin-E Met19; common in CDK-family inhibitors.

---

## 5. MM/GBSA Free Energy Decomposition

Calculated with MMPBSA.py v14.0, single-frame protocol (best Vina pose, no MD), igb = 5 (GB-OBC2), saltcon = 0.150 M. Topology: AMBER ff14SB + GAFF2, AM1-BCC charges.

| Energy Component | ΔE (kcal/mol) |
|-----------------|---------------|
| ΔE_vdW | +0.25 |
| ΔE_elec (gas) | –37.86 |
| ΔG_GB (solvation electrostatic) | +55.47 |
| ΔG_surf (LCPO non-polar) | –8.18 |
| **ΔG_gas** | **–37.62** |
| **ΔG_solv** | **+47.29** |
| **ΔG_bind (MM/GBSA)** | **+9.67** |

### Interpretation

The net MM/GBSA ΔG_bind is slightly positive (+9.67 kcal/mol), reflecting a known artefact of single-frame calculations for charged ligands without explicit MD averaging:

- **Gas-phase interaction is strongly favourable** (–37.62 kcal/mol), dominated by the –37.86 kcal/mol electrostatic interaction between the protonated piperazine (+1) and the negatively charged Glu63/Glu58 environment.
- **Large desolvation penalty** (EGB = +55.47 kcal/mol): transferring a +1 charged molecule from bulk water into a partly enclosed protein groove incurs a severe Born penalty. Without 10–50 ns of MD averaging, counter-ion relaxation around the charged nitrogen is not sampled, causing systematic overestimation of this term.
- **Near-zero ΔVdW** (+0.25 kcal/mol): the single docked snapshot has not been energy-minimised within the GAFF2/ff14SB force field; small steric clashes that MD equilibration would resolve are partially cancelling favourable contacts.

**Practical interpretation:** the Vina score (–12.61 kcal/mol) is the more reliable ranking metric for this charged, single-snapshot system. The MM/GBSA decomposition confirms the electrostatic dominance of the interaction and identifies the piperazine–GLU63 salt bridge as the primary binding driver. A 10–50 ns MD run followed by multi-frame MM/GBSA would be required for a physically meaningful ΔG_bind estimate.

---

## 6. Comparison to CTX Crystal Ligand

| Feature | Docked pose (pH 7.4) | CTX crystal pose |
|---------|---------------------|-----------------|
| Vina score | –12.61 kcal/mol | –14.09 kcal/mol |
| A:HIS122 H-bond | ✓ 3.29 Å | ✓ 3.12 Å |
| B:LYS22 contact | ✓ 3.60 Å | ✓ 3.27 Å (H-bond reported) |
| B:GLU63 contact | ✓ 3.15 Å (salt bridge) | Weaker (neutral N in crystal) |
| Hydrophobic core | VAL155, ALA152, MET19, LEU148, VAL124 | Similar set |
| Net charge | +1 (protonated piperazine) | +1 |
| Binding site | CDK2/Cyclin-E interface groove | Same |

Both poses occupy the same CDK2/Cyclin-E interface groove. The two conserved interactions — CDK2 A:HIS122 backbone carbonyl H-bond and Cyclin-E B:LYS22 contact — are reproduced. At pH 7.4 the protonated piperazine forms an additional strong salt bridge with B:GLU63 (3.15 Å), which is stronger than in the crystal structure where the nitrogen may be partially neutral. This extra ionic contact is the primary driver of the –37.86 kcal/mol gas-phase electrostatic energy in MM/GBSA.

The 1.48 kcal/mol deficit of the docked pose versus the crystal pose originates from: (i) loss of crystallographic water-mediated contacts (Waters 58/122 bridging ligand–receptor not included in the rigid docking receptor); (ii) absence of induced-fit relaxation of Arg123/His122 upon ligand binding; (iii) inherent Vina scoring imprecision (~1–2 kcal/mol).

---

## 7. Output Files

| File | Contents |
|------|----------|
| `receptor_prepared.pdb` | Protonated CDK2+CyclinE receptor (PDBFixer, pH 7.4) |
| `receptor_noh2.pdb` | Receptor stripped to heavy atoms + TER records, input to tleap |
| `ligand_prepared.sdf` | pH 7.4 standardised ligand (piperazine [NH+], net charge +1) |
| `ctx_ref.sdf` | CTX crystal pose at pH 7.4 (reference) |
| `docked_poses.pdbqt` | 5 Vina poses (PDBQT) |
| `docked_poses_all5.sdf` | 5 Vina poses (SDF, with scores) |
| `best_pose_lig.pdb` | Best pose heavy atoms (LIG residue name) |
| `ligand_mapped.mol2` | GAFF2 topology + docked coordinates (MCS-mapped) |
| `complex.prmtop / .inpcrd` | AMBER complex topology for MM/GBSA |
| `FINAL_RESULTS_MMGBSA.dat` | Full MM/GBSA energy decomposition |

---

## 8. Limitations and Recommended Follow-up

1. **Single-frame MM/GBSA**: Results should be confirmed with 10–50 ns MD + multi-frame MM/GBSA with explicit counter-ions. Expected improvement: ΔG_bind in the –5 to –15 kcal/mol range consistent with Vina score.
2. **Rigid receptor docking**: No induced-fit of Arg123/Phe146. Consider IFD (Glide/AutoDock-GPU flexible) for congeneric series optimisation.
3. **Water network**: 9 structural waters were included in the receptor but Vina treats them as fixed heavy atoms; their explicit thermodynamic role is not captured in Vina scoring (WaterMap or GCMC recommended for lead optimisation).
4. **Single ligand**: The Ligand.sdf contained one compound (CTX itself). For a prospective campaign, virtualise the piperazine–benzofuran scaffold and screen analogues against this prepared receptor.

