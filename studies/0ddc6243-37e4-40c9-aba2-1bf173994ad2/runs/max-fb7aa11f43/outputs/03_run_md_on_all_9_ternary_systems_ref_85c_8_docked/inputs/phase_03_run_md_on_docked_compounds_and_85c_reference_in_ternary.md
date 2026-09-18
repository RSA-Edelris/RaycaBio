---
title: "Phase 3: Run MD on docked compounds and 85C reference in ternary complex"
study_id: "0ddc6243-37e4-40c9-aba2-1bf173994ad2"
run_id: "max-b1dc357bbc"
phase_index: 3
phase_id: "3"
phase_goal: "Run MD on all docked compounds + 85C reference to confirm ternary binding"
status: "in progress — LUMI job 22075127 running"
model: "claude-sonnet-4-6"
generator: "manual phase write-up"
---

# Phase 3: Run MD on docked compounds and 85C reference in ternary complex

## Summary

Nine CRBN–GSPT1–ligand ternary systems are being simulated by AMBER CPU MD on
LUMI to assess whether each docked compound maintains the bridging contacts that
define molecular glue activity. The reference system uses the 85C (CC-885) crystal
pose from 5HXB. The eight test systems use the top GNINA CNN-ranked poses from
Phase 2. LUMI job 22075127 was submitted 2026-09-15 and is currently running.

## Objective

For each of the 9 ternary systems (REF_85C + CPD1, CPD4, CPD7, CPD8, CPD9, CPD10,
CPD11, CPD12), determine:
1. Whether the ligand remains in the docked pose (heavy-atom RMSD vs frame 1)
2. Whether the CRBN Trp-cage anchor is maintained (distance to W380 Cα)
3. Whether the GSPT1 neo-interface bridge is maintained (distance to K628 Cα)
4. Whether the CRBN–GSPT1 complex stays assembled (COM distance, chains 196–575 vs 1–195)

## Methods

### System construction

**Receptor:** `receptor_nozn.pdb` — CRBN (chain Z, 380 residues, AMBER res 196–575)
and GSPT1 (chain X, 195 residues, AMBER res 1–195) from 5HXB. HIS353→HIE
(NE2 contacts 85C O4 at 2.72 Å); all other His→HID. ZN removed (seqid 501,
>20 Å from ligand site) to avoid metal-parameter complications in tleap.

**Ligands:** 9 SDF files extracted from Phase 2 GNINA output:
- REF_85C: crystal pose from 5HXB (31 heavy atoms, C₁₈H₁₇ClN₃O₃)
- CPD1–CPD12 (8 compounds): top CNN-ranked GNINA pose per compound

**Parameterisation:**
- Protein: AMBER ff14SB (`source leaprc.protein.ff14SB`)
- Ligand: GAFF2 (`source leaprc.gaff2`), charges by AM1-BCC
  (`antechamber -c bcc -at gaff2 -nc 0`), missing parameters by
  `parmchk2 -s gaff2`
- Water: TIP3P (`source leaprc.water.tip3p`)
- Ions: JC ion parameters (`loadamberparams frcmod.ionsjc_tip3p`)
- Box: truncated octahedron, 12 Å buffer (`solvateOct TIP3PBOX 12.0`)
- Salt: system neutralised with Na⁺, then 40 Na⁺ + 40 Cl⁻ added (~150 mM)

**AMBER topology residue indices:**
```
GSPT1 chain X  AMBER res   1– 195  (seqids 440–634)
CRBN  chain Z  AMBER res 196– 575  (seqids  48–500)
LIG            AMBER res 576       (appended by tleap)
W380 Trp-cage  AMBER res 518
K628 neo-iface AMBER res 189
```

### Simulation protocol

All runs: AMBER 24 CPU (`module load Local-CSC; module load amber/24-cpu`),
`pmemd.MPI` with Cray MPICH, 13 MPI ranks per system via
`srun --ntasks=13 --overcommit`.

| Stage | Length | Thermostat | Barostat | Restraints | dt |
|:------|:-------|:-----------|:---------|:-----------|:---|
| Minimisation | 5 000 steps (2 500 steepest + 2 500 conjugate) | — | — | 10 kcal/mol/Ų on non-H heavy atoms | — |
| NVT heating | 500 ps | Langevin γ=2 ps⁻¹ (ntt=3), 0→300 K | off | 5 kcal/mol/Ų on non-H heavy atoms | 2 fs |
| NPT equil | 1 ns | Langevin γ=2 ps⁻¹, 300 K | Berendsen taup=1 ps, 1 bar | 2 kcal/mol/Ų on non-H heavy atoms | 2 fs |
| Production | 3 × 5 ns | Langevin γ=2 ps⁻¹, 300 K | Berendsen taup=2 ps, 1 bar | none | 2 fs |

All three production replicas start from the same NPT restart file (`npt.rst`)
with different random velocity seeds (ig=-1, wall-clock-seeded). SHAKE
applied to all bonds involving hydrogen (ntc=2, ntf=2). PME for long-range
electrostatics, cut=10 Å. Coordinates saved every 25 000 steps (50 ps) in
NetCDF format.

### Analysis (cpptraj)

Trajectories are imaged with `autoimage :LIG anchor` before analysis.

| Observable | cpptraj command | Threshold for "stable" |
|:-----------|:----------------|:-----------------------|
| Ligand RMSD | `rmsd :LIG & !@H= first` | mean < 4.0 Å |
| CRBN anchor | `distance :LIG :518@CA` (W380) | mean < 10.0 Å |
| GSPT1 bridge | `distance :LIG :189@CA` (K628) | mean < 12.0 Å |
| PPI association | `distance :196-575 :1-195` (COM) | mean < 55.0 Å |
| CRBN contacts | `nativecontacts :LIG :196-575 distance 4.5` | — |
| GSPT1 contacts | `nativecontacts :LIG :1-195 distance 4.5` | — |

**Glue classification rule** (applied to mean of last 50% of combined trajectories):
- `STABLE_GLUE`: RMSD < 4.0 Å AND CRBN_anchor < 10 Å AND GSPT1_bridge < 12 Å AND PPI_COM < 55 Å
- `CRBN_only`: RMSD < 4.0 Å AND CRBN_anchor < 10 Å (no GSPT1 bridge)
- `unstable`: any threshold exceeded
- `NO_DATA`: topology build or MD failed

## Cluster and compute details

| Item | Value |
|:-----|:------|
| Cluster | LUMI (lumi.csc.fi), project_462001483 |
| Job ID | 22075127 |
| Partition | standard (CPU-only, 128 cores AMD EPYC) |
| Requested | 128 CPUs, 0 GPUs, 2880 min wall time |
| Submitted | 2026-09-15 |
| AMBER module | amber/24-cpu (version 24, compiled 2026-02-03 per probe log) |
| MPI | Cray MPICH 8.1.32 |
| Expected wall time | 36–42 h (est. ~11 ns/day per system at 13 CPUs, ~75 k atoms) |

**Note on GPU:** Three GPU submission attempts (gpus=1, gpus=8, gpus=8 w/ 128 CPUs)
all rejected by LUMI scheduler ("Requested node configuration is not available").
Root cause confirmed: LUMI's GRES type is `gpu:mi250` but the platform connector
submits generic `gpu:N`. CPU-only AMBER with pmemd.MPI is the operational path
for this study.

## Expected output

On job completion, `$RAYCA_OUT/md_crbn_gspt1/analysis/` will contain:
- `${LIG}_lig_rmsd.dat` — frame-by-frame ligand RMSD (Å)
- `${LIG}_crbn_anchor.dat` — LIG–W380 distance (Å)
- `${LIG}_gspt1_bridge.dat` — LIG–K628 distance (Å)
- `${LIG}_ppi_com.dat` — CRBN–GSPT1 COM distance (Å)
- `${LIG}_crbn_nc.dat` — CRBN native contacts count
- `${LIG}_gspt1_nc.dat` — GSPT1 native contacts count
- `summary.tsv` — per-compound means, SDs, and verdict

The summary table will be appended to `report.md` and this phase report once
the job completes.

## Limitations

1. Three 5 ns replicas (15 ns total) is shorter than the 3×20 ns originally
   specified. This is adequate for classifying gross stability and contact
   persistence but would be insufficient for free energy estimation or
   convergence of slow conformational changes.
2. CPU MD at 13 ranks/system is ~3–4× slower than GPU pmemd.hip; performance
   estimates carry ~40% uncertainty.
3. All three production replicas start from the same equilibrated structure
   (npt.rst). True independence would require separate equilibration runs with
   different initial velocity draws.
4. ZN was removed from the receptor. CRBN's structural zinc (C173/C176/H228/H230)
   is distant from the binding site and its absence should not affect stabiliser
   binding, but this is not validated for this system.

## References

- AMBER 24: Case DA et al., AMBER 2024, University of California, San Francisco.
- ff14SB: Maier JA et al., J Chem Theory Comput 2015, 11, 3696–3713.
- GAFF2: Wang J et al., J Comput Chem 2004, 25, 1157–1174; Bayly CI et al.
- TIP3P: Jorgensen WL et al., J Chem Phys 1983, 79, 926–935.
- JC ion parameters: Joung IS & Cheatham TE, J Phys Chem B 2008, 112, 9020–9041.
- 5HXB: Matyskiela ME et al., Nature 2016, 535, 252–257.
