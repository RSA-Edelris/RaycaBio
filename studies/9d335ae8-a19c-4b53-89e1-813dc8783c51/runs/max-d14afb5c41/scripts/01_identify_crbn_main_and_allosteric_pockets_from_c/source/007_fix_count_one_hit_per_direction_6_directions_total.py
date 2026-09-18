
# ── Fix: count ONE hit per direction (6 directions total) ────────────────────
n_dirs = np.zeros(len(cand), dtype=int)
for i, d in enumerate(directions):
    dir_hit = np.zeros(len(cand), dtype=bool)
    for s in range(1, 13):
        pts = cand + d * (ray_len / 12) * s
        dist_s, _ = tree.query(pts, k=1)
        dir_hit |= (dist_s < 1.6)
    n_dirs += dir_hit.astype(int)

pocket_mask = n_dirs >= 5        # ≥5 of 6 directions blocked → buried
pocket_pts  = cand[pocket_mask]
print(f"Pocket probe points (≥5/6 directions blocked): {len(pocket_pts):,}")

# ── Cluster with DBSCAN ──────────────────────────────────────────────────────
db2 = DBSCAN(eps=3.5, min_samples=4, n_jobs=-1).fit(pocket_pts)
labs2 = db2.labels_
n_cl2 = len(set(labs2)) - (1 if -1 in labs2 else 0)
print(f"Clusters: {n_cl2}")

cluster_info2 = []
for cl in set(labs2):
    if cl == -1: continue
    mask = labs2 == cl
    pts  = pocket_pts[mask]
    cen  = pts.mean(axis=0)
    cluster_info2.append(dict(id=cl, n=mask.sum(), centroid=cen))
cluster_info2.sort(key=lambda x: -x['n'])

lvy_cen = np.array([84.80015789, 154.93652632, 13.24152632])
zn_pos  = np.array([75.756, 152.112, 31.429])

print(f"\nTop clusters — d_LVY, d_ZN:")
for c in cluster_info2[:12]:
    d_lvy = np.linalg.norm(c['centroid'] - lvy_cen)
    d_zn  = np.linalg.norm(c['centroid'] - zn_pos)
    print(f"  Cl {c['id']:3d}: {c['n']:4d} pts  cen=({c['centroid'][0]:.1f},{c['centroid'][1]:.1f},{c['centroid'][2]:.1f})"
          f"  d_LVY={d_lvy:.1f}  d_ZN={d_zn:.1f}")
