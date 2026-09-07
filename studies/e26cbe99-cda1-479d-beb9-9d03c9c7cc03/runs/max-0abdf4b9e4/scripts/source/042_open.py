
import numpy as np

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'

with open(f'{WD}/complex_EDS01806218_ent2.pdb') as f:
    lines = f.readlines()

lig_coords = []
prot_atoms = []

for line in lines:
    rec = line[:6].strip()
    if len(line) < 54:
        continue
    try:
        x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
    except:
        continue
    chain = line[21]
    resi = int(line[22:26].strip())
    resn = line[17:20].strip()
    aname = line[12:16].strip()
    
    if chain == 'Z':
        lig_coords.append((x, y, z))
    elif rec == 'ATOM':
        prot_atoms.append((chain, resi, resn, aname, x, y, z))

lig_arr = np.array(lig_coords)

pocket_residues = set()
for (chain, resi, resn, aname, x, y, z) in prot_atoms:
    dists = np.sqrt(np.sum((lig_arr - np.array([x, y, z]))**2, axis=1))
    if dists.min() < 4.5:
        pocket_residues.add((chain, resi, resn))

print("Pocket residues within 4.5A:")
for r in sorted(pocket_residues, key=lambda x: x[1]):
    print(f"  {r[2]:3s} {r[1]:4d}")
