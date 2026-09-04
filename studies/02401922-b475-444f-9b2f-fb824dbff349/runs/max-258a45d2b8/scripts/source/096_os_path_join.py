
import subprocess, os
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
results_dir = os.path.join(wd, "docking_results")
receptor_pdb = os.path.join(wd, "receptor_ab.pdb")

# Load receptor atoms for contact analysis
rec_atoms = []  # (resname, resnum, chain, atomname, x, y, z)
with open(receptor_pdb) as f:
    for line in f:
        if line.startswith(('ATOM','HETATM')) and line[17:20].strip() != 'HOH':
            try:
                chain = line[21]
                resnum = int(line[22:26])
                resname = line[17:20].strip()
                atomname = line[12:16].strip()
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                rec_atoms.append((resname, resnum, chain, atomname, x, y, z))
            except: pass

rec_arr = np.array([(x,y,z) for *_, x,y,z in rec_atoms])
print(f"Receptor atoms loaded: {len(rec_atoms)}")

def parse_pdbqt_pose1(pdbqt_path):
    """Extract MODEL 1 atom coordinates from PDBQT."""
    coords = []
    in_model1 = False
    with open(pdbqt_path) as f:
        for line in f:
            if line.startswith('MODEL'):
                if in_model1: break
                in_model1 = True
                continue
            if line.startswith('ENDMDL') and in_model1:
                break
            if in_model1 and line.startswith(('ATOM','HETATM')):
                try:
                    x=float(line[30:38]); y=float(line[38:46]); z=float(line[46:54])
                    aname = line[12:16].strip()
                    if not aname.startswith('H'):  # heavy atoms only
                        coords.append((aname,x,y,z))
                except: pass
    return coords

def get_contacts(lig_coords, cutoff=4.5):
    """Return receptor residues within cutoff of any ligand heavy atom."""
    lig_arr = np.array([(x,y,z) for _,x,y,z in lig_coords])
    contacts = {}
    for li, (la, lx, ly, lz) in enumerate(lig_coords):
        diffs = rec_arr - np.array([lx, ly, lz])
        dists = np.sqrt((diffs**2).sum(axis=1))
        close = np.where(dists <= cutoff)[0]
        for idx in close:
            resname, resnum, chain, atomname, rx, ry, rz = rec_atoms[idx]
            dist = dists[idx]
            key = (chain, resnum, resname, atomname)
            if key not in contacts or contacts[key] > dist:
                contacts[key] = dist
    # Sort by distance
    return sorted(contacts.items(), key=lambda x: x[1])

# Analyze top 10 + CTX-1017233
top11_info = [
    ('CTX-1020521', 61, -12.979),
    ('CTX-1020520', 62, -12.948),
    ('CTX-1020810', 12, -12.844),
    ('CTX-1019660', 77, -12.819),
    ('CTX-1020458', 68, -12.797),
    ('CTX-1019813', 74, -12.768),
    ('CTX-1020882',  4, -12.706),
    ('CTX-1020555', 59, -12.698),
    ('CTX-1020816', 10, -12.594),
    ('CTX-1020751', 27, -12.551),
    ('CTX-1017233', 84, -12.449),
]

for name, lig_n, score in top11_info:
    pdbqt_out = os.path.join(results_dir, f"lig{lig_n}_out.pdbqt")
    lig_coords = parse_pdbqt_pose1(pdbqt_out)
    contacts = get_contacts(lig_coords, cutoff=3.5)  # tight contacts ≤3.5Å
    close5 = [(f"{c},{r}{n}", f"{d:.2f}Å") for (c,n,r,a),d in contacts[:6]]
    print(f"\n{name}  (Vina={score})")
    for label, dist in close5:
        print(f"  {label}  {dist}")
