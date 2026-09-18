
import os
# Check harbor directory
for root, dirs, files in os.walk('/data/harbor', topdown=True):
    # Limit depth
    depth = root.replace('/data/harbor', '').count(os.sep)
    if depth > 2:
        dirs[:] = []
        continue
    for f in files[:5]:
        print(os.path.join(root, f))
    if dirs:
        print(f"  dirs: {dirs[:10]}")
