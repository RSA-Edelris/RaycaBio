## Objective

Parameterise all 9 ligands (REF_85C + CPD1/4/7/8/9/10/11/12) with GAFF2/AM1-BCC charges locally, build solvated AMBER systems with tleap, package topologies, and submit a pmemd.MPI production job to LUMI.

## Why local parameterisation

LUMI job 22074955 and 22075097 (earlier probe jobs) confirmed that `sqm` — the semi-empirical QM engine used by antechamber for AM1-BCC charge fitting — fails on LUMI compute nodes. `pmemd.MPI` (v24.0) and `cpptraj` are both present via `module load Local-CSC; module load amber/24-cpu`. The fix: generate all GAFF2 parameters locally, stage pre-built `system.prmtop` + `system.inpcrd` pairs to LUMI, and run only pmemd.MPI there.

## Receptor

`md/receptor_nozn.pdb` — CRBN (chain Z, 380 residues, seqids 48–500) + GSPT1 (chain X, 195 residues, seqids 440–634), ZN (seqid 501) removed. 575 residues total; AMBER residue 576 = ligand.

**Key AMBER residue mapping:**
| Biological label | AMBER residue |
|---|---|
| GSPT1 K628 (neo-interface) | 189 |
| CRBN W380 (anchor) | 518 |
| Ligand (LIG) | 576 |
| CRBN chain | 196–575 |
| GSPT1 chain | 1–195 |

## Ligand parameterisation

### Antechamber (GAFF2 + AM1-BCC)

Input: top-ranked GNINA docking pose per compound (`md/ligands/{LIG}_top.sdf`).

Three compounds (CPD4, CPD7, CPD10) had sufficient explicit H in the original SDF and were run directly.  
Six compounds (REF_85C, CPD1, CPD8, CPD9, CPD11, CPD12) had missing explicit H — `sqm` raised "odd electron count". Fix: `AllChem.AddHs(mol_noH, addCoords=True)` preserves heavy-atom docked-pose coordinates while adding only the H atoms, then antechamber re-ran successfully.

CPD1 completed QM but did not write the mol2 output; recovered from `ANTECHAMBER_AM1BCC.AC` using:
```
antechamber -i ANTECHAMBER_AM1BCC.AC -fi ac -o CPD1.mol2 -fo mol2 -at gaff2 -rn LIG -dr no
```

### Coordinate fix

antechamber may regenerate coordinates internally. After parameterisation all nine `{LIG}_fixed.mol2` files had their XYZ block replaced with the original docked-pose coordinates, preserving GAFF2 atom types and BCC charges.

- If mol2 atom count == original SDF atom count: use original SDF coordinates directly.
- If mol2 atom count > original SDF atom count (H added): use `AddHs(addCoords=True)` coordinates.

### parmchk2

```
parmchk2 -i {LIG}_fixed.mol2 -f mol2 -o {LIG}.frcmod -s gaff2 -a Y
```

`-a Y` ("include all atoms") was required for CPD4 and CPD7 to generate all missing torsion terms (e.g. `c1-ce-n-c`, `c1-c-ns-hn`). Without `-a Y`, tleap reported 11 "No torsion terms" errors for CPD4.

### frcmod sizes (bytes)

| Ligand | frcmod |
|---|---|
| REF_85C | 9,540 |
| CPD1 | 3,624 |
| CPD4 | 8,452 (v2 with `-a Y`) |
| CPD7 | 7,056 (regenerated with `-a Y`) |
| CPD8 | 4,560 |
| CPD9 | 4,624 |
| CPD10 | 3,621 |
| CPD11 | 4,866 |
| CPD12 | 4,745 |

## tleap system building

Force fields: ff14SB (protein), GAFF2 (ligand), TIP3P (solvent), ionsjc_tip3p (Na⁺/Cl⁻).  
Box: truncated octahedron, 12 Å buffer.  
Ions: neutralise then add 50 Na⁺ + 50 Cl⁻ (≈ 150 mM NaCl).

All 9 systems built successfully:

| System | Atoms | prmtop (KB) |
|---|---|---|
| REF_85C | 127,261 | 22,304 |
| CPD1 | 127,257 | 22,302 |
| CPD4 | 127,043 | 22,256 |
| CPD7 | 127,204 | 22,281 |
| CPD8 | 127,241 | 22,296 |
| CPD9 | 127,242 | 22,299 |
| CPD10 | 127,213 | 22,282 |
| CPD11 | 127,237 | 22,302 |
| CPD12 | 127,248 | 22,304 |

## AMBER input protocol

Staged in `systems_stage.tar.gz` (29.9 MB) alongside topologies:

| Stage | Input | Duration | Notes |
|---|---|---|---|
| Minimisation | min.in | 10,000 steps (5 k SD + 5 k CG) | backbone restrained 5 kcal/mol/Å² |
| Heating | heat.in | 100 ps NVT, 0→300 K | backbone restrained 5 kcal/mol/Å² |
| Equilibration | equil.in | 200 ps NPT 300 K/1 atm | backbone restrained 1 kcal/mol/Å² |
| Production | prod.in | 1 ns NPT 300 K/1 atm | unrestrained; save every 5 ps |

PME cut-off 10 Å; SHAKE on H bonds (ntc=2, ntf=2); dt = 2 fs; Langevin thermostat γ = 2 ps⁻¹; Monte Carlo barostat.

## LUMI job submission

Job **22076147** — 128 CPUs (1 node, AMD EPYC 7763), `standard` partition, 2880 min (48 h) walltime.

Script runs all 9 systems as background tasks; `srun -n 64` (no `--exclusive`) causes SLURM to schedule 2 tasks of 64 cores concurrently on the 128-core node. Estimated wall-clock: ~25 h for all 9 systems. After MD completes, cpptraj runs inline to extract:

- `rmsd_lig.dat` — ligand RMSD vs docked pose (after protein backbone superposition)
- `rmsd_backbone.dat` — protein backbone RMSD
- `dist_W380_LIG.dat` — CRBN W380 CA (res 518) → ligand COM distance
- `dist_K628_LIG.dat` — GSPT1 K628 NZ (res 189) → ligand COM distance
- `dist_PPI.dat` — CRBN–GSPT1 COM distance

## Key files

| Path | Description |
|---|---|
| `md/receptor_nozn.pdb` | Receptor (CRBN + GSPT1, no ZN) |
| `md/param/{LIG}/{LIG}_fixed.mol2` | GAFF2 types + BCC charges + docked coordinates |
| `md/param/{LIG}/{LIG}.frcmod` | Missing GAFF2 parameters |
| `md/systems/{LIG}/system.prmtop` | Solvated AMBER topology |
| `md/systems/{LIG}/system.inpcrd` | Initial coordinates |
| `md/systems_stage.tar.gz` | Tarball staged to LUMI (29.9 MB) |
| `md/amber_inputs/` | min.in, heat.in, equil.in, prod.in |

## Container image

Docking (GNINA) was performed using the `gnina` tool dispatched via the platform's containerised tool registry. The top-ranked pose per compound was used as the ligand input for parameterisation in this phase.

## Lessons learned

1. `parmchk2 -a Y` is required when ligands contain sp-hybridised carbons (c1) attached to amide or conjugated-amine nitrogens — the default run silently omits torsion parameters that tleap then rejects.
2. `AllChem.AddHs(mol, addCoords=True)` is the correct method to add H while preserving docked heavy-atom coordinates; `EmbedMolecule(ETKDGv3)` discards the pose.
3. tleap accepts the tarball-extracted mol2/frcmod/pdb paths as absolute paths in the `tleap.in` script.
4. LUMI `standard` partition clamps CPU requests at 128 (1 node); the platform does not pass multi-node allocations for this account tier.
