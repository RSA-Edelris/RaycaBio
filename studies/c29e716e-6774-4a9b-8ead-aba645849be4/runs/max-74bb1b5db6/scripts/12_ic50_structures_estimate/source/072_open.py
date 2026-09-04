
import json

with open('/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/autodock-vina-results.json') as f:
    vina_out = json.load(f)

print(type(vina_out))
if isinstance(vina_out, dict):
    for k, v in vina_out.items():
        print(f"  {k}: {str(v)[:200]}")
elif isinstance(vina_out, list):
    for item in vina_out[:5]:
        print(item)
