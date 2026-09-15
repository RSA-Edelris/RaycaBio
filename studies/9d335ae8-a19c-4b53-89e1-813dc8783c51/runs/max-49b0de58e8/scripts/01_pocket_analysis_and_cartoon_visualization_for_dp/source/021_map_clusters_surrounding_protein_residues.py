
# ── Map clusters to surrounding protein residues ────────────────────────────
def cluster_residues(pts, protein_atoms, cutoff=5.0):
    ptree = cKDTree(pts)
    res_set = {}
    for pa in protein_atoms:
        d,_ = ptree.query([pa['x'],pa['y'],pa['z']])
        if d <= cutoff:
            res_set[(pa['chain'], pa['resseq'], pa['resname'])] = True
    return sorted(res_set.keys())

# Check top clusters and a few small ones
focus = [1, 4, 14, 11, 26, 10]
for cid in focus:
    c = next((x for x in clusters if x['id']==cid), None)
    if not c: continue
    res = cluster_residues(c['pts'], protein)
    print(f"\n=== Cluster {cid} ({c['n']} pts) cen=({c['centroid'][0]:.1f},{c['centroid'][1]:.1f},{c['centroid'][2]:.1f}) ===")
    for ch,rseq,rname in res:
        print(f"  [{ch}] {rname:3s} {rseq}")
