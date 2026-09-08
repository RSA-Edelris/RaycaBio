
import requests, json, time, urllib.parse, pickle
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
BASE = "https://www.ebi.ac.uk/chembl/api/data"

def chembl_get_all_pages(url, params=None, key="molecules", limit=100):
    rows = []
    p = dict(params or {})
    p["limit"] = limit
    p["offset"] = 0
    while True:
        r = requests.get(url, params=p, timeout=30, headers={"Accept": "application/json"})
        r.raise_for_status()
        d = r.json()
        batch = d.get(key, [])
        rows.extend(batch)
        meta = d.get("page_meta", {})
        total = meta.get("total_count", 0)
        if len(rows) >= total or not batch:
            break
        p["offset"] += limit
        time.sleep(0.3)
    return rows

compounds = {
    "BX912":         "O=C(Nc1cccc(Nc2ncc(Br)c(NCCc3cnc[nH]3)n2)c1)N1CCCC1",
    "EL2003A":       "O=C(Nc1cccc(Nc2nc(NCCc3cnc[nH]3)c3nc[nH]c3n2)c1)N1CCCC1",
    "EL2003A-A2U1":  "Cc1ccc(Nc2nc(NCCc3c[nH]cn3)c3nc[nH]c3n2)cc1NC(=O)N1CCCC1",
    "EL2003A-A4U1":  "O=C(Nc1cc(Nc2nc(NCCc3c[nH]cn3)c3nc[nH]c3n2)ccc1C(F)(F)F)N1CCCC1",
    "EL5001A":       "O=C(NCCNc1ncc(Br)c(NCCc2c[nH]cn2)n1)N1CCCC1",
    "EL5003A":       "O=C(N[C@@H]1CC[C@@H](Nc2ncc(Br)c(NCCc3c[nH]cn3)n2)C1)N1CCCC1",
}

TC_THRESHOLD = 40
all_hits = {}

for cname, smi in compounds.items():
    smi_enc = urllib.parse.quote(smi, safe='')
    url = f"{BASE}/similarity/{smi_enc}/{TC_THRESHOLD}.json"
    mols = chembl_get_all_pages(url, key="molecules")
    hits = []
    for m in mols:
        try:
            tc = float(m.get("similarity", 0)) / 100.0
        except (TypeError, ValueError):
            tc = 0.0
        hits.append({"chembl_id": m["molecule_chembl_id"],
                     "tanimoto": tc,
                     "pref_name": m.get("pref_name", "")})
    all_hits[cname] = hits
    print(f"{cname}: {len(hits)} analogs  top: {hits[0]['chembl_id']} Tc={hits[0]['tanimoto']:.3f} '{hits[0]['pref_name']}'" if hits else f"{cname}: 0 hits")

all_chembl_ids = set()
for hits in all_hits.values():
    all_chembl_ids.update(h["chembl_id"] for h in hits)
print(f"\nUnique analog ChEMBL IDs: {len(all_chembl_ids)}")

with open(f"{WS}/similarity_hits.pkl", "wb") as f:
    pickle.dump(all_hits, f)
print("Saved.")
