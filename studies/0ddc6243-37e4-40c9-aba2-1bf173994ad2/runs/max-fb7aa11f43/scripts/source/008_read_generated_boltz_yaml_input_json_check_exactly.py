
# Read the generated Boltz YAML and input JSON to check exactly what was passed
with open('protacfold_out/gspt1_crbn_molecular_glue_ternary.yaml') as f:
    print("=== boltz input YAML ===")
    print(f.read())

with open('protacfold_out/gspt1_crbn_molecular_glue_ternary.json') as f:
    import json
    print("\n=== AF3 input JSON ===")
    print(json.dumps(json.load(f), indent=2))
