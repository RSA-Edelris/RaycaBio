
# ── Cluster probe points with DBSCAN (eps=3 Å, min_samples=5) ───────────────
from sklearn.cluster import DBSCAN

db = DBSCAN(eps=3.0, min_samples=5, n_jobs=-1).fit(probe_coords)
labels = db.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
print(f"DBSCAN clusters found: {n_clusters}")

# Score each cluster by size and characterise by its centroid
cluster_info = []
for cl in range(n_clusters):
    mask = labels == cl
    pts  = probe_coords[mask]
    cen  = pts.mean(axis=0)
    cluster_info.append(dict(id=cl, n=mask.sum(), centroid=cen))

cluster_info.sort(key=lambda x: -x['n'])
print(f"\nTop clusters (size, centroid):")
for c in cluster_info[:10]:
    print(f"  Cluster {c['id']:3d}: {c['n']:5d} pts  centroid=({c['centroid'][0]:.1f},{c['centroid'][1]:.1f},{c['centroid'][2]:.1f})")

# Distance from each cluster centroid to LVY centroid and ZN
lvy_cen = np.array([84.80015789, 154.93652632, 13.24152632])
zn_pos  = np.array([75.756, 152.112, 31.429])
print("\nDistance to LVY centroid and ZN site for top 10 clusters:")
for c in cluster_info[:10]:
    d_lvy = np.linalg.norm(c['centroid'] - lvy_cen)
    d_zn  = np.linalg.norm(c['centroid'] - zn_pos)
    print(f"  Cluster {c['id']:3d}: d_LVY={d_lvy:.1f} Å  d_ZN={d_zn:.1f} Å  ({c['n']:5d} pts)")
