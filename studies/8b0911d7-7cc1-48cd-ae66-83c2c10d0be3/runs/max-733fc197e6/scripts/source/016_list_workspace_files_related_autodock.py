
import os

# List workspace files related to autodock
workspace = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc'
for f in os.listdir(workspace):
    if 'autodock' in f.lower() or 'vina' in f.lower() or 'dock' in f.lower():
        fpath = os.path.join(workspace, f)
        print(f, os.path.getsize(fpath))
