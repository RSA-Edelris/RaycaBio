
import os, glob

# Search for pdbqt files in and around WORKDIR
print("WORKDIR:", WORKDIR)
for root, dirs, files in os.walk(WORKDIR):
    for f in files:
        if f.endswith('.pdbqt') or 'vina' in f.lower() or 'ligand_out' in f.lower():
            fpath = os.path.join(root, f)
            print(fpath, os.path.getsize(fpath))
