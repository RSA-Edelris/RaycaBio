
import json, subprocess
from pathlib import Path

BASE      = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
BEST_DIR  = BASE / "best_poses2_top1"
VENV_PY   = "/home/ubuntu/rayca-runtime/.venv/bin/python3"

# Load data
dock_list  = json.loads((BASE/"docking2_ranked.json").read_text())['ranked']
mmgbsa     = json.loads((BASE/"mmgbsa2_results.json").read_text())
ints_data  = json.loads((BASE/"interaction_fingerprints.json").read_text())

dock_map = {r['name']: r for r in dock_list}
names    = sorted(dock_map.keys())

# Combined table: docking + MM-GBSA
print(f"{'Compound':<22} {'Parent':<12} {'Affinity':>9} {'CNN':>6} {'ΔG_GBSA':>10}")
print("─"*62)
combined = []
for r in dock_list:
    n   = r['name']
    dg  = mmgbsa.get(n, {}).get('DELTA_TOTAL', None)
    combined.append({**r, 'DELTA_TOTAL': dg})
    dg_str = f"{dg:.1f}" if dg is not None else "N/A"
    print(f"{n:<22} {r['parent']:<12} {r['affinity']:>9.2f} {r['cnn']:>6.3f} {dg_str:>10}")

print(f"\nTotal: {len(combined)} compounds")
