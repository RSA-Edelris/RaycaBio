
import json

BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
with open(f"{BASE}/docking_scores_all32.json") as fh:
    dock = json.load(fh)

# Show actual keys for first compound
first = list(dock.keys())[0]
print(f"First compound: {first}")
print(f"Keys: {list(dock[first].keys())}")
print(f"Values: {dock[first]}")
