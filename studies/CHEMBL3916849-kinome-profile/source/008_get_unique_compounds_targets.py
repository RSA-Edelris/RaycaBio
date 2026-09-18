
# Get unique compounds and targets
unique_mols = df_raw['molecule_chembl_id'].dropna().unique().tolist()
unique_targets = df_raw['target_chembl_id'].dropna().unique().tolist()
print(f"Unique compounds: {len(unique_mols)}, unique targets: {len(unique_targets)}")

# Batch-fetch compound SMILES (50 per request)
def fetch_smiles_batch(chembl_ids):
    result = {}
    for i in range(0, len(chembl_ids), 50):
        batch = chembl_ids[i:i+50]
        ids_str = ','.join(batch)
        r = requests.get(f"{BASE}/molecule.json",
                        params={"chembl_id__in": ids_str, "limit": 50},
                        timeout=30)
        for m in r.json().get('molecules', []):
            smiles = (m.get('molecule_structures') or {}).get('canonical_smiles')
            if smiles:
                result[m['molecule_chembl_id']] = smiles
        time.sleep(0.2)
    return result

print("Fetching compound SMILES...")
smiles_map = fetch_smiles_batch(unique_mols[:500])  # limit to 500 unique compounds for speed
print(f"SMILES fetched: {len(smiles_map)}")
