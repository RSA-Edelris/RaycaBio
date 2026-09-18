
import os, glob
# Quick targeted checks
for p in ['/data', '/mnt', '/scratch', '/tmp']:
    if os.path.exists(p):
        try:
            items = os.listdir(p)[:20]
            print(f"{p}: {items}")
        except Exception as e:
            print(f"{p}: {e}")
