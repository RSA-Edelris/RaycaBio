
## Objective

Perform single-frame MM-GBSA endpoint rescoring of the best docking pose for each of the 22 stereoisomers, compute protein–ligand interaction fingerprints, produce an annotated SDF with all scores, and write the final campaign report.

---

## MM-GBSA Protocol

### Receptor Preparation for AMBER

The docking receptor (`4CI2_receptor_for_docking.pdb`) required two fixes before tleap would accept it:

1. **Histidine naming**: PDBFixer writes `HIS` regardless of protonation state. tleap maps `HIS`→`HIE` by default, but the PDB had δ-protonated residues (with `HD1` atoms) — unrecognised in the `HIE` template. Fix: inspected each `HIS` residue for `HD1` vs `HE2` atoms and renamed to `HID` (12 residues) or `HIE` (1 residue, Res 264).

2. **N-terminal atom naming**: AMBER `NMET` template expects `H1/H2/H3` for the ammonium protons. PDBFixer had written `H/H2/H3`. Fix: renamed `H`→`H1` at Met47.

**Fixed receptor**: `mmgbsa2/receptor_amber.pdb`

### Per-Compound Pipeline

| Step | Tool | Key parameters |
|------|------|----------------|
| Ligand parameterisation | antechamber | `-c gas` (Gasteiger), `-at gaff2`, GAFF2 FF |
| Missing parameters | parmchk2 | GAFF2 |
| System assembly | tleap | ff14SB (protein) + GAFF2 (ligand), no explicit water |
| Topology→trajectory | cpptraj | 1-frame NetCDF from inpcrd |
| Free energy | MMPBSA.py | igb=5, saltcon=0.100, endframe=1 |

**Charge method note**: AM1BCC (`-c bcc`) timed out after 180 s on compounds with 30–38 heavy atoms. Switched to Gasteiger (`-c gas`) which completes in <1 s. Values are suitable for *relative* ranking within the series, not absolute ΔG estimates.

**Net receptor charge**: +7 (from basic residues at pH 7.4); handled by GB solvation term. No counterions were added (single-frame, no dynamics).

**Results**: 22/22 compounds succeeded.

---

## MM-GBSA Results

| Compound | Parent | ΔG_GBSA (kcal/mol) | VdW | EEL | EGB |
|----------|--------|--------------------|-----|-----|-----|
| Compound_4_s12 | Compound_4 | −37.6 | — | — | — |
| Compound_4_s16 | Compound_4 | −36.1 | — | — | — |
| Compound_10_ent2 | Compound_10 | −36.0 | — | — | — |
| Compound_4_s8 | Compound_4 | −35.6 | — | — | — |
| Compound_4_s1 | Compound_4 | −33.1 | — | — | — |
| Compound_10_ent1 | Compound_10 | −33.0 | — | — | — |
| Compound_4_s9 | Compound_4 | −33.0 | — | — | — |
| Compound_4_s5 | Compound_4 | −30.7 | — | — | — |
| Compound_7_ent2 | Compound_7 | −30.6 | — | — | — |
| Compound_11_ent2 | Compound_11 | −30.3 | — | — | — |
| Compound_11_ent1 | Compound_11 | **+9.4** ⚠️ | — | — | — |

Full per-term breakdown in `mmgbsa2_results.json`. Compound_11_ent1 is the only compound with a positive ΔG (unfavourable binding), consistent with a geometrically mismatched docked pose for this enantiomer.

---

## Interaction Analysis

ProLIF v2.2.1 was attempted but crashed with exit code 139 (segfault) when converting the full 6 188-atom receptor to RDKit molecule, even after restricting to binding-site residues within 8 Å. A custom RDKit-only interaction fingerprinter was written (`run_interactions_rdkit.py`) with the following geometry criteria:

| Interaction | Threshold |
|------------|-----------|
| H-bond (donor/acceptor) | D–A ≤ 3.5 Å, angle ≥ 120° |
| Hydrophobic | C–C ≤ 4.0 Å (non-aromatic) |
| π-stacking | centroid–centroid ≤ 5.5 Å, angle ≤ 30° or ≥ 60° |
| π-cation | centroid–N ≤ 5.0 Å |

All 22 poses analysed in ~2 s; results in `interaction_fingerprints.json`.

### Key Pharmacophoric Features (frequency over 22 compounds)

| Residue | Interaction | Frequency |
|---------|------------|:---------:|
| TRP388 | Hydrophobic | 100% |
| TRP402 | Hydrophobic + PiCation | 95% |
| TRP388 | PiCation | 95% |
| TRP382 | Hydrophobic + PiCation | 82% |
| HID380 | HBDonor + HBAcceptor | 77% / 73% |
| ILE390 | Hydrophobic | 50% |
| PHE404 | Hydrophobic | 45% |

The binding pocket is a **tri-tryptophan aromatic cage** (TRP382/388/402) with HID380 as the gating H-bond residue — consistent with the canonical CRBN pharmacophore described in the literature for molecular glue degraders.

---

## Annotated SDF

`CRBN_ID_enantio2_docking_GBSA.sdf` — 22 poses with SD tags:
- `Docking_Affinity_kcal_mol`
- `CNN_Affinity`
- `MMGBSA_dG_kcal_mol`
- `MMGBSA_VdW_kcal_mol`, `MMGBSA_EEL_kcal_mol`, `MMGBSA_EGB_kcal_mol`
- `Interacting_Residues`
- `HBond_Residues`
- `N_Interactions`

---

## Output Artifacts

| File | Description |
|------|-------------|
| `mmgbsa2_results.json` | MM-GBSA ΔG, VdW, EEL, EGB, ESURF per compound |
| `mmgbsa2/` | Per-compound AMBER topology + MMPBSA output |
| `mmgbsa2/receptor_amber.pdb` | AMBER-corrected receptor (HID/HIE, H1 N-term) |
| `interaction_fingerprints.json` | Per-compound interactions + frequency tables |
| `run_interactions_rdkit.py` | Custom RDKit interaction fingerprinter |
| `CRBN_ID_enantio2_docking_GBSA.sdf` | Annotated SDF with all scores (82 KB) |
| `CRBN_docking_mmgbsa_report.md` | Full campaign report (11.9 KB) |

---

## Limitations

- Single-frame MM-GBSA; no MD relaxation. Outliers (Compound_11_ent1 +9.4 kcal/mol) should be re-examined with short MD.
- Gasteiger charges: adequate for rank-ordering, not calibrated for absolute ΔG.
- Custom interaction analysis: geometry-based only, no electrostatic potential; may over- or under-count near-threshold interactions.
- ProLIF segfault: root cause not fully diagnosed; the custom RDKit approach is a valid but less validated alternative.
