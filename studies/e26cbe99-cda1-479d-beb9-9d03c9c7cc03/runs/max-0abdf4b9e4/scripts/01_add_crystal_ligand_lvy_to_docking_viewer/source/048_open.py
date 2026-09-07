
WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'

with open(f'{WD}/PB-20260903-4CI2_raw.pdb') as f:
    raw_lines = f.readlines()

lvy_serials = set()
lvy_lines = []
for line in raw_lines:
    rec = line[:6].strip()
    if rec == 'HETATM' and line[17:20].strip() == 'LVY':
        lvy_lines.append(line)
        lvy_serials.add(int(line[6:11].strip()))

conect_lines = []
for line in raw_lines:
    if line.startswith('CONECT'):
        parts = line[6:].split()
        if any(int(p) in lvy_serials for p in parts if p.isdigit()):
            conect_lines.append(line)

lvy_pdb = ''.join(lvy_lines + conect_lines) + 'END\n'

# Save for verification
with open(f'{WD}/crystal_lvy.pdb', 'w') as f:
    f.write(lvy_pdb)

print(f"LVY atoms  : {len(lvy_lines)}")
print(f"CONECTs    : {len(conect_lines)}")
print("\nSample HETATM:")
print(lvy_lines[0].rstrip())
print("\nSample CONECT:")
print(conect_lines[0].rstrip() if conect_lines else "(none)")
