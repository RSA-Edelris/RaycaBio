
import numpy as np

# ── Helper: local window clash check ─────────────────────────────────────────
# Only residues cys_res ± WINDOW are physically constrained at the approach site.
WINDOW = 12   # residues on each side

def local_clash_check(cys_res, sg_target, brd9_xyz, dcaf_atoms_list, window=WINDOW,
                      clash_d=2.5, intf_d=5.0, n_rot=24):
    """
    Translate DCAF16 local window onto sg_target, then rotate around the
    approach axis in n_rot steps.  Return best (min-clash) rotation result.
    """
    # Select local window atoms
    local_atoms = [a for a in dcaf_atoms_list
                   if abs(a["resseq"] - cys_res) <= window]
    if not local_atoms:
        return None
    local_xyz = np.array([[a["x"],a["y"],a["z"]] for a in local_atoms])
    
    # SG original position
    sg_orig = np.array([a["x"] for a in local_atoms if a["name"]=="SG" and a["resseq"]==cys_res] +
                       [a["y"] for a in local_atoms if a["name"]=="SG" and a["resseq"]==cys_res] +
                       [a["z"] for a in local_atoms if a["name"]=="SG" and a["resseq"]==cys_res])
    # Rebuild properly
    for a in local_atoms:
        if a["name"] == "SG" and a["resseq"] == cys_res:
            sg_orig = np.array([a["x"],a["y"],a["z"]]); break
    
    # Approach axis = outward direction from BRD9 (same as warhead direction)
    approach_axis = np.array([-0.808, -0.586, -0.054])  # C25 outward vector
    
    best = {"clashes": 999999, "intf_atoms": 0, "theta": 0}
    
    for i in range(n_rot):
        theta = 2 * np.pi * i / n_rot
        # Rotation matrix around approach_axis by theta (Rodrigues)
        u = approach_axis
        K = np.array([[  0,  -u[2],  u[1]],
                      [ u[2],   0, -u[0]],
                      [-u[1],  u[0],   0]])
        R = np.eye(3) + np.sin(theta)*K + (1-np.cos(theta))*(K @ K)
        
        # Rotate local_xyz around sg_orig, then translate to sg_target
        centered = local_xyz - sg_orig
        rotated  = (R @ centered.T).T
        placed   = rotated + sg_target
        
        # Clash and interface
        n_cl = 0; n_if = 0
        chunk = 200
        for j in range(0, len(placed), chunk):
            D = np.linalg.norm(placed[j:j+chunk,None,:] - brd9_xyz[None,:,:], axis=2)
            n_cl += int((D < clash_d).any(axis=1).sum())
            n_if += int((D < intf_d).any(axis=1).sum())
        
        if n_cl < best["clashes"]:
            best = {"clashes": n_cl, "intf_atoms": n_if,
                    "intf_area": n_if*15, "theta_deg": np.degrees(theta)}
    
    best["n_local_atoms"] = len(local_atoms)
    return best

# ── Scan: linker lengths × cysteines (local window + rotation) ───────────────
c25     = np.array([2.07, -1.73, 5.32])
c25_out = np.array([-0.808, -0.586, -0.054])

print(f"Local window ±{WINDOW} residues, 24 rotations around approach axis")
print(f"{'Linker':>7}  {'CYS':>5}  {'BestClash':>10}  {'IntfAts':>9}  {'IntfArea':>10}  {'BestTheta':>11}  Verdict")

scan_results = []
for L in [5, 7, 9, 12, 15]:
    warhead = c25 + L * c25_out
    for cys_res in [177, 178, 179, 173, 58]:
        if cys_res not in cys_sg:
            continue
        r = local_clash_check(cys_res, warhead, brd9_all_xyz, af_atoms, window=WINDOW)
        if r is None: continue
        v = ("clean" if r["clashes"]==0 else
             "OK"    if r["clashes"]<=3 else
             "marginal" if r["clashes"]<=10 else "CLASH")
        print(f"  {L:5d}Å   C{cys_res:3d}  {r['clashes']:10d}  "
              f"{r['intf_atoms']:9d}  {r['intf_area']:8d}Å²  "
              f"{r['theta_deg']:9.1f}°  {v}")
        scan_results.append(dict(L=L, cys=cys_res, **r))
