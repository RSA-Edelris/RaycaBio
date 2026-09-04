
import numpy as np, os

WORKDIR = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc'
PDB_IN  = '/home/ubuntu/rayca-artifacts/db61873ef1ff7fa5e8bf27d4/files/9C56.pdb'
RECEPTOR_PDB = os.path.join(WORKDIR, '9C56_receptor.pdb')

# --- Parse FRJ ligand atoms from original PDB ---
frj_atoms, receptor_atoms = [], []

with open(PDB_IN) as f:
    for line in f:
        if line.startswith('HETATM') and 'FRJ' in line:
            try:
                x,y,z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                name = line[12:16].strip()
                frj_atoms.append((name, x, y, z))
            except: pass
        elif line.startswith('ATOM'):
            try:
                x,y,z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                res  = line[17:20].strip()
                rnum = int(line[22:26].strip())
                aname= line[12:16].strip()
                receptor_atoms.append((aname, res, rnum, x, y, z))
            except: pass

frj_coords = np.array([[a[1],a[2],a[3]] for a in frj_atoms])
rec_coords  = np.array([[a[3],a[4],a[5]] for a in receptor_atoms])

cx, cy, cz = frj_coords.mean(axis=0)
print(f"FRJ centroid: {cx:.2f}, {cy:.2f}, {cz:.2f}")
print(f"FRJ atoms: {len(frj_atoms)}")

# --- Find pocket residues within 5 Å of any FRJ heavy atom ---
pocket_residues = set()
for fa in frj_coords:
    dists = np.linalg.norm(rec_coords - fa, axis=1)
    close = np.where(dists < 5.0)[0]
    for i in close:
        rnum = receptor_atoms[i][2]
        rname= receptor_atoms[i][1]
        pocket_residues.add((rnum, rname))

pocket_residues = sorted(pocket_residues)
print(f"\nPocket residues within 5Å of FRJ ({len(pocket_residues)} residues):")
for r in pocket_residues:
    print(f"  {r[1]} {r[0]}")

# --- Pocket bounding box for docking ---
pad = 8.0  # Å padding around FRJ extent
x_ext = frj_coords[:,0].max() - frj_coords[:,0].min()
y_ext = frj_coords[:,1].max() - frj_coords[:,1].min()
z_ext = frj_coords[:,2].max() - frj_coords[:,2].min()
width  = x_ext + pad
height = y_ext + pad
depth  = z_ext + pad
print(f"\nDocking box:")
print(f"  Center: ({cx:.2f}, {cy:.2f}, {cz:.2f})")
print(f"  Dimensions: {width:.1f} x {height:.1f} x {depth:.1f} Å")
