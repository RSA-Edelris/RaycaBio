
import json, shutil
from pathlib import Path

BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
MMGBSA_DIR = Path(f"{BASE}/mmgbsa2")
RESULTS_FILE = Path(f"{BASE}/mmgbsa2_results.json")

# Clear all failed compound subdirectories (empty prmtop etc.)
names = sorted([f.stem.replace('_pose1','') 
                for f in Path(f"{BASE}/best_poses2_top1").glob('*_pose1.sdf')])
print(f"Compounds to process: {len(names)}")

cleared = 0
for name in names:
    wd = MMGBSA_DIR / name
    if wd.exists():
        shutil.rmtree(wd)
        cleared += 1
print(f"Cleared {cleared} old compound directories")

# Reset results to empty
RESULTS_FILE.write_text('{}')
print("Results JSON reset")
print("\nNames:", names[:5], '...')
