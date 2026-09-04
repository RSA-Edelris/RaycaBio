
wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'

# Write receptor with only chains A and B (drop chain C stray fragment)
kept, dropped = [], 0
with open(f'{wd}/receptor_noh2.pdb') as f:
    lines = f.readlines()

out = []
ter_count = 0
for line in lines:
    if line.startswith(('ATOM','HETATM')):
        if line[21] == 'C':
            dropped += 1
            continue
    if line.startswith('TER'):
        ter_count += 1
        if ter_count <= 2:     # keep only A/B TER
            out.append(line)
        continue
    out.append(line)

with open(f'{wd}/receptor_ab.pdb', 'w') as f:
    f.writelines(out)

print(f"Dropped {dropped} chain-C atoms")
print(f"TER records kept: 2 of {ter_count}")
# Verify 
chains_out = set()
n_atoms = 0
with open(f'{wd}/receptor_ab.pdb') as f:
    for line in f:
        if line.startswith(('ATOM','HETATM')):
            chains_out.add(line[21])
            n_atoms += 1
print(f"Chains: {chains_out}, atoms: {n_atoms}")
