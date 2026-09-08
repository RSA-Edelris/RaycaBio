
import os, glob
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
# Check phase report was written
reports = sorted(glob.glob(f"{WS}/phase_similarity*.md") + glob.glob(f"{WS}/*inference*.md"))
for f in reports:
    print(f"{os.path.basename(f)}: {os.path.getsize(f)} bytes")
