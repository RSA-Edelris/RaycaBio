
# Verify the cartoon image exists and recap pocket residues from session state
import os

files = [
    "/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8/CDK2_CCNE1_cartoon_pockets.png",
    "/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8/CDK2_CCNE1_pocket_analysis.md",
]
for f in files:
    print(f, "→", "EXISTS" if os.path.exists(f) else "MISSING", os.path.getsize(f) if os.path.exists(f) else "")
