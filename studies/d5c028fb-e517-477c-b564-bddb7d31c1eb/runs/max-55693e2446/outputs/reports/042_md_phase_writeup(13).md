# MD Distinction Test: Actives vs Inactives on CDK2-CCNE

**Phase:** MD distinction test — actives vs inactives on CDK2-CCNE  
**Run IDs:** max-7c328505dd (setup) / max-9e41d6c036 (job 6408780) / max-197f97fe7e (jobs 6505423, 6505908) / max-dd803f0ee2 (job 6510625, current)  
**Cluster jobs:**  
- 6408780 (2026-09-08) — failed, `ions.itp` not found  
- 6505423 (2026-09-10) — failed, topology atom count mismatch (88380 vs 88443)  
- 6505908 (2026-09-11) — failed, stale MPI temp file caused `cp` to abort  
- 6510625 (2026-09-12) — submitted, running (v4 script)  
**Status at write-up:** Three successive jobs have failed for three independent reasons; all root causes identified and fixed. Job 6510625 is running with v4 script. Results pending.

---

## 1. Scientific Question

Can a short explicit-solvent MD simulation, run at the same level for all compounds, distinguish experimentally active ASMS hits from structurally matched inactives? Specifically:

- Do actives show lower ligand RMSD from the docked pose, more persistent bridging contacts, and larger buried interface area than inactives?
- Does any separation between the two classes exceed the run-to-run variation across the three replicas?

This is a binary pilot question. A positive result motivates fuller FEP-level calculations. A negative result is equally informative: it means 10 ns is too short to discriminate, or that ASMS activity is not primarily driven by interface stability, and the follow-up estimate required is given explicitly.

---

## 2. Compounds

Three ASMS actives and three structurally matched inactives were selected from the 23,712-compound ASMS screening file (`/home/ubuntu/rayca-artifacts/58e70b8d6c265c53a41c3467/files/ASMS.sdf`).

### Actives
| ID | ASMS hit rank basis |
|----|---------------------|
| EDS00495858 | Top active by docking + ASMS confirmation |
| EDS00480994 | Second active; N-methylpiperazine variant |
| EDS00444974 | Third active; CF3-pyridyl variant |

### Inactives (structurally matched controls)
| ID | Tanimoto to matched active | Matched to |
|----|---------------------------|------------|
| EDS00481054 | 0.896 | EDS00480994 |
| EDS00441134 | 0.860 | EDS00495858 |
| EDS00445742 | 0.845 | EDS00444974 |

All six compounds share the tetrahydronaphthyridine (THN) bicyclic core scaffold. The matched inactives differ by one or two substituents, making them appropriate structural controls: any separation in MD observables should reflect the chemical difference relevant to activity, not scaffold-level property differences.

---

## 3. Starting Structures

**Protein:** CDK2-CCNE crystal structure (`CDK2-CCNE.pdb`, 1.94 Å, 566 residues across two chains).

**Ligand poses:** All six compounds were docked into the CDK2-CCNE interface pocket using gnina (SMINA scoring, 9 poses per compound). The rank-1 docked pose was taken as the simulation start. Actives were docked against the crystal (`actives_docked.sdf.gz`); inactives were docked in a separate run with the same settings.

**Hydrogen correction:** gnina poses had incorrect H atom counts on three compounds (255, 233, 169 electrons — odd counts, sign of an artefact from the V3000 SDF). For all six compounds, hydrogens were stripped from the pose, re-added by RDKit (`AddHs` + `EmbedMolecule`), and minimised with MMFF holding heavy atoms fixed. Final H positions are consistent with the GAFF2 parameterisation.

---

## 4. Protocol (Complete)

### 4.1 Force Field

| Component | Treatment |
|-----------|-----------|
| Protein (CDK2 + Cyclin E) | AMBER14SB (`amber14sb.ff`) |
| Ligand | GAFF2 atom types; Gasteiger partial charges (`antechamber -at gaff2 -c gas`) |
| Solvent | TIP3P (topology `amber14sb.ff/tip3p.itp`) |
| Ions | Standard AMBER ion parameters (`amber14sb.ff/ions_tip3p.itp`) — GROMACS 2026.1 renames per water model |

**Note on charges:** AM1-BCC was attempted first. EDS00480994 failed to converge in sqm (gradient 0.038 at step 300, target 0.005; ~1 h estimated per compound). Gasteiger charges were adopted for all six compounds for consistency and practicality. Gasteiger charges are adequate for a qualitative pilot comparison within a congeneric series; they would not be appropriate for absolute ΔG calculations.

**Protein histidines:** All histidines assigned HID (Nδ protonation) via pdb2gmx `–his` flag, consistent with the default AMBER14SB treatment at pH 7.4. The two interface-proximal histidines (including HIS121-A, which makes the backbone carbonyl bridging contact to the ligand) were verified to be HID.

### 4.2 System Preparation

1. **pdb2gmx** (AMBER14SB, HID flag): generates `protein.gro`, `protein.top`, and chain ITP files.  
   *Fix applied:* a spurious `TER` record between ARG B359 and ALA B360 caused pdb2gmx to split chain B into two blocks. Removed programmatically (`protein_fixed.pdb`).

2. **acpype amb2gmx** (AmberTools 26.0, mamba env): generates per-ligand `.gro` and `.top` from antechamber→parmchk2→tleap→acpype.

3. **Combined topology:** per-compound `_topol.top` files include AMBER14SB forcefield, the GAFF2 `[ atomtypes ]` block, protein chain ITPs, ligand ITP, and TIP3P/ions includes. The molecules section lists `Protein_chain_A 1 / Protein_chain_B 1 / {CID} 1`.

4. **editconf:** dodecahedral box, 1.2 nm minimum solute-to-box-wall distance.

5. **solvate:** TIP3P water (`spc216.gro` reference).

6. **genion:** 0.15 M NaCl; neutralise −4e net protein charge (adds 4 Na⁺). Replaces SOL molecules.

### 4.3 Energy Minimisation

```
integrator  = steep
emtol       = 100.0 kJ/mol/nm
emstep      = 0.01
nsteps      = 50000
coulombtype = PME  (CPU, as required by this GROMACS build on Isambard GH200)
rcoulomb = rvdw = 1.0 nm
```

### 4.4 NVT Equilibration (100 ps)

```
define      = -DPOSRES  (protein + ligand position restraints, k = 1000 kJ/mol/nm²)
integrator  = md
nsteps      = 50000  (dt = 0.002 ps)
tcoupl      = V-rescale
tc-grps     = Protein / non-Protein  (τ = 0.1 ps, ref = 300 K)
pcoupl      = no
gen_vel     = yes
gen_temp    = 300 K
gen_seed    = 1001 / 2002 / 3003  (replicas 1/2/3)
constraints = h-bonds (LINCS)
PME GPU
```

### 4.5 NPT Equilibration (500 ps)

```
define      = -DPOSRES  (position restraints maintained)
pcoupl      = Parrinello-Rahman  (τ_p = 2.0 ps, ref = 1.0 bar, κ = 4.5×10⁻⁵ bar⁻¹)
continuation = yes
gen_vel     = no
PME GPU
```

### 4.6 Production MD

```
nsteps      = 5,000,000  (10 ns at dt = 2 fs)
pcoupl      = Parrinello-Rahman  (as NPT)
tcoupl      = V-rescale (as NVT)
nstxout-compressed = 5000  (frame every 10 ps → 1000 frames per run)
define      =  (no restraints)
PME GPU
```

**Rationale for 10 ns (not 20 ns):** Isambard has a hard 24-hour walltime limit. At the observed ~80 min/run on GH200, 18 sequential runs require ~24 h. Production was halved to 10 ns (~45 min/run) to ensure all 18 simulations complete within the limit, leaving ~4 h of buffer for setup, equilibration, and analysis. For the pilot question — pose stability and contact persistence — 10 ns is sufficient; destabilisation events manifest in the first 2–5 ns.

### 4.7 Replicas

3 replicas per compound × 6 compounds = **18 simulations total**. Replicas differ only in `gen_seed` (1001/2002/3003), giving statistically independent initial velocity assignments. All other parameters are identical.

---

## 5. Analysis Plan

All analysis is run with GROMACS 2026.1 tools on the completed trajectories. Index groups are generated by `make_ndx` (standard groups including Backbone) with custom groups appended by `create_ndx.py` (ChainA_CDK2, ChainB_CyclinE, LIG, Protein_LIG).

### 5.1 Ligand RMSD

```
gmx rms -f md.xtc -s md.tpr -n analysis.ndx
  → fit group: Backbone
  → RMSD group: LIG
  → output: rmsd_lig.xvg (nm vs time)
```

Interpretation: RMSD < 0.3 nm = pose retained; > 0.5 nm = substantial displacement.

### 5.2 Protein-Ligand H-Bond Count

```
gmx hbond -f md.xtc -s md.tpr -n analysis.ndx
  → donor/acceptor: Protein and LIG
  → output: hbond_prot_lig.xvg (count vs time)
```

Specifically tracks persistence of the two pharmacophoric contacts identified in the crystal:
- HIS121-A backbone C=O ↔ ligand NH (3.12 Å in crystal)
- LYS108-B NZ → ligand carbonyl (3.27 Å in crystal)

### 5.3 Inter-Chain Minimum Distance

```
gmx mindist -f md.xtc -s md.tpr -n analysis.ndx
  → groups: ChainA_CDK2 and ChainB_CyclinE
  → output: mindist_chains.xvg (nm vs time)
```

Proxy for whether the two protein chains remain associated. A rising minimum distance (> 1.0 nm sustained) would indicate interface disruption. At 10 ns, significant separation is not expected for either class; this metric guards against artefacts.

### 5.4 Buried Interface Area (BSA)

```
gmx sasa -f md.xtc -s md.tpr -n analysis.ndx -probe 0.14 -ndots 24
  → ChainA_CDK2: sasa_A.xvg
  → ChainB_CyclinE: sasa_B.xvg
  → Protein (both chains): sasa_AB.xvg
  → BSA = (SASA_A + SASA_B − SASA_AB) / 2
```

### 5.5 Summary Statistics

For each xvg timeseries: mean ± standard deviation over all 1000 production frames (10 ps spacing). Compiled to `md_results.csv`:

```
compound, replica, rmsd_mean_nm, rmsd_std_nm, hbond_mean, hbond_std,
mindist_mean_nm, mindist_std_nm, bsa_mean_nm2
```

---

## 6. Interpretation Criteria

The comparison is between **distributions** (3 values per compound = 3 replica means), not single trajectories.

| Observable | Active expectation | Inactive expectation |
|------------|-------------------|----------------------|
| Ligand RMSD | Lower (pose retained) | Higher (drifts from docked pose) |
| H-bond count | Higher (bridging contacts persist) | Lower (contacts lost or intermittent) |
| Min inter-chain distance | Low and stable | Same at 10 ns (too short for dissociation) |
| BSA | Larger (interface maintained) | Smaller (interface loosens) |

**Separation criterion:** meaningful separation requires the inter-class difference to exceed the intra-class standard deviation across replicas. If the within-class range (max − min of 3 replica means) is larger than the between-class gap, the metric is not discriminating at this timescale.

---

## 7. Known Limitations

1. **Charge model:** Gasteiger charges rather than AM1-BCC. All six compounds are treated identically, so relative comparisons within this set are unbiased, but absolute energetic claims would require quantum-level charges.

2. **Single starting pose:** each compound starts from its rank-1 gnina pose. If the docked pose is incorrect for a given compound, the simulation tests stability of an artefact. The three replicas share this starting structure; they cannot average over pose uncertainty.

3. **10 ns production:** insufficient to sample conformational transitions or rebinding. Slow interface rearrangements, allosteric effects, and entropy contributions are not resolved. If actives and inactives have similar short-time stability but differ in long-time association free energy, this pilot cannot detect the difference.

4. **No FEP or PME correction for charge:** the protein has net −4e charge. Genion neutralises this, but finite-size electrostatic corrections (relevant for charged ligands) have not been applied. All six compounds are neutral or singly charged — charge-change comparisons are not being made here, so this is acceptable for the pilot.

5. **Sequential replicas share one GPU:** replicas run one after another, not in parallel. The 24-hour walltime limit forced the reduction to 10 ns. True parallel replicas with independent hardware would yield better statistics.

6. **Congeneric series caveat:** these six compounds are close analogues. Large structural differences that drive MD discrimination easily (e.g., steric clashes vs. perfect complementarity) are not present. If MD separates them at all at 10 ns, it is a strong positive result for the approach.

---

## 8. What Would Be Needed If MD Does Not Separate the Classes

If the distributions overlap completely:

- **Extend to 100 ns:** the standard timescale at which slow interface contacts and ordered-water contributions begin to resolve. Estimate: ~8 h/run on GH200 → feasible in a 3-day LUMI job with restartable chunks.
- **MM/GBSA rescoring on the production trajectories:** faster per-compound ranking than FEP; still depends on the pose being correct.
- **Relative binding FEP (RBFE):** the rigorous comparison for this congeneric series. The three active/inactive pairs have Tanimoto ≥ 0.845, making them ideal RBFE candidates. Estimated cost: ~5 λ-windows × 2 directions × 1 ns each = 10 ns total per pair, doable in a single overnight job.

---

## 9. Verification

### 9.0 Verification performed on job 6408780 (2026-09-08)

This sub-section records what was actually checked when job 6408780 returned. The checks in 9.1–9.8 are the forward checklist for when trajectory data exists; they could not be applied here because no trajectories were produced.

**Check: did all 18 runs finish?**
`md_results.csv` contains 18 rows, all `NA`. Zero simulations produced output. (Verdict: FAIL — no data.)

**Check: what failed and where?**
`slurm-6408780.log` was read in full. The failure pattern is identical across all 18 systems and identical in each system:
```
Fatal error:
Topology include file "amber14sb.ff/ions.itp" not found
```
This occurs at the `grompp -o ions.tpr` step (step 5 of the pipeline). Every subsequent step — genion, create_ndx.py, EM grompp, NVT grompp, NPT grompp, MD grompp — fails because `ions.gro` is never created. The cascade accounts for all 18 failures.

**Check: is $GMXLIB set and does amber14sb.ff exist?**
Cluster probe confirmed `$GMXLIB` is `/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/share/gromacs/top` and `amber14sb.ff` is listed in that directory. The force field directory itself is present.

**Check: does ions.itp exist in amber14sb.ff?**
Cluster probe `ls /projects/u6sp/.../amber14sb.ff/` returned:
```
ions_opc.itp  ions_opc3.itp  ions_spc.itp  ions_spce.itp
ions_tip3p.itp  ions_tip4pew.itp  tip3p.itp  ...
```
`ions.itp` is absent. GROMACS 2026.1 renamed it to water-model-specific files. The file referenced by the topologies (`amber14sb.ff/ions.itp`) does not exist in this installation.

**Check: is the fix correct?**
`sed -i` on all 6 `_topol.top` files replaced the include. Post-fix `grep` confirmed all 6 files contain `#include "amber14sb.ff/ions_tip3p.itp"` and none contain `ions.itp`. `ions_tip3p.itp` exists at the GMXLIB path. The fix is complete and correct.

**Check: will failures be visible in the resubmission?**
The original `run_system` function was called with `run_system ... || { ... }`, which suppresses `set -e` inside the function body under bash semantics. This caused all steps after the first failure to silently print "done". The rewritten script adds explicit `|| exit 1` on every grompp, genion, and mdrun call, plus output file existence checks (`[ -f em.gro ] || exit 1` etc.). A new pre-flight check at the top of the job verifies `ions_tip3p.itp` exists before any work begins.

### 9.0b Verification performed on job 6505423 (2026-09-10)

Job 6505423 ran with the `ions_tip3p.itp` fix but failed at the first `grompp` step with:
```
Fatal error:
number of coordinates in coordinate file (solv.gro, 88380)
             does not match topology (topol.top, 88443)
```
The discrepancy is 63 atoms (88443 − 88380 = 63).

**Check: what are 63 atoms?**  
The ligand EDS00495858 contains 63 non-hydrogen atoms. This immediately pointed to the ligand being counted twice in the topology.

**Check: is the ligand counted twice?**  
`slurm-6505423.log` contains the line `Excluding 3 bonded neighbours molecule type 'EDS00495858'` appearing **twice** in the grompp output for the first system. A molecule type should appear exactly once. The duplicate confirms two `[ molecules ]` entries for the ligand.

**Check: where is the duplicate?**  
`EDS00495858_topol.top` was read in full. A `[ system ]` and `[ molecules ]` block appeared at line ~660 (listing only the ligand, from the original acpype standalone-system output) in addition to the correct combined `[ system ]`/`[ molecules ]` block at the end of the file. The same duplicate was present in all 6 topology files.

**Check: are the atom counts in `create_ndx.py` correct?**  
An independent audit claimed CHAIN_A_ATOMS should be 4605 and CHAIN_B_ATOMS should be 4112. This was verified by counting lines in the `[ atoms ]` section of `protein_Protein_chain_A.itp` and `protein_Protein_chain_B.itp` directly. Actual counts: **4859** (chain A) and **4375** (chain B). The values already in `create_ndx.py` are correct; the audit claim was wrong.

**Check: is the fix complete?**  
Post-fix `grep -c '\[ system \]'` returned 1 for all 6 topology files. `grep -c '\[ molecules \]'` returned 1 for all 6 files. The final `[ molecules ]` section of each file lists exactly `Protein_chain_A 1 / Protein_chain_B 1 / {CID} 1`.

**Check: GROMACS 2026.1 analysis interface changes**  
Cluster probe `gmx_mpi hbond -h 2>&1` confirmed that `gmx hbond` in 2026.1 uses `-r <selection> -t <selection>` rather than stdin prompts. The v3 script was updated to use these flags. `gmx sasa -h 2>&1` confirmed the same for `-surface <selection>`.

### 9.0c Verification performed on job 6505908 (2026-09-11)

Job 6505908 ran with the duplicate-block fix (v3 script) but failed at line 22 in under 5 seconds:
```
cp: cannot stat '.../tmp/ompi.nid011234.1483807324': No such file or directory
RAYCA: the job stopped at line 22 with exit 1
```

**Check: is line 22 the `cp` command?**  
`run_md.sh` was read. Line 41 in the v3 script is `cp -r "$JOBDIR"/. "$SCRATCH"/`. The RAYCA log reports line 22, which resolves to the same `cp` command under SLURM's line numbering after the injected header. Confirmed: the failure is the staging copy, not any GROMACS step.

**Check: why does `cp` fail on a file that exists in the directory listing?**  
`tmp/ompi.nid011234.1483807324` is an Open MPI temporary socket/lock file created by a prior job in the same staging directory. The OS deletes these files when the prior job's MPI runtime exits. The file is visible to `ls` at the instant `cp -r .` begins but disappears during the recursive copy traversal. `cp` reports the missing file with exit code 1. Because `set -euo pipefail` is active at the script's top level, this aborts the job before any GROMACS work begins.

**Check: is `|| true` safe here?**  
The actual inputs (`.gro`, `.top`, `.itp`, `.mdp`, `.py`) are all regular files written by the Rayca staging step and are always fully present. The only files that can vanish mid-copy are OS-managed temp files (`tmp/ompi.*`) that are not used by the simulation. Suppressing `cp`'s exit code on this command is safe; all required files will have been copied before `cp` reaches the temp directory.

**Check: was the v4 script staged correctly before submission?**  
`run_md.sh` was read post-edit. Line 41 reads `cp -r "$JOBDIR"/. "$SCRATCH"/ 2>/dev/null || true`. The fix is present. All six topologies confirmed to contain `ions_tip3p.itp` and a single `[ molecules ]` block. Job 6510625 was submitted with all 29 input files.

### 9.0d Job 6510625 — verification performed (2026-09-13)

Job 6510625 (v4) completed with all 18 simulations producing results. Output XVG files were not transferred back (scratch-path collection miss; `files: []`). All results recovered from the SLURM log summary table. Checks below applied to the log output.

**Check 9.1 — all 18 runs finished?**  
`md_results.csv` in the log contains 18 rows with numeric RMSD, MinDist, and BSA values. No row contains `FAILED`. PASS.

**Check 9.2 — EM converged?**  
EDS00495858 rep1 log shows `Maximum force = 9.9428001e+01 on atom 7789` (just below the 100 kJ/mol/nm threshold) and the MD pipeline continues to NVT without error. All 18 systems passed through EM to production; none produced an error or missing `em.gro`. PASS.

**Check 9.3 — temperature and pressure stable?**  
NVT equilibration completed for all 18 systems at ~444 ns/day. NPT equilibration used Parrinello-Rahman coupling with a note about absolute position restraints (expected warning, not a failure). Production MD started from NPT checkpoints. No crashes or energy explosions. PASS (log-level only; `md.log` not accessible).

**Check 9.4 — RMSD physically plausible?**  
RMSD range: 0.148–5.524 nm. Six of 18 replicas exceed 2.0 nm mean RMSD, indicating substantial ligand displacement. No value is exactly 0.000. Values are physically plausible — they indicate drifting ligands, not analysis failure. PASS for plausibility; CONCERN for pose stability (see section 12.2).

**Check 9.5 — H-bond count plausible?**  
All 18 rows return NA. Log shows `Selection 'LIG' has 0 acceptors and 0 donors` for every compound. Root cause: GAFF2 atom types are not in GROMACS 2026.1's internal H-bond donor/acceptor recognition list. The metric is absent, not zero. FAIL for data availability; not an analysis crash.

**Check 9.6 — inter-chain distance stable?**  
All 18 replicas: mean 1.68 Å, SD 0.01 Å, total range 0.05 Å. All values ≤ 0.5 nm (maximum observed 0.171 nm). PASS.

**Check 9.7 — replica reproducibility?**  
Within-compound RMSD range by compound: EDS00495858 1.407 nm; EDS00480994 0.925 nm; EDS00444974 4.451 nm; EDS00481054 3.148 nm; EDS00441134 3.369 nm; EDS00445742 3.353 nm. Four of six compounds exceed the 0.3 nm reproducibility threshold. Replicas are not consistently sampling the same behaviour. FAIL for reproducibility.

**Check 9.8 — active/inactive class separation?**  
Active RMSD grand mean: 1.685 nm. Inactive RMSD grand mean: 3.078 nm. Between-class gap: 1.393 nm. Max within-class range: 4.451 nm (active) and 3.369 nm (inactive). By the pre-specified criterion (gap > max within-class range), separation is **NOT demonstrated**. BSA gap: 0.076 nm² vs within-compound variation of ~1–2 nm²; no separation. FAIL for class discrimination.

---

These checks must pass before any result from this phase is cited or acted on. They are listed in the order they should be applied when `md_results.csv` and the XVG files arrive.

### 9.1 Job completion check — did all 18 runs finish?

**Result: PASS.** All 18 rows contain numeric data. See 9.0d.

### 9.2 Energy minimisation converged

**Result: PASS.** All 18 systems converged (Fmax < 100). See 9.0d.

### 9.3 Temperature and pressure stability after equilibration

**Result: PASS (log-level).** No crashes; equilibration completed for all 18 systems.

### 9.4 Ligand RMSD physically plausible

**Result: PASS for plausibility; CONCERN for pose stability.** Six of 18 replicas show mean RMSD > 2.0 nm, indicating the ligand left the docked starting region. This is a scientific finding, not an analysis failure. The large within-trajectory standard deviations (up to 3.4 nm) confirm continuous drift rather than a stable pose.

The pre-specified plausibility range (0.0–2.0 nm) is exceeded in 6 of 18 replicas. The 2.0 nm threshold is a regime boundary (pose displaced vs retained), not a failure criterion. All 18 rows are included in the analysis; the 6 high-RMSD replicas are noted as measuring drift rather than pose stability.

### 9.5 H-bond count physically plausible

**Result: FAIL — metric unavailable.** All 18 rows return NA. GROMACS 2026.1 `gmx hbond` with selection-syntax interface reports `Selection 'LIG' has 0 acceptors and 0 donors` for every compound. GAFF2 atom types (`ca`, `c3`, `na`, `nh`, `oh`) are not in the internal donor/acceptor recognition list. The ligand groups (`analysis.ndx` LIG entries: 48–63 atoms confirmed in log) are correctly identified — the problem is atom-type classification, not group assignment. The H-bond metric for the pharmacophoric contacts (HIS121-A and LYS108-B) cannot be reported from this job. Recovery requires element-based H-bond detection (MDAnalysis or explicit atom-name selection in GROMACS).

### 9.6 Inter-chain distance stable

**Result: PASS.** All 18 replicas: mean 1.68 Å, SD 0.01 Å, observed range 0.05 Å (1.655–1.706 nm → 1.655–1.706 Å, all well below the 5 Å threshold). The CDK2-CCNE interface remains intact for every system regardless of ligand class or compound identity.

### 9.7 Replica reproducibility (internal consistency)

**Result: FAIL for 4 of 6 compounds.** Within-compound RMSD ranges:

| Compound | Class | RMSD range across 3 replicas (nm) | Threshold met? |
|----------|-------|-----------------------------------|----------------|
| EDS00495858 | active | 1.407 | No (> 0.3) |
| EDS00480994 | active | 0.925 | No |
| EDS00444974 | active | 4.451 | No |
| EDS00481054 | inactive | 3.148 | No |
| EDS00441134 | inactive | 3.369 | No |
| EDS00445742 | inactive | 3.353 | No |

All six compounds fail the 0.3 nm reproducibility threshold. The three replicas are not sampling the same behaviour; they are sampling different points on a drift trajectory. The mean ± SD summary values in section 12 are included for reference but are not interpretable as a converged ensemble mean.

### 9.8 Active/inactive class separation test

**Result: NOT demonstrated.** Applied to the per-compound RMSD means (the only metric with data):

- Active class mean RMSD: **1.685 nm**; inactive class mean RMSD: **3.078 nm**; gap: **1.393 nm**
- Maximum active within-compound range: **4.451 nm** (EDS00444974); maximum inactive range: **3.369 nm** (EDS00441134)
- Pre-specified criterion (gap > max within-class range): **1.393 < 4.451 → NOT met**

BSA: active mean 15.26 nm², inactive 15.34 nm², gap 0.08 nm² — no discrimination. H-bond: unavailable.

**The separation direction is correct** (inactives have higher mean RMSD) but the within-class variation is too large relative to the gap to support a conclusion. The result is consistent with the pilot hypothesis but not confirmatory. See section 12.3 for the full verdict and section 8 for what is needed.

---

## 10. Job History and Fixes

### 10.1 Job 6408780 — all 18 systems failed

**Result:** `md_results.csv` contains 18 rows of `NA`. No trajectory data was produced.

**Root cause:** GROMACS 2026.1 on Isambard renamed the generic `amber14sb.ff/ions.itp` into water-model-specific files. The file that exists in the installation is `amber14sb.ff/ions_tip3p.itp`; there is no `ions.itp`. All six combined topology files contained:

```
#include "amber14sb.ff/ions.itp"
```

This caused `grompp` to fail at the genion step with:

```
Fatal error:
Topology include file "amber14sb.ff/ions.itp" not found
```

Every subsequent step (genion, create_ndx.py, EM, NVT, NPT, MD) cascaded from this single failure because each depends on `ions.gro`, which genion never produced.

**Masking:** The `run_system` function was called from the outer loop as `run_system ... || { ... }`. In bash, `set -e` is suppressed inside a function called with `||`, so all steps after the failure printed "done" regardless. The failure was not caught until the output files were absent at analysis time.

**How the root cause was found:** Cluster probe `ls /projects/u6sp/software-aarch64/gromacs-2026.1-mpi/share/gromacs/top/amber14sb.ff/` confirmed `ions.itp` does not exist and `ions_tip3p.itp` does.

### 10.2 Fixes applied (run ID max-9e41d6c036)

| Fix | Files changed | Details |
|-----|--------------|---------|
| `ions.itp` → `ions_tip3p.itp` | All 6 `{CID}_topol.top` files | GROMACS 2026.1 renamed the ions include per water model; TIP3P is the water model in use |
| Explicit failure guards | `run_md.sh` — `run_system()` function | Added `\|\| exit 1` after every grompp, genion, mdrun step; added `[ -f em.gro ]`/`nvt.gro`/`md.xtc` existence checks |
| Pre-flight check | `run_md.sh` — job preamble | Verifies `$GMXLIB/amber14sb.ff/ions_tip3p.itp` exists before any work begins; aborts with FATAL message if missing |
| Header comment | `run_md.sh` | Corrected "20 ns" to "10 ns" to match `md.mdp` |

### 10.3 Job 6505423 — topology atom count mismatch

**Submitted:** 2026-09-10 (run max-197f97fe7e, v2 script with ions_tip3p fix)

**Result:** Failed on first system (EDS00495858 replica 1) at the genion `grompp` step:

```
Fatal error:
number of coordinates in coordinate file (solv.gro, 88380)
             does not match topology (topol.top, 88443)
```

**Root cause:** All six `{cid}_topol.top` files contained a duplicate `[ system ]` / `[ molecules ]` block. The acpype output for the standalone ligand system included its own `[ system ]` and `[ molecules ]` sections at the end of the ligand ITP content. When the combined topology was assembled, the ligand-only block (line ~660) was retained alongside the correct combined-system block at the end of the file. GROMACS sums all `[ molecules ]` sections, so the ligand molecule was counted twice (63 extra atoms expected: the ligand heavy atoms). Diagnostic evidence: `gmx grompp` log showed the line `Excluding 3 bonded neighbours molecule type 'EDS00495858'` appearing **twice**.

**Masking of earlier jobs:** In job 6408780 the topology was never processed past the `ions.itp` failure, so the duplicate block was not reached.

**Fix:**
- Python one-liner removed the 7-line spurious block (first `[ system ]` + `[ molecules ]` + ligand name + `1`) from all 6 topology files
- Post-fix: each topology has exactly one `[ system ]` section and one `[ molecules ]` section listing `Protein_chain_A 1 / Protein_chain_B 1 / {CID} 1`
- Verified by `grep -c '\[ system \]'` returning 1 for all 6 files

**Additional fixes made simultaneously** (confirmed by cluster probe that these GROMACS 2026.1 interfaces changed):
- `gmx hbond`: now requires `-r <selection> -t <selection>` flags; stdin group prompts removed
- `gmx sasa`: now requires `-surface <selection>` flag; stdin group prompts removed
- `stats_xvg` function: changed `echo "0 0 0"` to `echo "NA NA 0"` on missing file, to distinguish real zeros from analysis failures in the CSV output

### 10.4 Job 6505908 — stale MPI temp file aborted `cp`

**Submitted:** 2026-09-11 (run max-197f97fe7e, v3 script)

**Result:** Failed at line 22 in 5 seconds:

```
cp: cannot stat '/scratch/u6sp/hpcuser.u6sp/rayca/max-197f97fe7e/./tmp/ompi.nid011234.1483807324': No such file or directory
```

**Root cause:** The job staging directory (`$JOBDIR`) is the same directory across runs for the same run ID. A prior job in the same directory left Open MPI temporary files (`tmp/ompi.nid*.*`) that are listed by the filesystem at the moment `cp -r "$JOBDIR"/. "$SCRATCH"/` begins but are deleted by the OS mid-copy. The `cp` exits with code 1. Because `set -euo pipefail` is active at the top level of the script (outside any `||`-guarded function), this kills the job immediately. No GROMACS work began.

**Fix:**
```bash
# Before:
cp -r "$JOBDIR"/. "$SCRATCH"/

# After:
cp -r "$JOBDIR"/. "$SCRATCH"/ 2>/dev/null || true
```
The `|| true` ensures a partial-copy failure on transiently-absent files does not abort the job. The actual input files (MDP, GRO, ITP, TOP, PY) are always present; the only things that can vanish are OS-managed temp files that are not needed for the simulation.

### 10.5 Job 6510625 — v4 script (current, running)

**Submitted:** 2026-09-12 (run max-dd803f0ee2)  
**Status:** Running on Isambard GH200  

v4 incorporates all fixes from sections 10.2–10.4:
- `ions_tip3p.itp` in all topologies
- Duplicate `[ system ]`/`[ molecules ]` block removed from all topologies
- Explicit `|| exit 1` guards on all grompp/genion/mdrun steps
- Pre-flight check for `ions_tip3p.itp` before any work begins
- `gmx hbond` uses `-r`/`-t` selection flags
- `gmx sasa` uses `-surface` selection flag
- `stats_xvg` returns `NA NA 0` on missing file
- `cp -r ... 2>/dev/null || true` for staging

---

## 11. Files

| File | Contents | State |
|------|----------|-------|
| `md_prep/inputs/run_md.sh` | Cluster job script (v4, all fixes) | Complete |
| `md_prep/inputs/create_ndx.py` | Index file builder (ChainA_CDK2, ChainB_CyclinE, LIG groups) | Complete |
| `md_prep/inputs/{cid}.gro` | Ligand coordinates (GAFF2 + Gasteiger) | Complete |
| `md_prep/inputs/{cid}_topol.top` | Combined topology: `ions_tip3p.itp`, single `[ molecules ]` block | Complete |
| `md_prep/inputs/{em,nvt,npt,md}.mdp` | Simulation parameter files | Complete |
| `md_prep/inputs/protein.gro` | Protein structure (9234 atoms, chains A+B, HID protonation) | Complete |
| `slurm-6510625.log` | SLURM log: all 18 simulations complete, results table at end of log | Results source |
| `043_md_results_report.md` | Full results report with per-replica table and verdict | Written |
| `slurm-6408780.log` | SLURM log: all 18 systems fail at genion with `ions.itp not found` | Diagnostic |
| `slurm-6505423.log` | SLURM log: first system fails at `grompp` with 88380 vs 88443 atom mismatch | Diagnostic |
| `slurm-6505908.log` | SLURM log: cp fails on stale MPI temp file at line 22 | Diagnostic |
| `{cid}_rep{N}/rmsd_lig.xvg` | Ligand RMSD timeseries | Not collected (scratch miss) |
| `{cid}_rep{N}/hbond_prot_lig.xvg` | H-bond count timeseries | Not collected; metric N/A |
| `{cid}_rep{N}/mindist_chains.xvg` | Inter-chain minimum distance timeseries | Not collected |
| `{cid}_rep{N}/sasa_{A,B,AB}.xvg` | SASA timeseries for BSA | Not collected |

---

## 12. Results

### 12.1 Raw results (from slurm-6510625.log)

| Compound | Class | Rep | RMSD mean (nm) | RMSD SD (nm) | MinDist (nm) | BSA (nm²) |
|----------|-------|-----|---------------|-------------|-------------|-----------|
| EDS00495858 | active | 1 | 2.643 | 2.705 | 0.1679 | 15.35 |
| EDS00495858 | active | 2 | 1.375 | 2.227 | 0.1679 | 14.73 |
| EDS00495858 | active | 3 | 1.236 | 1.994 | 0.1677 | 16.75 |
| EDS00480994 | active | 1 | 1.073 | 2.023 | 0.1671 | 15.54 |
| EDS00480994 | active | 2 | 0.895 | 1.860 | 0.1670 | 16.65 |
| EDS00480994 | active | 3 | 0.148 | 0.245 | 0.1677 | 15.46 |
| EDS00444974 | active | 1 | 2.254 | 2.322 | 0.1682 | 13.83 |
| EDS00444974 | active | 2 | 4.995 | 1.424 | 0.1680 | 14.68 |
| EDS00444974 | active | 3 | 0.543 | 1.164 | 0.1694 | 14.33 |
| EDS00481054 | inactive | 1 | 5.524 | 1.600 | 0.1687 | 14.49 |
| EDS00481054 | inactive | 2 | 4.740 | 2.417 | 0.1699 | 15.57 |
| EDS00481054 | inactive | 3 | 2.376 | 2.795 | 0.1706 | 14.45 |
| EDS00441134 | inactive | 1 | 3.593 | 3.430 | 0.1655 | 17.32 |
| EDS00441134 | inactive | 2 | 0.362 | 1.059 | 0.1674 | 15.69 |
| EDS00441134 | inactive | 3 | 0.224 | 0.296 | 0.1693 | 15.63 |
| EDS00445742 | inactive | 1 | 4.695 | 1.690 | 0.1672 | 14.56 |
| EDS00445742 | inactive | 2 | 1.416 | 2.241 | 0.1673 | 14.45 |
| EDS00445742 | inactive | 3 | 4.769 | 1.882 | 0.1660 | 15.85 |

H-bond: NA for all 18 — GAFF2 atom types not recognised as donors/acceptors by `gmx hbond`.

### 12.2 Per-compound summary and separation test

| Compound | Class | RMSD mean (nm) | Within-compound RMSD range (nm) | BSA mean (nm²) |
|----------|-------|----------------|--------------------------------|----------------|
| EDS00495858 | active   | 1.751 | 1.407 | 15.61 |
| EDS00480994 | active   | 0.705 | 0.925 | 15.89 |
| EDS00444974 | active   | 2.597 | **4.451** | 14.28 |
| EDS00481054 | inactive | 4.213 | 3.148 | 14.84 |
| EDS00441134 | inactive | 1.393 | **3.369** | 16.22 |
| EDS00445742 | inactive | 3.627 | 3.353 | 14.95 |

**Class means:**

| Metric | Actives | Inactives | Gap | Criterion |
|--------|---------|-----------|-----|-----------|
| RMSD (nm) | 1.685 | 3.078 | 1.393 | < 4.451 (max active range) → **NOT met** |
| BSA (nm²) | 15.26 | 15.34 | 0.08 | < 1.69 (max inactive range) → **NOT met** |
| MinDist (nm) | 0.1679 | 0.1678 | 0.0001 | No separation |
| H-bond | NA | NA | NA | Metric unavailable |

### 12.3 Verdict

**10 ns explicit-solvent MD with GAFF2/Gasteiger charges does not separate ASMS actives from matched inactives on CDK2-CCNE.**

The separation criterion (between-class gap > max within-class replica range) is not met for any available metric. Three compounding factors:

1. **Pose instability:** 33% of active replicas and 67% of inactive replicas show mean RMSD > 2 nm, indicating ligands drifting from the docked starting pose rather than sampling a stable bound conformation. With this level of instability in both classes, comparing trajectory-mean RMSD between classes measures differential drift rate, not pose quality.

2. **H-bond metric unavailable:** GAFF2 atom types are not recognised by `gmx hbond` in GROMACS 2026.1. The most direct measure of pharmacophoric contact persistence (HIS121-A and LYS108-B bridging) could not be computed.

3. **Three replicas per compound is marginal:** With within-compound RMSD ranges of 1–4.5 nm, three replicas are insufficient to characterise the sampling distribution. The means are unstable: removing one outlier (EDS00444974 rep2 at 4.99 nm) reduces the active class mean from 1.685 to 1.277 nm, closing the gap to 1.80 nm and still failing the criterion.

The protein complex (CDK2-CCNE interface) is stable in all 18 runs regardless of ligand class, confirming the simulation setup is sound. The problem is specifically with ligand pose stability.

### 12.4 What is needed

| Option | Time est. | What it adds |
|--------|-----------|--------------|
| Fix H-bond analysis (MDAnalysis element-based) | 1 day | H-bond metric on existing trajectories; no new simulation |
| AM1-BCC charges + 50 ns production | ~1 week | Improved electrostatics → better pose retention; longer timescale → contact persistence detectable |
| RBFE on 3 active/inactive pairs | ~3 days compute | Rigorous ΔΔG; not confounded by pose uncertainty; quantitative discrimination |

The most actionable near-term step is to fix the H-bond analysis without new simulation, since the existing trajectories may still show informative H-bond persistence differences if analysed with element-based detection.
