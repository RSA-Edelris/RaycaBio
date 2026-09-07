
import json
from pathlib import Path

BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

# Load all data
with open(BASE/"docking2_ranked.json") as f:
    docking_ranked = json.load(f)
with open(BASE/"mmgbsa2_results.json") as f:
    mmgbsa = json.load(f)
with open(BASE/"interaction_fingerprints.json") as f:
    ints = json.load(f)

# Build lookup dicts
dock_map = {r['name']: r for r in docking_ranked}
print(f"Docking: {len(dock_map)} compounds")
print(f"MM-GBSA: {len(mmgbsa)} compounds")
print(f"Interactions: {len(ints['fingerprints'])} compounds")

# Check all 22 present
names = sorted(dock_map.keys())
print("\nMissing MM-GBSA:", [n for n in names if n not in mmgbsa])
print("Missing interactions:", [n for n in names if n not in ints['fingerprints']])
