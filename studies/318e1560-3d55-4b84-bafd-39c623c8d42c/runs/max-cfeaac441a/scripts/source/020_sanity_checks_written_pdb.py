
# Sanity checks on the written PDB
out_pdb = work_dir / "BRD4BD1_VHL_ternary_model.pdb"

def chain_ca_centroid(path, chain_id):
    coords = []
    with open(path) as f:
        for line in f:
            if line[:4] == "ATOM" and line[21] == chain_id and line[12:16].strip() == "CA":
                coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return np.array(coords)

# Centroids from ternary model PDB
cen_bd1 = chain_ca_centroid(out_pdb, 'A').mean(axis=0)
cen_vhl = chain_ca_centroid(out_pdb, 'B').mean(axis=0)
cen_elc = chain_ca_centroid(out_pdb, 'C').mean(axis=0)
cen_elb = chain_ca_centroid(out_pdb, 'D').mean(axis=0)

# Reference centroids from 5T35
def chain_ca_centroid_raw(path, chain_id):
    coords = []
    with open(path) as f:
        for line in f:
            if line[:4] == "ATOM" and line[21] == chain_id and line[12:16].strip() == "CA":
                coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return np.array(coords)

cen_bd2_ref = chain_ca_centroid_raw(pdb5, 'A').mean(axis=0)  # BD2 reference
cen_vhl_ref = chain_ca_centroid_raw(pdb5, 'D').mean(axis=0)
cen_elc_ref = chain_ca_centroid_raw(pdb5, 'C').mean(axis=0)
cen_elb_ref = chain_ca_centroid_raw(pdb5, 'B').mean(axis=0)

print("Centroid displacement (model vs 5T35 reference):")
print(f"  BD1 (A) vs BD2 (5T35-A): {np.linalg.norm(cen_bd1 - cen_bd2_ref):.2f} Å  "
      f"← small = good superposition")
print(f"  VHL (B) vs VHL (5T35-D): {np.linalg.norm(cen_vhl - cen_vhl_ref):.2f} Å  "
      f"← should be 0 (copied verbatim)")
print(f"  ElonginC (C) vs 5T35-C:  {np.linalg.norm(cen_elc - cen_elc_ref):.2f} Å")
print(f"  ElonginB (D) vs 5T35-B:  {np.linalg.norm(cen_elb - cen_elb_ref):.2f} Å")

print(f"\nInter-chain centroid distances in ternary model:")
print(f"  BD1–VHL:       {np.linalg.norm(cen_bd1 - cen_vhl):.1f} Å")
print(f"  BD1–ElonginC:  {np.linalg.norm(cen_bd1 - cen_elc):.1f} Å")
print(f"  BD1–ElonginB:  {np.linalg.norm(cen_bd1 - cen_elb):.1f} Å")
print(f"  VHL–ElonginC:  {np.linalg.norm(cen_vhl - cen_elc):.1f} Å")

# Count atoms per chain
from collections import Counter
chain_counts = Counter()
with open(out_pdb) as f:
    for line in f:
        if line[:4] in ("ATOM","HETA"):
            chain_counts[line[21]] += 1
print(f"\nAtom counts per chain: {dict(chain_counts)}")
print(f"\nFile size: {out_pdb.stat().st_size:,} bytes")
print(f"Path: {out_pdb}")
