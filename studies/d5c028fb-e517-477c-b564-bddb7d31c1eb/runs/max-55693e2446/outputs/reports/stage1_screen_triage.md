
## Input

- **File**: user-supplied `ASMS.sdf` (V3000 format, 23,712 entries)
- **Activity field**: `HIT P841` — values `"Active"` / `"Inactive"`
- **Quantitative field**: `AS_ratio` (affinity-selection signal ratio; higher = stronger binder)
- **Target context**: CDK2–Cyclin E protein–protein interface stabilisation (confirmed from crystal structure analysis in Stage 2)

## Active/Inactive counts

| Class | Count | Fraction |
|---|---|---|
| Active | 15 | 0.063% |
| Inactive | 23,697 | 99.937% |
| Total | 23,712 | — |

## AS-ratio distribution (actives)

| Compound | AS ratio | Rank |
|---|---|---|
| EDS00495858 | 0.1720 | 1 |
| EDS00480994 | 0.0891 | 2 |
| EDS00490594 | 0.0301 | 3 |
| EDS00469766 | 0.0333 | 4 |
| EDS00481762 | 0.0181 | 5 |
| EDS00459346 | 0.0208 | 6 |
| EDS00444974 | 0.0163 | 7 |
| EDS00492874 | 0.0106 | 8 |
| EDS00492986 | 0.0097 | 9 |
| EDS00459442 | 0.0083 | 10 |
| EDS00459274 | 0.0074 | 11 |
| EDS00474254 | 0.0037 | 12 |
| EDS00474362 | 0.0026 | 13 |
| EDS00470458 | 0.0015 | 14 |
| EDS00490706 | 0.0012 | 15 |

Range: 0.0012 – 0.172 (143-fold spread across the 15 actives).

## Scaffold analysis

All 15 actives were loaded as RDKit mol objects from their SMILES strings (no 3D coordinates used at this stage). Murcko scaffolds were computed; all 15 are unique, confirming genuine structural diversity across actives.

Maximum common substructure (MCS) search across all 15 actives:

- **MCS**: 15 atoms, 16 bonds
- **SMARTS**: `[#6](=O)-[#7]1-[#6]-[#6]-[#6]2:[#6](-[#6]-1):[#7]:[#6](:[#6]:[#6]:2)-[#6](=O)-[#7]`

This MCS corresponds to the **tetrahydronaphthyridine (THN) bicyclic core** with two flanking amide groups (N-acyl at ring N and C3-amide-NH linker).

## Chemotype breakdown

| Chemotype | Count | Members |
|---|---|---|
| THN scaffold (matches MCS) | 13 | All actives except EDS00492874 and EDS00492986 |
| Piperidinyl-succinamide (alternate) | 2 | EDS00492874, EDS00492986 |

The two non-THN actives (EDS00492874, EDS00492986) share a distinct core: a piperidine ring with succinamide-type amide substitution and no fused ring. They are treated as a separate chemotype for design purposes.

## R-group positions on THN core

The THN scaffold carries two variable positions:

- **R1** (N-acyl group): heteroaromatic ring acylating the ring nitrogen — varies across all 13 THN actives
- **R2** (C3-amide arm): an NH–CH₂–Ar group appended to the pyridine ring C3-position — varies across all 13 THN actives

## Physicochemical properties of actives

| Metric | Min | Median | Max |
|---|---|---|---|
| MW (Da) | 353 | 487 | 549 |
| clogP | 1.5 | 3.6 | 4.4 |
| HBD | 1 | 1 | 2 |
| TPSA (Å²) | 62 | 89 | 121 |

All actives carry exactly 1–2 H-bond donors. HBD = 1 is present in 14/15 actives (the conserved THN ring NH). EDS00444974 is the smallest active (MW 353) and represents the minimal pharmacophore.

## Parsing note

Inactive records in the SDF have an empty `Hit_rank` field. A strict integer cast raises `ValueError` for empty strings, which caused silent dropping of inactives during initial loading. This did not affect the active compound analysis but means inactive properties were not profiled. No inactive structural analysis was performed in this stage.

## Output of this stage

- 15 active SMILES with AS ratios and compound IDs
- Identified THN as the dominant scaffold (13/15)
- Identified two R-group positions for analogue design
- Smallest active (EDS00444974, MW 353) flagged as minimal pharmacophore reference

These outputs were consumed directly by Stage 2 (binding site characterisation) and Stage 4 (analogue design).
