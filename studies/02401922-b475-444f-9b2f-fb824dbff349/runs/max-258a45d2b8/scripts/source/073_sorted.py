
import os, glob

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
files = sorted(os.listdir(wd))
print("Workspace files:")
for f in files:
    sz = os.path.getsize(os.path.join(wd, f))
    print(f"  {f:50s}  {sz:10d} B")
