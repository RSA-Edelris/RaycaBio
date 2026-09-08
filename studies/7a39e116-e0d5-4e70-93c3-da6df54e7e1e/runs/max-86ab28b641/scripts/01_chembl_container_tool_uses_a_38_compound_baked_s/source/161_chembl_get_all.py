
import requests, time, pandas as pd
BASE = "https://www.ebi.ac.uk/chembl/api/data"
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

def chembl_get_all(url, params=None, key="activities", limit=1000):
    rows, offset = [], 0
    p = dict(params or {}); p["limit"] = limit
    while True:
        p["offset"] = offset
        r = requests.get(url, params=p, timeout=60, headers={"Accept": "application/json"})
        r.raise_for_status(); d = r.json()
        batch = d.get(key, [])
        rows.extend(batch)
        total = d.get("page_meta", {}).get("total_count", 0)
        if len(rows) >= total or not batch: break
        offset += limit; time.sleep(0.25)
    return rows

ids_csv = ",".join(sorted(all_chembl_ids))

# ── Check PKIS Nanosyn panel for our analogs ─────────────────────────────────
pkis_acts = chembl_get_all(f"{BASE}/activity.json",
    {"document_chembl_id": "CHEMBL1961873",
     "molecule_chembl_id__in": ids_csv, "format": "json"})
print(f"PKIS Nanosyn hits for our analogs: {len(pkis_acts)}")
if pkis_acts:
    df_pkis = pd.DataFrame(pkis_acts)
    print(df_pkis[["molecule_chembl_id","target_pref_name","standard_type","standard_value"]].head(10).to_string())

# ── Check SGC KinomeScan for our analogs ─────────────────────────────────────
sgc_acts = chembl_get_all(f"{BASE}/activity.json",
    {"document_chembl_id": "CHEMBL4507330",
     "molecule_chembl_id__in": ids_csv, "format": "json"})
print(f"\nSGC KinomeScan hits for our analogs: {len(sgc_acts)}")
if sgc_acts:
    df_sgc = pd.DataFrame(sgc_acts)
    print(df_sgc[["molecule_chembl_id","target_pref_name","standard_type","standard_value"]].head(10).to_string())

# ── Also check PKIS2/UNC document ────────────────────────────────────────────
pkis2_acts = chembl_get_all(f"{BASE}/activity.json",
    {"document_chembl_id": "CHEMBL2007661",
     "molecule_chembl_id__in": ids_csv, "format": "json"})
print(f"\nPKIS UNC hits for our analogs: {len(pkis2_acts)}")
