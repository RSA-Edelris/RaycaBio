#!/usr/bin/env python3
"""
Extract the last MD frame (t=1000 ps) for EL2003A as an SDF in crystal frame.
Aligns the trajectory back onto the original 1Z5M receptor (crystal coords)
via matching Cα atoms before extracting ligand coordinates.
"""
import numpy as np, sys, os

WS   = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
WORK = f"{WS}/gbsa_run/EL2003A_pose2"

import mdtraj as mdt
from rdkit import Chem
from rdkit.Geometry import Point3D

# ── 1. Load trajectory ───────────────────────────────────────────────────────
traj = mdt.load(f"{WORK}/traj_com.xtc", top=f"{WORK}/complex_reres.pdb")
print(f"Trajectory: {traj.n_frames} frames, {traj.n_atoms} atoms")
t_last = float(traj.time[-1])
print(f"Last frame t = {t_last:.0f} ps")

# ── 2. Load crystal receptor as alignment reference ──────────────────────────
# Use receptor_pH74_noH.pdb (same source as the GBSA container input)
for ref_path in [f"{WS}/receptor_pH74_noH.pdb",
                 f"{WS}/1Z5M_receptor_pH7.4.pdb"]:
    if os.path.exists(ref_path):
        break
receptor = mdt.load(ref_path)
print(f"Crystal reference: {ref_path}")
print(f"  {receptor.n_atoms} atoms, {receptor.n_residues} residues")

# ── 3. Match Cα atoms between trajectory and receptor by residue sequence nr ─
ca_traj = traj.topology.select("name CA")
ca_rec  = receptor.topology.select("name CA")

traj_res_ca = {traj.topology.atom(a).residue.resSeq: a    for a in ca_traj}
rec_res_ca  = {receptor.topology.atom(a).residue.resSeq: a for a in ca_rec}

common_res  = sorted(set(traj_res_ca.keys()) & set(rec_res_ca.keys()))
traj_match  = np.array([traj_res_ca[r] for r in common_res])
rec_match   = np.array([rec_res_ca[r]  for r in common_res])
print(f"Matched Cα atoms: {len(common_res)}")

# ── 4. Superpose last frame of trajectory onto crystal receptor ──────────────
# Extract single-frame trajectory of just the last frame
last_traj = traj[-1]

# MDTraj superpose: align last_traj onto receptor using matched Cα
last_traj.superpose(receptor, frame=0,
                    atom_indices=traj_match,
                    ref_atom_indices=rec_match)

# Verify alignment quality
ca_traj_pos = last_traj.xyz[0, traj_match, :]  # (n_match, 3) nm
ca_rec_pos  = receptor.xyz[0, rec_match,   :]  # (n_match, 3) nm
rmsd_align  = float(np.sqrt(np.mean(np.sum((ca_traj_pos - ca_rec_pos)**2, axis=1)))) * 10.0  # Å
print(f"Post-alignment Cα RMSD: {rmsd_align:.3f} Å")

# ── 5. Extract ligand coordinates from aligned last frame ────────────────────
lig_idx    = traj.topology.select("resname MOL")
lig_xyz_A  = last_traj.xyz[0, lig_idx, :] * 10.0  # nm → Å
print(f"Ligand atoms: {len(lig_idx)}")
print(f"Ligand centroid (crystal frame): {lig_xyz_A.mean(axis=0)}")

# ── 6. Verify atom ordering: compare traj frame 0 (aligned) to original SDF ─
# Also align frame 0 the same way
frame0 = traj[0]
frame0.superpose(receptor, frame=0,
                 atom_indices=traj_match,
                 ref_atom_indices=rec_match)
f0_lig_xyz_A = frame0.xyz[0, lig_idx, :] * 10.0  # Å

mol_orig = Chem.MolFromMolFile(f"{WS}/all_poses/EL2003A_pose2.sdf",
                               removeHs=False, sanitize=True)
orig_conf = mol_orig.GetConformer()
orig_xyz  = np.array([list(orig_conf.GetAtomPosition(i))
                      for i in range(mol_orig.GetNumAtoms())])

rmsd_order = float(np.sqrt(np.mean((f0_lig_xyz_A - orig_xyz)**2)))
print(f"Atom-order check (frame 0 aligned vs original SDF): RMSD = {rmsd_order:.3f} Å "
      f"({'OK' if rmsd_order < 2.0 else 'WARNING: check order'})")

# ── 7. Build SDF with MD final coordinates ───────────────────────────────────
from rdkit.Chem import RWMol
mol_final = RWMol(mol_orig)
conf      = mol_final.GetConformer()
for i in range(mol_final.GetNumAtoms()):
    x, y, z = float(lig_xyz_A[i, 0]), float(lig_xyz_A[i, 1]), float(lig_xyz_A[i, 2])
    conf.SetAtomPosition(i, Point3D(x, y, z))

mol_final = mol_final.GetMol()
mol_final.SetProp("_Name",           "EL2003A_MD_final")
mol_final.SetProp("Source",          "EL2003A pose2, GROMACS 1 ns MD, last frame t=1000 ps")
mol_final.SetProp("Aligned_to",      os.path.basename(ref_path))
mol_final.SetProp("Ca_RMSD_A",       f"{rmsd_align:.3f}")
mol_final.SetProp("MD_time_ps",      str(int(t_last)))
mol_final.SetProp("pIC50_PDK",       "7.9")
mol_final.SetProp("dG_bind_kcalmol", "-44.51")
mol_final.SetProp("method",          "MM-GBSA OBC2 1-traj 1 ns GROMACS AMBER03+GAFF2")

out = f"{WS}/EL2003A_pose2_MD_final.sdf"
writer = Chem.SDWriter(out)
writer.write(mol_final)
writer.close()
print(f"\nWritten: {out}")
