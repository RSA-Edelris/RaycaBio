
# Check actual keys in one JSON to see correct field names
import json
jf = f"{SESSION}/ARV_001/boltz_results_ARV_001_constrained/predictions/ARV_001_constrained/confidence_ARV_001_constrained_model_0.json"
with open(jf) as f:
    d = json.load(f)
print("Keys:", list(d.keys()))
print("Full JSON:", json.dumps(d, indent=2)[:1500])
