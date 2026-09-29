
import urllib.request, os, pathlib

session_dir = pathlib.Path("/home/ubuntu/rayca-sessions/318e1560-3d55-4b84-bafd-39c623c8d42c-c53814dd4ebb")
work_dir = session_dir / "brd4_vhl_protac"
work_dir.mkdir(exist_ok=True)

for pdb_id in ["3MXF", "5T35"]:
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    out = work_dir / f"{pdb_id}.pdb"
    if not out.exists():
        urllib.request.urlretrieve(url, out)
    print(f"{pdb_id}: {out.stat().st_size} bytes")
