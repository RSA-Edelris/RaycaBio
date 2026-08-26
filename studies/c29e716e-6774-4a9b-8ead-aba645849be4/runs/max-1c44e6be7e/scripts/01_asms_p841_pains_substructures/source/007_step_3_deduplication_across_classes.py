
# Step 3: Deduplication across classes
actives = df[df['HIT P841'] == 'Active'].copy()
inactives = df[df['HIT P841'] == 'Inactive'].copy()

print(f"Actives: {len(actives)}, Inactives: {len(inactives)}")

# Duplicates within actives
dup_active = actives[actives.duplicated('inchi_key', keep=False)]
print(f"\nDuplicates within actives (same InChIKey): {len(dup_active)}")
if len(dup_active):
    print(dup_active[['EDS_Number','inchi_key','can_smiles','HIT P841']].to_string())

# Duplicates within inactives
dup_inactive_count = inactives.duplicated('inchi_key').sum()
print(f"Duplicates within inactives: {dup_inactive_count}")

# Cross-class duplicates: active InChIKey appears in inactives
active_ikeys = set(actives['inchi_key'].dropna())
cross_dups = inactives[inactives['inchi_key'].isin(active_ikeys)]
print(f"\nCross-class duplicates (active IK in inactives): {len(cross_dups)}")
if len(cross_dups):
    print(cross_dups[['EDS_Number','inchi_key','can_smiles']].to_string())

# Show active molecules
print("\n--- ACTIVE MOLECULES ---")
print(actives[['EDS_Number','can_smiles','MW','LogP','HBD','HBA','RotB','Hit_rank','AS ratio','RTmin','Stereo  Configuration']].to_string())
