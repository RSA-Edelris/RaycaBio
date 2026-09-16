
# Inspect SDF field names without parsing chemistry
with open('/home/ubuntu/rayca-artifacts/70045e3ed20155a95e1cafc3/files/ASMS.sdf', 'r', errors='replace') as f:
    lines = []
    for i, line in enumerate(f):
        lines.append(line.rstrip())
        if i >= 300:
            break

print("=== FIRST 300 LINES ===")
for i, l in enumerate(lines):
    print(f"{i:3d}: {l}")
