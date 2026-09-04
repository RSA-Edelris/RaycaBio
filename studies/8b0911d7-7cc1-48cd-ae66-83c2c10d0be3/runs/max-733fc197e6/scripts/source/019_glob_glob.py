
import os, glob

workspace = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc'

# Check for any pdbqt files
pdbqts = glob.glob(os.path.join(workspace, '**/*.pdbqt'), recursive=True)
print('pdbqt files:', pdbqts)

# Check /work directory
work_exists = os.path.exists('/work')
print('/work exists:', work_exists)
if work_exists:
    for root, dirs, files in os.walk('/work'):
        for f in files:
            if 'pdbqt' in f.lower() or 'vina' in f.lower():
                print(os.path.join(root, f))

# Use first run data (better affinity -7.0)
import json
with open(os.path.join(workspace, 'autodock-vina-results.json')) as f:
    run1 = json.load(f)
print('\nRun 1 data:', json.dumps(run1, indent=2))
