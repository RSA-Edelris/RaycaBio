
# Scan all records quickly (no RDKit yet) to understand the full field inventory
# and all unique values in key fields

from collections import defaultdict, Counter

SDF_PATH = '/home/ubuntu/rayca-artifacts/70045e3ed20155a95e1cafc3/files/ASMS.sdf'

records = []
current = {}
current_field = None
in_mol = True  # start in mol block

with open(SDF_PATH, 'r', errors='replace') as f:
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('$$$$'):
            records.append(current)
            current = {}
            current_field = None
            in_mol = True
        elif line.startswith('>') and '<' in line:
            # field header
            in_mol = False
            field = line.split('<')[1].split('>')[0].strip()
            current_field = field
            current[field] = ''
        elif not in_mol and current_field:
            if line.strip():  # non-empty data line
                current[current_field] = (current.get(current_field, '') + line.strip() + ' ').strip()
        elif line.strip() == 'M  END':
            in_mol = False

print(f"Total records parsed: {len(records)}")
print(f"\nAll field names found:")
all_fields = Counter()
for r in records:
    for k in r:
        all_fields[k] += 1
for f, c in sorted(all_fields.items()):
    print(f"  '{f}' : {c} records")
