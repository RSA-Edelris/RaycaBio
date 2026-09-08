
import requests, time, pandas as pd, numpy as np
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
BASE = "https://www.ebi.ac.uk/chembl/api/data"

def pull_activities_batch(chembl_ids, limit=1000):
    rows = []
    offset = 0
    id_str = ",".join(chembl_ids)
    while True:
        params = {
            "molecule_chembl_id__in": id_str,
            "assay_type__in": "B,F",
            "standard_relation": "=",
            "target_organism": "Homo sapiens",
            "limit": limit,
            "offset": offset,
            "format": "json",
        }
        r = requests.get(f"{BASE}/activity.json", params=params,
                         timeout=60, headers={"Accept": "application/json"})
        r.raise_for_status()
        d = r.json()
        batch = d.get("activities", [])
        rows.extend(batch)
        total = d.get("page_meta", {}).get("total_count", 0)
        if len(rows) >= total or not batch:
            break
        offset += limit
        time.sleep(0.25)
    return rows

ids_list = sorted(all_chembl_ids)
batch_size = 20
all_acts = []
for i in range(0, len(ids_list), batch_size):
    batch = ids_list[i:i+batch_size]
    acts = pull_activities_batch(batch)
    all_acts.extend(acts)
    print(f"  Batch {i//batch_size+1}: {len(batch)} IDs → {len(acts)} activities")

df = pd.DataFrame(all_acts)
print(f"\nTotal activities: {len(df)}")
if len(df):
    print("standard_type value counts (top 10):\n", df["standard_type"].value_counts().head(10))
    print("\nUnique compounds with data:", df["molecule_chembl_id"].nunique())
    print("Sample targets:", df["target_pref_name"].dropna().unique()[:8].tolist())

df.to_parquet(f"{WS}/chembl_activities_raw.parquet", index=False)
print("\nSaved.")
