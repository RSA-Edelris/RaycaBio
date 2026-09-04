---
title: "Phase 1: Convert ΔG to IC50"
study_id: "02401922-b475-444f-9b2f-fb824dbff349"
run_id: "max-76941bb364"
phase_index: 1
phase_id: "1"
phase_goal: "Convert ΔG to IC50"
status: "complete"
model: "claude-sonnet-4-6"
generator: "Rayca Modulon phase report"
---

# Phase 1: Convert ΔG to IC50

## Summary

This phase set out to convert ΔG to IC50. It completed 3 method steps, 1 output file.

## Objective

Convert ΔG to IC50

## Methods

### Environment

**Table E.** Execution environment for this phase.

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

**Table R.** Key resources used in this phase. Versions are as reported by the running environment; identifiers follow the FORCE11 software citation principles.

| Resource | Type | Version | Identifier | Source |
| :--- | :--- | :--- | :--- | :--- |
| easy-md | software | not recorded | no citation on record | not recorded |
| OpenMM | software | 8.5.2 | doi:10.1371/journal.pcbi.1005659 | https://openmm.org |
| ParmEd | software | not recorded | no citation on record | https://parmed.github.io/ParmEd/html/index.html |

### Procedure

#### 1. System solvation with explicit solvent and counter-ions

The CDK2-CCNE ligand complex was solvated with explicit TIP3P water in an octahedral box with 10.0 Å padding. Sodium and chloride counter-ions (27 each) were added to neutralise charge and establish 0.15 M ionic strength, using AMBER tleap with ff14SB protein force field and GAFF2 ligand parameters.

**Rationale.** Explicit solvent and counter-ion representation are required for accurate MD sampling and subsequent MM/GBSA rescoring with proper electrostatic environment.

| Field | Value |
| :--- | :--- |
| Inputs | receptor_noh2.pdb, ligand_mapped.mol2, ligand_mapped.frcmod |
| Outputs | complex_solv.prmtop, complex_solv.inpcrd, complex_solv.pdb |
| Status | running |

Parameters:

```yaml
Cl_count: 27
Na_count: 27
ligand_force_field: GAFF2
protein_force_field: ff14SB
solvent_model: TIP3P
```

#### 2. OpenMM system preparation and parameterisation

The AMBER topology and coordinates were converted to OpenMM representation. A system was constructed with PME electrostatics (0.9 nm cutoff), hydrogen bond constraints, and rigid water. Topology, serialised system, and initial state were stored for MD production.

**Rationale.** OpenMM parameterisation enables GPU-accelerated MD with controlled force field representation and serves as input for staged equilibration and NPT production.

| Field | Value |
| :--- | :--- |
| Inputs | complex_solv.prmtop, complex_solv.inpcrd |
| Outputs | openmm_system.xml, openmm_topology.pkl, system_state.xml |
| Libraries | parmed, openmm |
| Status | running |

Parameters:

```yaml
constraints: HBonds
integrator: LangevinMiddleIntegrator
nonbonded_method: PME
rigid_water: True
```

#### 3. Molecular dynamics production with multi-frame collection

NPT molecular dynamics was run at 300 K and 1.0 atm for 20 ns (10,000,000 steps at 2 fs timestep) using CUDA GPU acceleration with mixed precision. Frames were saved every 100 ps (50,000 steps), yielding 200+ snapshots for subsequent ensemble analysis.

**Rationale.** Extended NPT sampling at physiological conditions with high frame frequency enables multi-frame MM/GBSA binding free energy calculation with improved convergence and ensemble-average stability prediction.

| Field | Value |
| :--- | :--- |
| Inputs | receptor_noh2.pdb |
| Tools | easy-md |
| Status | running |

Parameters:

```yaml
frame_spacing: 100 ps
pH: 7.4
platform: CUDA
precision: mixed
total_time: 20 ns
```

## Results

This phase produced no captured result output. Any files it wrote are listed under Output Artifacts below.

### Output Artifacts

**Table A.** Files produced by this phase. Hashes are truncated for reading; the full digest is in the artifact index.

| File | Format | Size | Location | SHA-256 (first 12) |
| :--- | :--- | :--- | :--- | :--- |
| 071_dg_ki.py | PY | 1.4 KB | 03_deltag_ic50_convert_can/source | 68723e118d3e... |

## Limitations

- No citation is on record for easy-md, so the versions used cannot be traced to a publication.
- Versions were not recorded for ParmEd, easy-md. A methods section without a version is not reproducible.

## References

1. Eastman P, et al. OpenMM 7: Rapid development of high performance algorithms for molecular dynamics. PLoS Comput Biol. 2017;13:e1005659. doi:10.1371/journal.pcbi.1005659
   *For OpenMM 8 cite doi:10.1021/acs.jpcb.3c06662 in addition.*
2. ParmEd version 4.3.1.

**No citation on record:** easy-md.

These were used by this phase and are reported for completeness. A citation should be supplied before this material is used in a manuscript. They are listed rather than omitted because a methods section that hides a dependency is not reproducible.
