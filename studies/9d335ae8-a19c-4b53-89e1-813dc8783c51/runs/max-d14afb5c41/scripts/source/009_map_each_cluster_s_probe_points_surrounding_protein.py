
# ── Map each cluster's probe points to surrounding protein residues (≤5 Å) ──
from collections import defaultdict

# We'll characterise the top 5 distinct clusters by their residue composition
# Skip tiny clusters (<5 pts) and noise

def cluster_residues(pts, protein, cutoff=5.0):
    """Return sorted list of (resseq, resname) within cutoff of any probe point."""
    ptree = cKDTree(pts)
    res_set = {}
    for pa in protein:
        pa_xyz = np.array([pa['x'],pa['y'],pa['z']])
        d, _ = ptree.query(pa_xyz)
        if d <= cutoff:
            key = (pa['resseq'], pa['resname'])
            res_set[key] = True
    return sorted(res_set.keys())

# Focus on cluster 23 (closest to LVY), cluster 27, cluster 29
# and clusters near ZN (25, 28)
focus_ids = [23, 27, 29, 25, 28, 0]
focus_cls = {c['id']: c for c in clusters3 if c['id'] in focus_ids}

for cid in focus_ids:
    if cid not in focus_cls:
        print(f"Cluster {cid} not found"); continue
    c = focus_cls[cid]
    res = cluster_residues(c['pts'], protein, cutoff=5.0)
    d_lvy = np.linalg.norm(c['centroid'] - lvy_cen)
    d_zn  = np.linalg.norm(c['centroid'] - zn_pos)
    print(f"\n=== Cluster {cid} ({c['n']} pts, d_LVY={d_lvy:.1f} Å, d_ZN={d_zn:.1f} Å) ===")
    for rseq, rname in res:
        print(f"  {rname:3s} {rseq}")
