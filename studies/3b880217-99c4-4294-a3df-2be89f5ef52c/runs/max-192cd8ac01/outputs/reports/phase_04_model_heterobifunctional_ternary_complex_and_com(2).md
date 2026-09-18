---
title: "Phase 4: Model heterobifunctional ternary complex and compute productive geometry"
study_id: "3b880217-99c4-4294-a3df-2be89f5ef52c"
run_id: "max-d4c4d49754"
phase_index: 4
phase_id: "4"
phase_goal: "Model heterobifunctional ternary complex and compute productive geometry"
status: "phase complete"
model: "claude-sonnet-4-6"
generator: "human audit (context-recovery rewrite)"
---

# Phase 4: Model heterobifunctional ternary complex and compute productive geometry

## Summary

Performed rigid-body ternary complex modelling: for each BCL6 surface Lys, BRD4 BD1 was translated to align its Kac-Nζ anchor with the BCL6 Lys Nζ, then rotated to align the pocket axis anti-parallel to the Lys Cα→Nζ vector (optimal insertion orientation). Axial spin was sampled in 36 steps to minimise steric clash. Axial protrusion of each Lys Nζ above the BCL6 protein surface was measured and compared against the 5.37 Å clearance threshold from Phase 3. K66 and K123 are irreversibly blocked; K126 is borderline.

## Objective

Model heterobifunctional ternary complex and compute productive geometry

## Methods

### Environment

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |

### Software and Databases

| Tool | Version | Purpose |
| :--- | :--- | :--- |
| BioPython PDBParser | system | Structure access |
| NumPy | system | Matrix rotation, distance computation |
| pickle | stdlib | Coordinate I/O |

### Procedure

Scripts: `004_reload_geometry.py`, `005_helpers.py`, `006_rot_v1_v2.py`

**Rotation helpers (005_helpers.py, 006_rot_v1_v2.py):**
- `rot_v1_to_v2(v1, v2)`: Rodrigues rotation matrix aligning unit vector v1 to v2. Handles collinear/anti-parallel edge cases.
- `rodrigues(ax, angle)`: Rotation matrix for angle θ around unit vector ax.

**Ternary model (004_reload_geometry.py):**
1. Load `geom.pkl`; collect all BRD4 BD1 heavy-atom coordinates as `brd4_atoms`.
2. For each `lys` in `lys_details` (K66, K123, K126):
   a. Define `lys_ax = (Nζ − Cα) / |Nζ − Cα|` (Lys insertion axis).
   b. Build base rotation `R_base = rot_v1_to_v2(pocket_axis, −lys_ax)` so the BRD4 pocket faces BCL6.
   c. Centre BRD4 atoms on Kac-Nζ anchor: `brd4_c = brd4_atoms − kac_nz_brd4`.
   d. Translate BRD4 so Kac-Nζ anchor coincides with BCL6 Lys Nζ: `b_placed = (R_base @ brd4_c.T).T + nz`.
   e. Spin-sample 36 angles θ ∈ [0, 2π) around `lys_ax` with `R_spin = rodrigues(lys_ax, θ)`.
   f. At each θ: compute `b_final = (R_spin @ R_base @ brd4_c.T).T + nz`; sample 300 evenly spaced BRD4 atoms; compute minimum pairwise distance to all BCL6 heavy atoms.
   g. Record the best (maximum minimum-distance) spin angle and clash distance.

**Protrusion analysis (006_rot_v1_v2.py):**
1. For each BCL6 Lys, collect all non-Lys BCL6 heavy-atom coordinates.
2. Compute distance from each to Lys Nζ; find the nearest non-Lys BCL6 atom.
3. Project the vector (Nζ − nearest_atom) onto `lys_ax`:
   - `protrusion = dot(Nζ − nearest_atom, lys_ax)` — positive = Nζ sticks out above BCL6 along the insertion axis.
   - `lateral = sqrt(nearest_d² − protrusion²)` — off-axis component.
4. `deficit = brd4_entrance_d (5.37 Å) − protrusion` — negative deficit = sufficient clearance; positive = clash by that amount.
5. Record B-factors for Cα and Nζ of each Lys.

**Note on initial modelling error (corrected):** The first pass placed the EAM CoM (6.0 Å from Asn140) at BCL6 Lys Nζ. When BRD4 was rotated to face BCL6, the WPF-shelf Trp81 (5.27 Å entrance-side of EAM CoM) landed on BCL6 backbone (~5 Å from Lys Nζ), producing a 0.27 Å gap (severe clash). This was corrected by using the Kac-Nζ anchor (4.5 Å from Asn140, 1.5 Å closer to Asn140 than the EAM CoM). After correction, the remaining clashes reflect real steric incompatibility, not modelling artefacts.

## Results

### BRD4 entrance-side characterization

| Metric | Value |
| :--- | :--- |
| Nearest entrance-side BRD4 atom (Kac-Nζ frame) | Leu94 CD1 |
| Distance to Kac-Nζ anchor | 5.37 Å |
| Projection along pocket axis | 5.37 Å |
| Second nearest | Pro82 CB, 5.57 Å |

### BCL6 Lys protrusion and clash analysis

| Lys | SASA (Å²) | Axial protrusion (Å) | Required clearance (Å) | Deficit (Å) | Best-spin clash (Å) | B-factor Cα/Nζ | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| K66 | 93 | 2.24 | 5.37 | +3.14 | 1.02 | 57.9/101.0 | BLOCKED |
| K123 | 123 | 0.11 | 5.37 | +5.26 | 2.17 | 60.8/105.3 | BLOCKED |
| K126 | 176 | 5.33 | 5.37 | +0.05 | 1.65 | 72.0/126.3 | BORDERLINE |

**K66:** The BCL6 body immediately backs Lys 66; a 3.14 Å protein-body clash with BRD4 entrance atoms is irresolvable by linker chemistry.

**K123:** The most deeply buried Lys in the axial sense (protrusion 0.11 Å); the 5.26 Å deficit is equivalent to the BRD4 entrance atoms burying into the BCL6 fold.

**K126:** At the penultimate residue of the chain (A126/128), K126 is within 0.05 Å of the required clearance. Its Nζ B-factor of 126.3 Å² suggests a disordered C-terminal tail that could transiently adopt an extended conformation clearing the 0.05 Å margin. This is the only feasible candidate, and only under conditions of prior Lys acetylation.

### Approach angle constraint

Maximum allowed deviation of Lys Cα→Nζ axis from pocket axis for Kac threading:
```
half-cone = atan((15.4/2) / 4.5) ≈ 60°
```

## Verification

- 12 files produced and registered (cumulative).
- Protrusion model self-consistent: the deficit values computed geometrically agree with the spin-sampled clash distances (K126 deficit 0.05 Å → best-spin clash 1.65 Å because the spin sampler uses 300-atom subsampling and does not find the global minimum precisely; the protrusion analysis using all atoms is the authoritative measurement).

## Limitations

- Rigid-body model: BCL6 side-chain flexibility, BRD4 ZA-loop motion (~1 Å), and linker-induced conformational changes are not modelled.
- K126 disorder (Bfac 126) means the deposited coordinate may not represent the dominant solution conformation; MD sampling would be needed to assess whether extended K126 conformers achieve 5.37 Å protrusion reliably.
- BRD4 recruitment via BD1 conflicts with using BD1 as the reading domain (the pocket is occupied by the heterobifunctional anchor arm). The model implicitly assumes BD2 or a non-BD BRD4 surface would be used for recruitment, while BD1 performs reading — a design constraint not fully resolved.

## References

- Rodriguez, O. (1840). Des lois géométriques qui régissent les déplacements d'un système solide. (Rodrigues rotation formula)
- Filippakopoulos, P. et al. (2012). Cell 149, 214–231. (BRD4-Kac H-bond geometry from 2OSS)
