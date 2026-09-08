
import os, glob
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
for pat in ["phase_similarity*", "phase_experimental*", "similarity_inference*",
            "bx912_docking*", "chembl_activities*"]:
    for f in sorted(glob.glob(f"{WS}/{pat}")):
        print(f"{os.path.basename(f):55s} {os.path.getsize(f):>8,} bytes")
