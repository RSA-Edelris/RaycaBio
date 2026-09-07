# Audit: System Preparation — MD + MM-GBSA for 4 CRBN-Pocket Compounds

**Date:** 2026-09-04  
**Phase:** Run MD + MM-GBSA on EDS01357518_ent1, EDS01357518_ent2, EDS01806218_ent1, EDS01889984  

---

## Claims vs Evidence

| Claim | Evidence | Pass? |
|:------|:---------|:-----:|
| GAFF2 parameterisation completed for all 4 ligands | `ligand.mol2` + `ligand.frcmod` present in each `md_*/` directory | PASS |
| Solvated AMBER topology built for all 4 | `complex.prmtop` + `complex.inpcrd` present (~5.3 MB each) | PASS |
| GROMACS topology converted for all 4 | `complex.top` + `complex.gro` present (~29,232–29,248 atoms) | PASS |
| Index groups correct (Protein_LIG = 1\|13, Water_and_ions = 15\|14) | `index.ndx` rebuilt with explicit group arithmetic after LIG confirmed as group 13 | PASS |
| grompp validation passed for all 4 | `em.tpr` produced without fatal errors (`-maxwarn 5`) | PASS |
| ante-MMPBSA.py stripped topologies present | `complex_nowater.prmtop`, `receptor.prmtop`, `ligand.prmtop` in each directory | PASS |
| Cluster jobs submitted to Isambard-AI_HPC | Jobs 6300385 (ent1), 6300401 (ent2), 6300420 (ent1b), 6300478 (EDS01889984) — state=submitted | PASS |

---

## Preparation Fixes Applied

| Issue | Fix |
|:------|:----|
| Initial make_ndx parsing returned `lig_g = None` | Confirmed LIG = group 13 explicitly; rebuilt all 4 index files with `1 \| 13` and `15 \| 14` |
| `cluster="Isambard-AI_HPC"` rejected by `run_on_cluster` | Used cluster id `own:7738ec0ba2c5bbae` instead of display label |

Lessons from EDS01806218_ent2 failure history applied to submission scripts:
- Absolute mpirun path (not srun, not PATH-resolved mpirun)
- `-pme cpu` for EM stage only (incompatible with steepest descent otherwise)
- No `-ntmpi` flag (MPI build, not thread-MPI)

---

## Verification

| Check | Status | Evidence |
|:------|:------:|:---------|
| `complex.prmtop` present for all 4 compounds | PASS | Files ~5.3 MB each in `md_EDS01357518_ent1/`, `md_EDS01357518_ent2/`, `md_EDS01806218_ent1/`, `md_EDS01889984/` |
| `complex.gro` atom counts consistent with solvated system | PASS | 29,232–29,248 atoms per system (protein 142 res + ligand + TIP3P) |
| `complex_nowater.prmtop` (mbondi2 radii) present for all 4 | PASS | ante-MMPBSA.py ran with mask `:WAT,Cl-` and mbondi2 radii |
| `em.tpr` validates without fatal grompp errors | PASS | All 4 `em.tpr` files built with `-maxwarn 5`, no fatal errors |
| Index file has Protein_LIG (group 18) and Water_and_ions (group 19) | PASS | Verified by reading `index.ndx` for each compound after rebuild |
| `mmpbsa.in` files contain no inline comments | PASS | Validated; inline `!` comments removed (known cause of MMPBSA.py parse failure) |
| Cluster submission scripts use proven protocol from job 6294174 | PASS | Absolute mpirun path, `-pme cpu` for EM, `-pme gpu` for MD stages |
| All 4 jobs accepted by Isambard-AI_HPC scheduler | PASS | Job IDs 6300385, 6300401, 6300420, 6300478 — state=submitted |

---

## Pending (awaiting cluster results)

- Job 6300385 (EDS01357518_ent1): trajectory not yet returned
- Job 6300401 (EDS01357518_ent2): trajectory not yet returned
- Job 6300420 (EDS01806218_ent1): trajectory not yet returned
- Job 6300478 (EDS01889984): trajectory not yet returned

MM-GBSA analysis (cpptraj strip → MMPBSA.py with `-cp complex_nowater.prmtop`, `startframe=200, endframe=1000, interval=4`) will run once each trajectory lands. This audit will be updated with ΔG_bind results and a verification of frame counts and energy balance at that time.

---

## Known Limitations

- System preparation only — no MD or binding affinity results in this phase.
- MM-GBSA estimates exclude conformational entropy (−TΔS).
- 10 ns may be insufficient for full sampling convergence on flexible ligands.
- Single replica per compound; no estimate of inter-replica variance.
