
import numpy as np
from collections import defaultdict

def read_ca_coords(path, chain_id):
    """Return {resnum: np.array([x,y,z])} for CA atoms."""
    coords = {}
    with open(path) as f:
        for line in f:
            if line[:4] == "ATOM" and line[21] == chain_id and line[12:16].strip() == "CA":
                resnum = int(line[22:26])
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                coords[resnum] = np.array([x, y, z])
    return coords

def read_hetatm_coords(path, chain_id, resname):
    """Return all heavy-atom coords for a specific HETATM residue."""
    atoms = []
    with open(path) as f:
        for line in f:
            if line[:6].strip() == "HETATM" and line[21] == chain_id:
                rn = line[17:20].strip()
                if rn == resname:
                    x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                    name = line[12:16].strip()
                    atoms.append((name, np.array([x, y, z])))
    return atoms

# Load BD1 (3MXF chain A) and BD2 (5T35 chain A) CA coords
pdb3 = work_dir / "3MXF.pdb"
pdb5 = work_dir / "5T35.pdb"

bd1_ca = read_ca_coords(pdb3, 'A')
bd2_ca = read_ca_coords(pdb5, 'A')

print(f"BD1 (3MXF): {len(bd1_ca)} CA atoms, residues {min(bd1_ca)}-{max(bd1_ca)}")
print(f"BD2 (5T35): {len(bd2_ca)} CA atoms, residues {min(bd2_ca)}-{max(bd2_ca)}")

# Find shared residue numbers for alignment (BD2 res 349-459, BD1 need mapping)
# BRD4 BD1 spans ~44-168 in canonical numbering used for isolated domain constructs
# BD2 spans 349-459. Both are ~111 residues.
# We'll align by sequential position (both have same fold)
bd1_res = sorted(bd1_ca.keys())
bd2_res = sorted(bd2_ca.keys())
print(f"\nBD1 residue range: {bd1_res[0]}-{bd1_res[-1]} ({len(bd1_res)} res)")
print(f"BD2 residue range: {bd2_res[0]}-{bd2_res[-1]} ({len(bd2_res)} res)")
n_align = min(len(bd1_res), len(bd2_res))
print(f"Aligning first {n_align} residues sequentially")
