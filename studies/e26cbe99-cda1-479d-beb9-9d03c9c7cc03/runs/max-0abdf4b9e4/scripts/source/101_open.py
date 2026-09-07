
import json

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'

with open(f'{WD}/final_results.json') as fh:
    scores = json.load(fh)

# Verify structure
for cid, v in scores.items():
    best = v['poses'][0]
    print(f"{cid}: vina={best.get('minimizedAffinity', best.get('vina_score')):.2f}  "
          f"cnn_pki={best.get('CNNaffinity', best.get('cnn_pki')):.2f}")
