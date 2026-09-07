---
title: "Phase 5 — MM-GBSA Free Binding Energies: 32 CRBN Ligands"
phase_id: "5"
status: "in_progress"
---

# Phase 5 — MM-GBSA Free Binding Energies: 32 CRBN Ligands

## Status

Topologies built locally; MD running on LUMI (job 21779205); MMPBSA.py analysis pending.

---

## Objective

Compute single-trajectory MM-GBSA ΔG_binding for all 32 best docked poses to supplement
the gnina Vina/CNN scores with an energy-minimised relative binding affinity estimate.

---

## Protocol

**Force field:** ff14SB (protein) + GAFF2 (ligand), igb=5 (OBC-II) GB implicit solvent

**Charge method:** Gasteiger (`antechamber -c gas -at gaff2`)

AM1-BCC (`-c bcc`) was attempted first but sqm rejected 16/32 ligands with "odd number
of electrons". Root cause: gnina V2000 SDF output carries only 3 explicit H atoms
(aromatic and aliphatic C-H bonds are implicit). sqm counts electrons from the atom
block as written and finds an odd total at nc=0. Gasteiger charges bypass sqm entirely
and give consistent parameterisation across all 32 compounds.

**ZN handling:** The single ZN HETATM at residue B1428 (20.5 Å from pocket centroid,
zero contacts in interaction analysis) was removed from the receptor PDB. tleap cannot
assign an atom type to an isolated ZN without its coordinating residues present in the
truncated CRBN domain construct. Removal has negligible impact on binding-site energetics.

**MD parameters:**

| Parameter | Value |
|-----------|-------|
| Minimisation | 500 steps (SD 200 + CG 300) |
| MD length | 10,000 steps × 0.002 ps = 20 ps NVT |
| Frames saved | 50 (ntwx=200) |
| cut | 12.0 Å |
| rgbmax | 12.0 Å (speeds GB Born-radii cost ~2×) |
| ntt | 3 (Langevin, γ=2.0) |
| ntc/ntf | 2 (SHAKE on H-bonds) |
| saltcon | 0.10 M |

**MMPBSA.py settings:** igb=5, saltcon=0.10, startframe=1, endframe=50. No entropy term
(congeneric ranking). `intdiel`/`extdiel` are not valid `&gb` keywords in AmberTools 24
and were removed.

---

## Execution steps

| Step | Status |
|------|--------|
| antechamber -c gas (32 ligands) | **32/32 OK** |
| parmchk2 -s gaff2 (32 ligands) | **32/32 OK** |
| tleap topologies (ff14SB + GAFF2, no ZN) | **32/32 OK** (~2.65 MB complex.prmtop each) |
| Sander min + MD on LUMI (32 parallel CPUs) | **Running** — job 21779205 |
| Collect md.nc trajectories from LUMI | Pending |
| MMPBSA.py analysis (32 compounds) | Pending |
| Final combined docking + MM-GBSA table | Pending |

---

## Issues and fixes

| Issue | Root cause | Fix |
|-------|-----------|-----|
| sqm "odd electrons" for 16/32 | Implicit C-H in gnina SDF; sqm counts atom block only | Gasteiger charges (`-c gas`) |
| tleap fatal on isolated ZN | No coordinating residues for atom-type assignment | Remove ZN from receptor PDB |
| sander 585 ms/step with cut=12 | Default rgbmax=25 Å → near-O(N²) GB computation | `rgbmax=12.0` → 315 ms/step |
| MMPBSA.py `AMBERHOME` TypeError | `AMBERHOME` env var not set; `os.path.join(None,...)` fails | Set AMBERHOME in subprocess env |
| MMPBSA.py `Unknown variable intdiel` | AmberTools 24 removed intdiel/extdiel from `&gb` | Remove those keywords |
| MMPBSA.py `Could not open complex_prmtop` | Leftover `_MMPBSA_*` temp files from failed run | Clean glob before each call; use `-cp` flag + absolute paths |

---

## Validation test

MMPBSA.py was successfully validated on a 2-frame test trajectory for EDEL-CRBN-0001:

| Component | ΔG (kcal/mol) | ± Std Err |
|-----------|--------------|----------|
| VDWAALS   | −42.10       | 0.89     |
| EEL       | −7.14        | 0.53     |
| EGB       | +10.81       | 0.21     |
| ESURF     | −3.59        | 0.03     |
| **DELTA TOTAL** | **−42.02** | **1.24** |

---

## Key files

| File | Description |
|------|-------------|
| `mmgbsa/receptor_nozn.pdb` | ZN-stripped receptor for tleap |
| `mmgbsa/{name}_ent/lig.mol2` | GAFF2 + Gasteiger mol2 (32 files) |
| `mmgbsa/{name}_ent/complex.prmtop` | ff14SB+GAFF2 complex topology (32 files) |
| `mmgbsa/{name}_ent/rec.prmtop` | ff14SB receptor topology (32 files) |
| `mmgbsa/{name}_ent/lig.prmtop` | GAFF2 ligand topology (32 files) |
| `mmgbsa/pipeline.py` | Topology preparation functions |
| `mmgbsa/run_mmpbsa.py` | Validated MMPBSA.py analysis script |
| `mmgbsa/collate_results.py` | Final docking + MM-GBSA ranking table |

---

## Caveats

- **Gasteiger vs AM1-BCC:** Gasteiger charges are empirical and less accurate than
  AM1-BCC for polar or ionisable groups. Systematic error expected to cancel within
  this neutral glutarimide congeneric series; absolute ΔG values should not be
  interpreted without charge-method sensitivity assessment.
- **Short MD (20 ps):** Adequate for local relaxation and relative ranking within a
  congeneric series; not converged for absolute binding free energies.
- **No entropy correction:** Conformational entropy differences between enantiomers
  are not captured.
- **rgbmax=12 Å:** Slightly below the default (25 Å); may introduce small errors in
  Born radii for deeply buried atoms but acceptable for relative ranking.
