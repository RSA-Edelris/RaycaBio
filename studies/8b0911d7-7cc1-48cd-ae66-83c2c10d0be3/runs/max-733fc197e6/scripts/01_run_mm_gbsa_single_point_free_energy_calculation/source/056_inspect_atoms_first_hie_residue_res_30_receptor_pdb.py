
# Inspect atoms in the first HIE residue (res 30) from the receptor PDB
RECEPTOR_PDB = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/9C56_receptor.pdb'

hie_res = {}
with open(RECEPTOR_PDB) as f:
    for line in f:
        if (line.startswith('ATOM') or line.startswith('HETATM')):
            resname = line[17:20].strip()
            resnum  = line[22:26].strip()
            aname   = line[12:16].strip()
            if resname == 'HIE':
                key = resnum
                hie_res.setdefault(key, []).append(aname)

# Show atom names for each HIE residue
for k, v in sorted(hie_res.items(), key=lambda x: int(x[0]))[:3]:
    has_hd1 = 'HD1' in v
    has_he2 = 'HE2' in v
    print(f"  HIE resnum={k}: HD1={has_hd1}, HE2={has_he2}  atoms={v}")
    
print(f"\nTotal HIE residues: {len(hie_res)}")
all_hd1 = [k for k,v in hie_res.items() if 'HD1' in v]
all_he2 = [k for k,v in hie_res.items() if 'HE2' in v]
print(f"HIE with HD1: {all_hd1}")
print(f"HIE with HE2: {all_he2}")
