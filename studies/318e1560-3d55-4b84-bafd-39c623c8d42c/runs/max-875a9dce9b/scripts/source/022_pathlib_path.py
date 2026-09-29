
import numpy as np
import pathlib

session_dir = pathlib.Path("/home/ubuntu/rayca-sessions/318e1560-3d55-4b84-bafd-39c623c8d42c-c53814dd4ebb")
work_dir = session_dir / "brd4_vhl_protac"
pdb3 = work_dir / "3MXF.pdb"
pdb5 = work_dir / "5T35.pdb"

def read_ca_coords(path, chain_id):
    coords = {}
    with open(path) as f:
        for line in f:
            if line[:4] == "ATOM" and line[21] == chain_id and line[12:16].strip() == "CA":
                resnum = int(line[22:26])
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                coords[resnum] = np.array([x, y, z])
    return coords

def kabsch(mobile, target):
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

bd1_ca = read_ca_coords(pdb3, 'A')
bd2_ca = read_ca_coords(pdb5, 'A')
bd1_res = sorted(bd1_ca.keys())
bd2_res = sorted(bd2_ca.keys())
print(f"BD1 residues: {bd1_res[0]}-{bd1_res[-1]} ({len(bd1_res)} res)")
print(f"BD2 residues: {bd2_res[0]}-{bd2_res[-1]} ({len(bd2_res)} res)")

# Replicate script 008: trim 16 from BD1, iterative kabsch
bd1_res_trim = bd1_res[16:]
mobile_arr = np.array([bd1_ca[r] for r in bd1_res_trim])
target_arr = np.array([bd2_ca[r] for r in bd2_res])

pm, pt = mobile_arr.copy(), target_arr.copy()
for i in range(10):
    Ri, ti = kabsch(pm, pt)
    fi = apply_transform(pm, Ri, ti)
    dists = np.sqrt(np.sum((fi - pt)**2, axis=1))
    cutoff = dists.mean() + 2*dists.std()
    keep = dists <= cutoff
    if keep.all():
        break
    pm, pt = pm[keep], pt[keep]

Rf_008, tf_008 = kabsch(pm, pt)
ff = apply_transform(pm, Rf_008, tf_008)
core_rmsd_008 = rmsd(ff, pt)
print(f"\nScript 008 approach (sequential trim): Core RMSD = {core_rmsd_008:.2f} Å over {len(pm)} residues")
