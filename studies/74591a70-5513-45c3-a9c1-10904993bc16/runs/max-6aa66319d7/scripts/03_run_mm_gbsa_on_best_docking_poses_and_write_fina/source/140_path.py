
import json
from pathlib import Path

BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

with open(BASE/"docking2_ranked.json") as f:
    docking_ranked = json.load(f)
with open(BASE/"mmgbsa2_results.json") as f:
    mmgbsa = json.load(f)
with open(BASE/"interaction_fingerprints.json") as f:
    ints_data = json.load(f)

print(type(docking_ranked), str(docking_ranked)[:200])
