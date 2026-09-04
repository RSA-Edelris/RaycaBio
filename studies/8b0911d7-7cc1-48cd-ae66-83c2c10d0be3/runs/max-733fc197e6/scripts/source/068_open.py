
import json
with open('/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/mmgbsa_results.json') as f:
    res = json.load(f)
for r in res:
    print(r)
