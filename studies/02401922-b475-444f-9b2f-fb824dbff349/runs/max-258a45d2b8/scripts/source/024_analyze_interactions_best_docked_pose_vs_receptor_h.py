
# Analyze interactions for best docked pose vs receptor
# H-bonds: donor-acceptor distance < 3.5A, angle > 120°
# Hydrophobic: C-C distance < 4.5A

import numpy as np

def parse_atoms_pdb(path, chain_filter=None):
    atoms = []
    with open(path) as f:
        for line in f:
            if not line.startswith(('ATOM','HETATM')): continue
            try:
                name   = line[12:16].strip()
                resname= line[17:20].strip()
                chain  = line[21]
                resnum = line[22:26].strip()
                x,y,z  = float(line[30:38]),float(line[38:46]),float(line[46:54])
                elem   = line[76:78].strip() if len(line)>=78 else name[0]
                atoms.append({'name':name,'resname':resname,'chain':chain,
                              'resnum':resnum,'x':x,'y':y,'z':z,'elem':elem})
            except: pass
    return atoms

# Parse prepared receptor (has H) and best pose
rec_atoms  = parse_atoms_pdb('receptor_prepared.pdb')
lig_atoms  = parse_atoms_pdb('best_pose.pdb')

# Define H-bond acceptors/donors by element/name
def is_hbond_heavy(a):
    return a['elem'] in ('N','O','F','S')

def is_hydrophobic(a):
    return a['elem'] == 'C' and a['resname'] not in ('HOH',)

# Find contacts between ligand and receptor heavy atoms
contacts = []
for la in lig_atoms:
    if la['elem'] == 'H': continue
    for ra in rec_atoms:
        if ra['elem'] == 'H': continue
        d = ((la['x']-ra['x'])**2+(la['y']-ra['y'])**2+(la['z']-ra['z'])**2)**0.5
        if d < 4.5:
            contacts.append({
                'lig_atom': la['name'], 'lig_elem': la['elem'],
                'rec_res': f"{ra['chain']}:{ra['resname']}{ra['resnum']}",
                'rec_atom': ra['name'], 'rec_elem': ra['elem'],
                'dist': round(d, 2)
            })

# H-bonds: both heavy atoms N or O, dist < 3.5
hbonds = [c for c in contacts if is_hbond_heavy({'elem':c['lig_elem']})
          and is_hbond_heavy({'elem':c['rec_elem']}) and c['dist'] < 3.5]

# Hydrophobic: both C, dist < 4.5
hydro = [c for c in contacts if c['lig_elem']=='C' and c['rec_elem']=='C' and c['dist']<4.5]

print("=== H-BOND CONTACTS (N/O dist < 3.5 Å) ===")
seen_hb = set()
for h in sorted(hbonds, key=lambda x: x['dist']):
    key = (h['lig_atom'], h['rec_res'], h['rec_atom'])
    if key not in seen_hb:
        seen_hb.add(key)
        print(f"  {h['lig_atom']:6s} -- {h['rec_res']:15s} {h['rec_atom']:6s}  {h['dist']:.2f} Å")

print(f"\n=== HYDROPHOBIC CONTACTS (C-C < 4.5 Å) — unique residues ===")
hyd_res = sorted(set(c['rec_res'] for c in hydro))
for r in hyd_res:
    print(f"  {r}")
