
import subprocess, json, os

WORKDIR = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc'
script  = os.path.join(WORKDIR, 'prep_ligands.py')

r = subprocess.run(['python3', script], capture_output=True, text=True, cwd=WORKDIR)
print(r.stdout[-3000:])
if r.returncode != 0:
    print("STDERR:", r.stderr[-1000:])
