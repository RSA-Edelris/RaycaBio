
import parmed as pmd
import mdtraj as md
import numpy as np
import os

work = "gbsa_run/EL2003A_pose2"

# 1. Load GROMACS topology + structure (already water-stripped)
print("Loading GROMACS topology...")
gmx = pmd.load_file(f"{work}/complex.top", xyz=f"{work}/complex_reres.pdb")

print(f"  Atoms: {len(gmx.atoms)}")
print(f"  Residues: {len(gmx.residues)}")
last_res = gmx.residues[-1]
print(f"  Last residue: {last_res.name} #{last_res.idx+1} n_atoms={len(last_res.atoms)}")

# Check if WAT present
res_names = set(r.name for r in gmx.residues)
print(f"  Residue types: {sorted(res_names)}")

# Identify ligand residue index
lig_idx = None
for i, r in enumerate(gmx.residues):
    if r.name == "MOL":
        lig_idx = i
        print(f"  Ligand 'MOL' residue index: {i}")
        break
