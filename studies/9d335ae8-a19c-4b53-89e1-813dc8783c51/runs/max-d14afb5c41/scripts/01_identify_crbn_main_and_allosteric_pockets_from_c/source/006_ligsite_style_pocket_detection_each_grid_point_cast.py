
# ── LIGSITE-style pocket detection ───────────────────────────────────────────
# For each grid point cast 6 rays (+/-x,+/-y,+/-z); count directions that hit
# a protein atom within 10 Å. Points with ≥ 5 hits = buried cavity.

step = 1.5
ray_len = 10.0   # max ray distance in Å
hit_thresh = 5   # of 6 directions must hit protein

def ray_hits_protein(origin, direction, tree, ray_len, n_steps=12):
    """True if any point along the ray is within 1.6 Å of a protein atom."""
    step_sz = ray_len / n_steps
    for i in range(1, n_steps+1):
        pt = origin + direction * step_sz * i
        d, _ = tree.query(pt)
        if d < 1.6:
            return True
    return False

directions = np.array([
    [1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]], dtype=float)

# Use coarser grid for speed: 2 Å
step2 = 2.0
xs2 = np.arange(xmin, xmax, step2)
ys2 = np.arange(ymin, ymax, step2)
zs2 = np.arange(zmin, zmax, step2)
XX2,YY2,ZZ2 = np.meshgrid(xs2,ys2,zs2,indexing='ij')
grid2 = np.stack([XX2.ravel(),YY2.ravel(),ZZ2.ravel()],axis=1)
print(f"Coarse grid: {len(grid2):,} points")

# Pre-filter: only points 1.4-8.0 Å from nearest protein atom
nd2,_ = tree.query(grid2, k=1)
pre_mask = (nd2 > 1.4) & (nd2 < 8.0)
cand = grid2[pre_mask]
print(f"Candidates after pre-filter: {len(cand):,}")

# Ray casting for burial
n_hits = np.zeros(len(cand), dtype=int)
for i,d in enumerate(directions):
    # vectorised: check 12 steps along each ray
    for s in range(1, 13):
        pts = cand + d * (ray_len/12) * s
        dist_s, _ = tree.query(pts, k=1)
        hit = dist_s < 1.6
        n_hits += hit.astype(int)
        n_hits = np.minimum(n_hits, 6)   # cap per direction not needed but fast

pocket_mask = n_hits >= hit_thresh
pocket_pts  = cand[pocket_mask]
print(f"Pocket probe points (≥{hit_thresh}/6 ray hits): {len(pocket_pts):,}")
