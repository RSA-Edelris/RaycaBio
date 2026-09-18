
import json

# Read the confidence JSON
with open('./boltz_out/boltz_results_boltz_input/predictions/boltz_input/confidence_boltz_input_model_0.json') as f:
    conf = json.load(f)
print("=== confidence ===")
print(json.dumps(conf, indent=2))

# Read the manifest to see which system this is
with open('./boltz_out/boltz_results_boltz_input/processed/manifest.json') as f:
    mf = json.load(f)
print("\n=== manifest ===")
print(json.dumps(mf, indent=2))

# CIF header to identify the system
with open('./boltz_out/boltz_results_boltz_input/predictions/boltz_input/boltz_input_model_0.cif') as f:
    cif_head = f.read(1500)
print("\n=== CIF (first 1500 chars) ===")
print(cif_head)
