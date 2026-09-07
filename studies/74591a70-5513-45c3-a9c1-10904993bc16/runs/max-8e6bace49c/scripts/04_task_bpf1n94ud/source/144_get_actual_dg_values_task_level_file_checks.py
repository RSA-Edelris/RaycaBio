
# Get actual dG values and task-level file checks
import json
from pathlib import Path

BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
gbsa_json = BASE / "mmgbsa2_results.json"
data = json.loads(gbsa_json.read_text())
# print keys of first entry
first_k = list(data.keys())[0]
print("First key:", first_k)
print("First value keys:", list(data[first_k].keys()) if isinstance(data[first_k], dict) else type(data[first_k]))
# collect dG
dg_vals = {}
for k, v in data.items():
    if isinstance(v, dict):
        for field in ('DELTA', 'delta_total', 'dg', 'TOTAL', 'delta_G', 'DeltaG'):
            if field in v:
                dg_vals[k] = v[field]
                break
        if k not in dg_vals:
            print(f"  {k}: keys={list(v.keys())[:6]}")

if dg_vals:
    print(f"\ndG range: {min(dg_vals.values()):.1f} to {max(dg_vals.values()):.1f} kcal/mol")
    print(f"Compounds with dG: {len(dg_vals)}")

# Check task artefacts
print("\nTask artefacts:")
for f in ['run_interactions_rdkit.py', 'run_mmgbsa2.py']:
    fp = BASE / f
    print(f"  {f}: exists={fp.exists()}, bytes={fp.stat().st_size if fp.exists() else 0}")
    
# Check receiver_amber receptor
rec = BASE / "mmgbsa2" / "receptor_amber.pdb"
print(f"  receptor_amber.pdb: exists={rec.exists()}, bytes={rec.stat().st_size if rec.exists() else 0}")

# Check best poses count
best2 = BASE / "best_poses2"
top1 = BASE / "best_poses2_top1"
print(f"  best_poses2/ files: {len(list(best2.glob('*.sdf')))}")
print(f"  best_poses2_top1/ files: {len(list(top1.glob('*.sdf')))}")
