
import numpy as np

# ---- Pockets from dpCDK2-CCNE1 analysis ----
# Main ATP pocket (chain A residue numbers)
atp_main = {
    15,17,18,30,31,32,33,34,35,46,47,48,49,50,51,52,53,54,55,56,
    58,63,64,65,66,67,76,77,78,79,80,81,82,83,84,85,86,89,
    118,123,125,126,127,128,129,132,134,135,136,137,
    142,143,144,145,146,147,148,149,150,
    158,163,164,165,172,173,175,176,177,178,179,180,
    185,233,234
}

# Interface pocket
iface_cdk2  = {116, 119, 120, 121, 122}      # chain A
iface_ccne1 = {90, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105}  # chain B

# CTX contact residues (from above)
ctx_cdk2  = {54, 57, 58, 121, 122, 123, 151, 152, 153}   # chain A
ctx_ccne1 = {90, 101, 102, 104, 105, 107, 108, 111, 149, 227, 228, 229, 233, 234, 237}  # chain B

# ---- Overlap vs ATP main pocket ----
overlap_atp  = ctx_cdk2 & atp_main
unique_ctx_vs_atp = ctx_cdk2 - atp_main
in_atp_not_ctx    = atp_main - ctx_cdk2

print("=== CTX pocket vs ATP-binding pocket (CDK2 chain A) ===")
print(f"  ATP main pocket size : {len(atp_main)} residues")
print(f"  CTX chain-A contacts : {len(ctx_cdk2)} residues")
print(f"  Overlap              : {len(overlap_atp)} residues  → {sorted(overlap_atp)}")
print(f"  CTX-only (not in ATP): {sorted(unique_ctx_vs_atp)}")
print(f"  Jaccard similarity   : {len(overlap_atp)/len(ctx_cdk2 | atp_main):.2f}")

# ---- Overlap vs interface pocket ----
overlap_iface_cdk2  = ctx_cdk2  & iface_cdk2
overlap_iface_ccne1 = ctx_ccne1 & iface_ccne1
total_iface = iface_cdk2 | iface_ccne1
total_ctx   = ctx_cdk2 | ctx_ccne1
total_overlap = overlap_iface_cdk2 | overlap_iface_ccne1

print("\n=== CTX pocket vs CDK2-CyclinE1 interface pocket ===")
print(f"  Interface pocket size    : {len(total_iface)} residues "
      f"({len(iface_cdk2)} CDK2 + {len(iface_ccne1)} CyclinE1)")
print(f"  CTX total contacts       : {len(total_ctx)} residues "
      f"({len(ctx_cdk2)} CDK2 + {len(ctx_ccne1)} CyclinE1)")
print(f"  Overlap CDK2 side        : {sorted(overlap_iface_cdk2)}")
print(f"  Overlap CyclinE1 side    : {sorted(overlap_iface_ccne1)}")
print(f"  Total shared             : {len(total_overlap)} residues")
print(f"  Jaccard similarity       : {len(total_overlap)/len(total_iface | total_ctx):.2f}")

# CTX centroid vs saved pocket centroids
ctx_cen = np.array([30.57, 5.37, -25.80])
atp_cen = np.array([31.96, 16.99, -10.69])   # from dpCDK2-CCNE1 analysis
tloop_cen_dist_from_atp = 23.3   # from earlier analysis

d_ctx_atp = np.linalg.norm(ctx_cen - atp_cen)
print(f"\nDistance: CTX centroid → ATP-site centroid : {d_ctx_atp:.1f} Å")
