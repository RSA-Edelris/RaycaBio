
import os, glob

# Find any log files written by this latest boltz run
for root, dirs, files in os.walk('.'):
    for f in files:
        full = os.path.join(root, f)
        if any(x in full for x in ['lightning_logs', 'boltz_results', '.log', 'version_']):
            size = os.path.getsize(full)
            print(f"{full}  ({size} b)")
