
import os, glob

# Check results directory for any gnina output
wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'
for root, dirs, files in os.walk(wd):
    for f in files:
        path = os.path.join(root, f)
        sz = os.path.getsize(path)
        print(f"  {path[len(wd):]:<55} {sz:>10,}")
