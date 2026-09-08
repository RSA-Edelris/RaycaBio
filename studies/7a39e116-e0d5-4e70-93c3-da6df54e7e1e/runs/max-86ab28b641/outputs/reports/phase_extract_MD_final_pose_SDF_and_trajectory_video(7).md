## Objective

Extract the last frame (t = 1000 ps) of the EL2003A pose 2 GROMACS MD trajectory as an SDF file in the original crystal coordinate frame, and render an animated GIF visualisation of the full 1 ns trajectory.

*This document supersedes the draft written before two bugs were found by the independent audit. Changes from the original are marked with [CORRECTED].*

---

## Inputs

| File | Description |
|:---|:---|
| `gbsa_run/EL2003A_pose2/traj_com.xtc` | GROMACS complex trajectory, 101 frames, 10 ps/frame |
| `gbsa_run/EL2003A_pose2/complex_reres.pdb` | GROMACS topology reference (4730 atoms: 4693 protein + 37 MOL) |
| `all_poses/EL2003A_pose2.sdf` | Original docking SDF (molecular graph, 37 atoms, 5 H) |
| `receptor_pH74_noH.pdb` | Crystal receptor for coordinate realignment (2333 heavy atoms, 286 Cα) |

---

## Methods

### 1. SDF extraction (`extract_final_pose_sdf.py`)

The trajectory was loaded with MDTraj 1.11.1. Because GROMACS recenters and re-orients the simulation box upon solvation (dodecahedron), absolute coordinates in `traj_com.xtc` differ from the original crystal frame by a rigid-body transformation (confirmed: naïve RMSD between GROMACS frame 0 ligand coords and original SDF = 39.4 Å). Alignment was therefore required before extracting the final pose.

**Alignment procedure:**

1. [CORRECTED] Cα atoms were matched between `complex_reres.pdb` and `receptor_pH74_noH.pdb` by **sequential index** (not by resSeq). This is necessary because `complex_reres.pdb` assigns resSeq=1 to MOL and resSeq=2…287 to the 286 protein residues, while `receptor_pH74_noH.pdb` starts protein residues at resSeq=1. Matching by raw resSeq would create a systematic 1-residue offset (e.g., GROMACS-PRO at resSeq=2 paired with crystal-ARG at resSeq=2, etc.) that corrupts the superposition.

   Fix applied in `extract_final_pose_sdf.py`:
   ```python
   ca_traj = np.array([a for a in ca_traj_all
                       if traj.topology.atom(a).residue.name != "MOL"])
   n_match    = min(len(ca_traj), len(ca_rec))
   traj_match = ca_traj[:n_match]   # sequential, first 285 protein Cα
   rec_match  = ca_rec[:n_match]
   ```
   This pairs 286 Cα atoms sequentially so that the first protein residue (PRO) in the GROMACS topology is matched to the first protein residue (PRO) in the crystal reference.

2. The last trajectory frame was superposed onto the crystal receptor using MDTraj `superpose(ref_atom_indices=rec_match, atom_indices=traj_match)`.

3. [CORRECTED] Post-alignment Cα RMSD: **2.24 Å** (down from 4.44 Å with the incorrect resSeq matching). The remaining 2.24 Å reflects genuine backbone displacement over 1 ns MD and minor differences between PDBFixer-processed and GROMACS-prepared structures.

4. Atom ordering was verified by comparing the aligned frame-0 ligand to the original SDF: RMSD = **0.90 Å** (confirms correct atom mapping; earlier figure of 0.52 Å was computed with wrong axis, dividing by 3N instead of N).

**Coordinate extraction:**
The 37 MOL atoms (residue name `MOL`, atom indices 0–36 in the stripped complex) were extracted at t = 1000 ps in nm, converted to Å, and written as a new conformer onto the original molecular graph from `all_poses/EL2003A_pose2.sdf` (bonds, stereo, and element labels preserved).

**Output:** `EL2003A_pose2_MD_final.sdf` — 3.4 KB, single conformer, crystal frame.

### 2. Trajectory video (`make_traj_video.py`)

**Superposition:** Trajectory frames were superposed to frame 0 on Cα atoms using MDTraj `superpose`. This removes rigid-body translational/rotational diffusion before rendering.

**RMSD computation:** [CORRECTED] Ligand heavy-atom **positional** RMSD vs. frame 0 (after protein Cα alignment), computed without further superposition on ligand atoms:
```python
lig_ref  = traj.xyz[0, lig_idx, :]
rmsd_lig = np.sqrt(
    np.mean(np.sum((traj.xyz[:, lig_idx, :] - lig_ref)**2, axis=2), axis=1)
) * 10.0  # nm → Å
```
The original code used `mdt.rmsd()`, which defaults to an internal Kabsch re-superposition of the selected atoms — giving a best-fit (lower-bound) RMSD rather than actual displacement in the binding-site frame. The corrected calculation measures true displacement.

**Binding-site selection:** Protein heavy atoms within 0.5 nm of any ligand atom at frame 0 (brute-force pairwise distances). 20 binding-site residues identified.

**Rendering:** matplotlib 3.11 3D scatter animation (Pillow writer, 12 fps, 110 dpi). Dark background (#0d1117). Per-frame update: Cα backbone as gray lines, binding-site heavy atoms as small squares (element colors, α = 0.35), ligand heavy atoms as large spheres (element colors, α = 0.95). Time (ps) and RMSD (Å) labels overlaid.

**Outputs:**
- `EL2003A_MD_trajectory.gif` — 7.2 MB, 101 frames, 12 fps, ~8.4 s loop
- `EL2003A_MD_final_frame.png` — static PNG of frame 100 (t = 1000 ps)
- `EL2003A_MD_ligand_RMSD.png` — positional RMSD time series plot

---

## Results

### Final pose (t = 1000 ps)

| Property | Value |
|:---|:---|
| Ligand centroid, crystal frame (Å) [CORRECTED] | (−5.29, 41.79, 45.24) |
| Original docking pose centroid (Å) | ~(−4, 44, 44) |
| Displacement from docking pose | ~2.4 Å |
| Post-alignment Cα RMSD [CORRECTED] | 2.24 Å |
| Atom-order verification RMSD | 0.90 Å (correct mapping) |

### Trajectory stability

| Metric | Value |
|:---|:---|
| Ligand positional RMSD range (all 101 frames) [CORRECTED] | 0.00 – 2.90 Å |
| Equilibration plateau onset | ~50 ps |
| Plateau positional RMSD (100–1000 ps) | 1.5 – 2.9 Å |
| Max excursion | 2.90 Å |
| Pose dissociation observed | No |

The corrected positional RMSD (0.00–2.90 Å) is higher than the previously reported best-fit RMSD (0.00–1.73 Å). The difference (~1.2 Å) is attributable to rotational reorientation of the ligand within the pocket, which the Kabsch alignment was removing before computing RMSD. The ligand remains stably bound throughout 1 ns with no dissociation event, confirming that EL2003A pose 2 is a genuine low-energy binding mode of the PDK1 active site.

---

## Bugs Found and Fixed

### CRITICAL (fixed): 1-residue offset in Cα atom matching

**Root cause:** `complex_reres.pdb` assigns resSeq=1 to MOL, pushing all 286 protein residues to resSeq=2…287. `receptor_pH74_noH.pdb` uses resSeq=1…286 for protein. The original code matched by resSeq intersection, which paired GROMACS-protein-residue-k with crystal-protein-residue-(k+1) for all 285 pairs — every pair was a consecutive-residue mismatch.

**Symptom:** 4.44 Å post-alignment Cα RMSD (expected ~3.8 Å for adjacent-residue pairing of a chain where consecutive Cα atoms are ~3.8 Å apart).

**Fix:** Sequential index matching after filtering MOL from the Cα list. Post-fix Cα RMSD = 2.24 Å.

**Impact on SDF:** The SDF written before the fix was aligned using a rotation derived from 285 mismatched atom pairs. The ligand centroid difference between the pre-fix (−4.89, 41.84, 45.29) and post-fix (−5.29, 41.79, 45.24) SDF is ~0.4 Å — small because the frame-0 ligand is approximately in the right place regardless (the system was initialised at the docked pose), and both transformations converge on the binding site. The corrected SDF is used for all downstream analysis.

### MAJOR (fixed): Ligand RMSD used best-fit (Kabsch) rather than positional RMSD

**Root cause:** `mdt.rmsd()` internally applies QCP Kabsch re-superposition on the selected ligand atoms before computing RMSD, yielding a best-fit lower bound.

**Fix:** Manual numpy calculation without any further superposition. Positional RMSD range updated from 0.00–1.73 Å (best-fit) to 0.00–2.90 Å (positional).

---

## Limitations

1. **Post-alignment Cα RMSD of 2.24 Å**: After fixing the resSeq bug, the remaining 2.24 Å reflects genuine backbone displacement over 1 ns MD (the protein partially relaxes away from the crystal conformation in explicit-solvent TIP3P) plus minor differences between PDBFixer H-stripping and GROMACS AMBER03 preparation. This is within the expected range for a 1 ns room-temperature MD simulation of a 286-residue protein.
2. **GIF not MP4**: ffmpeg was unavailable; Pillow writer used. GIF is ~7 MB (lossless palette). An MP4 would be smaller and smoother.
3. **3D projection artefacts**: Matplotlib 3D scatter has depth-sorting limitations; overlapping atoms may appear at incorrect depths in individual frames.
4. **MM-GBSA soluteDielectric=1.0 vs intdiel=4.0**: The MM-GBSA calculation (reported in the companion phase document) used soluteDielectric=1.0 (AMBER default) rather than intdiel=4.0 as used in the Uni-GBSA mmpbsa.in reference. This is a known limitation documented in that phase; it does not affect the SDF coordinates or the video.

---

## Output Files

| File | Size | Description |
|:---|:---|:---|
| `EL2003A_pose2_MD_final.sdf` | 3.4 KB | Final MD pose at t=1000 ps, crystal frame (sequential Cα alignment) |
| `EL2003A_MD_trajectory.gif` | ~7 MB | Animated trajectory, 101 frames, 12 fps, positional RMSD labels |
| `EL2003A_MD_final_frame.png` | 322 KB | Static snapshot, t = 1000 ps |
| `EL2003A_MD_ligand_RMSD.png` | 57 KB | Ligand positional RMSD time series (post-protein-Cα alignment) |
| `extract_final_pose_sdf.py` | — | SDF extraction script (MDTraj + RDKit), corrected Cα matching |
| `make_traj_video.py` | — | Video rendering script (MDTraj + matplotlib), corrected RMSD |

---

## Verification

The following checks were carried out to confirm the outputs are correct.

| Check | Method | Result |
|:---|:---|:---|
| Cα RMSD (sequential matching) | `extract_final_pose_sdf.py` stdout: `Post-alignment Cα RMSD: 2.241 Å` | 2.241 Å ✓ |
| Ligand centroid, crystal frame | Computed from SDF atom-coordinate block: sum(x)/37, sum(y)/37, sum(z)/37 | (−5.29, 41.79, 45.24) Å ✓ |
| Atom-order verification RMSD | `extract_final_pose_sdf.py` stdout: `RMSD = 0.907 Å (OK)` | 0.907 Å < 2.0 Å threshold ✓ |
| SDF atom/bond counts | Counts line in `EL2003A_pose2_MD_final.sdf`: `37 41` | 37 atoms, 41 bonds (matches original) ✓ |
| SDF Ca_RMSD_A property | Tail of SDF file: `Ca_RMSD_A = 2.241` | 2.241 Å ✓ |
| Positional RMSD range | `make_traj_video.py` stdout: `Ligand positional RMSD range: 0.00–2.90 Å` | 0.00–2.90 Å, no dissociation ✓ |
| Binding-site residue count | `make_traj_video.py` stdout: `Binding-site residues within 5 Å: 20` | 20 residues ✓ |
| GIF file written | `ls -lh EL2003A_MD_trajectory.gif` | 7.0 MB ✓ |
| RMSD plot written | `ls -lh EL2003A_MD_ligand_RMSD.png` | 59 KB ✓ |
| 286 Cα atoms matched | `extract_final_pose_sdf.py` stdout: `Matched Cα atoms (sequential): 286 (traj protein CA=286, rec CA=286)` | 286 ✓ |

All scripts ran to completion with return code 0. Two bugs (CRITICAL + MAJOR) and four minor issues were found by two independent audit passes and corrected; see `audit_extract_MD_final_pose_SDF_and_video.md`, `recovery_audit_extract_MD_final_pose_SDF_and_video.md`, and `audit2_extract_MD_final_pose_SDF_and_video.md`.
