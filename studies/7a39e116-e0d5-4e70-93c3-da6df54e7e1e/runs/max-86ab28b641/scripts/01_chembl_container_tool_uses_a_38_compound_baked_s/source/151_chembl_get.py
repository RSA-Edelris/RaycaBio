
import requests, json, time, urllib.parse

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

# Try SMILES-based similarity search for BX912
BX912_SMILES = "O=C(Nc1cccc(Nc2ncc(Br)c(NCCc3cnc[nH]3)n2)c1)N1CCCC1"
smi_enc = urllib.parse.quote(BX912_SMILES, safe='')
url = f"{BASE}/similarity/{smi_enc}/40.json"
print("Similarity URL:", url[:80], "...")
data = chembl_get(url, params={"limit": 50})
total = data.get("page_meta", {}).get("total_count", 0)
print(f"Similarity hits at Tc≥0.4: {total}")
if total:
    for m in data.get("molecules", [])[:5]:
        sim = m.get("similarity", "?")
        print(f"  {m['molecule_chembl_id']}: {m.get('pref_name','?')} Tc={sim}")
