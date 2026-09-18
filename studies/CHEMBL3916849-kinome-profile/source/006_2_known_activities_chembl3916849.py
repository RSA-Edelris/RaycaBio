
import time

# 2. Known activities for CHEMBL3916849
r2 = requests.get(
    f"{BASE}/activity.json",
    params={"molecule_chembl_id": "CHEMBL3916849", "limit": 100},
    timeout=30
)
acts = r2.json()
print(f"Total known activities: {acts['page_meta']['total_count']}")
for a in acts['activities'][:20]:
    print(f"  {a.get('target_chembl_id')} | {a.get('target_pref_name')} | {a.get('standard_type')} = {a.get('standard_value')} {a.get('standard_units')} | assay: {a.get('assay_chembl_id')}")
