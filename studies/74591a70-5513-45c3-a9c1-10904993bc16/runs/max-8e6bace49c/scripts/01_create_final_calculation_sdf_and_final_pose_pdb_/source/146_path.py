
from pathlib import Path
import json

BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

for f in [
    "best_poses2_top1",
    "best_poses2",
    "docking2_results.json",
    "docking2_ranked.json",
    "mmgbsa2_results.json",
    "interaction_fingerprints.json",
    "CRBN_ID_enantio_2.sdf",
    "CRBN_ID_enantio2_docking_GBSA.sdf",
    "4CI2_receptor_for_docking.pdb",
    "mmgbsa2/receptor_amber.pdb",
]:
    fp = BASE / f
    if fp.is_dir():
        files = list(fp.glob("*.sdf"))
        print(f"DIR  {f}: {len(files)} SDF files, names e.g. {[x.name for x in files[:3]]}")
    elif fp.exists():
        print(f"FILE {f}: {fp.stat().st_size:,} bytes")
    else:
        print(f"MISS {f}")

dr = json.loads((BASE / "docking2_results.json").read_text())
first_k = list(dr.keys())[0]
print(f"\ndocking2_results schema: {first_k} -> {dr[first_k]}")

gr = json.loads((BASE / "mmgbsa2_results.json").read_text())
first_k = list(gr.keys())[0]
print(f"mmgbsa2_results schema: {first_k} -> {gr[first_k]}")
