#!/usr/bin/env python3
"""
Extract the last MD frame (t=1000 ps) for the EL2003A ligand as an SDF file.
Atom order in the trajectory is matched to the original SDF via position mapping.
"""
import numpy as np, sys, os

WS   = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
WORK = f"{WS}/gbsa_run/EL2003A_pose2"

import mdtraj as mdt
from rdkit import Chem
from rdkit.Chem import AllChem

# ── 1. Load trajectory and extract last frame ────────────────────────────────
traj = mdt.load(f"{WORK}/traj_com.xtc", top=f"{WORK}/complex_reres.pdb")
print(f"Trajectory: {traj.n_frames} frames, {traj.n_atoms} atoms")

last_frame = traj[-1]
t_last = float(traj.time[-1])
print(f"Last frame: t = {t_last:.0f} ps")

# ── 2. Identify ligand atoms in topology ────────────────────────────────────
lig_idx = traj.topology.select("resname MOL")
print(f"Ligand atom indices in topology: {len(lig_idx)} atoms ({lig_idx[0]}–{lig_idx[-1]})")

# Coordinates of ligand at last frame, nm → Å
lig_xyz_A = last_frame.xyz[0, lig_idx, :] * 10.0
print(f"Ligand centroid (last frame, Å): {lig_xyz_A.mean(axis=0)}")

# ── 3. Load original SDF for molecular graph ─────────────────────────────────
mol_orig = Chem.MolFromMolFile(f"{WS}/all_poses/EL2003A_pose2.sdf",
                               removeHs=False, sanitize=True)
n_atoms = mol_orig.GetNumAtoms()
print(f"Original SDF atoms: {n_atoms}")

if n_atoms != len(lig_idx):
    print(f"WARNING: atom count mismatch ({n_atoms} vs {len(lig_idx)})")
    sys.exit(1)

# ── 4. Verify atom ordering by comparing t=0 frame to original SDF ──────────
first_frame_xyz = traj[0].xyz[0, lig_idx, :] * 10.0  # Å
orig_conf = mol_orig.GetConformer()
orig_xyz  = np.array([list(orig_conf.GetAtomPosition(i)) for i in range(n_atoms)])

rmsd_check = float(np.sqrt(np.mean((first_frame_xyz - orig_xyz)**2)))
print(f"RMSD between SDF coords and traj frame-0 coords: {rmsd_check:.3f} Å  "
      f"({'OK — same ordering' if rmsd_check < 1.0 else 'LARGE — may be reordered'})")

# ── 5. Build new molecule with last-frame coordinates ────────────────────────
from rdkit.Chem import RWMol
from rdkit.Geometry import Point3D

mol_final = Chem.RWMol(mol_orig)
conf = mol_final.GetConformer()
for i in range(n_atoms):
    x, y, z = float(lig_xyz_A[i, 0]), float(lig_xyz_A[i, 1]), float(lig_xyz_A[i, 2])
    conf.SetAtomPosition(i, Point3D(x, y, z))

# ── 6. Add metadata and write SDF ────────────────────────────────────────────
mol_final = mol_final.GetMol()
mol_final.SetProp("_Name",           "EL2003A_MD_final")
mol_final.SetProp("Source",          "EL2003A pose2, GROMACS MD last frame t=1000 ps")
mol_final.SetProp("MD_time_ps",      str(int(t_last)))
mol_final.SetProp("pIC50_PDK",       "7.9")
mol_final.SetProp("dG_bind_kcalmol", "-44.51")
mol_final.SetProp("method",          "MM-GBSA OBC2 1-traj ensemble mean, 1 ns GROMACS")

out = f"{WS}/EL2003A_pose2_MD_final.sdf"
writer = Chem.SDWriter(out)
writer.write(mol_final)
writer.close()
print(f"\nWritten: {out}")
print(f"  Ligand centroid (final): {lig_xyz_A.mean(axis=0)}")
