
import requests, time, json
BASE = "https://www.ebi.ac.uk/chembl/api/data"

# Fetch target sequences for all 197 unique training targets
# Target endpoint returns protein sequences in target_components
seq_map = {}   # target_chembl_id -> (pref_name, sequence, target_type)
for i in range(0, len(unique_targets), 50):
    batch = unique_targets[i:i+50]
    r = requests.get(f"{BASE}/target.json",
                     params={"chembl_id__in": ','.join(batch), "limit": 50},
                     timeout=30)
    for t in r.json().get('targets', []):
        tid = t['target_chembl_id']
        comps = t.get('target_components', [])
        if comps:
            seq = comps[0].get('target_component_sequences', '')
            # sequence is under component_sequences in older format
            # Try multiple fields
            if not seq:
                seq = comps[0].get('sequence', '')
            seq_map[tid] = {
                'name': t.get('pref_name', ''),
                'seq': seq,
                'type': t.get('target_type', '')
            }
    time.sleep(0.2)

print(f"Targets with data: {len(seq_map)}")
# Check sequence field
sample_tid = list(seq_map.keys())[0]
print(f"Sample: {sample_tid} -> name={seq_map[sample_tid]['name']}")
print(f"  seq keys in component: {list(r.json()['targets'][0]['target_components'][0].keys())[:10]}")
