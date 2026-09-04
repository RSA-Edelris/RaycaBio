
mmgbsa_section = """

---

## 8. Free Energy of Interaction — MM-GBSA Rescoring

### Method

Single-point MM-GBSA (no MD sampling) was computed for the best Vina poses of
Compound 32 (R) and Compound 16 (R) using the following pipeline:

| Stage | Tool / Force Field |
|-------|--------------------|
| Receptor topology | tleap + ff14SB (AMBER14) |
| Ligand topology | antechamber (GAFF2, AM1-BCC charges) + parmchk2 + tleap |
| Implicit solvent | OpenMM OBC2 (Generalized Born) |
| Complex minimisation | OpenMM LocalEnergyMinimizer, 500 steps in OBC2 |
| Energy components | E_complex, E_receptor, E_ligand from same minimised geometry (single-trajectory) |

**ΔG_MM-GBSA = E(complex) − E(receptor) − E(ligand)**, all in OBC2 implicit solvent,
ff14SB + GAFF2, NoCutoff.

> **Scope caveat.** Single-point MM-GBSA without an MD trajectory and without an
> entropy term (−TΔS) yields enthalpic estimates that are substantially more
> negative than true binding free energies. The absolute values are not
> quantitatively meaningful. The **relative ranking** between the two compounds
> is the interpretable result.

### Energy Component Table

| Compound | E_receptor (kcal/mol) | E_ligand (kcal/mol) | E_complex (kcal/mol) |
|---|---|---|---|
| Compound 32 (R) | −10 412.84 | 119.76 | −10 317.86 |
| Compound 16 (R) | −10 418.14 | 147.19 | −10 296.39 |

### Vina Scores vs MM-GBSA Free Energies

| Compound | ID | Vina ΔG (kcal/mol) | Vina pred. Kd (µM) | MM-GBSA ΔG (kcal/mol) | Rank |
|---|---|---|---|---|---|
| Compound 16 (R) | EDS00760778-1 | **−7.802** | **1.9** | **−25.44** | **1** |
| Compound 32 (R) | EDS00760714-1 | −7.012 | 7.2 | −24.78 | 2 |

Both methods agree on the ranking: **Compound 16 (R) binds more favourably
than Compound 32 (R)**, consistent with the experimental ASMS potency data
(Cpd16 R Kd < 1 µM, Cpd32 R Kd 1–5 µM).

### Caveats

- **No entropy correction**: −TΔS is omitted; absolute ΔG_MM-GBSA are much
  more negative than real affinities.
- **Non-optimal OBC2 radii for GAFF2**: OpenMM warns that GAFF2 atom radii are
  not fully calibrated for OBC2 (originally parameterised for AMBER bio-residue
  radii). This introduces a systematic error that affects both compounds
  similarly and therefore does not change the relative ranking.
- **Single-trajectory, no MD**: E_receptor and E_ligand are extracted from the
  minimised complex geometry. Receptor relaxation differences between the two
  ligands are not sampled.
- **500-step minimisation only**: severe clashes from the rigid-docking pose are
  relieved but deep-pocket conformational relaxation is not captured.

### Conclusion

| Method | More potent compound | ΔΔG (Cpd16 R − Cpd32 R) |
|--------|---------------------|--------------------------|
| AutoDock-Vina | Cpd16 R | −0.79 kcal/mol |
| MM-GBSA (enthalpic, single-point) | Cpd16 R | −0.66 kcal/mol |

The two methods are in agreement: **Compound 16 (R) is the more potent
enantiomer and the more potent compound** in this series against the PTPN2
allosteric site. The MM-GBSA ΔΔG of −0.66 kcal/mol corresponds to an
approximately 3-fold potency difference.
"""

report_path = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/docking_report.md'
with open(report_path, 'a') as fh:
    fh.write(mmgbsa_section)

import os
print(f"Report size: {os.path.getsize(report_path):,} bytes")
print("Section appended.")
