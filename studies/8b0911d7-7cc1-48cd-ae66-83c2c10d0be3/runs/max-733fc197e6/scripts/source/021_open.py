
import json

with open('/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/autodock-vina-results-3.json') as f:
    data = json.load(f)

print(json.dumps(data, indent=2))
