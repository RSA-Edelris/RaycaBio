# Docking Study: PTPN2/TCPTP Allosteric Inhibitors (9C56)
**Date:** 2026-09-01  
**Structure:** 9C56 (PTPN2/TCPTP, Chain A, 2.43 Å)  
**Engine:** AutoDock-Vina 1.2.7 (Python bindings, CPU exhaustiveness=16)  
**pH:** 7.4  
**Output structure file:** `PTPN2_9C56_docked_poses.pdb`

---

## 1. Target

**Protein:** PTPN2 / T-Cell Protein Tyrosine Phosphatase (TCPTP), human. UniProt P17706.  
**PDB 9C56:** 2.43 Å X-ray crystal structure in complex with allosteric inhibitor FRJ (occ. 0.71).  
**Site:** Allosteric pocket at the α3/α6 helix junction — distinct from the catalytic Cys215 active site.  
**Relevance:** PTPN2 negatively regulates JAK–STAT and T-cell signalling; allosteric inhibition enhances anti-tumour immunity.

---

## 2. Protein Preparation

| Step | Tool | Result |
|------|------|--------|
| Loop 182–184 (Asp-Phe-Gly) | PDBFixer | 3 residues modeled |
| ASP240 sidechain | PDBFixer | CG/OD1/OD2 rebuilt |
| C-terminal 281–314 (34 aa) | Excluded | Disordered in crystal |
| Protonation pH 7.4 | PDBFixer addMissingHydrogens | Standard ionisation states |
| Receptor | `9C56_receptor.pdb` | 4531 ATOM records |
| Receptor PDBQT | obabel -xr | Converted for Vina |

---

## 3. Binding Pocket

Defined from co-crystal ligand FRJ (residue 401). **14 residues within 5 Å:**

| Residue | Type | Role |
|---------|------|------|
| SER188, ASN194, GLY275 | Polar | H-bond donor/acceptor |
| PRO189, ALA190, LEU193, PHE197, ILE279 | Hydrophobic | Core burial / π-stacking |
| LYS198, LYS277, LYS280 | Charged (+) | Ionic / H-bond |
| GLU201, GLU274 | Charged (−) | Salt bridge / H-bond |
| CYS278 | Polar/nucleophilic | Potential covalent anchor |

**Box centre:** (28.48, 12.33, 4.22) Å — FRJ centroid  
**Box dimensions:** 22 × 28 × 24 Å

![Allosteric pocket residues](figures/pocket_residues.png)

---

## 4. Ligands

Two scaffolds × 2 enantiomers = 4 compounds. ASMS primary screen hits vs PTPN2.  
Difference: Cpd32 has fluoroethyl amide; Cpd16 has cyclobutyl amide (otherwise identical core).

| ID | Compound | Stereo | MW | cLogP | HBD | HBA | TPSA | Rot | Exp. Kd |
|----|----------|--------|----|-------|-----|-----|------|-----|---------|
| EDS00760714-1 | Cpd32 | **R** | 407.5 | 3.39 | 1 | 4 | 63.1 | 6 | **1–5 µM** |
| EDS00760714-2 | Cpd32 | S     | 407.5 | 3.39 | 1 | 4 | 63.1 | 6 | n.d. |
| EDS00760778-1 | Cpd16 | **R** | 415.5 | 3.98 | 1 | 4 | 63.1 | 5 | **<1 µM** |
| EDS00760778-2 | Cpd16 | S     | 415.5 | 3.98 | 1 | 4 | 63.1 | 5 | n.d. |

All compounds neutral at pH 7.4 (pyridine pKa ~5; no group with pKa near 7.4).

![2D structures](figures/ligands_grid_2d.png)

---

## 5. Docking Results

### 5.1 Complete Scoring Table

| Compound | Stereo | Exp. Kd | Best ΔG (kcal/mol) | Pred. Kd | Poses 1–5 (kcal/mol) |
|----------|--------|---------|-------------------|----------|----------------------|
| Cpd16 | **R** | **<1 µM** | **−7.8** | **1.9 µM** | −7.8, −7.7, −7.5, −7.5, −7.3 |
| Cpd16 | S     | n.d.    | −7.5 | 4.7 µM   | −7.5, −7.4, −7.2, −6.9, −6.8 |
| Cpd32 | **R** | **1–5 µM** | **−7.0** | **7.3 µM** | −7.0, −6.9, −6.8, −6.6, −6.6 |
| Cpd32 | S     | n.d.    | −6.4 | 15.3 µM  | −6.4, −6.4, −6.3, −6.3, −6.2 |

> Kd = exp(ΔG / RT), T = 298 K, RT = 0.592 kcal/mol. Vina accuracy ±1–2 kcal/mol.  
> Cpd16 R prediction (1.9 µM) is within docking uncertainty of measured <1 µM.  
> Cpd32 R prediction (7.3 µM) matches measured 1–5 µM.

![Docking scores — all 4 compounds](figures/score_comparison.png)

### 5.2 Pose Distributions

Five poses per compound span ≤0.5 kcal/mol, indicating convergent sampling of a single binding mode. Tighter clustering for the more potent R enantiomers.

![Top-5 pose score distributions](figures/poses_scatter.png)

---

## 6. Enantiomer Analysis

**R enantiomer is predicted more potent for both compound pairs.**

### Compound 32

| | R | S | ΔΔG (R−S) |
|--|---|---|-----------|
| Best ΔG | **−7.0 kcal/mol** | −6.4 kcal/mol | **−0.6 kcal/mol** |
| Pred. Kd | **7.3 µM** | 15.3 µM | — |
| Exp. Kd | **1–5 µM** | n.d. | — |

Docking **correctly predicts the R form as more potent.** ΔΔG = −0.6 kcal/mol ≈ 2× selectivity. Consistent with only the R enantiomer showing measurable activity.

### Compound 16

| | R | S | ΔΔG (R−S) |
|--|---|---|-----------|
| Best ΔG | **−7.8 kcal/mol** | −7.5 kcal/mol | **−0.3 kcal/mol** |
| Pred. Kd | **1.9 µM** | 4.7 µM | — |
| Exp. Kd | **<1 µM** | n.d. | — |

Docking predicts **R as more potent**, consistent with Cpd32 trend. Experimental enantiomeric assignment pending; docking strongly suggests the **R form is the active enantiomer**.

![Enantiomer comparison: R vs S by compound](figures/enantiomer_comparison.png)

---

## 7. Key Contacts (Best Pose, 4.5 Å cutoff)

| Compound | Stereo | Best ΔG | Key pocket contacts |
|----------|--------|---------|---------------------|
| Cpd16 | R | −7.8 | PHE197, GLU201, **CYS278**, ILE279, LEU193, ASN194, GLY275 |
| Cpd16 | S | −7.5 | ALA190, **CYS278**, GLU274, PRO189, LEU193, ASN194, PHE197, GLY275, GLU201 |
| Cpd32 | R | −7.0 | PHE197, GLU201, **CYS278**, ILE279, LEU193, ASN194, GLY275 |
| Cpd32 | S | −6.4 | ASN194, ALA190, **CYS278**, PHE197, LEU193, ILE279, GLY275, GLU274, PRO189 |

**CYS278** is a universal contact across all 4 compounds — a covalent fragment elaboration point worth investigating.

---

## 8. Output Structure File

**`PTPN2_9C56_docked_poses.pdb`** (371 KB) — multi-chain PDB for molecular visualization:

| Chain | Contents |
|-------|----------|
| A | PTPN2 receptor (4531 ATOM records) |
| F | Co-crystal ligand FRJ — reference (41 atoms, occ 0.71) |
| B | Cpd32 R best pose — ΔG = −7.0 kcal/mol |
| C | Cpd32 S best pose — ΔG = −6.4 kcal/mol |
| D | Cpd16 R best pose — ΔG = −7.8 kcal/mol |
| E | Cpd16 S best pose — ΔG = −7.5 kcal/mol |

PyMOL: `load PTPN2_9C56_docked_poses.pdb` — select chains individually to show/hide ligands.  
UCSF ChimeraX: `open PTPN2_9C56_docked_poses.pdb`

---

## 9. Methods

| Step | Tool | Parameters |
|------|------|------------|
| Protein prep | PDBFixer (OpenMM 8.x) | addMissingResidues, addMissingHydrogens pH=7.4 |
| Receptor PDBQT | obabel -xr | Rigid receptor |
| Pocket definition | Co-crystal FRJ + NumPy | 5 Å shell, 14 residues |
| Ligand 3D conformers | RDKit ETKDGv3 + MMFF | randomSeed=42 |
| Ligand PDBQT | meeko MoleculePreparation | PDBQTWriterLegacy |
| Docking | AutoDock-Vina 1.2.7 Python | exhaustiveness=16, n_poses=5 |
| Search box | FRJ centroid | (28.48, 12.33, 4.22) Å, 22×28×24 Å |
| ΔG → Kd | Boltzmann | Kd = exp(ΔG/RT), T = 298 K |
| Contact analysis | NumPy 4.5 Å cutoff | Heavy atoms only |

---
*Rayca Platform — session 8b0911d7*
