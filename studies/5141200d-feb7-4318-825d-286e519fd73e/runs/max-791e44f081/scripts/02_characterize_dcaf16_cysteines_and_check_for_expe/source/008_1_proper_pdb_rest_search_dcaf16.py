
import urllib.request, json, numpy as np

# ── 1. Proper PDB REST search for DCAF16 ────────────────────────────────────
pdb_query = {
    "query": {
        "type": "group",
        "logical_operator": "and",
        "nodes": [{
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_polymer_entity.pdbx_description",
                "operator": "contains_words",
                "value": "DCAF16"
            }
        }]
    },
    "return_type": "entry",
    "request_options": {"return_all_hits": True}
}
url = "https://search.rcsb.org/rcsbsearch/v2/query"
req = urllib.request.Request(url,
        data=json.dumps(pdb_query).encode(),
        headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read().decode())
    ids = [h["identifier"] for h in result.get("result_set", [])]
    print(f"Experimental DCAF16 PDB entries: {len(ids)} → {ids}")
except Exception as e:
    print(f"PDB search error: {e}")

# ── 2. Ternary complex geometry: model the reach requirement ─────────────────
# 
# Strategy: given BI-7273 exposed atoms on BRD9, compute what linker length and
# direction would be needed to reach DCAF16 C173/177/178/179.
# We model this by:
#  (a) choosing the best attachment atom on BI-7273 (most exposed, good chemistry)
#  (b) sampling DCAF16 orientations that place a reactive cysteine near a warhead
#      appended to BI-7273, subject to no steric clash with BRD9
#  (c) reporting the range of viable geometries

# Best attachment atoms (most exposed, heteroatoms or ring C accessible to derivatization)
# From earlier: N15, C25, C14, C16 have 0 protein contacts
# O22 and O23 are oxygens already in the scaffold – harder to functionalize
# N15 is an NH → ideal for acylation/alkylation to attach electrophilic linker
# C25 is an aromatic/aliphatic C with 0 contacts → could add a substituent here

# BI-7273 structure (5SW): it's a naphthyridine/quinoline-based compound.
# In the PDB CCD, 5SW is the BRD9 inhibitor BI-7273.
# N15 at (3.54, -1.78, 5.20) is most likely the indazole NH → primary attachment point
# C25 at (2.07, -1.73, 5.32) is further out, 0 contacts → terminal position

# Let's define "warhead point" as C25 + 3*outward_vector 
# (representing a ~3Å linker + warhead atom)
c25 = np.array([2.07, -1.73, 5.32])
c25_outward = np.array([-0.808, -0.586, -0.054])  # normalized outward vector

# Linker lengths to explore: 3-9 Å (1-3 bond lengths of linker)
print("\nWarhead position as function of linker length from C25:")
warhead_positions = {}
for L in [3, 5, 7, 9, 12]:
    wp = c25 + L * c25_outward
    warhead_positions[L] = wp
    print(f"  Linker={L:2d}Å  warhead=({wp[0]:6.2f},{wp[1]:6.2f},{wp[2]:6.2f})")

# ── 3. Cysteine cluster geometry (DCAF16 C173/177/178/179) ──────────────────
# Get coordinates
cys_cluster = {c["resseq"]: np.array([c["x"],c["y"],c["z"]]) for c in cys_records
               if c["resseq"] in (173,177,178,179)}
print("\nDCAF16 cysteine cluster (C173/177/178/179) positions:")
for r, xyz in sorted(cys_cluster.items()):
    print(f"  C{r}: ({xyz[0]:.2f},{xyz[1]:.2f},{xyz[2]:.2f})")

cys_centroid = np.mean(list(cys_cluster.values()), axis=0)
print(f"  Cluster centroid: ({cys_centroid[0]:.2f},{cys_centroid[1]:.2f},{cys_centroid[2]:.2f})")

# Pairwise distances within cluster
print("\nIntra-cluster Cα–Cα distances:")
res_sorted = sorted(cys_cluster.keys())
for i, r1 in enumerate(res_sorted):
    for r2 in res_sorted[i+1:]:
        d = np.linalg.norm(cys_cluster[r1]-cys_cluster[r2])
        print(f"  C{r1}–C{r2}: {d:.1f} Å")

# ── 4. What BRD9 surface looks like near the exposed vectors ─────────────────
# Find BRD9 surface atoms near each exposed BI-7273 atom (atoms with few contacts)
# to characterize the exit vector cavity

# BRD9 CA atoms
brd9_ca = [a for a in brd9_atoms if a["name"]=="CA"]
print(f"\nBRD9 has {len(brd9_ca)} Cα atoms")

# For C25 specifically, find the nearest BRD9 residues (potential interface residues)
c25_xyz = np.array([2.07, -1.73, 5.32])
brd9_ca_xyz = np.array([[a["x"],a["y"],a["z"]] for a in brd9_ca])
dists_c25 = np.linalg.norm(brd9_ca_xyz - c25_xyz, axis=1)
nearest_idx = np.argsort(dists_c25)[:8]
print(f"BRD9 residues nearest to C25 (attachment point):")
for i in nearest_idx:
    print(f"  {brd9_ca[i]['resname']}{brd9_ca[i]['resseq']:4d}  dist={dists_c25[i]:.1f}Å")
