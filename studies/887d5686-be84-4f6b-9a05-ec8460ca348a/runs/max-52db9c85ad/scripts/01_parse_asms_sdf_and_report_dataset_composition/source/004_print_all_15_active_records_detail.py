
# Print all 15 active records in detail
actives = [r for r in records if r.get('HIT P841') == 'Active']
inactives = [r for r in records if r.get('HIT P841') == 'Inactive']
print(f"Actives: {len(actives)}, Inactives: {len(inactives)}")

print("\n=== ALL 15 ACTIVE RECORDS ===")
for i, r in enumerate(actives):
    print(f"\n--- Active {i+1} ---")
    for k, v in r.items():
        if k != 'Smiles':
            print(f"  {k}: {v}")
    print(f"  SMILES: {r.get('Smiles','')}")
