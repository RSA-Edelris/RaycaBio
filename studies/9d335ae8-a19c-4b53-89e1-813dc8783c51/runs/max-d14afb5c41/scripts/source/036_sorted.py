
import os, glob
base = '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8'
scripts = sorted(glob.glob(os.path.join(base, '0*.py')))
for s in scripts[-10:]:
    print(os.path.basename(s), os.path.getsize(s))
