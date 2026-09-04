
wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'

# Show unique residue names and first/last residues of each chain
chains = {}
with open(f'{wd}/receptor_noh2.pdb') as f:
    for line in f:
        if line.startswith(('ATOM','HETATM')):
            chain = line[21]
            resnum = int(line[22:26])
            resname = line[17:20].strip()
            aname = line[12:16].strip()
            if chain not in chains:
                chains[chain] = {'first': (resnum, resname), 'last': (resnum, resname), 'names': set()}
            chains[chain]['last'] = (resnum, resname)
            chains[chain]['names'].add(resname)

for c, d in chains.items():
    print(f"Chain {c}: first={d['first']}, last={d['last']}")
    print(f"  unique residues: {sorted(d['names'])[:15]}...")

# Also check residue 566 in the combined numbering (from error)
# Count residues
res_list = []
seen = set()
with open(f'{wd}/receptor_noh2.pdb') as f:
    for line in f:
        if line.startswith(('ATOM','HETATM')):
            chain = line[21]
            resnum = int(line[22:26])
            key = (chain, resnum)
            if key not in seen:
                seen.add(key)
                res_list.append((len(res_list)+1, chain, int(line[22:26]), line[17:20].strip()))

print(f"\nTotal residues: {len(res_list)}")
# Show around residue 566
for idx, ch, rn, rname in res_list[560:575]:
    print(f"  seq#{idx}: chain={ch} resnum={rn} name={rname}")
