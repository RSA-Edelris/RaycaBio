
import sys, pathlib
sys.path.insert(0, str(pathlib.Path("/home/ubuntu/rayca-sessions/318e1560-3d55-4b84-bafd-39c623c8d42c-c53814dd4ebb/brd4_vhl_protac")))

def kabsch(mobile, target):
    mob_c = mobile.mean(axis=0); tgt_c = target.mean(axis=0)
    mob_ = mobile - mob_c; tgt_ = target - tgt_c
    H = mob_.T @ tgt_
    U, S, Vt = np.linalg.svd(H)
    d = np.linalg.det(Vt.T @ U.T)
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    t = tgt_c - mob_c @ R.T
    return R, t

def apply_transform(coords, R, t):
    return coords @ R.T + t

def rmsd_fn(a, b):
    return float(np.sqrt(np.mean(np.sum((a - b)**2, axis=1))))

# BD1 has 127 res (42-168), BD2 has 111 (349-459) — skip 16 N-term residues of BD1
bd1_res_trim = bd1_res[16:]   # res 58-168, 111 residues
mobile_arr = np.array([bd1_ca[r] for r in bd1_res_trim])
target_arr = np.array([bd2_ca[r] for r in bd2_res])

R2, t2 = kabsch(mobile_arr, target_arr)
fit2 = apply_transform(mobile_arr, R2, t2)
print(f"BD1(58-168) → BD2 full 111 RMSD: {rmsd_fn(fit2, target_arr):.2f} Å")

# Iterative trimming
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

Rf, tf = kabsch(pm, pt)
ff = apply_transform(pm, Rf, tf)
core_rmsd = rmsd_fn(ff, pt)
print(f"Core RMSD after iterative trim: {core_rmsd:.2f} Å over {len(pm)} residues")
