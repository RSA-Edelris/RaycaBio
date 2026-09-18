
import os

# Walk new protacfold_out
for root, dirs, files in os.walk('protacfold_out'):
    for f in files:
        full = os.path.join(root, f)
        print(f"{full}  ({os.path.getsize(full)} bytes)")
