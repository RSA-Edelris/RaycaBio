
# Step 1: Find BX912 in ChEMBL and pull all its kinase bioactivities
import requests, json, time

BASE = "https://www.ebi.ac.uk/chembl/api/data"

def chembl_get(url, params=None, retries=3):
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=30, headers={"Accept": "application/json"})
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == retries-1:
                raise
            time.sleep(2)

# Search for BX912 by preferred name
data = chembl_get(f"{BASE}/molecule.json", params={"pref_name__icontains": "BX912", "format": "json"})
print(f"Name search 'BX912': {data['page_meta']['total_count']} hits")
for mol in data.get("molecules", []):
    print(f"  {mol['molecule_chembl_id']}: {mol['pref_name']} | MW={mol['molecule_properties'].get('mw_freebase') if mol.get('molecule_properties') else 'N/A'}")

# Also try BX-912
data2 = chembl_get(f"{BASE}/molecule.json", params={"pref_name__icontains": "BX-912", "format": "json"})
print(f"\nName search 'BX-912': {data2['page_meta']['total_count']} hits")
for mol in data2.get("molecules", []):
    print(f"  {mol['molecule_chembl_id']}: {mol['pref_name']}")

# Also search by synonym
data3 = chembl_get(f"{BASE}/molecule.json", params={"molecule_synonyms__synonyms__icontains": "BX912", "format": "json"})
print(f"\nSynonym search 'BX912': {data3['page_meta']['total_count']} hits")
for mol in data3.get("molecules", []):
    print(f"  {mol['molecule_chembl_id']}: {mol['pref_name']} | synonyms: {[s['synonyms'] for s in mol.get('molecule_synonyms', [])][:5]}")
