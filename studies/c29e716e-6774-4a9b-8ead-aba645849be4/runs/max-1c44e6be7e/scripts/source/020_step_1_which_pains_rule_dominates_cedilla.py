
# Step 1: Which PAINS rule dominates Cedilla?
from collections import Counter

ced_pains_hits = ced_df[ced_df['pains'] != '']['pains']
print("Cedilla PAINS rule distribution:")
for rule, count in Counter(ced_pains_hits).most_common(15):
    print(f"  {count:>3}  {rule}")

print(f"\nCedilla Brenk hits:")
for rule, count in Counter(ced_df[ced_df['brenk']!='']['brenk']).most_common():
    print(f"  {count:>3}  {rule}")

# Step 2: Cross-set overlap by InChIKey
asms_ikeys = set(asms_df['inchi_key'].dropna())
ced_ikeys  = set(ced_df['inchi_key'].dropna())
overlap = asms_ikeys & ced_ikeys

print(f"\nASMS_active InChIKeys: {len(asms_ikeys)}")
print(f"Cedilla    InChIKeys: {len(ced_ikeys)}")
print(f"Exact matches (same InChIKey): {len(overlap)}")

if overlap:
    print("\nOverlapping compounds:")
    for ik in overlap:
        a_row = asms_df[asms_df['inchi_key']==ik].iloc[0]
        c_row = ced_df[ced_df['inchi_key']==ik].iloc[0]
        print(f"  ASMS:{a_row['EDS_Number']} / Cedilla:{c_row['Molecule Name']} | AS={a_row['AS ratio']} | pIC50={c_row['pIC50']}")

# Step 3: Near-matches by first 14 chars of InChIKey (ignore stereo layer)
asms_ikey14 = {ik[:14]: ik for ik in asms_ikeys if ik}
ced_ikey14  = {ik[:14]: ik for ik in ced_ikeys  if ik}
near_overlap = set(asms_ikey14.keys()) & set(ced_ikey14.keys())
print(f"\nNear-matches (first 14 chars, ignores stereochemistry): {len(near_overlap)}")
if near_overlap:
    for k14 in near_overlap:
        a_row = asms_df[asms_df['inchi_key'].str.startswith(k14)].iloc[0]
        c_row = ced_df[ced_df['inchi_key'].str.startswith(k14)].iloc[0]
        print(f"  ASMS:{a_row['EDS_Number']} / Cedilla:{c_row['Molecule Name']} | AS={a_row['AS ratio']} | pIC50={c_row.get('pIC50','N/A')}")
