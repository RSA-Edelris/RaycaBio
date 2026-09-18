
import json

# Read hparams
with open('protacfold_out/boltz_pred/boltz_results_gspt1_crbn_molecular_glue_ternary/lightning_logs/version_0/hparams.yaml') as f:
    print("=== hparams.yaml ===")
    print(f.read())

# Read manifest
with open('protacfold_out/boltz_pred/boltz_results_gspt1_crbn_molecular_glue_ternary/processed/manifest.json') as f:
    print("\n=== manifest.json ===")
    print(json.dumps(json.load(f), indent=2))

# Read record
with open('protacfold_out/boltz_pred/boltz_results_gspt1_crbn_molecular_glue_ternary/processed/records/gspt1_crbn_molecular_glue_ternary.json') as f:
    print("\n=== record.json ===")
    print(json.dumps(json.load(f), indent=2))
