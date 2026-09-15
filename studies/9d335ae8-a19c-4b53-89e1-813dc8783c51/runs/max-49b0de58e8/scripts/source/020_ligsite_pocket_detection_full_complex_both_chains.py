
# ── LIGSITE pocket detection on full complex (both chains) ──────────────────
prot_coords = np.array([[a['x'],a['y'],a['z']] for a in protein])
tree = cKDTree(prot_coords)

pad, step = 5.0, 2.0
xmin,ymin,zmin = prot_coords.min(axis=0) - pad
xmax,ymax,zmax = prot_coords.max(axis=0) + pad
xs = np.arange(xmin,xmax,step); ys = np.arange(ymin,ymax,step); zs = np.arange(zmin,zmax,step)
XX,YY,ZZ = np.meshgrid(xs,ys,zs,indexing='ij')
grid = np.stack([XX.ravel(),YY.ravel(),ZZ.ravel()],axis=1)

nd, _ = tree.query(grid, k=1)
pre = (nd > 1.4) & (nd < 8.0)
cand = grid[pre]
print(f"Candidates: {len(cand):,}")

# 6-ray burial test
ray_len = 10.0
directions = np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],dtype=float)
n_dirs = np.zeros(len(cand),dtype=int)
for d in directions:
    hit = np.zeros(len(cand),dtype=bool)
    for s in range(1,13):
        pts = cand + d*(ray_len/12)*s
        dist_s,_ = tree.query(pts,k=1)
        hit |= (dist_s < 1.6)
    n_dirs += hit.astype(int)

deep = cand[n_dirs==6]
print(f"Deep buried (6/6): {len(deep):,}")

# Cluster
db = DBSCAN(eps=2.5, min_samples=3, n_jobs=-1).fit(deep)
labs = db.labels_
n_cl = len(set(labs))-(1 if -1 in labs else 0)
print(f"Clusters: {n_cl}")

clusters = []
for cl in set(labs):
    if cl==-1: continue
    m = labs==cl
    pts = deep[m]
    clusters.append(dict(id=cl, n=m.sum(), centroid=pts.mean(axis=0), pts=pts))
clusters.sort(key=lambda x:-x['n'])

print(f"\nTop 12 clusters:")
for c in clusters[:12]:
    print(f"  Cl {c['id']:3d}: {c['n']:4d} pts  cen=({c['centroid'][0]:.1f},{c['centroid'][1]:.1f},{c['centroid'][2]:.1f})")
