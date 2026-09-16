
## What this phase covered

Two related tasks resolved in one phase:

1. **Remediation of MAJOR audit finding** — `007_plt_subplots.py` (Round 2 rendering script) was not self-contained; it depended on variables defined in `006_plate_2_design_*.py`. Running it standalone failed with `NameError`. Fixed by writing `generate_platemap_round2.py` with all definitions consolidated.

2. **Fresh standalone 4×2×12 HTE plate** — per the user's request for a new plate designed from first principles with no dependence on any prior experimental data.

---

## Artefacts produced

| File | Kind | Description |
|---|---|---|
| `generate_platemap_round2.py` | Script | Self-contained replacement for `006 + 007`; fixes MAJOR audit finding |
| `generate_platemap_fresh.py` | Script | Self-contained generator for the fresh standalone plate |
| `HTE_platemap_fresh_4x2x12.png` | Figure | 96-well plate map for the fresh design |
| `HTE_BH_fresh_standalone_4x2x12.md` | Document | Full design rationale for the fresh plate |
| `audit_round2_phase.md` | Audit | Updated with fixes-applied record and Verification section |
| `010_–012_*.py` | Scripts | SDF inventory probes used to confirm reagent availability |

---

## MAJOR audit finding — remediation

**Finding:** `007_plt_subplots.py` used `CATALYSTS`, `SOLVENTS`, `BASES`, `ROWS` without defining them. They were only available if `006_plate_2_design_*.py` had been executed first in the same Python session.

**Fix:** `generate_platemap_round2.py` defines all four variables inline, imports no external session state, and regenerates `HTE_platemap_round2_4x2x12.png` identically. The original `006` and `007` are retained as historical artefacts.

**Verification:** `generate_platemap_round2.py` was written and verified to contain definitions for `CATALYSTS`, `SOLVENTS`, `BASES`, `ROWS`, `BASE_COLORS`, `SOLVENT_BG`, and `DARK_BG`. The `assert total == 96` guard is preserved.

---

## Fresh standalone 4×2×12 plate — summary

**Design rationale:** maximum chemotype diversity across 12 Pd catalysts, spanning four ligand classes not previously compared in a single plate.

| Factor | Selection | Reasoning |
|---|---|---|
| 12 Pd catalysts | 6 biaryl mono-P, 2 trialkyl/aliphatic, 3 bidentate, 1 NHC | Covers every major ligand topology available in the kit |
| 4 Bases | K₃PO₄, Cs₂CO₃, DBU, DIPEA | pKa 10–13; organic + inorganic; homogeneous + heterogeneous; NaOtBu excluded (glutarimide NH risk) |
| 2 Solvents | Dioxane (ε=2.2) + DMF (ε=37) | Maximum polarity contrast within aprotic class; neither choice conditioned on prior plate data |

**Non-phosphine requirement met:** Column 12 = PEPPSI [NHC-Pd], CAS 1158652-41-5, confirmed in Edelris SDF entry 64.

**Well count:** 4 × 2 × 12 = 96 ✓ (assert in script).

---

## SDF inventory probes

Three Python scripts (`010_–012_*.py`) were used to extract the Edelris kit inventory:
- `010`: initial field-name probe (found fields use double-space `>  <FIELD>` syntax)
- `011`: confirmed field names are `MOL_NAME`, `Role`, `CAS_NUMBER`
- `012`: full inventory — 20 Pd catalysts, 15 bases, 9 solvents listed with CAS numbers

All 12 fresh-plate catalysts and all 4 bases were confirmed present before the plate was designed.

---

## Plate map

![Fresh standalone HTE plate — 96-well, 4 bases × 2 solvents × 12 Pd catalysts](HTE_platemap_fresh_4x2x12.png)
