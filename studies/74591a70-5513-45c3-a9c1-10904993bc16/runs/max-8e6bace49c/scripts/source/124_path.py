
import json
from pathlib import Path

BASE     = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
results  = json.loads((BASE / "docking2_results.json").read_text())

# Also load EC50 from summary
summary  = json.loads((BASE / "CRBN_enantio2_summary.json").read_text())
ec50_map = {s['name']: s['ec50_um'] for s in summary['compounds']}

# Ranked by Vina affinity
rows = []
for name, v in results.items():
    if v.get('affinity') is not None:
        rows.append({
            'name': name,
            'parent': '_'.join(name.split('_')[:2]),
            'affinity': v['affinity'],
            'cnn': v.get('cnn_affinity', 0),
            'ec50': ec50_map.get(name, 'N/A'),
        })
rows.sort(key=lambda r: r['affinity'])

print(f"{'Rank':<5} {'Name':<22} {'Vina ΔG':>9} {'CNN pKd':>9} {'EC50(µM)':>10}")
print("─"*58)
for i, r in enumerate(rows, 1):
    print(f"{i:<5} {r['name']:<22} {r['affinity']:>9.2f} {r['cnn']:>9.2f} {str(r['ec50']):>10}")

# Save ranked results
(BASE / "docking2_ranked.json").write_text(json.dumps({'ranked': rows}, indent=2))

# Extract best pose (first molecule) from each SDF to best_poses2/
POSES_DIR = BASE / "best_poses2"
BEST_DIR  = BASE / "best_poses2_top1"
BEST_DIR.mkdir(exist_ok=True)

extracted = 0
for name, v in results.items():
    src = POSES_DIR / f"{name}_poses.sdf"
    if not src.exists():
        print(f"MISSING poses: {name}")
        continue
    text = src.read_text()
    # Split on $$$$ and take first complete block
    blocks = [b.strip() for b in text.split("$$$$") if b.strip()]
    if blocks:
        (BEST_DIR / f"{name}_pose1.sdf").write_text(blocks[0] + "\n$$$$\n")
        extracted += 1

print(f"\nExtracted {extracted} best poses to best_poses2_top1/")
