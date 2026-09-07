
import numpy as np, json, os

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'

compounds = ['EDS01357518_ent1','EDS01357518_ent2','EDS01806218_ent1','EDS01806218_ent2','EDS01889984']

# Parse trimmed receptor atoms once
with open(f'{WD}/PB-20260903-4CI2_receptor_trimmed_fixed.pdb') as f:
    rec_lines = f.readlines()

prot_atoms = []
for line in rec_lines:
    if line[:4] != 'ATOM': continue
    if len(line) < 54: continue
    try:
        x,y,z = float(line[30:38]), float(line[38:46]), float(line[46:54])
    except: continue
    resi = int(line[22:26].strip())
    resn = line[17:20].strip()
    aname = line[12:16].strip()
    prot_atoms.append((resi, resn, aname, x, y, z))

# For each compound, get best pose (pose 0) from poses SDF and find contacts ≤4.0 Å
from rdkit import Chem

contacts = {}
for cid in compounds:
    with open(f'{WD}/poses_{cid}.sdf') as f:
        content = f.read()
    blocks = [b.strip() for b in content.split('$$$$') if b.strip()]
    mol = Chem.MolFromMolBlock(blocks[0], removeHs=False)
    if mol is None:
        contacts[cid] = []
        continue
    conf = mol.GetConformer()
    lig_coords = np.array([[conf.GetAtomPosition(i).x,
                            conf.GetAtomPosition(i).y,
                            conf.GetAtomPosition(i).z]
                           for i in range(mol.GetNumAtoms())])
    
    nearby = {}
    for (resi, resn, aname, x, y, z) in prot_atoms:
        d = np.min(np.linalg.norm(lig_coords - np.array([x,y,z]), axis=1))
        if d <= 4.0:
            key = (resi, resn)
            if key not in nearby or d < nearby[key]:
                nearby[key] = d
    contacts[cid] = sorted(nearby.keys(), key=lambda k: k[0])

# Also compute crystal LVY contacts
with open(f'{WD}/crystal_lvy.pdb') as f:
    lvy_lines = [l for l in f.readlines() if l.startswith('HETATM')]
lvy_coords = np.array([[float(l[30:38]), float(l[38:46]), float(l[46:54])] for l in lvy_lines])

lvy_nearby = {}
for (resi, resn, aname, x, y, z) in prot_atoms:
    d = np.min(np.linalg.norm(lvy_coords - np.array([x,y,z]), axis=1))
    if d <= 4.0:
        key = (resi, resn)
        if key not in lvy_nearby or d < lvy_nearby[key]:
            lvy_nearby[key] = d
crystal_contacts = sorted(lvy_nearby.keys(), key=lambda k: k[0])

print("Crystal LVY contacts:", [(r,n) for r,n in crystal_contacts])
print()
for cid in compounds:
    print(f"{cid}: {contacts[cid]}")
