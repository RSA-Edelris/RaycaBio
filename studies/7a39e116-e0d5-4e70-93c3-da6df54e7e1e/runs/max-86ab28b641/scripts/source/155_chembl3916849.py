
import requests
BASE = "https://www.ebi.ac.uk/chembl/api/data"

# Test CHEMBL3916849 (BX912 exact match) directly — no __in, no filter noise
r = requests.get(f"{BASE}/activity.json",
    params={"molecule_chembl_id": "CHEMBL3916849", "limit": 20, "format": "json"},
    timeout=30, headers={"Accept": "application/json"})
r.raise_for_status()
d = r.json()
print(f"CHEMBL3916849 total activities (no filter): {d['page_meta']['total_count']}")
if d.get("activities"):
    a = d["activities"][0]
    print("Sample:", a.get("molecule_chembl_id"), a.get("target_pref_name"),
          a.get("standard_type"), a.get("standard_value"), a.get("assay_type"))

# Now test __in with comma separator (not semicolon)
r2 = requests.get(f"{BASE}/activity.json",
    params={"molecule_chembl_id__in": "CHEMBL3916849,CHEMBL5085430",
            "limit": 20, "format": "json"},
    timeout=30, headers={"Accept": "application/json"})
r2.raise_for_status()
d2 = r2.json()
print(f"\nComma-separated __in total: {d2['page_meta']['total_count']}")

# And try pipe separator
r3 = requests.get(f"{BASE}/activity.json",
    params={"molecule_chembl_id__in": "CHEMBL3916849|CHEMBL5085430",
            "limit": 20, "format": "json"},
    timeout=30, headers={"Accept": "application/json"})
r3.raise_for_status()
d3 = r3.json()
print(f"Pipe-separated __in total: {d3['page_meta']['total_count']}")
