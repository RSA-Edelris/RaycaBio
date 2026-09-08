
import requests, time, pandas as pd, pickle
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
BASE = "https://www.ebi.ac.uk/chembl/api/data"

def chembl_activities_batch(chembl_ids, limit=1000):
    """Pull binding/functional activities for a batch of ChEMBL IDs."""
    id_str = ";".join(chembl_ids)
    rows = []
    offset = 0
    while True:
        params = {
            "molecule_chembl_id__in": id_str,
            "assay_type__in": "B;F",
            "standard_type__in": "IC50;Ki;Kd;EC50;pIC50;pKi",
            "target_organism": "Homo sapiens",
            "standard_relation": "=",
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
        time.sleep(0.3)
    return rows

# Batch into groups of 20
ids_list = sorted(all_chembl_ids)
batch_size = 20
all_activities = []
for i in range(0, len(ids_list), batch_size):
    batch = ids_list[i:i+batch_size]
    acts = chembl_activities_batch(batch)
    all_activities.extend(acts)
    print(f"  Batch {i//batch_size+1}/{-(-len(ids_list)//batch_size)}: {len(batch)} IDs → {len(acts)} activities")

print(f"\nTotal raw activities: {len(all_activities)}")

df_acts = pd.DataFrame(all_activities)
print("Columns:", list(df_acts.columns))
print("standard_type counts:\n", df_acts["standard_type"].value_counts().head(10) if "standard_type" in df_acts.columns else "N/A")
print("Sample target names:", df_acts["target_pref_name"].dropna().unique()[:8].tolist() if "target_pref_name" in df_acts.columns else "N/A")

df_acts.to_parquet(f"{WS}/chembl_activities_raw.parquet", index=False)
print("Saved parquet.")
