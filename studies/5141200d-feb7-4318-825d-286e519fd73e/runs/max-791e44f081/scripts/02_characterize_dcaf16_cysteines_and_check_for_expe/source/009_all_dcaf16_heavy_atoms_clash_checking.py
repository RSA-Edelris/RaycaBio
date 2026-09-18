
import numpy as np

# ── All DCAF16 heavy atoms (for clash checking) ──────────────────────────────
dcaf_all_xyz = np.array([[a["x"],a["y"],a["z"]] for a in af_atoms])
brd9_all_xyz = np.array([[a["x"],a["y"],a["z"]] for a in brd9_atoms])

# ── Get SG (sulfur) coords for the cysteine cluster ──────────────────────────
cys_sg = {}
for line in af_text.splitlines():
    if line.startswith("ATOM"):
        aname  = line[12:16].strip()
        resseq = int(line[22:26])
        resname= line[17:20].strip()
        if resname == "CYS" and aname == "SG":
            cys_sg[resseq] = np.array([float(line[30:38]),
                                       float(line[38:46]),
                                       float(line[46:54])])

print("Cys SG positions (DCAF16 AF frame):")
for r, xyz in sorted(cys_sg.items()):
    print(f"  C{r} SG: ({xyz[0]:.2f},{xyz[1]:.2f},{xyz[2]:.2f})")

# ── Warhead positions (5EU1 frame, extending from C25) ───────────────────────
c25     = np.array([2.07, -1.73, 5.32])
c25_out = np.array([-0.808, -0.586, -0.054])

results = []
print("\n=== Ternary geometry scan ===")
print(f"{'Linker':>7}  {'CYS':>5}  {'Clashes':>8}  {'IntfAts':>9}  {'IntfArea_est':>13}  Verdict")

for L in [5, 7, 9, 12]:
    warhead = c25 + L * c25_out          # warhead electrophilic carbon
    
    for cys_res in [177, 178, 179, 173]:  # try each candidate cysteine
        if cys_res not in cys_sg:
            continue
        sg_orig = cys_sg[cys_res]
        
        # Translation that brings this SG onto the warhead position
        T = warhead - sg_orig
        
        # Translate all DCAF16 atoms
        dcaf_T = dcaf_all_xyz + T
        
        # Clash check: DCAF16 atoms within 2.5Å of any BRD9 atom
        # (vectorised pairwise – manageable sizes: ~1700 × ~920)
        # Use broadcasting in chunks to avoid memory issues
        n_clashes = 0
        chunk = 200
        for i in range(0, len(dcaf_T), chunk):
            D = np.linalg.norm(
                dcaf_T[i:i+chunk, None, :] - brd9_all_xyz[None, :, :], axis=2)
            n_clashes += int((D < 2.5).any(axis=1).sum())
        
        # Interface atom count: DCAF16 atoms within 5Å of BRD9
        n_intf = 0
        for i in range(0, len(dcaf_T), chunk):
            D = np.linalg.norm(
                dcaf_T[i:i+chunk, None, :] - brd9_all_xyz[None, :, :], axis=2)
            n_intf += int((D < 5.0).any(axis=1).sum())
        
        # Rough buried surface estimate: ~15 Å² per interface atom
        intf_area = n_intf * 15
        
        verdict = ("CLASH" if n_clashes > 30 else
                   "marginal" if n_clashes > 5 else
                   "OK" if n_intf > 20 else "sparse")
        
        print(f"  {L:5d}Å   C{cys_res:3d}  {n_clashes:8d}  {n_intf:9d}  {intf_area:10d} Å²  {verdict}")
        results.append(dict(L=L, cys=cys_res, clashes=n_clashes,
                            intf_atoms=n_intf, intf_area=intf_area, T=T))
