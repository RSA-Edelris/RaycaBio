
import requests, time, json
BASE = "https://www.ebi.ac.uk/chembl/api/data"

# Fetch all 197 training targets → extract UniProt accessions + names
target_info = {}  # chembl_id -> {name, uniprot, type}

for i in range(0, len(unique_targets), 50):
    batch = unique_targets[i:i+50]
    r = requests.get(f"{BASE}/target.json",
                     params={"chembl_id__in": ','.join(batch), "limit": 50},
                     timeout=30)
    for t in r.json().get('targets', []):
        comps = t.get('target_components', [])
        acc = comps[0].get('accession', '') if comps else ''
        target_info[t['target_chembl_id']] = {
            'name': t.get('pref_name', ''),
            'uniprot': acc,
            'type': t.get('target_type', '')
        }
    time.sleep(0.25)

print(f"Target info fetched: {len(target_info)}")

# Also fetch kinase targets from ChEMBL (target_class=Kinase, human, single protein)
# Get up to 500 kinase targets for the prediction sweep
kinase_targets = {}
r_k = requests.get(f"{BASE}/target.json",
                   params={"target_type": "SINGLE PROTEIN",
                           "organism": "Homo sapiens",
                           "target_class__icontains": "kinase",
                           "limit": 500},
                   timeout=60)
for t in r_k.json().get('targets', []):
    comps = t.get('target_components', [])
    acc = comps[0].get('accession', '') if comps else ''
    if acc:
        kinase_targets[t['target_chembl_id']] = {
            'name': t.get('pref_name', ''),
            'uniprot': acc,
            'type': t.get('target_type', '')
        }
print(f"Kinase targets from ChEMBL: {len(kinase_targets)}")
print("Sample kinases:", list(kinase_targets.items())[:3])
