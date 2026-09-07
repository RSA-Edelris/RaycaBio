## Scope

This report covers the setup work that preceded the ABFE production runs for EDS01806218_ent1, EDS01806218_ent2, and EDS01889984 bound to CRBN. The inputs were equilibrated MD trajectories for each complex; the outputs were GROMACS-ready topologies with Boresch restraints and all 102 FEP MDP files.

---

## Input trajectories

| Compound | Structure | Trajectory | Frames used for anchor selection |
|---|---|---|---|
| EDS01806218_ent1 | `md_EDS01806218_ent1/complex.gro` | `npt_prod_EDS01806218_ent1.xtc` | frames 500–1000 (last ~5 ns) |
| EDS01806218_ent2 | `md_EDS01806218_ent2/complex.gro` | `npt_prod.xtc` | frames 500–1000 |
| EDS01889984 | `md_EDS01889984/complex.gro` | `npt_prod.6304913.xtc` | frames 500–1000 |

Trajectories were aligned on backbone Cα before RMSF analysis (`126_compounds_items.py`).

---

## Boresch anchor selection protocol

Scripts: `source/124_compounds_items.py` → `source/125_compounds_items.py` → `source/126_compounds_items.py` (iterative refinement of the selection logic).

**Receptor atoms (r1, r2, r3):** Protein Cα atoms within 12 Å of the ligand centroid (last frame), ranked by RMSF over the last 5 ns. The three lowest-RMSF atoms that satisfy pairwise geometry constraints (r2–r1–l1 angle 20°–160°) were chosen.

**Ligand atoms (l1, l2, l3):** Ligand heavy atoms ranked by RMSF on the aligned trajectory; the three lowest-RMSF atoms with satisfactory geometry (no collinear triples) were chosen.

**Equilibrium Boresch values** (r₀, θ_A, θ_B, φ_A, φ_B, φ_C) were measured from the final trajectory frame.

**Analytical restraint-release correction** was computed from the full Boresch formula at 300 K, standard-state V₀ = 1.661 nm³ (1 M), using k_r = 4184 kJ mol⁻¹ nm⁻², k_θ = 41.84 kJ mol⁻¹ rad⁻²:

| Compound | r₀ (nm) | ΔG°_restr (kcal/mol) |
|---|---|---|
| EDS01806218_ent1 | 0.8406 | +7.33 |
| EDS01806218_ent2 | 0.8128 | +7.36 |
| EDS01889984 | 0.7066 | +7.89 |

---

## Topology preparation

For each compound:

1. **AMBER → GROMACS conversion** (`acpype` / `parmed`): AMBER prmtop/inpcrd → GROMACS `.gro` / `.top`. Intermediate AMBER files retained at `md_{NAME}/abfe_solv/lig_solv.inpcrd`, `lig_solv.prmtop`.

2. **Boresch restraint block** added to `[ intermolecular_interactions ]` in each complex topology. Uses:
   - Bond ftype **6** (harmonic restraint; ftype 1 was tried first but rejected by GROMACS 2026.1 as a "chemically bonding interaction")
   - 1 distance + 2 angles (ftype 1) + 3 dihedrals (ftype 2)
   - k = 4184 kJ mol⁻¹ nm⁻² (distance) / 41.84 kJ mol⁻¹ rad⁻² (angles/dihedrals), same in both λ-states A and B

3. **Ligand-in-water boxes** built with tLEAP for the solvent decoupling leg: `md_{NAME}/abfe_solv/lig_solv.gro` + `.top`.

4. **GROMACS index files** (`{NAME}_index.ndx`) defining `Protein_LIG` and `Water_and_ions` groups for the complex-leg thermostat coupling.

---

## MDP files

102 FEP MDP files generated (3 compounds × 2 legs × 17 windows = `{NAME}_{cplx|solv}_win{00–16}.mdp`).

Lambda schedule (17 windows, COUL then VDW):
```
COUL_LAMBDAS = [0, 0.25, 0.50, 0.75, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
VDW_LAMBDAS  = [0, 0,    0,    0,    0, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.85,0.9,0.95,1]
```

Key MDP settings after iterative fixes:

| Parameter | Value | Reason |
|---|---|---|
| `couple-moltype` | `LIG` | identifies the decoupled species |
| `couple-lambda0` | `vdw-q` | fully coupled at λ=0 |
| `couple-lambda1` | `none` | fully decoupled at λ=1 |
| `couple-intramol` | `yes` | prevents GROMACS 2026.1 exclusionchecker crash for flexible ligands (intramolecular terms cancel between legs) |
| `rcoulomb` / `rvdw` | 1.2 nm | raised from 1.0 nm to keep auto-adjusted rlist below the pair-list cutoff |
| `sc-alpha` | 0.5 | softcore for VDW decoupling |
| `calc-lambda-neighbors` | -1 | full overlap matrix for MBAR |
| `nstdhdl` | 100 | dHdL output every 100 steps |
| Production steps | 750,000 × 2 fs = 1.5 ns | per window |

---

## Outputs staged for cluster jobs

All files copied to session root with compound-name prefix for flat staging (avoids `$RAYCA_INPUTS` subdirectory issue):

```
{NAME}_abfe_start.gro          equilibrated complex coordinates
{NAME}_complex_abfe.top        topology with Boresch restraints (ftype 6 bond)
{NAME}_index.ndx               Protein_LIG / Water_and_ions index
{NAME}_lig_solv.gro            ligand-in-water box
{NAME}_lig_solv.top            ligand-in-water topology
{NAME}_cplx_win{00-16}.mdp     17 complex-leg FEP MDPs
{NAME}_solv_win{00-16}.mdp     17 solvent-leg FEP MDPs
```
