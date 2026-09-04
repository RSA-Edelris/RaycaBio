
wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'

# Show all atoms of chain C residue 566
print("=== Chain C atoms ===")
with open(f'{wd}/receptor_noh2.pdb') as f:
    for line in f:
        if line.startswith(('ATOM','HETATM')) and line[21] == 'C':
            print(repr(line.rstrip()))

# Also count waters
print("\n=== HOH / WAT atoms ===")
hoh_count = 0
with open(f'{wd}/receptor_noh2.pdb') as f:
    for line in f:
        if line.startswith(('ATOM','HETATM')):
            rname = line[17:20].strip()
            if rname in ('HOH','WAT','TIP'):
                hoh_count += 1
print(f"Water atoms: {hoh_count}")

# Show TER records
print("\n=== TER records ===")
with open(f'{wd}/receptor_noh2.pdb') as f:
    for line in f:
        if line.startswith('TER'):
            print(repr(line.rstrip()))
