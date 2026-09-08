
import os, glob, json

ART = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# Find all relevant files
gbsa_jsons = sorted(glob.glob(f"{ART}/gbsa_*.json"))
pose_sdfs  = sorted(glob.glob(f"{ART}/all_poses/*_pose*.sdf"))
best_sdfs  = sorted(glob.glob(f"{ART}/all_poses/*_best.sdf"))

print("GBSA JSONs:", gbsa_jsons)
print("\nAll-poses dir:", sorted(glob.glob(f"{ART}/all_poses/*.sdf"))[:20])
print("\nOther SDFs:", sorted(glob.glob(f"{ART}/*.sdf")))
print("\nOther key files:", [f for f in sorted(glob.glob(f"{ART}/*")) if os.path.isfile(f) and not f.endswith('.py')][:30])
