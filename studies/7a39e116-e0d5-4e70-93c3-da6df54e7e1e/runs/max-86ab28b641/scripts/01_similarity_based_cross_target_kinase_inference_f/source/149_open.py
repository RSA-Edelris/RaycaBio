
import json, os
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# Read the first result file to understand what came back
result_file = f"{WS}/chembl-results.json"
with open(result_file) as f:
    raw = json.load(f)
print("Keys:", list(raw.keys()))
print("num_results:", raw.get("num_results"))
print("query:", raw.get("query"))
print("summary:", raw.get("summary"))
if raw.get("results"):
    print("results sample:", raw["results"][:2])
else:
    print("results: empty list")
