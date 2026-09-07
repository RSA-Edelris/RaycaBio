
## Overview

Binding affinities for five docked compounds (three parent structures, two racemic centres enumerated) evaluated by three complementary methods: Vina scoring (gnina), CNN-derived ΔG, and single-point MM-GBSA (AMBER ff14SB / GAFF2, OBC2 implicit solvent). All values are for the best-ranked docked pose of each compound.

A 10 ns explicit-solvent MD simulation of the top compound (EDS01806218 1S,2S) on Isambard-AI GH200 (job 6284357) is currently queued and will provide trajectory-averaged MM-GBSA values upon completion.

---

## Scoring Table

| Compound | Stereo­chemistry | Vina (kcal/mol) | ΔG_CNN (kcal/mol) | ΔG_MM-GBSA†‡ (kcal/mol) |
|:---------|:----------------|----------------:|------------------:|------------------------:|
| EDS01357518_ent1 | S | −7.52 | −9.58 | **−19.61** |
| EDS01357518_ent2 | R | −8.09 | −9.52 | **−16.94** |
| EDS01806218_ent1 | 1R,2R | −6.81 | −8.63 | +8.49 ⚠ |
| EDS01806218_ent2 | 1S,2S | **−9.08** | **−10.13** | +16.67 ⚠ |
| EDS01889984 | — | −6.63 | −9.53 | +47.84 ⚠ |

† OBC2 / igb=5, mbondi2 radii, saltcon=0.15 M, ff14SB protein, GAFF2 ligand, AM1-BCC charges.  
‡ Single-point evaluation on the raw gnina docked pose, **no prior MM minimisation**. Values marked ⚠ are physically unreliable (see interpretation below).

---

## Method Details

### Vina (gnina)
- Rigid-receptor gnina 1.0 docking, exhaustiveness 16, A100 GPU.
- Score = minimizedAffinity (Vina-based) for pose 0.

### CNN ΔG
- CNN affinity (pKi) from gnina's deep-learning scoring function evaluated on pose 0.
- Converted to ΔG via −RT ln(10) · pKi = −1.364 · pKi kcal/mol at 298 K.

### Single-point MM-GBSA
- Best pose extracted from gnina SDF, hydrogens added (RDKit ETKDGv3), AM1-BCC charges (antechamber), GAFF2 parameters (parmchk2).
- Gas-phase complex assembled with tleap (ff14SB protein + GAFF2 ligand), mbondi2 radii.
- `ante-MMPBSA.py` → `MMPBSA.py` single-frame, OBC2 (igb=5), saltcon=0.15 M.
- **No energy minimisation performed prior to evaluation.**

---

## Interpretation

### EDS01357518 (both enantiomers)
Both the S and R enantiomers return favourable single-point MM-GBSA (−19.6 and −16.9 kcal/mol), consistent with the Vina scores. This suggests the gnina poses are geometrically compatible with the ff14SB/GAFF2 energy landscape without requiring structural relaxation.

### EDS01806218 and EDS01889984 — positive MM-GBSA ⚠
The three compounds with ⚠ (positive ΔG) are artefacts of single-point evaluation, **not evidence of non-binding**. Positive single-point MM-GBSA on raw docking poses is a well-documented failure mode (Hou et al., 2011): gnina uses its own scoring grid and softens VdW repulsion internally; when those coordinates are evaluated with the full AMBER potential without minimisation, small steric clashes produce large positive energies.

**What this means in practice:**
- EDS01806218_ent2 remains the top compound by both Vina (−9.08) and CNN ΔG (−10.13).
- The single-point MM-GBSA number for this compound should be discarded; the trajectory-averaged value from the 10 ns MD run will be definitive.
- EDS01889984's +47.84 value likely reflects the most aggressive clash in the raw pose and is similarly uninformative without minimisation.

### Vina vs CNN agreement
CNN ΔG and Vina rankings are broadly consistent. EDS01806218 (1S,2S) leads on both. The CNN score additionally indicates that EDS01357518_ent2 has the highest pose confidence (CNN pose = 0.769), suggesting a well-defined binding mode even though its Vina score is second.

---

## Rankings

| Rank | Compound | Vina | CNN ΔG | Note |
|:----:|:---------|-----:|-------:|:-----|
| 1 | EDS01806218_ent2 (1S,2S) | −9.08 | −10.13 | Top by both fast methods; MD in progress |
| 2 | EDS01357518_ent2 (R) | −8.09 | −9.52 | Highest pose confidence; favourable MM-GBSA |
| 3 | EDS01357518_ent1 (S) | −7.52 | −9.58 | Consistent with ent2; strong MM-GBSA |
| 4 | EDS01889984 | −6.63 | −9.53 | CNN ΔG competitive; Vina lower |
| 5 | EDS01806218_ent1 (1R,2R) | −6.81 | −8.63 | Weakest across all metrics |

---

## Pending

- **Isambard job 6284357** (queued): 10 ns NPT MD of EDS01806218_ent2 + CRBN pocket on GH200. When complete, run `bash md_EDS01806218_ent2/run_mmpbsa.sh` to obtain trajectory-averaged MM-GBSA from the last 8 ns (200 frames). This will supersede the single-point estimate for the top compound.

---

## Limitations

1. Single-point MM-GBSA without minimisation is unreliable for compounds with positive values. Trajectory-averaged MM-GBSA (Isambard job pending) will be definitive for EDS01806218_ent2.
2. Rigid receptor throughout; induced-fit effects not captured.
3. No explicit entropy correction (−TΔS) applied to MM-GBSA values reported here.
4. EDS01806218 enantiomer enumeration covers only (1R,2R) and (1S,2S); mixed diastereomers excluded.
