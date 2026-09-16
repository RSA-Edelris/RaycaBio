
from rdkit.ML.Cluster import Butina

# Butina needs a 1D condensed distance list (upper triangle, row by row)
dists = []
for i in range(1, n):
    for j in range(i):
        dists.append(1.0 - sim_matrix[i][j])

# Cluster at Tanimoto >= 0.40 (distance cutoff = 0.60)
clusters_60 = Butina.ClusterData(dists, n, 0.60, isDistData=True)
# Cluster at Tanimoto >= 0.50 (distance cutoff = 0.50) — tighter
clusters_50 = Butina.ClusterData(dists, n, 0.50, isDistData=True)

def report_clusters(clusters, cutoff_name):
    print(f"\n=== Butina clustering (Tanimoto ≥ {1-cutoff_name:.2f}, distance ≤ {cutoff_name:.2f}) ===")
    for ci, cl in enumerate(clusters):
        members = [results[i] for i in cl]
        print(f"\nCluster {ci+1} ({len(cl)} members):")
        for m in members:
            br = float(m['Avg BR'])
            ar = float(m['AS ratio'])
            print(f"  {m['EDS_Number']} | Avg BR={br:.4f} | AS ratio={ar:.4f} | rank={m['Hit_rank']} | "
                  f"MW={m['pc']['MW']:.0f} | cLogP={m['pc']['cLogP']:.2f} | "
                  f"PAINS={m['pains'][:30]} | "
                  f"SMILES={m['std_smi'][:80]}")

report_clusters(clusters_50, 0.50)
report_clusters(clusters_60, 0.60)
