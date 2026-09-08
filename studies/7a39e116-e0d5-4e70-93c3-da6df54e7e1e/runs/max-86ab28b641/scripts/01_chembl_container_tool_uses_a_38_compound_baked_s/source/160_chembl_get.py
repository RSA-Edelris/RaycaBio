
import requests, json, time
BASE = "https://www.ebi.ac.uk/chembl/api/data"

def chembl_get(url, params=None):
    r = requests.get(url, params=params, timeout=30, headers={"Accept": "application/json"})
    r.raise_for_status()
    return r.json()

# ── 1. Full activity list for CHEMBL3916849 (BX912) including ALL assay types ─
d_bx = chembl_get(f"{BASE}/activity.json",
                  params={"molecule_chembl_id": "CHEMBL3916849",
                          "target_organism": "Homo sapiens",
                          "limit": 200, "format": "json"})
print(f"BX912 total ChEMBL activities: {d_bx['page_meta']['total_count']}")
acts = d_bx.get("activities", [])
for a in acts:
    print(f"  {a.get('target_pref_name','?')[:45]:45s} "
          f"{a.get('standard_type',''):8s} {str(a.get('standard_value',''))[:8]:8s} "
          f"{a.get('standard_units',''):6s}  assay={a.get('assay_chembl_id','')}")

# ── 2. Search for PKIS dataset in ChEMBL documents ─────────────────────────
d_doc = chembl_get(f"{BASE}/document.json",
                   params={"title__icontains": "PKIS", "limit": 10})
print(f"\nPKIS document hits: {d_doc['page_meta']['total_count']}")
for doc in d_doc.get("documents", []):
    print(f"  {doc['document_chembl_id']}: {doc.get('title','')[:80]}")

d_doc2 = chembl_get(f"{BASE}/document.json",
                    params={"title__icontains": "KinomeScan", "limit": 10})
print(f"\nKinomeScan document hits: {d_doc2['page_meta']['total_count']}")
for doc in d_doc2.get("documents", []):
    print(f"  {doc['document_chembl_id']}: {doc.get('title','')[:80]}")
