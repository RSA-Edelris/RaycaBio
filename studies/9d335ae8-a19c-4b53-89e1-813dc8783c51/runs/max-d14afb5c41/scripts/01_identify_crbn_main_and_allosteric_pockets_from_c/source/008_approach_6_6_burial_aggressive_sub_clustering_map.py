
# ── Approach: 6/6 burial + aggressive sub-clustering ─────────────────────────
# Then map each cluster to its surrounding protein residues

# All-6-directions blocked = deepest buried points only
deep_mask = n_dirs == 6
deep_pts  = cand[deep_mask]
print(f"Deep buried points (6/6 directions): {len(deep_pts):,}")

# Tighter DBSCAN
db3 = DBSCAN(eps=2.5, min_samples=3, n_jobs=-1).fit(deep_pts)
labs3 = db3.labels_
n_cl3 = len(set(labs3)) - (1 if -1 in labs3 else 0)
print(f"Clusters (eps=2.5): {n_cl3}")

clusters3 = []
for cl in set(labs3):
    if cl == -1: continue
    mask = labs3 == cl
    pts  = deep_pts[mask]
    cen  = pts.mean(axis=0)
    clusters3.append(dict(id=cl, n=mask.sum(), centroid=cen, pts=pts))
clusters3.sort(key=lambda x: -x['n'])

print(f"\nAll clusters with size and distance to LVY / ZN:")
for c in clusters3:
    d_lvy = np.linalg.norm(c['centroid'] - lvy_cen)
    d_zn  = np.linalg.norm(c['centroid'] - zn_pos)
    print(f"  Cl {c['id']:3d}: {c['n']:4d} pts  "
          f"cen=({c['centroid'][0]:.1f},{c['centroid'][1]:.1f},{c['centroid'][2]:.1f})  "
          f"d_LVY={d_lvy:.1f}  d_ZN={d_zn:.1f}")
