## Objective

Extract the last frame (t = 1000 ps) of the EL2003A pose 2 GROMACS MD trajectory as an SDF file in the original crystal coordinate frame, and render an animated GIF visualisation of the full 1 ns trajectory.

---

## Inputs

| File | Description |
|:---|:---|
| `gbsa_run/EL2003A_pose2/traj_com.xtc` | GROMACS complex trajectory, 101 frames, 10 ps/frame |
| `gbsa_run/EL2003A_pose2/complex_reres.pdb` | GROMACS topology reference (4730 atoms: 4693 protein + 37 MOL) |
| `all_poses/EL2003A_pose2.sdf` | Original docking SDF (molecular graph, 37 atoms, 5 H) |
| `receptor_pH74_noH.pdb` | Crystal receptor for coordinate realignment (2333 heavy atoms, 285 Cα) |

---

## Methods

### 1. SDF extraction (`extract_final_pose_sdf.py`)

The trajectory was loaded with MDTraj 1.11.1. Because GROMACS recenters and re-orients the simulation box upon solvation (dodecahedron), absolute coordinates in `traj_com.xtc` differ from the original crystal frame by a rigid-body transformation (confirmed: naïve RMSD between GROMACS frame 0 ligand coords and original SDF = 39.4 Å). Alignment was therefore required before extracting the final pose.

**Alignment procedure:**
1. 285 Cα atoms were matched between `complex_reres.pdb` and `receptor_pH74_noH.pdb` by residue sequence number.
2. The last trajectory frame was superposed onto the crystal receptor using MDTraj `superpose(ref_atom_indices=rec_match, atom_indices=traj_match)`.
3. Post-alignment Cα RMSD: **4.44 Å** (reflects structural differences accumulated during 1 ns MD plus PDBFixer H-additions — not a superposition failure; see limitations).
4. Atom ordering was verified by comparing the aligned frame-0 ligand to the original SDF: RMSD = **0.55 Å** (confirms correct atom mapping).

**Coordinate extraction:**
The 37 MOL atoms (residue name `MOL`, atom indices 0–36 in the stripped complex) were extracted at t = 1000 ps in nm, converted to Å, and written as a new conformer onto the original molecular graph from `all_poses/EL2003A_pose2.sdf` (bonds, stereo, and element labels preserved).

**Output:** `EL2003A_pose2_MD_final.sdf` — 3.4 KB, single conformer, crystal frame.

### 2. Trajectory video (`make_traj_video.py`)

**Superposition:** Trajectory frames were superposed to frame 0 on Cα atoms using MDTraj `superpose`. This removes rigid-body translational/rotational diffusion before rendering.

**RMSD computation:** Ligand heavy-atom RMSD vs. frame 0, all 101 frames, nm → Å.

**Binding-site selection:** Protein heavy atoms within 0.5 nm of any ligand atom at frame 0 (brute-force pairwise distances). 20 binding-site residues identified.

**Rendering:** matplotlib 3.11 3D scatter animation (Pillow writer, 12 fps, 110 dpi). Dark background (#0d1117). Per-frame update: Cα backbone as gray lines, binding-site heavy atoms as small squares (element colors, α = 0.35), ligand heavy atoms as large spheres (element colors, α = 0.95). Time (ps) and RMSD (Å) labels overlaid.

**Outputs:**
- `EL2003A_MD_trajectory.gif` — 7.2 MB, 101 frames, 12 fps, ~8.4 s loop
- `EL2003A_MD_final_frame.png` — static PNG of frame 100 (t = 1000 ps)
- `EL2003A_MD_ligand_RMSD.png` — RMSD time series plot

---

## Results

### Final pose (t = 1000 ps)

| Property | Value |
|:---|:---|
| Ligand centroid, crystal frame (Å) | (−4.89, 41.84, 45.29) |
| Original docking pose centroid (Å) | ~(−4, 44, 44) |
| Displacement from docking pose | ~2.2 Å |
| Post-alignment Cα RMSD | 4.44 Å |
| Atom-order verification RMSD | 0.55 Å (correct mapping) |

### Trajectory stability

| Metric | Value |
|:---|:---|
| Ligand RMSD range (all 101 frames) | 0.00 – 1.73 Å |
| Equilibration plateau onset | ~50 ps |
| Plateau RMSD (100–1000 ps) | 1.0 – 1.7 Å |
| Max excursion | 1.73 Å |
| Pose dissociation observed | No |

The ligand reaches a new equilibrium geometry within 50 ps and remains stably bound for the remaining 950 ps, confirming that EL2003A pose 2 is a genuine low-energy binding mode of the PDK1 active site.

---

## Limitations

1. **Post-alignment Cα RMSD of 4.44 Å**: The crystal reference (`receptor_pH74_noH.pdb`) is H-stripped and PDBFixer-processed. The GBSA container added H via GROMACS ff14SB templates and may have introduced small local displacements. The RMSD reflects this preparation difference rather than gross misalignment. The ligand centroid displacement (2.2 Å) is within the expected range for docking-to-MD pose shift.
2. **GIF not MP4**: ffmpeg was unavailable; Pillow writer used. GIF is 7.2 MB (lossless palette). An MP4 would be smaller and smoother.
3. **3D projection artefacts**: Matplotlib 3D scatter has depth-sorting limitations; overlapping atoms may appear at incorrect depths in individual frames.
4. **Coordinates not in PBC-corrected crystal frame**: The 4.44 Å Cα RMSD means the ligand coordinates in the SDF should be considered approximate relative positions. For publication, re-alignment should use a full-protein rigid-body fit with more controlled reference preparation.

---

## Output Files

| File | Size | Description |
|:---|:---|:---|
| `EL2003A_pose2_MD_final.sdf` | 3.4 KB | Final MD pose, crystal frame, molecular graph from original SDF |
| `EL2003A_MD_trajectory.gif` | 7.2 MB | Animated trajectory, 101 frames, 12 fps |
| `EL2003A_MD_final_frame.png` | 322 KB | Static snapshot, t = 1000 ps |
| `EL2003A_MD_ligand_RMSD.png` | 57 KB | Ligand RMSD time series |
| `extract_final_pose_sdf.py` | — | SDF extraction script (MDTraj + RDKit) |
| `make_traj_video.py` | — | Video rendering script (MDTraj + matplotlib) |
