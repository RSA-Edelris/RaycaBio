
import json, os, glob

ART = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# Check GBSA JSON outputs for refined coordinate files
gbsa_files = sorted(glob.glob(f"{ART}/gbsa_*.json"))
for jpath in gbsa_files:
    with open(jpath) as fh:
        d = json.load(fh)
    out = d.get('output', {})
    print(f"=== {os.path.basename(jpath)} ===")
    print("  output keys:", list(out.keys()) if isinstance(out, dict) else "")
    if isinstance(out, dict):
        for k in ('files_written', 'binding_energy_csv', 'summary', 'results'):
            if k in out:
                v = out[k]
                print(f"  {k}: {str(v)[:200]}")
    print()

# Also check for any *_refined* or *_min* SDF files
refined = glob.glob(f"{ART}/**/*min*.sdf", recursive=True) + \
          glob.glob(f"{ART}/**/*refin*.sdf", recursive=True) + \
          glob.glob(f"{ART}/**/*em*.sdf", recursive=True)
print("Refined/EM SDF files:", refined)
