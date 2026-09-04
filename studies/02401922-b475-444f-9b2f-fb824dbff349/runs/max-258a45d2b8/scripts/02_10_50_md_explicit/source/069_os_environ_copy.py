
import subprocess, os

wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
amber_home = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
env = os.environ.copy()
env['AMBERHOME'] = amber_home
python  = f"{amber_home}/bin/python"
mmpbsa  = f"{amber_home}/bin/MMPBSA.py"

# Check if minimized structure exists
import os
for f in ['complex_min.rst7', 'min.out']:
    if os.path.exists(f'{wd}/{f}'):
        sz = os.path.getsize(f'{wd}/{f}')
        print(f"{f}: {sz} bytes")
    else:
        print(f"{f}: NOT FOUND")
