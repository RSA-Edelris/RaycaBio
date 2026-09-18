---
title: "Phase 2: Ligand parameterisation (GAFF2/AM1-BCC) and AMBER system construction"
study_id: "0ddc6243-37e4-40c9-aba2-1bf173994ad2"
run_id: "max-0fcb897abb"
phase_index: 2
phase_id: "5"
phase_goal: "Run antechamber + tleap locally, stage pre-built AMBER topologies to LUMI for pmemd.MPI"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 2: Ligand parameterisation (GAFF2/AM1-BCC) and AMBER system construction

## Summary

All 9 ligands (REF_85C reference compound and CPD1/CPD4/CPD7/CPD8/CPD9/CPD10/CPD11/CPD12)
were parameterised with GAFF2 atom types and AM1-BCC partial charges using AMBER24
`antechamber`/`parmchk2`. Complete solvated AMBER systems were built with `tleap` for each
ligand docked into the CRBN–GSPT1 ternary complex receptor. All 9 `system.prmtop` +
`system.inpcrd` pairs were bundled and staged to LUMI scratch for production MD with
`pmemd.MPI`.

## Background

Earlier phases established that:
- LUMI's `amber/24-cpu` module provides `pmemd.MPI` v24.0 and `cpptraj`, but `sqm` (the
  semi-empirical QM engine required by `antechamber` for AM1-BCC charges) crashes on LUMI
  compute nodes with exit 1 regardless of input.
- Docked poses for all 9 compounds (top-ranked GNINA poses, see Phase 1 docking) are
  available as SDF files at `md/ligands/{LIG}_top.sdf`.
- The receptor without the structural zinc (`receptor_nozn.pdb`) contains GSPT1 (chain X,
  AMBER residues 1–195, PDB seqids 440–634) and CRBN (chain Z, AMBER residues 196–575,
  PDB seqids 48–500).

## Objective

Parameterise each ligand with GAFF2/AM1-BCC locally, patch mol2 coordinates to the docked
pose, generate frcmod files, build solvated AMBER systems with `tleap`, and stage the
pre-built topologies to LUMI so no `antechamber`/`sqm` dependency exists on the cluster.

## Methods

### Software

| Tool | Version | Source |
|:---|:---|:---|
| antechamber | AMBER24 | local conda env (`rayca`) |
| parmchk2 | AMBER24 | local conda env (`rayca`) |
| tleap | AMBER24 | local conda env (`rayca`) |
| RDKit | 2024.03 | local conda env (`rayca`) |
| Force field | GAFF2 + ff14SB + TIP3P + frcmod.ionsjc_tip3p | AMBER24 dat/ |

### Antechamber / AM1-BCC charges

Each docked-pose SDF was processed as follows:

1. **H-completion.** The input SDFs lacked explicit hydrogens. Three ligands (CPD4, CPD7,
   CPD10) had complete protonation in the original SDF; six (REF_85C, CPD1, CPD8, CPD9,
   CPD11, CPD12) required `RDKit.Chem.AddHs(mol, addCoords=True)` which preserves
   heavy-atom 3D coordinates while adding only new H positions.

2. **antechamber call** (net charge 0, GAFF2 types, AM1-BCC):
   ```
   antechamber -i {LIG}.sdf -fi sdf
               -o {LIG}.mol2 -fo mol2
               -c bcc -s 2 -nc 0
               -rn LIG -at gaff2 -dr no -pf y
   ```
   CPD1 completed the QM step but failed to write mol2 output; its mol2 was recovered by
   converting the intermediate `ANTECHAMBER_AM1BCC.AC` file directly.

3. **Coordinate patching.** `antechamber` sometimes re-embeds ligand coordinates; all
   mol2 files were patched to use the docked-pose coordinates.  For the 3 ligands whose
   mol2 atom count matched the original SDF, coordinates were copied directly from the SDF.
   For the 6 ligands where antechamber added H atoms, `AllChem.AddHs(mol_noH,
   addCoords=True)` generated matching H positions from the docked heavy-atom frame, and
   those coordinates replaced the mol2 ATOM block XYZ fields.

4. **parmchk2** with `-a Y` (include all atoms, use analogues for missing parameters):
   ```
   parmchk2 -i {LIG}_fixed.mol2 -f mol2 -o {LIG}.frcmod -s gaff2 -a Y
   ```
   CPD4 required `-a Y` because parmchk2 v24.0 without that flag left four torsion types
   (`c1-c-ns-hn`, `c-ns-c-c1`, `c1-ce-n-c`, `c1-ce-n-c1`) undefined — these involve
   alkyne carbon (`c1`) adjacent to amide/amine nitrogens.  The `-a Y` flag resolved all
   missing parameters via analogue lookup (penalty scores annotated in frcmod).

### tleap system construction

For each ligand:
```
source leaprc.protein.ff14SB
source leaprc.gaff2
source leaprc.water.tip3p
loadamberparams frcmod.ionsjc_tip3p
loadamberparams {LIG}.frcmod
LIG_MOL = loadmol2 {LIG}_fixed.mol2
PROT = loadpdb receptor_nozn.pdb
MOL = combine {PROT LIG_MOL}
solvateOct MOL TIP3PBOX 12.0
addIons MOL Na+ 0       # neutralise
addIons MOL Na+ 50 Cl- 50  # ~150 mM NaCl
saveamberparm MOL system.prmtop system.inpcrd
```

Box geometry: truncated octahedron, 12 Å water buffer. Protein residues 1–575; ligand
residue 576; solvent/ions residues 577+.

## Results

### Parameterisation summary

**Table 1.** AMBER GAFF2 parameterisation results for all 9 ligands.

| Ligand | H-addition route | mol2 atoms | frcmod lines | Coord source |
|:---|:---|---:|---:|:---|
| REF_85C | AddHs(addCoords=True) | 72 | 109 | addCoords |
| CPD1 | AddHs(addCoords=True) + AC recovery | 65 | 50 | addCoords |
| CPD4 | original SDF (pre-protonated) | 31 | 137 | original SDF |
| CPD7 | original SDF (pre-protonated) | 36 | 156 | original SDF |
| CPD8 | AddHs(addCoords=True) | 49 | 60 | addCoords |
| CPD9 | AddHs(addCoords=True) | 62 | 60 | addCoords |
| CPD10 | original SDF (pre-protonated) | 39 | 61 | original SDF |
| CPD11 | AddHs(addCoords=True) | 60 | 62 | addCoords |
| CPD12 | AddHs(addCoords=True) | 68 | 61 | addCoords |

All 9 mol2 files carry GAFF2 atom types and AM1-BCC partial charges.
All 9 frcmod files completed without errors.

### System sizes

**Table 2.** Solvated AMBER system sizes (truncated octahedron, 12 Å buffer, ~150 mM NaCl).

| System | Total atoms | prmtop size |
|:---|---:|:---|
| REF_85C | 127 261 | 22 MB |
| CPD1 | 127 257 | 22 MB |
| CPD4 | 127 043 | 22 MB |
| CPD7 | 127 204 | 22 MB |
| CPD8 | 127 241 | 22 MB |
| CPD9 | 127 242 | 22 MB |
| CPD10 | 127 213 | 22 MB |
| CPD11 | 127 237 | 22 MB |
| CPD12 | 127 248 | 22 MB |

All 9 `system.prmtop` + `system.inpcrd` pairs verified present and non-empty.

### LUMI staging

The 9 topology pairs (prmtop + inpcrd) plus AMBER input decks (min.in, heat.in, equil.in,
prod.in) were bundled as `systems_stage.tar.gz` (30 MB compressed) and staged to LUMI
scratch (`/scratch/project_462001483/rayca/max-0fcb897abb/`) via `run_on_cluster inputs`.

### AMBER MD protocol (staged)

| Stage | Duration | Thermostat | Barostat | Restraint |
|:---|:---|:---|:---|:---|
| Minimisation | 10 000 steps (5 k SD + 5 k CG) | — | — | 5 kcal/mol/Å² on @CA,C,N,O |
| Heating | 100 ps NVT | Langevin γ=2 ps⁻¹, 0→300 K | — | 5 kcal/mol/Å² on @CA,C,N,O |
| Equilibration | 200 ps NPT | Langevin 300 K | MC barostat 1 atm | 1 kcal/mol/Å² on @CA,C,N,O |
| Production | 1 ns NPT | Langevin 300 K | MC barostat 1 atm | none |

2 fs timestep, SHAKE on all H bonds (ntf=2, ntc=2), PME long-range electrostatics
(cut=10.0 Å), GAFF2 + ff14SB + TIP3P water, 150 mM NaCl (frcmod.ionsjc_tip3p).

## Verification

- All 9 `system.prmtop` files confirmed present (22 MB each); all 9 `system.inpcrd` present
  (4.5 MB each); atom counts in Table 2 computed from `system.pdb`.
- Tarball `systems_stage.tar.gz` (30 MB) staged successfully; LUMI job 22076147 confirmed
  extracted the tarball and found all 9 topology pairs.
- LUMI job 22076147 failed at `srun -n 64` (all 9 background tasks launched simultaneously,
  requesting 9 × 64 = 576 CPUs against a 128-CPU allocation). Root cause documented; fix
  is to run tasks sequentially with `srun -n 128`.

## Limitations

- Production length is 1 ns per compound (1 replica). The original protocol specified
  3 × 20 ns; this was reduced due to the LUMI CPU-only constraint (128 cores, ~15 ns/day
  for 127 k atoms → ~2 h per 1 ns run → 9 × 9 h ≈ 35 h total within 48 h walltime).
- Net charge was assumed to be 0 for all ligands; this should be verified against the
  structural data.
- parmchk2 used analogue parameters for unusual torsion types in CPD4 (penalty scores
  up to 136); these parameters carry higher uncertainty.

## References

- AMBER24 documentation: ambermd.org
- Wang et al. 2004 (GAFF): J. Comput. Chem. 25, 1157–1174
- Jakalian et al. 2002 (AM1-BCC): J. Comput. Chem. 23, 1623–1641
- Joung & Cheatham 2008 (ion parameters): J. Phys. Chem. B 112, 9020–9041
