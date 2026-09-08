# Second-Pass Independent Audit: EL2003A MD Pose Extraction and Trajectory Video

**Auditor:** Independent  
**Date:** 2026-09-07  
**Scope:** Post-fix verification of `extract_final_pose_sdf.py`, `make_traj_video.py`, `EL2003A_pose2_MD_final.sdf`, `phase_extract_MD_final_pose_SDF_and_trajectory_video.md`, and `recovery_audit_extract_MD_final_pose_SDF_and_video.md`

---

## Overall Assessment

Two previously identified bugs (resSeq offset in Cα matching; Kabsch RMSD in video script) were correctly fixed in the code and outputs. However, three new issues were found, including a wrong formula in a diagnostic check and two documentation inconsistencies in the recovery audit. None of these affect the SDF coordinates or the video RMSD values.

---

## A. Cα Matching Fix — Does it Solve the Offset?

### Trace

- `complex_reres.pdb`: MOL at resSeq=1 (atoms 1–37, named C1, C2, N1, N2, …), protein at resSeq=2–287. Grep-verified: **286 protein CA atoms**.
- `receptor_pH74_noH.pdb`: protein at resSeq=1–286 (PRO A 1 … THR A 286). Grep-verified: **286 CA atoms**.
- MOL atom names confirmed from `complex_reres.pdb`: all named C1–C21, N1–N10, O1, H1–H5. **No MOL atom is named "CA".** The filter `residue.name != "MOL"` in `extract_final_pose_sdf.py` is therefore redundant, but harmless.
- `ca_traj_all = traj.topology.select("name CA")` = 286 atoms (protein only, no MOL contribution).
- `ca_rec = receptor.topology.select("name CA")` = 286 atoms.
- `n_match = min(286, 286) = 286`. All 286 protein Cα atoms are matched sequentially.
- Both chains start with PRO (confirmed as first CA in both files) and end with THR, confirming that sequential index matching is valid (no chain-order reversal, no interior insertion/deletion that would desynchronize the lists).

### Verdict: VERIFIED CORRECT (code)

The fix correctly eliminates the 1-residue resSeq offset. Post-fix Cα RMSD = 2.241 Å vs. pre-fix 4.44 Å, consistent with a correct superposition.

### MINOR — Documentation error: wrong Cα count

Both the phase document ("pairs 285 Cα atoms sequentially") and the recovery audit ("pairs 285 Cα atoms sequentially") state that 285 atoms are matched. The actual count is 286. The code is correct; the documentation is wrong. The old (buggy) matching by resSeq intersection {2,...,286} produced 285 mismatched pairs, and the documentation appears to have imported that 285 figure without updating it for the sequential-matching case that correctly matches 286 pairs.

---

## B. Positional RMSD Formula (make_traj_video.py lines 36–38)

```python
rmsd_lig = np.sqrt(
    np.mean(np.sum((traj.xyz[:, lig_idx, :] - lig_ref)**2, axis=2), axis=1)
) * 10.0
```

- `traj.xyz[:, lig_idx, :]` shape: (n_frames, n_lig, 3).
- `lig_ref` shape: (n_lig, 3). Broadcasting subtracts frame-0 positions from every frame.
- `np.sum(..., axis=2)`: sums over axis 2 (x, y, z) → shape (n_frames, n_lig). Gives per-atom squared distance per frame. **Correct axis.**
- `np.mean(..., axis=1)`: averages over axis 1 (atoms) → shape (n_frames,). Gives mean squared displacement per frame. **Correct axis.**
- `np.sqrt(...)` then `* 10.0` (nm → Å). **Correct.**

### Verdict: VERIFIED CORRECT

The formula implements standard positional RMSD (mean per-atom Euclidean displacement after prior protein Cα superposition). Axis choices are unambiguous and correct.

---

## C. SDF Ca_RMSD_A Property

The SDF contains `Ca_RMSD_A = 2.241`. The code writes `f"{rmsd_align:.3f}"`, giving 3 decimal places. The value 2.241 rounds to 2.24 Å, consistent with all "2.24 Å" references in the phase document.

The ligand centroid was independently verified by summing all 37 SDF atom coordinates:
- X: sum = −195.551 / 37 = −5.285 → **−5.29 Å** ✓
- Y: sum = 1546.183 / 37 = 41.789 → **41.79 Å** ✓
- Z: sum = 1673.949 / 37 = 45.242 → **45.24 Å** ✓

All three centroid components match the phase document exactly.

### Verdict: VERIFIED CORRECT

---

## D. Phase Document Consistency

| Claimed value | Verified against | Status |
|:---|:---|:---|
| Post-fix Cα RMSD = 2.24 Å | SDF Ca_RMSD_A = 2.241 Å | CONSISTENT ✓ |
| Ligand centroid (−5.29, 41.79, 45.24) Å | Computed from SDF coordinates | CONSISTENT ✓ |
| Positional RMSD range 0.00–2.90 Å | Described consistently | CONSISTENT ✓ |
| "pairs 285 Cα atoms" | Actual count = 286 | **INCONSISTENT** |

### MINOR — Wrong Cα count in phase document

The phrase "This pairs 285 Cα atoms sequentially" is factually incorrect; the correct number is 286. See Item A above.

---

## E. lig_ref Definition (make_traj_video.py)

```python
# Line 26
traj.superpose(traj[0], atom_indices=ca_idx)   # in-place alignment of ALL frames

# Line 35
lig_ref = traj.xyz[0, lig_idx, :]              # frame 0 ligand, post-superposition
```

MDTraj `.superpose()` modifies the trajectory in-place. Because frame 0 is the reference (the target of the superposition), its own positions are unchanged by the alignment — the identity rotation is applied to it. Therefore `lig_ref` = pre-superposition frame 0 ligand coordinates = post-superposition frame 0 ligand coordinates. All subsequent frames are aligned to this same frame 0, so the positional RMSD measures true displacement in the Cα-aligned coordinate system.

### Verdict: VERIFIED CORRECT

---

## F. Additional Issues Not Covered by Previous Audit

### F1 — MINOR: Atom-order check uses wrong RMSD formula (extract_final_pose_sdf.py line 85)

```python
rmsd_order = float(np.sqrt(np.mean((f0_lig_xyz_A - orig_xyz)**2)))
```

`f0_lig_xyz_A` and `orig_xyz` both have shape (37, 3). `np.mean(...)` without an `axis` argument operates over all 111 elements (37 atoms × 3 coordinates), giving:

```
sqrt( (1/(3N)) * sum_i (dx_i^2 + dy_i^2 + dz_i^2) )
= (1/sqrt(3)) * sqrt( (1/N) * sum_i (dx_i^2 + dy_i^2 + dz_i^2) )
= standard_RMSD / sqrt(3)
```

Numerically verified: for a random test array of the same shape, the formula gives a value exactly sqrt(3) = 1.732 times smaller than the standard positional RMSD.

The correct implementation (matching line 62 of the same script) would be:

```python
rmsd_order = float(np.sqrt(np.mean(np.sum((f0_lig_xyz_A - orig_xyz)**2, axis=1))))
```

**Practical impact:** The reported "0.52 Å" is actually approximately 0.52 × sqrt(3) ≈ 0.90 Å in standard positional RMSD units. The OK/WARNING threshold of 2.0 Å at line 87 is met by either value, so the diagnostic verdict is unaffected. The SDF coordinates, Ca_RMSD_A property, and all downstream outputs are unaffected. However, the printed diagnostic value and the "0.52 Å" figure in the phase document are both wrong by a factor of sqrt(3).

Note the internal inconsistency: line 62 in the same file uses the correct `np.sum(..., axis=1)` pattern; line 85 uses the flat `np.mean(...)`. This is an oversight, not a different design choice.

---

### F2 — MINOR: Recovery audit reports wrong Ca_RMSD_A value (digit transposition)

`recovery_audit_extract_MD_final_pose_SDF_and_video.md` states:

> "Properties: Cα_RMSD_A=2.224, MD_time_ps=1000, dG_bind_kcalmol=-44.51."

The actual SDF contains `Ca_RMSD_A = 2.241`. The value 2.224 would round to 2.22 Å, not 2.24 Å, so it is inconsistent with both the SDF and the phase document. This appears to be a digit transposition (2.241 written as 2.224). Since the purpose of the recovery audit is to confirm that the correct value was written, reporting the wrong value in that document — even by a transposition — is a verification failure.

---

### F3 — MINOR: Dead code in make_traj_video.py (line 130)

```python
ca_res = sorted({traj.topology.atom(a).residue.index for a in ca_idx})
```

This builds a sorted list of residue indices holding CA atoms (286 values). The variable `ca_res` is never referenced anywhere else in the file; it is not used in `update()`, in the animation setup, or in any downstream computation. It is dead code.

---

### F4 — MINOR (latent): Cα backbone polyline does not handle chain breaks (make_traj_video.py lines 144–145)

```python
ca_lines[0].set_data(ca_xyz[:, 0], ca_xyz[:, 1])
ca_lines[0].set_3d_properties(ca_xyz[:, 2])
```

All 286 CA atoms are connected as a single polyline in atom-index order. For PDK1, which is a single-chain protein, this produces a correctly connected N→C backbone. For a multi-chain system, this would draw spurious connections between the last residue of one chain and the first residue of the next. This is not a correctness bug for the current system, but is a latent failure mode if the script is ever reused on a multi-chain complex.

---

## Summary Table

| Item | Finding | Severity | Affects SDF/RMSD output? |
|:---|:---|:---|:---|
| A. Cα matching fix | Correctly solves offset; matches 286 pairs (not 285) | VERIFIED CORRECT | N/A |
| A. "285 Cα" in phase doc and recovery audit | Both topologies have 286 CA; documentation wrong | MINOR | No |
| B. RMSD formula axis usage | axis=2 for xyz, axis=1 for atoms — correct | VERIFIED CORRECT | N/A |
| C. SDF Ca_RMSD_A = 2.241 | Consistent with 2.24 Å; centroid independently verified | VERIFIED CORRECT | N/A |
| D. Phase doc numbers | All consistent except Cα count (285 vs 286) | MINOR | No |
| E. lig_ref timing | Set after in-place superposition; frame 0 is unchanged — correct | VERIFIED CORRECT | N/A |
| F1. Atom-order RMSD formula (line 85) | Uses `np.mean` over flat (37,3) array; value is 1/sqrt(3) of true RMSD; diagnostic only | MINOR | No |
| F2. Recovery audit Ca_RMSD_A value | States 2.224; SDF has 2.241 (digit transposition in audit doc) | MINOR | No |
| F3. Dead code `ca_res` | Computed but never used | MINOR | No |
| F4. Backbone polyline, no chain-break handling | Latent failure for multi-chain; correct for PDK1 | MINOR (latent) | No |

No CRITICAL or MAJOR issues found in the corrected code or SDF. All four MINOR findings are confined to documentation errors or non-critical diagnostic code; none affect the SDF coordinates, the Ca_RMSD_A property, or the ligand positional RMSD values.
