
# Check actual field names in the SDF
sdf_path = "/home/ubuntu/rayca-artifacts/9b531d029532706a25e7a959/files/HTE_Edelris.sdf"
with open(sdf_path) as f:
    content = f.read()

# Find all field names
import re
fields = sorted(set(re.findall(r'>  <([^>]+)>', content)))
print("Field names:", fields)

# Show first entry fully
entries_raw = content.split('$$$$')
print("\nFirst entry:")
print(entries_raw[0][:500])
