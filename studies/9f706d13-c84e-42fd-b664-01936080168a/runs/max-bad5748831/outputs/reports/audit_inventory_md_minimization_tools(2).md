# Audit Report: Inventory MD and Minimization Tools Phase

**Auditor:** Independent schema-verification agent  
**Method:** Each claim verified against the live tool registry via `mcp__rayca__aidd_tool_schema`  
**Date:** 2026-09-09

## Verification

- **9 tools audited:** openmm, gromacs, chaperong, membrane-gromacs, openmm-metadynamics, af-calvados, orb-models3, auto-martini, dynamate
- **9 live `aidd_tool_schema` calls made**, one per tool, results compared directly against phase claims
- **0 CRITICAL findings** — no claim found that would invalidate a simulation result
- **2 MAJOR findings** — (1) no persistent phase document written; (2) gromacs force field enum incomplete (amber94, amber96, amber99 omitted)
- **55 individual parameter/field claims verified correct** across the 9 tools
- Verification was performed by a second independent agent with no access to the inventory agent's tool call results; all schema comparisons were made from fresh queries

---

## Meta-Finding: No Phase Document

**MAJOR.** The "Inventory MD and minimization tools" phase produced its findings live from tool schema queries and wrote no persistent document. There is no file-backed audit trail, no reproducible record of what was queried or when, and no way to diff this inventory against future schema changes. All findings below were reconstructed from claims stated inline in the audit request, not from a stored document.

---

## Tool-by-Tool Findings

---

### 1. openmm

| Claim | Live Schema | Verdict |
|---|---|---|
| Required: `pdbFile` (PDB) | `"required": ["pdbFile"]` | VERIFIED CORRECT |
| Force field enum: ff19SB, ff14SB, amber14, amber99sb, amber99sb-ildn, amber03, amber10, charmm36 | Enum exactly matches | VERIFIED CORRECT |
| Default force field: ff19SB | `"default": "ff19SB"` | VERIFIED CORRECT |
| Default water model: tip3p | `"default": "tip3p"` | VERIFIED CORRECT |
| Water model enum: tip3p, tip3pfb, spce, tip4pew, tip5p, opc | Enum exactly matches | VERIFIED CORRECT |
| Default timestep: 2 fs | `"default": 2` on `timestep` (fs) | VERIFIED CORRECT |
| Default minimizationSteps: 10000 | `"default": 10000` | VERIFIED CORRECT |
| Default equilibrationTime: 0.2 ns | `"default": 0.2` | VERIFIED CORRECT |
| Default productionTime: 2 ns | `"default": 2` | VERIFIED CORRECT |
| systemType enum: ["protein"] only | `"enum": ["protein"]` | VERIFIED CORRECT |
| Output fields (14 fields listed) | Live output_fields array matches exactly | VERIFIED CORRECT |

**No discrepancies found for openmm.**

---

### 2. gromacs

| Claim | Live Schema | Verdict |
|---|---|---|
| Required: systemType, uploadType, forceField | All three marked `"required": true` | VERIFIED CORRECT |
| Force fields: AMBER99SB, AMBER99SB-ILDN, AMBER03, CHARMM27, OPLS-AA, GROMOS54A7 (6 listed) | Enum has 9 values: amber99sb, amber99sb-ildn, amber03, **amber94**, **amber96**, **amber99**, charmm27, oplsaa, gromos54a7 | **MAJOR** |
| Output fields (11 fields listed) | Live output_fields array matches exactly | VERIFIED CORRECT |

**MAJOR: gromacs force field enum is incomplete.** The phase listed 6 force fields but the live schema exposes 9. Three options were omitted: `amber94`, `amber96`, and `amber99`. Any downstream decision about which force field to use for a run was made without knowledge of these three available options. The claim was derived from a partial inspection of the enum.

---

### 3. chaperong

| Claim | Live Schema | Verdict |
|---|---|---|
| Required: `input` (PDB) | `"required": ["input"]` | VERIFIED CORRECT |
| Default force field: amber99sb | Parameter `ff`, `"default": "amber99sb"` | VERIFIED CORRECT |
| Default water: tip3p | Parameter `water`, `"default": "tip3p"` | VERIFIED CORRECT |
| Default temp: 300 K | `"default": 300` | VERIFIED CORRECT |
| Default dt: 0.002 ps (2 fs) | `"default": 0.002` | VERIFIED CORRECT |
| Default em_nsteps: 50000 | `"default": 50000` | VERIFIED CORRECT |
| Default nvt_nsteps: 50000 | `"default": 50000` | VERIFIED CORRECT |
| Default npt_nsteps: 50000 | `"default": 50000` | VERIFIED CORRECT |
| Default md_nsteps: 500000 (= 1 ns at 2 fs) | `"default": 500000`; duration = 500000 * 0.002 ps = 1000 ps = 1 ns | VERIFIED CORRECT |
| sysType enum: ["protein-only"] only | `"enum": ["protein-only"]` | VERIFIED CORRECT |
| mdType enum: ["conventional"] only | `"enum": ["conventional"]` | VERIFIED CORRECT |
| Output fields (14 fields listed) | Live output_fields array matches exactly | VERIFIED CORRECT |

**No discrepancies found for chaperong.**

---

### 4. membrane-gromacs

| Claim | Live Schema | Verdict |
|---|---|---|
| Required: `pdbFile` | `"required": ["pdbFile"]` | VERIFIED CORRECT |
| Output fields: gpu, membrane, n_atoms, steps, structure, summary, temperature_K, topology, trajectory (9 fields) | Live output_fields array matches exactly | VERIFIED CORRECT |

**No discrepancies found for membrane-gromacs.**

Note: The phase made only sparse claims for this tool (required input and output fields only). The live schema additionally exposes 10 optional parameters (cgEquilibrationTime, lipidLowerLeaflet, lipidUpperLeaflet, membranePreset, membraneType, numReplicas, salt, saveFreq, simulationTime, temp) and a default temperature of 310 K (physiological), which were not inventoried in the phase. This is an omission rather than an error.

---

### 5. openmm-metadynamics

| Claim | Live Schema | Verdict |
|---|---|---|
| Required: `pdbFile` + `cv1Atoms` | `"required": ["pdbFile", "cv1Atoms"]` | VERIFIED CORRECT |
| cv1Atoms: 1-based atom serial indices | Schema description confirms 1-based serials | VERIFIED CORRECT |
| collectiveVariable1 enum: rmsd, distance, angle, torsion, gyration | Enum exactly matches | VERIFIED CORRECT |
| Default metadynamicsType: well-tempered | `"default": "well-tempered"` | VERIFIED CORRECT |
| Default biasFactor: 10 | `"default": 10` | VERIFIED CORRECT |
| Default productionTime: 10 ns | `"default": 10` | VERIFIED CORRECT |
| Default minimizationSteps: 10000 | `"default": 10000` | VERIFIED CORRECT |
| Output fields (17 fields listed) | Live output_fields array matches exactly: bias_factor, collective_variables, colvar_file, fes_file, force_field, free_energy_range_kj_mol, gpu, hills_file, metadynamics_type, n_atoms, n_gaussians, openmm_version, plumed_version, steps, structure, summary, trajectory | VERIFIED CORRECT |

**No discrepancies found for openmm-metadynamics.**

---

### 6. af-calvados

| Claim | Live Schema | Verdict |
|---|---|---|
| Required: `name` (string — protein name, used to find <name>.pdb and <name>.json) | `"required": ["name"]`; description confirms PDB + PAE JSON lookup | VERIFIED CORRECT |
| Default box_L: 50 nm | `"default": 50` | VERIFIED CORRECT |
| Default temp: 293.15 K | `"default": 293.15` | VERIFIED CORRECT |
| Default ionic: 0.15 M | `"default": 0.15` | VERIFIED CORRECT |
| Default n_frames: 10 | `"default": 10` | VERIFIED CORRECT |
| Default platform: CUDA | `"default": "CUDA"` | VERIFIED CORRECT |
| Output fields: log, n_frames, platform_used, radius_of_gyration_nm, summary, topology, trajectory | Live output_fields array matches exactly | VERIFIED CORRECT |

**No discrepancies found for af-calvados.**

---

### 7. orb-models3

| Claim | Live Schema | Verdict |
|---|---|---|
| Zero required inputs | `"required": []` | VERIFIED CORRECT |
| Default model: orb-v3-conservative-inf-omat | `"default": "orb-v3-conservative-inf-omat"` | VERIFIED CORRECT |
| optimize default: false (single-point evaluation) | `"default": false` | VERIFIED CORRECT |
| Default fmax: 0.05 eV/Å | `"default": 0.05` | VERIFIED CORRECT |
| Default max_steps: 200 | `"default": 200` | VERIFIED CORRECT |
| Output fields: energy, forces, model, n_atoms, optimized, stress, summary | Live output_fields array matches exactly | VERIFIED CORRECT |

**No discrepancies found for orb-models3.**

---

### 8. auto-martini

| Claim | Live Schema | Verdict |
|---|---|---|
| Zero required inputs | `"required": []` | VERIFIED CORRECT |
| Input via smiles OR sdf OR sdf_content | Parameters `smiles`, `sdf`, `sdf_content` all present | VERIFIED CORRECT |
| Default molname: MOL | `"default": "MOL"` | VERIFIED CORRECT |
| Default write_cg_gro: true | `"default": true` | VERIFIED CORRECT |
| Default write_aa_gro: false | `"default": false` | VERIFIED CORRECT |
| Output fields: aa_gro_file, atom_partitioning, auto_martini_version, bead_names, cg_gro_file, molname, n_beads, summary, topology, topology_file | Live output_fields array matches exactly | VERIFIED CORRECT |

**No discrepancies found for auto-martini.**

---

### 9. dynamate

| Claim | Live Schema | Verdict |
|---|---|---|
| Required: `systemType` | `"required": ["systemType"]` | VERIFIED CORRECT |
| Output fields: analysis, analysis_report, force_field, gpu, n_atoms, pressure_bar, steps, structure, summary, temperature_K, topology, trajectory, water_model (13 fields) | Live output_fields array matches exactly | VERIFIED CORRECT |

**No discrepancies found for dynamate.**

Note: The phase made only sparse claims for dynamate (required input and output fields). The live schema exposes a full set of optional parameters not inventoried in the phase; this is an omission rather than an error. The dynamate `forceField` enum (amber99sb, amber99sb-ildn, amber03, amber99, charmm27, oplsaa, gromos54a7) was not claimed in the phase and was not checked.

---

## Summary Table

| Tool | Findings | Severity |
|---|---|---|
| (All tools) | No phase document written; findings have no audit trail | MAJOR |
| gromacs | Force field enum incomplete: amber94, amber96, amber99 not listed | MAJOR |
| openmm | All checked claims correct | VERIFIED CORRECT |
| chaperong | All checked claims correct | VERIFIED CORRECT |
| membrane-gromacs | All checked claims correct (sparse coverage) | VERIFIED CORRECT |
| openmm-metadynamics | All checked claims correct | VERIFIED CORRECT |
| af-calvados | All checked claims correct | VERIFIED CORRECT |
| orb-models3 | All checked claims correct | VERIFIED CORRECT |
| auto-martini | All checked claims correct | VERIFIED CORRECT |
| dynamate | All checked claims correct (sparse coverage) | VERIFIED CORRECT |

---

## No CRITICAL Findings

No claim was found that would directly invalidate a simulation result. The gromacs omission affects which force fields an operator knows are available but does not corrupt any run that was actually submitted.

---

## Recommendations

1. **Write a stored inventory document** for any future inventory phase. Live-only findings cannot be diffed against schema updates.
2. **Re-inventory gromacs force fields**: users should be informed that amber94, amber96, and amber99 are also available options, in addition to the six listed.
3. **Expand membrane-gromacs and dynamate inventory**: both tools have optional parameters (notably the 310 K physiological default temperature for membrane-gromacs) that were not captured in the phase.
