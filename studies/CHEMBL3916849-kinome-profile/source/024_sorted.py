
import os, glob

ws = "/home/ubuntu/rayca-sessions/b96424ba-16ee-41cb-b71c-c27a58be87c0-8a50fbf21660"
# Find the output files
for f in sorted(os.listdir(ws)):
    fpath = os.path.join(ws, f)
    if os.path.isfile(fpath):
        size = os.path.getsize(fpath)
        print(f"{f}  ({size} bytes)")
