## Summary

EL2003A pose 2 (the top-ranked GNINA pose, affinity −9.80 kcal/mol) was refined by 1 ns explicit-solvent GROMACS molecular dynamics. Binding free energy was recalculated by MM-GBSA (OBC2 implicit solvent, 1-trajectory approach) over 91 production frames (100–1000 ps).

**MD-refined ΔG_bind = −44.51 ± 2.56 kcal/mol** (mean ± SD, 91 frames)

---

## Methods

### System Preparation

| Parameter | Value |
|:---|:---|
| Receptor | 1Z5M PDK1 (PDBFixer pH 7.4, all H stripped before tleap) |
| Ligand | EL2003A pose 2 (`EL2003A_pose2.sdf`, 37 atoms, GNINA rank 1) |
| Protein FF | AMBER03 |
| Ligand FF | GAFF2 (Gasteiger charges) |
| Water model | TIP3P |
| Box | Dodecahedron, ~7.9 nm sides |
| Ions | 0.15 M NaCl |

### MD Protocol (GROMACS 2026+GPU)

| Stage | Steps | dt (fs) | Notes |
|:---|:---|:---|:---|
| Energy minimisation | 50 000 | — | Steepest descent |
| NVT equilibration | 50 000 | 2 | Berendsen thermostat, 300 K |
| NPT equilibration | 50 000 | 2 | Parrinello-Rahman, 1 bar |
| Production MD | 500 000 | 2 | **1 ns total**; frame every 10 ps |

Performance: 168 ns/day on A100 GPU (Rayca sandbox). Total wall time: ~514 s.

### MM-GBSA Protocol

| Parameter | Value |
|:---|:---|
| Method | 1-trajectory MM-GBSA |
| Implicit solvent | OpenMM OBC2 (ε_in = 1, ε_out = 80) |
| GB radii | mbondi2 (assigned via ParmEd changeRadii) |
| Frames analysed | 91 (100–1000 ps, first 100 ps discarded as equilibration) |
| Trajectory tool | ParmEd 4.3.1 + MDTraj 1.11.1 + OpenMM 8.5.2 |
| ΔG formula | ΔG = ⟨E_complex − E_receptor − E_ligand⟩_OBC2 |

---

## Results

### Binding Free Energy

| Quantity | Value |
|:---|:---|
| **ΔG_bind (MD-ensemble, mean)** | **−44.51 kcal/mol** |
| ΔG_bind (SD) | 2.56 kcal/mol |
| ΔG_bind (SEM) | 0.27 kcal/mol |
| ΔG_bind range | −50.32 to −35.62 kcal/mol |
| Prior EM-mode value | −61.84 kcal/mol |
| GNINA CNN affinity | −9.80 kcal/mol |

### Energy Components (mean over 91 frames)

| Component | Value (kcal/mol) |
|:---|:---|
| ⟨E_complex⟩ | −4 778.9 |
| ⟨E_receptor⟩ | −5 024.4 |
| ⟨E_ligand⟩ | +290.0 |
| **ΔG_bind** | **−44.51** |

The positive ligand internal energy (+290 kcal/mol) reflects the intramolecular strain and solvation penalty of EL2003A in the bound conformation.

### Convergence

| Checkpoint | Running mean ΔG_bind |
|:---|:---|
| 200 ps (frame 20) | −43.1 kcal/mol |
| 500 ps (frame 50) | −43.4 kcal/mol |
| 1000 ps (frame 100) | −44.5 kcal/mol |

The running mean drifts < 1 kcal/mol over the final 500 ps, indicating adequate convergence for a qualitative estimate.

---

## Interpretation

The MD-refined ΔG_bind (−44.51 kcal/mol) is ~17 kcal/mol less negative than the single-point EM-mode value (−61.84 kcal/mol). This is expected: EM-mode collapses the complex to a local energy minimum, while the MD ensemble samples thermal fluctuations that include less optimal contact geometries. The MD-refined value is a more realistic estimate of binding affinity under physiological conditions.

EL2003A maintains stable contacts throughout 1 ns of MD with no evidence of pose dissociation (per-frame ΔG remains negative and bounded within ≈15 kcal/mol), consistent with strong PDK1 binding.

---

## Limitations

1. **No entropy correction**: MM-GBSA as computed here omits translational, rotational, and vibrational entropy (ΔS). Including normal-mode entropy typically raises ΔG_bind by +10–20 kcal/mol, bringing calculated values closer to experimental ΔG.
2. **1-trajectory approximation**: Receptor and ligand geometries are extracted from the complex trajectory; conformational relaxation upon unbinding is not sampled.
3. **Implicit vs. explicit solvent**: OBC2 post-processing differs from the TIP3P explicit solvent used during MD; the rescoring is an approximation.
4. **Force field**: AMBER03 protein / GAFF2 ligand — slightly older parameter set; AMBER14SB/GAFF2 would be preferred for a publication-quality result.

---

## Files

| File | Description |
|:---|:---|
| `gbsa_run/EL2003A_pose2/traj_com.xtc` | GROMACS production trajectory (101 frames, 1 ns) |
| `gbsa_run/EL2003A_pose2/complex.top` | GROMACS topology (AMBER03+GAFF2) |
| `gbsa_run/EL2003A_pose2/complex.pdb` | Final complex structure |
| `gbsa_run/EL2003A_pose2/complex.GMX/md.log` | GROMACS MD log (performance: 168 ns/day) |
| `mmgbsa_result.json` | Per-frame energies and summary statistics |
| `mmgbsa_calc.py` | MM-GBSA calculation script (ParmEd + OpenMM OBC2) |
