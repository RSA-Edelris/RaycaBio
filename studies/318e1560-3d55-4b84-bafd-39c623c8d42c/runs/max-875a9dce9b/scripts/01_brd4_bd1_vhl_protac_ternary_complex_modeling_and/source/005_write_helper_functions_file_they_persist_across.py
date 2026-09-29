
# Write helper functions to file so they persist across calls
helpers = '''
import numpy as np

def read_ca_coords(path, chain_id):
    coords = {}
    with open(path) as f:
        for line in f:
            if line[:4] == "ATOM" and line[21] == chain_id and line[12:16].strip() == "CA":
                resnum = int(line[22:26])
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                coords[resnum] = np.array([x, y, z])
    return coords

def read_all_atom_coords(path, chain_id, record="ATOM"):
    atoms = []
    with open(path) as f:
        for line in f:
            rt = line[:6].strip()
            if rt == record and line[21] == chain_id:
                name = line[12:16].strip()
                resnum = int(line[22:26])
                resname = line[17:20].strip()
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                atoms.append((name, resnum, resname, np.array([x, y, z])))
    return atoms

def read_hetatm_ligand(path, chain_id, resname_filter=None):
    atoms = []
    with open(path) as f:
        for line in f:
            if line[:6].strip() == "HETATM" and line[21] == chain_id:
                rn = line[17:20].strip()
                if resname_filter and rn != resname_filter:
                    continue
                name = line[12:16].strip()
                resnum = int(line[22:26])
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                atoms.append((name, resnum, rn, np.array([x, y, z])))
    return atoms

def kabsch(mobile, target):
    """Return R, t such that mobile @ R.T + t ~= target. mobile/target: (N,3)."""
    mob_c = mobile.mean(axis=0)
    tgt_c = target.mean(axis=0)
    mob_ = mobile - mob_c
    tgt_ = target - tgt_c
    H = mob_.T @ tgt_
    U, S, Vt = np.linalg.svd(H)
    d = np.linalg.det(Vt.T @ U.T)
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    t = tgt_c - mob_c @ R.T
    return R, t

def apply_transform(coords_arr, R, t):
    return coords_arr @ R.T + t

def rmsd(a, b):
    return float(np.sqrt(np.mean(np.sum((a - b)**2, axis=1))))
'''

with open(work_dir / "helpers.py", "w") as f:
    f.write(helpers)
print("helpers.py written")
