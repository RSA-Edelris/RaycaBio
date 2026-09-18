
import os

# Walk the protacfold_out directory
for root, dirs, files in os.walk('protacfold_out'):
    for f in files:
        full = os.path.join(root, f)
        size = os.path.getsize(full)
        print(f"{full}  ({size} bytes)")
