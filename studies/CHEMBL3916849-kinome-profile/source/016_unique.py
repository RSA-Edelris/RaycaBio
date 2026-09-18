
import requests, time
BASE = "https://www.ebi.ac.uk/chembl/api/data"

mol_ids = df_train['molecule_chembl_id'].unique().tolist()
print(f"Fetching SMILES for {len(mol_ids)} compounds...")

smiles_map2 = {}
for i in range(0, len(mol_ids), 50):
    batch = mol_ids[i:i+50]
    # Fetch one by one to work around the filter bug
    for mid in batch:
        try:
            r = requests.get(f"{BASE}/molecule/{mid}.json", timeout=10)
            mdata = r.json()
            ms = (mdata.get('molecule_structures') or {}).get('canonical_smiles')
            if ms:
                smiles_map2[mid] = ms
        except:
            pass
    print(f"  {len(smiles_map2)}/{len(mol_ids)}", end='\r')
    time.sleep(0.05)

print(f"\nSMILES fetched: {len(smiles_map2)}")
