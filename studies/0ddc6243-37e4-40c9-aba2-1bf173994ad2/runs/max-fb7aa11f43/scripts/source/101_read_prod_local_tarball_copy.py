
import subprocess, os

# Read prod.in from the local tarball copy
tarball = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/md/stage"
# Try the work directory copies
import glob
for p in glob.glob("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/**/prod.in", recursive=True):
    print(f"=== {p} ===")
    with open(p) as f:
        print(f.read())
    print()
