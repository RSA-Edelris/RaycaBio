
MD = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d/md_prep'

lines_in = open(f"{MD}/protein_hid.pdb").readlines()
lines_out = []
for line in lines_in:
    # Drop only the spurious TER between ARG B 359 and ALA B 360
    if line.startswith("TER") and "ARG B 359" in line:
        continue
    lines_out.append(line)
with open(f"{MD}/protein_fixed.pdb", "w") as fh:
    fh.writelines(lines_out)
print(f"Written {len(lines_out)} lines (removed 1 TER)")

# Verify chain B is now contiguous
ters = [(i+1, l.strip()) for i, l in enumerate(lines_out) if l.startswith("TER")]
print("TER records:")
for lineno, t in ters:
    print(f"  line {lineno}: {t}")

# Check chain B residue continuity around the break point
atoms = [(i+1, l[21], int(l[22:26])) for i, l in enumerate(lines_out) if l.startswith("ATOM") and l[21]=='B']
# Find 358-360
local = [a for a in atoms if 357 <= a[2] <= 361]
for a in local[:10]:
    print(f"  chain {a[1]} res {a[2]}")
