
import numpy as np

# Parse PDB manually - extract all ATOM/HETATM records
pdb_path = "/home/ubuntu/rayca-artifacts/c2db8d53fb710fe21c5fee43/files/CRBN.pdb"

atoms = []
with open(pdb_path) as f:
    for line in f:
        rec = line[:6].strip()
        if rec not in ("ATOM", "HETATM"):
            continue
        try:
            serial = int(line[6:11])
            name   = line[12:16].strip()
            resname= line[17:20].strip()
            chain  = line[21].strip()
            resseq = int(line[22:26])
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            atoms.append(dict(rec=rec, serial=serial, name=name,
                              resname=resname, chain=chain, resseq=resseq,
                              x=x, y=y, z=z))
        except:
            pass

print(f"Total atoms parsed: {len(atoms)}")

# Separate protein, LVY ligand, ZN
protein = [a for a in atoms if a['rec']=='ATOM']
lvy     = [a for a in atoms if a['resname']=='LVY']
zn_atm  = [a for a in atoms if a['resname']=='ZN']
water   = [a for a in atoms if a['resname']=='HOH']

print(f"Protein atoms: {len(protein)}")
print(f"LVY atoms: {len(lvy)}")
print(f"ZN atoms: {len(zn_atm)}")

# LVY centroid
lvy_xyz = np.array([[a['x'],a['y'],a['z']] for a in lvy])
lvy_cen = lvy_xyz.mean(axis=0)
print(f"\nLVY centroid: {lvy_cen}")

# ZN position
zn_xyz = np.array([[a['x'],a['y'],a['z']] for a in zn_atm])
print(f"ZN position:  {zn_xyz[0]}")
