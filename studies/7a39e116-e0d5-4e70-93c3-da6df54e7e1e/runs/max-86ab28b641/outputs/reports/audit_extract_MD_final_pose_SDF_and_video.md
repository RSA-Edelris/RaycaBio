# Audit: Extract MD-Refined Final Pose SDF and Trajectory Video for EL2003A

**Auditor:** independent review  
**Date:** 2026-09-07  
**Scope:** `extract_final_pose_sdf.py`, `make_traj_video.py`, `EL2003A_pose2_MD_final.sdf`, phase document

---

## CRITICAL (invalidates result)

### 1. Systematic 1-residue offset in Cα atom matching corrupts the alignment and final SDF coordinates

**Finding:** The residue-sequence-number matching that drives the Cα superposition pairs every GROMACS protein residue k with crystal protein residue k+1, because GROMACS resequenced the complex starting from resSeq 1 for MOL, pushing all protein residues up by 1. The intersection of the two resSeq sets therefore maps mismatched atoms for all 285 "matched" pairs, and the rotation/translation applied to extract ligand coordinates is wrong.

**Evidence, step by step:**

*complex_reres.pdb* (GROMACS topology PDB, lines 5-41 and 42+):
```
ATOM      1  C1  MOL     1   ...   (MOL occupies resSeq 1)
ATOM     37  H5  MOL     1   ...
ATOM     38  N   PRO     2   ...   (first protein residue: PRO at resSeq 2)
ATOM     50  CA  PRO     2   ...
ATOM     56  CA  ARG     3   ...
ATOM     80  CA  LYS     4   ...
ATOM    102  CA  LYS     5   ...
ATOM    124  CA  ARG     6   ...
```

*receptor_pH74_noH.pdb* (crystal reference, lines 4+):
```
ATOM      4  CA  PRO A   1   ...   (first protein residue: PRO at resSeq 1)
ATOM     19  CA  ARG A   2   ...
ATOM     43  CA  LYS A   3   ...
ATOM     65  CA  LYS A   4   ...
ATOM     87  CA  ARG A   5   ...
```

*Matching logic* (`extract_final_pose_sdf.py`, lines 36-41):
```python
traj_res_ca = {traj.topology.atom(a).residue.resSeq: a    for a in ca_traj}
rec_res_ca  = {receptor.topology.atom(a).residue.resSeq: a for a in ca_rec}
common_res  = sorted(set(traj_res_ca.keys()) & set(rec_res_ca.keys()))
```

- `traj_res_ca.keys()` = {2, 3, 4, ..., 287} (GROMACS protein)
- `rec_res_ca.keys()` = {1, 2, 3, ..., 286} (crystal reference)
- `common_res` = {2, 3, 4, ..., 286} — **285 values**

For each resSeq `r` in {2,...,286}, the pairing is:
- GROMACS resSeq r = protein residue r−1 by name (e.g., r=2 → PRO, r=3 → ARG, r=4 → LYS ...)
- Crystal resSeq r = protein residue r by name (e.g., r=2 → ARG, r=3 → LYS, r=4 → LYS ...)

Therefore resSeq 2 pairs GROMACS-PRO (protein residue 1) with crystal-ARG (protein residue 2); resSeq 3 pairs GROMACS-ARG (residue 2) with crystal-LYS (residue 3); and so on. Every pair involves adjacent residues, not the same residue. The matched atom sets are 285 pairs of consecutive-residue Cα atoms — not the same-residue Cα atoms that a valid alignment requires.

**Consequence for the 4.44 Å Cα RMSD:** A one-residue offset pairs Cα atoms that are ~3.8 Å apart along the backbone. After optimal superposition of 285 such mismatched pairs, the post-alignment RMSD is expected to be on the order of that inter-Cα spacing. The measured 4.44 Å is fully consistent with this arithmetic. The phase document's explanation — "H-addition differences from PDBFixer" — is incorrect; the dominant cause is systematic mismatched atom pairing.

**Consequence for the final SDF:** `last_traj.superpose(receptor, frame=0, atom_indices=traj_match, ref_atom_indices=rec_match)` (line 49-51 of `extract_final_pose_sdf.py`) computes and applies a rotation/translation derived from this mismatched set. The ligand coordinates extracted from the resulting aligned frame (`lig_xyz_A`, line 61) are therefore in a reference frame built from wrong correspondences. The absolute coordinates in `EL2003A_pose2_MD_final.sdf` are not reliably aligned to the crystal frame.

**Partial mitigation:** Frame-0 ligand RMSD vs original SDF = 0.55 Å (reported). Because frame 0 of the XTC starts from the docked pose (the same coordinates as the original SDF, before GROMACS solvation and equilibration shifts them to a new box origin), the misaligned transformation still places the ligand approximately near its original location — the system was initialized there and the misalignment error in the transformation is "small enough" to keep the result within ~0.55 Å at t=0. This partially masks the error. For t=1000 ps the accumulated error from incorrect alignment could be larger; the reported centroid (-4.89, 41.84, 45.29) should be treated as approximate.

**Correct fix:** Subtract 1 from all GROMACS protein resSeq values before matching (or, equivalently, match by residue name and sequential index, not by raw resSeq), so that GROMACS protein residue 1 (PRO, resSeq 2) is paired with crystal residue 1 (PRO, resSeq 1).

---

## MAJOR (may affect accuracy)

### 2. Ligand RMSD in `make_traj_video.py` uses internal re-superposition (superpose=True by default), underestimating positional displacement

**Finding:** `mdt.rmsd(traj, traj[0], atom_indices=lig_idx) * 10.0` (line 31) calls `mdt.rmsd` with its default `superpose=True`. This causes MDTraj to perform an additional optimal superposition of the ligand heavy atoms before computing RMSD, yielding best-fit (Kabsch-optimal) RMSD rather than positional RMSD in the binding-site frame. The trajectory has already been Cα-aligned at line 26 (`traj.superpose(traj[0], atom_indices=ca_idx)`), so the relevant quantity for "ligand RMSD in the binding site" is the positional RMSD after that protein alignment alone, computed without further superposition.

**Evidence:** `mdt.rmsd` docstring (extracted from `mdtraj._rmsd` compiled module):
```
superpose : bool, default=True
    Whether to use the Theobald QCP method to calculate RMSD. If True, the
    QCP method is used, which inherently superposes the structure based on
    the atom_indices selection.
```

**Consequence:** The reported range 0.00–1.73 Å is a lower bound on the actual ligand RMSD relative to its t=0 position in the aligned binding-site frame. For a molecule that undergoes rotational reorientation in the pocket, the best-fit RMSD can be substantially smaller than the positional RMSD. The figure title "EL2003A ligand RMSD vs. t=0 pose" and the document statement "Ligand RMSD range: 0.00–1.73 Å" imply positional RMSD; they should be labelled "best-fit RMSD" or the call should use `superpose=False`.

**Fix:** `mdt.rmsd(traj, traj[0], atom_indices=lig_idx, superpose=False) * 10.0` after the Cα superposition at line 26.

---

## VERIFIED CORRECT

### Item 1 — MDTraj 1.11.1 `superpose` accepts `ref_atom_indices`

Source: `/home/ubuntu/rayca-runtime/.venv/lib/python3.12/site-packages/mdtraj/core/trajectory.py`, lines 1083-1109:
```python
def superpose(
    self,
    reference,
    frame=0,
    atom_indices=None,
    ref_atom_indices=None,        # line 1088: parameter exists
    parallel=True,
):
    """...
    ref_atom_indices : array_like, or None
        Use these atoms on the reference structure. If not supplied,
        the same atom indices will be used for this trajectory and the
        reference one.
    ...
    """
```
The call `last_traj.superpose(receptor, frame=0, atom_indices=traj_match, ref_atom_indices=rec_match)` (lines 49-51 of `extract_final_pose_sdf.py`) is syntactically valid and dispatches the correct code path. There is no silent fallback. VERIFIED.

---

### Item 2 — MOL atom indices 0–36 are correct

`complex_reres.pdb` lines 5-41 (ATOM serials 1-37) are all `MOL resSeq 1`. Protein begins at serial 38 (`PRO resSeq 2`, line 42). MDTraj 0-indexes atoms in file order, so `traj.topology.select("resname MOL")` returns indices 0–36. The document's claim of "atom indices 0–36 in the stripped complex" is accurate. VERIFIED.

---

### Item 3 — MDTraj coordinate unit is nm; `* 10.0` is correct

`mdtraj/core/trajectory.py` line 733:
```python
_distance_unit = "nanometers"
```
The conversions `last_traj.xyz[0, lig_idx, :] * 10.0` (line 61) and `frame0.xyz[0, lig_idx, :] * 10.0` (line 71) correctly convert from nm to Å. Same applies to `traj.xyz[0, ...]  * 10` in `make_traj_video.py`. VERIFIED.

---

### Item 4 — Atom-ordering check (0.55 Å RMSD frame 0 vs original SDF) is a meaningful sanity test

Original SDF centroid computed from `all_poses/EL2003A_pose2.sdf` atom-coordinate block: (−4.82, 43.16, 44.52) Å. Raw GROMACS box centroid of the same 37 MOL atoms from `complex_reres.pdb` (lines 5-41): (60.52, 59.30, 28.61) Å. Centroid distance = 69.2 Å, consistent with the document's stated naïve RMSD of 39.4 Å (centroid difference is not the same as atom-by-atom RMSD). After alignment, frame-0 RMSD vs SDF = 0.55 Å, and SDF bond table is identical to the complex PDB atom ordering (both use the same 37 atoms in the same connectivity order). A random permutation of 37 atoms of varied element would produce RMSD >> 5 Å. The check is meaningful for confirming that the topology preserved atom order through GROMACS preparation. VERIFIED.

---

### Item 5 — RMSD formula correctness in `extract_final_pose_sdf.py` (lines 54-56)

```python
ca_traj_pos = last_traj.xyz[0, traj_match, :]  # (n_match, 3) nm
ca_rec_pos  = receptor.xyz[0, rec_match,   :]  # (n_match, 3) nm
rmsd_align  = float(np.sqrt(np.mean(np.sum((ca_traj_pos - ca_rec_pos)**2, axis=1)))) * 10.0
```

`np.sum(..., axis=1)` sums the three squared coordinate differences for each atom → per-atom squared distance; `np.mean` averages over atoms; `np.sqrt` gives the RMS distance in nm; `* 10.0` converts to Å. This is the standard RMSD formula with no axis confusion or off-by-one error. VERIFIED.

---

### Item 6 — Binding-site distance calculation axes are correct

`make_traj_video.py` lines 40-43:
```python
diffs = pro_pos_f0[:, None, :] - lig_pos_f0[None, :, :]  # shape (n_pro, n_lig, 3)
dists = np.sqrt((diffs**2).sum(axis=2))                   # shape (n_pro, n_lig)
min_dist = dists.min(axis=1)                              # shape (n_pro,)
```

`diffs.shape = (n_pro, 1, 3) - (1, n_lig, 3)` broadcasts to `(n_pro, n_lig, 3)`. `.sum(axis=2)` sums over the 3 Cartesian coordinates → `(n_pro, n_lig)` matrix of squared Euclidean distances. `.min(axis=1)` takes the minimum over the n_lig ligand atoms for each of the n_pro protein atoms → `(n_pro,)` vector of minimum atom-to-ligand distances. The mask `site_mask = min_dist < 0.5` then correctly identifies protein heavy atoms within 0.5 nm of any ligand atom. Axes are not confused; the calculation is correct. VERIFIED.

---

### Item 7 — Note on 4.44 Å post-alignment Cα RMSD

As established in the CRITICAL finding above, the 4.44 Å is primarily caused by the 1-residue offset in atom matching, not by MD structural drift. An inter-Cα spacing of ~3.8 Å along the backbone, after optimal superposition of 285 consecutive-residue pairs, produces post-alignment RMSD of approximately this magnitude. The document's explanation ("PDBFixer H-additions") is inconsistent with what H-addition would actually cause (< 0.5 Å local perturbation of backbone atoms). This is not an independent issue; it is the symptom identified in the CRITICAL finding.

---

### Item 8 — SDF molecular graph and conformer modification are correct

`Chem.RWMol(mol_orig)` (line 85) copies the molecular graph including all conformers. `mol_final.GetConformer()` (line 86) returns the existing conformer (index 0), not a new one. `conf.SetAtomPosition(i, Point3D(x, y, z))` (line 89) modifies the existing conformer's coordinate array in-place. `mol_final.GetMol()` (line 91) returns a read-only Mol retaining the modified conformer. Output SDF counts line: `37 41` (37 atoms, 41 bonds) matches the original SDF counts line `37 41`. Bond block is identical between original and output SDF (both have 41 bond entries in the same order). Centroid recomputed from the output SDF atom coordinate block = (−4.89, 41.84, 45.29) Å, matching the document's reported value exactly. VERIFIED.

---

## Summary table

| Item | Classification | One-line finding |
|:---|:---|:---|
| Residue-number offset in Cα matching | **CRITICAL** | GROMACS protein starts at resSeq 2 (MOL=1); crystal starts at resSeq 1; every Cα pair is 1 residue off; alignment and final SDF coordinates are wrong |
| Ligand RMSD uses superpose=True (re-superposes on lig atoms) | **MAJOR** | mdt.rmsd default gives best-fit (lower-bound) RMSD, not positional RMSD in binding-site frame; use superpose=False after Cα alignment |
| `ref_atom_indices` parameter valid in MDTraj 1.11.1 | VERIFIED CORRECT | trajectory.py line 1088 |
| MOL atom indices 0–36 | VERIFIED CORRECT | complex_reres.pdb ATOM 1-37 all MOL, protein starts at ATOM 38 |
| nm → Å conversion (`* 10.0`) | VERIFIED CORRECT | trajectory.py line 733: `_distance_unit = "nanometers"` |
| Atom-ordering check RMSD 0.55 Å | VERIFIED CORRECT | 69 Å initial offset, 37-atom random permutation would give >> 5 Å; 0.55 Å confirms ordering |
| RMSD formula in extract script | VERIFIED CORRECT | sqrt(mean(sum((Δ)²,axis=1))) is standard formula, no axis error |
| Binding-site distance axis choice | VERIFIED CORRECT | dists(n_pro,n_lig).min(axis=1) = (n_pro,) min over ligand atoms |
| SDF molecular graph preserved | VERIFIED CORRECT | RWMol + SetAtomPosition modifies existing conformer; output 37 atoms / 41 bonds matches original |
