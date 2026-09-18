
import requests, json, time
import pandas as pd
import numpy as np

BASE = "https://www.ebi.ac.uk/chembl/api/data"

# Pull kinase-compound Ki/Kd data from ChEMBL
# Target class = "Kinase", single protein, human, Ki or Kd, nM, pChEMBL >= 5
# Use pChEMBL value directly (already -log10 molar)
all_rows = []
offset = 0
limit = 1000
max_records = 5000

print("Fetching kinase training data from ChEMBL REST...")
while len(all_rows) < max_records:
    params = {
        "target_type": "SINGLE PROTEIN",
        "standard_type__in": "Ki,Kd",
        "standard_units": "nM",
        "pchembl_value__gte": 5.0,
        "target_organism": "Homo sapiens",
        "limit": limit,
        "offset": offset,
        "assay_type": "B",  # binding assay
        "format": "json"
    }
    r = requests.get(f"{BASE}/activity.json", params=params, timeout=60)
    data = r.json()
    batch = data.get('activities', [])
    if not batch:
        break
    all_rows.extend(batch)
    total = data['page_meta']['total_count']
    print(f"  Fetched {len(all_rows)}/{min(total, max_records)} (total in DB: {total})")
    if len(all_rows) >= total or len(all_rows) >= max_records:
        break
    offset += limit
    time.sleep(0.3)

print(f"\nTotal rows fetched: {len(all_rows)}")
df_raw = pd.DataFrame(all_rows)
print(df_raw[['molecule_chembl_id','target_chembl_id','target_pref_name','standard_type','pchembl_value']].head(10))
