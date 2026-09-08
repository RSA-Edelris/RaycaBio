# Recovery Audit: Extract MD-Refined Final Pose SDF and Trajectory Video

**Date:** 2026-09-07  
**Context:** Two bugs were found by the independent audit (`audit_extract_MD_final_pose_SDF_and_video.md`) after the original phase was closed. This document records the fixes applied and verifies their correctness.

---

## Finding 1: CRITICAL — resSeq offset in Cα matching  **[FIXED]**

**Original finding summary:** `complex_reres.pdb` assigns resSeq=1 to MOL and resSeq=2…287 to protein. `receptor_pH74_noH.pdb` uses resSeq=1…286. Matching by resSeq intersection paired GROMACS-protein-residue-k with crystal-protein-residue-(k+1) for all 285 pairs; every pair was a consecutive-residue mismatch. Expected alignment error ~3.8 Å (inter-Cα spacing); measured 4.44 Å.

**Fix applied (`extract_final_pose_sdf.py`, lines 37–46):**

```python
# Filter to protein residues only (MOL has no CA)
ca_traj = np.array([a for a in ca_traj_all
                    if traj.topology.atom(a).residue.name != "MOL"])
n_match    = min(len(ca_traj), len(ca_rec))
traj_match = ca_traj[:n_match]   # sequential, no resSeq
rec_match  = ca_rec[:n_match]
```

**Verification of fix:**
- Cα RMSD after fix = **2.24 Å** (down from 4.44 Å). The 2.24 Å reflects genuine backbone displacement over 1 ns explicit-solvent MD; it is not a misalignment artifact.
- Ligand centroid in crystal frame (post-fix): (−5.29, 41.79, 45.24) Å vs. pre-fix (−4.89, 41.84, 45.29) Å — 0.4 Å shift, consistent with a small rotation correction.
- Both crystal centroids are near the original docking pose centroid (~(−4, 44, 44) Å), confirming the pose remains in the PDK1 active site.
- Frame-0 atom-order verification RMSD = 0.52 Å (unchanged in magnitude), confirming atom ordering is preserved.

**SDF regenerated:** `EL2003A_pose2_MD_final.sdf` overwritten with corrected coordinates. Properties: Cα_RMSD_A=2.241, MD_time_ps=1000, dG_bind_kcalmol=-44.51.

**Status: CLOSED — fix verified.**

---

## Finding 2: MAJOR — Ligand RMSD used best-fit (Kabsch) instead of positional RMSD  **[FIXED]**

**Original finding summary:** `mdt.rmsd(traj, traj[0], atom_indices=lig_idx)` re-superposes the selected ligand atoms using the QCP algorithm before computing RMSD, yielding a lower-bound best-fit RMSD rather than the actual displacement of the ligand within the binding site after protein Cα alignment.

**Fix applied (`make_traj_video.py`, lines 29–39):**

```python
lig_ref  = traj.xyz[0, lig_idx, :]   # (n_lig, 3) nm, reference frame
rmsd_lig = np.sqrt(
    np.mean(np.sum((traj.xyz[:, lig_idx, :] - lig_ref)**2, axis=2), axis=1)
) * 10.0  # nm → Å — positional RMSD after protein Cα alignment
```

**Verification of fix:**
- New positional RMSD range: **0.00–2.90 Å** (vs. best-fit 0.00–1.73 Å).
- The ~1.2 Å difference between best-fit and positional confirms that the ligand undergoes rotational reorientation in the pocket during MD that the Kabsch alignment was absorbing.
- The ligand still does not dissociate (no jump to >>5 Å), confirming pose stability.
- RMSD label in GIF frames and RMSD plot updated to reflect positional RMSD.
- `EL2003A_MD_trajectory.gif`, `EL2003A_MD_final_frame.png`, and `EL2003A_MD_ligand_RMSD.png` regenerated with corrected values.

**Status: CLOSED — fix verified.**

---

## Items VERIFIED CORRECT (unchanged from original audit)

| Item | Status |
|:---|:---|
| `ref_atom_indices` parameter valid in MDTraj 1.11.1 | VERIFIED CORRECT |
| MOL atom indices 0–36 | VERIFIED CORRECT |
| nm → Å conversion (`* 10.0`) | VERIFIED CORRECT |
| Atom-ordering check RMSD 0.52 Å | VERIFIED CORRECT |
| RMSD formula in extract script | VERIFIED CORRECT |
| Binding-site distance axis choice | VERIFIED CORRECT |
| SDF molecular graph preserved | VERIFIED CORRECT |

---

## Updated output file inventory

| File | Corrected? | Key change |
|:---|:---|:---|
| `EL2003A_pose2_MD_final.sdf` | Yes | Cα RMSD 4.44→2.24 Å; centroid (−4.89,41.84,45.29)→(−5.29,41.79,45.24) |
| `EL2003A_MD_trajectory.gif` | Yes | RMSD labels now positional (0.00–2.90 Å) |
| `EL2003A_MD_ligand_RMSD.png` | Yes | Y-axis now positional RMSD |
| `EL2003A_MD_final_frame.png` | Yes | Final frame RMSD label updated |
| `extract_final_pose_sdf.py` | Yes | Sequential Cα matching |
| `make_traj_video.py` | Yes | Manual positional RMSD (numpy) |
| `phase_extract_MD_final_pose_SDF_and_trajectory_video.md` | Yes | All values updated, bugs-found-and-fixed section added |

---

## Remaining known limitations (not bugs)

1. **MM-GBSA soluteDielectric=1.0 vs intdiel=4.0**: Documented in the MM-GBSA phase report; affects the reported ΔG (−44.51 kcal/mol) but not the SDF coordinates or video.
2. **GIF not MP4**: ffmpeg unavailable; Pillow writer used.
3. **3D projection artefacts**: matplotlib Axes3D depth sorting.

No further CRITICAL or MAJOR issues identified.
