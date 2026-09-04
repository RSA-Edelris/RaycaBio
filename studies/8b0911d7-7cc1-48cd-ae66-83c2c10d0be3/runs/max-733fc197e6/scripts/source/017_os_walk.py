
import os, glob

workspace = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc'

# List all files in workspace including subdirs
for root, dirs, files in os.walk(workspace):
    # Skip hidden dirs
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in files:
        fpath = os.path.join(root, f)
        print(fpath, os.path.getsize(fpath))
