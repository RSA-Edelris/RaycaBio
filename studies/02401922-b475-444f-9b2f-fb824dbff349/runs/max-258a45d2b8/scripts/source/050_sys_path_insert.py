
import sys, numpy as np
sys.path.insert(0, '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/lib/python3.11/site-packages')
from rdkit import Chem

# Load receptor heavy atoms
rec_atoms = []
with open('/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a/receptor_noh2.pdb') as f:
    for line in f:
        if line.startswith(('ATOM','HETATM')) and line[17:20].strip() not in ('HOH','LIG'):
            try:
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                chain = line[21].strip()
                resname = line[17:20].strip()
                resnum = int(line[22:26])
                atname = line[12:16].strip()
                rec_atoms.append({'coord': np.array([x,y,z]), 'chain': chain, 
                                  'resname': resname, 'resnum': resnum, 'atname': atname})
            except: pass

print(f"Receptor atoms: {len(rec_atoms)}")

# Load best ligand pose (all atoms including H)
suppl = Chem.SDMolSupplier('/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a/docked_poses_all5.sdf', removeHs=False)
mol = next(iter(suppl))
conf = mol.GetConformer()
lig_coords = conf.GetPositions()
lig_atoms = [(mol.GetAtomWithIdx(i).GetAtomicNum(), lig_coords[i]) for i in range(mol.GetNumAtoms())]

# Find close contacts (4.5 Å) between ligand heavy atoms and receptor
contacts = {}
H_DONORS = {'N', 'O', 'S'}  # potential H-bond donors/acceptors
for lat, lcoord in lig_atoms:
    if lat == 1: continue  # skip H
    for ratom in rec_atoms:
        d = np.linalg.norm(lcoord - ratom['coord'])
        if d < 4.5:
            key = (ratom['chain'], ratom['resname'], ratom['resnum'])
            if key not in contacts or contacts[key]['dist'] > d:
                contacts[key] = {'dist': d, 'atname': ratom['atname']}

# Sort by distance
sorted_contacts = sorted(contacts.items(), key=lambda x: x[1]['dist'])
print("\nAll contacts within 4.5 Å (sorted by distance):")
for (chain, resname, resnum), info in sorted_contacts[:30]:
    print(f"  Chain {chain} {resname}{resnum} {info['atname']:6s} {info['dist']:.2f} Å")
