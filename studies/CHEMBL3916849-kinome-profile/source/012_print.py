
import requests, time
BASE = "https://www.ebi.ac.uk/chembl/api/data"

# Debug: check unique_targets size
print(f"unique_targets length: {len(unique_targets)}")
print("First 5:", unique_targets[:5])

# Fetch ALL training target info properly
target_info2 = {}
for i in range(0, len(unique_targets), 50):
    batch = unique_targets[i:i+50]
    r = requests.get(f"{BASE}/target.json",
                     params={"chembl_id__in": ','.join(batch), "limit": 50},
                     timeout=30)
    rj = r.json()
    for t in rj.get('targets', []):
        comps = t.get('target_components', [])
        acc = comps[0].get('accession', '') if comps else ''
        target_info2[t['target_chembl_id']] = {
            'name': t.get('pref_name', ''),
            'uniprot': acc,
        }
    print(f"  batch {i}: got {len(rj.get('targets',[]))} targets, total so far: {len(target_info2)}")
    time.sleep(0.2)

print(f"\nFinal training target count: {len(target_info2)}")
