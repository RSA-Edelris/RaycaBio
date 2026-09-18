# MD Distinction Test: Actives vs Inactives on CDK2-CCNE

**Phase:** MD distinction test — actives vs inactives on CDK2-CCNE  
**Run ID:** max-7c328505dd  
**Cluster job:** Isambard-AI_HPC job 6408780 (submitted 2026-09-08)  
**Status at write-up:** Running (results pending)

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
| Ions | Standard AMBER ion parameters (`amber14sb.ff/ions.itp`) |

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

## 9. Files

| File | Contents |
|------|----------|
| `md_prep/inputs/run_md.sh` | Complete cluster job script |
| `md_prep/inputs/create_ndx.py` | Index file builder (appends custom groups to GROMACS defaults) |
| `md_prep/inputs/{cid}.gro` | Ligand coordinates (GAFF2 + Gasteiger) |
| `md_prep/inputs/{cid}_topol.top` | Complete combined topology for each compound |
| `md_prep/inputs/{em,nvt,npt,md}.mdp` | Simulation parameter files |
| `md_prep/protein.gro` | Protein structure (9234 atoms, chains A+B, HID protonation) |
| `md_results.csv` | Per-replica summary statistics (populated after job completes) |
| `{cid}_rep{N}/rmsd_lig.xvg` | Ligand RMSD timeseries per replica |
| `{cid}_rep{N}/hbond_prot_lig.xvg` | H-bond count timeseries per replica |
| `{cid}_rep{N}/mindist_chains.xvg` | Inter-chain minimum distance per replica |
| `{cid}_rep{N}/sasa_{A,B,AB}.xvg` | SASA timeseries for BSA calculation |
