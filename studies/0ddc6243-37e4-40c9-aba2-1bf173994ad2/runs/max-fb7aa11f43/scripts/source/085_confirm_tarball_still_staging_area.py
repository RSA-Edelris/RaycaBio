
import pathlib

# Confirm the tarball is still in the staging area
base = pathlib.Path("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b")
tarballs = list(base.rglob("systems_stage.tar.gz"))
for t in tarballs:
    print(t, t.stat().st_size)
