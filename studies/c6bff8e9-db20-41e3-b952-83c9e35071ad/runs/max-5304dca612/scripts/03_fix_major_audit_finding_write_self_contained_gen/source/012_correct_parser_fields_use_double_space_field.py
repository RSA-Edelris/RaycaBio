
# Correct parser: fields use double-space ">  <FIELD>"
sdf_path = "/home/ubuntu/rayca-artifacts/9b531d029532706a25e7a959/files/HTE_Edelris.sdf"
with open(sdf_path) as f:
    lines = f.readlines()

entries = []
current = {}
i = 0
while i < len(lines):
    line = lines[i].rstrip()
    if line == '>  <MOL_NAME>':
        current['name'] = lines[i+1].strip()
    elif line == '>  <Role>':
        current['role'] = lines[i+1].strip()
    elif line == '>  <CAS_NUMBER>':
        current['cas'] = lines[i+1].strip()
    elif line == '$$$$':
        if current:
            entries.append(dict(current))
        current = {}
    i += 1

from collections import defaultdict
by_role = defaultdict(list)
for e in entries:
    by_role[e.get('role','?')].append(e)

for role in sorted(by_role):
    print(f"\n{'='*55}\n{role} ({len(by_role[role])})")
    for e in by_role[role]:
        print(f"  {e.get('name','?'):<42} {e.get('cas','?')}")
